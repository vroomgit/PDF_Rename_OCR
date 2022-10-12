"""
This script reads a pdf document (lien waivers in this case) via OCR and renames the file based on the generated text. 
libraries used: pdf2image, pytesseract, openCV, re, os

@author: varun.singh

Install libraries commands:

pip install pdf2image
conda install -c conda-forge poppler 
pip install opencv-python==4.5.5.64

Set tesseract_cmd to folder containing tesseract.exe
pytesseract.pytesseract.tesseract_cmd = 'SYSTEM PATH TO TESSERACT.EXE'
"""

# import libraries
from pdf2image import convert_from_path
import cv2

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'SYSTEM PATH TO TESSERACT.EXE'

import re
import os


# Loop performs the following actions:
# 1. Open each pdf file in the working directory.
# 2. Convert file to image and save image.
# 3. Reading and parsing text from image via regex.
# 4. Rename file based on parsed text.
# 5. If parsing is unsuccessful or the parsed name is too large (>100 chars), renames the file with "notChanged" prefix
# Set working directory to folder containing pdf files
for file in os.listdir('.'):
    if file.lower()[-3:] != 'pdf':
        continue
    print(file)
    
    pages = convert_from_path(file, 500) #500 dpi resolution for image conversion
    
    # save image
    imName = file[:-4] + '.jpg'
    pages[0].save(imName, 'JPEG')
    
    # read image
    image = cv2.imread(imName,0)
    
    # generate text from image
    text = pytesseract.image_to_string(image, lang='eng')
    
    # parsing date of format Month DD, YYYY
    date = re.search(r'\s{1}\D{2,9}\s{1}\d{0,2},\s{1}\d{4}',text)
    try:
        date = date.group(0)
        date = date[1:]
        date = date.replace(",", "")
        date = date.replace("\n", "")
    except:
        date = ''
    
    if re.search(r'UNCONDITIONAL',text) == None:
        lwType = 'LWC'
    else:
        lwType = 'LWU'
    
    sub = re.search(r'Undersigned Lienor.{2,20}',text)
    
    try:
        sub = sub.group(0)
        sub = sub[20:]
        sub = sub.replace("\n", "")
    except:
        sub = ''
    
    invNo = re.search(r'Invoice/Payment Number.{4,7}',text)
    try:
        invNo = invNo.group(0)
        invNo = invNo[24:]
        invNo = invNo.replace("\n", "")
    except:
        invNo = ''
    
    amt = re.search(r'Payment Amount.{4,15}',text)
    
    try:
        amt = amt.group(0)
        amt = amt[16:]
        amt = amt.replace("\n", "")
    except:
        amt = ''
    
    toCompany = re.search(r'to\D{5,}on the job of',text)
    try:
        toCompany = toCompany.group(0)
        toCompany = toCompany[3:]
        ind = len(toCompany) - len(' on the job of')
        toCompany = toCompany[:ind]
        toCompany = toCompany.replace(",", "")
        toCompany = toCompany.replace(".", "")
        toCompany = toCompany.replace("\n", "")
    except:
        toCompany = ''
    
    print(lwType)
    print(sub)
    print(invNo)
    print(date)
    print(toCompany)
    createdName = lwType + " " + sub +  " " + invNo + " " + date + " " + toCompany + ".pdf"      
    if len(createdName) > 100:
        os.rename(file, file[:-4]+"notchanged.pdf")
        continue
    try:
        os.rename(file,createdName)
    except:
        continue

    
    



