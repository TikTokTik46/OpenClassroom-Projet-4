import shortuuid


class Player:
    """Model representing a player"""

    def __init__(self, first_name, last_name, birth_date, gender, rank):
        """Initialize attributes related to a player"""
        self.first_name = first_name
        self.last_name = last_name
        self.name = first_name + " " + last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.id = "P_" + shortuuid.uuid()

    def serialize(self):
        """Transform a player object in a dictionary"""
        return {'id': self.id, 'first_name': self.first_name,
                'last_name': self.last_name, 'name': self.name,
                'birth_date': self.birth_date, 'gender': self.gender,
                'rank': self.rank}
