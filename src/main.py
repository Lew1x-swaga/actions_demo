class Book:
    def __init__(self, title, author, year, available=True):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = available
    
    def get_title(self):
        return (self.__title)
    
    def get_author(self):
        return (self.__author)
    
    def get_year(self):
        return (self.__year)
    
    def is_available(self):
        return (self.__available)
    
    def mark_as_taken(self):
        self.__available = False
    
    def mark_as_returned(self):
        self.__available = True
    
    def __str__(self):
        status = "доступна" if self.__available else "выдана"
        return f'"{self.__title}" - "{self.__author}", {self.__year}; ({status})'


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition, available=True):
        super().__init__(title, author, year, available) 
        self.pages = pages
        self.condition = condition
    
    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"

    def __str__(self):
        base = super().__str__()
        return (f"{base}, {self.pages} стр., состояние: {self.condition}")
    


class EBook(Book):
    def __init__(self, title, author, year, file_size, format_type, available=True):
        super().__init__(title, author, year, available)
        self.file_size = file_size
        self.format = format_type
    
    def download(self):
        print(f'Книга "{self.get_title()}" загружается...{self.file_size} МБ')
    


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []
    
    def borrow(self, book):
        # 1-ое доп задание
        if len(self.__borrowed_books) >= 3:
            print(f"Ошибка: у {self.name} уже максимальное количество книг (3)")
            return False
        
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(f'Книга "{book.get_title()}" выдана {self.name}')
            return True
        else:
            print(f'Книга "{book.get_title()}" уже выдана')
            return False
    
    def return_book(self, book):
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            print(f'Книга "{book.get_title()}" возвращена by {self.name}')
            return True
        else:
            print(f'У {self.name} нет книги "{book.get_title()}"')
            return False
    
    def show_books(self):
        if not self.__borrowed_books:
            print(f"У {self.name} нет книг")
        else:
            print(f"Книги {self.name}:")
            for i, book in enumerate(self.__borrowed_books, 1):
                print(f"  {i}. {book.get_title()} - {book.get_author()}")
    
    def get_borrowed_books(self):
        return self.__borrowed_books.copy()


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)
    
    def remove_book(self, library, title):
        library.remove_book(title)
    
    def register_user(self, library, user):
        library.add_user(user)


class Library:
    def __init__(self): 
        self.__books = []
        self.__users = []
    
    def add_book(self, book):
        self.__books.append(book)
        print(f'Книга "{book.get_title()}" добавлена в библиотеку')
    
    def remove_book(self, title):
        book = self.find_book(title)
        if book is None:
            print(f'Книга "{title}" не найдена')
            return False
        elif not book.is_available():
            print(f'Нельзя удалить книгу "{title}" - она уже выдана')
            return False
        else:
            self.__books.remove(book)
            print(f'Книга "{title}" удалена из библиотеки')
            return True
        
    def add_user(self, user):
        self.__users.append(user)
        print(f"{user.name} зарегистрирован в библиотеке")
    
    def find_book(self, title):
        for book in self.__books:
            if book.get_title().lower() == title.lower():
                return book
        return None
    
    def find_user(self, name):
        for user in self.__users:
            if user.name == name:
                return user
        return None
    
    def show_all_books(self):
        if len (self.__books) == 0:
            print("В библиотеке нет книг")
        else:
            print("Все книги в библиотеке:")
            for book in self.__books:
                print(f"{book}")
    
    def show_available_books(self):
        available_books = [book for book in self.__books if book.is_available()]
        if not available_books:
            print("Нет доступных книг")
        else:
            print("Доступные книги:")
            for book in available_books:
                print(f"{book}")
    
    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)
        
        if not book:
            print(f'Книга "{title}" не найдена в библиотеке')
            return False
        
        if not user:
            print(f"{user_name} не зарегистрирован в библиотеке")
            return False
        
        return user.borrow(book)
    
    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)
        
        if not book:
            print(f'Книга "{title}" не найдена в библиотеке')
            return False
        
        if not user:
            print(f"{user_name} не зарегистрирован в библиотеке")
            return False
        
        return user.return_book(book)
    #2 доп задание

    def list_author(self, author):
        i = 0
        books = []
        for book in self.__books:
            if book.get_author()    .lower() == author.lower():
                i += 1
                books.append(book)
        if i == 0:
            print(f'В библиотеки нет книг автора "{author}"')
        else: 
                for book in books:
                    print(f"- {book}")
        return None
    
    #2 доп задание
    def list_year(self, year):
        i = 0
        books = []
        for book in self.__books:
            if book.get_year() == year:
                i += 1
                books.append(book)   
        if i == 0:
            print(f'В библиотеки нет книг {year} года')
        else:
            for book in books:
                print(f"- {book}")
        return None
                

if __name__ == '__main__':
    lib = Library()

    # --- создаём книги ---
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

    # --- создаём пользователей ---
    user1 = User("Анна")
    librarian = Librarian("Мария")

    # --- библиотекарь добавляет книги ---
    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)

    # --- библиотекарь регистрирует пользователя ---
    librarian.register_user(lib, user1)

    # --- пользователь берёт книгу ---
    lib.lend_book("Война и мир", "Анна")

    # --- пользователь смотрит свои книги ---
    user1.show_books()

    # --- возвращает книгу ---
    lib.return_book("Война и мир", "Анна")

    # --- электронная книга ---
    b2.download()

    # --- ремонт книги ---
    b3.repair()
    print(b3)
