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
        players = sorted(players, key=lambda d: d["rank"], reverse=True)
        for player in players:
            id_players.append(player["id"])
        tournament = Tournament(input_new_tournament[0], id_players, input_new_tournament[1])
        self.db.insert_db(tournament)
        round_1 = Controller().first_round_pair(tournament, self.db)
        View().match_result_rules()
        Controller().get_round_result(round_1)
        for round_ in range(tournament.round_number-1):
            next_round = Controller().next_round_pair(tournament, round_+2, self.db)
            Controller().get_round_result(next_round)


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

    def next_round_pair(self, tournament, round_number, db):
        next_round = Round("Round "+str(round_number), tournament.id)
        self.db.insert_db(next_round)
        players_sorted = Controller().sorting_players_by_rank_and_score(tournament)
        previous_pair = Controller().tournament_previous_pair(tournament)
        round_pair = Controller().next_round_pair_sorting_algorithm(players_sorted, previous_pair)
        for round_ in round_pair:
            match = Match(round_[0], round_[1], next_round.id, tournament.id)
            View().display_match_pair(match, db)
            self.db.insert_db(match)
        return next_round

    def sorting_players_by_rank_and_score(self, tournament):
        players_sorted = []
        for player in tournament.players:
            rank = self.db.search_value_with_id("Player", player, "rank")
            score = self.db.search_value_with_id("Player", player, "score")
            players_sorted.append({"player": player, "rank": rank, "score": score, "id": player})
        players_sorted = sorted(players_sorted, key=lambda d: (d["score"], d["rank"]), reverse=True)
        return players_sorted

    def next_round_pair_sorting_algorithm(self, players_sorted, previous_pair):
        pairs_possible = Controller().pairs_possibilities(players_sorted, previous_pair)
        next_round_pairs = []
        for i in range(len(pairs_possible)):
            if len(next_round_pairs) > 0:
                next_round_pairs.pop()
            next_round_pairs.append(pairs_possible[i])
            for j in range(i + 1, len(pairs_possible)):
                if len(next_round_pairs) > 1:
                    next_round_pairs.pop()
                if Controller().check_player_exist(next_round_pairs, pairs_possible[j]):
                    next_round_pairs.append(pairs_possible[j])
                    for k in range(j + 1, len(pairs_possible)):
                        if len(next_round_pairs) > 2:
                            next_round_pairs.pop()
                        if Controller().check_player_exist(next_round_pairs, pairs_possible[k]):
                            next_round_pairs.append(pairs_possible[k])
                            for m in range(k + 1, len(pairs_possible)):
                                if len(next_round_pairs) > 3:
                                    next_round_pairs.pop()
                                if Controller().check_player_exist(next_round_pairs, pairs_possible[m]):
                                    next_round_pairs.append(pairs_possible[m])
                                    return next_round_pairs
        return print("Pas de paires possible")

    def check_player_exist(self, list_matchs, match):
        for list_match in list_matchs:
            if match[0] == list_match[0] or match[0] == list_match[1] or match[1] == list_match[0] or match[1] == list_match[1]:
                return False
        return True

    def pairs_possibilities(self,players_sorted, previous_pair):
        pairs_possible = []
        for player_one in range(len(players_sorted)):
            for player_two in range(player_one+1, len(players_sorted)):
                if [players_sorted[player_one]["id"], players_sorted[player_two]["id"]] not in previous_pair:
                    pair_total_score = players_sorted[player_one]["score"] + players_sorted[player_one]["score"]
                    pairs_possible.append([players_sorted[player_one]["id"], players_sorted[player_two]["id"], pair_total_score])
        pairs_possible.sort(key=lambda d: (d[2]), reverse=True)
        return pairs_possible

    def tournament_previous_pair(self, tournament):
        previous_matches = self.db.search_1("Match", "tournament_id", tournament.id)
        previous_pair = []
        for previous_match in previous_matches:
            match_players = [previous_match["player_one"], previous_match["player_two"]]
            previous_pair.append(match_players)
        return previous_pair

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
