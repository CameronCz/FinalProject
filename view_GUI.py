'''
Software Carpentry Final Project
Personal Finance GUI
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''
import sys
#We need sys so that we can pass argv to Qapplication
# from guicalc import *

# import main
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import yfinance as yf

import pickle
import os.path
from os import path


'''
Instalations
pip install PyQtChart
sys
widgets
core
gui
'''

'''
References
Window - https://www.learnpyqt.com/tutorials/creating-your-first-window/
Sliders - https://pythonprogramminglanguage.com/pyqt5-sliders/
Multiple Pages - https://stackoverflow.com/questions/56867107/how-to-make-a-multi-page-application-in-pyqt5
QStackedWidget - https://learndataanalysis.org/rotate-widgets-with-qstackedwidget-class/
BarGraph - https://codeloop.org/pyqtchart-how-to-create-barchart-in-pyqt5/
StackedBarGraph - https://doc.qt.io/qt-5/qtcharts-stackedbarchart-example.html
Layouts - https://www.learnpyqt.com/tutorials/layouts/
Layouts - http://zetcode.com/gui/pyqt5/layout/
Date - https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup
Date to text - https://doc.qt.io/qt-5/qdate.html
Drop Down Box - https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
Grid Width - https://doc.qt.io/qtforpython/PySide2/QtWidgets/QGridLayout.html
Make LCD - https://learndataanalysis.org/control-lcd-number-widget-with-a-slider-pyqt5-tutorial/
Refresh LCD - https://stackoverflow.com/questions/52015269/displaying-numbers-with-qlcdnumber-display-with-pyqt
Saving - https://www.jessicayung.com/how-to-use-pickle-to-save-and-load-variables-in-python/
Pickle dictionary - https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
Popups - https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/
LCD Color - https://stackoverflow.com/questions/52312768/change-qlcdnumber-colour-when-a-specific-value-is-read-using-pyqt5
Get combo box text - https://www.geeksforgeeks.org/pyqt5-getting-the-text-of-selected-item-in-combobox/
Update Dictionary - https://stackoverflow.com/questions/41063744/how-to-update-the-value-of-a-key-in-a-dictionary-in-python
Check if path exists - https://www.guru99.com/python-check-if-file-exists.html
Update Graph - https://stackoverflow.com/questions/59751779/update-chart-data-in-pyqt5
Refresh Grid - https://www.qtcentre.org/threads/14701-Trying-to-refresh-a-QGridLayout
'''

'''
General notes:
GUI is broken into 3 layers
Main layer - this is the layer of the GUI that the user
primarily uses. They can add their most recent expenses
on this layer, and their general spending is aggregated
here.
Budget Layer - this layer is for the user to create or edit
their budget. Here they input their income and adjust their
categorical spending based on their own needs
Checking Live Stock Layer - this layer helps you check the 
related live stock information for the past 30 days to help
manage your budget and investment
'''



class Main_Budget(QWidget):
    def __init__(self):
        super().__init__()

        self.lcdprice = QLCDNumber()
        self.lcdprice.display(0)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDateTime(QDateTime.currentDateTime())

        self.spend_cb = QComboBox()
        self.spend_cb.addItems(["housing", "food", "transportation",
                                "savings", "necessities", "fun_money"])

        # Bar Chart
        housing = QBarSet("Housing")
        food = QBarSet("Food")
        transportation = QBarSet("Transportation")
        savings = QBarSet("Savings")
        necessities = QBarSet("Necessities")
        fun_money = QBarSet("Fun Money")

        # Read monthly values for each category
        month_name_today = self.date_edit.date().toString("MMMM")
        if month_name_today == "December":
            self.months_list = ["October", "November", "December"]
        elif month_name_today == "November":
            self.months_list = ["September", "October", "November"]
        elif month_name_today == "October":
            self.months_list = ["August", "September", "October"]
        elif month_name_today == "September":
            self.months_list = ["July", "August", "September"]
        elif month_name_today == "August":
            self.months_list = ["June", "July", "August"]
        elif month_name_today == "July":
            self.months_list = ["May", "June", "July"]
        elif month_name_today == "June":
            self.months_list = ["April", "May", "June"]
        elif month_name_today == "May":
            self.months_list = ["March", "April", "May"]
        elif month_name_today == "April":
            self.months_list = ["February", "March", "April"]
        elif month_name_today == "March":
            self.months_list = ["January", "February", "March"]
        elif month_name_today == "February":
            self.months_list = ["December", "January", "February"]
        elif month_name_today == "January":
            self.months_list = ["November", "December", "January"]

        month3_dict = {'housing': 0,
                        'food': 0,
                        'transportation': 0,
                        'savings': 0,
                        'necessities': 0,
                        'fun_money': 0}

        month2_dict = {'housing': 0,
                        'food': 0,
                        'transportation': 0,
                        'savings': 0,
                        'necessities': 0,
                        'fun_money': 0}

        month1_dict = {'housing': 0,
                        'food': 0,
                        'transportation': 0,
                        'savings': 0,
                        'necessities': 0,
                        'fun_money': 0}

        if path.exists(self.months_list[2] + ".pickle"):
                with open(self.months_list[2] + ".pickle", 'rb') as handle:
                    month3_dict = pickle.load(handle)
                    # month3_dict = December["housing"]
                    # December[combo_box_text] += int(self.lcdprice.value())
                # with open(self.months_list[2] + ".pickle", 'wb') as handle:
                #     pickle.dump(December, handle,
                #                 protocol=pickle.HIGHEST_PROTOCOL)

        if path.exists(self.months_list[1] + ".pickle"):
                with open(self.months_list[1] + ".pickle", 'rb') as handle:
                    month2_dict = pickle.load(handle)
                    # month2_dict = December["housing"]
                    # December[combo_box_text] += int(self.lcdprice.value())
                # with open(self.months_list[1] + ".pickle", 'wb') as handle:
                #     pickle.dump(December, handle,
                #                 protocol=pickle.HIGHEST_PROTOCOL)

        if path.exists(self.months_list[0] + ".pickle"):
                with open(self.months_list[0] + ".pickle", 'rb') as handle:
                    month1_dict = pickle.load(handle)
                    # month1_dict = December["housing"]
                    # December[combo_box_text] += int(self.lcdprice.value())
                # with open(self.months_list[0] + ".pickle", 'wb') as handle:
                #     pickle.dump(December, handle,
                #                 protocol=pickle.HIGHEST_PROTOCOL)

        housing << month1_dict["housing"] << month2_dict["housing"] << month3_dict["housing"]
        food << month1_dict["food"] << month2_dict["food"] << month3_dict["food"]
        transportation << month1_dict["transportation"] << month2_dict["transportation"] << month3_dict["transportation"]
        savings << month1_dict["savings"] << month2_dict["savings"] << month3_dict["savings"]
        necessities << month1_dict["necessities"] << month2_dict["necessities"] << month3_dict["necessities"]
        fun_money << month1_dict["fun_money"] << month2_dict["fun_money"] << month3_dict["fun_money"]

        self.spend_data = QPercentBarSeries()
        # self.spend_data = QBarSeries()
        # self.spend_data = QStackedBarSeries()
        self.spend_data.append(housing)
        self.spend_data.append(food)
        self.spend_data.append(transportation)
        self.spend_data.append(savings)
        self.spend_data.append(necessities)
        self.spend_data.append(fun_money)

        self.monthly_spend_c = QChart()
        self.monthly_spend_c.createDefaultAxes()
        self.monthly_spend_c.addSeries(self.spend_data)
        self.monthly_spend_c.setTitle("Monthly Spending Percentages")
        self.monthly_spend_c.setAnimationOptions(QChart.SeriesAnimations)

        self.axis = QBarCategoryAxis()
        self.axis.append(self.months_list)
        self.monthly_spend_c.setAxisX(self.axis, self.spend_data)
        # self.monthly_spend_c_View = QChartView(self.monthly_spend_c)
        # self.monthly_spend_c_View.setRenderHint(QPainter.Antialiasing)
        self.monthly_spend_c = QChartView(self.monthly_spend_c)
        self.monthly_spend_c.setRenderHint(QPainter.Antialiasing)

        # LCDs for main page lcdm
        if path.exists("budget.pickle"):
                with open("budget.pickle", 'rb') as handle:
                    month_budget = pickle.load(handle)

        # lcdm = lcd main
        # lcdmt = lcd main total allowed spending for the month

        self.lcdm_h = QLCDNumber()
        self.lcdm_h.display(month3_dict["housing"])
        self.lcdmt_h = QLCDNumber()
        self.lcdmt_h.display(month_budget["housing"])

        self.lcdm_f = QLCDNumber()
        self.lcdm_f.display(month3_dict["food"])
        self.lcdmt_f = QLCDNumber()
        self.lcdmt_f.display(month_budget["food"])

        self.lcdm_t = QLCDNumber()
        self.lcdm_t.display(month3_dict["transportation"])
        self.lcdmt_t = QLCDNumber()
        self.lcdmt_t.display(month_budget["transportation"])

        self.lcdm_s = QLCDNumber()
        self.lcdm_s.display(month3_dict["savings"])
        self.lcdmt_s = QLCDNumber()
        self.lcdmt_s.display(month_budget["savings"])

        self.lcdm_n = QLCDNumber()
        self.lcdm_n.display(month3_dict["necessities"])
        self.lcdmt_n = QLCDNumber()
        self.lcdmt_n.display(month_budget["necessities"])

        self.lcdm_fm = QLCDNumber()
        self.lcdm_fm.display(month3_dict["fun_money"])
        self.lcdmt_fm = QLCDNumber()
        self.lcdmt_fm.display(month_budget["fun_money"])

        self.lcdm_income = QLCDNumber()
        self.lcdm_income.display(month_budget["income"])

        self.lcdm_spent = QLCDNumber()
        self.lcdm_spent.display(self.lcdm_h.value() + self.lcdm_f.value() +
                                self.lcdm_t.value() + self.lcdm_s.value() +
                                self.lcdm_n.value() + self.lcdm_fm.value())


        # Set up Grid layout
        self.grid = QGridLayout()
        self.grid.addWidget(self.add_text("Information"), 0, 0)
        self.grid.addWidget(self.add_text("Input Expense"), 0, 1)

        self.grid.addWidget(self.add_text("Date"), 1, 0)
        self.grid.addWidget(self.date_edit, 1, 1)

        self.grid.addWidget(self.add_text("Price"), 2, 0)
        self.grid.addWidget(self.lcdprice, 2, 1)

        self.grid.addWidget(self.price_input(), 3, 0, 1, 2)

        self.grid.addWidget(self.add_text("Category"), 4, 0)
        self.grid.addWidget(self.spend_cb, 4, 1)

        self.grid.addWidget(self.add_text("Confirm"), 5, 0)
        self.grid.addWidget(self.save_expense(), 5, 1)

        self.grid.addWidget(self.add_text("Category"), 0, 2)
        self.grid.addWidget(self.add_text("Current Spending"), 0, 3)
        self.grid.addWidget(self.add_text("Total Budget"), 0, 4)
        self.grid.addWidget(self.add_text("Total Monthly Income"), 0, 5)
        self.grid.addWidget(self.lcdm_income, 1, 5)
        self.grid.addWidget(self.add_text("Total Spent this Month"), 2, 5)
        self.grid.addWidget(self.lcdm_spent, 3, 5)

        self.grid.addWidget(self.add_text("Housing"), 1, 2)
        self.grid.addWidget(self.lcdm_h, 1, 3)
        self.grid.addWidget(self.lcdmt_h, 1, 4)

        self.grid.addWidget(self.add_text("Food"), 2, 2)
        self.grid.addWidget(self.lcdm_f, 2, 3)
        self.grid.addWidget(self.lcdmt_f, 2, 4)

        self.grid.addWidget(self.add_text("Transportation"), 3, 2)
        self.grid.addWidget(self.lcdm_t, 3, 3)
        self.grid.addWidget(self.lcdmt_t, 3, 4)

        self.grid.addWidget(self.add_text("Savings"), 4, 2)
        self.grid.addWidget(self.lcdm_s, 4, 3)
        self.grid.addWidget(self.lcdmt_s, 4, 4)

        self.grid.addWidget(self.add_text("Necessities"), 5, 2)
        self.grid.addWidget(self.lcdm_n, 5, 3)
        self.grid.addWidget(self.lcdmt_n, 5, 4)

        self.grid.addWidget(self.add_text("Fun Money"), 6, 2)
        self.grid.addWidget(self.lcdm_fm, 6, 3)
        self.grid.addWidget(self.lcdmt_fm, 6, 4)

        # self.grid.addWidget(self.current_spend_c, 6, 0, 1, 2)
        self.grid.addWidget(self.monthly_spend_c, 7, 0, 1, 6)

        self.setLayout(self.grid)


    def add_text(self, line_text):
        text = QLabel()
        text.setText(line_text)
        return text

    def price_input(self):
        slider_price = QSlider(Qt.Horizontal)
        slider_price.setFocusPolicy(Qt.StrongFocus)
        slider_price.setTickPosition(QSlider.TicksBothSides)
        slider_price.setMaximum(2000)
        slider_price.setMinimum(0)
        slider_price.setTickInterval(100)
        slider_price.setSingleStep(1)
        slider_price.setSliderPosition(0)
        slider_price.valueChanged.connect(self.updateLCDprice)
        return slider_price
        # return price

    def updateLCDprice(self, event):
        # print(event)
        self.lcdprice.setStyleSheet("""QLCDNumber { 
                                                    background-color: black; 
                                                    color:  white; }""")
        self.lcdprice.display(event)

    # def updateLCDm_spent(self, event):
    #     # print(event)
    #     current_total = self.lcdm_spent.value()
    #     event = int(self.lcdprice.value() + self.lcdm_spent.value())
    #     self.lcdm_spent.display(event)

    def save_expense(self):
        save_e_button = QPushButton('Save Expense')
        save_e_button.clicked.connect(self.save_expense_click)
        # month_name = self.date_edit.date().toString("MMMM")

        return save_e_button


    def save_expense_click(self):
        expense_save = {'housing': 0,
                        'food': 0,
                        'transportation': 0,
                        'savings': 0,
                        'necessities': 0,
                        'fun_money': 0}

        month_name = self.date_edit.date().toString("MMMM")
        combo_box_text = self.spend_cb.currentText()

        # Connect save Expense to LCDs
        # if month_name == self.date_edit.date().toString("MMMM"):
        #     print("hi")
        #     current_total = self.lcdm_spent.value()
        #     event = int(self.lcdprice.value() + self.lcdm_spent.value())
        #     self.lcdm_spent.display(event)

            # print("hi")
            # save_e_button.clicked.connect(self.updateLCDm_spent)

        # Save the expense using pickle
        if month_name == "December":
            if path.exists("December.pickle"):
                with open('December.pickle', 'rb') as handle:
                    December = pickle.load(handle)
                    December[combo_box_text] += int(self.lcdprice.value())
                with open('December.pickle', 'wb') as handle:
                    pickle.dump(December, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                December = expense_save
                December[combo_box_text] += int(self.lcdprice.value())
                with open('December.pickle', 'wb') as handle:
                    pickle.dump(December, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
        elif month_name == "November":
            if path.exists("November.pickle"):
                with open('November.pickle', 'rb') as handle:
                    November = pickle.load(handle)
                    November[combo_box_text] += int(self.lcdprice.value())
                with open('November.pickle', 'wb') as handle:
                    pickle.dump(November, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                November = expense_save
                November[combo_box_text] += int(self.lcdprice.value())
                with open('November.pickle', 'wb') as handle:
                    pickle.dump(November, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "October":
            if path.exists("October.pickle"):
                with open('October.pickle', 'rb') as handle:
                    October = pickle.load(handle)
                    October[combo_box_text] += int(self.lcdprice.value())
                with open('October.pickle', 'wb') as handle:
                    pickle.dump(October, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                October = expense_save
                October[combo_box_text] += int(self.lcdprice.value())
                with open('October.pickle', 'wb') as handle:
                    pickle.dump(October, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "September":
            if path.exists("September.pickle"):
                with open('September.pickle', 'rb') as handle:
                    September = pickle.load(handle)
                    September[combo_box_text] += int(self.lcdprice.value())
                with open('September.pickle', 'wb') as handle:
                    pickle.dump(September, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                September = expense_save
                September[combo_box_text] += int(self.lcdprice.value())
                with open('September.pickle', 'wb') as handle:
                    pickle.dump(September, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "August":
            if path.exists("August.pickle"):
                with open('August.pickle', 'rb') as handle:
                    August = pickle.load(handle)
                    August[combo_box_text] += int(self.lcdprice.value())
                with open('August.pickle', 'wb') as handle:
                    pickle.dump(August, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                August = expense_save
                August[combo_box_text] += int(self.lcdprice.value())
                with open('August.pickle', 'wb') as handle:
                    pickle.dump(August, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "July":
            if path.exists("July.pickle"):
                with open('July.pickle', 'rb') as handle:
                    July = pickle.load(handle)
                    July[combo_box_text] += int(self.lcdprice.value())
                with open('July.pickle', 'wb') as handle:
                    pickle.dump(July, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                July = expense_save
                July[combo_box_text] += int(self.lcdprice.value())
                with open('July.pickle', 'wb') as handle:
                    pickle.dump(July, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "June":
            if path.exists("June.pickle"):
                with open('June.pickle', 'rb') as handle:
                    June = pickle.load(handle)
                    June[combo_box_text] += int(self.lcdprice.value())
                with open('June.pickle', 'wb') as handle:
                    pickle.dump(June, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                June = expense_save
                June[combo_box_text] += int(self.lcdprice.value())
                with open('June.pickle', 'wb') as handle:
                    pickle.dump(June, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "May":
            if path.exists("May.pickle"):
                with open('May.pickle', 'rb') as handle:
                    May = pickle.load(handle)
                    May[combo_box_text] += int(self.lcdprice.value())
                with open('May.pickle', 'wb') as handle:
                    pickle.dump(May, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                May = expense_save
                May[combo_box_text] += int(self.lcdprice.value())
                with open('May.pickle', 'wb') as handle:
                    pickle.dump(May, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "April":
            if path.exists("April.pickle"):
                with open('April.pickle', 'rb') as handle:
                    April = pickle.load(handle)
                    April[combo_box_text] += int(self.lcdprice.value())
                with open('April.pickle', 'wb') as handle:
                    pickle.dump(April, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                April = expense_save
                April[combo_box_text] += int(self.lcdprice.value())
                with open('April.pickle', 'wb') as handle:
                    pickle.dump(April, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "March":
            if path.exists("March.pickle"):
                with open('March.pickle', 'rb') as handle:
                    March = pickle.load(handle)
                    March[combo_box_text] += int(self.lcdprice.value())
                with open('March.pickle', 'wb') as handle:
                    pickle.dump(March, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                March = expense_save
                March[combo_box_text] += int(self.lcdprice.value())
                with open('March.pickle', 'wb') as handle:
                    pickle.dump(March, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)

        elif month_name == "February":
            if path.exists("February.pickle"):
                with open('February.pickle', 'rb') as handle:
                    February = pickle.load(handle)
                    February[combo_box_text] += int(self.lcdprice.value())
                with open('February.pickle', 'wb') as handle:
                    pickle.dump(February, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                February = expense_save
                February[combo_box_text] += int(self.lcdprice.value())
                with open('February.pickle', 'wb') as handle:
                    pickle.dump(February, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
        elif month_name == "January":
            if path.exists("January.pickle"):
                with open('January.pickle', 'rb') as handle:
                    January = pickle.load(handle)
                    January[combo_box_text] += int(self.lcdprice.value())
                with open('January.pickle', 'wb') as handle:
                    pickle.dump(January, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                January = expense_save
                January[combo_box_text] += int(self.lcdprice.value())
                with open('January.pickle', 'wb') as handle:
                    pickle.dump(January, handle,
                                protocol=pickle.HIGHEST_PROTOCOL)
        filename = month_name
        instance = Budget_Maker()            
        with open(filename + '.pickle', 'rb') as handle:
            b = pickle.load(handle)
        # print(b.values())
        if sum(b.values()) >= instance.lcdi.value():
            #it will still save the money
            error_gui("You spend more than your income this month!")

        return

def error_gui(error_msg):
    MessageScreen(QMessageBox.Critical,"An Error Occured!",error_msg)

class MessageScreen(QWidget):

    def __init__(self, message_type, title, message):
        super().__init__()

        self.move_to_centre()

        error_box = QMessageBox(self)
        error_box.setIcon(message_type)
        error_box.setText(title)

        error_box.setInformativeText(str(message))
        error_box.addButton(QMessageBox.Ok)

        error_box.setDefaultButton(QMessageBox.Ok)
        ret = error_box.exec_()

        if ret == QMessageBox.Ok:
            return

    def move_to_centre(self):
        resolution = QDesktopWidget().screenGeometry()

        width = resolution.width() / 2
        height = resolution.height() / 2

        frame_width = self.frameSize().width() / 2
        frame_height = self.frameSize().height() / 2

        self.move(width - frame_width, height - frame_height)

class Stock_Maker(QWidget):
    #Put everything we wrote in main.py about live stock info to here 
    def __init__(self):
        super().__init__()
        self.sc_im_label = QLabel()
        self.main_layout = QVBoxLayout()
        self.init_page()


    def init_page(self):
        #Start here putting 4 stocks live to the current GUI page
        

        id_label = QLabel("Please select an option:")

        nasdaq_button = QPushButton('Nasdaq Stock Daily Info', self)
        nasdaq_button.clicked.connect(self.nasdaq_button_is_pressed)

        dji_button = QPushButton('Dow Johns Industrial Average Stock Daily Info', self)
        dji_button.clicked.connect(self.dji_button_is_pressed)

        sp500_button = QPushButton('S&P 500 Index Stock Daily Info', self)
        sp500_button.clicked.connect(self.sp500_button_is_pressed)
        
        msft_button = QPushButton('Microsoft Stock Daily Info',self)
        msft_button.clicked.connect(self.msft_button_is_pressed)

        sc_im_map = QPixmap("sc.png")
        self.sc_im_label.setPixmap(sc_im_map)
        self.sc_im_label.show()

        im_layout = QGridLayout()
        im_layout.addWidget(self.sc_im_label,0,0)
        # im_layout.addStretch(1)

        nasdaq_layout = QGridLayout()
        nasdaq_layout.addWidget(nasdaq_button, 0, 0)

        dji_layout = QGridLayout()
        dji_layout.addWidget(dji_button, 0, 0)

        sp500_layout = QGridLayout()
        sp500_layout.addWidget(sp500_button, 0, 0)
        
        msft_layout = QGridLayout()
        msft_layout.addWidget(msft_button, 0, 0)

        id_layout = QGridLayout()
        id_layout.addWidget(id_label, 0, 0)


        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        # buttons_layout.addWidget(exit_button)

        
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(im_layout)
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(id_layout)
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(nasdaq_layout)
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(dji_layout)
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(sp500_layout)
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(msft_layout)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(buttons_layout)
        self.setLayout(self.main_layout)
    
    def nasdaq_button_is_pressed(self):
        ndaq = yf.Ticker("NDAQ")
        hist = ndaq.history(period = '30d')
        hist['Close'].plot(figsize=(16,9))
        plt.title("Nasdaq Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def dji_button_is_pressed(self):
        dji = yf.Ticker("DJI")
        hist = dji.history(period = '30d')
        hist['Close'].plot(figsize=(16,9))
        plt.title("Dow Jones Industrial Average Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def sp500_button_is_pressed(self):
        inx = yf.Ticker("^GSPC")
        hist = inx.history(period = '30d')
        hist['Close'].plot(figsize=(16,9))
        plt.title("S&P 500 Index Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def msft_button_is_pressed(self):
        msft = yf.Ticker("MSFT")
        #Get your stock infomation
        # print(msft.info)
        hist = msft.history(period = '30d')
        hist['Close'].plot(figsize=(16,9))
        plt.title("Microsoft Stock Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())


class Budget_Maker(QWidget):
    def __init__(self):
        super().__init__()

        # make LCDs
        self.lcdi = QLCDNumber()
        self.lcdi.display(2000)

        # Housing LCDs
        self.lcdh = QLCDNumber()
        self.lcdh.display(35)
        self.lcdh_d = QLCDNumber()
        self.lcdh_d.display(700)

        # Food LCDs
        self.lcdf = QLCDNumber()
        self.lcdf.display(15)
        self.lcdf_d = QLCDNumber()
        self.lcdf_d.display(300)

        # Transportation LCDs
        self.lcdt = QLCDNumber()
        self.lcdt.display(15)
        self.lcdt_d = QLCDNumber()
        self.lcdt_d.display(300)

        # Savings LCDs
        self.lcds = QLCDNumber()
        self.lcds.display(15)
        self.lcds_d = QLCDNumber()
        self.lcds_d.display(300)

        # Necessities LCDS
        self.lcdn = QLCDNumber()
        self.lcdn.display(15)
        self.lcdn_d = QLCDNumber()
        self.lcdn_d.display(300)

        # Fun Money LCDs
        self.lcdfm = QLCDNumber()
        self.lcdfm.display(5)
        self.lcdfm_d = QLCDNumber()
        self.lcdfm_d.display(100)

        self.lcdtotal = QLCDNumber()
        self.lcdtotal.display(100)

        grid = QGridLayout()
        grid.addWidget(self.add_text("Input Monthly Income $"), 1, 0)
        grid.addWidget(self.slider_income(2000), 1, 1)
        grid.addWidget(self.lcdi, 1, 3)
        # grid.addWidget(self.income_input(), 0, 1)

        # grid.addWidget(self.generate_budget(), 1, 0, 1, 2)
        grid.addWidget(self.add_text("Category"), 0, 0)
        grid.addWidget(self.add_text("Adjust Slider"), 0, 1)
        # grid.addWidget(self.add_text("Percentage"), 0, 2)
        grid.addWidget(QPushButton(f'Percentage'), 0, 2)
        # grid.addWidget(self.add_text("Dollars"), 0, 3)
        grid.addWidget(QPushButton(f'Dollars'), 0, 3)

        grid.addWidget(self.add_text("Housing"), 2, 0)
        grid.addWidget(self.slider_housing(35), 2, 1)
        grid.addWidget(self.lcdh, 2, 2)
        grid.addWidget(self.lcdh_d, 2, 3)

        grid.addWidget(self.add_text("Food"), 3, 0)
        grid.addWidget(self.slider_food(15), 3, 1)
        grid.addWidget(self.lcdf, 3, 2)
        grid.addWidget(self.lcdf_d, 3, 3)

        grid.addWidget(self.add_text("Transportation"), 4, 0)
        grid.addWidget(self.slider_transportation(15), 4, 1)
        grid.addWidget(self.lcdt, 4, 2)
        grid.addWidget(self.lcdt_d, 4, 3)

        grid.addWidget(self.add_text("Savings"), 5, 0)
        grid.addWidget(self.slider_savings(15), 5, 1)
        grid.addWidget(self.lcds, 5, 2)
        grid.addWidget(self.lcds_d, 5, 3)

        grid.addWidget(self.add_text("Necessities"), 6, 0)
        grid.addWidget(self.slider_necessities(15), 6, 1)
        grid.addWidget(self.lcdn, 6, 2)
        grid.addWidget(self.lcdn_d, 6, 3)

        grid.addWidget(self.add_text("Fun Money"), 7, 0)
        grid.addWidget(self.slider_fun_money(5), 7, 1)
        grid.addWidget(self.lcdfm, 7, 2)
        grid.addWidget(self.lcdfm_d, 7, 3)

        grid.addWidget(self.add_text("Total Percent"), 8, 0)
        grid.addWidget(self.check_budget(), 8, 1)
        grid.addWidget(self.lcdtotal, 8, 2)

        grid.addWidget(self.add_text("Save Budget"), 9, 0)
        grid.addWidget(self.save_budget(), 9, 1)

        self.setLayout(grid)

    def add_text(self, line_text):
        text = QLabel()
        text.setText(line_text)
        return text

    def slider_income(self, slider_value):
        slider_i = QSlider(Qt.Horizontal)
        slider_i.setFocusPolicy(Qt.StrongFocus)
        slider_i.setTickPosition(QSlider.TicksBothSides)
        slider_i.setMaximum(5000)
        slider_i.setMinimum(0)
        slider_i.setTickInterval(500)
        slider_i.setSingleStep(100)
        slider_i.setSliderPosition(slider_value)
        slider_i.valueChanged.connect(self.updateLCDi)
        slider_i.valueChanged.connect(self.updateLCDh_d)
        slider_i.valueChanged.connect(self.updateLCDf_d)
        slider_i.valueChanged.connect(self.updateLCDt_d)
        slider_i.valueChanged.connect(self.updateLCDs_d)
        slider_i.valueChanged.connect(self.updateLCDn_d)
        slider_i.valueChanged.connect(self.updateLCDfm_d)
        # print(slider_value)
        return slider_i

    def updateLCDi(self, event):
        # print(event)
        self.lcdi.display(event)

    def save_budget(self):
        save_b_button = QPushButton(f'Save Budget')
        save_b_button.clicked.connect(self.save_budget_click)
        return save_b_button

    def save_budget_click(self):
        budget = {'income': self.lcdi.value(),
                  'housing': self.lcdh_d.value(),
                  'food': self.lcdf_d.value(),
                  'transportation': self.lcdt_d.value(),
                  'savings': self.lcds_d.value(),
                  'necessities': self.lcdn_d.value(),
                  'fun_money': self.lcdfm_d.value()}

        # print(self.lcdi.value())
        with open('budget.pickle', 'wb') as handle:
            pickle.dump(budget, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return

    def check_budget(self):
        check_b_button = QPushButton(f'Check Budget')
        check_b_button.clicked.connect(self.updateLCDtotal)
        return check_b_button

    def updateLCDtotal(self):
        event = (self.lcdh.value() + self.lcdf.value() +
                 self.lcdt.value() + self.lcds.value() +
                 self.lcdn.value() + self.lcdfm.value())
        # print(event)
        if event == 100:
            self.lcdtotal.setStyleSheet("""QLCDNumber { 
                                                    background-color: green; 
                                                    color: white; }""")
        elif event != 100:
            self.lcdtotal.setStyleSheet("""QLCDNumber { 
                                                    background-color: red; 
                                                    color: white; }""")
        self.lcdtotal.display(event)
        self.lcdtotal.repaint()

    def slider_housing(self, slider_value):
        slider_h = QSlider(Qt.Horizontal)
        slider_h.setFocusPolicy(Qt.StrongFocus)
        slider_h.setTickPosition(QSlider.TicksBothSides)
        slider_h.setMaximum(100)
        slider_h.setMinimum(0)
        slider_h.setTickInterval(10)
        slider_h.setSingleStep(1)
        slider_h.setSliderPosition(slider_value)
        slider_h.valueChanged.connect(self.updateLCDh)
        slider_h.valueChanged.connect(self.updateLCDh_d)
        return slider_h

    def updateLCDh(self, event):
        # print(event)
        self.lcdh.display(event)

    def updateLCDh_d(self, event):
        # print(event)
        event = int(self.lcdi.value() * self.lcdh.value() * 0.01)
        self.lcdh_d.display(event)

    def slider_food(self, slider_value):
        slider_f = QSlider(Qt.Horizontal)
        slider_f.setFocusPolicy(Qt.StrongFocus)
        slider_f.setTickPosition(QSlider.TicksBothSides)
        slider_f.setMaximum(100)
        slider_f.setMinimum(0)
        slider_f.setTickInterval(10)
        slider_f.setSingleStep(1)
        slider_f.setSliderPosition(slider_value)
        slider_f.valueChanged.connect(self.updateLCDf)
        slider_f.valueChanged.connect(self.updateLCDf_d)
        return slider_f

    def updateLCDf(self, event):
        # print(event)
        self.lcdf.display(event)

    def updateLCDf_d(self, event):
        # print(event)
        event = int(self.lcdi.value() * self.lcdf.value() * 0.01)
        self.lcdf_d.display(event)

    def slider_transportation(self, slider_value):
        slider_t = QSlider(Qt.Horizontal)
        slider_t.setFocusPolicy(Qt.StrongFocus)
        slider_t.setTickPosition(QSlider.TicksBothSides)
        slider_t.setMaximum(100)
        slider_t.setMinimum(0)
        slider_t.setTickInterval(10)
        slider_t.setSingleStep(1)
        slider_t.setSliderPosition(slider_value)
        slider_t.valueChanged.connect(self.updateLCDt)
        slider_t.valueChanged.connect(self.updateLCDt_d)
        return slider_t

    def updateLCDt(self, event):
        # print(event)
        self.lcdt.display(event)

    def updateLCDt_d(self, event):
        # print(event)
        event = int(self.lcdi.value() * self.lcdt.value() * 0.01)
        self.lcdt_d.display(event)

    def slider_savings(self, slider_value):
        slider_s = QSlider(Qt.Horizontal)
        slider_s.setFocusPolicy(Qt.StrongFocus)
        slider_s.setTickPosition(QSlider.TicksBothSides)
        slider_s.setMaximum(100)
        slider_s.setMinimum(0)
        slider_s.setTickInterval(10)
        slider_s.setSingleStep(1)
        slider_s.setSliderPosition(slider_value)
        slider_s.valueChanged.connect(self.updateLCDs)
        slider_s.valueChanged.connect(self.updateLCDs_d)
        return slider_s

    def updateLCDs(self, event):
        # print(event)
        self.lcds.display(event)

    def updateLCDs_d(self, event):
        # print(event)
        event = int(self.lcdi.value() * self.lcds.value() * 0.01)
        self.lcds_d.display(event)

    def slider_necessities(self, slider_value):
        slider_n = QSlider(Qt.Horizontal)
        slider_n.setFocusPolicy(Qt.StrongFocus)
        slider_n.setTickPosition(QSlider.TicksBothSides)
        slider_n.setMaximum(100)
        slider_n.setMinimum(0)
        slider_n.setTickInterval(10)
        slider_n.setSingleStep(1)
        slider_n.setSliderPosition(slider_value)
        slider_n.valueChanged.connect(self.updateLCDn)
        slider_n.valueChanged.connect(self.updateLCDn_d)
        return slider_n

    def updateLCDn(self, event):
        # print(event)
        self.lcdn.display(event)

    def updateLCDn_d(self, event):
        # print(event)
        event = int(self.lcdi.value() * self.lcdn.value() * 0.01)
        self.lcdn_d.display(event)

    def slider_fun_money(self, slider_value):
        slider_fm = QSlider(Qt.Horizontal)
        slider_fm.setFocusPolicy(Qt.StrongFocus)
        slider_fm.setTickPosition(QSlider.TicksBothSides)
        slider_fm.setMaximum(100)
        slider_fm.setMinimum(0)
        slider_fm.setTickInterval(10)
        slider_fm.setSingleStep(1)
        slider_fm.setSliderPosition(slider_value)
        slider_fm.valueChanged.connect(self.updateLCDfm)
        slider_fm.valueChanged.connect(self.updateLCDfm_d)
        return slider_fm

    def updateLCDfm(self, event):
        # print(event)
        self.lcdfm.display(event)

    def updateLCDfm_d(self, event):
        # print(event)
        event = int(self.lcdi.value() * self.lcdfm.value() * 0.01)
        self.lcdfm_d.display(event)


class PersonalFinance_GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Budget App Cameron & Tianxin")

        # mainLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(Main_Budget())
        self.stackedWidget.addWidget(Budget_Maker())
        # self.stackedWidget.addWidget(Main_Budget.exit_button(self.stackedWidget))
        self.stackedWidget.addWidget((Stock_Maker()))

        buttonMain = QPushButton('Main Budget')
        buttonMain.clicked.connect(self.mainWidget)

        buttonBudget = QPushButton('Budget Maker')
        buttonBudget.clicked.connect(self.budgetWidget)

        buttonStock = QPushButton('Daily Stock Information')
        buttonStock.clicked.connect(self.stockWidget)

        buttonExit = QPushButton('Exit')
        buttonExit.clicked.connect(self.close)

        buttonRefresh = QPushButton('Refresh')
        buttonExit.clicked.connect(self.refreshWidget)


        # buttonExit

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(buttonMain)
        buttonLayout.addWidget(buttonBudget)
        buttonLayout.addWidget(buttonStock)
        # buttonLayout.addStretch(1)

        bl3 = QVBoxLayout()
        # bl2.addStretch(2)
        bl3.addWidget(buttonRefresh, alignment=QtCore.Qt.AlignRight)

        bl2 = QVBoxLayout()
        # bl2.addStretch(2)
        bl2.addWidget(buttonExit, alignment=QtCore.Qt.AlignRight)

        self.mainLayout.addWidget(self.stackedWidget)
        self.mainLayout.addLayout(buttonLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(bl3)
        self.mainLayout.addLayout(bl2)
        self.setLayout(self.mainLayout)
        
        QtWidgets.QApplication.processEvents()

    # def exitWidget(self):
    #     self.stackedWidget.setCurrentIndex(2)
    def stockWidget(self):
        self.stackedWidget.setCurrentIndex(2)

    def refreshWidget(self):
        self.stackedWidget.removeWidget(Main_Budget())
        self.stackedWidget.addWidget(Main_Budget())
        QtWidgets.QApplication.processEvents()
        # self.mainLayout.hide()
        # self.mainLayout.show()

    def budgetWidget(self):
        self.stackedWidget.setCurrentIndex(1)
        QtWidgets.QApplication.processEvents()

    def mainWidget(self):
        self.stackedWidget.setCurrentIndex(0)
        QtWidgets.QApplication.processEvents()


if __name__ == '__main__':
    # upon start up read previous expenses text file
    app = QApplication(sys.argv)
    QtWidgets.QApplication.processEvents()
    pf_gui = PersonalFinance_GUI()
    pf_gui.show()
    sys.exit(app.exec_())
