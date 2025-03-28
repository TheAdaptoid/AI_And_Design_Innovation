import random

from backend.types import Location


LOCATIONS: list[Location] = [
    Location(
        branch="Main Library",
        address="303 N. Laura St., Jacksonville, FL 32202",
    ),
    Location(
        branch="Argyle Branch",
        address="7973 Old Middleburg Road S, Jacksonville, FL 32222",
    ),
    Location(
        branch="Beaches Branch",
        address="600 3rd Street, Neptune Beach, FL 32266",
    ),
    Location(
        branch="Bill Brinton Murray Hill Branch",
        address="918 Edgewood Avenue South, Jacksonville, FL 32205",
    ),
    Location(
        branch="Bradham and Brooks Branch",
        address="1755 Edgewood Avenue W, Jacksonville, FL 32208",
    ),
    Location(
        branch="Brentwood Branch",
        address="3725 Pearl Street, Jacksonville, FL 32206",
    ),
    Location(
        branch="Brown Eastside Branch",
        address="1390 Harrison Street, Jacksonville, FL 32206",
    ),
    Location(
        branch="Charles Webb Wesconnett Regional",
        address="6887 103rd Street, Jacksonville, FL 32210",
    ),
    Location(
        branch="Dallas Graham Branch",
        address="2304 Myrtle Avenue N, Jacksonville, FL 32209",
    ),
    Location(
        branch="Highlands Regional",
        address="1826 Dunn Avenue, Jacksonville, FL 32218",
    ),
]


def locate_book(book_title: str) -> dict[str, str]:
    """
    Locate a book in the library.

    Args:
        book_title (str): The title of the book to locate.

    Returns:
        dict[str, str]: A dictionary containing the branch and address of the
            library where the book is located.
    """
    location = random.choice(LOCATIONS).to_dict()
    location.update({"book_title": book_title})
    return location
