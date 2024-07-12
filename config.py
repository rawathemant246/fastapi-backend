import os 
import sys
import logging
import importlib.metadata
import pkgutil
import chromadb
from chromadb import Settings
from base64 import b64encode
from bs4 import BeautifulSoup
from typing import TypeVar, Generic, Union
from pydantic import BaseModel
from typing import Optional

from pathlib import Path
import json
import yaml
import markdown
import requests
import shutil

from secrets import token_bytes
from constants import ERROR_MESSAGES


BACKEND_DIR = Path(__file__).parent
BASE_DIR = BACKEND_DIR.parent

#print(BASE_DIR)
print(BACKEND_DIR)

try:
    from dotenv import load_dotenv, find_dotenv
    
    load_dotenv(find_dotenv(str(BASE_DIR/".env")))

except ImportError:
    print("dotenv not installed, skipping...")
    


log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

GLOBAL_LOG_LEVEL = os.environ.get("GLOBAL_LOG_LEVEL", "").upper()
if GLOBAL_LOG_LEVEL in log_levels:
    logging.basicConfig(stream=sys.stdout, level=GLOBAL_LOG_LEVEL)

else:
    GLOBAL_LOG_LEVEL="INFO"


log = logging.getLogger(__name__)

log.info(f"GLOBAL_LOG_LEVEL: {GLOBAL_LOG_LEVEL}")


log_sources = [
    
    "AUDIO"
    "DB"
]


SRC_LOG_LEVELS={}

for source in log_sources:
    log_env_var = source + "_LOG_LEVEL"
    
    SRC_LOG_LEVELS[source] = os.environ.get(log_env_var, "").upper()
    if SRC_LOG_LEVELS[source] not in log_levels:
        SRC_LOG_LEVELS[source]=GLOBAL_LOG_LEVEL
    
    log.info(f"{log_env_var}: {SRC_LOG_LEVELS[source]}")
    

log.setLevel(SRC_LOG_LEVELS["CONFIG"])

###
####
####
####
####
####
ENV=os.environ.get("ENV", "dev")

try

