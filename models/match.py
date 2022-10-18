import shortuuid


class Match:
    """Model representing a match"""

    def __init__(self, player_one, player_two, round_id, tournament_id):
        """Initialize attributes related to a match"""
        self.player_one = player_one
        self.player_two = player_two
        self.round_id = round_id
        self.result = -1
        self.tournament_id = tournament_id
        self.id = "M_" + shortuuid.uuid()

    def serialize(self):
        """Transform a match object in a dictionary"""
        return {"id": self.id, "player_one": self.player_one,
                "player_two": self.player_two, "result": self.result,
                "tournament_id": self.tournament_id, "round_id": self.round_id}
