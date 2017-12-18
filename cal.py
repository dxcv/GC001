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














