# Contacts Web Application
Implementation of a Contacts Web Application with a MySQL database in the back-end
1. Overview:
• The homepage is a search bar. On clicking search icon, all the records in the database that match any of the search terms are returned.
• The first name, middle name and last name are displayed as the search results.
• View button opens a contact display page, modify button opens a contact modify page and the delete button deletes the contact.
• Modify and delete can also be done from the contact display page.
2. Database:
A MySQL database is used to store the Contact data. There are four tables:
• CONTACT : Auto-increment int Contact_id, varchar fname, mname and lname.
• PHONE: Auto-increment int Phone_id,int Contact_id, varchar Phone_type, int Area_code and int Number.
• ADDRESS: Auto-increment int Address_id,int Contact_id, varchar Address_type, Address, City, State and Zip.
• DATE: Auto-increment int Date_id, int Contact_id, varchar Date_type and date Date.
Contact_id is the foreign key for PHONE, ADDRESS and DATE table.
3. Middleware:
Python 3 along with an SQL connector (mysqldb) and a web framework (Flask) form the middle ware of the application.
LoadData.py is used to load the data from ‘contacts.csv’ into the database. The SQL insert statements are executed through the mysqldb connector.
Contacts.py is the main application file which connects the database to the web application.
4. Routing:
‘/’: Displays the homepage.
‘/search’: Displays the search results. The search terms are queried through the database and the hits are displayed. A no results page is displayed if there are no hits. Each of the search results can be viewed, modified or deleted.
‘/display’: Displays the Contact Details when a hit from the search is clicked. The contact can be modified or deleted by clicking the appropriate button.
‘/new_contact’: Redirects to a form where a new contact can be created.
‘/add_contact’: If the contact details are filled in correctly, a new contact entry is pushed into the database.
‘/delete’: Used to delete a contact from the database. The delete is cascaded across all tables.
‘/modify_contact’: Redirects to a form where the current contact can be modified, and new fields can be added.
‘/update_contact’: If the contact details are filled correctly, existing records are updated and new records are created in the database.
5. Assumptions:
• First Name and Last Name are compulsory.
• At least one phone type, area code and number are compulsory.
• Zip code must be empty or 5 digits.
• Area Code must be 3 digits.
• Number must be 7 digits.
• Search terms must be separated by a comma.
• Phone number is entered without hyphen.
• Area Code and Number are searched separately.
