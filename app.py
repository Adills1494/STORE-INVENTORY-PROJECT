from ast import Expression
from models import (Base, session, Product, engine)

import csv
import datetime
import time


def menu():
    while True:
        print('''\n*~*~*~*~*~*~*
          \rTONY's STORE INVENTORY
          \r*~*~*~*~*~*~*''')
        print('''\r---Menu---
              \r1.) View all Products
              \r2.) Add a new product to inventory
              \r3.) Backup the entire Database
              \r4.) Exit program
              \r*~*~*~*~*~*''')
        menu_choice = input('What would you like to do?:  ')
        if menu_choice in  ['1', '2', '3', '4']:
            return menu_choice
        else:
            input('''\n*~*~*~*~*~*~*~*~*
                  \rOOPS!! That was not a valid option!
                  \rPlease choose an option above.
                  \rPress enter to try again.''')       
   

def clean_date(date_int):        
    months = ['1', '2', '3', '4', '5', '6', 
              '7', '8', '9', '10', '11', '12']
    try:
        split_date = date_int.split('/')
        return_date = datetime.date(int(split_date[2]), int(split_date[0]), int(split_date[1]))
    except ValueError:
        input('''
              \n*~*~*~*~*~* DATE ERROR *~*~*~*~*~*
              \rThe date format should include a valid Month day, year.
              \rEx: MM/DD/YYYY
              \rPress Enter to try again.
              \r*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*''')
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
              \n*~*~*~*~*~* PRICE ERROR *~*~*~*~*~*
              \rThe data format should be a number starting with the $.
              \rEx: $10.99
              \rPress Enter to try again.
              \r*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*''')
        return
    else:
        return price_int
    

def clean_id(id_str, options):
        try:
            product_id = str(id_str)
        except ValueError:
            input('''
                \n*~*~*~*~*~* ID ERROR *~*~*~*~*~*
                \rThe ID format should be a letters.
                \rPress Enter to try again.
                \r*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*''') 
            return
        else:
            if product_id in options:
                return product_id
            else:
                input('''
                \n*~*~*~*~*~* ID ERROR *~*~*~*~*~*
                \rOptions: {options}
                \rPress Enter to try again.
                \r*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*''') 
                return


def clean_quantity(quantity_str):
    try:
        quantity_int = int(quantity_str)
    except ValueError:
        input('''\n*~*~*~*~*QUANTITY ERROR *~*~*~*~*
            \rThe Quantity should be a number.
            \rPress Enter to try again.
            \r*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*''')


def edit_check(column_name, current_value):
    print(f'\n*** EDIT {column_name} ***')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
            print(f'\rCurrent Value: {current_value.strftime("%m/%D/%Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')
     
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = row[2]
                date_updated = clean_date(row[3])
                new_product = Product(name = name, price = price, quantity = quantity, date_updated = date_updated)
                session.add(new_product)
        session.commit()  


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            for product in session.query(Product):
                print(f'{product.name} | {product.price} | {product.quantity} | {product.date_updated}')
            input('\nPress Enter to return to the Main Menu.') 
        elif choice == '2':
            name = input('\nProduct Name: ')
            price = input('Product Price: ')
            quantity = input('Product Quantity: ')
            date = input('Product Date: ')
            date_error = True
            while date_error:
                date = clean_date
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: $25.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                quantity = input('Quantity (Ex: 94): ')
                quantity = clean_quantity(quantity)
                if type(quantity) == int:
                    quantity_error = False
            new_product = Product(name = name, price = price, quantity = quantity, date_updated = date)
            session.add(new_product)
            session.commit()
            print('Product Added!')
            time.sleep(1.5)
        elif choice == '3':
            print("Backing up the database to 'backup.csv'...")
            time.sleep(1.5)
            with open('backup.csv', 'w', newline='') as csv_file:
                headers = ['product_name', 'product_price', 'product_quantity', 'date_updated']
                writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=headers)
                writer.writeheader()
                for product in session.query(Product):
                    writer.writerow({
                        'product_name': product.name,
                        'product_price': product.price,
                        'product_quantity': product.quantity,
                        'date_updated': product.date_updated})
                print("All done!")
                time.sleep(1.5)
        elif choice == '4':
            app_running = False
            print('!!!GOODBYE!!!')

       
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()          