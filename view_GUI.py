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
Make LCD - https://learndataanalysis.org/control-lcd-number-widget-with-a-slider-pyqt5-tutorial/
Refresh LCD - https://stackoverflow.com/questions/52015269/displaying-numbers-with-qlcdnumber-display-with-pyqt
Saving - https://www.jessicayung.com/how-to-use-pickle-to-save-and-load-variables-in-python/
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

    # def income_input(self):
    #     income = QLineEdit(f'Input Price in $')
    #     return income

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
        return slider_i

    def updateLCDi(self, event):
        # print(event)
        self.lcdi.display(event)

    # def generate_budget(self):
    #     generate_budget_button = QPushButton(f'Generate Budget from Income')
    #     return generate_budget_button

    def save_budget(self):
        save_b_button = QPushButton(f'Save Budget')
        return save_b_button

    def check_budget(self):
        check_b_button = QPushButton(f'Check Budget')
        check_b_button.clicked.connect(self.updateLCDtotal)
        return check_b_button

    def updateLCDtotal(self):
        event = (self.lcdh.value() + self.lcdf.value() +
                 self.lcdt.value() + self.lcds.value() + self.lcdn.value() + self.lcdfm.value())
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
        # bl2.addStretch(2)
        bl2.addWidget(buttonExit, alignment=QtCore.Qt.AlignRight)

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
