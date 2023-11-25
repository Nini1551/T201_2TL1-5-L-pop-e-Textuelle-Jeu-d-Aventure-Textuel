import json
from .character import Character


class Aventure:
    """
    Représente une aventure jouée par un joueur.
    L'aventure suit les choix de celui-ci et se termine quand l'aventure est terminée
    (quand il n'y a plus de choix disponibles)
    """
# Tag des clés primaires
    LIB_TAG = 'lib'
    TEXT_TAG = 'text'
    CHOICES_TAG = 'choices'
    ITEM_TAG = 'item'
    CONDITION_TAG = 'condition'
    
# Tag pour les id des choix
    ID_TAG = 'id'
    
# Tag de gestion des conditions et actions
    ACTION_TAG = 'action'
    GET_TAG = 'get'
    REMOVE_TAG = 'remove'
    NAME_TAG = 'name'
    NEED_TAG = 'need'
    ID_TO_REACH_TAG = 'id_to_reach'

    def __init__(self, scenario_path: str):
        """
        Initialise une aventure via un premier choix généralement appelé introduction
        PRE: - scenario_path: le nom du fichier JSON du scénario joué par le joueur.
               Le fichier JSON doit avoir un format précis. Il s'agit d'un dictionnaire représentant un choix.
                Il est composé de plusieurs attributs :
                - lib : une chaîne de caractères donnant l'intitulé du choix en une ligne.
                - text : le texte de narration lié au choix. Il doit terminer par un retour à la ligne
                - choices : une liste qui sera soit vide, soit constituée elle-même de choix (suivre ce format-ci)
        POST: Initialise une aventure constituée de l'attribut suivant :
              - main_choice : le choix actuel de l'aventure.
                              Il est initialisé sur le choix d'introduction contenu dans le dictionnaire du document
                              JSON ouvert via 'scenario_path'.
        """
        encoding = 'utf-8'

        with open(scenario_path, encoding=encoding) as scenario_file:
            self.__main_choice = json.load(scenario_file)

        player = Character(input('Quel est votre nom jeune aventurier ? :\n'))
        self.__player = player

    def __str__(self) -> str:
        """
        POST: Retourne une chaine de caractère comprenant :
              - le texte de narration du choix actuel suivi d'un passage à la ligne.
              - une liste numérotée des libellés des sous-choix du choix actuel.
        """
        to_display = f"{self.__main_choice[self.TEXT_TAG]}\n"
        if self.check_if_any_condition():
            
            if self.check_if_condition_is_valid(self.__main_choice[self.CONDITION_TAG]):
                for i, choice in enumerate(self.__main_choice[self.CHOICES_TAG]):
                    to_display += f"{i+1}. {choice[self.LIB_TAG]}\n"
            else:
                self.enlever_proposition(self.__main_choice[self.CHOICES_TAG],
                                         self.__main_choice[self.CONDITION_TAG][self.ID_TO_REACH_TAG])
                for i, choice in enumerate(self.__main_choice[self.CHOICES_TAG]):
                    to_display += f"{i+1}. {choice[self.LIB_TAG]}\n"
       
        else:
            for i, choice in enumerate(self.__main_choice[self.CHOICES_TAG]):
                to_display += f"{i+1}. {choice[self.LIB_TAG]}\n"
                    
        return to_display[:-1]

    def is_final_choice(self) -> bool:
        """
        POST: Renvoie si le choix actuel est un choix final, c'est à dire s'il a lui-même un ou plusieurs sous-choix.
        """
        return not len(self.__main_choice[self.CHOICES_TAG])
    
    def get_new_choice(self, choice_id: str) -> dict:
        """
        PRE : -
        Affiche l'état actuel de l'aventure.
        Demande au joueur de choisir, en fonction de la liste numérotée des sous-choix, quel choix il veut faire.
        Le programme repose la question si le joueur ne rentre pas un entier valide et l'avertit s'il ne rentre
        pas un nombre.
        PRE: - choice_id : une chaîne de caractère correspondant à l'identifiant d'un des sous-choix du choix actuel
                de l'aventure.
        POST: Renvoie le choix actuel pour le sous-choix sélectionné par le joueur.
        """

        choices = self.__main_choice[self.CHOICES_TAG]
        choice_id = int(choice_id) - 1
        if choice_id not in range(len(choices)):
            raise ValueError

        return choices[choice_id]    

    def run(self):
        """
        PRE : -
        Permet au joueur de partir à l'aventure tant que celui-ci peut encore faire des choix.
        Quand ce n'est plus le cas, affiche un message de félicitations.
        POST: Parcoure le scénario de l'aventure jusqu'à ce que le joueur ne puisse plus faire de choix.
        """
        congratulations_message = ("Félicitations ! Vous avez terminé l'aventure. "
                                   "\nN'hésitez pas à redémarrer le programme pour tester "
                                   "les autres choix disponibles !")
        error_value = -1
        error_message = "Insérez un nombre entier valide !"
        prompt = '>>> '

        while not self.is_final_choice():
            
            print(f"\n{self}")
            print(
                '''



                Pour afficher : - votre inventaire 'i'
                                - vos caractéristiques 'c'
                
                Pour faire un choix :  le numéro ce celui-ci

                
                ''')
            print('---------------------------------------------------------------')

            answer = error_value
            while answer == error_value:
                answer = input(prompt)
                if answer.lower() == 'i':
                    print(self.__player.inventory)
                elif answer.lower() == "c":
                    print(self.__player)
                else:
                    try:
                        self.__main_choice = self.get_new_choice(answer)

                        if self.looking_for_item():
                            self.gestion_item()

                    except ValueError:
                        print(f"\n{error_message}")
                        answer = error_value

        print(self)
        print(congratulations_message)
    
    def looking_for_item(self) -> bool:

        """
        Permet de vérifier si le dictionnaire Item existe et si il possède au moins une paire de clé/valeur

        """
        if self.ITEM_TAG in self.__main_choice:
            item = self.__main_choice[self.ITEM_TAG]
            if len(item) > 0:
            
                return True
            else:
                return False
        else:
            return False
        
    def gestion_item(self):
        """
        Permet de récupérer du dictionnaire item du Choix actuel afin de pouvoir interagir avec et vérifier
        l'action qui y est définie
        
        """

        item = self.__main_choice[self.ITEM_TAG]
        if item[self.ACTION_TAG] == self.GET_TAG:

            self.get_item(item)

        elif item[self.ACTION_TAG] == self.REMOVE_TAG:
            
            self.remove_item(item)

    def get_item(self, item):
        """
        
        Permet d'ajouter un item à l'inventaire ou non
        
        """
        if item[self.ACTION_TAG] == self.GET_TAG:
            answer = self.ask_user_loot(item)
            if answer.lower() == 'y':
                self.__player.inventory_add(item[self.NAME_TAG])
                return self.obtention_item(item)
                
            else:
                return self.refus_obtention_item(item)

    def remove_item(self, item):
        """
        
        Permet d'enlever un item de l'inventaire

        """
        if item[self.ACTION_TAG] == self.ITEM_TAG:
            self.__player.inventory_remove(item[self.NAME_TAG])

    def check_if_any_condition(self) -> bool:
        """
        Vérifie si il y'a une condition, et si elle est remplie
        
        """
        if self.CONDITION_TAG in self.__main_choice:
            return True
        else:
            return False

    def check_if_condition_is_valid(self, condition) -> bool:
        """
        Permet de gérer une condition si elle est présente

        """
       
        if condition[self.ACTION_TAG] == self.NEED_TAG:
            
            if condition[self.NAME_TAG] in self.__player.inventory.inventory:
                return True
            else:
                return False
        
    def enlever_proposition(self, item, id_value):
        """
        
        Permet de supprimer de la liste des choix possibles les propositions dont les conditions ne sont pas remplies

        """
        for index, obj in enumerate(item):
            if obj[self.ID_TAG] == id_value:
                del(item[index])

    def obtention_item(self, item):
        """
        
        Affiche l'obtention d'un objet dans l'inventaire
        
        """
        print(f"\nVous obtenez [ {item[self.NAME_TAG]} ]\n")

    def refus_obtention_item(self, item):
        """
        Affiche le refus du joueur d'ajouter l'objet à l'inventaire
        
        """
        print(f"Vous jetez {item[self.NAME_TAG]} par dessus votre "
              f"épaule sans même prendre la peine de regarder derrière vous")

    def ask_user_loot(self, item) -> str:
        """

        Affiche l'obtention d'un loot et demande au joueur si il désire l'accepter

        """
        return input(f"Tu viens de drop [ {item[self.NAME_TAG]} ],"
                     f" souhaite tu l'ajouter à ton inventaire ? 'y' or 'n'\n >>> ")
