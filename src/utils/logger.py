import logging
import json
from datetime import datetime
import sys

class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage()
        }
        if hasattr(record, 'extra'):
            log_record.update(record.extra)
        return json.dumps(log_record)

def setup_logger(name='credit_card_api', log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if logger.handlers:
        logger.handlers.clear()
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    formatter = CustomJsonFormatter()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def log_request(logger, request_data, response_data, duration_ms, model_version):
    logger.info(
        f'API Request processed',
        extra={
            'endpoint': '/predict',
            'model_version': model_version,
            'duration_ms': duration_ms,
            'prediction': response_data.get('prediction'),
            'probability': response_data.get('probability'),
            'request_size': len(str(request_data))
        }
    )

def log_error(logger, error, endpoint='/predict'):
    logger.error(
        f'API Error: {str(error)}',
        extra={
            'endpoint': endpoint,
            'error_type': type(error).__name__,
            'error_message': str(error)
        }
    )