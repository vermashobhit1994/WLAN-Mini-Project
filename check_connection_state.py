#check whether you're connected to wifi or not
#this is done by iwgettid -r which return the access point name if connected
import subprocess
from tkinter import messagebox
def check_connection_state():
    
    try:
        Popen_obj = subprocess.check_output(['iwgetid','-r'])
        #reading the output from stdout and decode to ascii 
        cmd_output= Popen_obj.decode( 'ascii',errors = 'backslashreplace')
        cmd_output = cmd_output[:-1]#remove the '\n'
        
        
    except:
        #print("Please connect to internet first")
        return False
    else:
        return cmd_output

def display_msg_disconnect():
    
    DISCONNECT_WINDOW_NAME = "Disconnect Window"
    DISCONNECT_WINDOW_MESSAGE = "Please connect to Internet first "
    messagebox.showinfo(DISCONNECT_WINDOW_NAME,DISCONNECT_WINDOW_MESSAGE)


check_connection_state()
