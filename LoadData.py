# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 16:41:02 2020

@author: nidhinanisham
"""

import csv
import MySQLdb
from datetime import datetime

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='password@123',
    db='Contacts')
cursor = mydb.cursor()

with open('Contacts.csv') as csvfile:
    next(csvfile)
    csv_data = csv.reader(csvfile, delimiter=',')
    for row in csv_data:
        
        c_id = row[0]
        first_name = row [1]
        middle_name = row[2]
        last_name = row[3]
        home_phone = row[4]      
        cell_phone = row[5]          
        home_address = row[6]
        home_city = row[7]
        home_state = row[8]
        home_zip = row[9]        
        work_phone = row[10]      
        work_address = row[11]
        work_city = row[12]
        work_state = row[13]
        work_zip = row[14]
        birth_date = row[15]
        
        home_phone = home_phone.replace('-','')
        cell_phone = cell_phone.replace('-','')
        work_phone = work_phone.replace('-','')
        
        if(birth_date == ''):
            birth_date = None
        else:
            birth_date = datetime.strptime(birth_date, '%m/%d/%Y')
            birth_date = birth_date.strftime('%Y-%m-%d')
        
        cursor.execute('ALTER TABLE CONTACT AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE ADDRESS AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE PHONE AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE DATE AUTO_INCREMENT=0')
        
        cursor.execute('INSERT INTO CONTACT(Fname,Mname,Lname) VALUES (%s,%s,%s)'
                       ,[first_name,middle_name,last_name])
        
        
        if(work_address or work_city or work_state or work_zip):
            cursor.execute('INSERT INTO ADDRESS(Contact_id,Address_type,Address,City,State,Zip) VALUES(%s,%s,%s,%s,%s,%s)'
                       ,[c_id,"work",work_address,work_city,work_state,work_zip])
        
        if(home_address or home_city or home_state or home_zip):
            cursor.execute('INSERT INTO ADDRESS(Contact_id,Address_type,Address,City,State,Zip) VALUES(%s,%s,%s,%s,%s,%s)'
                       ,[c_id,"home",home_address,home_city,home_state,home_zip])
        
        if(home_phone):
            cursor.execute('INSERT INTO PHONE(Contact_id,Phone_type,Area_code,Number) VALUES(%s,%s,%s,%s)'
                       ,[c_id,"home",home_phone[:3],home_phone[3:]])
        
        if(cell_phone):
            cursor.execute('INSERT INTO PHONE(Contact_id,Phone_type,Area_code,Number) VALUES(%s,%s,%s,%s)'
                       ,[c_id,"cell",cell_phone[:3],cell_phone[3:]])
        
        if(work_phone):
            cursor.execute('INSERT INTO PHONE(Contact_id,Phone_type,Area_code,Number) VALUES(%s,%s,%s,%s)'
                       ,[c_id,"work",work_phone[:3],work_phone[3:]])
            
        if(birth_date):
            cursor.execute('INSERT INTO DATE(Contact_id,Date_type,Date) VALUES(%s,%s,%s)'
                       ,[c_id,"birthday",birth_date])
        
        
        
    mydb.commit()
    cursor.close()
