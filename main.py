import numpy 
import matplotlib.pyplot as plt
import pickle as p
import time
import pandas as pd
import yfinance as yf
import datetime
from fpdf import FPDF
import pandas as pd


#Using two functions here to
#Using as a wallet to save the money
#Another to record the usage of every payment

#The date right now
# date = time.strftime('%Y%m%d')



def save_money(date):
	'''
	# Let the user save the amount of money
	# and usage to let the program know
	# and add to the previous section/balance
	'''
	# date = insert_date()
	sav_amt = float(input('The amount of money you would like to save: '))
	# print("Please insert the number for categories: ")
	# print("1-Housing\t2-Food\t3-Savings\n4-Transportation\t5-Other Expenses\t6-Free Spend")
	sav_comment =str("Savings")

	f = open('wallet.data','rb')
	balance = p.load(f)
	f.close()

	new_balance = balance+sav_amt

	f = open('wallet.data','wb')
	p.dump(new_balance,f,0)


	content = '%-12s%-8s%-8s%-10s%-25s\n'%(date,'N/A',sav_amt,new_balance,sav_comment)
	
	with open('record.txt','a+') as f:
		#a is append here to add records; can convert to pdf statement for user
		f.write(content)

	print(content)
		
def spend_money(balance_check,date):#Adding blance_cehck back
	'''
	This function tells you the money you spend
	and the category it is used 
	'''
	# date = insert_date()
	spend_amt = float(input('please insert the money you spend: '))
	print("Please insert the number for categories: ")
	print("1-Housing\t2-Food\t3-Savings\n4-Transportation\t5-Other Expenses\t6-Free Spend")
	spend_comment_dict = {1:"Housing",2:'Food',3:'Savings',4:'Transportation',5:'Other Expenses',6:'Free Spend'}
	s_input = int(input("What category this for: "))
	spend_cmt = spend_comment_dict[s_input]

	f = open('wallet.data','rb')
	balance = p.load(f)
	new_balance = balance - spend_amt
	f.close()

	f = open('wallet.data','wb')
	p.dump(new_balance,f,0)

	if new_balance <= 0:
		print("You need to save money now!")

	if new_balance <= balance_check:
			print("Attention: You spend more than your budget!!")

	with open('record.txt','a+') as f:
		content = '%-12s%-8s%-8s%-10s%-25s\n'%(date, spend_amt,'N/A',new_balance,spend_cmt)
		f.write(content)
	# list.append(content)
	print(content)

def query_info():
	# date = insert_date()
	with open('record.txt') as f:
		for line in f:
			print(line)

	line = '=' * 65
	content = '%s\n%-12s%-8s%-8s%-10s%-25s'%(line,'Date','Cost','Save','Balance','Comment')

	f = open('wallet.data','rb')
	new_balance = p.load(f)
	# with open('wallet.data') as f:
	# 	new_balance = p.load(f)
	print("\nThe new balance is: ")
	print(new_balance)
	# print(content)

	
			#Connect this to summary file 

# global date

# def insert_date():

#     # d = input("Select 1 to insert date or 2 to record today's date: ")
#     # if d == 1:
#     a = input("Please insert the date, yyyy-mm-dd: ")
#     # This could be the drop down menu or just simply user input
#     t = time.strptime(a, "%Y-%m-%d")
#     y, m, d = t[0:3]
#     date = datetime.datetime(y, m, d)
#     # elif d == 2:
#     #     date = time.strftime('%Y%m%d')
#     # else:
#     #     print("You can only select between 1 and 2! Please insert again!")
#     #     sys.exit()
#     return date


def init_txt():
	balance = 0.0
	line = '=' * 65
	content = '%-12s%-8s%-8s%-10s%-25s\n%s\n'%('Date','Cost','Save','Balance','Category',line)
	f = open('record.txt','w+')
	f.write(str(content))
	return

def to_csv():
	read_file = pd.read_csv('record.txt')
	a = read_file.to_csv('record.csv')
	df = pd.read_csv('record.csv',header = None)
	# print(df.head(2))
	# df = read_file.to_csv('record.csv',)
	# print(type(df))
	# df = pd.read_csv(r'record.dsv'))
	# df.columns[]
	# df_period = df.to_period('M')
	# df.columns = ['Date','Cost','Save','Balance','Category']
	# print(df.columns)
	# print(csv_file)
	# return csv_file


def save_pdf():
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size = 20)
	pdf.cell(200,10,txt = 'Summary for this month\n',ln=1,align = "C")
	pdf.set_font("Arial", size = 14)
	f = open("record.txt",'r')
	for x in f:
		pdf.cell(0,10,txt = x, ln = 1, align = True)
	pdf.output("Summary.pdf")


def show_menu():
	'''
	Let user input their budget and total income
	and if the balance is less than balance_check
	show warning message
	'''
	# date = insert_date()
	

	
	
	prompt = '''
	'0':'spend_money'
	'1':'save_money'
	'2':'query_info'
	'3':'quit'
	'''
	while True:
		date_entry = input("Enter a date in yyyy-mm-dd format: ")
		year, month, day = map(int,date_entry.split('-'))
		date = datetime.date(year,month,day)

		budget = float(input("Input the number of maximum spending this month: "))
		total_income = float(input('Input total income this month: '))
		balance_check = total_income - budget

		f = open('wallet.data','wb')
		p.dump(total_income,f,0)
		with open('record.txt','a+')as f:
			pass

		test = {'0':spend_money,'1':save_money,'2':query_info}
		choice = input("Please input the option: (0/1/2/3) %s"%prompt)

		if choice not in '0''1''2''3':
			print("Invalid Input, try again")
			continue
		elif choice == '3':
			break
		elif choice == '0':
			balance_check = balance_check
			test[choice](balance_check,date)
		elif choice == '1':
			test[choice](date)
		else:
			test[choice]()

def stock_live():
	'''
	This function showed the past 30 days live stock graph
	'''
	# list_stock = ["NDAQ",'DJI','INX','MSFT']
	
	print("input the number you would like to check: ")
	print("0: NDAQ -- Nasdaq")
	print("1: DJI -- Dow Jones Industrial Average")
	print("2: ^GSPC -- S&P 500 Index")
	print("3: MSFT -- Microsoft")
	num =int(input('\ninput number here: '))
	if num == 3: 
		msft = yf.Ticker("MSFT")
		#Get your stock infomation
		# print(msft.info)
		hist = msft.history(period = '30d')
		hist['Close'].plot(figsize=(16,9))
		plt.title("Microsoft")
		plt.ylabel("Dollar")
		plt.xlabel('Days')
		plt.show()
	elif num == 0:
		ndaq = yf.Ticker("NDAQ")
		hist = ndaq.history(period = '30d')
		hist['Close'].plot(figsize=(16,9))
		plt.title("Nasdaq")
		plt.ylabel("Dollar")
		plt.xlabel('Days')
		plt.show()
	elif num == 1:
		dji = yf.Ticker("DJI")
		hist = dji.history(period = '30d')
		hist['Close'].plot(figsize=(16,9))
		plt.title("Dow Jones Industrial Average")
		plt.ylabel("Dollar")
		plt.xlabel('Days')
		plt.show()
	elif num == 2:
		inx = yf.Ticker("^GSPC")
		hist = inx.history(period = '30d')
		hist['Close'].plot(figsize=(16,9))
		plt.title("S&P 500 Index")
		plt.ylabel("Dollar")
		plt.xlabel('Days')
		plt.show()


def init_view():
	model.view_application = view.init_view()
	#This connect to view.py to start the gui 
	view.init_menu_screen()
	#if we have a model.py
# class Parameters:
# 	view_application = ""

if __name__ =='__main__':
	to_csv()
	# init_txt()
	# show_menu()
	# save_pdf()
	# spend_money()
	# insert_date()
	# init_view()# This is help with the 
	# stock_live()
