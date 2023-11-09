import json


class Aventure:
    """
    Représente une aventure jouée par un joueur.
    L'aventure suit les choix de celui-ci et se termine quand l'aventure est terminée (quand il n'y a plus de choix disponibles)
    """
    def __init__(self, scenario_path: str):
        """
        Initialise une aventure via un premier choix généralement appelé introduction
        PRE: - scenario_path: le nom du fichier JSON du scénario joué par le joueur.
               le fichier JSON doit avoir un format précis. Il s'agit d'un dictionnaire représentant un choix.
                Il est composé de plusieurs attributs :
                - lib: une chaîne de caractères donnant l'intitulé du choix en une ligne.
                - text: le texte de narration lié au choix. Il doit terminer par un retour à la ligne
                - choices: une liste qui sera soit vide, soit constituée elle-même de choix (suivre ce format-ci)
        POST: Initialise une aventure constitué de l'attribut suivant :
              - main_choice : le choix actuel de l'aventure.
                              Il est initialisé sur le choix d'introduction contenu dans le dictionnaire du document JSON ouvert via 'scenario_path'.
        """
        with open(scenario_path, encoding='utf-8') as scenario_file:
            self.__main_choice = json.load(scenario_file)

    def __str__(self) -> str:
        """
        POST: Retourne une chaine de caractère comprenant :
              - le texte de narration du choix actuel suivi d'un passage à la ligne.
              - une liste numérotée des libellés des sous-choix du choix actuel.
        """
        to_display = f"{self.__main_choice['text']}\n"
        for i, choice in enumerate(self.__main_choice['choices']):
            to_display += f"{i+1}. {choice['lib']}\n"
        return to_display[:-1]

    def set_new_choice(self):
        """
        Affiche l'état actuel de l'aventure.
        Demande au joueur de choisir, en fonction de la liste numérotée des sous-choix, quel choix il veut faire.
        Le programme repose la question si le joueur ne rentre pas un entier valide et l'avertit s'il ne rentre pas un nombre.
        POST: Change le choix actuel pour le sous-choix sélectionné par le joueur.
        """
        print(self)

        choices = self.__main_choice['choices']
        answer = -1
        while answer == -1:
            answer = input('>>> ')
            try:
                answer = int(answer) - 1
                if answer not in range(len(choices)):
                    raise ValueError
            except ValueError:
                print("\nInsérez un nombre entier valide !")
                answer = -1

        self.__main_choice = choices[answer]

    def is_final_choice(self) -> bool:
        """
        POST: Renvoie si le choix actuel est un choix final, c'est à dire s'il a lui-même un ou plusieurs sous-choix.
        """
        return not len(self.__main_choice['choices'])

    def run(self):
        """
        Permet au joueur de partir à l'aventure tant que celui-ci peut encore faire des choix.
        Quand ce n'est plus le cas, affiche un message de félicitations.
        POST: Parcoure le scénario de l'aventure jusqu'à ce que le joueur ne puisse plus faire de choix.
        """
        while not self.is_final_choice():
            self.set_new_choice()
        print(self)
        print("Félicitations ! Vous avez terminé l'aventure. \nN'hésitez pas à redémarrer le programme pour tester les autres choix disponibles !")
