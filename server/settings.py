from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.', '.env')
load_dotenv(dotenv_path = env_path)
USER = os.getenv('USER')
DB_PASS = os.getenv('DB_PASS')
