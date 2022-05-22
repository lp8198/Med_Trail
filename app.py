# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

from flask import Flask, redirect,url_for,render_template,request
import pickle
import pandas as pd

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def welcome():
    return render_template('sample.html')


@app.route('/success/<float:score>')
def success(score):
    return render_template('final.html', result = int(score*100))

### Scoring
def scoring(data):
    with open("encoding.sav", 'rb') as f:
        encoding = pickle.load(f)
        
    with open("RF.sav", 'rb') as f:
        parameter = pickle.load(f)
        
    sel_var= ['Left Ventricle', 'PW(s) cms', 'IVS(s) cms', 'EF %', 'IVS(d) cms', 'PW(d) cms', 'Age', 'ESV ml', 'LVID(s) cms',  'Aortic Valve', 'LA cms', 'Mitral Valve A m/sec', 'Mitral Valve E m/sec', 'Mitral Valve Summary', 'Aortic Valve m/sec', 'EDV ml', 'LVID(d) cms', 'IVC', 'AO cms' ]        
    cats = ['Left Ventricle', 'Aortic Valve', 'Mitral Valve Summary','IVC']
    data[cats] = data[cats].fillna('Misc')
    data[cats] = encoding.transform(data[cats])
    predict_prob = parameter.predict_proba(data[sel_var].fillna(0))
    
    return predict_prob


### Result checker submit html page
@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        data = pd.DataFrame(columns = ['UHID', 'Left Ventricle', 'PW(s) cms', 'IVS(s) cms', 'EF %', 'IVS(d) cms', 'PW(d) cms', 'Age', 'ESV ml', 'LVID(s) cms', 'Aortic Valve', 'LA cms', 'Mitral Valve A m/sec', 'Mitral Valve E m/sec', 'Mitral Valve Summary', 'Aortic Valve m/sec', 'EDV ml','LVID(d) cms', 'IVC', 'AO cms'])
        a1= request.form['UHID']
        a2=request.form['Left Ventricle']
        a3=float(request.form['PW(s) cms'])
        a4=float(request.form['IVS(s) cms'])
        a5=float(request.form['EF %'])
        a6=float(request.form['IVS(d) cms'])
        a7=float(request.form['PW(d) cms'])
        a8=float(request.form['Age'])
        a9=float(request.form['ESV ml'])
        a10=float(request.form['LVID(s) cms'])
        a11=request.form['Aortic Valve']
        a12=float(request.form['LA cms'])
        a13=float(request.form['Mitral Valve A m/sec'])
        a14=float(request.form['Mitral Valve E m/sec'])
        a15=request.form['Mitral Valve Summary']
        a16=float(request.form['Aortic Valve m/sec'])
        a17=float(request.form['EDV ml'])
        a18=float(request.form['LVID(d) cms'])
        a19=request.form['IVC']
        a20=float(request.form['AO cms'])
        lis = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20]
 
        data.loc[0] = lis
        prob = scoring(data)
        val = prob[0][1]
    return redirect(url_for('success',score=val))

app.run()