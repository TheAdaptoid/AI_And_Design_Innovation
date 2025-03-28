from datetime import datetime, timedelta

def check_out_book(title):
    print(title + " checked out")

def renew_book(title):
    new_expiration = datetime.now() + timedelta(days=30)
    formatted_date = new_expiration.strftime("%Y-%m-%d")
    print(f"{title} renewed, expires on {formatted_date}")
