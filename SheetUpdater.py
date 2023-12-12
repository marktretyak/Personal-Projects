import turtle
from turtle import textinput
import gspread
import oauth2client
from oauth2client import *
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import date

#google auth related items
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('F:\Downloads\sheetupdater-407816-5ec0bb00b98d.json', scope)
client = gspread.authorize(creds)

#find the row
today = date.today()
date = today.strftime("%m/%d/%Y")
workbook = client.open('Mark Tretyak')
sheet = workbook.get_worksheet(2)
row = sheet.find(date)
row = row.row
value = sheet.cell(row, 3).value
if not value:
    #Pop up boxes
    Column_list = sheet.row_values(1)
    for column in Column_list:
        user_input = turtle.textinput(column, f"{column} value:")
        colu = Column_list.index(column) + 1
        sheet.update_cell(row, colu, user_input)
else:
    exit()
