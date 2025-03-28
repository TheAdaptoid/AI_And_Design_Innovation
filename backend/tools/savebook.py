import json
import os

FAVORITES_FILE = "user_favorites.json"

# Load user favorites from a JSON file.
def load_user_favorites():
    """
    Load user favorites from the JSON file.

    Returns:
        dict: A dictionary mapping user IDs to a list of favorite books.
              If the file doesn't exist or is invalid, returns an empty dictionary.
    """
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Save the updated favorites to the JSON file.
def save_user_favorites(favorites):
    """
    Save the updated favorites dictionary to the JSON file.

    Args:
        favorites (dict): A dictionary mapping user IDs to their list of favorite books.
    """
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)

# Add a book to the user's favorites.
def add_favorite(user_id, book):
    """
    Add a book to the user's favorites.

    This function assumes that the provided 'book' dictionary contains full details:
    "title", "author", "publisher", "year", and "description".

    Args:
        user_id (str): The identifier for the user.
        book (dict): A dictionary with the complete details of the book. Example:
                     {
                         "title": "The Great Gatsby",
                         "author": "F. Scott Fitzgerald",
                         "publisher": "Charles Scribner's Sons",
                         "year": 1925,
                         "description": "A novel about the American dream."
                     }

    Returns:
        str: A message indicating whether the book was added or if it already exists.
    """
    favorites = load_user_favorites()
    if user_id not in favorites:
        favorites[user_id] = []

    # Check if the book already exists in the user's favorites.
    if any(b["title"].lower() == book["title"].lower() and b["author"].lower() == book["author"].lower()
           for b in favorites[user_id]):
        return "Book already in favorites."

    favorites[user_id].append(book)
    save_user_favorites(favorites)
    return "Book added to favorites."

def get_user_favorites(user_id):
    """
    Retrieve the list of saved books for a specified user.

    Args:
        user_id (str): The identifier for the user.

    Returns:
        list: A list of dictionaries representing the user's favorite books.
              Returns an empty list if no books are saved.
    """
    favorites = load_user_favorites()
    return favorites.get(user_id, [])

# Example usage:
if __name__ == "__main__":
    user_id = "default"
    book_test = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Charles Scribner's Sons",
        "year": 1925,
        "description": "A novel about the American dream.",
    }

    # Save the book for the user
    result = add_favorite(user_id, book_test)
    print("Add Favorite Result:", result)

    # Retrieve the user's favorites
    saved_books = get_user_favorites(user_id)
    print("User's Favorites:", saved_books)
    print(json.dumps(saved_books, indent=1))  


