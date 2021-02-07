""" ################################## MODULE DESCRIPTION #########################
#Module Description : Provides the functionality to display the ssid name of
                        each accesspoint detected for particular channel no and 
                        frequency.
#Name of Person : Lakshminarayana
################################################################################"""


#This task will find the device names alongwith channels used of nearby devices
import subprocess,re,platform
WIFI_INTERFACE_NAME = 'wlp3s0'
import convert_list_of_tuples,check_connection_state
#import capture_data_frame


#scan all channels and convert whole output into list of strings
def scan_all_channels_with_freq(interface):
    #run the command using Popen() and collect output
    cmd = ["iwlist","channel"]
    Popen_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #read the data from stdout and convert into string from binary string
    channel_No_with_freq_out_str = Popen_obj.stdout.read().decode('ascii',errors="backslashreplace")
    
    #get the channel and freq and convert into list of strings
    channel_No_with_freq_out_str = channel_No_with_freq_out_str.replace("\r","")
    channel_No_with_freq_list= channel_No_with_freq_out_str.split("\n")
    channel_No_with_freq_list=channel_No_with_freq_list[1:]
    return channel_No_with_freq_list

#scan all 2.4GHz channel alongwith frequency
def scan_2_4GHz_channel_with_freq():
    ch=scan_all_channels_with_freq(WIFI_INTERFACE_NAME)

    channel_No_freq_list=[]
    i=0
    for item in ch:
         
        current_channel_No_freq_tuple = ()#Initialize tuple
        #find the frequency that start with 2.4 and store it into channel_No_freq_list
        if item.find('2.4')>0:
            #item=str(item)
            
            #omit the leading spaces and put the current channel in tuple
            current_channel_No=item[10:(10+11)]
            
            
            #Storing the current channel No in current_channel_No_tuple  
            current_channel_No_freq_tuple = current_channel_No_freq_tuple+(current_channel_No,)

            #extract the frequency and store it into current_channel_No_freq_tuple
            current_freq=item[23:]
            

            current_channel_No_freq_tuple=current_channel_No_freq_tuple+(current_freq,)
            channel_No_freq_list.append(current_channel_No_freq_tuple)
            del current_channel_No_freq_tuple#delete the tuple to store next channel no and frequency
        
        #If find the current frequency used then append that whole string 
        #into channel_No_freq_list
        if item.find("Current Frequency:2.4")>0:
            channel_No_freq_list=channel_No_freq_list[:-1]
            
    return channel_No_freq_list

#scan all the 5GHz channel with freq and return in form of list of strings
def scan_5GHz_channel_with_freq():
    ch=scan_all_channels_with_freq(WIFI_INTERFACE_NAME)
    lis=[]
    i=0
    
    for item in ch:
        ch1=()
        
        if item.find('5.')>0:
            item=str(item)
            channel=item[10:(10+11)]#extract the channel NO
            
            ch1=ch1+(channel,)
            freq=item[23:]
            freq = freq.strip()

            ch1=ch1+(freq,)
            lis.append(ch1)
            del ch1
        if item.find("Current Frequency:5.")>0:
            lis=lis[:-1]
    
    return lis


def scan_all_channels_nearby_devices(interface):
    
    #run the command using Popen() and collect output
    cmd = ["sudo","iwlist", interface, "scan"]
    Popen_obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #read the data from stdout and convert into string from binary string
    channel_No_with_freq_out_str = Popen_obj.stdout.read().decode('ascii',errors="backslashreplace")

    return channel_No_with_freq_out_str

def extract_all_data():

    data = scan_all_channels_nearby_devices(WIFI_INTERFACE_NAME)
    #print(data)
    
    #creating a list of channel ,frequency and essid 
    #freq_devices_list,channel_No_list,SSID_list = re.findall("Frequency:([25]\.[0-9]+)",data)
    channel_data_list = re.findall("Channel:[0-9]+",data)
    Frequency_data_list = re.findall("Frequency:([25]\.[0-9]+ GHz)",data)
    ssid_data_list = re.findall("ESSID:\"(\S+)\"",data)
    #print(channel_data_list,Frequency_data_list,ssid_data_list)



    #used by 5 GHz frequency . Here created a copy by copy() to avoid change by 2.4GHz
    temp_channel_data_list = channel_data_list.copy()
    temp_Frequency_data_list = Frequency_data_list.copy()
    temp_ssid_data_list = ssid_data_list.copy()
    #print(temp_channel_data_list,temp_Frequency_data_list,temp_ssid_data_list)


##################################### Extracting data for 2.4GHz##################

    

    #Remove the 5 GHz frequency from list
    for (ch,freq,ssid) in zip(channel_data_list,Frequency_data_list,ssid_data_list):
        #if find the 5GHz frequency then remove that entry from all three lists
        
        if freq.find('5.') != -1:
            #print("matched")
            Frequency_data_list.remove(freq)
            channel_data_list.remove(ch)
            ssid_data_list.remove(ssid)
    
   
    #print(channel_data_list,Frequency_data_list,ssid_data_list)
    data_2_4GHz = convert_list_of_tuples.func_convert_list_of_tuple(channel_data_list,Frequency_data_list,ssid_data_list)
    #print("DDDDDDD",data_2_4GHz)

    #get the updated data without username added for 2.4GHz
    channels_data_2_4GHz = scan_2_4GHz_channel_with_freq()
    #print("2.4GGGGGGGGGGGGG",channels_data_2_4GHz)


    ################ checking the current ssid used and add **** to it
    #get the output of iwgetid -r command
    cmd_out_metadata = subprocess.check_output(['iwgetid','-r'])
    cmd_out = cmd_out_metadata.decode('ascii')
    current_ssid = cmd_out[:-1]#remove '\n'

    #for item in data_2_4GHz:
    #    if item[2] == current_ssid and current_ssid != '':
            
    ###################################################################

    ################ Adding the SSID to channels list#####################

    nearby_router_index = 0   
    for item_nearby_router in data_2_4GHz:
        #Case I : if frequency and channel of two or more routers are same

        #Case II : If frequency and channel of two or more routers are different
        #checking the frequency of channels list with channels used by nearby routers
        item_index = 0
        for item_channel in channels_data_2_4GHz:
            temp_tuple = ()
            
            if item_nearby_router[1] == item_channel[1]:
                #print("match found")

                #adding the ssid name to channels list 
                ssid_name = item_nearby_router[2]
                temp_list = list(item_channel)

                ########### adding ******* to current ssid name #############
                current_ssid_name = check_connection_state.check_connection_state()
                if ssid_name == current_ssid_name:
                    ssid_name += "********"
                ################################################################           

                temp_list.append(ssid_name)
                temp_tuple = tuple(temp_list)

                #removing the old item
                channels_data_2_4GHz.remove(item_channel)

                #add the new item at particular index
                channels_data_2_4GHz.insert(item_index,temp_tuple)

                #update the item_channel
                #add signal strength for two router if there are same frequency
                item_channel = temp_tuple
            item_index += 1 
                

    #print(channels_data_2_4GHz)

    ########################################################################

##################################### Extracting data for 5GHz##################

        
    
    #creating a temporary list for removing data
    channel_list = temp_channel_data_list.copy()
    freq_list = temp_Frequency_data_list.copy()
    ssid_list = temp_ssid_data_list.copy()

    

    #Remove the 2.4 GHz frequency from list
    for (ch,freq,ssid) in zip(channel_data_list,Frequency_data_list,ssid_data_list):    
        #if find the 2.4GHz frequency then remove that entry from all three lists        
        if freq.find('2.4') != -1:
            #print("matched")
            channel_list.remove(ch)
            freq_list.remove(freq)
            ssid_list.remove(ssid)

    
    #print(channel_list,freq_list,ssid_list)
    #get the updated data without username added for 5GHz
    channels_data_5GHz = scan_5GHz_channel_with_freq()
    #print(channels_data_5GHz)

    
    #to remove any leading or trailing spaces from frequency list
    #for item in 
    #for i in range(len(Frequency_data_list)):
    #    Frequency_data_list[i] = Frequency_data_list[i].strip()
        

    #convert data into list of tuples
    data_5GHz = convert_list_of_tuples.func_convert_list_of_tuple(channel_list,freq_list,ssid_list)
    #print(data_5GHz)
    
    ################ Adding the SSID to channels list#####################

    nearby_router_index = 0   
    for item_nearby_router in data_5GHz:
        
        
        
        #Case I : if frequency and channel of two or more routers are same

        #Case II : If frequency and channel of two or more routers are different
        #checking the frequency of channels list with channels used by nearby routers
        item_index = 0
        for item_channel in channels_data_5GHz:
            
            temp_tuple = ()
            
            #checking the frequency of nearby router with available channel frequency
            if item_nearby_router[1] == item_channel[1]:
                

                ###################### adding the ssid name to channels list 
                ssid_name = item_nearby_router[2]
                temp_tuple = list(item_channel)
                
                ########### adding ******* to current ssid name #############
                current_ssid_name = check_connection_state.check_connection_state()
                if ssid_name == current_ssid_name and current_ssid_name != False:
                    ssid_name += '**********'
                ################################################################           


                temp_tuple.append(ssid_name)
                temp_tuple = tuple(temp_tuple)

                #removing the old item
                channels_data_5GHz.remove(item_channel)

                #add the new item
                channels_data_5GHz.insert(item_index,temp_tuple)

                #print(channels_data_5GHz,'\n\n')
                #update the item_channel
                #add signal strength for two router if there are same frequency
                item_channel = temp_tuple
                del temp_tuple

            item_index += 1 
        
    #print("FINAL",channels_data_5GHz,channels_data_2_4GHz)   
    return (channels_data_2_4GHz,channels_data_5GHz)
                


def get_data_both_freq():
    if not check_connection_state.check_connection_state():
        return None
    else:
        
        return extract_all_data()

