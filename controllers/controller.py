from models.player import Player
from views.view import View
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from models.database import Database


class Controller:
    """Controller model"""

    def __init__(self):
        """Initialize attributes related to the controller"""
        self.db = Database("data_base")

    @staticmethod
    def load_interface():
        """Launch the welcome interface and the main menu"""
        View().welcome_interface()
        Controller().main_menu()

    @staticmethod
    def main_menu():
        """Launch the main menu interface and directs to the method
        corresponding to the user choice"""
        choice = View().main_menu()
        if choice == 0:
            Controller().new_player()
        if choice == 1:
            Controller().new_tournament()
        if choice == 2:
            Controller().reload_tournament()
        if choice == 3:
            Controller().report_displayer()

    @staticmethod
    def report_displayer():
        """Launch the report interface and directs to the method
        corresponding to the user choice"""
        selection = View().report_selection()
        if selection == 0:
            Controller().all_players_report()
        if selection == 1:
            Controller().tournament_players_report()
        if selection == 2:
            Controller().tournaments_report()
        if selection == 3:
            Controller().rounds_report()
        if selection == 4:
            Controller().matchs_report()

    def all_players_report(self):
        """Launch the player report then return to the main menu"""
        players_info = self.db.info_table("Player")
        Controller().players_report(players_info)
        Controller().main_menu()

    def tournament_players_report(self):
        """Launch the tournament players report then return to the
        main menu"""
        tournaments = self.db.info_table("Tournament")
        players_info = self.db.info_table("Player")
        tournament = View().tournament_selection(tournaments)
        tournaments_deserialized = Controller().deserialize_tournament(tournament)
        players_id = list(tournaments_deserialized.players_and_scores.keys())
        tournament_players_info = []
        for player_info in players_info:
            if player_info["id"] in players_id:
                tournament_players_info.append(player_info)
        Controller().players_report(tournament_players_info)
        Controller().main_menu()

    def tournaments_report(self):
        """Launch tournaments report then return to the main menu"""
        tournaments = self.db.info_table("Tournament")
        View().tournaments_report(tournaments)
        Controller().main_menu()

    def rounds_report(self):
        """Launch rounds of a tournament report then return to the main menu"""
        tournaments = self.db.info_table("Tournament")
        tournament = View().tournament_selection(tournaments)
        tournament_rounds = self.db.search("Round", "tournament_id", tournament["id"])
        View().rounds_report(tournament_rounds, tournament["tournament_name"])
        Controller().main_menu()

    def matchs_report(self):
        """Launch matchs of a tournament report then return to the main menu"""
        tournaments = self.db.info_table("Tournament")
        tournament = View().tournament_selection(tournaments)
        tournament_matchs = self.db.search("Match", "tournament_id", tournament["id"])
        View().matchs_report(tournament_matchs, tournament["tournament_name"], self.db)
        Controller().main_menu()

    @staticmethod
    def players_report(players_info):
        """Launch players report with a sorting method then return
        to the main menu"""
        sorting_method = View().report_sorting_method_selection()
        players_info_sorted = []
        if sorting_method == 0:
            players_info_sorted = \
                sorted(players_info, key=lambda d: (d["name"]))
        if sorting_method == 1:
            players_info_sorted = \
                sorted(players_info, key=lambda d: (int(d["rank"])))
        View().player_list(players_info_sorted)

    def new_tournament(self):
        """Create a new tournament"""
        players_info = self.db.info_table("Player")
        players_info_sorted_by_name = sorted(players_info, key=lambda d: (d["name"]))
        input_new_tournament = View().new_tournament(players_info_sorted_by_name)
        tournament = Tournament(input_new_tournament[0],
                                input_new_tournament[2],
                                input_new_tournament[3],
                                input_new_tournament[4],
                                input_new_tournament[5],
                                input_new_tournament[6])
        self.db.insert_db(tournament)
        if View().run_tournament(tournament):
            Controller().launch_tournament(tournament)
        Controller().main_menu()

    def reload_tournament(self):
        """Reload an existing tournament"""
        tournaments_info_db = self.db.info_table("Tournament")
        selected_tournament = View().reload_tournament(tournaments_info_db)
        if selected_tournament is not False:
            tournament = Controller().deserialize_tournament(selected_tournament)
            Controller().launch_tournament(tournament)
        Controller().main_menu()

    def launch_tournament(self, tournament):
        """Launch a tournament"""
        round_done = len(self.db.search("Round", "tournament_id", tournament.id))
        if round_done == 0:
            Controller().first_round(tournament, self.db)
            round_done = 1
        for round_ in range(tournament.round_number - round_done):
            Controller().next_round(tournament, round_ + round_done + 1, self.db)
        Controller().tournament_closing(tournament)

    def tournament_closing(self, tournament: Tournament):
        """Launch the tournament final report"""
        self.db.modify_db("Tournament", "id", tournament.id, "status", "Ended")
        View().tournament_final_report(tournament, self.db)

    def new_player(self):
        """Create a new player"""
        player_info = View().new_player()
        player = Player(player_info[0], player_info[1], player_info[2], player_info[3], player_info[4])
        self.db.insert_db(player)
        Controller().main_menu()
        pass

    def first_round(self, tournament: Tournament, db) -> Round:
        """Create the first pair of a tournament"""
        first_round = Round("Round 1", tournament.id)
        View().new_round_info(first_round, tournament)
        round_matches = []
        players_sorted = Controller().sorting_players_by_rank_and_score(tournament)
        for i in range(4):
            match = Match(players_sorted[i]["id"], players_sorted[i + 4]["id"],
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
        """Create the next pair of a tournament"""
        next_round = Round("Round " + str(round_number), tournament.id)
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

    @staticmethod
    def get_round_result(round_matches, tournament):
        """Create the next pair of a tournament"""
        View().match_result_rules()
        for match in round_matches:
            match.result = View().match_result(match)
            Controller().set_score(match, tournament)

    def sorting_players_by_rank_and_score(self, tournament) -> list:
        """Return a list of players from the database sorted by
        rank and score"""
        players_unsorted = []
        for player_id in list(tournament.players_and_scores.keys()):
            rank = self.db.search("Player", "id", player_id)[0]["rank"]
            score = tournament.players_and_scores[player_id]
            players_unsorted.append(
                {"id": player_id, "rank": rank, "score": score})
        players_sorted = sorted(players_unsorted, key=lambda d: (d["score"], d["rank"]), reverse=True)
        return players_sorted

    @staticmethod
    def next_round_pair_sorting_algorithm(players_sorted, previous_pair):
        """Algorithm that sort the players to create pairs regarding the
        previous round pairs and following the
        swiss system"""
        pairs_possible = Controller().pairs_possibilities(players_sorted,
                                                          previous_pair)
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

    @staticmethod
    def check_player_exist(list_matchs, match):
        """Verify if a match belong to a list of matchs, return true if
        it's the case"""
        for list_match in list_matchs:
            if match[0] == list_match[0] or match[0] == list_match[1] or \
                    match[1] == list_match[0] or match[1] == list_match[1]:
                return False
        return True

    @staticmethod
    def pairs_possibilities(players_sorted, previous_pair):
        """Give a list of pairs possible for the round that exclude the
        previous pairs of a tournament"""
        pairs_possible = []
        for player_one in range(len(players_sorted)):
            for player_two in range(player_one + 1, len(players_sorted)):
                if [players_sorted[player_one]["id"], players_sorted[player_two]["id"]] not in previous_pair:
                    pair_total_score = players_sorted[player_one]["score"] + players_sorted[player_two]["score"]
                    pairs_possible.append([players_sorted[player_one]["id"], players_sorted[player_two]["id"],
                                           pair_total_score])
        pairs_possible.sort(key=lambda d: (d[2]), reverse=True)
        return pairs_possible

    def tournament_previous_pair(self, tournament):
        """Give a list of all the previous pairs of a tournament"""
        previous_matches = self.db.search("Match", "tournament_id", tournament.id)
        previous_pair = []
        for previous_match in previous_matches:
            match_players = [previous_match["player_one"], previous_match["player_two"]]
            previous_pair.append(match_players)
        return previous_pair

    def set_score(self, match, tournament):
        """Display the score of a match and update the database with
        the new score"""
        winner_codex = {
            0: [{"winner_id": match.player_one, "score": 0.5},
                {"winner_id": match.player_two, "score": 0.5}],
            1: [{"winner_id": match.player_one, "score": 1.0}],
            2: [{"winner_id": match.player_two, "score": 1.0}]}
        winners = winner_codex[match.result]
        for winner in winners:
            player_db = self.db.search("Player", "id", winner["winner_id"])[0]
            tournament.players_and_scores[winner["winner_id"]] += winner["score"]
            View().winner_score(player_db["name"], winner["score"],
                                tournament.players_and_scores.get(winner["winner_id"]))
        return winners

    @staticmethod
    def deserialize_tournament(tournament_serialized):
        """Transform a dictionary of a tournament serialized
        in a tournament object"""
        players = tournament_serialized['players'].split(";")
        scores = list(map(lambda score: float(score), tournament_serialized['scores'].split(";")))
        players_and_scores = {}
        for i in range(len(players)):
            players_and_scores[players[i]] = scores[i]
        tournament_deserialized = \
            Tournament(tournament_serialized['tournament_name'],
                       players_and_scores,
                       tournament_serialized['tournament_place'],
                       tournament_serialized['tournament_date'],
                       tournament_serialized['time_control'],
                       tournament_serialized['description'])
        tournament_deserialized.id = tournament_serialized['id']
        return tournament_deserialized
