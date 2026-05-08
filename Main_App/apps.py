import os
import pandas as pd
import faiss
from django.apps import AppConfig
from django.conf import settings

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Added this for safety
    name = 'Main_App'
    
    _df = None
    _ai_brain = None # Renamed from _model
    _index = None

    @classmethod
    def get_ai_df(cls): # Renamed from get_df
        if cls._df is None:
            path = os.path.join(settings.BASE_DIR, 'Main_App', 'ml_models', 'df.csv')
            cls._df = pd.read_csv(path)
        return cls._df

    @classmethod
    def get_ai_model(cls): # Renamed from get_model to avoid the ERROR
        if cls._ai_brain is None:
            from sentence_transformers import SentenceTransformer
            cls._ai_brain = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._ai_brain

    @classmethod
    def get_ai_faiss(cls): # Renamed from get_faiss
        if cls._index is None:
            path = os.path.join(settings.BASE_DIR, 'Main_App', 'ml_models', 'faiss_index.bin')
            cls._index = faiss.read_index(path)
        return cls._index

    def ready(self):
        print("🚀 Django Server Started Successfully")