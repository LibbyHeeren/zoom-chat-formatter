# Import libararies
import os
import sys
import argparse
from zchat_fmt import process_zoom_chat

# Define function to process a folder full of .txt files
def process_directory(input_dir, output_dir):
    """
    Process all .txt files in the input directory and save results to the output directory
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Get all .txt files in the input directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if not files:
        print(f"No .txt files found in {input_dir}")
        return
    
    print(f"Found {len(files)} .txt files to process")
    
    # Process each file
    for i, filename in enumerate(files):
        input_path = os.path.join(input_dir, filename)
        
        # Create output filename - same name but in output directory
        output_path = os.path.join(output_dir, filename)
        
        print(f"Processing {i+1}/{len(files)}: {filename}")
        try:
            process_zoom_chat(input_path, output_path)
            print(f"  → Saved to {output_path}")
        except Exception as e:
            print(f"  → Error processing {filename}: {e}")
    
    print(f"Completed processing {len(files)} files")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process multiple Zoom chat files')
    parser.add_argument('input_dir', help='Directory containing input .txt files')
    parser.add_argument('output_dir', help='Directory where processed files will be saved')
    
    args = parser.parse_args()
    
    process_directory(args.input_dir, args.output_dir)