class View:
    """User interface management model"""

    @staticmethod
    def welcome_interface():
        """Welcome interface"""
        print("\n Bienvenue dans le gestionnaire de Tournoi Suisse !")
        pass

    @staticmethod
    def main_menu():
        """Main menu interface"""
        print("\n - Menu principale -\n"
              "\n"
              "0 : Créer un nouveau joueur\n"
              "1 : Créer un nouveau tournois\n"
              "2 : Reprendre un tournois\n"
              "3 : Rapports")
        choice = int(input())
        if choice in (0, 1, 2, 3):
            return choice
        print("Veuillez entrer une valeure entre 0 et 3.")
        return View().main_menu()

    @staticmethod
    def new_player():
        """New player creation interface"""
        print("\n - Création d'un nouveau joueur - \n")
        first_name = input("Prenom : ")
        last_name = input("Nom : ")
        birth_date = input("Date de naissance : ")
        gender = input("Sexe : ")
        rank = input("Rang : ")
        return first_name, last_name, birth_date, gender, rank

    @staticmethod
    def new_tournament(players_info):
        """Interface for creating a new tournament"""
        print("\n - Création d'un nouveau tournois - \n ")
        tournament_name = input("Nom du tournois : ")
        round_number = View.round_number()
        tournament_place = input("Lieu : ")
        tournament_date = input("Date : ")
        description = input("Description / Remarques : ")
        time_control = View.time_control()
        players_and_scores = {}
        player_list_number = 1
        print("|Liste des joueurs présent dans la base de donnée|")
        for player in players_info:
            print(f"n°{player_list_number:02d} - Nom : "
                  + player["name"].ljust(30, ' ') + " | ID : " + player["id"])
            player_list_number += 1
        players_selection = []
        while len(players_selection) != 8:
            players_selection = input("Choisir les 8 joueurs participant "
                                      "en entrant leur numéro suivi d'un"
                                      " point virgule :").split(";")
        for player_chosen in players_selection:
            players_and_scores[players_info[int(player_chosen) - 1]["id"]] =\
                0.0
        print("Voulez vous lancer le tournois maintenant ?")
        print("Oui (o) ou Non (n) ?")
        return tournament_name, round_number, players_and_scores,\
            tournament_place, tournament_date, time_control, description

    @staticmethod
    def time_control():
        time_control_list = ["Bullet", "Blitz", "Coup rapide"]
        choice = int(input("Contrôle du temps : \n"
                           "0 : Bullet\n"
                           "1 : Blitz\n"
                           "2 : Coup rapide\n"))
        if choice in [0, 1, 2]:
            return time_control_list[choice]
        return View.time_control()

    @staticmethod
    def round_number():
        """Interface to choose the number of rounds"""
        round_number = int(input("Nombre de round (entre 2 et 4) : "))
        if round_number in (2, 3, 4):
            return round_number
        return View.round_number()

    @staticmethod
    def player_list(players_info):
        """Interface to display all the players stored in the database"""
        print("\n|Information sur les joueurs présent"
              " dans la base de donnée|\n")
        for player in players_info:
            print("Prénom : " + player["first_name"].ljust(20, ' ') +
                  "| Nom : " + player["last_name"].ljust(20, ' ') +
                  "| Date de naissance : " +
                  player["birth_date"].ljust(20, ' ') +
                  "| Sexe : " + player["gender"].ljust(20, ' ') +
                  "| ID : " + player["id"].ljust(35, ' ') +
                  "| Rang : " + player["rank"])

    @staticmethod
    def run_tournament(tournament):
        """Interface to ask if the user want to start the tournament now"""
        answer = input()
        if answer == "o":
            return True
        if answer == "n":
            return False
        print("Veuillez répondre par la lettre o pour Oui ou n pour Non")
        return View().run_tournament(tournament)

    @staticmethod
    def reload_tournament(tournaments_info_db):
        """Interface to display and choose an existing tournament"""
        tournament_list_number = 1
        print("|Liste des tournois en cours dans la base de donnée|")
        tournament_to_load = []  # permet de récupérer les tournois qui ne sont
        # pas terminé
        for tournament_info in tournaments_info_db:
            if tournament_info["status"] == "In_progress":
                print(f"n°{tournament_list_number:02d} - Nom : "
                      + tournament_info["tournament_name"] + " | ID : " +
                      tournament_info["id"])
                tournament_to_load.append(tournament_info)
                tournament_list_number += 1
            pass
        if tournament_list_number == 1:
            print("\n Oups ! Aucun tournois en cours dans la base de donnée !")
            return False
        tournament_selection = int(input("Choisir le tournois en entrant"
                                         " son numéro :")) - 1
        return tournament_to_load[tournament_selection]

    @staticmethod
    def display_match_pair(match, db):
        """Interface to display the pair of players of a match"""
        player_one_name = \
            db.search("Player", "id", match.player_one)[0]["name"]
        player_two_name = \
            db.search("Player", "id", match.player_two)[0]["name"]
        print(f"ID Match {match.id} - : Joueur 1 -> {player_one_name} "
              f"contre Joueur 2 -> {player_two_name}")

    @staticmethod
    def new_round_info(round_, tournament):
        """Interface to display the round information"""
        print(f"\n"
              f"{round_.round_name} - Tournois : {tournament.tournament_name}"
              f"\n")

    @staticmethod
    def match_result_rules():
        """Display the rules to register the results"""
        print("Régles pour enregistrer les résultats : \n"
              "0 : Match nul\n"
              "1 : Victoire Joueur 1\n"
              "2 : Victoire Joueur 2\n")

    @staticmethod
    def match_result(match):
        """Interface to save the result of a match"""
        short_match_id = match.id[:5] + "..."
        result = int(input(f"Gagnant du match {short_match_id} : "))
        if result in (0, 1, 2):
            return result
        print("Résultat inccorect, veuillez vous référer"
              " aux régles ci-dessous.")
        View().match_result_rules()
        return View().match_result(match)

    @staticmethod
    def winner_score(winner_name, point, winner_score):
        """Display the score of the winning player"""
        print(f"Le joueur {winner_name} à gagné {point} point. Score total"
              f" sur le tournois : {winner_score} points")

    @staticmethod
    def report_selection():
        """Interface to select the type of report"""
        print("\n|Liste des rapports|\n"
              "0 : Liste des joueurs\n"
              "1 : Liste des joueurs d'un tournoi\n"
              "2 : Liste des tournois\n"
              "3 : Liste des tours d'un tournoi\n"
              "4 : Liste des matchs d'un tournoi\n")
        report_selection = int(input("Choisir le rapport souhaité"
                                     " en entrant son numéro :"))
        return report_selection

    @staticmethod
    def report_sorting_method_selection():
        """Interface to ask the sorting method"""
        print("\n"
              "0 : Par ordre alphabétique\n"
              "1 : Par classement\n")
        report_sorting_method = int(input("Choisir le rapport souhaité"
                                          " en entrant son numéro :"))
        return report_sorting_method

    @staticmethod
    def tournament_selection(tournaments):
        """Interface to choose a tournament in the report section"""
        tournament_list_number = 1
        print("\n|Liste des tournois dans la base de donnée|\n")
        for tournament in tournaments:
            print(f"n°{tournament_list_number} - Nom : "
                  + tournament["tournament_name"].ljust(20, ' ') +
                  " | ID : " + tournament["id"])
            tournament_list_number += 1
        tournament_selection = int(input("\nChoisir le tournois "
                                         "souhaité en entrant son numéro :"))
        return tournaments[tournament_selection - 1]

    @staticmethod
    def tournaments_report(tournaments):
        """Display the report of the tournaments in the database"""
        print("\n|Liste des tournois dans la base de donnée|\n")
        for tournament in tournaments:
            print("Nom : " + tournament["tournament_name"].ljust(25, ' ') +
                  " | Lieu : " + tournament["tournament_place"].ljust(15, ' ') +
                  " | Date : " + tournament["tournament_date"].ljust(15, ' ') +
                  " | Contrôle du temps : " + tournament["time_control"].ljust(15, ' ') +
                  " | Status : " + tournament["status"].ljust(15, ' ') +
                  " | ID : " + tournament["id"] +
                  "\nDescription : " + tournament["description"] + "\n")

    @staticmethod
    def rounds_report(rounds, tournament_name):
        """Display the report of rounds of a tournament in the database"""
        print(f"\n|Liste des rounds du tournois -> {tournament_name}|\n")
        for round_ in rounds:
            print("Nom : " + round_["round_name"].ljust(20, ' ')
                  + " | ID : " + round_["id"])

    @staticmethod
    def matchs_report(matchs, tournament_name, db):
        """Display the report of matchs of a tournament in the database"""
        print(f"\n|Liste des matchs du tournois -> {tournament_name}|")
        for match in matchs:
            player_one_name = db.search("Player", "id", match["player_one"])[0]["name"]
            player_two_name = db.search("Player", "id", match["player_two"])[0]["name"]
            round_name = db.search("Round", "id", match["round_id"])[0]["round_name"]
            result_sentence = ""
            if match["result"] == 0:
                result_sentence = "Egalitée"
            if match["result"] == 1:
                result_sentence = "Le joueur 1 à remporté le match"
            if match["result"] == 2:
                result_sentence = "Le joueur 2 à remporté le match"
            print("ID du match : " + match["id"].ljust(20, ' ') +
                  " | Nom du round : " + round_name.ljust(20, ' ') +
                  " | Joueur 1 : " + player_one_name.ljust(20, ' ') +
                  " | Joueur 2 : " + player_two_name.ljust(20, ' ') +
                  " | Résultat : " + result_sentence)

    @staticmethod
    def tournament_final_report(tournament, db):
        """Display the final ranking of players at the end of a tournament"""
        print(f"\n|Fin du Tournois - {tournament.tournament_name} - |")
        print("\n|Résultats du tournois|\n")
        ranking = 1
        for k, v in sorted(tournament.players_and_scores.items(),
                           key=lambda x: x[1], reverse=True):
            player_name = db.search("Player", "id", k)[0]["name"]
            print(str(ranking) + f" - {player_name}".ljust(20, ' ') + f" | Score final : {v}")
            ranking += 1
