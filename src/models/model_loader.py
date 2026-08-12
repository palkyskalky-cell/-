import joblib
import pickle
import os
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    _models = {}
    
    @classmethod
    def load_model(cls, model_path: str) -> Any:
        if model_path in cls._models:
            logger.info(f"Returning cached model from {model_path}")
            return cls._models[model_path]
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            try:
                model = joblib.load(model_path)
                logger.info(f"Model loaded with joblib from {model_path}")
            except Exception:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"Model loaded with pickle from {model_path}")
            
            cls._models[model_path] = model
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    @classmethod
    def clear_cache(cls):
        cls._models.clear()
        logger.info("Model cache cleared")