''' DataConn.py '''
print(" - DataConn.py loaded")

import sqlite3
import PasswordHandler
database = "accounts.db"

### This variable overwrites the DEBUG variable present in the main.py file - this allows for each section of the code to be developed and debugged independantly ###
DEBUG = False

### This function checks if the tblAccounts table exists, if it does then it prints that it is found, if it does not then it creates the table and prints that it has created a new table ###
def initialize():
	try:
		c.execute("SELECT * FROM tblAccounts")
		print("   Accounts table found")
	except:
		print("   Accounts table not found - generating")
		createtable("tblAccounts", "(username TEXT, password TEXT, firstname TEXT, surname, PRIMARY KEY (username))")

def createtable(tblName, SQLCMD):
	try:
		c.execute("CREATE TABLE " + tblName + " " + SQLCMD)
		conn.commit()
		print("   Successfully created " + tblName)
	except:
		error("   Could not create " + tblName + ". Either the table exists or SQL is malformed")

def createrecord(tblName, records):
	try:
		c.execute("INSERT INTO " + tblName + " VALUES " + records)
		conn.commit()
		return True
	except:
		return False

### This function checks the given username and password against the one that are stored in the database - if they match then the user is allows access, if not then an error is given ###
def checklogin(username, password):
	dbpassword = ''
	for row in c.execute('SELECT password FROM tblAccounts WHERE username = "' + username + '"'):
		dbpassword = str(row)[3:int(len(row)-4)]
		dbpassword = PasswordHandler.decrypt(dbpassword)
	if password == dbpassword:
		if password == "": #Check if the entered password is NULL - if so, do not allow login
			return False #' password is empty '#
		else:
			return True #' password is correct '#
	else:
		return False #' password is incorrect or username does not exist '#

### This function formats the firstname and surname that are stored in the database, which uses the username to pull the information ###
def getName(username):
	firstName = ''
	surname = ''
	for row in c.execute('SELECT firstname FROM tblAccounts WHERE username = "' + username + '"'):
		firstName = str(row)[3:int(len(row)-4)]
	for row in c.execute('SELECT surname FROM tblAccounts WHERE username = "' + username + '"'):
		surname = str(row)[3:int(len(row)-4)]
	return firstName + " " + surname

### This correctly formats any errors for the console so that they stand out against the other text ###
def error(msg):
	print(' ERROR '.center(80, '*'))
	print('*' + msg.center(78, ' ') + '*')
	print(''.center(80, '*'))

try:
	conn = sqlite3.connect(database)
	print("   Connected to " + database)
	c = conn.cursor()
	initialize()
except:
	print("   ERROR: Could not connect to " + database)

### Allows the developer to see the contents of the database - useful when programming the fucnctions that interact with the database ###	
if DEBUG == True:
	for row in c.execute('SELECT * FROM tblAccounts'):
		print(row)
