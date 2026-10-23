from pandas import DataFrame

class AutismModel:
    def __init__(self, preprocessing_object, trained_model_object, threshold: float = 0.30):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        self.threshold = threshold

    def predict(self, dataframe: DataFrame):
        transformed = self.preprocessing_object.transform(dataframe)
        proba = self.trained_model_object.predict_proba(transformed)[:, 1]
        return (proba >= self.threshold).astype(int)
