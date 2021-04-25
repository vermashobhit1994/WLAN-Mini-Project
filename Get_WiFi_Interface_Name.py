
""" Module to get the Wifi interface name e.g wlp3s0, wlp3s2"""
#module to get the wifi interface name
from pywifi import PyWiFi
from tkinter import messagebox

#user define module for error 
from Error_Flags import * 


#Here we are assuming that only single wifi card is connected to system.
def Get_WiFi_Interface_Name():
    
	
    #creating an object of PyWiFi class
    wifiobj = PyWiFi()
	
    wifi_interface_name = -1
    wifi_interfaces = []
    #getting the list of all the wifi interfaces connected to system
    try:
        wifi_interfaces = wifiobj.interfaces()
        
    except (FileNotFoundError,PermissionError,Exception) as err:
         
         ErrorName = type(err).__name__
         ErrorMsg = str(err)
         
         
         if ErrorName == "FileNotFoundError":#error when we aren't connected to WiFi
             return CONNECTION_ERROR
         elif ErrorName == "PermissionError": #error when Permissions aren't given
             return PERMISSION_ERROR
    
    else:
        for item in wifi_interfaces:
            wifi_interface_name = item.name()
  
	    #check the wifi interface name start with "wl"
            if wifi_interface_name[0:2] == "wl":    
                break
                
        return wifi_interface_name
 
         
                
		

