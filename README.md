Self Budget GUI APP 
===

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

By using this standard, users can spend less time searhcing for the information they want. 

# Final Project
Software Carpentry Final Project Fall 2020
Team member: Cameron Czerpek & Tianxin Zhang

## Table of Coontents

- [Background](#background)
- [Specification](#specification)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Unit Test](#unittest)
- [References](#references)

## Background

We build this GUI since we are interested in learning PyQt5 and we never did a project on visulization.  
Having this budgeting app, we can enjoy our life worry free and let us take up the burden of organizing the finacial needs.

## Specifications
Please download sc.png and budget.pickle to your current directory to run python code.  
The file directory you downloaded have to be the same directory as your python code.

Our GUI is broken into 3 layers:  
- Main layer:  
This is the layer of the GUI that the userprimarily uses. They can add their most recent expenses on this layer, and their general spending is aggregated here.

- Budget Layer:  
This layer is for the user to create or edit their budget. Here they input their income and adjust their categorical spending based on their own needs.

- Checking Live Stock Layer:  
This layer helps you check the related live stock information for the past 30 days to help manage your budget and investment.

## Installation
- This project uses the following packages. 
- Please check them if you don't have them locally installed.
```diff
- Please use PyQt5 verion 5.15.1 or newer to run the python code.
- Attention: if you install PyQt5 newest version(5.15.2) in order to  
  run using terminal or sublime text on macbook.
```
- You may have a problem getting to run spyder.
- If you experience this situation, please downgrade the version to 5.10.1 after finish running GUI to use Anaconda.

Users may use pip install to install following packages.
```sh
pip install yfinance

pip install PyQt5

pip install sys

pip install sys

pip install matplotlib

pip install pickle

pip install os
```

## Usage

For everyday consumer, planning for the future and working to an objective allows us to plan big purchases, like houses and cars, without worrying you will miss the mark. If we can all stick to our budgets, putting money aside or having more disposable income can become easier and take us a step closer to achieve the financial goals.  
Checking stocks like S&P 500 and Dow Jones can help us manage our investment for future after looking at the economic indicator.

## Contributions

This project exists thanks to all the people who contribute, thanks for the instructor and grader at Software Carpentry class.  
<!-- ALL-CONTRIBUTORS-LIST: START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->



## License 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Unit Test 
- This unit test can test a month's total data to match the GUI visulization.
- Simply copying these lines to a new python file under same directory.
- Testing for each month we have for the past year, not listed all of them in this chapter.
```sh
import pickle as p
with open('December.pickle','rb') as handle:
    b = p.load(handle)print(b.values())
```

## References:
* Window - https://www.learnpyqt.com/tutorials/creating-your-first-window/
* Sliders - https://pythonprogramminglanguage.com/pyqt5-sliders/
* Multiple Pages - https://stackoverflow.com/questions/56867107/how-to-make-a-multi-page-application-in-pyqt5
* QStackedWidget - https://learndataanalysis.org/rotate-widgets-with-qstackedwidget-class/
* BarGraph - https://codeloop.org/pyqtchart-how-to-create-barchart-in-pyqt5/
* StackedBarGraph - https://doc.qt.io/qt-5/qtcharts-stackedbarchart-example.html
* Layouts - https://www.learnpyqt.com/tutorials/layouts/
* Layouts - http://zetcode.com/gui/pyqt5/layout/
* Date - https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup
* Date to text - https://doc.qt.io/qt-5/qdate.html
* Drop Down Box - https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
* Grid Width - https://doc.qt.io/qtforpython/PySide2/QtWidgets/QGridLayout.html
* Make LCD - https://learndataanalysis.org/control-lcd-number-widget-with-a-slider-pyqt5-tutorial/
* Refresh LCD - https://stackoverflow.com/questions/52015269/displaying-numbers-with-qlcdnumber-display-with-pyqt
* Saving - https://www.jessicayung.com/how-to-use-pickle-to-save-and-load-variables-in-python/
* Pickle dictionary - https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
* Popups - https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/
* LCD Color - https://stackoverflow.com/questions/52312768/change-qlcdnumber-colour-when-a-specific-value-is-read-using-pyqt5
* Get combo box text - https://www.geeksforgeeks.org/pyqt5-getting-the-text-of-selected-item-in-combobox/
* Update Dictionary - https://stackoverflow.com/questions/41063744/how-to-update-the-value-of-a-key-in-a-dictionary-in-python
* Check if path exists - https://www.guru99.com/python-check-if-file-exists.html
* Update Graph - https://stackoverflow.com/questions/59751779/update-chart-data-in-pyqt5
* Refresh Grid - https://www.qtcentre.org/threads/14701-Trying-to-refresh-a-QGridLayout
* Max in dictionary - https://stackoverflow.com/questions/42044090/return-the-maximum-value-from-a-dictionary/42044202

