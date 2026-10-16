#from Autism.logger import logging
#from Autism.exception import AutismException
#import sys

#logging.info("Welcome")


#try:
 #   a=2/0
#except Exception as e:
#    raise AutismException(e,sys)

#import os 
#mongo_db_url = os.getenv("mangoDB")
#print(mongo_db_url)

from Autism.pipline.training_pipline import TrainPipeline
obj=TrainPipeline()
obj.run_pipeline()