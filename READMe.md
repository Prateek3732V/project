

Prerequisites

Before running the application, make sure the following software is installed on your system:

1.Python 
2.MySQL 

Clone or Set Up the Project Repository

Install the required MySQL connector package by giving the command in terminal:   "pip install mysql-connector-python"


Configuration & First-Time Database Setup
Start MySQL Service:Ensure your local MySQL server is up and running.Database Auto-Initialization:
The application automatically initializes the required database (warehouse_management) and schema tables (admins, managers, sales_person, suppliers, products, stock_movements, login_history) upon the first run.   

Creating Initial Seed Users (First Launch)
Because the database starts empty, user authentication will fail until user accounts exist. You must populate at least one initial user directly via the MySQL Workbench before logging into the application.   
Open MySQL command line
Execute the following SQL commands to seed initial accounts
USE warehouse_management;

-- Seed an Admin user using the following command
INSERT INTO admins (user_id, username, password) VALUES ('0001', 'admin1', 'adminpassword');

-- Seed a Manager user (Optional) using the following command
INSERT INTO managers (user_id, username, password) VALUES ('0002', 'manager1', 'mgrpassword');

-- Seed a Sales Person user (Optional) using the following command
INSERT INTO sales_person (user_id, username, password) VALUES ('0003', 'sales1', 'salespassword');





Execution Instructions 

Run the Application:
Execute the main script using Python
When launched, the program will prompt: your MySQL password:
Provide the password for your local MySQL root user.   
Login & Usage:Select option 1 to Login.   
Select your role (1. Sales Person, 2. Manager, 3. Admin).   
Enter your User ID, Username, and Password as seeded during the configuration step.   
Once logged in, you can navigate through the menu options to perform various warehouse management tasks based on your role.
