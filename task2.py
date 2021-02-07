""" ################################## MODULE DESCRIPTION #########################"""
#Module Description : Provides the Details of connected devices to router.
                    # This include name, IP Address and MAC Address of device. 
#Name of Person : Delli Priya
""" ################################################################################"""


import subprocess,re,sys,platform
import convert_list_of_tuples
import check_connection_state


""" To extract address from ifconfig command """
def extract_inet_mac_addr():
    #list that contains the inet address and mac address
    device_addr_list = []

    ipaddr_metadata = subprocess.check_output(['ifconfig'])
    data = ipaddr_metadata.decode()

    ######################## Extract the device ip and mac address##########################
    # Extract the inet address only if connected to internet
    device_inet_metadata = re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",data)
    
    try :
        device_inet_addr = device_inet_metadata[2]
    except  :
        return 
    else:
        #add the inet address to inet_addr_list
        device_inet_addr = device_inet_metadata[2]
        device_addr_list.append(device_inet_addr)

        ############# Here the MAC Address is extracted only if inet address is found
        #Extract the device MAC Address and add it to device_addr_list
        device_mac_addr_metadata = re.findall("HWaddr ([0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2})",data)
        
        #extract the mac address
        device_mac_addr = device_mac_addr_metadata[1]
        
        device_addr_list.append(device_mac_addr)
        return device_addr_list

#used to get the ip,mac and name of device
def Device_Details():

    #device_addr_list[0] means inet address , device_addr_list[1] means mac address
    #here it is done for current device  
    device_addr_list =  extract_inet_mac_addr()
    
    #replace the last digit of ip address by 0/24 only if connected to internet
    try:
        #replace the last digit of ip address by 0 and add /24
        inet_search_addr = re.sub("[0-9]+\Z","0/24",device_addr_list[0]) 
        
    except:
        #print("Please connect to internet first to search for ip address")
        return None
    else:
        #search all the ip address and mac address 
        cmd_meta_data = subprocess.check_output(['nmap','-sn',inet_search_addr])
        cmd_data = cmd_meta_data.decode('utf-8',errors="backslashreplace")
        return extract_ip_mac_addr_name(cmd_data,device_addr_list[0],device_addr_list[1])
        


#data returned as list of tuples
#if device isn't connected then return None
def get_device_details():
    return Device_Details()
    

#get the ip , mac address and name of devices as list of tuples
def extract_ip_mac_addr_name(string,device_inet_addr,device_mac_addr):
    
    ip_addr_list = []
    mac_addr_list = []
    ssid_list = []

    ####### extract the mac and ip address of access point and devices connected ##########
    #ip_addr_list[0] -> ip addr for access point 
    ip_addr_list = re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",string)
    #mac_addr_list[0] -> mac addr for access point
    mac_addr_list = re.findall("[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}\:[0-9 A-Z a-z]{2}",string)
    

    

    ####### add the mac address of current device to the mac_addr_list at inet address index 
    # if the ip address is found in ip_addr_list
    if device_inet_addr in ip_addr_list:
        index = ip_addr_list.index(device_inet_addr)
        #if mac address found then add to mac_addr_list
        if mac_addr_list:
            mac_addr_list.insert(index,device_mac_addr)
        #if mac_addr_list is empty then put the empty '' where mac address isn't found
        else:
            for i in range(0,index+1):
                mac_addr_list.insert(i,'')
            mac_addr_list.insert(index,device_mac_addr)

       

    
    ##### Add the current device,access point name to ssid_list
    #get the ssid name of router Access Point
    ssid_access_point_name = check_connection_state.check_connection_state()
    
    #append the access point name to ssid_list
    ssid_list.append(ssid_access_point_name)
    
    #extract the other device company name 
    device_cmpny = re.findall("""MAC Address: ..\:..\:..\:..\:..\:.. \(([\w ]+)\)""",string)
    
    #remove the first element if run with sudo
    if device_cmpny:
        device_cmpny.remove(device_cmpny[0])#remove the name of router i.e unknown
    
    #exclude the access point name 
    #append the hostname to ssid_list by adding empty string where no hostname found
    #put the empty string until hostname address isn't matched
    i = 0
    for ipaddr in ip_addr_list[1:len(ip_addr_list)+1]:
        
        #if device ip address isn't matched then put ''
        if ipaddr != device_inet_addr:
            
            #if found any device company name add to the ssid list
            #checking if device exists in device_cmpny list
            if device_cmpny and i < len(device_cmpny):
                ssid_list.append(device_cmpny[i])
                i += 1
            #if don't find company name put ''
            else:
                ssid_list.append('') 
        #add the device name to ssid_list  
        else :
            hostname = str(platform.node())
            ssid_list.append(hostname)

    
    #add the *** to current ip address
    index_current_ipaddr = ip_addr_list.index(device_inet_addr)
    ip_addr_list[index_current_ipaddr] = ipaddr+"*******"
    
    
    #importing module to convert to list of tuples from list of lists
    extract_data = convert_list_of_tuples.func_convert_list_of_tuple(ip_addr_list,mac_addr_list,ssid_list)
    return extract_data







    






