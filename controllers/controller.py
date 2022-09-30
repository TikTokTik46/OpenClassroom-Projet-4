from views.view import View
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from models.database import Database

class Controller:
    """Contrôleur principal."""

    def __init__(self, ):
        """Initialise le controleur"""
        self.db = Database("test")

    def new_tournament(self):
        """Créer un nouveau tournois"""
        input_new_tournament = View().new_tournament()
        players = []
        id_players = []
        for i in range(8):
            new_player = Controller().new_player()
            players.append(new_player.serialize())
        players = sorted(players, key=lambda d: d["rank"])
        for player in players:
            id_players.append(player["id"])
        tournament = Tournament(input_new_tournament[0], id_players, input_new_tournament[1])
        self.db.insert_db(tournament)
        round_1 = Controller().first_round_pair(tournament, self.db)
        View().match_result_rules()
        Controller().get_round_result(round_1)
        pass


    def new_player(self):
        """Créer un nouveau joueur"""
        input_new_player = View().new_player()
        player = Player(input_new_player[0], input_new_player[1])
        self.db.insert_db(player)
        return player

    def first_round_pair(self, tournament, db):
        """Créer les premiéres paire d'un tournois"""
        first_round = Round("Round 1", tournament.id)
        self.db.insert_db(first_round)
        for i in range(4):
            match = Match(tournament.players[i], tournament.players[i + 4], first_round.id, tournament.id)
            View().display_match_pair(match, db)
            self.db.insert_db(match)
        return first_round

    def get_round_result(self, round):
        round_matches = self.db.search_1("Match", "round_id", round.id)
        for match in round_matches:
            match_result = View().match_result(match)
            winners = Controller().set_winner(match_result)
            for winner in winners:
                print(winner["match_player"])
                print(self.db.search_1("Match", "id", match["id"])[0][winner["match_player"]])
                print(winner["score"])
                self.db.modify_db("Player", "id", self.db.search_1("Match", "id", match["id"])[0][winner["match_player"]], "score", winner["score"])

    def set_winner(self, match_result):
        winner_codex = {0: [{"match_player": "player_one", "score": 0.5}, {"match_player": "player_two", "score": 0.5}],
                        1: [{"match_player": "player_one", "score": 1}],
                        2: [{"match_player": "player_two", "score": 1}]}
        winners = winner_codex[match_result]
        return winners
