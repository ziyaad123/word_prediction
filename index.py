from flask import Flask,render_template,request
from pdf2image import convert_from_path
from PIL import Image
import pytesseract as ts
import pandas as pd
import nltk
from fuzzywuzzy import fuzz
import operator
import numpy as np







app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    






@app.route('/htm',methods=['GET', 'POST'])
def htmpage():
    pdf = request.form['fileToUpload']
    images = convert_from_path(pdf)
    img1 = images[0]
    img2 = images[1]

    text1 = ts.image_to_string(img1)
    text2 = ts.image_to_string(img2)


    text1 = text1.replace('\n',' ')
    text1 = text1.replace('.',' ')

    a = text1.find('FINAL DIAGNOSIS')
    b = text1.find('HISTORY OF PRESENT ILLNESS')
    c = len('FINAL DIAGNOSIS')

    txt = text1[a+c:b]

    word_token = nltk.word_tokenize(txt)

    list1 = ['1','2','3','4','5','6','7','8','9','0']

    for i in range(len(txt)):
      if txt[i] in list1:
        txt = txt.replace(txt[i],'.')

    sent_token = nltk.sent_tokenize(txt)
    sent_token = sent_token[1:]

    for i in range(len(sent_token)):
      sent_token[i] = sent_token[i].replace('.','')


    diag_data = pd.read_csv('categories.csv')

    

    index_dict = {}
    for i in sent_token:
      list_ = []
        
      for j in diag_data['DIAG']:
          ratio = fuzz.token_sort_ratio(i,j)
          list_.append(ratio)
            
        
      index, value = max(enumerate(list_), key=operator.itemgetter(1))
       
      index_dict[index] = value
    
    
    x1 = []
    x2 = []
    x3 = []

    for i in index_dict.keys():
      x1.append(diag_data['CODE'].iloc[i])
      x2.append(diag_data['DIAG'].iloc[i])
      x3.append(index_dict[i])








    text2 = text2.replace('.',' ')
    text2 = text2.replace('\n',' ')

    a2 = text2.find('PROCEDURES')
    b2 = text2.find('LABORATORY')
    c2 = len('PROCEDURES')

    txt2 = text2[a2+c2:b2]
    word_token2 = nltk.word_tokenize(txt2)


    for i in range(len(txt2)):
      if txt2[i] in list1:
        txt2 = txt2.replace(txt2[i],'.')

    sent_token2 = nltk.sent_tokenize(txt2)

    for i in range(len(sent_token2)):
      sent_token2[i] = sent_token2[i].replace('.','')

    sent_token2 = list(filter(None, sent_token2))
    sent_token2 = sent_token2[1:]


    proc_data = pd.read_excel('CMS32_DESC_LONG_SHORT_SG.xlsx')


   

    index_dict2 = {}
    for i in sent_token2:
        list2_ = []
        
        for j in proc_data['LONG DESCRIPTION']:
            ratio = fuzz.token_sort_ratio(i,j)
            list2_.append(ratio)
            
        
        index, value = max(enumerate(list2_), key=operator.itemgetter(1))
        print(index,value)
        index_dict2[index] = value
    

    


    y1 = []
    y2 = []
    y3 = []

    for i in index_dict2.keys():
      y1.append(proc_data['PROCEDURE CODE'].iloc[i])
      y2.append(proc_data['LONG DESCRIPTION'].iloc[i])
      y3.append(index_dict2[i])

    
    
    return render_template('details.html',x1=x1,x2=x2,x3=x3,y1=y1,y2=y2,y3=y3)





if __name__ == "__main__":
    app.run(debug=True,port=8009)


