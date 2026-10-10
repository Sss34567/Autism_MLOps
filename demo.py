from Autism.logger import logging
from Autism.exception import AutismException
import sys

logging.info("Welcome")


try:
    a=2/0
except Exception as e:
    raise AutismException(e,sys)