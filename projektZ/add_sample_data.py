import sqlite3
from datetime import datetime

def add_books():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    sample_books = [
        ('Wichrowe Wzgórza', 'Emily Brontë', 'Romans', 'powieść', 'Klasyczna powieść o nieszczęśliwej miłości i zemście', '1847-12-01', 4.5),
        ('Duma i uprzedzenie', 'Jane Austen', 'Romans', 'powieść', 'Historia miłosna z konfliktami społecznymi i rodzinami', '1813-01-28', 4.8),
        ('Władca Pierścieni', 'J.R.R. Tolkien', 'Fantastyka i Science Fiction', 'epos', 'Epicka opowieść o walce dobra ze złem w Śródziemiu', '1954-07-29', 4.9),
        ('Diuna', 'Frank Herbert', 'Fantastyka i Science Fiction', 'epos', 'Sagi o polityce, religii i walce o zasoby na pustynnej planecie', '1965-08-01', 4.7),
        ('Zbrodnia i kara', 'Fiodor Dostojewski', 'Powieść historyczna', 'powieść', 'Głęboka analiza psychologiczna popełnienia zbrodni', '1866-01-01', 4.6),
        ('Imię róży', 'Umberto Eco', 'Powieść historyczna', 'powieść', 'Średniowieczna zagadka kryminalna w klasztorze benedyktyńskim', '1980-01-01', 4.4),
        ('Lśnienie', 'Stephen King', 'Horror', 'powieść', 'Historia o nawiedzonym hotelu i szaleństwie', '1977-01-28', 4.3),
        ('Dracula', 'Bram Stoker', 'Horror', 'powieść', 'Klasyczna powieść o wampirze Draculi', '1897-05-26', 4.2),
        ('Morderstwo w Orient Expressie', 'Agatha Christie', 'Kryminał i Thriller', 'powieść', 'Kryminalna zagadka na pokładzie luksusowego pociągu', '1934-01-01', 4.8),
        ('Dziewczyna z pociągu', 'Paula Hawkins', 'Kryminał i Thriller', 'powieść', 'Thriller psychologiczny o obserwowaniu obcych i tajemnicach', '2015-01-13', 4.1),
        ('Dziennik Anne Frank', 'Anne Frank', 'Biografia i reportaż', 'dziennik', 'Pamiętnik żydowskiej dziewczyny ukrywającej się podczas II wojny światowej', '1947-01-01', 4.9),
        ('Steve Jobs', 'Walter Isaacson', 'Biografia i reportaż', 'biografia', 'Kompleksowa biografia współzałożyciela Apple', '2011-01-01', 4.7),
        ('Harry Potter i Kamień Filozoficzny', 'J.K. Rowling', 'Książki dla młodzieży', 'powieść', 'Pierwsza część przygód młodego czarodzieja Harry\'ego Pottera', '1997-06-26', 4.9),
        ('Percy Jackson i Bogowie Olimpijscy', 'Rick Riordan', 'Książki dla młodzieży', 'powieść', 'Przygody młodego półboga w świecie mitologii greckiej', '2005-01-01', 4.8),
        ('Mały Książę', 'Antoine de Saint-Exupéry', 'Bajka', 'bajka', 'Filozoficzna opowieść o małym chłopcu z innej planety', '1943-04-06', 4.8),
        ('Królowa Śniegu', 'Hans Christian Andersen', 'Bajka', 'bajka', 'Klasyczna baśń o przyjaźni i odwadze', '1844-12-21', 4.6),
        ('Odyseja', 'Homer', 'Ballada', 'epos', 'Epicka opowieść o podróży Odyseusza', '800 p.n.e.', 4.7),
        ('Iliada', 'Homer', 'Ballada', 'epos', 'Epicka opowieść o wojnie trojańskiej', '800 p.n.e.', 4.6),
        ('Odyseja', 'Homer', 'Poemat', 'epos', 'Epicka opowieść o podróży Odyseusza', '800 p.n.e.', 4.7),
        ('Iliada', 'Homer', 'Poemat', 'epos', 'Epicka opowieść o wojnie trojańskiej', '800 p.n.e.', 4.6),
        ('Dziennik Bridget Jones', 'Helen Fielding', 'Dziennik', 'dziennik', 'Zabawna i wzruszająca opowieść o życiu singielki', '1996-02-01', 4.3),
        ('Dziennik Anne Frank', 'Anne Frank', 'Dziennik', 'dziennik', 'Pamiętnik żydowskiej dziewczyny ukrywającej się podczas II wojny światowej', '1947-01-01', 4.9),
        ('Liryki lozańskie', 'Adam Mickiewicz', 'Elegia', 'poezja', 'Zbiór wierszy i elegii Mickiewicza', '1839-01-01', 4.6),
        ('Treny', 'Jan Kochanowski', 'Elegia', 'poezja', 'Cykl 19 trenów poświęconych zmarłej córce', '1580-01-01', 4.8),
        ('Eneida', 'Wergiliusz', 'Epos', 'epos', 'Epicka opowieść o losach Eneasza', '29 p.n.e.', 4.6),
        ('Odyseja', 'Homer', 'Epos', 'epos', 'Epicka opowieść o podróży Odyseusza', '800 p.n.e.', 4.7),
        ('Próby', 'Michel de Montaigne', 'Esej', 'esej', 'Zbiór esejów filozoficznych Montaigne\'a', '1580-01-01', 4.4),
        ('Notatki z podziemia', 'Fiodor Dostojewski', 'Esej', 'esej', 'Refleksje nad ludzką naturą', '1864-01-01', 4.5),
        ('Fraszki', 'Jan Kochanowski', 'Fraszka', 'fraszka', 'Zbiór krótkich utworów literackich', '1584-01-01', 4.3),
        ('Epigramy', 'Marek Waleriusz Marcjalis', 'Fraszka', 'fraszka', 'Zbiór epigramów rzymskiego poety', '86-103', 4.4),
        ('Kazania sejmowe', 'Piotr Skarga', 'Kazanie', 'kazanie', 'Kazania wygłoszone na sejmie', '1597-01-01', 4.3),
        ('Kazania niedzielne', 'John Wesley', 'Kazanie', 'kazanie', 'Zbiór kazań na niedziele', '1778-01-01', 4.2),
        ('Listy do Felicji', 'Stanisław Ignacy Witkiewicz', 'List', 'list', 'Listy do Felicji, kochanki Witkacego', '1934-01-01', 4.4),
        ('Listy do Matki', 'Fryderyk Chopin', 'List', 'list', 'Listy do matki Fryderyka Chopina', '1831-01-01', 4.5),
        ('Odyseja', 'Homer', 'Oda', 'epos', 'Epicka opowieść o podróży Odyseusza', '800 p.n.e.', 4.7),
        ('Iliada', 'Homer', 'Oda', 'epos', 'Epicka opowieść o wojnie trojańskiej', '800 p.n.e.', 4.6),
        ('Opowiadania', 'Isaac Bashevis Singer', 'Opowiadanie', 'opowiadanie', 'Zbiór opowiadań Singera', '1971-01-01', 4.5),
        ('Sanatorium pod Klepsydrą', 'Bruno Schulz', 'Opowiadanie', 'opowiadanie', 'Zbiór opowiadań Schulza', '1933-01-01', 4.6),
        ('Pan Tadeusz', 'Adam Mickiewicz', 'Pieśń', 'poemat', 'Epopeja narodowa', '1834-01-01', 4.8),
        ('Sonety krymskie', 'Adam Mickiewicz', 'Pieśń', 'poemat', 'Zbiór sonetów inspirowanych podróżą na Krym', '1826-01-01', 4.7),
        ('Psalm 23', 'Dawid', 'Psalm', 'psalm', 'Psalm Dawida', '1000 p.n.e.', 4.9),
        ('Psalm 91', 'Dawid', 'Psalm', 'psalm', 'Psalm Dawida', '1000 p.n.e.', 4.8),
        ('Satyry', 'Ignacy Krasicki', 'Satyra', 'satyra', 'Zbiór satyr Krasickiego', '1779-01-01', 4.6),
        ('Satyry', 'Horacy', 'Satyra', 'satyra', 'Zbiór satyr Horacego', '35 p.n.e.', 4.7),
        ('Pieśń nad pieśniami', 'Salomon', 'Sielanka', 'sielanka', 'Biblijna pieśń miłosna', '900 p.n.e.', 4.8),
        ('Anakreontyki', 'Anakreont', 'Sielanka', 'sielanka', 'Zbiór sielanek Anakreonta', '500 p.n.e.', 4.5),
        ('Sonety do Laury', 'Petrarka', 'Sonet', 'sonet', 'Zbiór sonetów miłosnych', '1374-01-01', 4.8),
        ('Sonety krymskie', 'Adam Mickiewicz', 'Sonet', 'sonet', 'Zbiór sonetów inspirowanych podróżą na Krym', '1826-01-01', 4.7),
        ('Pamiętniki', 'Juliusz Cezar', 'Pamiętnik', 'pamiętnik', 'Zapisy działań wojennych Cezara', '50 p.n.e.', 4.6),
        ('Dziennik Anne Frank', 'Anne Frank', 'Pamiętnik', 'pamiętnik', 'Pamiętnik żydowskiej dziewczyny ukrywającej się podczas II wojny światowej', '1947-01-01', 4.9),
        ('Treny', 'Jan Kochanowski', 'Tren', 'tren', 'Cykl 19 trenów poświęconych zmarłej córce', '1580-01-01', 4.8),
        ('Epitafium', 'Szekspir', 'Tren', 'tren', 'Zbiór epitafiów', '1609-01-01', 4.7),
        ('Hymn do miłości', 'Św. Paweł', 'Hymn', 'hymn', 'Hymn o miłości', '50 n.e.', 4.9),
        ('Hymny', 'Kasjan Sakowicz', 'Hymn', 'hymn', 'Zbiór hymnów', '1642-01-01', 4.5)
    ]

    for book in sample_books:
        c.execute('''
            INSERT INTO books (title, author, genre, category, description, publish_date, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', book)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_books()
    print("Books added successfully.")
