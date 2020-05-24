create database contacts;

use contacts;

create table CONTACT(Contact_id INT UNIQUE NOT NULL AUTO_INCREMENT, Fname VARCHAR(100), Mname VARCHAR(100), Lname VARCHAR(100));

create table ADDRESS(Address_id INT UNIQUE NOT NULL AUTO_INCREMENT,Contact_id INT, Address_type VARCHAR(50), Address VARCHAR(50),City VARCHAR(50),State VARCHAR(50),Zip VARCHAR(50), constraint foreign key(Contact_id) references CONTACT(Contact_id));

create table PHONE(Phone_id INT UNIQUE NOT NULL AUTO_INCREMENT, Contact_id INT, Phone_type VARCHAR(50),Area_code INT, Number INT, constraint foreign key(Contact_id) references CONTACT(Contact_id));

create table DATE(Date_id INT UNIQUE NOT NULL AUTO_INCREMENT, Contact_id INT, Date_type VARCHAR(50), Date DATE, constraint foreign key(Contact_id) references CONTACT(Contact_id));