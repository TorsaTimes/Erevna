import cv2
import pytesseract
# import module
from pdf2image import convert_from_path
import os.path
from os import path
import os

# Validierung der drag and drop, explore search oder input field eingabe!!!!! 
# nach der Validierung der eingabe wird der txt ausgelesen und in einer variablen gespeichert. 
# diese variable wird dann in die funktion der passwort überprüfung gegeben.


list_of_filename = []

def check_file_ex(f):

      # Split the extension from the path and normalise it to lowercase.
      ext = os.path.splitext(f)[-1].lower()

      # Now we can simply use == to check for equality, no need for wildcards.
      if ext == ".pdf":
          print("is an pdf!")
          return "PDF"
      elif ext == ".png":
          print("is a png file!")
          return "PNG"
      elif ext == ".jpg":
        print("is a png file!")
        return "JPG"
      elif ext == ".txt":
          print("is a txt file!")
          return "TXT"
      else:
          print("is an unknown file format.")

def extract_file(f):
  print("HALLO bin drin")
  string_var = ""
  var = check_file_ex(f)
  print(var)
  pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  
  if var == "PDF":
    print("moin")
    # Store Pdf with convert_from_path function
    images = convert_from_path(f)
    counter = 0
    print("moin")
    for i in range(len(images)):
        print("moin FFF")  
        # Save pages as images in the pdf
        images[i].save('page'+ str(i) +'.png', 'PNG')
        counter = i
        
    print(" PNG generated")
    counter = counter + 1
    for x in range(0,counter):
      filename_var = "page" + str(x) + ".png"
      list_of_filename.append(filename_var)
      print(filename_var)
      if path.exists(filename_var):
        extract(filename_var)
      else:
        break
  elif var == "PNG":
    string_var = extract(f)
  
  elif var == "TXT":
        print("in text")
        file1 = open(f, "r+")
        print("txt write")
        string_var = file1.read()
  
  return string_var

def extract(filename):
  print("drin")
  img = cv2.imread(filename)
  text = pytesseract.image_to_string(img)
  print(text)
  print("############"+ filename +"###################")
  return text

def remove_files(f):
    print("WARUM" + " " + f)
    if os.path.exists(f):
        print("exist")
        os.remove(f)
    else:
        print("gibts nicht ")
