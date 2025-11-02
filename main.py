"""
Main script to run all deep learning model training notebooks for tomato leaf disease classification.
This script executes the following notebooks in sequence:
1. vgg19-tomato - Copy.ipynb
2. vgg16-tomato - Copy.ipynb
3. resnet50-tomato - Copy.ipynb
4. inception-v3-tomato - Copy.ipynb
"""

import os
import sys
import subprocess
from pathlib import Path
import time

def run_notebook(notebook_path):
    """
    Execute a Jupyter notebook using papermill or jupyter nbconvert.
    
    Args:
        notebook_path: Path to the notebook file
        
    Returns:
        True if execution successful, False otherwise
    """
    notebook_path = Path(notebook_path)
    
    if not notebook_path.exists():
        print(f"Error: Notebook not found: {notebook_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Executing: {notebook_path.name}")
    print(f"{'='*60}\n")
    
    # Try papermill first (recommended method)
    try:
        import papermill
        result = subprocess.run(
            [
                sys.executable, "-m", "papermill",
                str(notebook_path),
                str(notebook_path),  # Execute in-place
                "--log-output"
            ],
            cwd=str(notebook_path.parent),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ Successfully executed: {notebook_path.name}")
            return True
        else:
            print(f"\n✗ Failed to execute with papermill: {notebook_path.name}")
            # Fall through to try jupyter nbconvert
    except ImportError:
        print("Papermill not found, trying jupyter nbconvert...")
    
    # Fallback: Try jupyter nbconvert as command
    try:
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--inplace",
                str(notebook_path)
            ],
            cwd=str(notebook_path.parent),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ Successfully executed: {notebook_path.name}")
            return True
        else:
            print(f"\n✗ Failed to execute: {notebook_path.name}")
            return False
            
    except FileNotFoundError:
        print("\n✗ Error: Neither papermill nor jupyter found.")
        print("Please install papermill: pip install papermill")
        print("Or install jupyter: pip install jupyter")
        return False
    except Exception as e:
        print(f"\n✗ Error executing {notebook_path.name}: {str(e)}")
        return False


def main():
    """Main function to run all notebooks in sequence."""
    
    # Get the script directory
    script_dir = Path(__file__).parent
    plantvillage_dir = script_dir 
    
    # List of notebooks to execute in order
    notebooks = [
        "vgg19-tomato - Copy.ipynb",
        "vgg16-tomato - Copy.ipynb",
        "resnet50-tomato - Copy.ipynb",
        "inception-v3-tomato - Copy.ipynb"
    ]
    
    print("="*60)
    print("Tomato Leaf Disease Classification - Model Training")
    print("="*60)
    print(f"\nWorking directory: {plantvillage_dir}")
    print(f"\nNotebooks to execute: {len(notebooks)}")
    
    # Check if plantvillage directory exists
    if not plantvillage_dir.exists():
        print(f"\nError: Directory not found: {plantvillage_dir}")
        print("Please ensure you're running this script from the correct location.")
        sys.exit(1)
    
    # Change to plantvillage directory
    os.chdir(plantvillage_dir)
    
    # Track execution results
    results = {}
    start_time = time.time()
    
    # Execute each notebook
    for notebook_name in notebooks:
        notebook_path = plantvillage_dir / notebook_name
        
        if not notebook_path.exists():
            print(f"\nWarning: Notebook not found: {notebook_path}")
            results[notebook_name] = False
            continue
        
        notebook_start = time.time()
        success = run_notebook(notebook_path)
        notebook_end = time.time()
        
        results[notebook_name] = success
        elapsed_minutes = (notebook_end - notebook_start) / 60
        print(f"Execution time: {elapsed_minutes:.2f} minutes")
        
        # Add a small delay between notebooks
        if notebook_name != notebooks[-1]:
            print("\nWaiting 5 seconds before next notebook...")
            time.sleep(5)
    
    # Print summary
    total_time = (time.time() - start_time) / 60
    
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)
    
    for notebook_name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{notebook_name:50s} {status}")
    
    print(f"\nTotal execution time: {total_time:.2f} minutes")
    print("="*60)
    
    # Exit with appropriate code
    if all(results.values()):
        print("\nAll notebooks executed successfully!")
        sys.exit(0)
    else:
        print("\nSome notebooks failed to execute. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

