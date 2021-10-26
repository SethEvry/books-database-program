from models import (Base, session, Book, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''
              \nProgramming Books
              \r1) Add book
              \r2) View all books
              \r3) Seach for book
              \r4) Book Analysis
              \r5) Exit
              ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rA number from 1-5.
                  \rPress enter to try again.''')


def clean_date(date_string):
    fmt = '%B %d, %Y'
    try:
        date = datetime.datetime.strptime(date_string, fmt).date()
    except ValueError:
        input('''
              \n****** DATE ERROR ******
              \rThe Date format should include a valid Month, Day, and Year from the past
              \r Ex: Juanuary 1, 2021
              \r Press Enter to try again.
              \r**************************''')
        return
    else:
        return date


def clean_price(price_string):
    try:
        price_float = float(price_string)
    except ValueError:
        input('''
              \n****** Price ERROR ******
              \rThe Date format should include a price without a currency symbol.
              \r Ex: 19.99
              \r Press Enter to try again.
              \r**************************''')
    return int(price_float * 100)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(
                Book.title == row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author,
                                published_date=date, price=price)
                session.add(new_book)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "1":  # Add book
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex: January 1, 2021): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 19.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author,
                            published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book Added!')
            time.sleep(1.5)
        elif choice == "2":  # View all books
            pass
        elif choice == "3":  # Search for a book
            pass
        elif choice == "4":  # Book Analysis
            pass
        else:                 # Exit
            print('Goodbye!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
