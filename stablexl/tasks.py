from celery import shared_task
import logging
import torch
import accelerate
from diffusers import StableDiffusionPipeline
import gc
import os
logger = logging.getLogger(__name__)

localmodel:str = 'static/stable1-5/'
modelurl:str = "runwayml/stable-diffusion-v1-5" #https://huggingface.co/runwayml/stable-diffusion-v1-5

def flush():
    gc.collect()
    torch.cuda.empty_cache()

def testfolder():
    try:
        contents = os.listdir(localmodel)
        logging.info(f"Contents of the directory '{localmodel}':")
        for item in contents:
            logging.info(item)
    except FileNotFoundError as e:
        logging.error(f"Directory not found: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")



def rungeneration():
    model_id:str = localmodel
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
    pipe.enable_freeu(s1=0.9, s2=0.2, b1=1.5, b2=1.6) # https://huggingface.co/docs/diffusers/main/en/using-diffusers/image_quality
    pipe.enable_model_cpu_offload()



@shared_task
def add(x, y):
    return x + y

@shared_task
def generate(prompt):
    logger.info(prompt)

@shared_task
def log_message_task():
    logger.info('This is a log message from the Celery task.')

@shared_task
def testfolder_task():
    logger.info('Testing your folder.')
    current_path = os.getcwd()
    logger.info('Current Directory:'+current_path)
    testfolder()