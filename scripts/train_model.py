import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data():
    logger.info("Loading data...")
    df = pd.read_csv('data/raw/default_credit_card_clients.csv')
    
    # Удаляем ПЕРВЫЙ столбец (ID)
    df = df.drop(df.columns[0], axis=1)
    
    target = df.columns[-1]
    y = df[target].values
    X = df.drop(columns=[target]).values
    logger.info(f"Data shape: {X.shape}")
    logger.info(f"Number of features: {X.shape[1]}")
    return X, y

def train_model():
    logger.info("Starting model training...")
    X, y = load_data()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        ))
    ])
    
    logger.info("Training RandomForest model...")
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    logger.info(f"F1 Score: {f1:.4f}")
    logger.info(f"ROC-AUC: {roc_auc:.4f}")
    logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    
    os.makedirs('models', exist_ok=True)
    model_path = 'models/model_v1.pkl'
    joblib.dump(pipeline, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Model v2 for A/B testing
    logger.info("Creating model v2 for A/B testing...")
    pipeline_v2 = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            class_weight='balanced'
        ))
    ])
    pipeline_v2.fit(X_train, y_train)
    model_path_v2 = 'models/model_v2.pkl'
    joblib.dump(pipeline_v2, model_path_v2)
    logger.info(f"Model v2 saved to {model_path_v2}")
    
    return pipeline, f1, roc_auc

if __name__ == '__main__':
    train_model()