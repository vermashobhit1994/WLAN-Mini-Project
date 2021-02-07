#Module to extract the current router ip
import subprocess,re

wifi_interface = 'wlp3s0'

#extract the router ip address by "nmcli dev show wlp3s0 command"
def extract_router_ipaddr():
    
    router_ip_addr = ""
    router_ip_metadata = subprocess.check_output(['nmcli', 'dev' ,'show' ,wifi_interface])
    router_ip_metadata = router_ip_metadata.decode('ascii',errors='backslashreplace')
    router_ip_metadata = router_ip_metadata.split('\n')
    for ipaddr in router_ip_metadata:
        if ipaddr.find('IP4.GATEWAY:') != -1:
            router_ip_addr = re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\Z',ipaddr)
            break
    try:
        return router_ip_addr[0]#extract ip address if connected to wifi 
    except:
        #print("Please connect to internet to access ip address")
        return None
    else:
        return router_ip_addr[0]

          