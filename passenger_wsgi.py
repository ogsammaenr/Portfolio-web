import sys
import os

# Proje dizinini Python path'ine ekliyoruz
sys.path.insert(0, os.path.dirname(__file__))

from a2wsgi import ASGIMiddleware
from main import app  # main.py içindeki 'app = FastAPI()' nesneniz

# Phusion Passenger bu 'application' değişkenini arar
application = ASGIMiddleware(app)
