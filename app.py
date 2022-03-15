from ast import Expression
from models import (Base, session, Product, engine)

import csv
import datetime
import time


def menu():
    while True:
        print('''\no o o o o o o o o o o o
              \rTONY's STORE INVENTORY
              \ro o o o o o o o o o o o''')
        print('''\n--- Menu ---
              \r1.) View all Products
              \r2.) Add a new product to inventory
              \r3.) Backup the entire Database
              \r4.) Search for a Product
              \r5.) Exit program
              \r----------''')
        menu_choice = input('\nWhat would you like to do?:  ')
        print('\n')
        if menu_choice in  ['1', '2', '3', '4', '5']:
            return menu_choice
        else:
            input('''\n*x*x*x*x*x*x*x*x*x*x*x*
                  \rOOPS!! That was not a valid option!
                  \rPlease choose an option above.
                  \rPress enter to try again.''')       
            

def submenu():
    while True:
        print('''\n--- Options ---
            \r1) Edit
             \r2) Delete
             \r3) Return to Main Menu
             \r--------''')
        choice = input('What would you like to do?  ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''\n*x*x*x*x*x*x*x*x*x*x*x*
                  \rPlease choose one of the options above.
                  \rA number from 1-3.
                  \rPress Enter to try again.''') 
            
                        
def clean_date(date_int):        
    months = ['1', '2', '3', '4', '5', '6', 
              '7', '8', '9', '10', '11', '12']
    try:
        split_date = date_int.split('/')
        return_date = datetime.date(int(split_date[2]), int(split_date[0]), int(split_date[1]))
    except ValueError:
        input('''
              \n*x*x*x*x*x*x*x*x*x*x*x* DATE ERROR *x*x*x*x*x*x*x*x*x*x*x*
              \rThe date format should include a valid Month day, year.
              \rEx: MM/DD/YYYY
              \rPress Enter to try again.''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        if price_str[0] != '$':
            raise ValueError    
        price_float = float(price_str[1::])
        price_int = int(price_float*100)
    except ValueError:
        input('''
              \n*x*x*x*x*x*x*x*x*x*x*x* PRICE ERROR *x*x*x*x*x*x*x*x*x*x*x*
              \rThe data format should be a number starting with the $.
              \rEx: $10.99
              \rPress Enter to try again.''')
        return
    else:
        return price_int
    

def clean_id(id_str, options):
        try:
            product_id = str(id_str)
        except ValueError:
            input('''
                \n*x*x*x*x*x*x*x*x*x*x*x* ID ERROR *x*x*x*x*x*x*x*x*x*x*x*
                \rThe ID format should be a letters.
                \rPress Enter to try again.''') 
            return
        else:
            if product_id in options:
                return product_id
            else:
                input('''
                \n*x*x*x*x*x*x*x*x*x*x*x* ID ERROR *x*x*x*x*x*x*x*x*x*x*x*
                \rOptions: {options}
                \rPress Enter to try again.''') 
                return


def clean_quantity(quantity_str):
    try:
        quantity_int = int(quantity_str)
    except ValueError:
        input('''\n*x*x*x*x*x*x*x*x*x*x*x* QUANTITY ERROR *x*x*x*x*x*x*x*x*x*x*x*
            \rThe Quantity should be a number.
            \rPress Enter to try again.''')    
    else:
        return quantity_int


def edit_check(column_name, current_value):
    print(f'''\n*-*-*-* EDIT {column_name} *-*-*-*
          \r ''')
    if column_name == 'Price ':
        print(f'\rCurrent Value: ${current_value/100, 2}')
        print('Enter value like this: $25.99')
    elif column_name == 'Quantity':
        print(f'\rCurrent Value: {current_value}')  
    elif column_name == 'Date':
            print(f'\rCurrent Value: {current_value.strftime("%m/%D/%Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change this value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
            elif column_name == 'Quantity':
                changes = clean_quantity(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change this value to? ')


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = clean_quantity(row[2])
                date = clean_date(row[3])
                new_product = Product(
                    product_name = name, 
                    product_price = price, 
                    product_quantity = quantity, 
                    product_date = date)
                session.add(new_product)
        session.commit()  


def app():
    app_running = True
    while app_running:
        choice = menu()
        
        if choice == '1':
            for product in session.query(Product):
                print(f'{product.product_id} | {product.product_name} | {product.product_quantity} | $' + (f'{product.product_price}'))
            input('\nPress Enter to return to the Main Menu.') 
        
        elif choice == '2':
            print('--- New product info ---')
            name = input('Product Name: ')
            date = datetime.date.today()
            price_error = True
            while price_error:
                price = input('Price (Ex: $25.64): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                quantity = input('Quantity (Ex: 94): ')
                quantity = clean_quantity(quantity)
                if type(quantity) == int:
                    quantity_error = False
            new_product = Product(
                product_name = name, 
                product_price = price, 
                product_quantity = quantity,
                product_date = date)
            session.add(new_product)
            print("Adding to database...")
            time.sleep(1.5)
            print('Product Added!')
            time.sleep(1.5)
            session.commit()
        
        elif choice == '3':
            print("Backing up the database to 'backup.csv'...")
            time.sleep(1.5)
            with open('backup.csv', 'w', newline='') as csv_file:
                headers = ['Product_name', 'Product_price', 'Product_quantity', 'Date_updated']
                writer = csv.DictWriter(csv_file, delimiter='|', fieldnames = headers)
                writer.writeheader()
                for product in session.query(Product):
                    writer.writerow({
                        'Product_name': product.product_name, 
                        'Product_price': product.product_price, 
                        'Product_quantity': product.product_quantity, 
                        'Date_updated': product.product_date})
                print("All done!")
                time.sleep(1.5) 
        
        elif choice == '4':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            id_choice = None
            while id_error:
                print(f'Options: {id_options}')
                try:
                    user_product_id = int(input("Enter Product ID: "))
                except ValueError:
                    print("Oops. The Product ID should be a number. Try again!")
                else:
                    if user_product_id in id_options:
                        id_choice = user_product_id
                        id_error = False
                    else:
                        print("Oops. That Product ID doesn't exist. Try again!")
            the_product = session.query(Product).filter(Product.product_id == id_choice).first()
            print('--------------------------')
            print(f'ID: {the_product.product_id}')
            print(f'Product Name: {the_product.product_name}')
            print('Product Price: $' + '{:.2f}'.format(the_product.product_price / 100, 2))
            print(f'Product Quantity: {the_product.product_quantity}')
            print(f'Last Updated: {the_product.product_date}')
            print('--------------------------')
            sub_choice = submenu()
            if sub_choice == '1':
                the_product.product_name = edit_check('Product Name: ', the_product.product_name)
                the_product.product_price = edit_check('Product Price: ', the_product.product_price)
                the_product.product_quantity = edit_check('Product Quantity: ', the_product.product_quantity)
                the_product.product_date = edit_check('Date: ', the_product.product_date)
                session.commit()
                print('Product updated')
                time.sleep(1.5)
            elif sub_choice == '2':
                session.delete(the_product)
                session.commit()
                print('Product Deleted!')
                time.sleep(1.5)
        
        elif choice == '5':
            app_running = False
            print('''!o!o! GOODBYE !o!o!
                  \r~_~_~_~_~_~_~_~_~_~_~
                  \r ''')

       
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()                   
