from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from Autism.constants import APP_HOST, APP_PORT
from Autism.pipline.prediction_pipline import AutismData, AutismClassifier
from Autism.pipline.training_pipline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FIELDS = [f"A{i}_Score" for i in range(1, 11)] + [
    "age", "ethnicity", "jaundice", "austim", "contry_of_res"
]


class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        for name in FIELDS:
            setattr(self, name, None)

    async def get_autism_data(self):
        form = await self.request.form()
        for name in FIELDS:
            setattr(self, name, form.get(name))


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse(
        "autism.html", {"request": request, "context": "Rendering"}
    )


@app.get("/train")
async def trainRouteClient():
    try:
        TrainPipeline().run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_autism_data()

        autism_data = AutismData(**{name: getattr(form, name) for name in FIELDS})
        autism_df = autism_data.get_autism_input_data_frame()

        value = AutismClassifier().predict(dataframe=autism_df)[0]

        status = "Positive: ASD traits likely" if value == 1 else "Negative: ASD traits unlikely"

        return templates.TemplateResponse(
            "autism.html", {"request": request, "context": status}
        )
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
