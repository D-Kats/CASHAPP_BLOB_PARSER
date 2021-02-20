import json
import sqlite3
import datetime
from datetime import timezone
import ctypes


JSONErrorFlag = False
JSONErrorLog = ''
errorFlag = False
errorLog = 'Error converting rows with\n'
csv = 'token\tauth_token\trole\tamount\tcurrency code\tpull_amount\tsender_payment_amount_in_default_currency\trecipient_payment_amount_in_default_currency\tstate\tnote\tinstrument_type\ttransaction_id\tcreated_at\tcaptured_at\treached_customer_at\tpaid_out_at\tdeposited_at\tdisplay_date\ttoken\tcard_brand\tbank_name\tdisplay_name'

conn = sqlite3.connect('CCEntitySync-api.squareup.com.sqlite')

conn.text_factory = bytes
c = conn.cursor()
data = c.execute('SELECT Z_PK, ZSYNCPAYMENT FROM ZPAYMENT')


count = 0
for row in data.fetchall():			
	init = str(row[1], errors='ignore')
	s = init[init.find('{'):init.rfind('}')+1]
	print(s)
	print('############################################')		
	# try: #cathcing the json conversion
	data = json.loads(s)
	try: #catching the json keys parsing
		if 'token' in data:
			csv += f"\n{data['token']}\t"
		else:
			csv += '\nKEY NOT FOUND\t'
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
		errorLog += f'Z_PK:{row[0]}, with error {e}\n'
	# except Exception as e:				
	# 	JSONErrorFlag = True
	# 	JSONErrorLog += f'{e}'

# if JSONErrorFlag:
# 	with open('JSON_Error.log', 'w', encoding='utf-8', errors='ignore') as foutJson:
# 		foutJson.write(JSONErrorLog)
# 	ctypes.windll.user32.MessageBoxW(0, 'Error parsing the BLOBs...\nJSON_Error.log file created', 'Warning!', 1)		
# else:
	with open('report.csv', 'w', encoding='utf-8', errors='ignore') as fout:
		fout.write(csv)
	count+=1
	print(count)
	# if errorFlag:
	# 	with open('error.log', 'w', encoding='utf-8', errors='ignore') as foutError:
	# 		foutError.write(errorLog)
	# 	ctypes.windll.user32.MessageBoxW(0, 'Script finished with error!\nerror.log file created', 'Warning!', 1) 
	# else:
	# 	ctypes.windll.user32.MessageBoxW(0, 'Script finished successfully!\nreport.csv file created', 'Success!', 1)

		 