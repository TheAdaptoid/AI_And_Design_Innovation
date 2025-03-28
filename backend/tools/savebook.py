import json
import os

FAVORITES_FILE = "user_favorites.json"

# Load user favorites from a JSON file.
def load_user_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Save the updated favorites to the JSON file.
def save_user_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)

# Add a book to the user's favorites.
def add_favorite(user_id, book):
    favorites = load_user_favorites()
    if user_id not in favorites:
        favorites[user_id] = []

    if any(b["title"].lower() == book["title"].lower() and b["author"].lower() == book["author"].lower()
           for b in favorites[user_id]):
        return "Book already in favorites."

    favorites[user_id].append(book)
    save_user_favorites(favorites)
    return "Book added to favorites."

# Retrieves saved books for the specified user.
def get_user_favorites(user_id):
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


