import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_APP = os.getenv('FLASK_APP', 'src/app/api.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/model_v1.pkl')
    MODEL_VERSION = os.getenv('MODEL_VERSION', 'v1')
    
    AB_TEST_ENABLED = os.getenv('AB_TEST_ENABLED', 'False').lower() == 'true'
    CONTROL_MODEL_PATH = os.getenv('CONTROL_MODEL_PATH', 'models/model_v1.pkl')
    TEST_MODEL_PATH = os.getenv('TEST_MODEL_PATH', 'models/model_v2.pkl')
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')
    
    FEATURE_NAMES = [
        'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
        'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
        'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 
        'BILL_AMT5', 'BILL_AMT6',
        'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 
        'PAY_AMT5', 'PAY_AMT6'
    ]

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MODEL_PATH = 'models/test_model.pkl'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}