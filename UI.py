#encoding=utf-8

import sys
import matplotlib
import pandas as pd
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
from QuantLib import *
import cal as cl

class Calculation(QWidget):
	def __init__(self):
		super(Calculation,self).__init__()

		self.CreateLabel()
		self.CreateEdit()
		self.CreateCombo()
		self.CreateButton()
		self.CreateCalendar()
		self.comboBoxAct()
		self.EditChange()
		

		self.initUI()
	def CreateLabel(self):
		self.lblStartDate=QLabel('起始日期',self)
		self.lblEndDate=QLabel('结束日期',self)
		self.lblUnderlyingCode=QLabel('标的代码',self)
		self.lblUnderlyingName=QLabel('标的名称',self)
		self.lblStrike=QLabel('执行价格',self)
		self.lblUnderlyingPrice=QLabel('标的现价',self)

		self.lblOptionPrice=QLabel('期权价格',self)
		self.lblOptionType=QLabel('期权类型',self)

		#self.lblCalculate=QLabel('开始计算',self)
		#self.lblReCalculate=QLabel('重置',self)
	def CreateButton(self):
		self.btnCalculate=QPushButton('开始计算',self)
		self.btnCalculate.clicked.connect(self.btncalculate)
		self.btnReCalculate=QPushButton('重置',self)
		self.btnReCalculate.clicked.connect(self.btnrecalculate)

		self.btnStartDate=QPushButton('',self)
		self.btnStartDate.clicked.connect(self.btnStartDateChange)

		self.btnEndDate=QPushButton('',self)
		self.btnEndDate.clicked.connect(self.btnEndDateChange)
	def CreateEdit(self):
		self.UnderlyingCodeEdit=QLineEdit(self)
		self.UnderlyingCodeEdit.setText('204001')
		self.UnderlyingNameEdit=QLineEdit(self)
		self.UnderlyingNameEdit.setText('GC001')

		self.StrikeEdit=QLineEdit(self)

		self.UnderlyingPriceEdit=QLineEdit(self)
		self.OptionPriceEdit=QLineEdit(self)
	def CreateCombo(self):
	

		self.comboType=QComboBox(self)
		self.comboType.addItem('')
		self.comboType.addItem('call')
		self.comboType.addItem('put')
	def CreateCalendar(self):
		self.calStartDate=QCalendarWidget(self)
		self.calStartDate.hide()
		self.calEndDate=QCalendarWidget(self)
		self.calEndDate.hide()
	
	def comboBoxAct(self):

		self.comboType.activated[str].connect(self.onActivatedType)
	def EditChange(self):
		self.StrikeEdit.textChanged[str].connect(self.StrikeChange)
	def initUI(self):



		grid=QGridLayout()
		grid.addWidget(self.lblUnderlyingCode,0,0)
		grid.addWidget(self.UnderlyingCodeEdit,0,1)
		grid.addWidget(self.lblStartDate,0,2)
		grid.addWidget(self.btnStartDate,0,3)
		grid.addWidget(self.calStartDate,0,3)

		grid.addWidget(self.lblUnderlyingPrice,0,4)	
		grid.addWidget(self.UnderlyingPriceEdit,0,5)
		grid.addWidget(self.lblUnderlyingName,1,0)
		grid.addWidget(self.UnderlyingNameEdit,1,1)
		grid.addWidget(self.lblEndDate,1,2)
		grid.addWidget(self.btnEndDate,1,3)
		grid.addWidget(self.calEndDate,1,3)			
	
		grid.addWidget(self.lblStrike,1,4)
		grid.addWidget(self.StrikeEdit,1,5)
		
		grid.addWidget(self.lblOptionPrice,3,0)
		grid.addWidget(self.OptionPriceEdit,3,1)
		grid.addWidget(self.lblOptionType,2,0)
		grid.addWidget(self.comboType,2,1)		
		
		grid.addWidget(self.btnCalculate,3,4)
		grid.addWidget(self.btnReCalculate,3,5)
		
		vbox=QVBoxLayout()
		vbox.addLayout(grid)
		self.setLayout(vbox)
		
		self.show()
		
		self.setWindowTitle('option calculation')
		self.setGeometry(300,300,900,300)

	def btncalculate(self):
		parameters=cl.Paras()
		sigma=parameters.sigma[0]
		alpha=parameters.alpha[0]
		mu=parameters.mu[0]
		spot=parameters.GC.iloc[-1][0]

		min_=parameters.min
		optionType=self.OptionType
		strike=self.strike
		china_calendar=China()
		
		tradedays=china_calendar.businessDaysBetween(self.st_date,self.ed_date)

		ML=cl.Model(alpha,mu,spot,sigma,tradedays,strike,10000,optionType,min_)
		self.OptionPriceEdit.setText(str(ML.price))
	def btnrecalculate(self):
		self.OptionPriceEdit.setText('')
	def btnStartDateChange(self):
		self.calStartDate.show()
		self.calStartDate.setGridVisible(True)
		self.calStartDate.resize(2,2)
		self.calStartDate.clicked[QDate].connect(self.showStartDate)
		
	def showStartDate(self,date):
		txt=date.toString()
		year=int(txt[-4:])
		day=int(txt[-7:-5])
		if (txt[3:5][-1]==u'月'):
			month=int(txt[3])
		else:
			month=int(txt[3:5])
		self.st_date=Date(day,month,year)

		self.btnStartDate.setText(str(year)+'/'+str(month)+'/'+str(day))

		
		self.calStartDate.hide()
	def btnEndDateChange(self):
		self.calEndDate.show()
		self.calEndDate.setGridVisible(True)
		self.calEndDate.resize(2,2)
		self.calEndDate.clicked[QDate].connect(self.showEndDate)
		
		
	def showEndDate(self,date):
		txt=date.toString()
		year=int(txt[-4:])
		day=int(txt[-7:-5])
		if (txt[3:5][-1]==u'月'):
			month=int(txt[3])
		else:
			month=int(txt[3:5])
		self.ed_date=Date(day,month,year)
		
		self.btnEndDate.setText(str(year)+'/'+str(month)+'/'+str(day))
		self.calEndDate.hide()
		
		
		

	def onActivatedType(self,Type):
		self.OptionType=Type
	def StrikeChange(self,strike):
		self.strike=float(strike)
if __name__=='__main__':
	#sns.set(color_codes=True)
	app=QApplication(sys.argv)
	ex=Calculation()
	sys.exit(app.exec_())




























