"""
Le module JSON permet de manipuler (créer, modifier et supprimer) des fichiers JSON (qui sont des structure de données)
"""
import io
import json
import os

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
        self.choices = ""
        self.tamp = ""
        self.choice_number = []
        self.list_choice_number = []
        self.list_labels = []
        self.list_text = []
        self.message = ""
        self.path_json_file = "./Fichier_json/mon_fichier.json"
        # self.path_json_file = r"C:\Users\pc\OneDrive - EPHEC asbl\Bureau\Cours\Cours 2ème\Dev 2\T201_2TL1-5_L-Epopee-Textuelle_Jeu-d-Aventure-Textuel\Fichier_json"

    def __str__(self):
        """
        Cette fonction renvoie le dictionnaire formés à partir du fichier texte sous formes de message
        s'affichant en console.
        PRE: -
        POST: Renvoi un message à l'écran avec le dictionnaire constitué des données structurées.
        """
        print(f"Voici vos données entrées mises sous format lisible par le programme et structurées,\n{self.message}")

    def format_to_json(self, my_dict: dict):
        """
        La fonction suivante ajoute au fichier JSON existant (ou créer un fichier JSON si il n'en existe pas)
        un dictionnaire formé a partir du fichier texte que vous lui fournissez et renvoi le dictionnaire
        qui vient d'y être ajouté.
        PRE: - my_dict : le dictionnaire créer à partir du fichier texte fournit à la fonction 'create_dict'
        POST: Renvoi le dictionnaire passé en paramètre si celui-ci est bien ajouté au fichier JSON.
        """
        try:
            # Vérifier si my_dict est bien un dictionnaire
            if not isinstance(my_dict, dict):
                raise TypeError("Le paramètre passé n'est pas un dictionnaire valide.")

            # Vérifier si le chemin du fichier JSON existe
            if not self.path_json_file:
                raise FileNotFoundError("Chemin du fichier JSON non spécifié.")

            # Vérifier si le dictionnaire est vide
            if not my_dict:
                raise ValueError("Le dictionnaire est vide.")

            # Vérifier si my_dict est différent du contenu actuel du fichier JSON
            if os.path.exists(self.path_json_file):
                with open(self.path_json_file, 'r', encoding="UTF-8") as existing_file:
                    existing_data = json.load(existing_file)
                if my_dict == existing_data:
                    return "Le contenu est le même et n'a pas été modifié"

            # Vérifier si le contenu du dictionnaire est serializable en JSON
            json.dumps(my_dict)

            with open(self.path_json_file, 'w', encoding="UTF-8") as file:
                json.dump(my_dict, file)
            return f"Le contenu suivant a été ajouté : {my_dict}"

        except FileNotFoundError as file_path:
            return f'Fichier introuvable. {file_path}'

        except IOError as e:
            return f'Erreur IO. {e}'

        except json.JSONDecodeError as e:
            return f'Erreur de sérialisation JSON : {e}'

    # ------Fin de la fonction format_to_json()---------

    def create_dict(self, choices, labels, texts):
        """
        La fonction ici créer le dictionnaire necessaire à la fonction 'format_to_json' à partir des listes
        de numéros de choix, libelle ainsi que leur texte associé.
        PRE: - choices : liste des numéros de choix.
             - labels : liste des libellé correspondant aux numéros de choix et aux textes.
             - texts : liste des textes correspondant aux numéros de choix et aux libellés.
        POST: Va créer un dictionnaire à partir des 3 listes reçues, l'envoyer à la fonction 'format_to_json'
                et retourner le dictionnaire construit si la fonction 'format_to_json' ne renvoie pas d'erreur.
        """
        # Vérifier si la longueur des trois listes est la même
        if len(choices) != len(labels) or len(choices) != len(texts):
            raise ValueError("Les listes doivent avoir la même longueur. \nErreur lors de la lecture et de l'echantillonage")

        # Initialiser le dictionnaire
        result = {"lib": labels[0], "text": texts[0], "choices": []}

        for choice, label, text in zip(choices[1:], labels[1:], texts[1:]):
            levels = choice.split('.')
            levels = list(filter(None, levels))  # Filtrage de lécriture du niveau, de manière propre (ex: '3')
            # levels = [level for level in choice.split('.') if level]

            temp_dict = {"lib": label, "text": text, "choices": []}

            parent = result  # On dit que le parent = result le dict de base
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
        try:
            self.list_choice_number = []
            self.list_labels = []
            self.list_text = []

            # Vérifier que l'entrée est une chaîne de caractères
            if isinstance(fl, str):
                if fl.strip():
                    fl = io.StringIO(fl)
                    print("Fichier transformé")
                else:
                    raise TypeError('Le fichier ne peut pas être vide')
            elif isinstance(fl, int) or isinstance(fl, float):
                raise TypeError('L\'entrée doit être une chaîne de caractères. Vous avez entré un \'Number\'.')
            elif type(fl) is not io.TextIOWrapper:
                raise TypeError('L\'entrée doit être une chaîne de caractères.')

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

                    #if j.startswith(' '):
                        #raise ValueError("Format invalide. Un espace est attendu après le numéro de choix.")

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

            # Vérifier que les listes ne sont pas vides
            if not self.list_choice_number or not self.list_labels or not self.list_text:
                raise ValueError("Aucune donnée valide extraite du fichier.")

            msg_result_dict = self.create_dict(self.list_choice_number, self.list_labels, self.list_text)

            return msg_result_dict
        except Exception as e:
            raise RuntimeError(f"Erreur dans la fonction read_and_cut : {str(e)}")

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
        except AttributeError as a:
            print(f"Il y a des retours à la ligne en trop entre 2 blocs : {a}")
        except TypeError as t:
            print(f"Erreur de Type, cela doit être une 'str' : {t}")


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