class View:
    """Gestion de l'interface utilisateur"""

    def welcome_interface(self):
        print("\n Bienvenu dans le gestionnaire de Tournoi Suisse !")
        pass

    def main_menu(self):
        print("\n - Menu principale -\n"
              "\n"
              "0 : Créer de nouveaux joueurs\n"
              "1 : Créer un nouveau tournois\n"
              "2 : Reprendre un tournois\n"
              "3 : Rapports")
        choice = int(input())
        if choice in (0, 1, 2, 3):
            return choice
        print("Veuillez entrer une valeure entre 0 et 3.")
        return View().main_menu()

    def new_players(self):
        """Interface de création de nouveaux joueur"""
        print("\n - Création de nouveaux joueurs - \n")
        players_information = []
        players_input = input("Entrer le nom et le rang du joueur en les séparant par une virgule.\n"
                             "Pour plusieur joueurs rajouter un point virgule entre chaque joueur :").split(";")
        for player_input in players_input:
            players_information.append(player_input.split(","))
        return players_information

    def new_tournament(self, players_info):
        """Interface de création d'un nouveau tournois"""
        print("\n - Création d'un nouveau tournois - \n ")
        tournament_name = input("Nom du tournois : ")
        round_number = int(input("Nombre de round : "))
        players_and_scores = {}
        player_list_number = 1
        print("|Liste des joueurs présent dans la base de donnée|")
        for player in players_info:
            print(f"n°{player_list_number} - Nom : " + player["name"] + " | ID : " + player["id"])
            player_list_number += 1
        players_selection = input("Choisir les joueurs participant "
                                  "en entrant leur numéro suivi d'un point virgule :").split(";")
        for player_chosen in players_selection:
            players_and_scores[players_info[int(player_chosen)-1]["id"]] = 0.0
        print("Voulez vous lancer le tournois maintenant ?")
        print("Oui (o) ou Non (n) ?")
        return tournament_name, round_number, players_and_scores

    def run_tournament(self, tournament):
        answer = input()
        if answer == "o":
            return True
        if answer =="n":
            return False
        print("Veuillez répondre par la lettre o pour Oui ou n pour Non")
        return View().run_tournament(tournament)

    def reload_tournament(self, tournaments_info_db):
        tournament_list_number = 1
        print("|Liste des tournois en cours dans la base de donnée|")
        tournament_to_load =[] #permet de récupérer les tournois qui ne sont pas terminé
        for tournament_info in tournaments_info_db:
            if tournament_info["status"] == "In_progress":
                print(f"n°{tournament_list_number} - Nom : " + tournament_info["tournament_name"] + " | ID : " + tournament_info["id"])
                tournament_to_load.append(tournament_info)
                tournament_list_number += 1
            pass
        tournament_selection = int(input("Choisir le tournois en entrant son numéro :"))-1
        return tournament_to_load[tournament_selection]


    def display_match_pair(self, match, db):
        player_one_name = db.search_1("Player", "id", match.player_one)[0]["name"]
        player_two_name = db.search_1("Player", "id", match.player_two)[0]["name"]
        print(f"ID Match {match.id} - : Joueur 1 -> {player_one_name} contre Joueur 2 -> {player_two_name}")

    def new_round_info(self, round_, tournament):
        print(f"\n"
              f"{round_.round_name} - Tournois : {tournament.tournament_name}"
              f"\n")

    def match_result_rules(self):
        print("Régles pour enregistrer les résultats : \n"
              "0 : Match nul\n"
              "1 : Victoire Joueur 1\n"
              "2 : Victoire Joueur 2\n")

    def match_result(self, match):
        short_match_id = match.id[:5]+"..."
        result = int(input(f"Gagnant du match {short_match_id} : "))
        if result in (0, 1, 2):
            return result
        print("Résultat inccorect, veuillez vous référer aux régles ci-dessous.")
        View().match_result_rules()
        return View().match_result(match)

    def winner_score(self, winner_name, point, winner_score):
        print(f"Le joueur {winner_name} à gagné {point} point. Score total sur le tournois : {winner_score} points")
