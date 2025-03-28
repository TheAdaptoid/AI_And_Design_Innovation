import random
from dataclasses import dataclass
from typing import List

@dataclass
class Location:
    """
    Represents a location of a library branch.

    Attributes:
        branch: The name of the library branch.
        address: The address of the library branch.
    """
    branch: str
    address: str

class LocationProvider:
    """
    Provides a random location from a list of library branches.

    Attributes:
        locations: A list of Location objects.
    """
    def __init__(self):
        """
        Initializes the LocationProvider with a list of locations.
        """
        self.locations = [
            Location(branch="Main Library", address="303 N. Laura St., Jacksonville, FL 32202"),
            Location(branch="Argyle Branch", address="7973 Old Middleburg Road S, Jacksonville, FL 32222"),
            Location(branch="Beaches Branch", address="600 3rd Street, Neptune Beach, FL 32266"),
            Location(branch="Bill Brinton Murray Hill Branch", address="918 Edgewood Avenue South, Jacksonville, FL 32205"),
            Location(branch="Bradham and Brooks Branch", address="1755 Edgewood Avenue W, Jacksonville, FL 32208"),
            Location(branch="Brentwood Branch", address="3725 Pearl Street, Jacksonville, FL 32206"),
            Location(branch="Brown Eastside Branch", address="1390 Harrison Street, Jacksonville, FL 32206"),
            Location(branch="Charles Webb Wesconnett Regional", address="6887 103rd Street, Jacksonville, FL 32210"),
            Location(branch="Dallas Graham Branch", address="2304 Myrtle Avenue N, Jacksonville, FL 32209"),
            Location(branch="Highlands Regional", address="1826 Dunn Avenue, Jacksonville, FL 32218")
        ]
        
    def get_random_location(self) -> Location:
        """
        Returns a random location from the list of locations.
        """
        return random.choice(self.locations)
    
if __name__ == "__main__":
    provider = LocationProvider()
    random_location = provider.get_random_location()
    print(f"Branch: {random_location.branch}, Address: {random_location.address}")
