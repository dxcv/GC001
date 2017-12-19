import numpy as np
import random
import pandas as pd
class Model:
	def __init__(self,a,b,r0,sigma,tradedays,strike,numberPaths,optiontype,min_):
		self.a=a
        	self.b=b
       		self.r0=r0
        	self.sigma=sigma
        	self.tradedays=tradedays
        	self.strike=strike
        	self.numberPaths=numberPaths
        	self.optiontype=optiontype
        	self.count=0.0
        	self.min_=min_
        	self.simulation()
	def simulation(self):
        	self.PathPrice=[]
        	for j in range(self.numberPaths-1):
            		self.r=[self.r0]
            		for i in range(self.tradedays-1):
                		temp=self.r[-1]+self.a*(self.b-self.r[-1])+self.sigma*np.sqrt(self.r[-1])*np.random.randn()
                		if temp>0:
                    			self.r.append(temp)
                		else:
                    			self.r.append(self.min_)
                    			self.count=self.count+1.0
            		temp=np.sum(self.r[1:])
            		if self.optiontype=='call':
                		self.payoff=(temp/self.tradedays-self.strike)
            		elif self.optiontype=='put':
                    		self.payoff=(self.strike-temp/self.tradedays)
            		else:
                		print 'enter the right option type'
            		if(self.payoff>0):
                		self.payoff=self.payoff*100.0
            		else:
                		self.payoff=0
            		self.PathPrice.append(self.payoff*np.exp(-self.r[-1]*(self.tradedays/360.0)))
        	self.price=np.mean(self.PathPrice)


class ETD:
    	def __init__(self,a,b,r0,sigma,tradedays,strike,numberPaths,OptionType):
        	self.a=a
        	self.b=b
        	self.r0=r0
        	self.sigma=sigma
        	self.tradedays=tradedays
        	self.strike=strike
        	self.d=4*b*a/(sigma**2)
        	self.numberPaths=numberPaths
        	self.OptionType=OptionType
        	if(self.d>1):
            		self.simulation_1()
        	else:
            		self.simulation_2()
    	def simulation_1(self):#d>1
        	c=(self.sigma**2)*(1-np.exp(-self.a))/(4*self.a)
        	print c
        	print self.d
        	self.PathPrice=[]
        	for j in range(self.numberPaths-1):
            		r=[self.r0]
            		for i in range(self.tradedays-1):
                		lambda_=r[-1]*np.exp(-self.a)/c
                		X=np.random.chisquare(self.d-1)
                		temp=(np.random.randn()+np.sqrt(lambda_))**2+X
                		r.append(c*temp)
            		temp_sum=np.sum(r[1:])
            		if self.OptionType=='call':
                		payoff=(temp_sum/self.tradedays-self.strike)
            		elif self.OptionType=='put':
                		payoff=(self.strike-temp_sum/self.tradedays)
            		else:
                		print 'enter the right option type'
            		if(payoff>0):
                		payoff=payoff*100
            		else:
                		payoff=0
            		self.PathPrice.append(payoff*np.exp(-r[-1]*(self.tradedays/360.0)))
            	#print j
        	self.price=np.mean(self.PathPrice)
       
    	def simulation_2(self):#d<=1
        	c=(self.sigma**2)*(1-np.exp(-self.a))/(4*self.a)
        	print c
        	print self.d
        	self.PathPrice=[]
        	for j in range(self.numberPaths-1):
            		r=[self.r0]
            		for i in range(self.tradedays-1):
                		lambda_=r[-1]*np.exp(-self.a)/c
                		N=st.poisson(lambda_/2)
                		X=self.Poisson_simulation(N)
                		r.append(c*X)
                		#print c*X
            		temp_sum=np.sum(r[1:])
            		#print temp_sum/self.tradedays
            		if self.OptionType=='call':
                		payoff=(temp_sum/self.tradedays-self.strike)
            		elif self.OptionType=='put':
               			payoff=(self.strike-temp_sum/self.tradedays)
            		else:
                		print 'enter the right option type'
            		if(payoff>0):
                		payoff=payoff*100.0
            		else:
                		payoff=0
            		self.PathPrice.append(payoff*np.exp(-r[-1]*(self.tradedays/360.0)))
            	#print j
        	self.price=np.mean(self.PathPrice)
    	def Poisson_simulation(self,N):
        	i=0
        	sum=0
       		while ((1-N.cdf(i))>0.05):
            		sum+=np.random.chisquare(self.d+2*i)*N.pmf(i)
            		i=i+1 
        	return sum

class Paras:
	def __init__(self):
		self.paras()
	def paras(self):
		data=pd.read_excel("GC001.xlsx")
		GC_index=pd.DatetimeIndex(data[3:].index)
		GC=pd.DataFrame(np.matrix(data[3:])/100.0,index=GC_index,columns=['spot'])
		self.GC=GC
		GC_average=np.mean(GC)
		GC_vol=np.std(GC)
		delta_T=np.sum(GC.diff(1)**2)
		self.sigma=np.sqrt(delta_T/(np.sum(GC[:-1])))
		self.mu=GC_average
		self.alpha=(self.sigma**2)*self.mu/(2*GC_vol)
		self.min=np.mean(GC)[0]

class LinearReg:
	def __init__(self):
		self.paras()
	def paras(self):
		data=pd.read_excel("GC001.xlsx")
		GC_index=pd.DatetimeIndex(data[3:].index)
		GC=pd.DataFrame(np.matrix(data[3:])/100.0,index=GC_index,columns=['spot'])
		self.GC=GC
		Y=self.diff_(GC.diff(1))/self.sqrt_(GC[:-1])
		X1=1.0/(self.sqrt_(GC[:-1]))
		X2=1.0/X1
		X1_=list(X1.values)
		X2_=list(X2.values)
		X_=np.hstack((X1_,X2_))
		Y_=list(Y.values)
		_paras=self.reg(X_,Y_)
		self.alpha=-_paras[1]
		self.mu=-_paras[0]/_paras[1]
		self.sigma=np.std(Y_-X_.dot(_paras))
	def sqrt_(self,A):
		temp=[]
		for i in A.values:
			temp.append(np.sqrt(i[0]))
		return pd.DataFrame(temp,index=A.index,columns=A.columns)
	def diff_(self,A):
		return pd.DataFrame(np.matrix(A[1:]),index=A.index[:-1],columns=A.columns)

	def reg(self,X,Y):
		temp1=X.T.dot(X)
		temp2=X.T.dot(Y)
		beta=(np.linalg.inv(temp1)).dot(temp2)
		return beta









