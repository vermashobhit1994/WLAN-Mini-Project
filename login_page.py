""" ################################## MODULE DESCRIPTION #########################"""
#Module Description : Provides the functionalities related to LogIn Page  
#Name of Person : Shobhit Verma
""" ################################################################################"""



#Make a login page
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import sys,os,subprocess

#imported from other modules
import display_window_modified
import check_connection_state
import extract_router_ipaddr


PASSWORD_DIR = '/etc/NetworkManager/system-connections' 


class Login_Window():

    #initialize the login window
    def __init__(self):

        tkobj_login_window = Tk()
        
        #set the screen to full size
        full_width  = tkobj_login_window.winfo_screenwidth()
        full_height = tkobj_login_window.winfo_screenheight()


        #window_size = "1320x1024"
        window_title = "Login Window"
        Image_name = 'background.jpg'
        background_image_path = os.path.abspath(Image_name)
        
        #adding the title 
        tkobj_login_window.title(window_title)

        #put the background image
        image_details = Image.open(background_image_path)
        #image1 is image object
        image1 = ImageTk.PhotoImage(image_details)#PhotoImage is class Name 
        image_width = image1.width()
        image_height = image1.height()

        tkobj_login_window.geometry('%dx%d+0+0' % (full_width,full_height))

        #label to place the background image
        label1 = Label(tkobj_login_window, image=image1,height=full_height,width=full_width)
        label1.pack()


        #Set the font family
        FONT_FAMILY = 'STIXIntegralsUp'
        #set the top heading
        title = Label(tkobj_login_window,text='LOGIN PAGE',borderwidth=2,relief='groove',font=(FONT_FAMILY,30,'bold'),fg='White',bg='#1a7eee')
        title.place(x=0,y=0,relwidth=1)

        #create a frame
        Login_frame = Frame(tkobj_login_window,bg = '#80b9f3')
        Login_frame.place(relx=0.18,rely=0.3)
        
        
        username_Label = Label(Login_frame,text = 'Username',font = ('bold',14),bg='#145496',fg='white')
        username_Label.grid(row=1,column=0,padx=20,pady=10)
        
        password_Label = Label(Login_frame,text = 'Password',font = ('bold',14),bg='#145496',fg='white')
        password_Label.grid(row=2,column=0,padx=20,pady=10)
        
    ################ NOTE : Entry() has show () to show what when we type ####################
    ###############  NOTE : Used lambda function to return the address of callback function####
        username_Var_obj = StringVar()#for storing the Var object in username text field 
        username_Entry = Entry(Login_frame,bd=2,font=20,textvariable = username_Var_obj)
        username_Entry.place(relx=0.19,rely=0.05,width=250,height=27)
        username_Entry.focus()#to make a blinking cursor in username Entry box

        password_Var_obj = StringVar()#for storing the Var object in Password text field 
        password_Entry = Entry(Login_frame,bd=2,font=(20),show = '*',textvariable=password_Var_obj).place(relx=0.19,rely=0.30,width=250,height=27)
        
        #create a login button
        login_button = Button(Login_frame,text = 'Login',command=login_user,fg='White',bg='#1a7eee',width =20,highlightcolor= 'Light yellow')
        login_button.grid(row=4,column=1,padx=30,pady=30)    
        login_button['command'] = lambda arg1=username_Var_obj,arg2=password_Var_obj,arg3=tkobj_login_window:login_user(arg1,arg2,arg3)
        
        
        #create a reset button    
        reset_btn = Button(Login_frame,text = 'Reset',command=reset_login_data,fg='White',bg='#1a7eee',width =20,highlightcolor= 'yellow')
        reset_btn.grid(row=4,column=2,padx=30,pady=30)
        reset_btn['command'] = lambda :reset_login_data(username_Var_obj,password_Var_obj)
        
        #create a close button    
        close_btn = Button(Login_frame,text = 'Close',command=close_window,fg='White',bg='#1a7eee',width =20,highlightcolor= 'Light Yellow')
        close_btn.grid(row=4,column=3,padx=20,pady=20)
        close_btn['command'] = lambda :close_window(tkobj_login_window)
        tkobj_login_window.mainloop()



""" ###########################  LOGIN WINDOW FUNCTIONS START ############## """

#function to access wifi password
#Note : It requires root permissions
def access_password(ssid_name):

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
        
    #adding the ssid  to password directory
    wifi_password_file = os.path.join(PASSWORD_DIR,str(ssid_name))
    
    #checking the output of password file
    cmd_out = subprocess.check_output(["sudo","cat",wifi_password_file])
    cmd_out = cmd_out.decode('ascii')
    
    #extracting password
    start = cmd_out.find("psk=")+4 #start index is next after "psk="
    end = cmd_out.find("\n",start)#end index is '\n'
    password = cmd_out[start:end] 
 
    #change the directory to current directory
    os.chdir(original_path)
    
    return password

#function to write the ssid and password to file  
def write_ssid_psk(ssid_name,psk):
    ssid_psk_filename = "ssid_psk_data.txt"
    with open(ssid_psk_filename,mode='a+') as fd:
        fd.write("userid : "+ssid_name+'\t')
        #fd.write("psk : "+psk+'\n')

#function to access the name and password of wifi router
def access_ssid_and_password():
    
    #convert the output the string from binary string
    ssid_name = subprocess.check_output(["iwgetid","-r"]).decode('ascii')
    ssid_name = ssid_name[:-1]#to remove the'\n'
    
    psk = access_password(ssid_name)
    #write_ssid_psk(ssid_name,psk)
    
    return tuple((ssid_name,psk))

#function to check the username and password is valid or not 
#current_data[0] -> username , current_data[1] -> password   
def check_username_password(current_data):
    
    if check_connection_state.check_connection_state():
        original_data  = access_ssid_and_password()
        
        if original_data[0] == current_data[0]and original_data[1] == current_data[1]:
            return True
        elif (current_data[0]=="" and current_data[1] =="") or (current_data[0] =="" or current_data    [1]==""):
            messagebox.showwarning("WARNING!!!!!","Fields can't be empty     ")
            return False
        
        messagebox.showerror("ERROR   ","Wrong details       ")
        return False

    else:
        check_connection_state.display_msg_disconnect()

#call when click on reset button to reset the text fields
def reset_login_data(username_Var_obj,password_Var_obj):
    #clear the fields only if they aren't clear
    if username_Var_obj.get() != "" and username_Var_obj.get() != "":
        username_Var_obj.set("")
        password_Var_obj.set("")
        messagebox.showinfo("Reset window","Fields Reset Successfully   ")


def login_user(username_Var_obj,password_Var_obj,tkobj_login_window):
    #username and password gets stored from string entered in text box
    username = username_Var_obj.get()
    password = password_Var_obj.get()
    
    #check the username and password
    if check_username_password(list([username,password])):
        messagebox.showinfo("Permission window","Permissions is granted")
        close_current_window(tkobj_login_window)#close the current window
        
        #extract the current router ip address
        router_ip = extract_router_ipaddr.extract_router_ipaddr()
        
        if router_ip != None:
            #send the router ip to display window function 
            display_window_modified.create_second_window(router_ip)
        else:
            messagebox.showinfo("Connection Error Window","Please connect to internet to access ip address")
        

def close_window(tkobj_login_window):
    messagebox.showinfo("Exit window","Application Exited")
    #close the current window
    tkobj_login_window.destroy()
    sys.exit()

def close_current_window(tkobj_login_window):
    messagebox.showinfo("Exit Current window","Current Application Exited")
    
    #close the current window
    tkobj_login_window.destroy()

    
    
""" ###########################  LOGIN WINDOW FUNCTIONS ENDS ############## """
    
    

