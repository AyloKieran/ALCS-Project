''' PasswordHandler.py '''
print("   - PasswordHandler.py loaded")

### I decided to use a pre-made library for the cryptogpraphy of the passwords as I felt that it would be more secure and robust than one I could create myself ###
from cryptography.fernet import Fernet

### I used a randomly generated key to salt the encryption process, so that if the database is ever stolen, then the attacker would not be able to decrpypt the passwords without also knowing the key that they were encrpyed with, adding another level of security to the system ###
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher = Fernet(key)

### These functions allow for the password handling to be called from the entirity of the program without having to first call the prerequisites ###
def encrypt(password):
	encryptedpassword = cipher.encrypt(password)
	return encryptedpassword

def decrypt(password):
	decryptedpassword = cipher.decrypt(password)
	return decryptedpassword