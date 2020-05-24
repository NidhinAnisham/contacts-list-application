# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:40:19 2020

@author: nidhinanisham
"""

from flask import Flask,render_template,request
import MySQLdb

app = Flask(__name__)
app.secret_key = 'secret_key'

mydb = MySQLdb.connect(host='localhost',user='root',passwd='password@123',db='Contacts')

def get_ids(terms):
    cursor = mydb.cursor()
    c_id = []
    for i in terms:
        cursor.execute('SELECT Contact_id FROM CONTACT WHERE Fname=%s or Mname=%s or Lname=%s',[i,i,i])
        result = cursor.fetchall()
        for j in result:
            if j[0] not in c_id:
                c_id.append(j[0])
        
        cursor.execute('SELECT Contact_id FROM ADDRESS WHERE Address_type=%s or Address=%s or City=%s or State=%s or Zip=%s',[i,i,i,i,i])
        result = cursor.fetchall()
        for j in result:
            if j[0] not in c_id:
                c_id.append(j[0])
        
        cursor.execute('SELECT Contact_id FROM PHONE WHERE Phone_type=%s or Area_code=%s or Number=%s',[i,i,i])
        result = cursor.fetchall()
        for j in result:
            if j[0] not in c_id:
                c_id.append(j[0])
    cursor.close()        
    return c_id

def fetch_details(terms):
    cursor = mydb.cursor()
    
    cursor.execute('SELECT Fname,Mname,Lname FROM CONTACT WHERE Contact_id=%s',[terms])
    names = list(cursor.fetchall()[0])
    
    cursor.execute('SELECT Phone_type,Area_code,Number,Phone_id FROM PHONE WHERE Contact_id=%s',[terms])
    phones = cursor.fetchall()
    if(len(phones)>0):
        phones = list(phones)
        for i in range(len(phones)):
            phones[i] = list(map(str,phones[i]))             
    else:
        phones = [["","","",-1]]

    cursor.execute('SELECT Address_type,Address,City,State,Zip,Address_id FROM ADDRESS WHERE Contact_id=%s',[terms])
    address = cursor.fetchall()
    if(len(address)>0):
        address = list(address)
    else:
        address = [["","","","","",-1]]
    cursor.execute('SELECT Date_type,Date,Date_id FROM DATE WHERE Contact_id=%s',[terms])
    dates = cursor.fetchall()
    if(len(dates)>0):
        dates = list(dates)
    else:
        dates = [["","",-1]]
    
    cursor.close()   
    return names,phones,address,dates
    
@app.route('/')
def index():
   return render_template('SearchPage.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    cursor = mydb.cursor()
    if request.method == 'POST':
        terms = request.form['search'].split(",")   
        c_id = get_ids(terms)
        result = []
        for i in c_id:
            cursor.execute('SELECT Fname,Mname,Lname FROM CONTACT WHERE Contact_id=%s',[i])
            temp = list(cursor.fetchall()[0])
            temp.insert(0,i)
            result.append(temp)
        cursor.close()
        if(len(result) == 0):
            return render_template('NoResults.html')
        return render_template('SearchResults.html',results = result)
   
@app.route('/display', methods = ['GET', 'POST'])
def display():
    if request.method == 'POST':
        terms = request.form['cid']
        names,phones,address,dates = fetch_details(terms)
        return render_template('Table.html',names=names,phones=phones,addresses=address,dates=dates,cid=terms)        
    
@app.route('/new_contact', methods = ['GET', 'POST'])
def new_contact():
    return render_template('CreateContact.html')

@app.route('/add_contact', methods = ['GET', 'POST'])
def add_contact():
    cursor = mydb.cursor()
    addr = {}
    phone = {}
    date = {}
    if request.method == "POST":
        for key,value in request.form.items():
            if key.startswith('addr'):
                if(key[:6] in addr):
                    addr[key[:6]][int(key[6])-1] = value
                else:
                    addr[key[:6]] = ["","","","",""]
                    addr[key[:6]][int(key[6])-1] = value
            
            if key.startswith('phone'):
                if(key[:7] in phone):
                    phone[key[:7]][int(key[7])-1] = value
                else:
                    phone[key[:7]] = ["","",""]
                    phone[key[:7]][int(key[7])-1] = value
            
            if key.startswith('date'):
                if(key[:6] in date):
                    date[key[:6]][int(key[6])-1] = value
                else:
                    date[key[:6]] = ["",""]
                    date[key[:6]][int(key[6])-1] = value
        
        if(len(''.join(phone['phone_1']))==0):
            text = "Phone number not entered!"
            return render_template('Add_Failure.html',error = text)
        
        if(len(request.form['fname'])==0 or len(request.form['lname'])==0):
            text = "Name not entered!"
            return render_template('Add_Failure.html',error = text)
        
        cursor.execute('INSERT INTO CONTACT(Fname,Mname,Lname) VALUES (%s,%s,%s)'
                       ,[request.form['fname'],request.form['mname'],request.form['lname']])
        cursor.execute('SELECT Contact_id FROM CONTACT ORDER BY Contact_id DESC LIMIT 1;')
        c_id=cursor.fetchall()[0][0]
     
        for key,value in addr.items():
            if(value[0] != '' and (value[1]!='' or value[2]!='' or value[3]!='' or value[4]!='')):
                cursor.execute('INSERT INTO ADDRESS(Contact_id,Address_type,Address,City,State,Zip) VALUES(%s,%s,%s,%s,%s,%s)'
                       ,[c_id,value[0],value[1],value[2],value[3],value[4]])
        
        for key,value in phone.items():
            cursor.execute('INSERT INTO PHONE(Contact_id,Phone_type,Area_code,Number) VALUES(%s,%s,%s,%s)'
                       ,[c_id,value[0],value[1],value[2]])
        
        for key,value in date.items():
            if(value[0]!='' and value[1] != ''):
                cursor.execute('INSERT INTO DATE(Contact_id,Date_type,Date) VALUES(%s,%s,%s)'
                       ,[c_id,value[0],value[1]])
        
        mydb.commit()
        cursor.close()
    return render_template("Success.html",success="Contact Added Successfully!")

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    cursor = mydb.cursor()
    if request.method == "POST":
        c_id = request.form['del']
        cursor.execute('DELETE FROM ADDRESS WHERE Contact_id = %s',[c_id])
        cursor.execute('DELETE FROM PHONE WHERE Contact_id = %s',[c_id])
        cursor.execute('DELETE FROM DATE WHERE Contact_id = %s',[c_id])
        cursor.execute('DELETE FROM CONTACT WHERE Contact_id = %s',[c_id])
        mydb.commit()
        cursor.close()
        return render_template("Success.html",success="Contact Deleted Successfully!")

@app.route('/modify_contact', methods = ['GET', 'POST'])
def modify_contact():
    if request.method == 'POST':
        terms = request.form['cid']
        names,phones,address,dates = fetch_details(terms)
        return render_template('ModifyContact.html',names=names,phones=phones,addresses=address,dates=dates,cid=terms)  
    
@app.route('/update_contact', methods = ['GET', 'POST'])
def update_contact():
    cursor = mydb.cursor()
    addr = {}
    phone = {}
    date = {}
    if request.method == "POST":
        for key,value in request.form.items():
            if key.startswith('addr'):
                if(key[:6] in addr):
                    addr[key[:6]][int(key[6])-1] = value
                else:
                    addr[key[:6]] = ["","","","","",-1]
                    addr[key[:6]][int(key[6])-1] = value
            
            if key.startswith('aid'):
               if('addr_'+key[4] in addr):
                   addr['addr_'+key[4]][5] = value
               else:
                   addr['addr_'+key[4]] = ["","","","","",value]
                    
            if key.startswith('phone'):
                if(key[:7] in phone):
                    phone[key[:7]][int(key[7])-1] = value
                else:
                    phone[key[:7]] = ["","","",-1]
                    phone[key[:7]][int(key[7])-1] = value
            
            if key.startswith('pid'):
                if('phone_'+key[4] in phone):
                    phone['phone_'+key[4]][3] = value
                else:
                    phone['phone_'+key[4]] = ["","","","","",value]
                    
            if key.startswith('date'):
                if(key[:6] in date):
                    date[key[:6]][int(key[6])-1] = value
                else:
                    date[key[:6]] = ["","",-1]
                    date[key[:6]][int(key[6])-1] = value
            
            if key.startswith('did'):
               if('date_'+key[4] in date):
                   date['date_'+key[4]][2] = value
               else:
                   date['date_'+key[4]] = ["","","","","",value]
        
        if(len(''.join(phone['phone_1']))==0):
            text = "Phone number not entered!"
            return render_template('Add_Failure.html',error = text)
        
        if(len(request.form['fname'])==0 or len(request.form['lname'])==0):
            text = "Name not entered!"
            return render_template('Add_Failure.html',error = text)
        
        c_id=request.form['cid']
        
        
        cursor.execute('UPDATE CONTACT SET Fname=%s,Mname=%s,Lname=%s WHERE Contact_id=%s'
                       ,[request.form['fname'],request.form['mname'],request.form['lname'],c_id])

        for key,value in addr.items():
            if(value[0] != '' and (value[1]!='' or value[2]!='' or value[3]!='' or value[4]!='')):
                if(value[5] == '-1'):
                    cursor.execute('INSERT INTO ADDRESS(Contact_id,Address_type,Address,City,State,Zip) VALUES(%s,%s,%s,%s,%s,%s)'
                       ,[c_id,value[0],value[1],value[2],value[3],value[4]])
                else:
                    cursor.execute('UPDATE ADDRESS SET Address_type=%s,Address=%s,City=%s,State=%s,Zip=%s WHERE Address_id=%s'
                       ,[value[0],value[1],value[2],value[3],value[4],value[5]])
        
        for key,value in phone.items():
            if(value[3] == '-1'):
                cursor.execute('INSERT INTO PHONE(Contact_id,Phone_type,Area_code,Number) VALUES(%s,%s,%s,%s)'
                       ,[c_id,value[0],value[1],value[2]])
            else:
                cursor.execute('UPDATE PHONE SET Phone_type=%s,Area_code=%s,Number=%s WHERE Phone_id=%s'
                       ,[value[0],value[1],value[2],value[3]])
        
        for key,value in date.items():
            if(value[0]!='' and value[1] != ''):
                if(value[2] == '-1'):
                   cursor.execute('INSERT INTO DATE(Contact_id,Date_type,Date) VALUES(%s,%s,%s)'
                       ,[c_id,value[0],value[1]])     
                else:
                    cursor.execute('UPDATE DATE SET Date_type=%s,Date=%s WHERE Date_id=%s'
                       ,[value[0],value[1],value[2]])
        
        mydb.commit()
        cursor.close()
    return render_template("Success.html",success="Contact Updated Successfully!")
    
if __name__ == '__main__':
   app.run() 