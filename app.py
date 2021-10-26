from models import (Base, session, Book, engine)
import csv
import datetime


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
    return datetime.datetime.strptime(date_string, fmt).date()


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            print(row)


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        else:
            print('Goodbye!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app()
