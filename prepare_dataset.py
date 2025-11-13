"""
Prepare Dataset Script
Combines multiple CSV files into a single dataset for training
"""

import os
import pandas as pd
import glob

def combine_datasets(source_dir, output_path):
    """Combine multiple CSV files into a single dataset."""
    print(f"Looking for CSV files in: {source_dir}")
    
    # Find all CSV files
    csv_files = glob.glob(os.path.join(source_dir, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {source_dir}")
        return False
    
    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")
    
    # Combine datasets
    combined_data = []
    
    for csv_file in csv_files:
        try:
            print(f"\nReading: {os.path.basename(csv_file)}")
            # Try different encodings and separators
            df = None
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    df = pd.read_csv(csv_file, encoding=encoding, low_memory=False, on_bad_lines='skip')
                    break
                except:
                    try:
                        df = pd.read_csv(csv_file, encoding=encoding, sep=';', low_memory=False, on_bad_lines='skip')
                        break
                    except:
                        continue
            
            if df is None or df.empty:
                print(f"  [SKIP] Cannot read file (skipping)")
                continue
            
            print(f"  [OK] Read {len(df)} rows, columns: {list(df.columns)}")
            
            # Check if it has the required columns
            if 'text' in df.columns and 'label' in df.columns:
                print(f"  [OK] Has 'text' and 'label' columns")
                combined_data.append(df[['text', 'label']])
            elif 'email' in df.columns or 'body' in df.columns or 'message' in df.columns:
                # Try to map columns
                text_col = None
                for col in ['email', 'body', 'message', 'content', 'text']:
                    if col in df.columns:
                        text_col = col
                        break
                
                label_col = None
                for col in ['label', 'spam', 'phishing', 'is_phishing', 'type', 'class']:
                    if col in df.columns:
                        label_col = col
                        break
                
                if text_col and label_col:
                    # Map columns
                    df_mapped = df[[text_col, label_col]].rename(columns={text_col: 'text', label_col: 'label'})
                    # Ensure label is binary (0 or 1)
                    if df_mapped['label'].dtype != 'int64':
                        df_mapped['label'] = df_mapped['label'].apply(
                            lambda x: 1 if str(x).lower() in ['phishing', 'spam', '1', 'true', 'yes', 'phish'] else 0
                        )
                    print(f"  [OK] Mapped columns: {text_col} -> text, {label_col} -> label")
                    combined_data.append(df_mapped)
                else:
                    print(f"  [SKIP] Cannot map columns (available: {list(df.columns)})")
            else:
                # Try to use first column as text and infer label
                if len(df.columns) >= 1:
                    print(f"  [INFO] Trying to infer structure from columns: {list(df.columns)}")
                    # Check if first column looks like text
                    first_col = df.columns[0]
                    if df[first_col].dtype == 'object':  # String type
                        # Create text column
                        df_mapped = pd.DataFrame({'text': df[first_col].astype(str)})
                        # Try to find label column or create default
                        if len(df.columns) >= 2:
                            df_mapped['label'] = df.iloc[:, 1].astype(str).apply(
                                lambda x: 1 if str(x).lower() in ['phishing', 'spam', '1', 'true', 'yes', 'phish'] else 0
                            )
                        else:
                            # No label column, create default (all 0 - safe)
                            df_mapped['label'] = 0
                            print(f"  [WARN] No label column found, marking all as safe (0)")
                        combined_data.append(df_mapped)
                        print(f"  [OK] Using first column as text")
                else:
                    print(f"  [SKIP] Cannot process file (skipping)")
        except Exception as e:
            print(f"  [ERROR] Error reading file: {str(e)}")
            continue
    
    if not combined_data:
        print("\n[ERROR] No valid datasets found")
        return False
    
    # Combine all datasets
    print(f"\nCombining {len(combined_data)} datasets...")
    try:
        combined_df = pd.concat(combined_data, ignore_index=True)
    except Exception as e:
        print(f"[ERROR] Error combining datasets: {e}")
        return False
    
    # Clean data
    # Remove rows with empty text
    initial_count = len(combined_df)
    combined_df = combined_df[combined_df['text'].notna()]
    combined_df = combined_df[combined_df['text'].astype(str).str.strip() != '']
    print(f"  Removed {initial_count - len(combined_df)} rows with empty text")
    
    # Remove duplicates
    initial_count = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['text'])
    final_count = len(combined_df)
    
    print(f"  Initial rows: {initial_count}")
    print(f"  After removing duplicates: {final_count}")
    print(f"  Removed: {initial_count - final_count} duplicates")
    
    # Ensure label is integer
    combined_df['label'] = combined_df['label'].astype(int)
    
    # Check label distribution
    if 'label' in combined_df.columns:
        label_counts = combined_df['label'].value_counts()
        print(f"\nLabel distribution:")
        for label, count in label_counts.items():
            print(f"  Label {label}: {count} ({count/len(combined_df)*100:.1f}%)")
    
    # Save combined dataset
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    combined_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n[SUCCESS] Dataset saved to: {output_path}")
    print(f"  Total rows: {len(combined_df)}")
    
    return True

def create_sample_dataset(output_path):
    """Create a sample dataset if no dataset is available."""
    print("Creating sample dataset...")
    
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
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✓ Sample dataset created: {output_path}")
    print("  Note: This is a small sample dataset. For better results, use a larger dataset.")

def main():
    """Main function."""
    print("="*60)
    print("Dataset Preparation Script")
    print("="*60)
    
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_root, "dataset", "phishing_dataset.csv")
    
    # Check parent directory for dataset files
    parent_dir = os.path.dirname(project_root)
    dataset_dir = os.path.join(parent_dir, "phishing_email_dataset.csv")
    
    # Try to combine datasets from parent directory
    if os.path.exists(dataset_dir):
        if os.path.isdir(dataset_dir):
            print(f"\nFound dataset directory: {dataset_dir}")
            if combine_datasets(dataset_dir, output_path):
                print("\n[SUCCESS] Dataset preparation completed successfully!")
                return True
        elif os.path.isfile(dataset_dir):
            # It's a single CSV file
            print(f"\nFound dataset file: {dataset_dir}")
            print(f"Copying to: {output_path}")
            import shutil
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            shutil.copy(dataset_dir, output_path)
            print("[SUCCESS] Dataset copied successfully!")
            return True
    
    # Check if dataset already exists
    if os.path.exists(output_path):
        print(f"\n[INFO] Dataset already exists: {output_path}")
        try:
            response = input("Do you want to recreate it? (y/n): ")
            if response.lower() != 'y':
                return True
        except:
            # If input is not available (non-interactive), skip
            print("[INFO] Skipping recreation (non-interactive mode)")
            return True
    
    # Create sample dataset
    print("\n[INFO] No dataset found. Creating sample dataset...")
    create_sample_dataset(output_path)
    print("\n[WARNING] Sample dataset is very small. For better results, use a larger dataset.")
    print("  You can add more emails to the dataset manually or use a public dataset.")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

