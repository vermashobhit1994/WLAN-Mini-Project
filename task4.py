""" ################################## MODULE DESCRIPTION #########################"""
#Module Description : Provides the display of internet speed.  
#Name of Person : Shanmitha Reddy
""" ################################################################################"""


import subprocess,os
import check_connection_state


def extract_data_cmd():
    #extract data of command output
    cmd = [ "sudo", "speedtest"]
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data= data.stdout.read().decode('ascii',errors="backslashreplace")
    
    
    data = data.split("\n")
    return data

#def get_speed_data():
def get_speed_data(pipe_obj):
    if not (check_connection_state.check_connection_state()):
        pipe_obj.send(None)
    else:    
        
        data = extract_data_cmd()
        
        list_data = []
    
        for line in data:
            #getting the download speed data 
            if (line.find("Download:")) != -1:
                index = line.index ("Download:")
                download_speed = line[index+len("Download:"):]
                list_data.append(str(download_speed))
            #gettig the upload speed data
            if line.find("Upload:") != -1:
                index = line.index ("Upload:")
                upload_speed = line[index+len("Upload:"):]
                
                list_data.append(str(upload_speed))

            #getting the hostname 
            if line.find("Hosted by ") != -1:
                index = line.index("Hosted by" )
                hosted_name = line[index+len("Hosted by"):-21]
                list_data.append(str(hosted_name))        
        
        pipe_obj.send(list_data)





    