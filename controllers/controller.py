from models.player import Player
from views.view import View
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from models.database import Database

class Controller:
    """Contrôleur principal."""

    def __init__(self, ):
        """Initialise le controleur"""
        self.db = Database("test")

    def load_interface(self):
        View().welcome_interface()
        Controller().main_menu()

    def main_menu(self):
        choice = View().main_menu()
        if choice == 0:
            Controller().new_players()
        if choice == 1:
            Controller().new_tournament()
        if choice == 2:
            Controller().reload_tournament()
        if choice == 3:
            View().reports()


    def new_tournament(self):
        """Créer un nouveau tournois"""
        players_info = self.db.info_table("Player")
        players_info_sorted_by_name = sorted(players_info, key=lambda d: (d["name"]))
        input_new_tournament = View().new_tournament(players_info_sorted_by_name)
        tournament = Tournament(input_new_tournament[0], input_new_tournament[2],
                                input_new_tournament[1])
        self.db.insert_db(tournament)
        if View().run_tournament(tournament):
            Controller().load_tournament(tournament)
        Controller().main_menu()

    def reload_tournament(self):
        """Charger un tournois existant"""
        tournaments_info_db = self.db.info_table("Tournament")
        selected_tournament = View().reload_tournament(tournaments_info_db)
        tournament = Controller().deserialize_tournament(selected_tournament)
        Controller().load_tournament(tournament)
        Controller().main_menu()

    def load_tournament(self, tournament):
        """Lancer un tournois"""
        round_done = len(self.db.search_1("Round", "tournament_id", tournament.id))
        print(round_done)
        if round_done == 0:
            Controller().first_round(tournament, self.db)
        for round_ in range(tournament.round_number-round_done):
            Controller().next_round(tournament, round_ + round_done + 1, self.db)
        Controller().tournament_closing(tournament)


    def tournament_closing(self, tournament):
        self.db.modify_db("Tournament", "id", tournament.id, "status", "Ended")
        print("Le tournois est terminé !")


    def new_players(self):
        """Créer de nouveaux joueurs"""
        new_players = View().new_players()
        for new_player in new_players:
            player = Player(new_player[0], new_player[1])
            self.db.insert_db(player)
        Controller().main_menu()
        pass

    def first_round(self, tournament, db):
        """Créer les premiéres paire d'un tournois"""
        first_round = Round("Round 1", tournament.id)
        View().new_round_info(first_round, tournament)
        round_matches = []
        for i in range(4):
            match = Match(list(tournament.players_and_scores.keys())[i], list(tournament.players_and_scores.keys())[i+4],
                          first_round.id, tournament.id)
            View().display_match_pair(match, db)
            round_matches.append(match)
        Controller().get_round_result(round_matches, tournament)
        for match in round_matches:
            self.db.insert_db(match)
        self.db.insert_db(first_round)
        self.db.modify_db("Tournament", "id", tournament.id, "scores",
                          ";".join(str(score) for score in list(tournament.players_and_scores.values())))
        return first_round

    def next_round(self, tournament, round_number, db):
        next_round = Round("Round "+str(round_number), tournament.id)
        View().new_round_info(next_round, tournament)
        players_sorted = Controller().sorting_players_by_rank_and_score(tournament)
        previous_pair = Controller().tournament_previous_pair(tournament)
        round_pair = Controller().next_round_pair_sorting_algorithm(players_sorted, previous_pair)
        round_matches = []
        for round_ in round_pair:
            match = Match(round_[0], round_[1], next_round.id, tournament.id)
            View().display_match_pair(match, db)
            round_matches.append(match)
        Controller().get_round_result(round_matches, tournament)
        for match in round_matches:
            self.db.insert_db(match)
        self.db.insert_db(next_round)
        self.db.modify_db("Tournament", "id", tournament.id, "scores",
                          ";".join(str(score) for score in list(tournament.players_and_scores.values())))
        return next_round

    def get_round_result(self, round_matches, tournament):
        View().match_result_rules()
        for match in round_matches:
            match.result = View().match_result(match)
            Controller().set_score(match, tournament)

    def sorting_players_by_rank_and_score(self, tournament):
        players_unsorted = []
        for player_id in list(tournament.players_and_scores.keys()):
            rank = self.db.search_1(Player, "id", player_id)
            score = tournament.players_and_scores[player_id]
            players_unsorted.append({"id": player_id, "rank": rank, "score": score})
        players_sorted = sorted(players_unsorted, key=lambda d: (d["score"], d["rank"]), reverse=True)
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

    def pairs_possibilities(self, players_sorted, previous_pair):
        pairs_possible = []
        for player_one in range(len(players_sorted)):
            for player_two in range(player_one+1, len(players_sorted)):
                if [players_sorted[player_one]["id"], players_sorted[player_two]["id"]] not in previous_pair:
                    pair_total_score = players_sorted[player_one]["score"] + players_sorted[player_two]["score"]
                    pairs_possible.append([players_sorted[player_one]["id"], players_sorted[player_two]["id"],
                                           pair_total_score])
        pairs_possible.sort(key=lambda d: (d[2]), reverse=True)
        return pairs_possible

    def tournament_previous_pair(self, tournament):
        previous_matches = self.db.search_1("Match", "tournament_id", tournament.id)
        previous_pair = []
        for previous_match in previous_matches:
            match_players = [previous_match["player_one"], previous_match["player_two"]]
            previous_pair.append(match_players)
        return previous_pair

    def set_score(self, match, tournament):
        winner_codex = {0: [{"winner_id": match.player_one, "score": 0.5}, {"winner_id": match.player_two, "score": 0.5}],
                        1: [{"winner_id": match.player_one, "score": 1.0}],
                        2: [{"winner_id": match.player_two, "score": 1.0}]}
        winners = winner_codex[match.result]
        for winner in winners:
            player_db = self.db.search_1("Player", "id", winner["winner_id"])[0]
            tournament.players_and_scores[winner["winner_id"]] += winner["score"]
            View().winner_score(player_db["name"], winner["score"], tournament.players_and_scores.get(winner["winner_id"]))
        return winners


    def deserialize_tournament(self, tournament_serialized):
        players = tournament_serialized['players'].split(";")
        scores = list(map(lambda score: float(score), tournament_serialized['scores'].split(";")))
        players_and_scores = {}
        for i in range(len(players)):
            players_and_scores[players[i]] = scores[i]
        tournament_deserialized = Tournament(tournament_serialized['tournament_name'], players_and_scores,
                                             tournament_serialized['round_number'])
        tournament_deserialized.id = tournament_serialized['id']
        return tournament_deserialized

    def deserialize_player(self, player_serialized):
        players_deserialized = Player(player_serialized['name'],
                                      player_serialized['rank'])
        players_deserialized.id = player_serialized['id']
        return players_deserialized

    def deserialize_round(self, round_serialized):
        round_deserialized = Round(round_serialized['round_name'],
                                   round_serialized['tournament_id'])
        round_deserialized.id = round_serialized['id']
        return round_deserialized

    def deserialize_match(self, match_serialized):
        match_deserialized = Match(match_serialized['player_one'],
                                   match_serialized['player_two'],
                                   match_serialized['round_id'],
                                   match_serialized['tournament_id'])
        match_deserialized.result = match_serialized['result']
        match_deserialized.id = match_serialized['id']
        return match_deserialized

