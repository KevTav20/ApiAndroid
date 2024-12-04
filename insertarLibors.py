import json
from sqlmodel import Session
from db import engine
from models import Book

# Lista de URLs
urls = [
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/Codigo%20limpio%20-%20Robert%20Cecil%20Martin.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/El-lenguaje-de-programacion-C-2-ed-kernighan-amp-ritchie.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/Introduction.to.Algorithms.4th.Leiserson.Stein.Rivest.Cormen.MIT.Press.9780262046305.EBooksWorld.ir.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/Practical%20UI%20Patterns%20for%20Design%20Systems.%20Fast-Track%20Interaction%20Design%20for%20a%20Seamless%20User%20Experience%20by%20Diana%20MacDonald%20(z-lib.org).pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/Sumergete%20en%20los%20patrones%20de%20dise%C3%B1o-Alexander%20Shvets.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/The%20Pragmatic%20Programmer.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/%5BJavaScript%20The%20Good%20Parts%201st%20Edition%20by%20Douglas%20Crockford%20-%202008%5D.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/book.pdf",
    "https://easyreadingbooks.sfo3.cdn.digitaloceanspaces.com/git%20github%20desde%20cero%202%C2%AA%20edici%C3%B3n.pdf"
]

# JSON con todos los libros
data = [
    {
        "author": "Harper Lee",
        "image": "https://m.media-amazon.com/images/I/81gepf1eMqL._SL1500_.jpg",
        "category": "Fiction",
        "title": "To Kill a Mockingbird",
        "year": "1960",
        "num_pages": 324,
        "id": 1,
        "synopsis": "Un clásico de la literatura estadounidense que aborda temas de justicia racial y la pérdida de la inocencia en el sur profundo a través de los ojos de Scout Finch."
    },
    {
        "author": "George Orwell",
        "image": "https://m.media-amazon.com/images/I/91jHOlKEPwL._SL1500_.jpg",
        "category": "Dystopian",
        "title": "1984",
        "year": "1949",
        "num_pages": 328,
        "id": 2,
        "synopsis": "Una novela distópica que explora un mundo totalitario bajo la vigilancia constante del Gran Hermano, donde el pensamiento libre es perseguido."
    },
    {
        "author": "Jane Austen",
        "image": "https://m.media-amazon.com/images/I/81WEdRhHhAL._SL1500_.jpg",
        "category": "Romance",
        "title": "Pride and Prejudice",
        "year": "1813",
        "num_pages": 279,
        "id": 3,
        "synopsis": "Una obra maestra del romance que sigue las vidas y los enredos amorosos de Elizabeth Bennet y Mr. Darcy en la Inglaterra del siglo XIX."
    },
    {
        "author": "F. Scott Fitzgerald",
        "image": "https://m.media-amazon.com/images/I/91TaDE-KbzL._SL1500_.jpg",
        "category": "Fiction",
        "title": "The Great Gatsby",
        "year": "1925",
        "num_pages": 180,
        "id": 4,
        "synopsis": "Una exploración de la decadencia de los años 20 en Estados Unidos, centrada en Jay Gatsby y su búsqueda del sueño americano."
    },
    {
        "author": "J.D. Salinger",
        "image": "https://m.media-amazon.com/images/I/8125BDk3l9L._SL1500_.jpg",
        "category": "Fiction",
        "title": "The Catcher in the Rye",
        "year": "1951",
        "num_pages": 214,
        "id": 5,
        "synopsis": "La historia de Holden Caulfield, un adolescente rebelde que lucha por encontrar su lugar en un mundo que considera superficial."
    },
    {
        "author": "Herman Melville",
        "image": "https://m.media-amazon.com/images/I/61PBBKyZ1rL._SL1360_.jpg",
        "category": "Adventure",
        "title": "Moby-Dick",
        "year": "1851",
        "num_pages": 585,
        "id": 6,
        "synopsis": "Una epopeya marina que narra la obsesiva búsqueda del capitán Ahab por cazar a la gigantesca ballena blanca, Moby Dick."
    },
    {
        "author": "Aldous Huxley",
        "image": "https://m.media-amazon.com/images/I/81fiJzvcB2L._SL1500_.jpg",
        "category": "Dystopian",
        "title": "Brave New World",
        "year": "1932",
        "num_pages": 268,
        "id": 8,
        "synopsis": "Un mundo futurista donde la felicidad es controlada por la ciencia y los individuos son condicionados desde el nacimiento."
    },
    {
        "author": "J.R.R. Tolkien",
        "image": "https://m.media-amazon.com/images/I/71S7Z+YhJFL._AC_UF1000,1000_QL80_.jpg",
        "category": "Fantasy",
        "title": "The Hobbit",
        "year": "1937",
        "num_pages": 310,
        "id": 9,
        "synopsis": "La emocionante aventura de Bilbo Bolsón, un hobbit que se embarca en una peligrosa búsqueda para recuperar un tesoro robado."
    },
    {
        "author": "Leo Tolstoy",
        "image": "https://m.media-amazon.com/images/I/91teiIZ5vwL._UF894,1000_QL80_.jpg",
        "category": "Historical Fiction",
        "title": "War and Peace",
        "year": "1869",
        "num_pages": 1225,
        "id": 10,
        "synopsis": "Una extensa narración que entrelaza la vida de varias familias rusas durante las guerras napoleónicas."
    },
    {
        "author": "J.R.R. Tolkien",
        "image": "https://m.media-amazon.com/images/I/81j4C6j3dRL._AC_UF1000,1000_QL80_.jpg",
        "category": "Fantasy",
        "title": "The Lord of the Rings",
        "year": "1954",
        "num_pages": 1178,
        "id": 12,
        "synopsis": "Un épico viaje para destruir el anillo único, liderado por Frodo Bolsón y un grupo de compañeros, enfrentando el mal de Sauron."
    },
    {
        "author": "Anne Frank",
        "image": "https://m.media-amazon.com/images/I/81bLPNVfJTL._UF1000,1000_QL80_.jpg",
        "category": "Biography",
        "title": "The Diary of a Young Girl",
        "year": "1947",
        "num_pages": 283,
        "id": 13,
        "synopsis": "El conmovedor diario de Anne Frank, una joven judía que se escondió durante la ocupación nazi en la Segunda Guerra Mundial."
    },
    {
        "author": "Ray Bradbury",
        "image": "https://m.media-amazon.com/images/I/61l8LHt4MeL._AC_UF1000,1000_QL80_.jpg",
        "category": "Dystopian",
        "title": "Fahrenheit 451",
        "year": "1953",
        "num_pages": 158,
        "id": 14,
        "synopsis": "Una sociedad futura donde los libros están prohibidos y los bomberos se dedican a quemarlos, explorando la lucha por el conocimiento."
    },
    {
        "author": "Oscar Wilde",
        "image": "https://m.media-amazon.com/images/I/71fm0Ap7JcL._AC_UF1000,1000_QL80_.jpg",
        "category": "Gothic Fiction",
        "title": "The Picture of Dorian Gray",
        "year": "1890",
        "num_pages": 254,
        "id": 15,
        "synopsis": "La fascinante historia de Dorian Gray, un joven cuya belleza permanece inalterable mientras su retrato envejece y revela su corrupción."
    },
    {
        "author": "Fyodor Dostoevsky",
        "image": "https://m.media-amazon.com/images/I/71OZJsgZzQL._AC_UF1000,1000_QL80_.jpg",
        "category": "Philosophical Fiction",
        "title": "The Brothers Karamazov",
        "year": "1880",
        "num_pages": 796,
        "id": 16,
        "synopsis": "Un profundo análisis de la fe, la moralidad y la dinámica familiar a través de los conflictos de los hermanos Karamazov."
    },
    {
        "author": "Fyodor Dostoevsky",
        "image": "https://m.media-amazon.com/images/I/41Xdvx45SFL._AC_UF1000,1000_QL80_.jpg",
        "category": "Psychological Fiction",
        "title": "Crime and Punishment",
        "year": "1866",
        "num_pages": 430,
        "id": 17,
        "synopsis": "Crimen y Castigo sigue a Rodion Raskólnikov, un joven que asesina a una usurera creyendo que sus acciones están justificadas. A lo largo de la novela, lucha con su culpa y su conciencia, enfrentándose a la redención y la moralidad. La obra explora temas como el sufrimiento, la justicia y la naturaleza humana."
    },
    {
        "author": "Paulo Coelho",
        "image": "https://m.media-amazon.com/images/I/81ioPZFMeUL._UF894,1000_QL80_.jpg",
        "category": "Fiction",
        "title": "The Alchemist",
        "year": "1988",
        "num_pages": 208,
        "id": 18,
        "synopsis": "Santiago, un joven pastor andaluz, sueña con un tesoro escondido en Egipto. Guiado por señales y su corazón, emprende un viaje lleno de desafíos y encuentros místicos, descubriendo que el verdadero tesoro yace en seguir sus sueños y entender su propósito en la vida."
    },
    {
        "author": "Stephen King",
        "image": "https://m.media-amazon.com/images/I/81nwnHTcV2L._AC_UF894,1000_QL80_.jpg",
        "category": "Horror",
        "title": "The Shining",
        "year": "1977",
        "num_pages": 447,
        "id": 19,
        "synopsis": "Jack Torrance, aspirante a escritor, acepta un trabajo como cuidador del Hotel Overlook durante el invierno. En el aislamiento, fuerzas sobrenaturales empiezan a influir en su mente, poniendo en peligro a su esposa e hijo, quien tiene un don especial llamado 'el resplandor'."
    },
    {
        "author": "Cormac McCarthy",
        "image": "https://m.media-amazon.com/images/I/817tOC36BUL.jpg",
        "category": "Post-apocalyptic",
        "title": "The Road",
        "year": "2006",
        "num_pages": 287,
        "id": 20,
        "synopsis": "En un mundo postapocalíptico, un padre y su hijo recorren un paisaje devastado en busca de esperanza y supervivencia. Su vínculo es lo único que les sostiene mientras enfrentan peligros constantes y la lucha por mantener su humanidad."
    },
    {
        "author": "Suzanne Collins",
        "image": "https://m.media-amazon.com/images/I/61I24wOsn8L._AC_UF1000,1000_QL80_.jpg",
        "category": "Dystopian Fiction",
        "title": "The Hunger Games",
        "year": "2008",
        "num_pages": 374,
        "id": 21,
        "synopsis": "Katniss Everdeen se ve obligada a participar en los Juegos del Hambre, una competencia mortal televisada en la que debe luchar por su vida contra otros tributos. Enfrentándose al Capitolio, Katniss se convierte en un símbolo de esperanza y rebelión."
    },
    {
        "author": "John Green",
        "image": "https://m.media-amazon.com/images/I/61fbVx3W5cL.jpg",
        "category": "Romance/Drama",
        "title": "The Fault in Our Stars",
        "year": "2012",
        "num_pages": 313,
        "id": 22,
        "synopsis": "Hazel Grace, una joven con cáncer terminal, encuentra el amor en Augustus Waters, un sobreviviente de cáncer. Juntos exploran el significado de la vida, el amor y la mortalidad, mientras enfrentan los desafíos de su enfermedad."
    }
]

# Agregar atributo 'url' a cada libro
for i, book in enumerate(data):
    book["url"] = urls[i % len(urls)]  # Asignar URLs cíclicamente

# Insertar libros en la base de datos
with Session(engine) as session:
    books = [
        Book(
            title=book["title"],
            author=book["author"],
            year=book["year"],
            category=book["category"],
            num_pages=book["num_pages"],
            image=book["image"],
            synopsis=book["synopsis"],
            url=book["url"]  # Nuevo atributo
        )
        for book in data
    ]
    session.add_all(books)
    session.commit()

print(f"{len(books)} books inserted successfully with URLs!")
