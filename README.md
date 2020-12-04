# Self Budget GUI APP 

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[![license](https://img.shields.io/github/license/:user/:repo.svg)](LICENSE)

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

## Background

## Specifications

## Installation
This project uses the following packages. Please check them if you don't have them locally installed
One thing to mention is if you install PyQt5 newest version(5.15.2) in order to run using terminal or sublime text on macbook
You may have a problem getting to run spyder.
If you experience this situation, please downgrade the version to 5.10.1 after finish running GUI to use Anaconda.
'''
pip install yfinance

pip install fpdf

pip install PyQtChart

sys

widgets

core

gui

matplotlib

yfinance
'''
## Usage

## Contributions

This project exists thanks to all the people who contribute.

## License 


## Unit Test 
This unit test can test a month's total data to match the GUI visulization
simply copying these lines to a new python file under same directory

------------------------------------------------------------------------------
import pickle as p
with open('December.pickle','rb') as handle:
b = p.load(handle)print(b.values())

--------------------------------------------------------------------

Reference for this README file:
We looked at some amazing README 
