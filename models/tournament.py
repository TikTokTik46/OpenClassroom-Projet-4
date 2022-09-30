import shortuuid

class Tournament:
    """Modèle représentant un tournois."""

    def __init__(self, tournament_name, players, round_number=4):
        """Initialise les détails relatifs à un tournois"""
        self.tournament_name = tournament_name
        self.players = players
        self.round_number = round_number
        self.id = "T_" + shortuuid.uuid()

    def serialize(self):
        """Used to return a dictionary of the instance attributes"""
        return {'id': self.id, 'tournament_name': self.tournament_name,
                'players': self.players, 'round_number': self.round_number}
