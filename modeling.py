import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pylab
import math


#nproc = [1,2,4,8,16,32,36,48,54,64,72]
def modeling(filename):

	data = pd.read_csv('data/'+ filename)
	solver_data = np.matrix(data)
	print(solver_data)
	X,Y = solver_data[:,0] , solver_data[:,1]
	regression_model = LinearRegression().fit(X,Y)
	#line intercept formula
	#y=mx+c 
	m = regression_model.coef_[0]
	c = regression_model.intercept_

	print('Function for CG+BJacobi: \n y = mx + c')
	print('m =',  m , 'and c = ', c, '\n') 

	nproc_test = pd.read_csv('data/test.csv')
	#nproc_test = [144]
	y_prediction=regression_model.predict(nproc_test)
	print("prediction --> ", y_prediction)
	#print(X,Y)
	plt.scatter(X,Y, color='green')
	plt.scatter(nproc_test,y_prediction, color='blue')
	plt.plot(X,Y,color='red')
	title = 'Linear Regression model for ' + filename

	plt.title(title, fontsize=18)
	plt.xlabel('Number of processors', fontsize=15)
	plt.ylabel('Number of iterations', fontsize=15)
	pylab.show()

def all_solvers():
	modeling('CG-BJacobi.csv')
	modeling('GMRES-BJacobi.csv')

all_solvers()