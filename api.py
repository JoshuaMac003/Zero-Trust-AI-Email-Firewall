"""
FastAPI Application for Phishing Email Detection
REST API endpoint for serving the phishing email detection model
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import os
from phishing_detector import PhishingEmailDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Phishing Email Detection API",
    description="REST API for detecting phishing emails using machine learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global detector instance
detector: Optional[PhishingEmailDetector] = None


# Request/Response models
class EmailRequest(BaseModel):
    """Request model for email prediction"""
    text: str = Field(..., description="Email text to analyze", min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Congratulations! You have won $1,000,000. Click here to claim your prize: http://fake-link.com/claim"
            }
        }


class EmailPrediction(BaseModel):
    """Response model for email prediction"""
    prediction: str = Field(..., description="Prediction: 'Phishing' or 'Legitimate'")
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0, le=1)
    email_length: int = Field(..., description="Length of input email")
    cleaned_length: int = Field(..., description="Length after preprocessing")


class BatchEmailRequest(BaseModel):
    """Request model for batch email predictions"""
    emails: List[str] = Field(..., description="List of email texts to analyze", min_items=1)
    
    class Config:
        schema_extra = {
            "example": {
                "emails": [
                    "Congratulations! You won $1,000,000...",
                    "Meeting reminder: Tomorrow at 2 PM..."
                ]
            }
        }


class BatchEmailPrediction(BaseModel):
    """Response model for batch predictions"""
    results: List[EmailPrediction] = Field(..., description="List of predictions")
    total_processed: int = Field(..., description="Total number of emails processed")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    message: str


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global detector
    try:
        logger.info("Loading phishing email detection model...")
        detector = PhishingEmailDetector()
        
        # Check if model files exist
        if os.path.exists('vectorizer.joblib') and os.path.exists('calibrated_model.joblib'):
            detector.load_model()
            logger.info("Model loaded successfully!")
        else:
            logger.warning("Model files not found. Train the model first using phishing_detector.py")
            detector = None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        detector = None


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "Phishing Email Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    model_loaded = detector is not None and detector.vectorizer is not None
    
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        message="Model is loaded and ready" if model_loaded else "Model not loaded. Train the model first."
    )


@app.post("/predict", response_model=EmailPrediction, tags=["Prediction"])
async def predict_email(request: EmailRequest):
    """
    Predict whether a single email is phishing or legitimate.
    
    Args:
        request: EmailRequest containing the email text
        
    Returns:
        EmailPrediction with prediction, confidence, and metadata
    """
    if detector is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first using phishing_detector.py"
        )
    
    try:
        # Make prediction
        prediction, confidence = detector.predict(request.text)
        
        # Get additional metadata
        cleaned_text = detector.clean_text(request.text)
        
        return EmailPrediction(
            prediction=prediction,
            confidence=confidence,
            email_length=len(request.text),
            cleaned_length=len(cleaned_text)
        )
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/batch", response_model=BatchEmailPrediction, tags=["Prediction"])
async def predict_batch_emails(request: BatchEmailRequest):
    """
    Predict whether multiple emails are phishing or legitimate (batch processing).
    
    Args:
        request: BatchEmailRequest containing a list of email texts
        
    Returns:
        BatchEmailPrediction with list of predictions
    """
    if detector is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first using phishing_detector.py"
        )
    
    try:
        results = []
        for email_text in request.emails:
            try:
                prediction, confidence = detector.predict(email_text)
                cleaned_text = detector.clean_text(email_text)
                
                results.append(EmailPrediction(
                    prediction=prediction,
                    confidence=confidence,
                    email_length=len(email_text),
                    cleaned_length=len(cleaned_text)
                ))
            except Exception as e:
                logger.warning(f"Error processing email in batch: {e}")
                # Continue with next email even if one fails
                results.append(EmailPrediction(
                    prediction="Error",
                    confidence=0.0,
                    email_length=len(email_text),
                    cleaned_length=0
                ))
        
        return BatchEmailPrediction(
            results=results,
            total_processed=len(results)
        )
    except Exception as e:
        logger.error(f"Error during batch prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")


@app.get("/model/info", tags=["Model"])
async def model_info():
    """
    Get information about the loaded model.
    
    Returns:
        Dictionary with model information
    """
    if detector is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    try:
        info = {
            "model_loaded": True,
            "vectorizer_loaded": detector.vectorizer is not None,
            "calibrated_model_loaded": detector.calibrated_model is not None,
            "using_spacy": detector.use_spacy if hasattr(detector, 'use_spacy') else False,
        }
        
        if detector.vectorizer is not None:
            info["vectorizer_features"] = detector.vectorizer.max_features
            info["vectorizer_ngram_range"] = str(detector.vectorizer.ngram_range)
        
        return info
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



