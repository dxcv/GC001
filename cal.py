import numpy as np
import random

class Model:
    def __init__(self,a,b,r0,sigma,tradedays,strike,numberPaths):
        self.a=a
        self.b=b
        self.r0=r0
        self.sigma=sigma
        self.tradedays=tradedays
        self.strike=strike
        self.numberPaths=numberPaths
        self.callsimulation()
        self.putsimulation()
    def callsimulation(self):
        self.PathPrice=[]
        for j in range(self.numberPaths-1):
            self.r=[self.r0]
            for i in range(self.tradedays-1):
                self.r.append(self.r[-1]+self.a*(self.b-self.r[-1])+self.sigma*np.random.randn())
            temp=np.sum(self.r[1:])
            self.payoff=(temp/self.tradedays-self.strike)
            if(self.payoff>0):
                self.payoff=self.payoff*100.0
            else:
                self.payoff=0
            self.PathPrice.append(self.payoff*np.exp(-self.r[-1]*(self.tradedays/360)))
        self.callprice=np.mean(self.PathPrice)
    def putsimulation(self):
        self.PathPrice=[]
        for j in range(self.numberPaths-1):
            self.r=[self.r0]
            for i in range(self.tradedays-1):
                self.r.append(self.r[-1]+self.a*(self.b-self.r[-1])+self.sigma*np.random.randn())
            temp=np.sum(self.r[1:])
            self.payoff=(self.strike-temp/self.tradedays)
            if(self.payoff>0):
                self.payoff=self.payoff*100.0
            else:
                self.payoff=0
            self.PathPrice.append(self.payoff*np.exp(-self.r[-1]*(self.tradedays/360)))
        self.putprice=np.mean(self.PathPrice)
        
