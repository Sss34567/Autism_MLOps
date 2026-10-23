

from Autism.pipline.training_pipline import TrainPipeline
obj=TrainPipeline()
obj.run_pipeline()

"""from Autism.pipline.prediction_pipline import AutismData, AutismClassifier
d = AutismData(1,1,0,1,0,1,1,0,1,1, 25, "White-European", "no", "no", "United States")
print(AutismClassifier().predict(d.get_autism_input_data_frame()))
"""