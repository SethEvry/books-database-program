from models import (Base, session, Book, engine)


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


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    menu()
