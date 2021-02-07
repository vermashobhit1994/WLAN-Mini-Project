""" ################################################################################

#This module is used internally by many modules to convert the list of list into 
#list of tuples where each tuple corresponding to row data displayed on display screen.
################################################################################"""



def func_convert_list_of_tuple(*mylist):

    list_of_tuple = list(mylist)#convert to list from tuple
    
    newlist = []#final list 
    
    no_of_columns = len(list_of_tuple)
    
    

    """ ################### Make two list into tuples #######################"""
    #combine only two list into list of tuples
    k=0#k is index to lists 
     
    tmplist_first = list_of_tuple[k]
    tmplist_second = list_of_tuple[k+1]
    
    #combine the two list of variable length into list of tuples
    for i in range (  max ( len(tmplist_first) , len(tmplist_second)  ) ):
        try :
            tuple_two_list = (tmplist_first[i], tmplist_second[i])
        except IndexError :
            if len(tmplist_first) > len(tmplist_second) :
                tmplist_second.append('')
                tuple_two_list = (tmplist_first[i], tmplist_second[i])
            elif len(tmplist_second) > len(tmplist_first):
                tmplist_first.append('')
                tuple_two_list = (tmplist_first[i], tmplist_second[i])
        else:
            tuple_two_list = (tmplist_first[i], tmplist_second[i])
        finally:
                newlist.append(tuple_two_list) 

    
    #k is index to lists  
    k += 2#increment k to show that first two list are complete
    
    
    """###################### Add the list from third to final list ##########"""
    if k < len(list_of_tuple):#to append one more list if list is still remaining 
        tmp_list = list_of_tuple[k]
        
        for i in range (  max ( len(tmp_list) , len(newlist)  ) ):    
            try :
                
                current_ele_list_of_tuple = tmp_list[i]
                #change the tuple into list to append new item
                current_ele_newlist = list(newlist[i])
                
                #print("try condi current_ele_newlist  ",current_ele_newlist)
            except IndexError:
                #if length of newlist is more than current list in list of lists
                if len(newlist) > len(tmp_list):
                    #create a tuple
                    current_ele_newlist = list(newlist[i])
                    current_ele_newlist.append('')
                    current_ele_newlist = tuple(current_ele_newlist)
                    #replace the current element
                    newlist[i] = current_ele_newlist    
                
                elif len(tmp_list) > len(newlist):
                    #create a tuple
                    current_ele_newlist = []
                    l = 0
                    #putting the '' where element isn't found newlist
                    while l < len(list_of_tuple)-1:
                        current_ele_newlist.append('')
                        l += 1
                    #add the last element of tmp_list 
                    current_ele_newlist.append(tmp_list[i])
                    current_ele_newlist = tuple(current_ele_newlist)
                    #add the new element to newlist at end
                    newlist.append(current_ele_newlist)    
                
                    
            #if length of list  are equal
            else:
                #make a tuple with adding the new element 
                #replace the current element by new tuple 
                #create a tuple
                current_ele_newlist = list(newlist[i])
                current_ele_newlist.append(tmp_list[i])
                current_ele_newlist = tuple(current_ele_newlist)
                #replace the current element of newlist
                newlist[i] = current_ele_newlist
            
        #k += 1
    return newlist
    


    
    

    

    
          

