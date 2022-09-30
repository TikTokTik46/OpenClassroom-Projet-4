from models.database import Database

class View:
    """Gestion de l'interface utilisateur"""

    def new_player(self):
        """Interface de création d'un nouveau joueur"""
        name = input("Nom du joueur : ")
        rank = int(input("Rang : "))
        return name, rank

    def new_tournament(self):
        """Interface de création d'un nouveau tournois"""
        tournament_name = input("Nom du tournois : ")
        round_number = int(input("Nombre de round : "))
        print("Veuillez entrer la liste des joueurs :")
        return tournament_name, round_number

    def display_match_pair(self, match, db):
        player_one_name = db.search_1("Player", "id", match.player_one)[0]["name"]
        player_two_name = db.search_1("Player", "id", match.player_two)[0]["name"]
        tournament_name = db.search_1("Tournament", "id", match.tournament_id)[0]["tournament_name"]
        round_name = db.search_1("Round", "id", match.round_id)[0]["round_name"]
        print(f"ID Match {match.id} - Tournois : {tournament_name} - {round_name} : Joueur 1 -> {player_one_name} contre Joueur 2 -> {player_two_name}")

    def match_result_rules(self):
        print("Régles pour enregistrer les résultats : \n"
              "0 : Match nul\n"
              "1 : Victoire Joueur 1\n"
              "2 : Victoire Joueur 2")

    def match_result(self, match):
        short_match_id = match["id"][:5]+"..."
        result = int(input(f"Gagnant du match {short_match_id} : "))
        if result in (0, 1, 2):
            return result
        print("Résultat inccorect, veuillez vous référer aux régles ci-dessous.")
        View().match_result_rules()
        return View().match_result(match)

