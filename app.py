from models import (Base, session, Book, engine)


if __name__ == '__main__':
    Base.metadate.create_all(engine)
