import unittest
from src.main import Book, PrintedBook, EBook, User, Librarian, Library


class TestBook(unittest.TestCase):
    
    def test_book_creation(self):
        book = Book("Test Book", "Test Author", 2023)
        self.assertEqual(book.get_title(), "Test Book")
        self.assertEqual(book.get_author(), "Test Author")
        self.assertEqual(book.get_year(), 2023)
        self.assertTrue(book.is_available())
    
    def test_book_mark_as_taken(self):
        book = Book("Test Book", "Test Author", 2023)
        book.mark_as_taken()
        self.assertFalse(book.is_available())
    
    def test_book_mark_as_returned(self):
        book = Book("Test Book", "Test Author", 2023, available=False)
        book.mark_as_returned()
        self.assertTrue(book.is_available())


class TestPrintedBook(unittest.TestCase):
    
    def test_printed_book_creation(self):
        book = PrintedBook("Test Book", "Test Author", 2023, 100, "хорошая")
        self.assertEqual(book.get_title(), "Test Book")
        self.assertEqual(book.pages, 100)
        self.assertEqual(book.condition, "хорошая")
    
    def test_printed_book_repair(self):
        book = PrintedBook("Test Book", "Test Author", 2023, 100, "плохая")
        book.repair()
        self.assertEqual(book.condition, "хорошая")
        
        book.repair()
        self.assertEqual(book.condition, "новая")


class TestEBook(unittest.TestCase):
    
    def test_ebook_creation(self):
        book = EBook("Test Book", "Test Author", 2023, 5, "epub")
        self.assertEqual(book.get_title(), "Test Book")
        self.assertEqual(book.file_size, 5)
        self.assertEqual(book.format, "epub")


class TestUser(unittest.TestCase):
    
    def test_user_creation(self):
        user = User("Дементий")
        self.assertEqual(user.name, "Дементий")
        self.assertEqual(len(user.get_borrowed_books()), 0)
    
    def test_user_borrow_book(self):
        user = User("Дементий")
        book = Book("Test Book", "Test Author", 2023)
        result = user.borrow(book)
        self.assertTrue(result)
        self.assertFalse(book.is_available())
        self.assertEqual(len(user.get_borrowed_books()), 1)
    
    def test_user_borrow_max_books(self):
        user = User("Дементий")
        book1 = Book("Book 1", "Author", 2023)
        book2 = Book("Book 2", "Author", 2023)
        book3 = Book("Book 3", "Author", 2023)
        book4 = Book("Book 4", "Author", 2023)
        
        user.borrow(book1)
        user.borrow(book2)
        user.borrow(book3)
        result = user.borrow(book4)
        self.assertFalse(result)
        self.assertEqual(len(user.get_borrowed_books()), 3)
    
    def test_user_return_book(self):
        user = User("Дементий")
        book = Book("Test Book", "Test Author", 2023)
        user.borrow(book)
        result = user.return_book(book)
        self.assertTrue(result)
        self.assertTrue(book.is_available())
        self.assertEqual(len(user.get_borrowed_books()), 0)


class TestLibrary(unittest.TestCase):
    
    def test_library_creation(self):
        lib = Library()
        self.assertIsNotNone(lib)
    
    def test_library_add_book(self):
        lib = Library()
        book = Book("Test Book", "Test Author", 2023)
        lib.add_book(book)
        found_book = lib.find_book("Test Book")
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.get_title(), "Test Book")
    
    def test_library_add_user(self):
        lib = Library()
        user = User("Дементий")
        lib.add_user(user)
        found_user = lib.find_user("Дементий")
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.name, "Дементий")
    
    def test_library_lend_book(self):
        lib = Library()
        book = Book("Test Book", "Test Author", 2023)
        user = User("Дементий")
        lib.add_book(book)
        lib.add_user(user)
        result = lib.lend_book("Test Book", "Дементий")
        self.assertTrue(result)
        self.assertFalse(book.is_available())
    
    def test_library_return_book(self):
        lib = Library()
        book = Book("Test Book", "Test Author", 2023)
        user = User("Дементий")
        lib.add_book(book)
        lib.add_user(user)
        lib.lend_book("Test Book", "Дементий")
        result = lib.return_book("Test Book", "Дементий")
        self.assertTrue(result)
        self.assertTrue(book.is_available())
    
    def test_library_remove_book(self):
        lib = Library()
        book = Book("Test Book", "Test Author", 2023)
        lib.add_book(book)
        result = lib.remove_book("Test Book")
        self.assertTrue(result)
        found_book = lib.find_book("Test Book")
        self.assertIsNone(found_book)
    
    def test_library_remove_book_when_borrowed(self):
        lib = Library()
        book = Book("Test Book", "Test Author", 2023)
        user = User("Дементий")
        lib.add_book(book)
        lib.add_user(user)
        lib.lend_book("Test Book", "Дементий")
        result = lib.remove_book("Test Book")
        self.assertFalse(result)


class TestLibrarian(unittest.TestCase):
    
    def test_librarian_add_book(self):
        lib = Library()
        librarian = Librarian("Мария")
        book = Book("Test Book", "Test Author", 2023)
        librarian.add_book(lib, book)
        found_book = lib.find_book("Test Book")
        self.assertIsNotNone(found_book)
    
    def test_librarian_register_user(self):
        lib = Library()
        librarian = Librarian("Мария")
        user = User("Дементий")
        librarian.register_user(lib, user)
        found_user = lib.find_user("Дементий")
        self.assertIsNotNone(found_user)


if __name__ == "__main__":
    unittest.main()
