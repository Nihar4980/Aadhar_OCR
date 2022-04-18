import pandas as pd
import numpy as np
import cv2
import pytesseract
import re
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
#from flask_ngrok  import run_with_ngrok

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
#run_with_ngrok(app)

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ocr-text',methods=['POST'])
def read():
    if (request.method=='POST'):
        front = request.files['front']
        back = request.files['back']
        file_name = front.filename
        file_name1 = back.filename

        front.save(os.path.join("static/images/", file_name))
        back.save(os.path.join("static/images/", file_name1))

        adhar_front_image = cv2.imread(file_name)
        print(adhar_front_image)
        ocr_front_text = pytesseract.image_to_string(adhar_front_image)

        adhar_back_image = cv2.imread(file_name1)
        print(adhar_back_image)
        ocr_back_text = pytesseract.image_to_string(adhar_back_image)

        adhar_number = re.findall("\w{4}\s\w{4}\s\w{4}", ocr_front_text )

        name = re.findall("\w{5}\s\w{6}\s\w{5}", ocr_front_text )
        first_name = name[0][0:12]
        last_name = name[0][13:]

        gender = None
        if 'Male' in ocr_front_text :
            gender = 'Male'
        else:
            gender = 'Female'

        ocr_dates = re.findall(r'\d{2}/\d{2}/\d{4}', ocr_front_text )
        date_of_birth = ocr_dates[1]

        # Address Extraction
        # Extract pattern to find word address in the text
        address_pattern = re.compile(r'Address')
        address_match = address_pattern.finditer(ocr_back_text)
        for i in address_match:
            print(i)
        address_text = ocr_back_text[120:182]
        address_split = address_text.split(' ')
        #
        address_first_part = address_split[0:3]
        address_last_part = address_split[3:8]
        address_last = ' '.join(address_last_part)

        pattern = r"[^a-zA-Z0-9]+"

        address_last_modified = re.sub(pattern, ' ', address_last)
        address_last_modified_split = address_last_modified.split(' ')

        address_final =  address_first_part + address_last_modified_split
        address = ' '.join(address_final)



        data = {'First_Name': name[0][0:12], 'Last_Name': name[0][13:], 'DOB': date_of_birth, 'Gender': gender,
                'Aadhar_Number': adhar_number, 'Address': address}

        df = pd.DataFrame(data).T
        result = 'Aadhar Details are: {}'.format(df)

        return render_template('results.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)



