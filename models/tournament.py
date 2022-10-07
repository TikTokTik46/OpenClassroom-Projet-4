import shortuuid

class Tournament:
    """Modèle représentant un tournois."""

    def __init__(self, tournament_name, players_and_scores, round_number=4):
        """Initialise les détails relatifs à un tournois"""
        self.id = "T_" + shortuuid.uuid()
        self.tournament_name = tournament_name
        self.players_and_scores = players_and_scores
        self.round_number = round_number
        self.status = "In_progress"

    def serialize(self):
        """Used to return a dictionary of the instance attributes"""
        return {'id': self.id, 'tournament_name': self.tournament_name,
                'players': ";".join(list(self.players_and_scores.keys())),
                'scores': ";".join(str(score) for score in list(self.players_and_scores.values())),
                'round_number': self.round_number,
                'status': self.status}
