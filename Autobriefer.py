import os
import re
import time
import shutil
import logging
from PIL import Image
from pytesseract import pytesseract
from pdf2image import convert_from_path

# Configure logging
logging.basicConfig(filename='autobriefer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the path to poppler here
poppler_path = r"C:\Users\danandnat\Desktop\poppler-25.03.0\poppler-24.08.0\Library\bin"

# Folder paths
WATCH_FOLDER = r"C:\\Users\\danandnat\\Desktop\\brief tester"
BRIEFED_FOLDER = r"C:\\Users\\danandnat\\Desktop\\briefed"
COMPLETE_FOLDER = r"C:\\Users\\danandnat\\Desktop\\COMPLETE"

# Form identifiers
FORM_TYPES = {"OA32A": [], "DWC-32": [], "OA32C": [], "OA32D": [], "OA32AM": []}
FORM_DATA_KEYS = ["claimant name", "DWC number", "appointment date", "doctor", "adjuster", "adjuster email", "reason for cancellation", "reason for denial", "changes to appointment"]

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
    
    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        logging.info(f"Converting PDF to images: {pdf_path}")
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
        for page_num, page in enumerate(pages, start=1):
            img_path = f"temp_page_{page_num}.png"
            page.save(img_path)
            logging.info(f"Extracting text from image: {img_path}")
            text += f"Page {page_num}:\n" + pytesseract.image_to_string(img_path) + "\n"
            os.remove(img_path)
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
    return text

def extract_claimant_and_form(text):
    """
    Extract claimant name and form name from the text.
    
    Args:
        text (str): The extracted text from the PDF.
    
    Returns:
        tuple: Claimant name and form name.
    """
    claimant_name = "Unknown_Unknown"
    form_name = "Unknown"

    try:
        logging.info("Extracting claimant name and form name from text")
        # Extract claimant name (assuming it's in the format "Last Name, First Name" in the top right)
        claimant_match = re.search(r"(?i)(\b[A-Z][a-z]+, [A-Z][a-z]+\b)", text)
        if claimant_match:
            claimant_name = claimant_match.group(1).replace(", ", "_")
        
        # Extract form name (assuming it's in the bottom left of every page)
        form_match = re.search(r"(OA32A|DWC-32|OA32C|OA32D|OA32AM)", text, re.IGNORECASE)
        if form_match:
            form_name = form_match.group(1).upper()

        logging.info(f"Claimant Name: {claimant_name}, Form Name: {form_name}")
    except Exception as e:
        logging.error(f"Error extracting claimant and form: {e}")
    return claimant_name, form_name

def process_pdf(file_path):
    """
    Process a PDF file to extract text, categorize it, and move it to the appropriate folders.
    
    Args:
        file_path (str): The path to the PDF file.
    """
    try:
        logging.info(f"Starting to process the PDF: {file_path}")
        text = extract_text_from_pdf(file_path)
        claimant_name, form_name = extract_claimant_and_form(text)
        
        # Ensure OA32A forms are followed by DWC-32 forms
        if form_name == "OA32A":
            dest_folder = os.path.join(BRIEFED_FOLDER, claimant_name, form_name)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, f"{claimant_name}_{form_name}.pdf")
            shutil.move(file_path, dest_path)
            logging.info(f"Moved {file_path} to {dest_path}")
            
            # Check for DWC-32 form
            dwc32_path = os.path.join(WATCH_FOLDER, f"{claimant_name}_DWC-32.pdf")
            if os.path.exists(dwc32_path):
                shutil.move(dwc32_path, os.path.join(dest_folder, f"{claimant_name}_DWC-32.pdf"))
                logging.info(f"Moved {dwc32_path} to {dest_folder}")
        else:
            dest_folder = os.path.join(BRIEFED_FOLDER, claimant_name, form_name)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, f"{claimant_name}_{form_name}.pdf")
            shutil.move(file_path, dest_path)
            logging.info(f"Moved {file_path} to {dest_path}")

        # Move original file to COMPLETE folder
        original_complete_path = os.path.join(COMPLETE_FOLDER, os.path.basename(file_path))
        shutil.move(file_path, original_complete_path)
        logging.info(f"Original PDF moved to COMPLETE folder: {original_complete_path}")
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")

def monitor_folder():
    """
    Monitor the folder for new PDF files and process them.
    """
    logging.info(f"Watching folder: {WATCH_FOLDER}")
    processed_files = set()
    while True:
        try:
            for file_name in os.listdir(WATCH_FOLDER):
                if file_name.endswith(".pdf") and file_name not in processed_files:
                    file_path = os.path.join(WATCH_FOLDER, file_name)
                    logging.info(f"Processing: {file_name}")
                    process_pdf(file_path)
                    processed_files.add(file_name)
            time.sleep(5)
        except Exception as e:
            logging.error(f"Error monitoring folder: {e}")

if __name__ == "__main__":
    monitor_folder()