from PyPDF2 import PdfReader
import os

def process_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    output_data = []
    
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            output_data.append(page.extract_text())
    
    return output_data

def save_processed_output(output_data, output_file_path):
    with open(output_file_path, "w") as output_file:
        for page_text in output_data:
            output_file.write(page_text + "\n")

def process_multiple_pdfs(file_paths, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for file_path in file_paths:
        try:
            output_data = process_pdf(file_path)
            output_file_name = os.path.basename(file_path).replace('.pdf', '_processed.txt')
            output_file_path = os.path.join(output_directory, output_file_name)
            save_processed_output(output_data, output_file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")