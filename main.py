''' main.py '''
### Import my custom made libraries ###
import DataConn
import CameraStreamer
import PasswordHandler
### Import existing libraries ###
from bottle import route, run, static_file, request, error, redirect, abort
import sys
import os

### Setup a Debug mode that can be used to disable the motor controls for when developing ###
DEBUG = True

if DEBUG != True:
	import RoverControl
	CMove = RoverControl.Control(9, 6)

### Create a function that can create symbolic links to files dynamically, regardless of the current working directory ###
def filepathgen(location):
  return os.getcwd() + "/" + location

'''WEB SERVER CODE BELOW'''

### This will take any request directly to the web server and forward them to the index page ###
@route('/')
def serve():
  return redirect("/index")

### This will serve any html file within the main directory ###
@route('/<filename>')
def webserver(filename):
    return static_file(filename + ".html", root=filepathgen(''))

### This function will only execute when a POST request is sent to the '/register' end point, and will interface with the database management codebase ###
@route('/register', method='POST')
def registerpost():
	username = request.forms.get('username')
	password = request.forms.get('password')
	firstname = request.forms.get('firstname').capitalize()
	surname = request.forms.get('surname').capitalize()

	if DataConn.createrecord('tblAccounts', "('" + username + "', '" + PasswordHandler.encrypt(password) + "', '" + firstname + "', '" + surname + "')") == True:
		return redirect("/login")
	else:
		return redirect("/register?error=Could not register account, that username is taken.")

### Similarly to the register function, this will only work when a POST request is recieved, and will interface with the database manegement codebase ###
@route('/drive', method='POST')
def do_login():
		username = request.forms.get('username')
		password = request.forms.get('password')
		if DataConn.checklogin(username, password) is True:
			return redirect("/drive?name="+DataConn.getName(username)+"&uname="+username)
		else:
			return redirect("/login?error=Incorrect username or password. Please try again.")

### If the file is not found by the web server, it will return a 404 page, instead of crashing ###
@error(404)
def error404(error):
    return static_file('404.html', root=filepathgen(''))

### Each move command will check the DEBUG variable to check weather to print the move to the console or to call the relevant function in the motor control library ###
@route('/api/move/<direction>')
def move(direction='none'):
	if direction == 'forwards':
		if DEBUG != True:
			CMove.forwards(0, 0.5)
		else:
			print("Forwards")
	elif direction == 'backwards':
		if DEBUG != True:
			CMove.backwards(0, 0.3)
		else:
			print("Backwards")
	elif direction == 'left':
		if DEBUG != True:
			CMove.left(0, 0.3)
		else:
			print("Left")
	elif direction == 'right':
		if DEBUG != True:
			CMove.right(0, 0.3)
		else:
			print("Right")
	elif direction == 'stop':
		if DEBUG != True:
			CMove.stop()
		else:
			print("Stop")
	else:
		abort(400, 'Invalid direction')

### Sets up a proper route to access any files from, using their symbolic link on the server ####
@route("/api/file/<filename>")
def raw(filename):
  return static_file(filename, root=filepathgen(''))

### Similar to the file route, this works exclusively in the images folder ###
@route('/api/img/<image>')
def image(image):
    return static_file(image, root=filepathgen('img/'))

### Starts the web server on the current interface, on a wildcard IP address with port 8081. This will also stop the server continuously reloading and will print all requests to the console ###
run(host='0.0.0.0', port=8081, debug=True, reloader=False)
