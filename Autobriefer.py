from pdf2image import convert_from_path
import numpy as np

# Path to the scanned PDF
test_file = r"C:\Users\danandnat\Desktop\appointments.pdf"

print("Converting page 6 to a NumPy array...")
pages = convert_from_path(test_file, dpi=200,)  

# Convert pages to a NumPy array
page_array = np.array(pages[0])  

# Verify the conversion
print(f"Pages : Shape = {page_array.shape}, Data Type = {page_array.dtype}")

print("Success!")
