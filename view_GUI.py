'''
Software Carpentry Final Project
Personal Finance GUI
EN.540.635
Tianxin Zhang & Cameron Czerpak
'''
import sys

# import main
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *

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
Layouts - https://www.learnpyqt.com/tutorials/layouts/
Layouts - http://zetcode.com/gui/pyqt5/layout/
Date - https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup
Drop Down Box - https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
Grid Width - https://doc.qt.io/qtforpython/PySide2/QtWidgets/QGridLayout.html
'''

'''
General notes:
GUI is broken into 2 layers
Main layer - this is the layer of the GUI that the user
primarily uses. They can add their most recent expenses
on this layer, and their general spending is aggregated
here.
Budget Layer - this layer is for the user to create or edit
their budget. Here they input their income and adjust their
categorical spending based on their own needs
'''


class Main_Budget(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        grid.addWidget(self.add_text("Information"), 0, 0)
        grid.addWidget(self.add_text("Input Expense"), 0, 1)

        grid.addWidget(self.add_text("Date"), 1, 0)
        grid.addWidget(self.date_input(), 1, 1)

        grid.addWidget(self.add_text("Price"), 2, 0)
        grid.addWidget(self.price_input(), 2, 1)

        grid.addWidget(self.add_text("Category"), 3, 0)
        grid.addWidget(self.spend_category(), 3, 1)

        grid.addWidget(self.add_text("Confirm"), 4, 0)
        grid.addWidget(self.save_expense(), 4, 1)

        grid.addWidget(self.monthly_spend_chart(), 5, 0, 1, 2)
        grid.addWidget(self.monthly_spend_chart(), 6, 0, 1, 2)

        self.setLayout(grid)

    def add_text(self, line_text):
        text = QLabel()
        text.setText(line_text)
        return text

    def date_input(self):
        date_edit = QDateEdit(calendarPopup=True)
        date_edit.setDateTime(QDateTime.currentDateTime())
        return date_edit

    def price_input(self):
        price = QLineEdit(f'Input Price in $')
        return price

    def spend_category(self):
        spend_cb = QComboBox()
        spend_cb.addItems(["Category", "Housing", "Food", "Transportation",
                           "Savings", "Necessities", "Fun Money"])
        return spend_cb

    def save_expense(self):
        save_button = QPushButton(f'Save Expnse')

        # Write date, price, and category to text file

        # Do not save if price isn't inputted correctly

        # Do not save if no category is selected

        # reset inputs
        return save_button

    # def exit_button(self):
    #     exit_button = QPushButton(f'Exit')
    #     return exit_button

    def monthly_spend_chart(self):
        # The QBarSet class represents a set of bars in the bar chart.
        # It groups several bars into a bar set

        housing = QBarSet("Housing")
        food = QBarSet("Food")
        transportation = QBarSet("Transportation")
        savings = QBarSet("Savings")
        necessities = QBarSet("Necessities")
        fun_money = QBarSet("Fun Money")

        # Read monthly values for each category
        housing << 1000 << 1000 << 1000
        food << 300 << 250 << 350
        transportation << 40 << 50 << 20
        savings << 300 << 100 << 240
        necessities << 100 << 90 << 120
        fun_money << 100 << 250 << 50

        spend_data = QPercentBarSeries()
        spend_data.append(housing)
        spend_data.append(food)
        spend_data.append(transportation)
        spend_data.append(savings)
        spend_data.append(necessities)
        spend_data.append(fun_money)

        monthly_spend_c = QChart()
        monthly_spend_c.addSeries(spend_data)
        monthly_spend_c.setTitle("Monthly Spending")
        monthly_spend_c.setAnimationOptions(QChart.SeriesAnimations)

        months_list = ["Oct", "Nov", "Dec"]
        axis = QBarCategoryAxis()
        axis.append(months_list)
        monthly_spend_c.setAxisX(axis, spend_data)
        monthly_spend_c_View = QChartView(monthly_spend_c)
        monthly_spend_c_View.setRenderHint(QPainter.Antialiasing)

        return monthly_spend_c_View


class Budget_Maker(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QPushButton(f'Button A'))
        layout.addWidget(QPushButton(f'Button B'))
        layout.addWidget(self.slider_percent())
        layout.addWidget(self.slider_percent())
        layout.addWidget(self.slider_percent())

        self.setLayout(layout)

    def slider_percent(self):
        slider_p = QSlider(Qt.Horizontal)
        slider_p.setFocusPolicy(Qt.StrongFocus)
        slider_p.setTickPosition(QSlider.TicksBothSides)
        slider_p.setTickInterval(10)
        slider_p.setSingleStep(1)
        return slider_p


class PersonalFinance_GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Budget App")

        mainLayout = QVBoxLayout()

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(Main_Budget())
        self.stackedWidget.addWidget(Budget_Maker())
        # self.stackedWidget.addWidget(Main_Budget.exit_button(self.stackedWidget))
        # self.stackedWidget.addWidget(())

        buttonMain = QPushButton('Main Budget')
        buttonMain.clicked.connect(self.mainWidget)

        buttonBudget = QPushButton('Budget Maker')
        buttonBudget.clicked.connect(self.budgetWidget)

        buttonExit = QPushButton('Exit')
        buttonExit.clicked.connect(self.close)

        # buttonExit

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(buttonMain)
        buttonLayout.addWidget(buttonBudget)
        # buttonLayout.addStretch(1)
        bl2 = QVBoxLayout()
        bl2.addStretch(2)
        bl2.addWidget(buttonExit,alignment = QtCore.Qt.AlignRight)

        mainLayout.addWidget(self.stackedWidget)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(bl2)
        self.setLayout(mainLayout)

    def exitWidget(self):
        self.stackedWidget.setCurrentIndex(2)

    def budgetWidget(self):
        self.stackedWidget.setCurrentIndex(1)

    def mainWidget(self):
        self.stackedWidget.setCurrentIndex(0)


if __name__ == '__main__':
    # upon start up read previous expenses text file
    app = QApplication(sys.argv)
    pf_gui = PersonalFinance_GUI()
    pf_gui.show()
    sys.exit(app.exec_())
