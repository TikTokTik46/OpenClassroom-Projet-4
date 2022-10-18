import shortuuid


class Round:
    """Model representing a round of a match"""

    def __init__(self, round_name, tournament_id):
        """Initialize attributes related to a round"""
        self.round_name = round_name
        self.tournament_id = tournament_id
        self.id = "R_" + shortuuid.uuid()

    def serialize(self):
        """Transform a round object in a dictionary"""
        return {"id": self.id, "round_name": self.round_name,
                "tournament_id": self.tournament_id}
