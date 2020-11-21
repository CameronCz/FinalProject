import numpy 
import matplotlib.pyplot as plt
import pickle as p
import time
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
import seaborn as sns
# from yahoo_fin import stock_info
# from plotly.offline import plot, init_notebook_mode
# init_notebook_mode()
# import cufflinks as cf
# %matplotlib inline
# cf.set_config_file(offline = True)

#Using two functions here to
#Using as a wallet to save the money
#Another to record the usage of every payment

#Here is initial value
date = time.strftime('%Y%m%d')
#Initial value on the account this month
# f = open('wallet.data','wb')
# p.dump(2000,f,0)
# with open('record.txt','wb')as f:
# 	pass
#Insert budget for this month 

# def basic_info():

# 	budget = input("Input the number of maximum spending this month: ")
# 	total_income = input('Input total income this month: ')
# 	balance_check = total_income - budget



def save_money():
	'''
	Let the user save the amount of money
	and usage to let the program know
	and add to the previous section/balance
	'''
	sav_amt = float(input('The amount of money you would like to save: '))
	sav_comment = input("Doing what: ")

	f = open('wallet.data','rb')
	balance = p.load(f)
	f.close()
	# with open('wallet.data') as f:
	# 	balance = p.load(f,encoding = 'bytes')

	new_balance = balance+sav_amt

	f = open('wallet.data','wb')
	p.dump(new_balance,f,0)
	# with open('wallet.data','wb') as f:
	# 	p.dump(new_balance,f)

	content = '%-12s%-8s%-8s%-10s%-25s\n'%(date,'N/A',sav_amt,new_balance,sav_comment)
	
	with open('record.txt','a') as f:
		#a is append here to add records; can convert to pdf statement for user
		f.write(content)

	print(content)
		
def spend_money(balance_check):
	'''
	This function tells you the money you spend
	and the category it is used 
	'''
	spend_amt = float(input('please insert the money you spend: '))
	spend_comment = input("What category this for: ")

	f = open('wallet.data','rb')
	balance = p.load(f)
	new_balance = balance - spend_amt
	f.close()
	# with open('wallet.data') as f:
	# 	balance = p.load(f, encoding = 'bytes')
	# new_balance = balance - spend_amt
	f = open('wallet.data','wb')
	p.dump(new_balance,f,0)
	# with open('wallet.data','wb') as f:
	# 	p.dump(new_balance,f)
	if new_balance <= balance_check:
			print("Attention: You spend more than your budget!!")

	with open('record.txt','a') as f:
		content = '%-12s%-8s%-8s%-10s%-25s\n'%(date, spend_amt,'N/A',new_balance,spend_comment)
	# list.append(content)
	print(content)

def query_info():
	line = '=' * 65
	content = '%s\n%-12s%-8s%-8s%-10s%-25s'%(line,'Date','Cost','Save','Balance','Comment')

	f = open('wallet.data','rb')
	new_balance = p.load(f)
	# with open('wallet.data') as f:
	# 	new_balance = p.load(f)
	print("The new balance is: ")
	print(new_balance)
	print(content)

	with open('record.txt') as f:
		for line in f:
			print(line)

def show_menu():
	'''
	Let user input their budget and total income
	and if the balance is less than balance_check
	show warning message
	'''
	budget = float(input("Input the number of maximum spending this month: "))
	total_income = float(input('Input total income this month: '))
	balance_check = total_income - budget

	f = open('wallet.data','wb')
	p.dump(total_income,f,0)
	with open('record.txt','wb')as f:
		pass
	
	prompt = '''
	'0':'spend_money'
	'1':'save_money'
	'2':'query_info'
	'3':'quit'
	'''
	while True:
		test = {'0':spend_money,'1':save_money,'2':query_info}
		choice = input("Please input the option: %s"%prompt)

		if choice == '3':
			break
		elif choice == '0':
			balance_check = balance_check
			test[choice](balance_check)
		else:
			test[choice]()

def stock_live():
	'''
	Gives 10 example of the live stock market
	for monthley information for each stock symbol
	'''
	from yahoo_fin import stock_info as si
	from plotly.offline import plot, init_notebook_mode
	init_notebook_mode()
	import cufflinks as cf
	#!!! Dont forget to install requests_html

	# %matplotlib inline
	cf.set_config_file(offline = True)
	# api_key = 'M4AC6SSMZQJKLEX1'
	# ts = TimeSeries(key = api_key, output_format = 'pandas')
	# data, meta_data = ts.get_monthly(symbol = 'MSFT')
	info1 = si.get_live_price('msft')
	print(info1)
	d_df = {}
	d_df['msft'] = si.get_data('msft', start_date='01/01/2020', end_date='03/01/2020')
	d_df['msft'].head()

	qf = cf.QuantFig(d_df['msft'])
	qf.add_bollinger_bands()
	qf.add_macd()
	qf.iplot()
	'''
	msft = yf.Ticker('MSFT')
	print(msft.info)
	hist = msft.history(period = '10d')
	hist['Close'].plot(figsize = (16,9))
	'''
	#Can also export the data to CSV
	# data_df = yf.download("AAPL",start = '2020-02-01', end = '2020-11-20')
	# data_df.to_csv('aapl.csv')

def stock_test():
	# list_stock = ["NDAQ",'DJI','INX','MSFT']
	
	# print("input the number you would like to check: ")
	# print("0: NDAQ -- Nasdaq")
	# print("1: DJI -- Dow Jones Industrial Average")
	# print("2: INX -- S&P 500 Index")
	# print("3: MSFT -- Microsoft")
	# num =int(input('\ninput number here: '))
	# if num == 3: 

	# msft = yf.Ticker("MSFT")
	# #Get your stock infomation
	# # print(msft.info)
	# hist = msft.history(period = '30d')
	# hist['Close'].plot(figsize=(16,9))
	# plt.title("Microsoft")
	# plt.ylabel("Dollar")
	# plt.xlabel('Days')
	# plt.show()
	# elif num == 0:
		# ndaq = yf.Ticker("NDAQ")
		# hist = ndaq.history(period = '30d')
		# hist['Close'].plot(figsize=(16,9))
		# plt.title("Nasdaq")
		# plt.ylabel("Dollar")
		# plt.xlabel('Days')
		# plt.show()
	# elif num == 1:
		# dji = yf.Ticker("DJI")
		# hist = dji.history(period = '30d')
		# hist['Close'].plot(figsize=(16,9))
		# plt.title("Dow Jones Industrial Average")
		# plt.ylabel("Dollar")
		# plt.xlabel('Days')
		# plt.show()
	# elif num == 2:
	# 	'''
	inx = yf.Ticker("INX")
	hist = inx.history(period = '30d')
	hist['Close'].plot(figsize=(16,9))
	plt.title("S&P 500 Index")
	plt.ylabel("Dollar")
	plt.xlabel('Days')
	plt.show()




if __name__ =='__main__':
	# show_menu()
	# stock_live()
	stock_test()







#
