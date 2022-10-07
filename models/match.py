import shortuuid


class Match:
    """Modèle représentant un match"""

    def __init__(self, player_one, player_two, round_id, tournament_id):
        """Initialise les détails relatifs à un match"""
        self.player_one = player_one
        self.player_two = player_two
        self.round_id = round_id
        self.result = -1
        self.tournament_id = tournament_id
        self.id = "M_" + shortuuid.uuid()

    def __str__(self):
        """Used in print."""
        player_one_name = self.player_one["name"]
        player_two_name = self.player_two["name"]
        return f"Tournois n° {self.tournament_id} - {self.round_id}, match n°{self.id} : {player_one_name} " \
               f"contre {player_two_name} "

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        return {"id": self.id, "player_one": self.player_one, "player_two": self.player_two, "result": self.result,
                "tournament_id": self.tournament_id, "round_id": self.round_id}
