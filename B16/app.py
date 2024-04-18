import pandas as pd
from flask import Flask,request, redirect, render_template, url_for

import pickle

app = Flask(__name__)
#IMPORTING THE MODEL FOR PREDICTING THE CHANCE OF ADMISSION
rnd_model = pickle.load(open('C:\\Users\\91939\\Desktop\\B16\\trained.pkl', 'rb'))
## THIS IS THE ROUTE THAT IS LOADED  AUTOMATICALLY WHEN WE RUN THE PROJECT AND CLICKS ON THE URL IN THE OUTPUT
@app.route('/')
def index():
    return render_template('index.html')

# AFTER ENTERING DETAILS AND CLIKING ON THE PREDICT BUTTON ,THIS IS THE ROUTE LOADED AND 
# IN  THIS  PREDICT METHOD FORM DATA IS RETRIVED ,CONVERTED INTO A DATAFRAME AND GIVEN AS INPUT TO THE TRAINDED MODEL THAT WE IMPORTED EARLIER . 
#AFTER THAT IT PRINTS THE CHANCE OF PROBABILITY ON THE SAME HTML PAGE 

@app.route('/predict', methods=['POST'])
def predict():
    GRE_Score = int(request.form['GRE Score'])
    TOEFL_Score = int(request.form['TOEFL Score'])
    University_Rating = int(request.form['University_Rating'])
    SOP = float(request.form['SOP'])
    LOR = float(request.form['LOR'])
    CGPA = float(request.form['CGPA'])
    Research = int(request.form['Research'])
    final_data = pd.DataFrame([[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research]])
    prediction = rnd_model.predict(final_data)  
    output = prediction[0]
    output=round(output*100)
    
    result=University_Rating
    return render_template('index.html', prediction_text=output)


#THIS ROUTE IS LOADED WHEN THE USER CLICKS ON THE RECOMEND UNIVERSITES BUTTON.ALSO IT RETRIVES THE RATING FROM THE FORM
#AND REDIRECTS THE BROWSER TO INDEX1.HTML ROUTE ALONG WITH A QUERY PARAMETER OUTPUT TO THE  INDEX1 METHOD IN /INDEX1.HTML ROUTE
#ALLTHE  ABOVE PROCESS EXECUTES IN THE BACKGROUND AND DIRECTLY OPEN /INDEX1.HTML ROUTE
@app.route('/rer', methods=[ 'POST'])
def rer():
    output=int(request.form['University_Rating'])
    return redirect(url_for('index1', output=output))
    
#IN THIS ROUTE UNIVERSITES DATA SET IS LOADED AND EACH RECORD IS CONVERTED INTO ADICTIONARY
# IN THAT THE RECORDS WHOSE RATING IS EQUAL THE VALUE OUTPUT ARE RETRIVED AND STORED IN A LIST
# THAT LIST CONTAINING THE DICTIONARIES ARE PASSED TO THE FILE INDEX1.HTML FILE IN THAT FILE UNIVERSITES ARE PRINTED IN TABLE 
@app.route('/index1.html')
def index1():
    # Load data from the Excel file
    df = pd.read_csv('C:\\Users\\91939\\Desktop\\B16\\universites1.csv')
    # Convert the DataFrame to a list of dictionaries
    universities = df.to_dict(orient='records')
    # Output  is Query parameter that is retrived from 
    output = int(request.args.get('output'))
    filtered_universities = [uni for uni in universities  if uni['University Rating']==output]
    return render_template('index1.html', universities=filtered_universities,rating=output)


if __name__ == '__main__':
    app.run(debug=True)








