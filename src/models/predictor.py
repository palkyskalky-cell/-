import numpy as np
from typing import Dict, Any, Tuple, Optional
import logging
from src.models.model_loader import ModelLoader
from src.app.config import Config

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or Config.MODEL_PATH
        self.model = None
        self.feature_names = Config.FEATURE_NAMES
        self._load_model()
    
    def _load_model(self):
        try:
            self.model = ModelLoader.load_model(self.model_path)
            logger.info(f"Predictor initialized with model: {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {str(e)}")
            raise
    
    def predict(self, features: Dict[str, Any]) -> Tuple[int, float]:
        try:
            feature_vector = self._prepare_features(features)
            prediction = self.model.predict(feature_vector)[0]
            proba = self.model.predict_proba(feature_vector)[0]
            probability = proba[1]
            return int(prediction), float(probability)
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def _prepare_features(self, features: Dict[str, Any]) -> np.ndarray:
        missing_features = set(self.feature_names) - set(features.keys())
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
        feature_vector = [features.get(name, 0) for name in self.feature_names]
        return np.array(feature_vector).reshape(1, -1)

_predictor_instance = None

def get_predictor(model_path: Optional[str] = None) -> Predictor:
    global _predictor_instance
    if _predictor_instance is None or model_path:
        _predictor_instance = Predictor(model_path)
    return _predictor_instance
