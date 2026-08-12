import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.app.config import config
from src.models.predictor import get_predictor
from src.utils.logger import setup_logger, log_request, log_error
from src.models.model_loader import ModelLoader

app = Flask(__name__)
CORS(app)

env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

logger = setup_logger(
    name='credit_card_api',
    log_level=getattr(logging, app.config['LOG_LEVEL'])
)

predictor = None
model_version = app.config['MODEL_VERSION']

def init_predictor():
    global predictor
    try:
        predictor = get_predictor(app.config['MODEL_PATH'])
        logger.info(f"Predictor initialized with model version: {model_version}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize predictor: {str(e)}")
        return False

with app.app_context():
    init_predictor()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        model_loaded = predictor is not None and predictor.model is not None
        response = {
            'status': 'healthy' if model_loaded else 'degraded',
            'model_loaded': model_loaded,
            'model_version': model_version,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'service': 'credit-card-default-prediction'
        }
        status_code = 200 if model_loaded else 503
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 400
        
        data = request.get_json()
        if 'features' not in data:
            return jsonify({
                'error': 'Missing "features" in request body',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }), 400
        
        features = data['features']
        
        # A/B TESTING LOGIC
        model_version_to_use = model_version
        predictor_to_use = predictor
        
        # Проверяем, включено ли A/B тестирование
        if app.config['AB_TEST_ENABLED']:
            requested_version = request.args.get('model_version')
            
            if requested_version == 'v2':
                try:
                    from src.models.predictor import get_predictor
                    predictor_to_use = get_predictor(app.config['TEST_MODEL_PATH'])
                    model_version_to_use = 'v2'
                    logger.info(f"Using test model v2 for A/B test")
                except Exception as e:
                    logger.error(f"Failed to load test model: {str(e)}")
                    predictor_to_use = predictor
                    model_version_to_use = model_version
            elif requested_version == 'v1':
                predictor_to_use = predictor
                model_version_to_use = 'v1'
                logger.info(f"Using control model v1")
            else:
                # Случайное распределение 50/50
                import random
                if random.random() < 0.5:
                    try:
                        from src.models.predictor import get_predictor
                        predictor_to_use = get_predictor(app.config['TEST_MODEL_PATH'])
                        model_version_to_use = 'v2'
                        logger.info(f"Randomly assigned to test model v2")
                    except Exception as e:
                        logger.error(f"Failed to load test model: {str(e)}")
                        predictor_to_use = predictor
                        model_version_to_use = model_version
                else:
                    predictor_to_use = predictor
                    model_version_to_use = 'v1'
                    logger.info(f"Randomly assigned to control model v1")
        
        if predictor_to_use is None:
            raise RuntimeError("Predictor not initialized")
        
        prediction, probability = predictor_to_use.predict(features)
        duration_ms = (time.time() - start_time) * 1000
        
        response = {
            'prediction': prediction,
            'probability': round(probability, 4),
            'model_version': model_version_to_use,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'processing_time_ms': round(duration_ms, 2)
        }
        
        log_request(logger, data, response, duration_ms, model_version_to_use)
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({
            'error': f'Invalid features: {str(e)}',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 400
    except Exception as e:
        log_error(logger, e, '/predict')
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )