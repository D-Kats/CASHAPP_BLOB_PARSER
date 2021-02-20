# DKats 2021 
# This script parses the CCEntitySync-api.squareup.com.sqlite database of the CashApp Application
# and extracts all the valuable data from the ZSYNCPAYMENT BLOB column of the ZPAYMENT table.
# A CSV report is being crated, ready to be imported to an excel spreadsheet for further data research. 
# IMPORTANT: 1. Import the csv text file with UTF-8 encoding in the spreadsheet, 2. Use tab as a delimiter
# More info on the documentation at https://github.com/D-Kats/CASHAPP_BLOB_PARSER/blob/main/README.md
#---Thanks to---
# PySimpleGUI module from  MikeTheWatchGuy at https://pypi.org/project/PySimpleGUI/
# executable's icon downloaded from www.freeiconspng.com
import PySimpleGUI as sg
import json
import sqlite3
import datetime
from datetime import timezone
import os
import webbrowser



#---functions definition
def  brace_trim(s, brace_diff):
	if brace_diff == 0:
		return s
	elif brace_diff > 0:
		for i in range(brace_diff):
			s = s[:s.rfind('}',0,-1)+1]
		return s
			
def reporting(outputFolder, csv):
	try:#catching write permission error for output folder
		with open(f'{outputFolder}\\report.csv', 'w', encoding='utf-8', errors='ignore') as fout:
			fout.write(csv)
		print('NO ERRORS - PARSING COMPLETED!')
		sg.PopupOK('Script finished successfully!\nCSV file created at output folder.', title=': )', background_color='#2a363b')
	except:	
		print(f'ERROR: {e}')
		sg.PopupOK('Error writing the CSV file to the output folder!\nCheck Error Console for more details', title='!', background_color='#2a363b')


#---menu definition
menu_def = [['File', ['Exit']],
			['Help', ['Documentation', 'About']],] 
#---layout definition
DBFrameLayout = [[sg.Text('Choose the database file to parse', background_color='#2a363b')],
					[sg.In(key='-DB-', readonly=True, background_color='#334147'), sg.FileBrowse(file_types=(('Database', '*.sqlite'),))]]

OutputSaveFrameLayout = [[sg.Text('Choose folder to save the csv report file', background_color='#2a363b')],
					[sg.In(key='-OUTPUT-', readonly=True, background_color='#334147'), sg.FolderBrowse()]] #key='-SAVEBTN-', disabled=True, enable_events=True

col_layout = [[sg.Frame('Database File to Parse', DBFrameLayout, background_color='#2a363b')],
				# [sg.Frame('Keywords (Optional - only for Documents)', KeywordsFrameLayout, background_color='#2a363b', pad=((0,0),(0,65))) ],				
				[sg.Frame('Output Folder', OutputSaveFrameLayout, background_color='#2a363b')],				
				[sg.Button('Exit', size=(7,1)), sg.Button('Parse', size=(7,1))]]

#---GUI Definition
layout = [[sg.Menu(menu_def, key='-MENUBAR-')],
			[sg.Column(col_layout, element_justification='c',background_color='#2a363b'), sg.Frame('Error Console',
			[[sg.Output(size=(35,15), key='-OUT-', background_color='#334147', text_color='#fefbd8')]], background_color='#2a363b')],
			[sg.Text('CashApp BLOB Parser Ver. 1.0.0', background_color='#2a363b', text_color='#b2c2bf')]]

window = sg.Window('CashApp BLOB Parser', layout, background_color='#2a363b') 

#---run
while True:
	event, values = window.read()
	# print(event, values)
	if event in (sg.WIN_CLOSED, 'Exit'):
		break
#---menu events
	if event == 'Documentation':
		try:
			webbrowser.open_new('https://github.com/D-Kats/CASHAPP_BLOB_PARSER/blob/main/README.md')
		except:
			sg.PopupOK('Visit https://github.com/D-Kats/CASHAPP_BLOB_PARSER/blob/main/README.md for documentation', title='Documentation', background_color='#2a363b')
	if event == 'About':
		sg.PopupOK('CashApp BLOB Parser Ver. 1.0.0 \n\n --DKats 2021', title='-About-', background_color='#2a363b')
	
#---buttons events
	if event == "Parse":
		if values['-DB-'] == '': # den exei epileksei db gia analysh
			sg.PopupOK('Please choose a database to parse!', title='!', background_color='#2a363b')
		elif values['-OUTPUT-'] == '': #den exei epileksei fakelo gia output			
			sg.PopupOK('Please choose a folder to save the csv report to!', title='!', background_color='#2a363b')
		else:
			try: #catching db connection error 
				db = values['-DB-']
				conn = sqlite3.connect(db)
				conn.text_factory = bytes
				c = conn.cursor()
				data = c.execute('SELECT Z_PK, ZSYNCPAYMENT FROM ZPAYMENT')

				#---variables					
				csv = 'Z_PK\ttoken\tauth_token\trole\tamount (from amount key)\tcurrency code (from amount key)\tpull_amount\tsender_payment_amount_in_default_currency\trecipient_payment_amount_in_default_currency\tstate\tnote\tinstrument_type\ttransaction_id\tcreated_at\tcaptured_at\treached_customer_at\tpaid_out_at\tdeposited_at\tdisplay_date\ttoken (from instrument key)\tcard_brand (from instrument key)\tbank_name (from instrument key)\tdisplay_name (from instrument key)'
				errorFlag = False

				for row in data.fetchall():			
					init = str(row[1], errors='ignore')
					s = init[init.find('{'):init.rfind('}')+1]
					s = brace_trim(s, s.count('}') - s.count('{')) # deleting any excess curly braces after the valid json part of the BLOB

					try: #cathcing the json conversion
						data = json.loads(s)
						
						csv += f"\n{row[0]}\t"
						if 'token' in data:
							csv += f"{data['token']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'auth_token' in data:
							csv += f"{data['auth_token']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'role' in data:
							csv += f"{data['role']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'amount' in data:
							if 'amount' in data['amount']:
								csv += f"{data['amount']['amount']}\t"
							else:
								csv += 'KEY NOT FOUND\t'
						else:
							csv += 'KEY NOT FOUND\t'
						if 'amount' in data:
							if 'currency_code' in data['amount']:  
								csv += f"{data['amount']['currency_code']}\t"
							else:
								csv += 'KEY NOT FOUND\t'
						else:
							csv += 'KEY NOT FOUND\t'
						if 'pull_amount' in data:
							csv += f"{data['pull_amount']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'sender_payment_amount_in_default_currency' in data:
							csv += f"{data['sender_payment_amount_in_default_currency']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'recipient_payment_amount_in_default_currency' in data:
							csv += f"{data['recipient_payment_amount_in_default_currency']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'state' in data:
							csv += f"{data['state']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'note' in data:
							csv += f"{data['note']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'instrument_type' in data:
							csv += f"{data['instrument_type']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'transaction_id' in data:
							csv += f"{data['transaction_id']}\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'created_at' in data:
							t = data['created_at']
							csv += f"{datetime.datetime.fromtimestamp(t/1000, tz=timezone.utc)} ({data['created_at']})\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'captured_at' in data:
							t = data['captured_at']
							csv += f"{datetime.datetime.fromtimestamp(t/1000, tz=timezone.utc)} ({data['captured_at']})\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'reached_customer_at' in data:
							t = data['reached_customer_at']
							csv += f"{datetime.datetime.fromtimestamp(t/1000, tz=timezone.utc)} ({data['reached_customer_at']})\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'paid_out_at' in data:
							t = data['paid_out_at']
							csv += f"{datetime.datetime.fromtimestamp(t/1000, tz=timezone.utc)} ({data['paid_out_at']})\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'deposited_at' in data:
							t = data['deposited_at']
							csv += f"{datetime.datetime.fromtimestamp(t/1000, tz=timezone.utc)} ({data['deposited_at']})\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'display_date' in data:
							t = data['display_date']
							csv += f"{datetime.datetime.fromtimestamp(t/1000, tz=timezone.utc)} ({data['display_date']})\t"
						else:
							csv += 'KEY NOT FOUND\t'
						if 'instrument' in data:
							if 'token' in data['instrument']:
								csv += f"{data['instrument']['token']}\t"
							else:
								csv += 'KEY NOT FOUND\t'
						else:
							csv += 'KEY NOT FOUND\t'
						if 'instrument' in data:
							if 'card_brand' in data['instrument']:
								csv += f"{data['instrument']['card_brand']}\t"
							else:
								csv += 'KEY NOT FOUND\t'
						else:
							csv += 'KEY NOT FOUND\t'
						if 'instrument' in data:
							if 'bank_name' in data['instrument']: 
								csv += f"{data['instrument']['bank_name']}\t"
							else:
								csv += 'KEY NOT FOUND\t'
						else:
							csv += 'KEY NOT FOUND\t'
						if 'instrument' in data:
							if 'display_name' in data['instrument']:
								csv += f"{data['instrument']['display_name']}\t"
							else:
								csv += 'KEY NOT FOUND\t'
						else:
							csv += 'KEY NOT FOUND\t'				
				
					except Exception as e:
						errorFlag = True
						print(f'ERROR in record with Z_PK:{row[0]}, Error: {e}')						
						print('####')
						print('MALFORMATED JSON STRING:')
						print(s)
						sg.PopupOK('Error converting the JSON data of the BLOB!\nCheck Error Console for more details', title='!', background_color='#2a363b')
						break	
				#creating the csv file
				if errorFlag:
					pass
				else:
					outputFolder = values['-OUTPUT-']
					reporting(outputFolder, csv)			
						
			except Exception as e:
				print(f'ERROR: {e}')
				sg.PopupOK('Error connecting to the database!\nCheck Error Console for more details', title='!', background_color='#2a363b')
	
window.close()
