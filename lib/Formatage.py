"""
Le module JSON permet de manipuler (créer, modifier et supprimer) des fichiers JSON (qui sont des structure de données)
"""
import json

class Formatage:
    """
    La classe Formatage permet de partir d'un fichier texte respectant une syntaxe bien définie et de fournir en retour
    un fichier structuré permettant au reste du programme d'utiliser ces données.
    Elle va permettre à un utilisateur de créer son propre scénario et de l'ajouter dans le programme.
    """
    def __init__(self):
        """
        Cette fonction ci ne renvoie rien, elle ne créer que des variables utiles et accessibles à toute la classe.
        PRE: -
        POST: Définis des variables avec des valeurs globale à toute la classe
        """
        self.section = []
        self.sections = []
        self.lines = []
        self.lib = ""
        self.text = ""
        self.list_text = []
        self.choices = ""
        self.tamp = ""
        self.choice_number = []
        self.list_choice_number = []
        self.list_labels = []
        self.message = ""

    def __str__(self):
        """
        Cette fonction renvoie le dictionnaire formés à partir du fichier texte sous formes de message
        s'affichant en console.
        PRE: -
        POST: Renvoi un message à l'écran avec le dictionnaire constitué des données structurées.
        """
        print(f"Voici vos données entrées mise sous format lisible par le programme et structurées :\n{self.message}")

    def format_to_json(self, my_dict: dict):
        """
        La fonction suivante ajoute au fichier JSON existant (ou créer un fichier JSON si il n'en existe pas)
        un dictionnaire formé a partir du fichier texte que vous lui fournissez et renvoi le dictionnaire
        qui vient d'y être ajouté.
        PRE: - my_dict : le dictionnaire créer à partir du fichier texte fournit à la fonction 'create_dict'
        POST: Renvoi le dictionnaire passé en paramètre si celui-ci est bien ajouté au fichier JSON.
        """
        try:
            with open("./Fichier_json/mon_fichier.json", 'w', encoding="UTF-8") as file:
                json.dump(my_dict, file)
            return my_dict

        except FileNotFoundError:
            return 'Fichier introuvable.'
        except IOError:
            return 'Erreur IO.'

    # ------Fin de la fonction format_to_json()---------

    def create_dict(self, choices, labels, texts):
        """
        La fonction ici créer le dictionnaire necessaire à la fonction 'format_to_json' à partir des listes
        de numéros de choix, libelle ainsi que leur texte associé.
        PRE: - choices : liste des numéros de choix.
             - labels : liste des libellé correspondant aux numéros de choix et aux textes.
             - texts : liste des textes correspondant aux numéros de choix et aux libellés.
        POST: Va créer un dictionnaire à partir des 3 listes reçues, l'envoyer à la fonction 'format_to_json'
                et retourner le dictionnaire construit si la fonction 'format_to_json' ne renvoi pas d'erreur.
        """
        # Vérifier si la longueur des trois listes est la même
        if len(choices) != len(labels) or len(choices) != len(texts):
            raise ValueError("Les listes doivent avoir la même longueur. \nErreur lors de la lecture et de l'echantillonage")

        # Initialiser le dictionnaire
        result = {"lib": labels[0], "text": texts[0], "choices": []}

        for choice, label, text in zip(choices[1:], labels[1:], texts[1:]):
            levels = choice.split('.')
            levels = list(filter(None, levels))
            # levels = [level for level in choice.split('.') if level]

            temp_dict = {"lib": label, "text": text, "choices": []}

            parent = result  # On dit que le parent = my_dict
            for level in levels[:-1]:
                parent = parent["choices"][int(level) - 1]

            parent["choices"].append(temp_dict)

        message = self.format_to_json(result)
        return message

    def read_and_cut(self, fl):
        """
        La fonction suivante reçois un fichier en lecture, le découpe en morceau et créer à partir d'une
        syntaxe 3 listes composées des numéros de choix, des libellés et des textes et envoie le tout à la
        fonction 'read_and_cut'.
        PRE: - fl : un fichier texte (donc une chaine de carctère)
        POST: Va passer en paramètre les 3 listes à la fonction 'creat_dict' et renvoie le message reçu par
                cette fonction.
        """
        # Division du fichier en lignes distinctes ajoutée à une liste
        for line_tamp in fl:
            line_tamp.strip()
            self.lines.append(line_tamp)
        self.lines.append("\n")

        # Création d'une liste de sections contenant chaque section
        # Chaque section est une liste constituée du numéro de choix et du libellé d'un coté
        # et du texte y étant associé de l'autre.
        for s in self.lines:
            if s == '\n':
                self.section.append(self.tamp)
                self.sections.append(self.section)
                self.section = []
                self.tamp = ""
            elif s.startswith('.'):
                self.section.append(s)
            else:
                self.tamp += s

        self.sections.append(self.section)
        self.sections.pop()

        #
        for i in self.sections:
            for j in i:
                indice_espace = 0
                i = 0

                for espace in j:
                    if espace == " ":
                        indice_espace = i
                        break
                    else:
                        i += 1

                if j.startswith('.'):
                    self.choice_number = j[:indice_espace]
                    self.lib = j[indice_espace + 1:]
                else:
                    self.text = j.strip()
            self.list_choice_number.append(self.choice_number)
            self.list_labels.append(self.lib.strip())
            self.list_text.append(self.text.strip())

        msg_result_dict = self.create_dict(self.list_choice_number, self.list_labels, self.list_text)

        return msg_result_dict

    # ------------Fin de la fonction read_and_cut()-----------

    def run(self, path_file):
        """
        Cette fonction est la fonction principale appelée au démarrage du programme. Elle reçcois en
        paramètre un chemin de fichier et renverra un texte dans la console.
        PRE: - path_file : le chemin où se trouve le fichier texte écris par l'utilisateur
        POST: Renvoi un petit message en console si jamais le fichier json à été mis à jour avec toutes
                les infos fournies, sinon renvois un message d'erreur adéquat.
        """
        try:
            with open(path_file, encoding='utf-8') as file:
                self.message = self.read_and_cut(file)
                print(f"\n")
                self.__str__()

        except FileNotFoundError as file_path:
            print(f'Fichier introuvable : {file_path}')
        except IOError as e:
            print(f'Erreur IO : {e}')
        except AttributeError:
            print("Il y a des retours à la ligne en trop entre 2 blocs")


"""
Message à afficher lorsque pas comme demandé : Si jamais les normes sont pas respectés : Veuillez respecter les normes 
 imposées par le format afin que votre scénario soit ajouté dans la base de données de scénarios
"""

"""
Les fonctionnalités de formatage dont terminées et fonctionnelles. 
Il ne reste plu qu'à : 
OK - trouver une solution pour implémenter ça dans un dictionnaire dans la structure que je veux
 - Gérer toutes les erreurs qui pourrait intervenir en fonction des cas
        (OK- Si des retour a la ligne en trop entre des blocs
          - Si un numéro qui manque entre des points d'un numéro de choix
          - Si il manque un point à la fin d'un numéro de choix
          - Si il manque un point au début d'un numéro de choix
          - Si il manque un point dans un numéro de choix
          - Si il y a un retour à la ligne en trop dans la partie texte
        )
OK - Faire toutes la doc pour l'utilisateur/joueur
OK - Faire docstring pour chaque fonctions
OK - Réécrire le code en beaucoup plus propre (Créer plus de petites fonctions, commenté, 
    écrire tout le code en anglais (nom de variables et fonctions), retirer tout les prompts debugger,...)
"""