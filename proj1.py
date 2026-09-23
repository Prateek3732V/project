import mysql.connector
MENU = """
========== WAREHOUSE MANAGEMENT ==========
 0. Exit
 1. Add/Remove supplier              
 2. List suppliers            
 3. Add product               
 4. List / search products   
 5. Receive stock (IN)       
 6. Issue stock (OUT)         
 7. Adjust stock
 8. Low-stock report
 9. Movement history
 10. Stock valuation
 11. Delete product
 12. Edit Admins List
 13. Edit Managers List
 14. Edit Sales Person List
===========================================
"""

MENU1 = """========== WAREHOUSE MANAGEMENT ==========
 0. Exit
 1. Add/Remove supplier              
 2. List suppliers            
 3. Add product               
 4. List / search products   
 5. Receive stock (IN)       
 6. Issue stock (OUT)         
 7. Adjust stock
 8. Low-stock report
 9. Movement history
 10. Stock valuation
 11. Delete product
==========================================="""

MENU2 = """========== WAREHOUSE MANAGEMENT ==========
 0. Exit
 1. List / search products   
 2. Issue stock (OUT)"""


pwd=input("Enter your MySQL password: ")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pwd
)
cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS warehouse_management")
cursor.execute("USE warehouse_management")
cursor.execute("CREATE TABLE IF NOT EXISTS sales_person (" \
"user_id VARCHAR(255) PRIMARY KEY," \
"username VARCHAR(255) not null, " \
"password VARCHAR(255) not null)")
cursor.execute("CREATE TABLE IF NOT EXISTS managers (" \
"user_id VARCHAR(255) PRIMARY KEY, " \
"username VARCHAR(255) not null, " \
"password VARCHAR(255) not null)")
cursor.execute("CREATE TABLE IF NOT EXISTS admins (" \
"user_id VARCHAR(255) PRIMARY KEY, " \
"username VARCHAR(255) not null, " \
"password VARCHAR(255) not null)")
cursor.execute("CREATE TABLE IF NOT EXISTS suppliers (" \
"supplier_id VARCHAR(255) PRIMARY KEY, " \
"name VARCHAR(255), " \
"contact_info VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS products (" \
"product_id VARCHAR(255) PRIMARY KEY, " \
"name VARCHAR(255), " \
"description VARCHAR(255), " \
"supplier_id VARCHAR(255), " \
"price INT, " \
"stock_quantity INT, " \
"FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id))")
cursor.execute("CREATE TABLE IF NOT EXISTS stock_movements (" \
"movement_id INT AUTO_INCREMENT PRIMARY KEY, " \
"product_id VARCHAR(255), " \
"movement_type ENUM('IN', 'OUT'), " \
"quantity INT, " \
"movement_date DATETIME, " \
"FOREIGN KEY (product_id) REFERENCES products(product_id))")
cursor.execute("CREATE TABLE IF NOT EXISTS login_history (" \
"login_id INT AUTO_INCREMENT PRIMARY KEY, " \
"user_id VARCHAR(255), " \
"login_time DATETIME, " \
"FOREIGN KEY (user_id) REFERENCES sales_person(user_id))")
mydb.commit()

check=0
while check==0:
    print("1.Login\n2.Exit")
    choice=int(input("Enter your choice: "))
    if choice==2:
        print("\nExiting the program.")
        check=1
    elif choice==1:
        print("\n\n1.Login as Sales Person\n2.Login as Manager\n3.Login as Admin\n\n")
        login_choice = int(input("Enter your choice: "))
        if login_choice == 1:
            sales_person_id = input("Enter your user ID: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cursor.execute("SELECT * FROM sales_person WHERE user_id=%s AND username=%s AND password=%s", (sales_person_id, username, password))
            user = cursor.fetchone()
            if user:
                print("Login successful!")
                q=0
                while q==0:
                    print("\n\n" + MENU2 + "\n\n")
                    choice1 = int(input("Enter your choice: "))
                    if choice1 == 0:
                        print("\nExiting the program.")
                        q=1
                        check=1
                        user=None
                    elif choice1 == 1:
                        search_choice = input("Search by (1) Name or (2) ID or (3) Show All? ")
                        if search_choice == '1':
                            name = input("Enter product name to search: ")
                            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + name + '%',))
                        elif search_choice == '2':
                            product_id = input("Enter product ID to search: ")
                            cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
                        elif search_choice == '3':
                            cursor.execute("SELECT * FROM products")
                        else:
                            print("Invalid choice.")
                        products = cursor.fetchall()
                        if not products:
                            print("Product not found.")
                        for product in products:
                            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Supplier ID: {product[3]}, Price: {product[4]}, Stock Quantity: {product[5]}")
                    elif choice1 == 2:
                        product_id = input("Enter product ID to issue stock: ")
                        quantity = int(input("Enter quantity to issue: "))
                        cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id=%s", (quantity, product_id))
                        cursor.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, movement_date) VALUES (%s, 'OUT', %s, NOW())", (product_id, quantity))
                        mydb.commit()
                        print("Stock issued successfully.")
            else:
                print("Invalid username or password.")


        elif login_choice == 2:
            manager_id = input("Enter your user ID: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cursor.execute("SELECT * FROM managers WHERE user_id=%s AND username=%s AND password=%s", (manager_id, username, password))
            user = cursor.fetchone()
            if user:
                print("Login successful!")
                q=0
                while q==0:
                    print("\n\n" + MENU1 + "\n\n")
                    choice1 = int(input("Enter your choice: "))
                    if choice1 == 0:
                        print("\nExiting the program.")
                        q=1
                        check=1
                        user=None
                    elif choice1 == 1:
                        ch=input("1.Add Supplier\n2.Remove Supplier\nEnter your choice: ")
                        if ch=='1':
                            name = input("Enter supplier name: ")
                            contact_info = input("Enter supplier contact info: ")
                            supplier_id = input("Enter supplier ID: ")
                            cursor.execute("INSERT INTO suppliers (name, contact_info, supplier_id) VALUES (%s, %s, %s)", (name, contact_info, supplier_id))
                            mydb.commit()
                            print("Supplier added successfully.")
                        elif ch=='2':
                            supplier_id = input("Enter supplier ID to remove: ")
                            cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
                            mydb.commit()
                            print("Supplier removed successfully.")
                        else:
                            print("Invalid choice.")
                    elif choice1==2:
                        cursor.execute("SELECT supplier_id, name, contact_info FROM warehouse_management.suppliers")
                        suppliers1 = cursor.fetchall()
                        if not suppliers1:
                            print("No suppliers found.")
                        else:
                            for supplier in suppliers1:
                                print("ID:", supplier[0], "Name:", supplier[1], "Contact Info:", supplier[2])
                    elif choice1 == 3:
                        name = input("Enter product name: ")
                        description = input("Enter product description: ")
                        supplier_id = input("Enter supplier ID: ")
                        product_id = input("Enter product ID: ")
                        price = float(input("Enter product price: "))
                        stock_quantity = int(input("Enter stock quantity: "))
                        cursor.execute("INSERT INTO products (name, description, supplier_id, product_id, price, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s)", (name, description, supplier_id, product_id, price, stock_quantity))
                        mydb.commit()
                        print("Product added successfully.")
                    elif choice1 == 4:
                        search_choice = input("Search by (1) Name or (2) ID or (3) Show All? ")
                        if search_choice == '1':
                            name = input("Enter product name to search: ")
                            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + name + '%',))
                        elif search_choice == '2':
                            product_id = input("Enter product ID to search: ")
                            cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
                        elif search_choice == '3':
                            cursor.execute("SELECT * FROM products")
                        else:
                            print("Invalid choice.")
                        products = cursor.fetchall()
                        if not products:
                            print("Product not found.")
                        for product in products:
                            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Supplier ID: {product[3]}, Price: {product[4]}, Stock Quantity: {product[5]}")
                    elif choice1 == 5:
                        product_id = input("Enter product ID to receive stock: ")
                        quantity = int(input("Enter quantity to receive: "))
                        cursor.execute("UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id=%s", (quantity, product_id))
                        cursor.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, movement_date) VALUES (%s, 'IN', %s, NOW())", (product_id, quantity))
                        mydb.commit()
                        print("Stock received successfully.")
                    elif choice1 == 6:
                        product_id = input("Enter product ID to issue stock: ")
                        quantity = int(input("Enter quantity to issue: "))
                        cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id=%s", (quantity, product_id))
                        cursor.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, movement_date) VALUES (%s, 'OUT', %s, NOW())", (product_id, quantity))
                        mydb.commit()
                        print("Stock issued successfully.")
                    elif choice1 == 7:
                        product_id = input("Enter product ID to adjust stock: ")
                        new_quantity = int(input("Enter new stock quantity: "))
                        cursor.execute("UPDATE products SET stock_quantity = %s WHERE product_id=%s", (new_quantity, product_id))
                        mydb.commit()
                        print("Stock adjusted successfully.")
                    elif choice1 == 8:
                        low_stock_threshold = int(input("Enter low stock threshold: "))
                        cursor.execute("SELECT * FROM products WHERE stock_quantity < %s", (low_stock_threshold,))
                        low_stock_products = cursor.fetchall()
                        for product in low_stock_products:
                            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Supplier ID: {product[3]}, Price: {product[4]}, Stock Quantity: {product[5]}")
                    elif choice1 == 9:
                        cursor.execute("SELECT * FROM stock_movements")
                        movements = cursor.fetchall()
                        for movement in movements:
                            print(f"Movement ID: {movement[0]}, Product ID: {movement[1]}, Type: {movement[2]}, Quantity: {movement[3]}, Date: {movement[4]}")
                    elif choice1 == 10:
                        cursor.execute("SELECT SUM(price * stock_quantity) FROM products")
                        total_valuation = cursor.fetchone()[0]
                        print(f"Total stock valuation: {total_valuation}")
                    elif choice1 == 11:
                        id = input("Enter product ID to delete: ")
                        cursor.execute("DELETE FROM products WHERE product_id=%s", (id,))
                        mydb.commit()
                        print("Product deleted successfully.")

            else:
                print("Invalid username or password.")

        elif login_choice == 3:
            uid = input("Enter your user ID: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s AND user_id=%s", (username, password, uid))
            user = cursor.fetchone()
            if user:
                print("Login successful!")
                q=0
                while q==0:
                    print("\n\n" + MENU + "\n\n")
                    choice1 = int(input("Enter your choice: "))
                    if choice1 == 0:
                        print("\nExiting the program.")
                        q=1
                        check=1
                        user=None
                    elif choice1 == 1:
                        ch=input("1.Add Supplier\n2.Remove Supplier\nEnter your choice: ")
                        if ch=='1':
                            name = input("Enter supplier name: ")
                            contact_info = input("Enter supplier contact info: ")
                            supplier_id = input("Enter supplier ID: ")
                            cursor.execute("INSERT INTO suppliers (name, contact_info, supplier_id) VALUES (%s, %s, %s)", (name, contact_info, supplier_id))
                            mydb.commit()
                            print("Supplier added successfully.")
                        elif ch=='2':
                            supplier_id = input("Enter supplier ID to remove: ")
                            cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
                            mydb.commit()
                            print("Supplier removed successfully.")
                        else:
                            print("Invalid choice.")

                    elif choice1==2:
                        cursor.execute("SELECT supplier_id, name, contact_info FROM warehouse_management.suppliers")
                        suppliers1 = cursor.fetchall()
                        if not suppliers1:
                            print("No suppliers found.")
                        else:
                            for supplier in suppliers1:
                                print("ID:", supplier[0], "Name:", supplier[1], "Contact Info:", supplier[2])
                    elif choice1 == 3:
                        name = input("Enter product name: ")
                        description = input("Enter product description: ")
                        supplier_id = input("Enter supplier ID: ")
                        product_id = input("Enter product ID: ")
                        price = float(input("Enter product price: "))
                        stock_quantity = int(input("Enter stock quantity: "))
                        cursor.execute("INSERT INTO products (name, description, supplier_id, product_id, price, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s)", (name, description, supplier_id, product_id, price, stock_quantity))
                        mydb.commit()
                        print("Product added successfully.")
                    elif choice1 == 4:
                        search_choice = input("Search by (1) Name or (2) ID or (3) Show All? ")
                        if search_choice == '1':
                            name = input("Enter product name to search: ")
                            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + name + '%',))
                        elif search_choice == '2':
                            product_id = input("Enter product ID to search: ")
                            cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
                        elif search_choice == '3':
                            cursor.execute("SELECT * FROM products")
                        else:
                            print("Invalid choice.")
                        products = cursor.fetchall()
                        if not products:
                            print("Product not found.")
                        for product in products:
                            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Supplier ID: {product[3]}, Price: {product[4]}, Stock Quantity: {product[5]}")

                    elif choice1 == 5:
                        product_id = input("Enter product ID to receive stock: ")
                        quantity = int(input("Enter quantity to receive: "))
                        cursor.execute("UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id=%s", (quantity, product_id))
                        cursor.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, movement_date) VALUES (%s, 'IN', %s, NOW())", (product_id, quantity))
                        mydb.commit()
                        print("Stock received successfully.")
                    elif choice1 == 6:
                        product_id = input("Enter product ID to issue stock: ")
                        quantity = int(input("Enter quantity to issue: "))
                        cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id=%s", (quantity, product_id))
                        cursor.execute("INSERT INTO stock_movements (product_id, movement_type, quantity, movement_date) VALUES (%s, 'OUT', %s, NOW())", (product_id, quantity))
                        mydb.commit()
                        print("Stock issued successfully.")
                    elif choice1 == 7:
                        product_id = input("Enter product ID to adjust stock: ")
                        new_quantity = int(input("Enter new stock quantity: "))
                        cursor.execute("UPDATE products SET stock_quantity = %s WHERE product_id=%s", (new_quantity, product_id))
                        mydb.commit()
                        print("Stock adjusted successfully.")
                    elif choice1 == 8:
                        low_stock_threshold = int(input("Enter low stock threshold: "))
                        cursor.execute("SELECT * FROM products WHERE stock_quantity < %s", (low_stock_threshold,))
                        low_stock_products = cursor.fetchall()
                        for product in low_stock_products:
                            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Supplier ID: {product[3]}, Price: {product[4]}, Stock Quantity: {product[5]}")
                    elif choice1 == 9:
                        cursor.execute("SELECT * FROM stock_movements")
                        movements = cursor.fetchall()
                        for movement in movements:
                            print(f"Movement ID: {movement[0]}, Product ID: {movement[1]}, Type: {movement[2]}, Quantity: {movement[3]}, Date: {movement[4]}")
                    elif choice1 == 10:
                        cursor.execute("SELECT SUM(price * stock_quantity) FROM products")
                        total_valuation = cursor.fetchone()[0]
                        print(f"Total stock valuation: {total_valuation}")
                    elif choice1 == 11:
                        id = input("Enter product ID to delete: ")
                        cursor.execute("DELETE FROM products WHERE product_id=%s", (id,))
                        mydb.commit()
                        print("Product deleted successfully.")
                    elif choice1 == 12:
                        cho=input("1.Add Admin\n2.Remove Admin\n3.Edit Admin\nEnter your choice: ")
                        if cho=='1':
                            username = input("Enter admin username: ")
                            password = input("Enter admin password: ")
                            admin_id = input("Enter admin user ID: ")
                            cursor.execute("INSERT INTO admins (username, password, user_id) VALUES (%s, %s, %s)", (username, password, admin_id))
                            mydb.commit()
                            print("Admin added successfully.")
                        elif cho=='2':
                            admin_id = input("Enter admin ID to remove: ")
                            cursor.execute("DELETE FROM admins WHERE user_id=%s", (admin_id,))
                            mydb.commit()
                            print("Admin removed successfully.")
                        elif cho=='3':
                            admin_id = input("Enter admin ID to edit: ")
                            new_username = input("Enter new admin username: ")
                            new_password = input("Enter new admin password: ")
                            cursor.execute("UPDATE admins SET username=%s, password=%s WHERE user_id=%s", (new_username, new_password, admin_id))
                            mydb.commit()
                            print("Admin edited successfully.")
                        else:
                            print("Invalid choice.")
                    elif choice1 == 13:
                        cho=input("1.Add Manager\n2.Remove Manager\n3.Edit Manager\nEnter your choice: ")
                        if cho=='1':
                            manager_id = input("Enter manager ID: ")
                            username = input("Enter manager username: ")
                            password = input("Enter manager password: ")
                            cursor.execute("INSERT INTO managers (user_id, username, password) VALUES (%s, %s, %s)", (manager_id, username, password))
                            mydb.commit()
                            print("Manager added successfully.")
                        elif cho=='2':
                            manager_id = input("Enter manager ID to remove: ")
                            cursor.execute("DELETE FROM managers WHERE user_id=%s", (manager_id,))
                            mydb.commit()
                            print("Manager removed successfully.")
                        elif cho=='3':
                            manager_id = input("Enter manager ID to edit: ")
                            new_username = input("Enter new manager username: ")
                            new_password = input("Enter new manager password: ")
                            cursor.execute("UPDATE managers SET username=%s, password=%s WHERE user_id=%s", (new_username, new_password, manager_id))
                            mydb.commit()
                            print("Manager edited successfully.")
                        else:
                            print("Invalid choice.")
                    
                    elif choice1 == 14:
                        cho=input("1.Add Sales Person\n2.Remove Sales Person\n3.Edit Sales Person\nEnter your choice: ")
                        if cho=='1':
                            sales_person_id = input("Enter sales person ID: ")
                            username = input("Enter sales person username: ")
                            password = input("Enter sales person password: ")
                            cursor.execute("INSERT INTO sales_person (user_id, username, password) VALUES (%s, %s, %s)", (sales_person_id, username, password))
                            mydb.commit()
                            print("Sales person added successfully.")
                        elif cho=='2':
                            sales_person_id = input("Enter sales person ID to remove: ")
                            cursor.execute("DELETE FROM sales_person WHERE user_id=%s", (sales_person_id,))
                            mydb.commit()
                            print("Sales person removed successfully.")
                        elif cho=='3':
                            sales_person_id = input("Enter sales person ID to edit: ")
                            new_username = input("Enter new sales person username: ")
                            new_password = input("Enter new sales person password: ")
                            cursor.execute("UPDATE sales_person SET username=%s, password=%s WHERE user_id=%s", (new_username, new_password, sales_person_id))
                            mydb.commit()
                            print("Sales person edited successfully.")
                        else:
                            print("Invalid choice.")
                    else:
                        print("Invalid choice.")

                   
    else:
        print("Invalid username or password.")