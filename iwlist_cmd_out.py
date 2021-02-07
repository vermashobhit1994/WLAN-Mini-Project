import subprocess
from wifi import Cell#to get the data from iwlist scan cmd

##################### Extracting useful data from raw data ##
# here the data extracted in form of list of dictionary
def extract_cell_data(WIFI_INTERFACE):
    ######### Getting the data from 'iwlist scan' cmd ###########
    
    cells_data = []
    try :
        cells = list(Cell.all(WIFI_INTERFACE))
    except:
        print("Error in extracting cells data")
    else:
        for i in range(len(cells)):
            cell_dict = {}
            cell_dict["APMACAddr"] = cells[i].address
            cell_dict['Siglevel'] = str(cells[i].signal) + "dBm"
            cell_dict['ssid'] = cells[i].ssid
            cell_dict["ChannelNo"] = str(cells[i].channel)
            cell_dict["Freq"] = cells[i].frequency
            cell_dict["Quality"] = cells[i].quality
            cell_dict["Mode"] = cells[i].mode
            cells_data.append(cell_dict)
        
        return cells_data
    
    return None #if there is any error in getting interface name   
    
#####################################################################


################### extract channel no and Frequency from iwlist channel cmd ##############################
def GetChannelNoFreqData():
    
    #extracting the data from command
    cmd = ['iwlist','channel']
    cmd_raw_data = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    cmd_raw_data = cmd_raw_data.stdout.read().decode('ascii')#reading data from stdout 
    cmd_raw_data = cmd_raw_data.split('\n')
    del cmd_raw_data[0]#drop first data from list
    
    #getting the string for current frequency
    current_freq_raw_data =cmd_raw_data.pop(-3)
    
    ######## Deleting the last two entries
    del cmd_raw_data[-1:-3:-1]   

    
    i = 0
    channels_dict = {}
    freq_dict = {}
    channels_No = []
    Freq_Value = []
        
    
    for i in range(len(cmd_raw_data)):
        #extracting channel NO
        channels_No.append( (cmd_raw_data[i].split(' : '))[0].lstrip())
        #extracting frequency
        Freq_Value.append( (cmd_raw_data[i].split(' : '))[1])
    
    #making a dictionary with key
    channels_dict["Channels"] = channels_No
    freq_dict["Freq"] = Freq_Value
    return [channels_dict,freq_dict]#return list of dictionary


######################################################################

