#!pip install diffusers --upgrade
#!pip install torch
#!pip install accelerate
#!pip install -U transformers
#!pip install safetensors
#!pip install -U peft

#import torch
#from diffusers import DiffusionPipeline
#import peft

#https://djangoforbeginners.com/hello-world/

#venv = .venv
#python -m venv .venv
#.venv\Scripts\Activate.ps1
#(.venv) $ python -m pip install django~=4.2.0
#(.venv) $ python -m pip install black


import gc

def flush():
    gc.collect()
    #torch.cuda.empty_cache()