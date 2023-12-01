import json

class Formatage:
    def __init__(self):
        self.section = []
        self.sections = []
        self.lines = []
        self.lib = ""
        self.text = ""
        self.list_text = []
        self.choices = ""
        self.tamp = ""
        self.numero_choix = []
        self.list_numero_choix = []
        self.list_libelle = []

    def __str__(self):
        pass

    def format_to_json(self, my_dict: dict):
        try:
            with open("./Fichier_json/mon_fichier.json", 'w', encoding="UTF-8") as file:
                json.dump(my_dict, file)

            # return "Le scenario a été ajouté au fichier JSON"
            return my_dict

        except FileNotFoundError:
            return 'Fichier introuvable.'
        except IOError:
            return 'Erreur IO.'

    # ------Fin de la fonction format_to_json()---------

    def create_dict(self, choices, labels, texts):
        # Vérifier si la longueur des trois listes est la même
        if len(choices) != len(labels) or len(choices) != len(texts):
            raise ValueError("Les listes doivent avoir la même longueur.")

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

        for line_tamp in fl:
            line_tamp.strip()
            self.lines.append(line_tamp)
        self.lines.append("\n")

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
                    self.numero_choix = j[:indice_espace]
                    self.lib = j[indice_espace + 1:]
                else:
                    self.text = j.strip()
            self.list_numero_choix.append(self.numero_choix)
            self.list_libelle.append(self.lib.strip())
            self.list_text.append(self.text.strip())

        msg_result_dict = self.create_dict(self.list_numero_choix, self.list_libelle, self.list_text)

        return msg_result_dict

    # ------------Fin de la fonction read_and_cut()-----------

    def run(self, path_file):
        try:
            with open(path_file, encoding='utf-8') as file:
                message = self.read_and_cut(file)
                print(f"\n")
                print(message)

        except FileNotFoundError as file_path:
            print(f'Fichier introuvable : {file_path}')
        except IOError as e:
            print(f'Erreur IO : {e}')


"""
Message à affciher lorsque pas comme demandé : Si jamais les normes sont pas respectés : Veuillez respecter les normes 
 imposées par le format afin que votre scénario soit ajouté dans la base de données de scénarios
"""

"""
Les fonctionnalités de formatage dont terminées et fonctionnelles. 
Il ne reste plu qu'à : 
OK - trouver une solution pour implémenter ca dans un dictionnaire dans la structure que je veux
 - Gérer toutes les erreurs qui pourrait intervenir en fonction des cas
 - Faire toutes la doc pour l'utilisateur/joueur
 - Réécrire le code en beaucoup plus propre (Créer plus de petites fonctions, commenté, 
    écrire tout le code en anglais (nom de variables et fonctions), retirer tout les prompts debugger,...)
"""