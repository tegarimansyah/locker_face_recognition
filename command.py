# Command.py
# Aplikasi untuk komunikasi serial dan logging
# Oleh: Dwi Fajar Suryanto
#

from datetime import datetime
import serial

def log(text):
    print(str(datetime.now().time()) + ': ' + text)

def send(text):
    print(text)
    
    