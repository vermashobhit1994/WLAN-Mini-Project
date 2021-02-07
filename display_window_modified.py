""" ################################## MODULE DESCRIPTION #########################"""
#Module Description : Provides the functionalities in display window
#Name of Person : Shobhit Verma
""" ################################################################################"""

from multiprocessing import Process,Pipe

#from tkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess,os,stat

################ import module by other persons #####################                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       vices Connected  module ################
import task2,task5,task4,task3,task1

import extract_router_ipaddr,check_connection_state

##################################################
######## to wait in speed test function ##########
def wait_func(current_tab,time_amt):
      
    var = IntVar()
    current_tab.after(time_amt,var.set,1)
    current_tab.wait_variable(var)#actual wait statement
    
####################### event handler function start ###################################   
#arg1 stores all the object of tabs created and arg2 stores the ipaddresss
################ event handler function i.e when the tab is select 
def event_handler_func(event,tab_obj_list,ip_addr,display_frame_tab_ctrl,close_window_btn):    
    tab_text = event.widget.tab('current')['text']
    
    if tab_text == "Show Signal Strength ":
        #field names of connected_devices_tab
        field_names = ["SSID_Name","Signal Strength","Signal Strength State"]
        
        #if we are on same tab
        if tab_text == "Show Signal Strength ":
            exclude_index = 0
            #disable all tabs
            control_tabs_state(False,display_frame_tab_ctrl,exclude_index)
            
            reset_data_treeview(tab_obj_list[0],field_names,0.8,0.9,0.04,0.05)
            
            #disable the button 
            close_window_btn["state"] = "disabled"
            

            #wait for some time
            wait_func(display_frame_tab_ctrl,100)

            

            #here arg[0] means signal strenght tab
            #also specify relheight,relwidth,relx and rely for treeview
            show_signal_strength(tab_obj_list[0],field_names,0.8,0.9,0.04,0.05)
    
            #enable all tabs 
            control_tabs_state(True,display_frame_tab_ctrl,exclude_index) 
            #enable the button 
            close_window_btn["state"] = "normal"
            


        
    elif tab_text == " Show Connected Devices ":
        field_names = ["Device IP","Device MAC Address","Device Name"]
        
        #checking againt the tab_text if it's changed or not
        tab_text = event.widget.tab('current')['text']
        
        #if we are on same tab
        if tab_text == " Show Connected Devices ":
            exclude_index = 1
            #disable all tabs
            control_tabs_state(False,display_frame_tab_ctrl,exclude_index)
            #disable the button 
            close_window_btn["state"] = "disabled"
            
            reset_data_treeview(tab_obj_list[1],field_names,0.8,0.9,0.04,0.05)

    
            #wait for some time
            wait_func(display_frame_tab_ctrl,100)

            #also specify relheight,relwidth,relx and rely for treeview
            show_connected_devices(tab_obj_list[1],field_names,ip_addr,0.8,0.9,0.04,0.05)
        
            #enable all tabs 
            control_tabs_state(True,display_frame_tab_ctrl,exclude_index) 
            #enable the button 
            close_window_btn["state"] = "normal"
            
        
        
    elif tab_text == " Show Speed Test ":
        
        #wait for certain amount of time
        #here 1000 means 1 sec 
        wait_func(display_frame_tab_ctrl,3000)
                
        #checking againt the tab_text if it's changed or not
        tab_text = event.widget.tab('current')['text']
        
        #if we are on same tab
        if tab_text == " Show Speed Test ":
            exclude_index = 2
            #disable all tabs
            control_tabs_state(False,display_frame_tab_ctrl,exclude_index)
            #disable the button 
            close_window_btn["state"] = "disabled"
            messagebox.showinfo("Disable tabs Window","All tabs disabled")

            #reset data before putting new data
            Reset_speed_test_data(tab_obj_list[2])
            
            #wait for some time
            wait_func(display_frame_tab_ctrl,100)

            #control_tabs_state(False,display_frame_tab_ctrl)
            show_speed_test(tab_obj_list[2],display_frame_tab_ctrl)

            #enable all tabs 
            control_tabs_state(True,display_frame_tab_ctrl,exclude_index) 
            #enable the button 
            close_window_btn["state"] = "normal"
            
            messagebox.showinfo("Enable tabs window","All tabs enabled")
            
        
    elif tab_text == " Show Channel Signal Strength ":
        field_names = ["Channel No ","Channel Frequency","Channel Signal Strength"]
        dimension_2_4GHz = (0.8,0.47,0.01,0.04)
        dimension_5GHz = (0.8,0.51,0.49,0.04)
        
        #checking againt the tab_text if it's changed or not
        tab_text = event.widget.tab('current')['text']
        
        #if we are on same tab
        if tab_text == " Show Channel Signal Strength ":
            exclude_index = 3
            #disable all tabs
            control_tabs_state(False,display_frame_tab_ctrl,exclude_index)
            
            #disable the button 
            close_window_btn["state"] = "disabled"
            

            #reset old data value for 2.4GHz
            reset_data_treeview(tab_obj_list[3],field_names,dimension_2_4GHz[0],
            dimension_2_4GHz[1],dimension_2_4GHz[2],dimension_2_4GHz[3])

            #reset old data value for 5GHz
            reset_data_treeview(tab_obj_list[3],field_names,dimension_5GHz[0],
            dimension_5GHz[1],dimension_5GHz[2],dimension_5GHz[3])

            
            #wait for some time
            wait_func(display_frame_tab_ctrl,100)

            #also specify relheight,relwidth,relx and rely for treeview
            show_channel_signal_strength(tab_obj_list[3],field_names,ip_addr,dimension_2_4GHz,dimension_5GHz)

            #enable all tabs 
            control_tabs_state(True,display_frame_tab_ctrl,exclude_index) 
            #enable  the button 
            close_window_btn["state"] = "normal"
            
        
        
        
    elif tab_text == " Show Channel Devices ":
        field_names = ["Channel No ","Channel Frequency","Connected channel ssid "]
        dimension_2_4GHz = (0.8,0.47,0.01,0.04)
        dimension_5GHz = (0.8,0.51,0.49,0.04)
        
        #if we are on same tab
        if tab_text == " Show Channel Devices ":
            exclude_index = 4
            #disable all tabs
            control_tabs_state(False,display_frame_tab_ctrl,exclude_index)
            
            #disable the button 
            close_window_btn["state"] = "disabled"
            
            #reset old data value for 2.4GHz
            reset_data_treeview(tab_obj_list[4],field_names,dimension_2_4GHz[0],
            dimension_2_4GHz[1],dimension_2_4GHz[2],dimension_2_4GHz[3])

            #reset old data value for 5GHz
            reset_data_treeview(tab_obj_list[4],field_names,dimension_5GHz[0],
            dimension_5GHz[1],dimension_5GHz[2],dimension_5GHz[3])

            #wait for some time
            wait_func(display_frame_tab_ctrl,100)

            #also specify relheight,relwidth,relx and rely for treeview
            show_scanned_devices(tab_obj_list[4],field_names,ip_addr,dimension_2_4GHz,dimension_5GHz)
        
            #enable all tabs 
            control_tabs_state(True,display_frame_tab_ctrl,exclude_index) 
            
            #enable the button 
            close_window_btn["state"] = "normal"
            
        
        
    
        
####################### event handler function ends ###################################   
    
        


##############################################################################################################################
#########################Create Second Window function start ###################################################
def create_second_window(router_ipaddr):
    
    tk_obj = Tk()
    tk_obj.configure(background='#5757ce')#background color
    
    full_width  = tk_obj.winfo_screenwidth()
    full_height = tk_obj.winfo_screenheight()
    

    window_title = "DISPLAY DATA WINDOW"
    tk_obj.geometry("%dx%d+0+0" % (full_width,full_height) )
    tk_obj.title(window_title)

    
    #Create a label for title
    title = Label(tk_obj,text=window_title,font=('helvetica',30,'bold'),bg='#154bcd',fg='white')
    title.place(relx=0,rely=0,relwidth=1)

    #make a frame so that buttons and other widgets can be put in it
    display_frame = Frame(tk_obj)
    display_frame.place(x=0,y=59,height=full_height-86,width=full_width-65)
    
#################################################################################################################################################
########################### creating the tabs ###################################################################################################
    #create a Style to add the color to frame to tab
    style = ttk.Style()
    style.configure("TNotebook.Tab",font=('Times New Roman', 18 ,'bold'), foreground = '#0c0c0c',background='#afedfc')
    
    #creating the control for all the tabs that is being created
    display_frame_tab_ctrl = ttk.Notebook(display_frame,height=full_height-120,width=full_width-150)
    display_frame_tab_ctrl.place(relx=1,rely=1,x=10,y=10)
    
    
    """#################### bind() is used to capture the trigger event##############"""
    """ NOTE : Use event as parameter in callback function ###############"""
    ############ creating the signal strength tab#########################
    signal_strength_tab = ttk.Frame(display_frame_tab_ctrl,style="TNotebook.Tab")
    
    display_frame_tab_ctrl.add(signal_strength_tab,text="Show Signal Strength ",state="normal") 
    display_frame_tab_ctrl.pack()
    
    
    ############ creating the signal strength tab ends #########################
     

    ############ creating the connected devices tab start #########################
    
    connected_devices_tab = ttk.Frame(display_frame_tab_ctrl,style="TNotebook.Tab")
    display_frame_tab_ctrl.add(connected_devices_tab,text=" Show Connected Devices ",state="normal") 
    display_frame_tab_ctrl.pack()
    ###################### create of connected devices tab ends ###################
    
    ###################### create of speed test tab start ###################
    #create a speed test tab
    speed_test_tab = ttk.Frame(display_frame_tab_ctrl,style="TNotebook.Tab")
    display_frame_tab_ctrl.add(speed_test_tab,text=" Show Speed Test ",state="normal") 
    display_frame_tab_ctrl.pack()

    ###################### create of speed test tab ends ###################
    

    ###################### create of channel signal strength tab start ###################
    #create a channel signal strength tab
    
    channel_signal_strength_tab = ttk.Frame(display_frame_tab_ctrl,style="TNotebook.Tab")
    display_frame_tab_ctrl.add(channel_signal_strength_tab,text=" Show Channel Signal Strength ",state="normal") 
    display_frame_tab_ctrl.pack()
    ###################### create of channel signal strength tab ends ###################
    
    
    ###################### create of channel devices tab start ###################
    
    #create a channel devices tab
    channel_devices_tab = ttk.Frame(display_frame_tab_ctrl,style="TNotebook.Tab")
    display_frame_tab_ctrl.add(channel_devices_tab,text=" Show Channel Devices ",state="normal") 
    display_frame_tab_ctrl.pack()
    ###################### create of channel devices tab ends ###################
    
#####################################################################################################
########################### close button code start ##############################################################################

    #close the window upon click on button
    close_window_btn = Button(display_frame,text = 'Close',command=close_window,bg = '#162bdc',font = ('Times New Roman', 20 ,'bold'),width =20,fg='black',highlightcolor = 'white')
    close_window_btn.place(x=500,y=600,relx=0.01,rely=0.01)
    close_window_btn['command'] = lambda :close_window(tk_obj)

########################### close button code ends ##############################################################################
#####################################################################################################


    #making a list of all tabs used
    tab_list = [] #make it global for testing
    tab_list.append(signal_strength_tab)
    tab_list.append(connected_devices_tab)
    tab_list.append(speed_test_tab)
    tab_list.append(channel_signal_strength_tab)
    tab_list.append(channel_devices_tab)
    
    
    #call the handler function upon click of particular tab
    display_frame_tab_ctrl.bind("<<NotebookTabChanged>>",lambda event,arg1=tab_list,arg2=router_ipaddr,arg3 = display_frame_tab_ctrl,arg4 =close_window_btn:event_handler_func(event,arg1,arg2,arg3,arg4))
    
    
    

########################### creating the tabs ends ###################################################################################################
#####################################################################################################

    
    tk_obj.mainloop()
############################ Create Second Window function ends ###################################################
#####################################################################################################


####################### Note: These are call back functions so you can't return #########
####################### Tabs call back functions Start ################################


#NOTE : Here data we get from other modules is in form of list of tuples ########


#checking the router ip with ip used at login time
def check_router_ip_again(router_ipaddr):

    current_router_ipaddr = extract_router_ipaddr.extract_router_ipaddr()
    #if the current router ip address is same as time at login 
    if router_ipaddr == current_router_ipaddr :
        return True
    elif current_router_ipaddr == None:
        display_msg_disconnect()
    else:
        messagebox.showerror("Login Error Window","Connected to different network")
        return False

def display_msg_disconnect():
    DISCONNECT_WINDOW_NAME = "Disconnect Window"
    DISCONNECT_WINDOW_MESSAGE = "Please connect to Internet first "
    messagebox.showinfo(DISCONNECT_WINDOW_NAME,DISCONNECT_WINDOW_MESSAGE)

def Reset_speed_test_data(tab_window_name):

    speed_test_download_clr_data = " ".rjust( (len("DOWNLOAD SPEED: ")+35),' ')  
    speed_test_downlaod_data_label = Label(tab_window_name,text=speed_test_download_clr_data,font=('bold',20),bg='green',fg='white')
    speed_test_downlaod_data_label.place(x=350,y=60)

    speed_test_upload_clr_data = " ".rjust( (len("UPLOAD SPEED: ")+30),' ')
    speed_test_upload_data_label = Label(tab_window_name,text=speed_test_upload_clr_data,font=('bold',20),bg='green',fg='white')
    speed_test_upload_data_label.place(x=350,y=60,rely=0.1)

    speed_test_hotname_clr_data = " ".rjust( (len("HOSTED BY: ")+63),' ')
    speed_test_hostname_data_label = Label(tab_window_name,text=speed_test_hotname_clr_data ,font=('bold',20),bg='green',fg='white')
    speed_test_hostname_data_label.place(x=350,y=60,rely=0.2)

    
def reset_data_treeview(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview):
     
    data = [""] 
    display_data_treeview(tab_window_name,field_names,data,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)


####################### TASK1 #######################################
def show_signal_strength(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview):

    #reset old data value
    #reset_data_treeview(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)

    
    #get the data from task1 module
    signal_strength_data = task1.get_essid_signal_strength_state()
    
    if signal_strength_data == -1:
        messagebox.showinfo("Permissions window","Please provide sudo permissions to access wifi interface")
    

    elif signal_strength_data != None:
        #reset old data value
        reset_data_treeview(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)

        
        #put the data in treeview
        display_data_treeview(tab_window_name,field_names,signal_strength_data,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)

    
    #display a message box when disconnect
    else : 
        #reset old data value
        reset_data_treeview(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)
   
        display_msg_disconnect()

######################## TASK2 #################################################
#show the connected devices only if ssid isn't changed and connected to wifi  
def show_connected_devices(tab_window_name,field_names,router_ipaddr,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview):
    
        
    #get the data from task2
    connected_devices_data = task2.get_device_details()

    #print the data in treeview only if connect to wifi and router_ipaddr matches
    if connected_devices_data != None :
        

            #if ip address isn't changed that means we are using same device
            if  check_router_ip_again(router_ipaddr):

                #reset old data value
                reset_data_treeview(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)
 
                #put the data in treeview
                display_data_treeview(tab_window_name,field_names,connected_devices_data,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)
            
    #display a message box when disconnect
    else: 
        #reset old data value
        reset_data_treeview(tab_window_name,field_names,relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview)

        display_msg_disconnect()


def control_tabs_state(state,display_frame_tab_ctrl,exclude_tab_index):
    if state == False:
        #disable all the tabs except current tab
        for i in range(0,5):
            if i == exclude_tab_index:
                continue
            display_frame_tab_ctrl.tab(i,state="disabled")
        
    elif state == True:
        #enable all tabs except current tab
        for i in range(0,5):
            if i == exclude_tab_index:
                continue
            display_frame_tab_ctrl.tab(i,state="normal")
        

############################# TASK4 ########################################
#here args[0] -> tab_window_name
#args[1] -> display_frame_tab_ctrl
#takes some time to create process
def show_speed_test(*args):

    speed_test_data_list = ""
    #creating a pipe with two file descriptor
    parent_read_fd,child_write_fd = Pipe()

    process_speed_test = Process(target=task4.get_speed_data, args=(child_write_fd,)) 
    process_speed_test.start()
    process_speed_test.join()

    #Here data is in form of list .
    #where first value = hosting name , second value = download speed ,
    #third value = upload speed 
    speed_test_data_list = parent_read_fd.recv()
    
    if speed_test_data_list != None:
        try:
            speed_test_download_data = speed_test_data_list[1]
            speed_test_upload_data = speed_test_data_list[2]
            speed_test_Hosting_data = speed_test_data_list[0]
        except IndexError as err:
            print("Error while extracting speed test data")
            
        else:
            #Clear the old data first before writing new data
            Reset_speed_test_data(args[0])

            #write the download speed data
            speed_test_downlaod_data_label = Label(args[0],text="DOWNLOAD SPEED:"+speed_test_data_list[1],font=('bold',20),bg='green',fg='white')
            speed_test_downlaod_data_label.place(x=350,y=60)

            #write the upload speed data
            speed_test_upload_data_label = Label(args[0],text="UPLOAD SPEED: "+speed_test_data_list[2],font=('bold',20),bg='green',fg='white')
            speed_test_upload_data_label.place(x=350,y=60,rely=0.1)

            #write the hostname  data
            speed_test_hostname_data_label = Label(args[0],text="HOSTED BY: "+speed_test_data_list[0],font=('bold',20),bg='green',fg='white')
            speed_test_hostname_data_label.place(x=350,y=60,rely=0.2)       
    else:
        
        #Clear the old data first before writing new data
        Reset_speed_test_data(args[0])
        display_msg_disconnect()
    

############################### TASK5 #########################
#args[0] -> tab_obj_list[4],   args[1] -> field_names,
#args[2] -> ip_addr,          args[3] -> dimension_2_4GHz,
#args[4] -> dimension_5GHz
def show_scanned_devices(*args):
    
    dimension_2_4GHz = args[3]
    dimension_5GHz = args[4]

    #get the data for first and second frequency from task5 module    
    show_devices_both_freq_data = task5.get_data_both_freq()

    
    #proceed only if connected to wifi 
    if show_devices_both_freq_data != None :
        
        #if ip address isn't changed that means we are using same device
        if  check_router_ip_again(args[2]):    
            

            #extracting the data for 2.4GHz freq
            show_devices_data_2_4GHz = show_devices_both_freq_data[0];

            #extracting the data for 5GHz freq
            show_devices_data_5GHz = show_devices_both_freq_data[1];
    
            #reset old data value for 2.4GHz
            reset_data_treeview(args[0],args[1],dimension_2_4GHz[0],
            dimension_2_4GHz[1],dimension_2_4GHz[2],dimension_2_4GHz[3])

            #reset old data value for 5GHz
            reset_data_treeview(args[0],args[1],dimension_5GHz[0],
            dimension_5GHz[1],dimension_5GHz[2],dimension_5GHz[3])


            #put the data in treeview for 2.4GHz
            display_data_treeview(args[0],args[1],show_devices_data_2_4GHz,
            dimension_2_4GHz[0],dimension_2_4GHz[1],dimension_2_4GHz[2],
            dimension_2_4GHz[3])

            #put the data in treeview for 5GHz
            display_data_treeview(args[0],args[1],show_devices_data_5GHz,
            dimension_5GHz[0],dimension_5GHz[1],dimension_5GHz[2],
            dimension_5GHz[3])
    
    else:
        #reset old data value for 2.4GHz
        reset_data_treeview(args[0],args[1],dimension_2_4GHz[0],
        dimension_2_4GHz[1],dimension_2_4GHz[2],dimension_2_4GHz[3])

        #reset old data value for 5GHz
        reset_data_treeview(args[0],args[1],dimension_5GHz[0],
        dimension_5GHz[1],dimension_5GHz[2],dimension_5GHz[3])

        display_msg_disconnect()



############################## TASK 3 ################################
#args[0] -> tab_obj_list[3],   args[1] -> field_names,
#args[2] -> ip_addr,          args[3] -> dimension_2_4GHz,
#args[4] -> dimension_5GHz
def show_channel_signal_strength(*args):
    
    dimension_2_4GHz = args[3]
    dimension_5GHz = args[4]
    
    #get the data for first frequency from task5 module    
    signal_strength_both_freq_data = task3.get_both_freq_data()
        
    if signal_strength_both_freq_data == -1:
        messagebox.showinfo("Permissions window","Please provide sudo permissions to access wifi interface")
    
    #proceed only if connected to wifi 
    if signal_strength_both_freq_data != None:
    
        #if ip address isn't changed that means we are using same device
        if  check_router_ip_again(args[2]):    
            
            #extracting the data for 2.4GHz freq
            signal_strength_data_2_4GHz = signal_strength_both_freq_data[0];

            #extracting the data for 5GHz freq
            signal_strength_data_5GHz = signal_strength_both_freq_data[1];
    
            #reset old data value for 2.4GHz
            reset_data_treeview(args[0],args[1],dimension_2_4GHz[0],
            dimension_2_4GHz[1],dimension_2_4GHz[2],dimension_2_4GHz[3])

            #reset old data value for 5GHz
            reset_data_treeview(args[0],args[1],dimension_5GHz[0],
            dimension_5GHz[1],dimension_5GHz[2],dimension_5GHz[3])

            #put the data in treeview for 2.4GHz
            display_data_treeview(args[0],args[1],signal_strength_data_2_4GHz,
            dimension_2_4GHz[0],dimension_2_4GHz[1],dimension_2_4GHz[2],
            dimension_2_4GHz[3])

            #put the data in treeview for 5GHz
            display_data_treeview(args[0],args[1],signal_strength_data_5GHz,
            dimension_5GHz[0],dimension_5GHz[1],dimension_5GHz[2],
            dimension_5GHz[3])
    
    else:
        #reset old data value for 2.4GHz
        reset_data_treeview(args[0],args[1],dimension_2_4GHz[0],
        dimension_2_4GHz[1],dimension_2_4GHz[2],dimension_2_4GHz[3])

        #reset old data value for 5GHz
        reset_data_treeview(args[0],args[1],dimension_5GHz[0],
        dimension_5GHz[1],dimension_5GHz[2],dimension_5GHz[3])

        display_msg_disconnect()



#close window forcefully to exit the program
def close_window(tkobj_login_window):
    
    messagebox.showinfo("Exit window","Application Exited")
    #close the current window
    tkobj_login_window.destroy()
    sys.exit()#use to abrupt exit


########################################################################################


#here data must be of form of list of tuples
def display_data_treeview(tab_window_name,field_names,data,
relheight_treeview,relwidth_treeview,relx_treeview,rely_treeview):

    

    #setting the height ,width and position of treeview table
    REL_HEIGHT_COLUMN_TREEVIEW = relheight_treeview
    REL_WIDTH_COLUMN_TREEVIEW = relwidth_treeview
    REL_X_TREEVIEW = relx_treeview
    REL_Y_TREEVIEW = rely_treeview

    MAX_COL_WIDTH = 90    
    
    #setting the Treeview window size and place it
    Treeview_window = tab_window_name
    Treeview_obj = ttk.Treeview(Treeview_window,selectmode='browse')
    Treeview_obj.place(relx=REL_X_TREEVIEW ,rely=REL_Y_TREEVIEW ,relwidth=REL_WIDTH_COLUMN_TREEVIEW,relheight=REL_HEIGHT_COLUMN_TREEVIEW)
    
    # Constructing vertical scrollbar
    verscrlbar = ttk.Scrollbar(Treeview_window,  orient ="vertical",  command = Treeview_obj.yview) 
    verscrlbar.place(relx=REL_X_TREEVIEW-0.01,rely= REL_Y_TREEVIEW ,relheight=REL_HEIGHT_COLUMN_TREEVIEW) 

    # Configuring treeview for vertical scrollbar
    Treeview_obj.configure(xscrollcommand = verscrlbar.set) 

    
    # Defining number of columns corresponding to fields as list
    #here started from 0
    columns_list = []
    count = 0
    for i in field_names:
        columns_list.append(count)
        count += 1
        

    #make a column tuple store the no of fiels as elements
    column_tuple = tuple(columns_list)   
    
    #specify the no of columns 
    Treeview_obj["columns"] = column_tuple

    # Defining heading 
    Treeview_obj['show'] = 'headings'

    
    column_No = 0
    
    #setting the width of specific column 
    #anchor specify the alignment to data placed in each column
    #c means center
    for i in column_tuple:
        Treeview_obj.column(i, width = MAX_COL_WIDTH,anchor ='c')
        
    
    column_No = 0
    
    
    #set and display the heading field
    
    for i in field_names:   
        #set and display the heading field
        Treeview_obj.heading(column_No,text=i)
        column_No +=1 
        
    #put the data in each row
    column_No=0
    index=0
    for i in data:   
        #Inserting the data
        Treeview_obj.insert("", 'end',  text = "L1",values = data[index])
        index += 1  
        column_No += 1
    
""" ############################## Methods Ends ###################### """

