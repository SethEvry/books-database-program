from models import (Base, session, Book, engine)
import csv
import datetime
import time

DATE_FORMAT = '%B %d, %Y'


def menu():
    while True:
        print('''
              \nPROGRAMMING BOOKS
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


def submenu():
    while True:
        print('''
              \n1) Edit
              \r2) Delete
              \r3) Return to main menu ''')
        choice = input('\nWhat would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rA number from 1-3.
                  \rPress enter to try again.''')


def clean_date(date_string):
    try:
        date = datetime.datetime.strptime(date_string, DATE_FORMAT).date()
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
    else:
        return int(price_float * 100)


def clean_id(id_string, options):
    try:
        book_id = int(id_string)
    except ValueError:
        input('''
              \n****** ID ERROR ******
              \rThe ID should be a number.
              \r Press Enter to try again.
              \r**************************''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
              \n****** ID ERROR ******
              \rOptions: {options}
              \r Press Enter to try again.
              \r**************************''')
            return


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


def edit_check(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {current_value.strftime(DATE_FORMAT)}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input(
                f'What would you like to change the {column_name} to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            else:
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes

    else:
        return input(f'What would you like to change the {column_name} to? ')


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
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\n\nPress enter to return to the main menu.')
        elif choice == "3":  # Search for a book
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
                id_error = True
            while id_error:
                id_choice = input(f'''
                    \nID Options: {id_options}
                    \rBookd id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(
                Book.id == id_choice).first()
            print(f'''
                    \n{the_book.title} by {the_book.author}
                    \rPublished: {the_book.published_date}
                    \rPrice: ${the_book.price/100}''')
            sub_choice = submenu()
            if sub_choice == '1':  # edit
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check(
                    'Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print('Book updated!')
                time.sleep(1.5)
            elif sub_choice == '2':
                session.delete(the_book)
                session.commit()
                print('Book deleted!')
                time.sleep(1.5)
                pass
        elif choice == "4":  # Book Analysis
            newest_book = session.query(Book).order_by(
                Book.published_date.desc()).first()
            oldest_book = session.query(Book).order_by(
                Book.published_date).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(
                Book.title.like('%Python%')).count()
            print(f'''
                  \n****** BOOK ANALYSIS ******
                  \r Oldest Book: {oldest_book}
                  \r Newest Book: {newest_book}
                  \r Total Books: {total_books}
                  \r Number of Python Books: {python_books}
                  \r***************************''')
            input('\n\nPress enter to return to the main menu.')
        else:                 # Exit
            print('Goodbye!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
