import shortuuid


class Round:
    """Modèle représentant un tour d'un match."""

    def __init__(self, round_name, tournament_id):
        """Initialise les détails relatifs à un tour"""
        self.round_name = round_name
        self.tournament_id = tournament_id
        self.id = "R_" + shortuuid.uuid()

    def serialize(self):
        return {"id": self.id, "round_name": self.round_name, "tournament_id": self.tournament_id}
