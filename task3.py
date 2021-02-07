""" ################################## MODULE DESCRIPTION #########################
#Module Description : Provides the functionality to display the signal strength
                        of each accesspoint detected for particular channel no and 
                        frequency.

#Name of Person : Ramakrishna
################################################################################"""

from tkinter import messagebox
#task3 of our project
from pywifi import wifi
import subprocess

import convert_list_of_tuples,check_connection_state
import iwlist_cmd_out#to get the raw data from iwlist scan and iwlist channel commmand 
######################### Get the 2.4GHz data #############

def Get2_4GHzAnd5GHz_Data(WIFI_INTERFACE):

    #extract the 2.4GHz channel and frequency data 
    Raw_Data = iwlist_cmd_out.GetChannelNoFreqData()
    Channel_Raw_Data = Raw_Data[0]["Channels"] 
    Freq_Raw_Data = Raw_Data[1]["Freq"]
    
    #storing in temp to be used by 5GHz
    Temp_Channel_Raw_Data = Channel_Raw_Data.copy()
    Temp_Freq_Raw_Data = Freq_Raw_Data.copy()
    
    
    #getting the 2.4GHz frequency data
    #removing the 5 GHz frequency data
    index = 0
    for (channel,freq) in list(zip(Channel_Raw_Data,Freq_Raw_Data)):
        if freq.find('5.') != -1:
            Channel_Raw_Data.remove(channel)
            Freq_Raw_Data.remove(freq)
    
    #extracting cell data
    Cell_Raw_Data_dict = iwlist_cmd_out.extract_cell_data(WIFI_INTERFACE)
    #proceed only if no error while extracting data
    if Cell_Raw_Data_dict != None:
        #making a list of tuple
        Data_2_4GHz_tuple = convert_list_of_tuples.func_convert_list_of_tuple(Channel_Raw_Data,Freq_Raw_Data)

        
        ############### adding the signal strength to all cells##########
        index = 0
        current_ssid_name = check_connection_state.check_connection_state()
        for tuple_data in Data_2_4GHz_tuple:
            temp = ()
            
            for dict_data in  Cell_Raw_Data_dict:
                
                
                #specify the used frequency 
                #checking the current frequency used with router nearby frequency
                #also checking the current ssid name  
                if tuple_data[1] == dict_data["Freq"] :#comparing the frequency
                    ######## adding the signal level to Data_2_4GHz_tuple
                    
                    temp = list(tuple_data)
                    
                    #add the siglevel only if frequency of AP isn't repeats
                    #add only if current signal level not in temp
                    signal_data = dict_data['Siglevel']

                    ########### adding ******* to current signal strength #############
                    
                    if dict_data['ssid'] == current_ssid_name:
                        current_freq = dict_data['Freq']
                        if tuple_data[1] == current_freq:#if frequency matches 
                                signal_data += "********"


                    ###################################################################
                
                    #adding the signal level 
                    temp.append(signal_data)

                    temp = tuple(temp) #convert back to tuple 
                    
                    #remove the old item
                    Data_2_4GHz_tuple.remove(tuple_data)

                    
                    #add the updated item
                    Data_2_4GHz_tuple.insert(index,temp)    
                
                    #update the tuple_data
                    #add signal strength for two router if there are same frequency 
                    tuple_data = temp
                    
                
            index += 1
        #####################################################
        ######################### Get the 5GHz data #############

        #done since to get the unchanged data
        Channel_Raw_Data = Temp_Channel_Raw_Data.copy()
        Freq_Raw_Data = Temp_Freq_Raw_Data.copy()
        
        #getting the 5GHz frequency data
        #removing the 2.4GHz frequency and channel data
        index = 0
        for (channel,freq) in list(zip(Channel_Raw_Data,Freq_Raw_Data)):
            if freq.find('2.4') != -1:
                Channel_Raw_Data.remove(channel)
                Freq_Raw_Data.remove(freq)

        #extracting cell data
        Cell_Raw_Data_dict = iwlist_cmd_out.extract_cell_data(WIFI_INTERFACE)
        Data_5GHz_tuple = convert_list_of_tuples.func_convert_list_of_tuple(Channel_Raw_Data,Freq_Raw_Data)
        

        ############### adding the signal strength ##########
        index = 0
        #get the data of current ssid used
        current_ssid_name = check_connection_state.check_connection_state()
                    
        for tuple_data in Data_5GHz_tuple:
            temp = ()
        
            for dict_data in  Cell_Raw_Data_dict:
                
                #specify the used channelNO
                if tuple_data[1] == dict_data["Freq"] :#comparing the frequency
                    ######## adding the signal level to Data_2_4GHz_tuple
                    
                    temp = list(tuple_data)
                    signal_data = dict_data['Siglevel']

                    ########### adding ******* to current signal strength #############
                    if dict_data['ssid'] == current_ssid_name:
                        current_freq = dict_data['Freq']
                        if tuple_data[1] == current_freq:#if frequency matches 
                                signal_data += "********"


                    ###################################################################
                
                    
                    #adding the signal level 
                    temp.append(signal_data)
                
                    temp = tuple(temp) #convert back to tuple 
                    
                    #remove the old item
                    Data_5GHz_tuple.remove(tuple_data)

                    #add the updated item to current index
                    Data_5GHz_tuple.insert(index,temp)  
                    #################################################################
                    #update the tuple_data
                    #add signal strength for two router if there are same frequency 
                    tuple_data = temp
                    
                
            index += 1
            
        
        return [Data_2_4GHz_tuple,Data_5GHz_tuple]       
    else:
        messagebox.showerror("Error in iwlist scan command extraction")
        
############################################################################




#########################################################

###############getting the interface name###############


def get_both_freq_data():
    #creating a object of PyWiFi class 
    wifi_obj = wifi.PyWiFi()

    #getting all interfaces 
    try:
        iface_obj = wifi_obj.interfaces()

    except:
        print("Required sudo permissions to access wifi interface")
        return -1
    else:
        iface_obj = wifi_obj.interfaces()
        WIFI_INTERFACE = iface_obj[1].name()#get the current interface name    
        if check_connection_state.check_connection_state():
            data = Get2_4GHzAnd5GHz_Data(WIFI_INTERFACE)
            return data
        else:
            return None

################## end of program ###########################################
##############################################################################
