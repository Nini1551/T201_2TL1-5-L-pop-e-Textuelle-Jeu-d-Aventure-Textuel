
from .inventaire import Inventaire


class Character:
    """
    Cette classe représente le personnage joué par le joueur
    Il a pour but d'évoluer pendant l'aventure en fonction des choix du joueur

    """

    def __init__(self, name='Dwarfy', race='Nain', level=1,
                 caract={'strenght': 1, 'speed': 1, 'vitality': 1, 'ability': 1}, inventory=Inventaire()):
        
        """
        Constructeur de Personnage : Permet de créer un nouveau personnage en attribuant les propriétés suivantes

        :param name : Le nom du personnage, par défaut ici 'Dwarfy' 
        :type name : str

        :param race : La race du personnage, par défaut ici 'Nain'
        :type race : str

        :param level : introduit le niveau du personnage, par défaut 1
        :type level: int

        :param caract : introduit les caractéristiques du personnage,
             par défaut un dictionnaire contenant les valeurs suivantes :
             {'strenght' : 1, 'speed' : 1, 'vitality' : 1, 'ability' : 1}
        :type caract : dict

        :param inventory : introduit l'inventaire du personnage, 
            par défaut un tuple qui contiendra les noms d'objets ['sword', 'shield', 'water', 'raw meat']
        :type inventory : tuple

        """
        # Déclaration et sécurisation des variables d'instances en leur attribuant les valeurs définies ou par défaut
        self.__name = name
        self.__race = race
        self.__level = level
        self.__caract = caract
        self.__inventory = inventory    

    def __str__(self):
        """
        POST = Affiche un message de confirmation de création du personnage en renvoyant un récap du nom, race, niveau,
              caractéristique, inventaire
              qu'on utilisera comme l'affichage d'inventaire également ce n'est que le descriptif du personnage au final
        
        """

        about_player = f'''
                                INFORMATIONS CONCERNANT LE PERSONNAGE :

              Nom : {self.__name}
              Race : {self.__race}
              Niveau : {self.__level}
              Caractéristiques :
                                Strenght : {self.__caract['strenght']}
                                Speed    : {self.__caract['speed']}
                                Vitality : {self.__caract['vitality']}
                                Ability  : {self.__caract['ability']}

              '''
        return about_player

    @property
    def name(self):
        """
        Propriété qui permet d'afficher le nom en utilisant la propriété name de Personnage => Personnage.name

        """
        return self.__name

    @property
    def race(self):
        """
        Propriété qui permet d'afficher la race en utilisant la propriété race de Personnage => Personnage.classe

        """
        return self.__race

    @property
    def level(self):
        """
        Propriété qui permet d'afficher le niveau en utilisant la propriété level de Personnage => Personnage.level
        
        """
        return self.__level

    @property
    def caract(self):
        """
        Propriété qui permet d'afficher les caractéristiques en utilisant la propriété caract de Personnage
        => Personnage.caract
        
        """
        return self.__caract

    @property
    def inventory(self):
        """
        Propriété qui permet d'afficher l'inventaire en utilisant la propriété inventory de Personnage
         => Personnage.inventory
        
        """
        return self.__inventory

# Déclarations des méthodes de modifications des valeurs de notre classe :

    def level_up(self, new_value: int):
        """

        Méthode qui permet d'augmenter / diminuer le niveau du personnage => Personnage.level()

        :param new_value : valeur qui indique de combien de niveau le personnage va augmenter
        :type new_value : int
        """
        self.__level += new_value

    def caract_up(self, carac_name: str, new_value: int):
        """
        Méthode qui permet de modifier les caractéristiques du personnage => Personnage.caract()

        :param carac_name : Nom de la caractéristique à modifier
        :type carac_name : str

        :param new_value: valeur indiquant de combien la caractéristique doit augmenter / diminuer
        :type new_value: int

        """
        self.__caract[carac_name] +=  new_value

    def inventory_add(self, item: str):
        """
        Méthode qui permet d'ajouter un objet à l'inventaire => Personnage.inventory_add()

        :param item : nom de l'objet à ajouter à l'inventaire
        :type item : str
        
        """
        self.__inventory.add_item(item)

    def inventory_remove(self, item: str):
        """
        Méthode qui permet d'enlever un objet de l'inventaire => Personnage.inventory_remove()

        :param item : nom de l'objet à retirer de l'inventaire
        :type item : str
        
        """
        self.__inventory.remove_item(item)
