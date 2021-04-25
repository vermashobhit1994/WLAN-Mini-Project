""" ################################## MODULE DESCRIPTION #########################"""
#Module Description : Provides the functionalities related to Login Page  
#Name of Person : Shobhit Verma
""" ################################################################################"""



#Module for graphics to make a login page
from tkinter import Tk,messagebox,Label,Frame,StringVar,Entry,Button,messagebox

#Module to put image at background
from PIL import ImageTk,Image


import sys,os,subprocess

########## user defined modules #############
from display_window import Display_Window
import check_connection_state
import extract_router_ipaddr
from Error_Flags import * 
#############################################





#********** Global Variable *******************# 
PASSWORD_DIR = '/etc/NetworkManager/system-connections'

class Login_Window():

    #initialize the login window with size, background image, label, Entybox
    def __init__(self,tkobj_login_window):
        
    
        #assign the value to instance variable from local variable
        self.tkobj = tkobj_login_window
        
        """#### set the screen height and width to full screen size for background image and login window #####""" 
        #window_size = "1320x1024"
        full_width  = self.tkobj.winfo_screenwidth()
        full_height = self.tkobj.winfo_screenheight()
        
       
        
        ############### put the background image ############################################
        Image_name = 'background.jpg'
        background_image_path = os.path.abspath(Image_name)
        image_details = Image.open(background_image_path)
        
        #customize the image size to full height and width
        image_details = image_details.resize((full_width,full_height), Image.ANTIALIAS)
        
        #image1 is PhotoImage object
        image1 = ImageTk.PhotoImage(image_details)#PhotoImage is class Name 
        

        #label to place the background image
        label_background_image = Label(self.tkobj, image=image1,height=full_height,width=full_width)
        label_background_image.pack()
         
        #######################################################################################

        ############# Configure the name and size of window ###############
        
        login_window_title = "Login Window"
        self.tkobj.geometry('%dx%d+0+0' % (full_width,full_height))
        self.tkobj.title (login_window_title)
        
        ##################################################################
        
        

        """###################################################################################################""" 
        
        
        ###################### Create a label of Name Login Page ##########################################
        #Set the font family
        FONT_FAMILY = 'STIXIntegralsUp'
        #set the top heading
        login_window_title = Label(self.tkobj,text='LOGIN PAGE',borderwidth=2,relief='groove',font=(FONT_FAMILY,40,'bold'),fg='White',bg='#1a7eee')
        login_window_title.place(x=0,y=0,relwidth=1)
	####################################################################################################
	
        
        """############ create a login frame #############################################################################"""
        Login_Frame = Frame(self.tkobj,bg = '#80b9f3',width=1400,height=300)
        #Login_Frame.place(relx=0.2,rely=0.3)
        Login_Frame.place(x=400,y=300)
        
        
        #create a Login label 
        username_Label = Label(Login_Frame,bd=5,text = 'Username',font = ('',30,'bold',),bg='#145496',fg='white',compound = 'left' )
        username_Label.grid(row=1,column=0,padx=20,pady=10)
        
        
        ######################## Creating Entry and label for Login and Password ##############################################
        
        #instance variable for storing username and Password obj of StringVar class
        self.username_Var_obj = StringVar()#for storing the Var object in username text field  
        self.password_Var_obj = StringVar()#for storing the Var object in Password text field 
        
        
        ################ NOTE : Entry() has show () to show what when we type ####################
        #create a entry box for text to be input by user
        
        username_Entry = Entry(Login_Frame,bd=5,font=("",20),textvariable = self.username_Var_obj,relief='groove',width=30)
        #username_Entry.place(relx=1,rely=0.1,width=500,height=27)#automatically adjust the Entry box when resize the window
        username_Entry.grid(row=1,column=1,padx=20,pady=20)
        username_Entry.focus()#to make a blinking cursor in username Entry box
        
        
        #create a password label
        password_Label = Label(Login_Frame,bd=5,text = 'Password',font = ('',30,'bold'),bg='#145496',fg='white')
        password_Label.grid(row=2,column=0,padx=20,pady=10)
        
        #create a password entry box
        password_Entry = Entry(Login_Frame,bd=5,font=("",20),show = '*',textvariable=self.password_Var_obj,width=30)
        #password_Entry.place(relx=0.5,rely=0.5,width=250,height=27)#automatically adjust the Entry box when resize the window
        password_Entry.grid(row=2,column=1,padx=20,pady=20)
 
        ##########################################################################################################################
    
    
    
       ########################### Creating the login, reset, close buttons ########################################################
       ###############  NOTE : Used lambda function to return the address of callback function####
    
    
        #create a login button
        login_button = Button(Login_Frame,bd=5,text = 'Login',command=self.login_user,fg='White',bg='#1a7eee',width =25,highlightcolor= 'Light yellow')
        #login_button.grid(row=4,column=1,padx=30,pady=30)  
        login_button.place(x=300,y=193)
         
        login_button['command'] = lambda :self.login_user()
        
        #create a reset button    
        reset_btn = Button(Login_Frame,bd=5,text = 'Reset',command=self.reset_login_data,fg='White',bg='#1a7eee',width =25,highlightcolor= 'yellow')
        #reset_btn.grid(row=4,column=2,padx=30,pady=30)
        reset_btn.place(x=580,y=193)
        reset_btn['command'] = lambda :self.reset_login_data()
        
        #create a close button    
        close_btn = Button(Login_Frame,bd=5,text = 'Close',command=self.close_window,fg='White',bg='#1a7eee',width =25,highlightcolor= 'Light Yellow')
        close_btn.grid(row=4,column=5,padx=10,pady=20)
        #close_btn.place(x=100,y=200)
        close_btn['command'] = lambda :self.close_window()
        
        ###########################################################################################################################
        
        """ ############################# Creation of Login Frame ends #############################################################"""
        
        #start the login window
        self.tkobj.mainloop()
        
        
        ###################### ******************** Login Window Initialization Ends Here **********************###################
        
         

    
    
    """ ###########################  LOGIN WINDOW INSTANCE FUNCTIONS START ############## """
    
    
    ########## function to access wifi password #################################################
    #Note : It requires root permissions
    def access_password(self,ssid_name):

        original_path = os.getcwd()#get the original file path
        os.chdir(PASSWORD_DIR)#change the directory to where password file
    
    
        ################# Adding the '\' if space in ssid name #######################3
        #This is done to ensure that whenever we specify path space replaced by '\ '
        #adding '\' if ssid name separated by space
        #here each space is replace by '\ '
        if ssid_name.find(' ') != -1:        
            space_index = ssid_name.index(' ')
        
            #replace all the space by '\ '
            ssid_name = ssid_name.replace(ssid_name[space_index:space_index+1],'\\ ')
        
        ####################################################################################
        
        
        
        ####################### extracting the password from ssid file ***********************     
    
        #adding the ssid  to password directory
        wifi_password_file = os.path.join(PASSWORD_DIR,str(ssid_name))
        #password file for ubuntu 20.04LTS
        wifi_password_file_new = os.path.join(PASSWORD_DIR,str(ssid_name)+".nmconnection")
    
        cmd_out = None
        password = ""
   
        #checking the output of password file
        try:
            #to flush the stderr for first time 
            fflush(stderr)
            args = ["sudo","cat",wifi_password_file]
            #if error in executing "sudo cat /etc/NetworkManager/system-connections/SSID then redirect it to stderr for avoiding the error message
            cmd_out = subprocess.check_output(args)
            
            
        
     
        #extract the password for ubuntu 20.04 with ssid.nmconnection file in PASSWORD_DIR path.
        except Exception as err:
        
            cmd_out = subprocess.check_output(["sudo","cat",wifi_password_file_new])
            cmd_out = cmd_out.decode('ascii',errors='backslashreplace')
        
    
            #extracting password
            start = cmd_out.find("psk=")+4 #start index is next after "psk="
            end = cmd_out.find("\n",start)#end index is '\n'
            password = cmd_out[start:end] 
            
        
        
        #extract the password for ubuntu version < 20.04 with ssid file in PASSWORD_DIR path. 
        else:
            cmd_out = str(cmd_out.communicate()[0])
    
            #extracting password
            start = cmd_out.find("psk=")+4 #start index is next after "psk="
            end = cmd_out.find("\n",start)#end index is '\n'
            password = cmd_out[start:end] 

        ###########################################################*****************************#
        
        finally:
            #change the directory to current directory
            os.chdir(original_path)
    
        return password

    ################### Function to access WiFi password ends here ###########################################    
    
    
    
    
    ########## function to write the ssid and password to file Start ################################################  
    def write_ssid_psk(self,ssid_name,psk):
        ssid_psk_filename = "ssid_psk_data.txt"
        with open(ssid_psk_filename,mode='a+') as fd:
            fd.write("userid : "+ssid_name+'\t')
            fd.write("psk : "+psk+'\n')

    ############### Function to Write SSID and Password to file ends here #######################################
    
    
    
    ############## function to access the name and password of wifi Access Point Start #################################
    def access_ssid_and_password(self):
    
        #convert the output the string from binary string
        ssid_name = subprocess.check_output(["iwgetid","-r"]).decode('ascii')
        ssid_name = ssid_name[:-1]#to remove the'\n'
    
        psk = self.access_password(ssid_name)
        #self.write_ssid_psk(ssid_name,psk)
        
        return tuple((ssid_name,psk))

    ################# Function to access name and password of WiFi Access Point Ends Here #################################

    
    ############# function to check the username and password is valid or not Start Here ##################################### 
    #current_data[0] -> username , current_data[1] -> password   
    def check_username_password(self,current_data):
    
        #check if connected to WiFi or not 
        if check_connection_state.check_connection_state():
            original_data  = self.access_ssid_and_password()
        
            if original_data[0] == current_data[0]and original_data[1] == current_data[1]:
                return True
            
            elif (current_data[0]=="" and current_data[1] =="") or (current_data[0] =="" or current_data    [1]==""):
                messagebox.showwarning("WARNING!!!!!","Fields can't be empty     ")
                return False
        
            messagebox.showerror("ERROR   ","Wrong Username or Password      ")
            return False
        
        else:
            check_connection_state.display_msg_disconnect()#if not connected display the connection error message

    #########function to check the username and password is valid or not Ends Here #####################################################
	

    ############### Function to check the username and Passoword start here ############################################################# 	

    def login_user(self):
        #username and password gets stored from string entered in text box
        username = self.username_Var_obj.get()
        password = self.password_Var_obj.get()
    
        #check the username and password by passing as list
        if self.check_username_password(list([username,password])):
        
        
            #extract the current router ip address
            router_ip = extract_router_ipaddr.extract_router_ipaddr()
        
            if router_ip == CONNECTION_ERROR:
                messagebox.showwarning("Connection Error ","Please connect to internet to access router ip address")
            elif router_ip == PERMISSION_ERROR:
                messagebox.showwarning("Permissions Access Error","Restart the file again with sudo permissions for accessing WiFi Interface")
            elif router_ip == NMCLI_CMD_ERROR:
                messagebox.showwarning("Commmand Error","Error in executing command \"nmcli devices show wifi_interface\"")
            else:
                messagebox.showinfo("Permission Access window","Permissions is granted")
                self.close_current_window()#close the current window
 
                #create a tkinter object for Display_Window page
                tkobj_display_window = Tk()
                
 
                #create an object of Display_Window Class
                disp_window_obj = Display_Window(router_ip,tkobj_display_window)
                
                

    ############### Function to check the username and Passoword Ends here ############################################################# 	


    ############## Function to Reset all fields Start Here ################################################################################

    #call when click on reset button to reset the text fields
    def reset_login_data(self):
    
       #if both fields are empty then print message
       if self.username_Var_obj.get() == "" and self.password_Var_obj.get() == "":
            messagebox.showinfo("Reset Window","Nothing to Reset")
       #clear the fields only if they aren't filled
       elif (self.username_Var_obj.get() != "" or self.password_Var_obj.get() != "") :
            self.username_Var_obj.set("")
            self.password_Var_obj.set("")
            messagebox.showinfo("Reset window","Fields Reset Successfully   ")
        
    ############## Function to Reset all fields Ends Here ################################################################################


    ############## Function to Close all windows Start Here ################################################################################

    def close_window(self):
        messagebox.showinfo("Exit window","Application Exited")
        #close the current window
        self.tkobj.destroy()
        sys.exit()#close the whole program
        
    ############## Function to Close All Windows Ends Here ################################################################################



    ############## Function to Close Current Window Start Here ################################################################################


    def close_current_window(self):
        messagebox.showinfo(" Exit Current window "," Login Window Exited Successfully   ")
    
        #close the current window
        self.tkobj.destroy()

    ############## Function to Close Current Window Ends Here ################################################################################

    
    """ ###########################  LOGIN WINDOW INSTANCE FUNCTIONS ENDS ############## """
    
    

