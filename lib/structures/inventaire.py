
class Inventaire:
    """
    Cette classe représente l'inventaire du personnage
    L'inventaire à pour but d'être modifié à chaque instant de la partie
    
    """

    def __init__(self, obj=['sword', 'torch']):
        """
        :param obj : nom des objets contenu dans l'inventaire
        :type obj : list
        
        """
        
        self.__inventory = obj
    
    @property
    def inventory(self):
        """
        Propriété qui permet d'afficher inventory

        """
        return self.__inventory

    def __str__(self):
        """
        POST = Affiche l'état de l'inventaire, ce qu'il contient
        
        
        """
        liste = []
        for item in self.__inventory:
            liste.append('[ ' + item + ' ]')
        inventory_str = "".join(liste)
        return f'''
                        VOICI VOTRE INVENTAIRE
                    
                        {inventory_str}
                    
                    
                    '''

    def add_item(self, obj_to_add):
        self.__inventory.append(obj_to_add)

    def remove_item(self, obj_to_remove):
        self.__inventory.remove(obj_to_remove)
