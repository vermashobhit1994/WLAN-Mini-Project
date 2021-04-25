#Module to extract the current router ip

import subprocess,re
from tkinter import messagebox

#user defined modules
import Get_WiFi_Interface_Name
from Error_Flags import * 
    

############ Note : -1 is used as error for not getting WiFi Interface Name 
############ Note : None is used as error for not connecting to WiFi .

#extract the router ip address by "nmcli dev show wlp3s0 command"
def extract_router_ipaddr():
    
    router_ip_addr = ""
    router_ip_metadata = ""
    
    wifi_interface = Get_WiFi_Interface_Name.Get_WiFi_Interface_Name()
   
    
    if wifi_interface != -1 and wifi_interface != None:
         
        try:
            router_ip_metadata = subprocess.check_output(['nmcli', 'device' ,'show' ,wifi_interface])
        except Exception as err:
            messagebox.showerror("Command Error nmcli",err)
            return NMCLI_CMD_ERROR
        else:
    
            router_ip_metadata   =router_ip_metadata.decode('ascii',errors='backslashreplace')
            router_ip_metadata = router_ip_metadata.split('\n')
            for ipaddr in router_ip_metadata:
                if ipaddr.find('IP4.GATEWAY:') != -1:
                    router_ip_addr = re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\Z',ipaddr)
                    break
    
            
            return router_ip_addr[0]
        
    else:
        return wifi_interface #if return None then Not connected to WiFi else Permissions error

          
