from celery import shared_task
import logging
import torch
import accelerate
from diffusers import StableDiffusionPipeline
import gc
import os
from PIL import Image
import random
import string
logger = logging.getLogger(__name__)

localmodel:str = 'static/stable1-5/'
modelurl:str = "runwayml/stable-diffusion-v1-5" #https://huggingface.co/runwayml/stable-diffusion-v1-5

#try to free up model from memory
def flush():
    gc.collect()
    torch.cuda.empty_cache()
    
    
#generates a string to append if the file name already exists
def generate_random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
    
@shared_task
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


@shared_task
def rungeneration(prompt:str="A cat on a armchair high quality hd"):
    logger.info("Prompt is:"+prompt)
    model_id:str = localmodel
    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
        #pipe.enable_freeu(s1=0.9, s2=0.2, b1=1.5, b2=1.6) # https://huggingface.co/docs/diffusers/main/en/using-diffusers/image_quality
        pipe.enable_model_cpu_offload()
        
        image = pipe(
            prompt,
            negative_prompt="",
            num_inference_steps=56,
            guidance_scale=7.0,
            height=512,
            width=512,
        ).images[0]
        
        directory = 'media/image'
        base_filename:str = f"{prompt[:10].replace(' ', '_')}"
        image_path = os.path.join(directory,f"{base_filename}.png").replace("\\", "/")
        mediapath = os.path.join('image', f"{base_filename}.png").replace("\\", "/")
        while os.path.exists(image_path):
            random_suffix = generate_random_string()
            image_path = os.path.join(directory, f"{base_filename}_{random_suffix}.png").replace("\\", "/")
            mediapath = os.path.join('image', f"{base_filename}_{random_suffix}.png").replace("\\", "/")

        image.save(image_path)
        
        
        pipe.maybe_free_model_hooks()
        del pipe
        flush()
        
        return mediapath
    except Exception as e:
        logger.error(f"Error generating: {e}")
        pipe.maybe_free_model_hooks()
        del pipe
        flush()
        return None
        
    
    



@shared_task
def add(x, y):
    return x + y

@shared_task
def generatelog(prompt):
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