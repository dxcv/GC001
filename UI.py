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
#import cal as cl

class Calculation(QWidget):
	def __init__(self):
		super(Calculation,self).__init__()

		self.CreateLabel()
		self.CreateEdit()
		self.CreateCombo()
		self.CreateButton()
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

		#self.lblCalculate=QLabel('开始计算',self)
		#self.lblReCalculate=QLabel('重置',self)
	def CreateButton(self):
		self.btnCalculate=QPushButton('开始计算',self)
		self.btnCalculate.clicked.connect(self.calculate)
		self.btnReCalculate=QPushButton('重置',self)
		self.btnReCalculate.clicked.connect(self.recalculate)
	def CreateEdit(self):
		self.UnderlyingCodeEdit=QLineEdit(self)
		self.UnderlyingNameEdit=QLineEdit(self)

		self.StrikeEdit=QLineEdit(self)

		self.UnderlyingPriceEdit=QLineEdit(self)
		self.OptionPriceEdit=QLineEdit(self)
	def CreateCombo(self):
		self.comboStartYear=QComboBox(self)
		self.comboEndYear=QComboBox(self)
		self.comboStartYear.addItem('')
		self.comboEndYear.addItem('')
		for i in range(2016,2020):
			self.comboStartYear.addItem(str(i))
			self.comboEndYear.addItem(str(i))
		
		self.comboStartMonth=QComboBox(self)
		self.comboEndMonth=QComboBox(self)
		self.comboStartMonth.addItem('')
		self.comboEndMonth.addItem('')
		for i in range(1,13):
			if len(str(i))==1:
				self.comboStartMonth.addItem(str(0)+str(i))
				self.comboEndMonth.addItem(str(0)+str(i))
			else:
				self.comboStartMonth.addItem(str(i))
				self.comboEndMonth.addItem(str(i))

		self.comboStartDay=QComboBox(self)
		self.comboEndDay=QComboBox(self)
		self.comboStartDay.addItem('')
		self.comboEndDay.addItem('')
		for i in range(1,32):
			if len(str(i))==1:
				self.comboStartDay.addItem(str(0)+str(i))
				self.comboEndDay.addItem(str(0)+str(i))
			else:
				self.comboStartDay.addItem(str(i))
				self.comboEndDay.addItem(str(i))
	
	def comboBoxAct(self):
		self.comboStartYear.activated[str].connect(self.onActivatedStartYear)
		self.comboStartMonth.activated[str].connect(self.onActivatedStartMonth)
		self.comboStartDay.activated[str].connect(self.onActivatedStartDay)
		
		self.comboEndYear.activated[str].connect(self.onActivatedEndYear)
		self.comboEndMonth.activated[str].connect(self.onActivatedEndMonth)
		self.comboEndDay.activated[str].connect(self.onActivatedEndDay)
	def EditChange(self):
		self.StrikeEdit.textChanged[str].connect(self.StrikeChange)
	def initUI(self):
		comboStartDate=QHBoxLayout()
		comboStartDate.addWidget(self.comboStartYear)
		comboStartDate.addWidget(self.comboStartMonth)
		comboStartDate.addWidget(self.comboStartDay)

		comboEndDate=QHBoxLayout()
		comboEndDate.addWidget(self.comboEndYear)
		comboEndDate.addWidget(self.comboEndMonth)
		comboEndDate.addWidget(self.comboEndDay)



		grid=QGridLayout()
		grid.addWidget(self.lblUnderlyingCode,0,0)
		grid.addWidget(self.UnderlyingCodeEdit,0,1)
		grid.addWidget(self.lblStartDate,0,2)
		grid.addLayout(comboStartDate,0,3)
		grid.addWidget(self.lblUnderlyingPrice,0,4)	
		grid.addWidget(self.UnderlyingPriceEdit,0,5)
		grid.addWidget(self.lblUnderlyingName,1,0)
		grid.addWidget(self.UnderlyingNameEdit,1,1)
		grid.addWidget(self.lblEndDate,1,2)
		grid.addLayout(comboEndDate,1,3)
		grid.addWidget(self.lblStrike,1,4)
		grid.addWidget(self.StrikeEdit,1,5)
		
		grid.addWidget(self.lblOptionPrice,2,0)
		grid.addWidget(self.OptionPriceEdit,2,1)
		
		grid.addWidget(self.btnCalculate,2,4)
		grid.addWidget(self.btnReCalculate,2,5)
		
		vbox=QVBoxLayout()
		vbox.addLayout(grid)
		self.setLayout(vbox)
		
		self.show()
		
		self.setWindowTitle('option calculation')
		self.setGeometry(300,300,900,300)

	def calculate(self):
		pass
	def recalculate(self):
		pass
	def onActivatedStartYear(self,StartYear):
		self.StartYear=StartYear
		self.StartDate=self.StartYear+self.StartDate[-4:]
	def onActivatedStartMonth(self,StartMonth):
		self.StartMonth=StartMonth
		self.StartDate=self.StartDate[:4]+self.StartMonth+self.StartDate[-2:]
	def onActivatedStartDay(self,StartDay):
		self.StartDay=StartDay
		self.StartDate=self.StartDate[:6]+self.StartDay

	def onActivatedEndYear(self,EndYear):
		self.EndYear=EndYear
		self.EndDate=self.EndYear+self.EndDate[-4:]
	def onActivatedEndMonth(self,EndMonth):
		self.EndMonth=EndMonth
		self.EndDate=self.EndDate[:4]+self.EndMonth+self.EndDate[-2:]
	def onActivatedEndDay(self,EndDay):
		self.EndDay=EndDay
		self.EndDate=self.EndDate[:6]+self.EndDay
	def StrikeChange(self):
		pass
if __name__=='__main__':
	#sns.set(color_codes=True)
	app=QApplication(sys.argv)
	ex=Calculation()
	sys.exit(app.exec_())




























