import shortuuid


class Tournament:
    """Model representing a tournament"""

    def __init__(self, tournament_name, players_and_scores, tournament_place,
                 tournament_date, time_control, description,
                 round_number=4):
        """Initialize attributes related to a tournament"""
        self.id = "T_" + shortuuid.uuid()
        self.tournament_name = tournament_name
        self.players_and_scores = players_and_scores
        self.round_number = round_number
        self.tournament_place = tournament_place
        self.tournament_date = tournament_date
        self.time_control = time_control
        self.description = description
        self.status = "In_progress"

    def serialize(self):
        """Transform a tournament object in a dictionary"""
        return {'id': self.id, 'tournament_name': self.tournament_name,
                'players': ";".join(list(self.players_and_scores.keys())),
                'scores': ";".join(str(score)
                                   for score in
                                   list(self.players_and_scores.values())),
                'round_number': self.round_number, 'status': self.status,
                'tournament_place': self.tournament_place,
                'tournament_date': self.tournament_date,
                'time_control': self.time_control,
                'description': self.description}
