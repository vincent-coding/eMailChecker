import sys

if sys.version_info < (3, 8):
	sys.exit("This program only runs on Python 3.8!")

import requests
import json
import time
import os

config = None
apiKey = None
emailList = None

if os.path.exists("./config.json"):
	try:
		with open("./config.json", 'r') as configFile:
			config = json.load(configFile)
			configFile.close()
		apiKey = config['token']
	except:
		sys.exit("The configuration file (config.json) is invalid or corrupt!")
else:
	print("The configuration file (config.json) does not exist!")

def simpleMode():
	email = input("Enter the email adress: ")
	if apiKey:
		req = requests.get("https://emailverifierapi.com/v2/?apiKey=" + apiKey + "&email=" + email)
		reqJSON = req.json()
		if not "error" in reqJSON:
			if reqJSON['status'] == "passed":
				print("The email adress (" + email + ") exists!")
			elif reqJSON['status'] == "failed":
				if reqJSON['event'] == "mailboxDoesNotExist":
					print("The email address (" + email + ") does not exist!")
				elif reqJSON['event'] == "mailboxIsFull":
					print("The mailbox of the email address (" + email + ") is full!")
				elif reqJSON['event'] == "domainDoesNotExist":
					print("The domain of the email address (" + email + ") does not exist!")
				elif reqJSON['event'] == "mxServerDoesNotExist":
					print("The MX server of the email address (" + email + ") does not exist!")
				elif reqJSON['event'] == "invalidSyntax":
					print("The entered email address (" + email + ") has an invalid syntax!")
				elif reqJSON['event'] == "possibleSpamtrap":
					print("The email address (" + email + ") is possibly a spamtrap!")
				else:
					print("A mistake has been made!")
			elif reqJSON['status'] == "unknown":
				print("The email address (" + email + ") is unverifiable!")
			elif reqJSON['status'] == "transient":
				print("The email address (" + email + ") is temporarily unverifiable!")
			else:
				print("A mistake has been made!")
			sys.exit()
		else:
			print("The key entered in the configuration file (config.json) is invalid!")
			sys.exit()
	else:
		print("A mistake has been made!")

def fileMode():
	print("The file should have a structure like this:")
	print("mail1@domain.com\nmail2@domain.com\nmail3@domain.com\nmail4@domain.com\nmail5@domain.com\n")
	filePath = input("Enter the name of the file containing the email addresses: ")
	if os.path.exists(filePath):
		try:
			with open(filePath, "r") as emailFile:
				emailList = emailFile.readlines()
				emailFile.close()
			emailList = [x.strip() for x in emailList]
			print("")
			for mail in emailList:
				req = requests.get("https://emailverifierapi.com/v2/?apiKey=" + apiKey + "&email=" + mail)
				reqJSON = req.json()
				if reqJSON["status"] == "passed":
					print("\033[32m", mail)
				elif reqJSON["status"] == "failed":
					print("\033[31m", mail)
				else:
					print("\033[90m", mail)
			print("\033[0m \nAll email addresses have been checked!")
		except:
			print("A mistake has been made!")
		sys.exit()
	else:
		print("The file does not exist!")
		sys.exit()

print("");
print("   ███████ ███    ███  █████  ██ ██       ██████ ██   ██ ███████  ██████ ██   ██ ███████ ██████  ")
print("   ██      ████  ████ ██   ██ ██ ██      ██      ██   ██ ██      ██      ██  ██  ██      ██   ██ ")
print("   █████   ██ ████ ██ ███████ ██ ██      ██      ███████ █████   ██      █████   █████   ██████  ")
print("   ██      ██  ██  ██ ██   ██ ██ ██      ██      ██   ██ ██      ██      ██  ██  ██      ██   ██ ")
print("   ███████ ██      ██ ██   ██ ██ ███████  ██████ ██   ██ ███████  ██████ ██   ██ ███████ ██   ██ ")
print("           By VCoding - https://github.com/vincent-coding/emailchecker")

print("\n Please choose an option.")
print(" 1 - Simple mode")
print(" 2 - File mode")
print(" 3 - Exit\n")
option = input(" > ")

if option == "1":
	simpleMode()
elif option == "2":
	fileMode()
elif option == "3":
	print("\nGood bye !")
	sys.exit()
else:
	print("Your entry is not a valid option!")
	sys.exit()