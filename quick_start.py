"""
Quick Start Script
Helps set up and start the Zero-Trust AI Email Firewall
"""

import os
import sys
import subprocess
import time

def print_step(step, message):
    """Print step message."""
    print(f"\n{'='*60}")
    print(f"Step {step}: {message}")
    print('='*60)

def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\nRunning: {description}")
    print(f"Command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ {description} failed")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description} exists: {filepath}")
        return True
    else:
        print(f"✗ {description} not found: {filepath}")
        return False

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("Zero-Trust AI Email Firewall - Quick Start")
    print("="*60)
    
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print(f"\nProject directory: {project_root}")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    # Step 2: Check dependencies
    print_step(2, "Checking Dependencies")
    try:
        import fastapi
        import streamlit
        import sklearn
        import spacy
        import pandas
        print("✓ All dependencies are installed")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return False
    
    # Step 3: Initialize database
    print_step(3, "Initializing Database")
    db_init_cmd = f'python backend/database/init_db.py'
    if not run_command(db_init_cmd, "Database initialization"):
        print("⚠ Database initialization failed, but continuing...")
    
    # Step 4: Check for dataset
    print_step(4, "Checking Dataset")
    dataset_path = os.path.join(project_root, "dataset", "phishing_dataset.csv")
    
    # Check parent directory for dataset
    parent_dir = os.path.dirname(project_root)
    parent_dataset = os.path.join(parent_dir, "phishing_email_dataset.csv")
    
    if check_file_exists(dataset_path, "Dataset"):
        print("✓ Dataset found in dataset/ directory")
    else:
        print("✗ Dataset not found in dataset/ directory")
        print("  Checking parent directory...")
        
        # Check if parent_dataset is a directory (contains CSV files)
        if os.path.exists(parent_dataset):
            if os.path.isdir(parent_dataset):
                print(f"✓ Found dataset directory: {parent_dataset}")
                print("  Preparing dataset from multiple CSV files...")
                # Use prepare_dataset.py to combine CSV files
                prepare_cmd = f'python prepare_dataset.py'
                if run_command(prepare_cmd, "Dataset preparation", check=False):
                    if check_file_exists(dataset_path, "Prepared dataset"):
                        print("✓ Dataset prepared successfully")
                    else:
                        print("⚠ Dataset preparation may have failed, creating sample dataset...")
                        create_sample_dataset(dataset_path)
                else:
                    print("⚠ Dataset preparation failed, creating sample dataset...")
                    create_sample_dataset(dataset_path)
            elif os.path.isfile(parent_dataset):
                print(f"✓ Dataset found in parent directory: {parent_dataset}")
                print(f"  Copying to dataset/phishing_dataset.csv...")
                import shutil
                os.makedirs(os.path.join(project_root, "dataset"), exist_ok=True)
                try:
                    shutil.copy(parent_dataset, dataset_path)
                    print("✓ Dataset copied successfully")
                except Exception as e:
                    print(f"✗ Error copying dataset: {e}")
                    print("  Creating sample dataset instead...")
                    create_sample_dataset(dataset_path)
            else:
                print("✗ Dataset not found")
                print("  Creating sample dataset...")
                create_sample_dataset(dataset_path)
        else:
            print("✗ Dataset not found in parent directory")
            print("  Creating sample dataset...")
            create_sample_dataset(dataset_path)
    
    # Step 5: Check for trained model
    print_step(5, "Checking Trained Model")
    model_path = os.path.join(project_root, "backend", "model", "calibrated_model.pkl")
    
    if check_file_exists(model_path, "Trained model"):
        print("✓ Model is already trained")
    else:
        print("✗ Model not found")
        print("Training model...")
        train_cmd = f'python backend/model/train_model.py --dataset "{dataset_path}" --no-grid-search'
        if not run_command(train_cmd, "Model training", check=False):
            print("⚠ Model training failed. You can train it later manually.")
            print("  Command: python backend/model/train_model.py")
            response = input("\nDo you want to continue without training? (y/n): ")
            if response.lower() != 'y':
                return False
    
    # Step 6: Start backend server
    print_step(6, "Starting Backend Server")
    print("\n" + "="*60)
    print("Starting FastAPI backend server...")
    print("="*60)
    print("\nThe server will start on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("\n" + "="*60)
    
    # Start server
    try:
        import uvicorn
        os.chdir(project_root)
        uvicorn.run(
            "backend.app:app",
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        print("\nYou can start the server manually with:")
        print("  python start_backend.py")
        return False

def create_sample_dataset(dataset_path):
    """Create a sample dataset."""
    import pandas as pd
    import os
    
    sample_data = {
        'text': [
            'Subject: URGENT: Your Account Will Be Suspended\n\nDear Customer,\n\nYour account will be suspended. Click here to verify: http://fake-link.com',
            'Subject: Meeting Reminder\n\nHi Team,\n\nThis is a reminder about our scheduled meeting tomorrow at 2 PM.',
            'Subject: Congratulations! You Won $1,000,000\n\nCongratulations! You have won $1,000,000. Click here to claim: http://fake-link.com',
            'Subject: Thanks for Your Order\n\nThanks for your order. Your package will arrive tomorrow.',
            'Subject: Verify Your Account\n\nPlease verify your account by clicking this link: http://bit.ly/verify-account',
            'Subject: Project Update\n\nHi Team,\n\nThis is an update on the project status.',
        ],
        'label': [1, 0, 1, 0, 1, 0]
    }
    
    df = pd.DataFrame(sample_data)
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    df.to_csv(dataset_path, index=False)
    print(f"✓ Sample dataset created: {dataset_path}")
    print("  Note: This is a small sample dataset. For better results, use a larger dataset.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

