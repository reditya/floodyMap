#!/usr/bin/python

# scrapper

from bs4 import BeautifulSoup
import requests
import re
import csv

#---------------------------------------------------------
# Simple csv writer
# @param : data ... data to be written
#        : path ... path to write
# @return : void
#---------------------------------------------------------
def csv_writer(data, path):
    
  print "TODO"
  
#---------------------------------------------------------
# Function to get the Name of element and Address of the element 
#  @param  : element .. list of element got from web
#          : is_type ... TEL or Address
#---------------------------------------------------------
def get_Address(element, is_type):
    
    
    is_name = "Jl"
    is_tel = "Telp"
    name = ""
    i = False
    
    if is_type == 0:
        for p in element:
            if p == is_name:
                break
            name += p+ " "
    else:
        for p in element:
            if p == is_name : 
                i=True
            elif p == is_tel : 
                break
            elif i: 
                name += p + " "
            else: pass
                
    return name
 
#---------------------------------------------------------
# Function to get the element based on URL 
#  @param  : url ....    URL of the address
#  @return 
#---------------------------------------------------------

def print_URL(url):
    
    print "Fetching Content"
    
    try:
        r  = requests.get("http://" +url)
    except:
        exit(1)
        
    i = 0
    is_elmtname = 0
    is_addrname = 1
    
    #last data to be fetched to csvdata_vin
    data_vin = []
            
    data = r.text
    friedrice = BeautifulSoup(data)
    for node in friedrice.findAll('li'):
        i+=1
        element = ''.join(node.findAll(text=True))
        element = element.encode("ascii")        
        #get first name in the line
        firstname = element.split('\n', 1)[0]
        # if \r returned, replace with empty
        if len(firstname) == 2: firstname = ""
        
        #get last chunk of name
        second = element.split('\n', 1)[1]
        third = re.findall(r'\w+', second)
        
        #postprocess last chunk of name
        secondname = get_Address(third,is_elmtname)
      
        #get name, to be used as element entity in map    
        real_name = firstname
        if secondname:
            real_name += secondname
       
        real_name = ''.join(real_name.splitlines())
        
        address = get_Address(third, is_addrname)
        address = address+ "Surabaya"
        #print "address is", address
        data_vin.append(real_name)
        data_vin.append(",")
        data_vin.append(address)
        data_vin.append("\n")
        
    return data_vin     
        


if __name__ == "__main__":
    path = "/opt/gitrepo/repo1/floodyMap/result.csv"
    data = print_URL("www.surabaya.go.id/eng/tourism.php?page=restoran")
    
    csv_writer(data, path)