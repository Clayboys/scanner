"""
-download python from their website
-open cmd and type: python --version
-reopen cmd if it doesnt work 
-type: pip install pytesseract
-download the pytesseract windows installer from github*
-https://github.com/UB-Mannheim/tesseract/wiki
*windows will try to stop you, click details, run anyway
-open the start menu and type: env
-click environment variables, click environment variables at the bottom
-the bottom section is system variables, code that can be called globally
-click Path, edit, click new, paste the full filepath to the folder called 'Tesseract-OCR'*
*the windows installer should have put it in program files
-click ok, ok, ok
-type: tesseract
-reopen cmd if it doesnt work
-to run this script type: python scan.py
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image
from pytesseract import pytesseract
from pdf2image import convert_from_path

#creating an instance of a tkinter window
root = tk.Tk()
#hiding the window without destroying it
root.withdraw()

#need a string that points to tesseract.exe
#tesPth = r"D:\Program Files\Tesseract-OCR\tesseract.exe"
#base text to spit out in case nothing gets interperated
text = ""
#prompting for a file location
if tk.messagebox.askyesno(title=None, message="pls select an image file for me to scan"):
    #try choosing a file using file explorer
    #try: 
    samplePth = filedialog.askopenfilename()
        #try opening the chosen file
        #try:
    print("Coverting PDF. Please Wait...")
    pages = convert_from_path(samplePth)
    print("Scanning for Text. Please Wait...")
    pageNum = 1
    for i in pages:
        i.save("out0.png")
        text += "Page " + pageNum + ":\n"
        text += pytesseract.image_to_string(".\out0.png")
    print("Writing Text to File...")
    with open(".\OutText.txt", "w") as file1:
        file1.write(text)
    print("Finished")
    #pages[9].save("out0.png", "PNG")
    #pages[10].save("out0.png", "PNG")
            #pages[0].save("out.bmp", "BMP")
            #img = Image.open(".\out.bmp")
            #try interperating text from opened image file, and print out the text
            #try:
    #text = pytesseract.image_to_string(".\out0.png")
    #file1 = open(".\OutText.txt", "a")
    #file1.writelines(text)
    #tk.messagebox.showinfo(title="here's what we found", message=text)
    input()
            #except:
                #something went wrong interperating that file
                #tk.messagebox.showinfo(title=None, message="something went wrong interperating that file! ask for help")
        #except:
            #something went wrong opening that file
            #tk.messagebox.showinfo(title=None, message="something went wrong opening that file! ask for help")
    #except:
        #something went wrong choosing that file
        #tk.messagebox.showinfo(title=None, message="something went wrong choosing that file! ask for help")
    #pytesseract.pytesseract_cmd = tesPth
else:
    #clicked no at initial prompt so just exit
    pass