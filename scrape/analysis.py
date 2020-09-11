import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import csv


CF=pd.read_csv("C:\Users\Dhia\Desktop\AAPL.csv")


dates =[]
prices=[]

df_date=df.loc[:,'Date']
df_open=df.loc[:,'Open']




for date in df_dates:
    dates.append([int(date.split('-')[2])])
for open_price in df_open:
    prices.append(float(open_price))


def predict_price(dates,prices,x):
    svr_lin=SVR(kernel='linear',C=1e3)
    svr_poly=SVR(kernel='poly',C=1e3,degre=2)
    svr_rbf=SVR(kernel='rbf',C=1e3,gamma=0.1)

    svr_lin.fit(dates,prices)
    svr_poly.fit(dates,prices)
    svr_rbf.fit(dates,prices)

    lin_reg=linearRegression()
    lin_reg.fit(dates,prices)


    plt.scatter(dates,prices,color='balck',lable='Data')
    plt.plot(dates,svr_rbf.predict(dates),color='blue',label='SVR RBF')
    plt.plot(dates,svr_lin.predict(dates),color='red',label='SVR Linear')
    plt.plot(dates,svr_poly.predict(dates),color='green',label='SVR Poly')
    plt.plot(dates,lin_reg.predict(dates),color='orange',label='linear Reg')

    plt.xlabel('Date')
    plt.ylablel('Price')
    plt.title('Regression')
    plt.legend()
    plt.show()


    return svr_rbf.predict(x)[0],svr_poly.predict(x)[0],svr_lin.predict(x)[0],lin_reg.predict(x)[0]






predict_price=predict_price(dates,prices,[[30]])





print(predict_price)

  
  
   
    
    
