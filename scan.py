"""
-download python from their website
-open cmd and type: python --version
-reopen cmd if it doesnt work 
-type: pip install pytesseract
-download the pytesseract windows installer from github*
*windows will try to stop you, click details, run anyway
-open the start menu and type: env
-click environment variables, click environment variables at the bottom
-the bottom section is system variables, code that can be called globally
-click edit, click new, paste the full filepath to the 'Tesseract-OCR'*
*the windows installer should have put it in program files
-click ok, ok, ok
-type: tesseract
-reopen cmd if it doesnt work
"""

from PIL import Image
from pytesseract import pytesseract

tesPth = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
samplePth = r"D:\code\sample.png"
img = Image.open(samplePth)
pytesseract.pytesseract_cmd = tesPth

text = pytesseract.image_to_string(img)
print(text)

print("hello world")