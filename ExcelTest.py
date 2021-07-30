# -*- coding: utf-8 -*-
"""
Created on Thu May 08 13:15:24 2014

@author: jlape
"""

from xlrd import open_workbook

book = open_workbook('ProfileScores.xlsx')
sheet = book.sheet_by_index(0)

print sheet.row_values(0,1,2)