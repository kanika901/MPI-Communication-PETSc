#!/usr/bin/env python3

# Author: Kanika Sood
# Date: April 17, 2017 

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pylab
import math

nproc_test = pd.read_csv('data/test.csv')


#nproc = [1,2,4,8,16,32,36,48,54,64,72] #change this to exclude test procs
def read_data(filename, type):
	test_procs = [36,54]
	data = pd.read_csv('data/'+ filename)
	solver_data = np.matrix(data)
	print(solver_data)
	X,Y = solver_data[:,0] , solver_data[:,1]

	if type == 'linear':
		return X,Y
	elif type == 'polynomial': 
		X1 = np.squeeze(np.asarray(solver_data[:,0]))
		Y1 = np.squeeze(np.asarray(solver_data[:,1]))
		return X1,Y1

def linear_modeling(filename):
	X,Y = read_data(filename, 'linear')
	
	regression_model = LinearRegression().fit(X,Y)
	#line intercept formula
	#y=mx+c 
	m = regression_model.coef_[0]
	c = regression_model.intercept_

	print('Function for the solver id: \n y = mx + c')
	print('m =',  m , 'and c = ', c, '\n') 

	nproc_test = pd.read_csv('data/test.csv')
	y_prediction=regression_model.predict(nproc_test)
	print("prediction --> ", y_prediction)
	plt.scatter(X,Y, color='green')
	plt.scatter(nproc_test,y_prediction, color='blue')
	plt.plot(X,Y,color='red')
	title = 'Linear Regression model for ' + filename

	plt.title(title, fontsize=18)
	plt.xlabel('Number of processors', fontsize=15)
	plt.ylabel('Number of iterations', fontsize=15)
	#pylab.show()
	plt.show()

def polynomial_modeling_cubic(filename):
	#degree of polynomial: 3
	X,Y = read_data(filename,'polynomial')
	poly3 = np.polyfit(X,Y,3)
	poly_cubic = np.poly1d(poly3)
	xp = np.linspace(0,200,100)
	p4 = np.poly1d(np.polyfit(X, Y, 4))
	poly3_plot = plt.plot(X,Y, '.', xp, poly_cubic(xp), '-', xp, p4(xp), '--')
	plt.ylim(0,10)
	title = 'Polynomial Regression model for ' + filename
	y_prediction = poly3.predict(nproc_test)
	print("prediction --> ", y_prediction)
	plt.scatter(X,Y, color='red')
	plt.scatter(nproc_test,y_prediction, color='blue')
	plt.title(title, fontsize=18)
	plt.xlabel('Number of processors', fontsize=15)
	plt.ylabel('Number of iterations', fontsize=15)
	plt.show()



def all_solvers():
	linear_modeling('CG-BJacobi.csv')
	linear_modeling('GMRES-BJacobi.csv')
	linear_modeling('BCGS-BJacobi.csv')
	linear_modeling('FGMRES-BJacobi.csv')
	linear_modeling('TFQMR-BJacobi.csv')
	linear_modeling('ex2CG-BJacobi.csv')
	linear_modeling('ex2GMRES-BJacobi.csv')
	linear_modeling('ex2BCGS-BJacobi.csv')
	linear_modeling('ex2FGMRES-BJacobi.csv')
	linear_modeling('ex2TFQMR-BJacobi.csv')

	
if __name__ == "__main__":
	all_solvers()
	polynomial_modeling_cubic('CG-BJacobi.csv')