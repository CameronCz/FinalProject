'''
Software Carpentry Final Project
Personal Finance GUI
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import yfinance as yf
import pickle
from os import path


'''
Instalations User must have.
User may use pip install to install
PyQt5
QtWidgets
QtCore
QtChart
QtGui
sys
matplotlib.pyplot
yfinance
pickle
os
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
max in dictionary - https://stackoverflow.com/questions/42044090/return-the-maximum-value-from-a-dictionary/42044202
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
    '''
    Main budget class. First page user sees. Makes the
    widget where user inputs expenses, shows the last 3
    months of spendings, and shows current spending this
    month
    '''

    def __init__(self):
        '''
        initializes the main budget class
        ** Parameters **
            self: object
                self. values in Main_Budget
        '''
        super().__init__()

        # Set up LCD, calendar, and combo box
        self.lcdprice = QLCDNumber()
        self.lcdprice.display(0)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDateTime(QDateTime.currentDateTime())

        self.spend_cb = QComboBox()
        self.spend_cb.addItems(["housing", "food", "transportation",
                                "savings", "necessities", "fun_money"])

        # Bar Chart is set up here initially, then again in
        # last_3_months_click(self). Original code didn't
        # use the bar chart as a popup window, so other
        # functions were made based on it being in the
        # init. Otherwise we would have removed this
        # instance of the bar chart.
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

        # Set up blank dictionaries
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

        # Overwrite dictionaries
        if path.exists(self.months_list[2] + ".pickle"):
            with open(self.months_list[2] + ".pickle", 'rb') as handle:
                month3_dict = pickle.load(handle)

        if path.exists(self.months_list[1] + ".pickle"):
            with open(self.months_list[1] + ".pickle", 'rb') as handle:
                month2_dict = pickle.load(handle)

        if path.exists(self.months_list[0] + ".pickle"):
            with open(self.months_list[0] + ".pickle", 'rb') as handle:
                month1_dict = pickle.load(handle)

        # Set up series for last 3 months of data
        housing << month1_dict["housing"] << month2_dict["housing"] << month3_dict["housing"]
        food << month1_dict["food"] << month2_dict["food"] << month3_dict["food"]
        transportation << month1_dict["transportation"] << month2_dict["transportation"] << month3_dict["transportation"]
        savings << month1_dict["savings"] << month2_dict["savings"] << month3_dict["savings"]
        necessities << month1_dict["necessities"] << month2_dict["necessities"] << month3_dict["necessities"]
        fun_money << month1_dict["fun_money"] << month2_dict["fun_money"] << month3_dict["fun_money"]

        # Make percent bar chart
        self.spend_data = QPercentBarSeries()
        self.spend_data.append(housing)
        self.spend_data.append(food)
        self.spend_data.append(transportation)
        self.spend_data.append(savings)
        self.spend_data.append(necessities)
        self.spend_data.append(fun_money)

        # Make chart widget, and add axes and series
        self.monthly_spend_c = QChart()
        self.monthly_spend_c.createDefaultAxes()
        self.monthly_spend_c.addSeries(self.spend_data)
        self.monthly_spend_c.setTitle("Last 3 Monthly Spending Percentages")
        self.monthly_spend_c.setAnimationOptions(QChart.SeriesAnimations)

        # make appropriate axes for data and view chart
        self.axis = QBarCategoryAxis()
        self.axis.append(self.months_list)
        self.monthly_spend_c.setAxisX(self.axis, self.spend_data)
        self.monthly_spend_c = QChartView(self.monthly_spend_c)
        self.monthly_spend_c.setRenderHint(QPainter.Antialiasing)

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

        self.grid.addWidget(self.last_3_months(), 6, 0)
        self.grid.addWidget(self.current_m_spend(), 6, 1)

        self.setLayout(self.grid)

    def current_m_spend(self):
        '''
        Makes current spend push button
        ** Parameters **
            self: object
                self. values in Main_Budget
        ** Returns **
            current_m_spend_button: widget
                UI widget
        '''
        # connects button to function
        current_m_spend_button = QPushButton('Current Month Spending')
        current_m_spend_button.clicked.connect(self.current_m_spend_click)

        return current_m_spend_button

    def current_m_spend_click(self):
        '''
        Makes graph comparing current monthly
        spending to the user's budget
        ** Parameters **
            self: object
                self. values in Main_Budget
        '''
        # Create spending categories
        housing = QBarSet("Housing")
        food = QBarSet("Food")
        transportation = QBarSet("Transportation")
        savings = QBarSet("Savings")
        necessities = QBarSet("Necessities")
        fun_money = QBarSet("Fun Money")

        # Check if path exists
        # If so, load the current month dictionary
        # and load the budget
        # Otherwise use blank budget
        if path.exists(self.months_list[2] + ".pickle"):
            with open(self.months_list[2] + ".pickle", 'rb') as handle:
                month3_dict_spend = pickle.load(handle)

        else:
            month3_dict_spend = {'housing': 0,
                                 'food': 0,
                                 'transportation': 0,
                                 'savings': 0,
                                 'necessities': 0,
                                 'fun_money': 0}

        if path.exists("budget.pickle"):
            with open("budget.pickle", 'rb') as handle:
                budget_dict = pickle.load(handle)
        else:
            budget_dict = {'income': 0,
                           'housing': 0,
                           'food': 0,
                           'transportation': 0,
                           'savings': 0,
                           'necessities': 0,
                           'fun_money': 0}

        # Add dollars to series
        housing << month3_dict_spend["housing"] << budget_dict["housing"]
        food << month3_dict_spend["food"] << budget_dict["food"]
        transportation << month3_dict_spend["transportation"] << budget_dict["transportation"]
        savings << month3_dict_spend["savings"] << budget_dict["savings"]
        necessities << month3_dict_spend["necessities"] << budget_dict["necessities"]
        fun_money << month3_dict_spend["fun_money"] << budget_dict["fun_money"]

        # make bar series and add categories to object
        self.current_spend_data = QBarSeries()
        self.current_spend_data.append(housing)
        self.current_spend_data.append(food)
        self.current_spend_data.append(transportation)
        self.current_spend_data.append(savings)
        self.current_spend_data.append(necessities)
        self.current_spend_data.append(fun_money)

        # Make Chart
        self.current_spend_c = QChart()
        self.current_spend_c.createDefaultAxes()

        # Add labels and animation
        self.current_spend_c.addSeries(self.current_spend_data)
        self.current_spend_c.setTitle("Current Month Spending")
        self.current_spend_c.setAnimationOptions(QChart.SeriesAnimations)
        self.current_s_Xaxis = ["Money Spent", "Planned Budget"]

        # Add axis and show graph
        self.current_s_axis = QBarCategoryAxis()
        self.current_s_axis.append(self.current_s_Xaxis)
        self.current_spend_c.setAxisX(self.current_s_axis,
                                      self.current_spend_data)
        self.current_spend_c = QChartView(self.current_spend_c)
        self.current_spend_c.setRenderHint(QPainter.Antialiasing)
        self.current_spend_c.show()

    def last_3_months(self):
        '''
        Makes last 3 months button
        ** Parameters **
            self: object
                self. values in Main_Budget
        ** Returns **
            last_3_months_button: widget
                UI widget
        '''
        # connects button to function
        last_3_months_button = QPushButton('Last 3 Months Spending')
        last_3_months_button.clicked.connect(self.last_3_months_click)

        return last_3_months_button

    def add_text(self, line_text):
        '''
        adds text widget
        ** Parameters **
            self: object
                self. values in Main_Budget
        ** Returns **
            text: widget
                UI widget
        '''
        text = QLabel()
        text.setText(line_text)
        return text

    def price_input(self):
        '''
        Makes slider for inputting price of item
        ** Parameters **
            self: object
                self. values in Main_Budget
        ** Returns **
            slider_price: widget
                UI widget
        '''
        # Set up slider and slider values
        slider_price = QSlider(Qt.Horizontal)
        slider_price.setFocusPolicy(Qt.StrongFocus)
        slider_price.setTickPosition(QSlider.TicksBothSides)
        slider_price.setMaximum(2000)
        slider_price.setMinimum(0)
        slider_price.setTickInterval(100)
        slider_price.setSingleStep(1)
        slider_price.setSliderPosition(0)
        # connects button to LCD
        slider_price.valueChanged.connect(self.updateLCDprice)
        return slider_price
        # return price

    def updateLCDprice(self, event):
        '''
        Updates price LCD and color
        ** Parameters **
            self: object
                self. values in Main_Budget
        '''
        self.lcdprice.setStyleSheet("""QLCDNumber {
                                                    background-color: black;
                                                    color:  white; }""")
        self.lcdprice.display(event)

    def save_expense(self):
        '''
        Makes save expnse button
        ** Parameters **
            self: object
                self. values in Main_Budget
        ** Returns **
            last_3_months_button: widget
                UI widget
        '''
        # conncets button to saving function
        save_e_button = QPushButton('Save Expense')
        save_e_button.clicked.connect(self.save_expense_click)
        return save_e_button

    def last_3_months_click(self):
        '''
        Displays the graph of the last 3 months
        of spending percentages
        ** Parameters **
            self: object
                self. values in Main_Budget
        '''
        # Bar Chart categories
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

        # Create blank dictionaries for each month
        # to be modified
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

        # Overwrite blank dictionaries
        if path.exists(self.months_list[2] + ".pickle"):
            with open(self.months_list[2] + ".pickle", 'rb') as handle:
                month3_dict = pickle.load(handle)

        if path.exists(self.months_list[1] + ".pickle"):
            with open(self.months_list[1] + ".pickle", 'rb') as handle:
                month2_dict = pickle.load(handle)

        if path.exists(self.months_list[0] + ".pickle"):
            with open(self.months_list[0] + ".pickle", 'rb') as handle:
                month1_dict = pickle.load(handle)

        # Add last 3 month values
        housing << month1_dict["housing"] << month2_dict["housing"] << month3_dict["housing"]
        food << month1_dict["food"] << month2_dict["food"] << month3_dict["food"]
        transportation << month1_dict["transportation"] << month2_dict["transportation"] << month3_dict["transportation"]
        savings << month1_dict["savings"] << month2_dict["savings"] << month3_dict["savings"]
        necessities << month1_dict["necessities"] << month2_dict["necessities"] << month3_dict["necessities"]
        fun_money << month1_dict["fun_money"] << month2_dict["fun_money"] << month3_dict["fun_money"]

        # Create percent bars for each category
        self.spend_data = QPercentBarSeries()
        self.spend_data.append(housing)
        self.spend_data.append(food)
        self.spend_data.append(transportation)
        self.spend_data.append(savings)
        self.spend_data.append(necessities)
        self.spend_data.append(fun_money)

        # Make the chart and add labels
        self.monthly_spend_c = QChart()
        self.monthly_spend_c.createDefaultAxes()
        self.monthly_spend_c.addSeries(self.spend_data)
        self.monthly_spend_c.setTitle("Last 3 Monthly Spending Percentages")
        self.monthly_spend_c.setAnimationOptions(QChart.SeriesAnimations)

        # Show chart and add animations
        self.axis = QBarCategoryAxis()
        self.axis.append(self.months_list)
        self.monthly_spend_c.setAxisX(self.axis, self.spend_data)
        self.monthly_spend_c = QChartView(self.monthly_spend_c)
        self.monthly_spend_c.setRenderHint(QPainter.Antialiasing)
        self.monthly_spend_c.show()

    def save_expense_click(self):
        '''
        Saves expense to dictionary in pickle
        ** Parameters **
            self: object
                self. values in Main_Budget
        ** Returns **
        '''
        # Make zeroed out dictionary for
        # modifiying
        expense_save = {'housing': 0,
                        'food': 0,
                        'transportation': 0,
                        'savings': 0,
                        'necessities': 0,
                        'fun_money': 0}

        # Get month and category that user selected
        month_name = self.date_edit.date().toString("MMMM")
        combo_box_text = self.spend_cb.currentText()

        # Save the expense using pickle
        # Each month has an if statement
        # First open pickled month expense
        # read and adjust the value
        # then dump the pickled month expense
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

        # Display error message when you overspend
        # during the month
        filename = month_name
        instance = Budget_Maker()
        with open(filename + '.pickle', 'rb') as handle:
            b = pickle.load(handle)
        # print(b.values())
        if sum(b.values()) >= instance.lcdi.value():
            # it will still save the money
            error_gui("You spent more than your income this month!")

        return


def error_gui(error_msg):
    '''
    Calls message screen to create error GUI
    ** Parameters **
        error_msg:
            error message
    '''
    MessageScreen(QMessageBox.Critical, "An Error Occured!", error_msg)


class MessageScreen(QWidget):
    def __init__(self, message_type, title, message):
        '''
        Creates message screen widget
        ** Parameters **
            self: object
                self. values in MessageScreen
            message_type:
                type of message
            title: str
                message to be displayed
            error_msg:
                error message
        '''
        super().__init__()

        # Move error to center of window
        self.move_to_centre()

        # Create and display the message box
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
        '''
        Centers message
        ** Parameters **
            self: object
                self. values in MessageScreen
        '''
        # Sets size and adds to self.move
        resolution = QDesktopWidget().screenGeometry()

        width = resolution.width() / 2
        height = resolution.height() / 2

        frame_width = self.frameSize().width() / 2
        frame_height = self.frameSize().height() / 2

        self.move(width - frame_width, height - frame_height)


class Stock_Maker(QWidget):
    # Daily stock class
    def __init__(self):
        '''
        Widgets that show stock prices
        '''
        super().__init__()
        self.sc_im_label = QLabel()
        self.main_layout = QVBoxLayout()
        self.init_page()

    def init_page(self):
        '''
        Sets up widget date
        ** Parameters **
            self: object
                self. values in Stock_maker
        '''
        # Start here putting 4 stocks live to the current GUI page
        id_label = QLabel("Please select an option:")

        # Creats buttons and link buttons for each of the stocks
        nasdaq_button = QPushButton('Nasdaq Stock Daily Info', self)
        nasdaq_button.clicked.connect(self.nasdaq_button_is_pressed)

        dji_button = QPushButton(
            'Dow Johns Industrial Average Stock Daily Info', self)
        dji_button.clicked.connect(self.dji_button_is_pressed)

        sp500_button = QPushButton('S&P 500 Index Stock Daily Info', self)
        sp500_button.clicked.connect(self.sp500_button_is_pressed)

        msft_button = QPushButton('Microsoft Stock Daily Info', self)
        msft_button.clicked.connect(self.msft_button_is_pressed)

        # Show image at top of grid
        sc_im_map = QPixmap("sc.png")
        self.sc_im_label.setPixmap(sc_im_map)
        self.sc_im_label.show()

        # set up grid layout
        im_layout = QGridLayout()
        im_layout.addWidget(self.sc_im_label, 0, 0)
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

        # Add spacing to layout
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

        # set up layout
        self.setLayout(self.main_layout)

    def nasdaq_button_is_pressed(self):
        '''
        Displays nasdaq when button is pressed
        ** Parameters **
            self: object
                self. values in Stock_maker
        '''
        # Gets stock ticker, plots stock,
        # shows graph
        ndaq = yf.Ticker("NDAQ")
        hist = ndaq.history(period='30d')
        hist['Close'].plot(figsize=(16, 9))
        plt.title("Nasdaq Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def dji_button_is_pressed(self):
        '''
        Displays Dow Jones when button is pressed
        ** Parameters **
            self: object
                self. values in Stock_maker
        '''
        # Gets stock ticker, plots stock,
        # shows graph
        dji = yf.Ticker("DJI")
        hist = dji.history(period='30d')
        hist['Close'].plot(figsize=(16, 9))
        plt.title("Dow Jones Industrial Average Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def sp500_button_is_pressed(self):
        '''
        Displays s&p500 when button is pressed
        ** Parameters **
            self: object
                self. values in Stock_maker
        '''
        # Gets stock ticker, plots stock,
        # shows graph
        inx = yf.Ticker("^GSPC")
        hist = inx.history(period='30d')
        hist['Close'].plot(figsize=(16, 9))
        plt.title("S&P 500 Index Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def msft_button_is_pressed(self):
        '''
        Displays MSFT when button is pressed
        ** Parameters **
            self: object
                self. values in Stock_maker
        '''
        # Gets stock ticker, plots stock,
        # shows graph
        msft = yf.Ticker("MSFT")
        hist = msft.history(period='30d')
        hist['Close'].plot(figsize=(16, 9))
        plt.title("Microsoft Stock Live Information")
        plt.ylabel("Dollar($)")
        plt.xlabel('Last 30 Days')
        plt.show()

    def clear_layout(self, layout):
        '''
        Clears layout
        ** Parameters **
            self: object
                self. values in Stock_maker
            layout: object
                widget layout
        '''
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
        '''
        Sets up the budget maker class
        Budget maker allows the user to adjust sliders
        for income, housing, food, savings, transportation,
        necessities, and fun money (money that can be spend
        on things that aren't necessities)
        '''
        super().__init__()

        # make income LCDs
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

        # Set up the grid layout for the budget page
        grid = QGridLayout()
        grid.addWidget(self.add_text("Input Monthly Income $"), 1, 0)
        grid.addWidget(self.slider_income(2000), 1, 1)
        grid.addWidget(self.lcdi, 1, 3)

        # Each gategory is added in the format of
        # category, adjust slider, percentage, and dollars
        grid.addWidget(self.add_text("Category"), 0, 0)
        grid.addWidget(self.add_text("Adjust Slider"), 0, 1)
        grid.addWidget(QPushButton(f'Percentage'), 0, 2)
        grid.addWidget(QPushButton(f'Dollars'), 0, 3)

        # We repeate this style for all budget categories
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

        # sets the layout
        self.setLayout(grid)

    def add_text(self, line_text):
        '''
        Add text to line
        ** Parameters **
            self: object
                self. values in Budget_Maker
        ** Returns **
            text: widget
                UI widget
        '''
        text = QLabel()
        text.setText(line_text)
        return text

    def slider_income(self, slider_value):
        '''
        Makes adjustable slider for the user
        ** Parameters **
            self: object
                self. values in Budget_Maker
        ** Returns **
            slider_i: widget
                UI widget
        '''
        # Make slider and set range
        slider_i = QSlider(Qt.Horizontal)
        slider_i.setFocusPolicy(Qt.StrongFocus)
        slider_i.setTickPosition(QSlider.TicksBothSides)
        slider_i.setMaximum(5000)
        slider_i.setMinimum(0)
        slider_i.setTickInterval(500)
        slider_i.setSingleStep(100)
        slider_i.setSliderPosition(slider_value)

        # connect slider to LCDs
        slider_i.valueChanged.connect(self.updateLCDi)
        slider_i.valueChanged.connect(self.updateLCDh_d)
        slider_i.valueChanged.connect(self.updateLCDf_d)
        slider_i.valueChanged.connect(self.updateLCDt_d)
        slider_i.valueChanged.connect(self.updateLCDs_d)
        slider_i.valueChanged.connect(self.updateLCDn_d)
        slider_i.valueChanged.connect(self.updateLCDfm_d)
        return slider_i

    def updateLCDi(self, event):
        '''
        updates LCD
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcdi.display(event)

    def save_budget(self):
        '''
        Makes push button to save budget
        ** Parameters **
            self: object
                self. values in Budget_Maker
        ** Returns **
            save_b_button: widget
                UI widget
        '''
        save_b_button = QPushButton(f'Save Budget')
        save_b_button.clicked.connect(self.save_budget_click)
        return save_b_button

    def save_budget_click(self):
        '''
        Function for saving dictionary with pickle
        ** Parameters **
            self: object
                self. values in Budget_Maker
        ** Returns **
        '''
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
        '''
        Determines if budget adds up to 100%
        ** Parameters **
            self: object
                self. values in Budget_Maker
        ** Returns **
            check_b_button: widget
                UI widget
        '''
        check_b_button = QPushButton(f'Check Budget')
        check_b_button.clicked.connect(self.updateLCDtotal)
        return check_b_button

    def updateLCDtotal(self):
        '''
        Updates total percent LCD
        ** Parameters **
            self: object
                self. values in Budget_Maker
        '''
        # sum all LCD values
        event = (self.lcdh.value() + self.lcdf.value() +
                 self.lcdt.value() + self.lcds.value() +
                 self.lcdn.value() + self.lcdfm.value())

        # If equal to 100 percent, good, show green
        if event == 100:
            self.lcdtotal.setStyleSheet("""QLCDNumber {
                                                    background-color: green;
                                                    color: white; }""")
        # Otherwise, bad, show red
        elif event != 100:
            self.lcdtotal.setStyleSheet("""QLCDNumber {
                                                    background-color: red;
                                                    color: white; }""")
        self.lcdtotal.display(event)
        self.lcdtotal.repaint()

    def slider_housing(self, slider_value):
        '''
        Slider for adjusting housing
        ** Parameters **
            self: object
                self. values in Budget_Maker
            slider_value: int
                value from slider
        ** Returns **
            slider_h: widget
                UI widget
        '''
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
        '''
        updates LCD for housing percent
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcdh.display(event)

    def updateLCDh_d(self, event):
        '''
        updates LCD for housing dollars
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        event = int(self.lcdi.value() * self.lcdh.value() * 0.01)
        self.lcdh_d.display(event)

    def slider_food(self, slider_value):
        '''
        Slider for adjusting food
        ** Parameters **
            self: object
                self. values in Budget_Maker
            slider_value: int
                value from slider
        ** Returns **
            slider_f: widget
                UI widget
        '''
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
        '''
        updates LCD for food percent
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcdf.display(event)

    def updateLCDf_d(self, event):
        '''
        updates LCD for food dollars
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        event = int(self.lcdi.value() * self.lcdf.value() * 0.01)
        self.lcdf_d.display(event)

    def slider_transportation(self, slider_value):
        '''
        Slider for adjusting transportation
        ** Parameters **
            self: object
                self. values in Budget_Maker
            slider_value: int
                value from slider
        ** Returns **
            slider_t: widget
                UI widget
        '''
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
        '''
        updates LCD for transportation percent
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcdt.display(event)

    def updateLCDt_d(self, event):
        '''
        updates LCD for transportation dollars
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        event = int(self.lcdi.value() * self.lcdt.value() * 0.01)
        self.lcdt_d.display(event)

    def slider_savings(self, slider_value):
        '''
        Slider for adjusting savings
        ** Parameters **
            self: object
                self. values in Budget_Maker
            slider_value: int
                value from slider
        ** Returns **
            slider_s: widget
                UI widget
        '''
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
        '''
        updates LCD for savings percent
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcds.display(event)

    def updateLCDs_d(self, event):
        '''
        updates LCD for savings dollars
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        event = int(self.lcdi.value() * self.lcds.value() * 0.01)
        self.lcds_d.display(event)

    def slider_necessities(self, slider_value):
        '''
        Slider for adjusting necessities
        ** Parameters **
            self: object
                self. values in Budget_Maker
            slider_value: int
                value from slider
        ** Returns **
            slider_n: widget
                UI widget
        '''
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
        '''
        updates LCD for necessities percent
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcdn.display(event)

    def updateLCDn_d(self, event):
        '''
        updates LCD for necessities dollars
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        event = int(self.lcdi.value() * self.lcdn.value() * 0.01)
        self.lcdn_d.display(event)

    def slider_fun_money(self, slider_value):
        '''
        Slider for adjusting fun money
        ** Parameters **
            self: object
                self. values in Budget_Maker
            slider_value: int
                value from slider
        ** Returns **
            slider_fm: widget
                UI widget
        '''
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
        '''
        updates LCD for fun money percent
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        self.lcdfm.display(event)

    def updateLCDfm_d(self, event):
        '''
        updates LCD for fun money dollars
        ** Parameters **
            self: object
                self. values in Budget_Maker
            event: int
                slider value
        '''
        event = int(self.lcdi.value() * self.lcdfm.value() * 0.01)
        self.lcdfm_d.display(event)


class PersonalFinance_GUI(QWidget):
    '''
    Class that sets up all of the pages of the GUI
    and adds constant buttons to the bottom of the
    GUI for nagigation
    '''

    def __init__(self):
        '''
        Initialize the GUI creator class
        '''
        super().__init__()

        # Add title
        self.setWindowTitle("Budget App Cameron & Tianxin")

        # Set up PyQt5 layout
        self.mainLayout = QVBoxLayout()

        # make multiple pages
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(Main_Budget())
        self.stackedWidget.addWidget(Budget_Maker())
        self.stackedWidget.addWidget((Stock_Maker()))

        # Create and link buttons to pages
        buttonMain = QPushButton('Main Budget')
        buttonMain.clicked.connect(self.mainWidget)

        buttonBudget = QPushButton('Budget Maker')
        buttonBudget.clicked.connect(self.budgetWidget)

        buttonStock = QPushButton('Daily Stock Information')
        buttonStock.clicked.connect(self.stockWidget)

        # Exit button for closing the app
        buttonExit = QPushButton('Exit')
        buttonExit.clicked.connect(self.close)

        # Set up bottom button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(buttonMain)
        buttonLayout.addWidget(buttonBudget)
        buttonLayout.addWidget(buttonStock)

        # Set up exit button layout
        bl2 = QVBoxLayout()
        bl2.addWidget(buttonExit, alignment=QtCore.Qt.AlignRight)

        # Format main layout
        self.mainLayout.addWidget(self.stackedWidget)
        self.mainLayout.addLayout(buttonLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(bl2)
        self.setLayout(self.mainLayout)

        QtWidgets.QApplication.processEvents()

    def stockWidget(self):
        '''
        Brings user to stock page
        ** Parameters **
            self: object
                self. values in PersonalFinance_GUI
        '''
        self.stackedWidget.setCurrentIndex(2)

    def budgetWidget(self):
        '''
        Brings user to budget maker page
        ** Parameters **
            self: object
                self. values in PersonalFinance_GUI
        '''
        self.stackedWidget.setCurrentIndex(1)
        QtWidgets.QApplication.processEvents()

    def mainWidget(self):
        '''
        Brings user to main page
        ** Parameters **
            self: object
                self. values in PersonalFinance_GUI
        '''
        self.stackedWidget.setCurrentIndex(0)
        QtWidgets.QApplication.processEvents()


if __name__ == '__main__':
    # Starts running the GUI
    app = QApplication(sys.argv)
    QtWidgets.QApplication.processEvents()
    pf_gui = PersonalFinance_GUI()
    pf_gui.show()
    sys.exit(app.exec_())
