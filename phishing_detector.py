"""
Phishing Email Detection System
A complete ML-based system to classify emails as "Phishing" or "Legitimate"
"""

import re
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, classification_report, confusion_matrix
)
import joblib
import spacy
from typing import Optional

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load spaCy model (use en_core_web_sm for better performance, fallback to basic if not available)
try:
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    logger_spacy = logging.getLogger('spacy')
    logger_spacy.setLevel(logging.ERROR)  # Reduce spaCy logging
except OSError:
    logger.warning("spaCy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
    logger.warning("Falling back to basic preprocessing...")
    nlp = None


class PhishingEmailDetector:
    """
    Complete phishing email detection system with preprocessing, 
    training, evaluation, and prediction capabilities.
    Uses spaCy pipeline for optimized NLP preprocessing.
    """
    
    def __init__(self, use_spacy: bool = True):
        self.vectorizer = None
        self.model = None
        self.calibrated_model = None
        self.use_spacy = use_spacy and (nlp is not None)
        if self.use_spacy:
            logger.info("Using spaCy pipeline for preprocessing")
        else:
            logger.info("Using basic preprocessing (spaCy not available)")
        
    def clean_text(self, text: str) -> str:
        """
        Clean email text using optimized spaCy pipeline or basic preprocessing.
        Removes HTML, URLs, punctuation, and stopwords with lemmatization.
        
        Args:
            text (str): Raw email text
            
        Returns:
            str: Cleaned text
        """
        if pd.isna(text):
            return ""
        
        # Convert to string
        text = str(text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
        text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Use spaCy pipeline for advanced preprocessing
        if self.use_spacy:
            try:
                # Process with spaCy
                doc = nlp(text)
                
                # Extract tokens: lemmatize, remove stopwords, punctuation, and short tokens
                tokens = [
                    token.lemma_.lower().strip()
                    for token in doc
                    if not token.is_stop
                    and not token.is_punct
                    and not token.is_space
                    and len(token.lemma_) > 2
                    and token.is_alpha
                ]
                
                text = ' '.join(tokens)
            except Exception as e:
                logger.warning(f"spaCy processing failed, falling back to basic preprocessing: {e}")
                # Fallback to basic preprocessing
                text = self._basic_clean(text)
        else:
            # Basic preprocessing fallback
            text = self._basic_clean(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _basic_clean(self, text: str) -> str:
        """
        Basic text cleaning fallback when spaCy is not available.
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and punctuation (keep alphanumeric and spaces)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Simple word filtering (remove short words)
        words = [word for word in text.split() if len(word) > 2]
        
        return ' '.join(words)
    
    def preprocess_data(self, df):
        """
        Preprocess the entire dataset.
        
        Args:
            df (pd.DataFrame): DataFrame with 'text' and 'label' columns
            
        Returns:
            tuple: (X_cleaned, y) where X_cleaned is cleaned text and y is labels
        """
        logger.info("Starting data preprocessing...")
        
        # Clean text
        df['cleaned_text'] = df['text'].apply(self.clean_text)
        
        # Remove empty texts
        df = df[df['cleaned_text'].str.len() > 0]
        
        X = df['cleaned_text'].values
        y = df['label'].values
        
        logger.info(f"Preprocessed {len(X)} samples")
        logger.info(f"Label distribution: {np.bincount(y)}")
        
        return X, y
    
    def train_model(self, X_train, y_train, perform_grid_search=True):
        """
        Train the phishing email detection model with optional hyperparameter tuning.
        
        Args:
            X_train (array-like): Training text data
            y_train (array-like): Training labels
            perform_grid_search (bool): Whether to perform grid search for hyperparameters
            
        Returns:
            tuple: (vectorizer, model, calibrated_model)
        """
        logger.info("Starting model training...")
        
        if perform_grid_search:
            logger.info("Performing hyperparameter tuning with GridSearchCV...")
            
            # Create pipeline
            pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(
                    sublinear_tf=True,
                    lowercase=True,
                    stop_words='english'
                )),
                ('classifier', LogisticRegression(
                    solver='saga',
                    class_weight='balanced',
                    max_iter=2000,
                    random_state=42,
                    n_jobs=-1
                ))
            ])
            
            # Define parameter grid
            param_grid = {
                'vectorizer__max_features': [10000, 20000],
                'vectorizer__ngram_range': [(1, 1), (1, 2)],
                'classifier__C': [0.1, 1.0, 5.0]
            }
            
            # Perform grid search with cross-validation
            logger.info("Running GridSearchCV (this may take a while)...")
            grid_search = GridSearchCV(
                pipeline,
                param_grid,
                cv=3,
                scoring='roc_auc',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_train, y_train)
            
            logger.info(f"Best parameters: {grid_search.best_params_}")
            logger.info(f"Best CV score (ROC-AUC): {grid_search.best_score_:.4f}")
            
            # Extract best components
            self.vectorizer = grid_search.best_estimator_.named_steps['vectorizer']
            self.model = grid_search.best_estimator_.named_steps['classifier']
            
        else:
            # Use default parameters
            logger.info("Training with default parameters...")
            self.vectorizer = TfidfVectorizer(
                max_features=20000,
                ngram_range=(1, 2),
                sublinear_tf=True,
                lowercase=True,
                stop_words='english'
            )
            
            X_train_tfidf = self.vectorizer.fit_transform(X_train)
            
            self.model = LogisticRegression(
                solver='saga',
                class_weight='balanced',
                max_iter=2000,
                random_state=42,
                C=1.0,
                n_jobs=-1
            )
            self.model.fit(X_train_tfidf, y_train)
        
        # Calibrate the model for reliable probabilities
        logger.info("Calibrating model for reliable probability estimates...")
        X_train_tfidf = self.vectorizer.transform(X_train)
        self.calibrated_model = CalibratedClassifierCV(
            self.model, 
            method='isotonic', 
            cv=3
        )
        self.calibrated_model.fit(X_train_tfidf, y_train)
        
        logger.info("Model training completed!")
        return self.vectorizer, self.model, self.calibrated_model
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluate the trained model on test data.
        
        Args:
            X_test (array-like): Test text data
            y_test (array-like): Test labels
            
        Returns:
            dict: Dictionary containing evaluation metrics
        """
        logger.info("Evaluating model on test set...")
        
        # Transform test data
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        # Predictions
        y_pred = self.calibrated_model.predict(X_test_tfidf)
        y_pred_proba = self.calibrated_model.predict_proba(X_test_tfidf)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc
        }
        
        # Print results
        logger.info("\n" + "="*50)
        logger.info("EVALUATION RESULTS")
        logger.info("="*50)
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1-Score:  {f1:.4f}")
        logger.info(f"ROC-AUC:   {roc_auc:.4f}")
        logger.info("="*50)
        
        # Classification report
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
        
        # Confusion matrix
        logger.info("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"                Predicted")
        logger.info(f"              Legit  Phish")
        logger.info(f"Actual Legit   {cm[0][0]:4d}   {cm[0][1]:4d}")
        logger.info(f"Actual Phish   {cm[1][0]:4d}   {cm[1][1]:4d}")
        
        return metrics
    
    def save_model(self, vectorizer_path='vectorizer.joblib', 
                   model_path='phishing_model.joblib',
                   calibrated_model_path='calibrated_model.joblib'):
        """
        Save the trained vectorizer and model to disk.
        
        Args:
            vectorizer_path (str): Path to save vectorizer
            model_path (str): Path to save base model
            calibrated_model_path (str): Path to save calibrated model
        """
        if self.vectorizer is None or self.model is None or self.calibrated_model is None:
            raise ValueError("Model not trained yet. Train the model before saving.")
        
        logger.info(f"Saving vectorizer to {vectorizer_path}...")
        joblib.dump(self.vectorizer, vectorizer_path)
        
        logger.info(f"Saving base model to {model_path}...")
        joblib.dump(self.model, model_path)
        
        logger.info(f"Saving calibrated model to {calibrated_model_path}...")
        joblib.dump(self.calibrated_model, calibrated_model_path)
        
        logger.info("Models saved successfully!")
    
    def load_model(self, vectorizer_path='vectorizer.joblib',
                   calibrated_model_path='calibrated_model.joblib'):
        """
        Load the trained vectorizer and model from disk.
        
        Args:
            vectorizer_path (str): Path to load vectorizer
            calibrated_model_path (str): Path to load calibrated model
        """
        logger.info(f"Loading vectorizer from {vectorizer_path}...")
        self.vectorizer = joblib.load(vectorizer_path)
        
        logger.info(f"Loading calibrated model from {calibrated_model_path}...")
        self.calibrated_model = joblib.load(calibrated_model_path)
        
        logger.info("Models loaded successfully!")
    
    def predict(self, email_text):
        """
        Predict whether an email is phishing or legitimate.
        
        Args:
            email_text (str): Raw email text
            
        Returns:
            str: "Phishing" or "Legitimate"
        """
        if self.vectorizer is None or self.calibrated_model is None:
            raise ValueError("Model not loaded. Load or train the model first.")
        
        # Clean the text
        cleaned_text = self.clean_text(email_text)
        
        # Transform
        text_tfidf = self.vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = self.calibrated_model.predict(text_tfidf)[0]
        probability = self.calibrated_model.predict_proba(text_tfidf)[0]
        
        result = "Phishing" if prediction == 1 else "Legitimate"
        prob_phishing = probability[1] if prediction == 1 else probability[0]
        
        return result, prob_phishing


def main():
    """
    Main function to run the complete training pipeline.
    """
    # Load dataset
    dataset_path = 'phishing_email_dataset.csv'
    logger.info(f"Loading dataset from {dataset_path}...")
    
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        logger.error(f"Dataset not found at {dataset_path}")
        logger.info("Please ensure the CSV file exists with 'text' and 'label' columns")
        return
    
    # Check required columns
    if 'text' not in df.columns or 'label' not in df.columns:
        logger.error("Dataset must contain 'text' and 'label' columns")
        return
    
    # Initialize detector
    detector = PhishingEmailDetector()
    
    # Preprocess data
    X, y = detector.preprocess_data(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"Training set size: {len(X_train)}")
    logger.info(f"Test set size: {len(X_test)}")
    
    # Train model
    detector.train_model(X_train, y_train, perform_grid_search=True)
    
    # Evaluate model
    metrics = detector.evaluate_model(X_test, y_test)
    
    # Save model
    detector.save_model()
    
    # Example prediction
    logger.info("\n" + "="*50)
    logger.info("Example Prediction:")
    logger.info("="*50)
    example_email = "Congratulations! You have won $1,000,000. Click here to claim your prize: http://fake-link.com/claim"
    result, prob = detector.predict(example_email)
    logger.info(f"Email: {example_email[:80]}...")
    logger.info(f"Prediction: {result}")
    logger.info(f"Confidence: {prob:.4f}")
    
    logger.info("\nTraining pipeline completed successfully!")


if __name__ == "__main__":
    main()

