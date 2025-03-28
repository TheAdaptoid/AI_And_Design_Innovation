from datetime import datetime, timedelta


def place_on_hold(title: str) -> str:
    """
    Place a book on hold.

    Args:
        title (str): The title of the book to place on hold.
    """
    return f"{title} placed on hold."


def renew_book(title: str) -> str:
    """
    Renew a book.

    Args:
        title (str): The title of the book to renew.
    """
    new_expiration = datetime.now() + timedelta(days=30)
    formatted_date = new_expiration.strftime("%Y-%m-%d")
    return f"{title} renewed, expires on {formatted_date}"
