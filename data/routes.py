import os
import pandas as pd
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, send_from_directory,send_file
from scrape import app,db
from scrape.models import data
import requests
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import sklearn
from sklearn.svm import SVR



ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET','POST'])
@app.route("/listingcsv", methods=['GET','POST'])
def listingcsv():
    
    file=os.listdir(os.path.abspath(os.path.dirname(__file__))+'/static/csv')
    return render_template('showcsv.html', file=file)
@app.route("/showcsv", methods=['GET','POST'])
def showcsv():
    if request.method=='GET':
        filename=request.args.get('filename')
        moy=request.args.get('moy')
        img=data.query.filter_by(name=filename.split('.csv')[0]).all()
        if img is None:
            dict2={}
        else:
            dict2={}
            for i in range(len(img)):
                dict2[i]=str(img[i]).split('=')[1].split(',')[0] 
        dict={}
        
        ds=pd.read_csv(os.path.abspath(os.path.dirname(__file__))+'/static/csv//'+filename)
        header=ds.columns

        for i in range(len(ds.values)):
            dict[i]=ds.values[i]
        
    return render_template('csv.html', form=dict,file=filename.split('.csv')[0],head=header,dict2=dict2,moy=moy)
@app.route("/savecsv", methods=['GET','POST'])
def savecsv():   
    if request.method=='GET':
        l=[]
        v=[]
        w=[]
        filename=request.args.get('filename')
        operation=request.args.get('operation')
        input1=request.args.get('input1')
        input2=request.args.get('input2')
        newcol=request.args.get('newcol')
        
        ds=pd.read_csv(os.path.abspath(os.path.dirname(__file__))+'/static/csv//'+filename+'.csv')
        for i in range(len(ds.loc[:,input1])):
           l.append(ds.loc[:,input1][i])
        for i in range(len(ds.loc[:,input2])):
           v.append(ds.loc[:,input2][i])
        if operation=='add':
          for i in range(len(l)):
           w.append(l[i]+v[i])
        if operation=='divide':
          for i in range(len(l)):
           w.append(l[i]/v[i])
        if operation=='multi':
          for i in range(len(l)):
           w.append(l[i]*v[i])
        if operation=='sous':
          for i in range(len(l)):
           w.append(l[i]-v[i])
        ds.insert(len(ds.columns),newcol,w) 
        ds.to_csv(os.path.abspath(os.path.dirname(__file__))+'/static/csv//'+filename+'modified.csv',index = False)


        plt.scatter([int(x.split('-')[2]) for x in ds.tail(15).loc[:,'Date']],[float(x) for x in ds.tail(15).loc[:,'High']])
        plt.ylabel('High')
        plt.xlabel('Date')
        plt.xticks([x for x in range(1,31)])
        plt.title('Date-High')
        plt.savefig('./scrape/static/'+filename+'datehigh.png')
        db.session.add(data(image=filename+'datehigh.png',name=filename+'modified'))
        db.session.commit()

    
        plt.scatter([int(x.split('-')[2]) for x in ds.tail(15).loc[:,'Date']],[float(x) for x in ds.tail(15).loc[:,'Volume']]) 
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.xticks([x for x in range(1,31)])
        plt.title('Date-Volume')
        plt.savefig('./scrape/static/'+filename+'datevolume.png')
        db.session.add(data(image=filename+'datevolume.png',name=filename+'modified'))
        db.session.commit()

    return redirect(url_for('showcsv',filename=filename+'modified.csv'))

@app.route('/uploadcsv', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('listingcsv'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
 if request.method=='GET':
        filename=request.args.get('filename')
        datex=int(str(request.args.get('datex')))
        dates =[]
        prices=[]
        
        ds=pd.read_csv(os.path.abspath(os.path.dirname(__file__))+'/static/csv//'+filename+'.csv')
        df_date=ds.tail(25).loc[:,'Date']
        df_open=ds.tail(25).loc[:,'Open']

        for date in df_date:
            dates.append([int(date.split('-')[2])])
        for open_price in df_open:
            prices.append(float(open_price))

        svr_lin=SVR(kernel='linear',C=1e3)
        svr_rbf=SVR(kernel='rbf',C=1e3,gamma=0.1)
        svr_poly=SVR(kernel='poly',C=1e3,degree=2)

        svr_lin.fit(dates,prices)
        svr_rbf.fit(dates,prices)
        svr_poly.fit(dates,prices)

        
        plt.scatter(dates,svr_rbf.predict(dates),c='blue',label='SVR RBF')
        plt.scatter(dates,svr_lin.predict(dates),c='red',label='SVR Linear')
        plt.scatter(dates,svr_poly.predict(dates),color='green',label='SVR Poly')
        
        plt.savefig('./scrape/static/'+filename+'dateprice.png')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Anylsis ML')
        db.session.add(data(image=filename+'dateprice.png',name=filename))
        db.session.commit()

        moy=(svr_rbf.predict([[datex]])[0]+svr_poly.predict([[datex]])[0]+svr_lin.predict([[datex]])[0])/3
        
        return redirect(url_for('showcsv',filename=filename+'.csv',moy=moy))


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = 'static//csv//'+filename
    return send_file(uploads,attachment_filename=filename)