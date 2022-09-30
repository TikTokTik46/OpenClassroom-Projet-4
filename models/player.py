import shortuuid

class Player:
    """Modèle représentant un joueur."""
    __score = 0 #Le double __ permet de protéger la variable en ecriture

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.id = "P_" + shortuuid.uuid()

    def __str__(self):
        """Used in print."""
        return f"Joueur {self.name}, ID du joueur {self.id}, rang {self.rank}, score {self.__score} "

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        """Used to return a dictionary of the instance attributes"""
        return {'id': self.id, 'name': self.name, 'rank': self.rank, 'score': self.__score}

    def set_score(self, new_score):
        self.__score = new_score