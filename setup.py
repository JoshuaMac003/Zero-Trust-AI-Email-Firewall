"""
Setup script for Zero-Trust AI Email Firewall
Initializes the project and downloads required dependencies
"""

import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_command(command, description):
    """Run a shell command and handle errors."""
    logger.info(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def create_directories():
    """Create required directories."""
    directories = [
        "backend/model",
        "backend/utils",
        "backend/database",
        "frontend/components",
        "dataset"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✓ Created directory: {directory}")


def install_dependencies():
    """Install Python dependencies."""
    return run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    )


def download_spacy_model():
    """Download spaCy language model."""
    return run_command(
        "python -m spacy download en_core_web_sm",
        "Downloading spaCy model"
    )


def initialize_database():
    """Initialize the database."""
    try:
        from backend.database.init_db import init_database
        db_path = "backend/database/firewall.db"
        init_database(db_path)
        logger.info(f"✓ Database initialized at {db_path}")
        return True
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False


def main():
    """Main setup function."""
    logger.info("=" * 50)
    logger.info("Zero-Trust AI Email Firewall - Setup")
    logger.info("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    logger.info("\nCreating directories...")
    create_directories()
    
    # Install dependencies
    logger.info("\nInstalling dependencies...")
    if not install_dependencies():
        logger.error("Failed to install dependencies")
        sys.exit(1)
    
    # Download spaCy model
    logger.info("\nDownloading spaCy model...")
    if not download_spacy_model():
        logger.warning("Failed to download spaCy model. The system will use basic preprocessing.")
    
    # Initialize database
    logger.info("\nInitializing database...")
    if not initialize_database():
        logger.error("Failed to initialize database")
        sys.exit(1)
    
    logger.info("\n" + "=" * 50)
    logger.info("Setup completed successfully!")
    logger.info("=" * 50)
    logger.info("\nNext steps:")
    logger.info("1. Prepare your dataset: dataset/phishing_dataset.csv")
    logger.info("2. Train the model: python backend/model/train_model.py")
    logger.info("3. Start the backend: python backend/app.py")
    logger.info("4. Start the frontend: streamlit run frontend/streamlit_app.py")
    logger.info("\nFor more information, see README.md")


if __name__ == "__main__":
    main()


