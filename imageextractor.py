import google.generativeai as genai
import cv2
from PIL import Image
import os
import numpy as np

def extract_text_image(image_path):
    file_bytes=np.asarray(bytearray(image_path.read()),dtype=np.uint8)
    image2=cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
    #image2=cv2.imread(image_path)
    image2=cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)
    image_grey=cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
    _,image_bw=cv2.threshold(image_grey,90,255,cv2.THRESH_BINARY)

    final_image=Image.fromarray(image_bw)

    key=os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=key)
    model=genai.GenerativeModel('gemini-2.5-flash-lite')

    promt='''You need to perform OCR on the given image and extract text from it
    Give only the text as output, do not give any other explanation or description.'''

    response=model.generate_content([promt,final_image])
    output_text=response.text
    return output_text