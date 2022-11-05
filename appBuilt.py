import streamlit as st
import numpy as np
import pandas as pd
import pickle
import re
from nltk.stem.snowball import SnowballStemmer


model = pickle.load(open('phishing-link-detection.sav', 'rb'))
cv = pickle.load(open("vector.pickel", "rb"))

@st.cache()

def prediction(url):
    url = re.sub('[^a-zA-Z\ \n]', '.', url.lower())
    url =  re.sub('\.{1,}', ' ', url)
    url = url.split(' ')
    
    stemmer = SnowballStemmer("english")
    url = [stemmer.stem(word) for word in url]
    url = ' '.join(url)
    
    a_trans = cv.transform(pd.Series(url))
    model_pred = model.predict(a_trans)
    
    if model_pred == 1:
        pred='Warning! Site highly likely to be a phishing link! Proceed with caution!'
    else:
        pred='Great! Site is likely to be safe!'
    
    return pred

def main():

	apptitle = 'Detection'
	st.set_page_config(page_title=apptitle, page_icon='random', 
		layout= 'wide', initial_sidebar_state="expanded")
	# random icons in the browser tab

	# give a title to your app
	st.title('Phishing Link Detection')

	html_temp = """ <div style ="background-color:AntiqueWhite;padding:15px"> 
       <h1 style ="color:black;text-align:center;">A phishing link detection application</h1> 
       </div> <br/>"""
    #display the front end aspect
	st.markdown(html_temp, unsafe_allow_html = True)
    	# let us make infrastructure to provide inputs
	# we will add the inputs to side bar
	st.info('Click Assess button below')

	input_link = st.text_input('Enter your link here: ', 'http: suspicious phishing link')
	st.write('input suspicious link', input_link)
    
	result =""
	# assessment button
	if st.button("Predict"):
		assessment = prediction(input_link)
		if assessment == 'Great! Site is likely to be safe!':
			st.balloons()
		else:
			st.snow()
		st.success('**System assessment says:** {}'.format(assessment))


	st.success("App is working!!") # other tags include st.error, st.warning, st.help etc.

if __name__ == '__main__':
	main()




