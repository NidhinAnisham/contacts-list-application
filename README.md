# Contacts Web Application
Implementation of a Contacts Web Application with a MySQL database in the back-end

## Overview:
1. The homepage is a search bar. On clicking search icon, all the records in the database that match any of the search terms are returned.
2. The first name, middle name and last name are displayed as the search results.
3. View button opens a contact display page, modify button opens a contact modify page and the delete button deletes the contact.
4. Modify and delete can also be done from the contact display page.

## Database:
A MySQL database is used to store the Contact data. There are four tables:
1. CONTACT : Auto-increment int Contact_id, varchar fname, mname and lname.
2. PHONE: Auto-increment int Phone_id,int Contact_id, varchar Phone_type, int Area_code and int Number.
3. ADDRESS: Auto-increment int Address_id,int Contact_id, varchar Address_type, Address, City, State and Zip.
4. DATE: Auto-increment int Date_id, int Contact_id, varchar Date_type and date Date.
Contact_id is the foreign key for PHONE, ADDRESS and DATE table.

## Middleware:
Python 3 along with an SQL connector (mysqldb) and a web framework (Flask) form the middle ware of the application.
LoadData.py is used to load the data from ‘contacts.csv’ into the database. The SQL insert statements are executed through the mysqldb connector.
Contacts.py is the main application file which connects the database to the web application.

## Routing:
1. ‘/’: Displays the homepage.
2. ‘/search’: Displays the search results. The search terms are queried through the database and the hits are displayed. A no results page is displayed if there are no hits. Each of the search results can be viewed, modified or deleted.
3. ‘/display’: Displays the Contact Details when a hit from the search is clicked. The contact can be modified or deleted by clicking the appropriate button.
4. ‘/new_contact’: Redirects to a form where a new contact can be created.
5. ‘/add_contact’: If the contact details are filled in correctly, a new contact entry is pushed into the database.
6. ‘/delete’: Used to delete a contact from the database. The delete is cascaded across all tables.
7. ‘/modify_contact’: Redirects to a form where the current contact can be modified, and new fields can be added.
8. ‘/update_contact’: If the contact details are filled correctly, existing records are updated and new records are created in the database.

## Assumptions:
1. First Name and Last Name are compulsory.
2. At least one phone type, area code and number are compulsory.
3. Zip code must be empty or 5 digits.
4. Area Code must be 3 digits.
5. Number must be 7 digits.
6. Search terms must be separated by a comma.
7. Phone number is entered without hyphen.
8. Area Code and Number are searched separately.
