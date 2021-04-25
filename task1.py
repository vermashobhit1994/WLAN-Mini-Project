""" ################################## MODULE DESCRIPTION #########################"""
#Module Description : Provides the functionality to display and scan nearby wifi devices   
#Name of Person : DharaniRaj
""" ################################################################################"""


from rssi import RSSI_Scan#to extract cell data 
from pywifi import wifi#to get the wifi interface name 

#import from same directory
import convert_list_of_tuples
import check_connection_state


from Error_Flags import *

def extract_essid_signal_strength(WIFI_INTERFACE):
    
    #to extract the raw data of cell 
    rssi_obj = RSSI_Scan(WIFI_INTERFACE)
    out = rssi_obj.getRawNetworkScan(sudo=True)
    out = out['output']
    out = out.decode()

    #getting the current cell data
    #it gives only signal strength, ssid and quality for particular cell
    format_cells = rssi_obj.formatCells(out)

    if format_cells == 0 or format_cells == 1:
        print("Error in extracting bool data ",format_cells)
    else:
        if check_connection_state.check_connection_state():
            ssid_list = []
            signal_list = []
            signal_state_list = [] 
            i = 0

            while i < len(format_cells) and len(format_cells) >= 0:
                data = format_cells[i]
                
                current_ssid = data['ssid']
                ######################################################
                #add *** to check the current device connected
                AP_ssid = check_connection_state.check_connection_state()
                
                if current_ssid == AP_ssid and AP_ssid != False:
                    current_ssid += '************'
                ##################################################
                
                ssid_list.append(current_ssid)
                signal_list.append(str(data['signal'])+'dbm')
                #check for strong,low or medium signal
                if int(data['signal']) <= 0 and int(data['signal'])>= -50:
                    signal_state_list.append("Strong")
                elif int(data['signal']) >= -90 and data['signal'] <-50:
                    signal_state_list.append("Medium")
                else:
                    signal_state_list.append("Low")
                
                i += 1
            
            newlist = convert_list_of_tuples.func_convert_list_of_tuple(ssid_list,signal_list,signal_state_list)
            return newlist
                
        else:
            return None

def get_essid_signal_strength_state():
    #creating a object of PyWiFi class 
    wifi_obj = wifi.PyWiFi()

    
    try:
        #getting all interfaces 
        iface_obj = wifi_obj.interfaces()

    except Exception as err:
        ErrorName = type(err).__name__
        
        
        if ErrorName == "FileNotFoundError":
            return CONNECTION_ERROR#if not connected to WiFi then no interface name is found
        else:
            return PERMISSION_ERROR
    else:
        iface_obj = wifi_obj.interfaces()
        
        WIFI_INTERFACE = iface_obj[1].name()#get the current interface name    
        return extract_essid_signal_strength(WIFI_INTERFACE)
        
