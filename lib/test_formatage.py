import unittest
from unittest.mock import patch, MagicMock, Mock
from Formatage import Formatage
import datetime
import math
import json


class TestFormatage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Configurer toutes les configurations ou ressources communes nécessaire pour les tests
        self.formatage = Formatage()

    @classmethod
    def tearDownClass(cls):
        # Néttoyer après que tous les tests aient été executés
        pass

    def setUp(self):
        # Configurer toutes les configurations ou ressources spécifiques aux test pour chaque test
        self.formatage.path_json_file = "../Fichier_json/mon_fichier.json"

    def tearDown(self):
        # Nettoyer après chaque cas de test
        pass
    # ------------------------------------------------------------------------

    def test_init(self):
        pass

    def test_str(self):
        pass
    # ------------------------------------------------------------------------

    def test_format_to_json(self):
        # Besoin de mocker la lib json
        """
        Cette fonction va tester tous les cas suivants pour la fonction 'format_to_json()':
        - vérification si jamais le dict n'est pas un dict
        (- vérification si le chemin du fichier json existe déjà)
        (- vérification du contenu json afin de savoir si il est serializable)
        - vérification si le dict est vide
        - vérification si le dict est le même que le json actuel

        1) le dict passé en paramètre n'est pas un dictionnaire
        2) le dict passé est vide
        3) le dict passé est correct
        3bis) le dict passé est le même que le précédent et donc que le json
        4..) le dict passé n'est pas sérializable :
                4bis1) Un objet custom
                4bis2) Un objet Date
                4bis3) Les cycliques
                4bis4) Les dict contenant des 'int' et des chaines binaires
        5) Un Infinity et un NaN dans un dict
        """
        default_json = {"valeur_1": "bonjour"}
        self.formatage.format_to_json(default_json)

        dict_1 = "bonjour"
        dict_2 = {}
        dict_3 = {'key1': 'value1', 'key2': 42, 'key3': [1, 2, 3]}
        dict_3bis = {'key1': 'value1', 'key2': 42, 'key3': [1, 2, 3]}

        class CustomObject:
            def __init__(self, value):
                self.value = value
        dict_4bis1 = {'custom_object': CustomObject(42)}
        dict_4bis2 = {'date': datetime.datetime.now()}
        dict_4bis3 = {}
        dict_4bis3['self_reference'] = dict_4bis3
        dict_4bis4 = {'set_example': {1, 2, 3}, 'bytes_example': b'hello'}
        dict_5 = {'infinity': float('inf'), 'nan': math.nan}

        # result_1
        with self.assertRaises(TypeError):
            self.formatage.format_to_json(dict_1)
        # result_2
        with self.assertRaises(ValueError):
            self.formatage.format_to_json(dict_2)

        result_3 = self.formatage.format_to_json(dict_3)
        self.assertEqual(result_3, f"Le contenu suivant a été ajouté : {dict_3}", msg="result_3 qui renvoi le dict")

        result_3bis = self.formatage.format_to_json(dict_3bis)
        self.assertEqual(result_3bis, "Le contenu est le même et n'a pas été modifié", msg="result_3bis qui renvois un message comme quoi c'est pareil")

        # result_4bis1
        with self.assertRaises(TypeError):
            self.formatage.format_to_json(dict_4bis1)

        # result_4bis2
        with self.assertRaises(TypeError):
            self.formatage.format_to_json(dict_4bis2)

        # result_4bis3
        with self.assertRaises(ValueError):
            self.formatage.format_to_json(dict_4bis3)
        
        # result_4bis4
        with self.assertRaises(TypeError):
            self.formatage.format_to_json(dict_4bis4)

        result_5 = self.formatage.format_to_json(dict_5)
        self.assertEqual(result_5, "Le contenu suivant a été ajouté : {'infinity': inf, 'nan': nan}")



    def test_create_dict(self):
        """
        Cette fonction va tester tous les cas suivants pour la fonction 'create_dict()':
        - vérification si les trois listes n'ont pas les mêmes longueur
        - vérification si jamais il manque un paramètre
        - vérification si jamais les listes sont inversées en tant que paramètre

        1) les 3 tableaux de la même longueur (version ok)
        2) un paramètre qui n'est pas un tableau mais une string
        3) un tableau pas de la même longueur, des données en plus
        4) un tableau vide
        5) un tableau de la même longueur mais avec des valeurs vides
        6) inversion de place des tableaux dans les paramètres lors de l'appel

        créer vérification lorsque: tableau vide, pas un tableau mais une string,
         tableau même longueur mais valeurs vides, inversion des tableaux en param
        """
        response_1 = r"""Le contenu suivant a été ajouté : {'lib': 'Introduction', 'text': 'Ceci est une introduction\nSi si je te jure', 'choices': [{'lib': 'Choix 1', 'text': 'Ceci est le premier choix\nSi si je te jure', 'choices': []}, {'lib': 'Choix 2', 'text': 'Ceci est le deuxième choix\nSi si je te jure', 'choices': [{'lib': 'Sous-choix 1', 'text': "Ceci est le premier sous choix\nSi si je te l'assure", 'choices': []}]}]}"""
        response_5 = r"""Le contenu suivant a été ajouté : {'lib': 'Introduction', 'text': 'Ceci est une introduction\nSi si je te jure', 'choices': [{'lib': 'Choix 1', 'text': 'Ceci est le premier choix\nSi si je te jure', 'choices': []}, {'lib': 'Choix 2', 'text': 'Ceci est le deuxième choix\nSi si je te jure', 'choices': []}, {'lib': 'Sous-choix 1', 'text': "Ceci est le premier sous choix\nSi si je te l'assure", 'choices': []}]}"""
        response_6 = r"""Le contenu suivant a été ajouté : {'lib': '.', 'text': 'Ceci est une introduction\nSi si je te jure', 'choices': [{'lib': '.1.', 'text': 'Ceci est le premier choix\nSi si je te jure', 'choices': []}, {'lib': '.2.', 'text': 'Ceci est le deuxième choix\nSi si je te jure', 'choices': []}, {'lib': '.2.1.', 'text': "Ceci est le premier sous choix\nSi si je te l'assure", 'choices': []}]}"""

        list_choice = ['.', '.1.', '.2.', '.2.1.']
        list_lib = ['Introduction', 'Choix 1', 'Choix 2', 'Sous-choix 1']
        list_text = ['Ceci est une introduction\nSi si je te jure',
                     'Ceci est le premier choix\nSi si je te jure',
                     'Ceci est le deuxième choix\nSi si je te jure',
                     "Ceci est le premier sous choix\nSi si je te l'assure"]
        a_simple_string = "Coucou"

        list_lib_longer = ['Introduction', 'Choix 1', 'Choix 2', 'Sous-choix 1', 'je suis', 'le surplus']
        list_choice_empty = []
        list_choice_empty_slots = ['', '', '', '']

        result_1 = self.formatage.create_dict(list_choice, list_lib, list_text)
        #result_2 = self.formatage.create_dict(a_simple_string, list_lib, list_text)
        #result_3 = self.formatage.create_dict(list_choice, list_lib_longer, list_text)
        #result_4 = self.formatage.create_dict(list_choice_empty, list_lib, list_text)
        result_5 = self.formatage.create_dict(list_choice_empty_slots, list_lib, list_text)
        result_6 = self.formatage.create_dict(list_lib, list_choice, list_text)

        self.assertEqual(result_1, response_1, msg="result_1 tout se passe nickel")
        # result_2
        with self.assertRaises(ValueError):
            #self.assertEqual(result_2, "Fichier introuvable. [Errno 2] No such file or directory: './Fichier_json/mon_fichier.json'", msg="result_2 tout se passe nickel")
            self.formatage.create_dict(a_simple_string, list_lib, list_text)
        # result_3
        with self.assertRaises(ValueError):
            #self.assertEqual(result_3, "Fichier introuvable. [Errno 2] No such file or directory: './Fichier_json/mon_fichier.json'")
            self.formatage.create_dict(list_choice, list_lib_longer, list_text)
        # result_4
        with self.assertRaises(ValueError):
            #self.assertEqual(result_4, "Fichier introuvable. [Errno 2] No such file or directory: './Fichier_json/mon_fichier.json'")
            self.formatage.create_dict(list_choice_empty, list_lib, list_text)
        self.assertEqual(result_5, response_5, msg="result_5 tout se passe nickel")
        self.assertEqual(result_6, response_6, msg="result_6 tout se passe nickel")

    def test_read_and_cut(self):
        """
        Cette fonction va tester tous les cas suivants pour la fonction 'read_and_cut()':
        - vérification du format de fichier
        - vérification que c'est bien une chaine de caractère
        - vérification que les listes ne sont pas vides

        1) le texte est correct, bon format
        (2) le fichier est écris sans point au début pour l'intro)
        (3) le fichier est écris sans espace entre le point et le nom de l'intro)
        (4) le fichier est écris avec plus de 1 retour à la ligne dans le texte intro)
        (5) le fichier est écris sans point au début du num d'un choix)
        (6) le fichier est écris sans point à la fin du num d'un choix)
        (7) le fichier est écris sans point au milieu du num d'un choix)
        (8) le fichier est écris sans espace entre le point et le nom d'un choix)

        9) le fichier est un nombre et non une chaine de caractère

        10) le fichier est une chaine de caractère vide
        (11) le fichier est écris avec un en-tête en moins (donc toute la ligne d'en tête d'un choix))
        """

        file_1 = (""". Introduction"
Ceci est une introduction
Si si je te jure

.1. Choix 1
Ceci est le premier choix
Si si je te jure

.1.1. Sous-choix 1
Ceci est le premier sous choix
Si si je te l'assure
prout prout prout""")

        # -------------------------------
        file_9 = 9
        # -------------------------------
        file_10 = ""

        result_1 = self.formatage.read_and_cut(file_1)

        #result_10 = self.formatage.read_and_cut(file_10)


        response_1 = r"""Le contenu suivant a été ajouté : {'lib': 'Introduction"', 'text': 'Ceci est une introduction\nSi si je te jure', 'choices': [{'lib': 'Choix 1', 'text': 'Ceci est le premier choix\nSi si je te jure', 'choices': [{'lib': 'Sous-choix 1', 'text': "Ceci est le premier sous choix\nSi si je te l'assure\nprout prout prout", 'choices': []}]}]}"""
        #response_10 = r"""Le contenu suivant a été ajouté : {'lib': 'Introduction"', 'text': 'Ceci est une introduction\nSi si je te jure', 'choices': [{'lib': 'Choix 1', 'text': 'Ceci est le premier choix\nSi si je te jure', 'choices': [{'lib': 'Sous-choix 1', 'text': "Ceci est le premier sous choix\nSi si je te l'assure\nprout prout prout", 'choices': []}, {'lib': 'Sous-choix 1', 'text': "Ceci est le premier sous choix\nSi si je te l'assure\nprout prout prout", 'choices': []}, {'lib': 'Sous-choix 1', 'text': '', 'choices': []}]}, {'lib': 'Introduction"', 'text': 'Ceci est une introduction\nSi si je te jure', 'choices': []}, {'lib': 'Choix 1', 'text': 'Ceci est le premier choix\nSi si je te jure', 'choices': []}]}"""

        self.assertEqual(result_1, response_1, msg="result_1")

        with self.assertRaises(RuntimeError):
            #self.assertEqual(result_9, "Fichier introuvable. [Errno 2] No such file or directory: './Fichier_json/mon_fichier.json'", msg="result_9 ne construit pas correctement les listes")
            self.formatage.read_and_cut(file_9)
            #print("Erreur 'RuntimeError : attrapée")

        with self.assertRaises(RuntimeError):
            self.formatage.read_and_cut(file_10)

        #self.assertEqual(result_10, response_10, msg="result_10")

    def test_run(self):
        """
        Cette fonction va tester tous les cas suivants pour la fonction 'run()':
        1) le chemin de fichier est un fichier texte
        1bis) Appeler une deuxième fois d'affiler la même fonction avec le même paramètre
        2) le chemin de fichier est un fichier autre que texte
        3) le chemin amène à un dossier vide
        4) le chemin n'est pas un chemin mais une bête string (ex: "je suis un cehmin mdr")
        5) le chemin est un number
        6) le chemin est un dict
        7) le chemin est un tableau
        """
        path_1 = r"C:\Users\pc\OneDrive - EPHEC asbl\Bureau\Cours\Cours 2ème\Dev 2\T201_2TL1-5_L-Epopee-Textuelle_Jeu-d-Aventure-Textuel\Fichier_texte\essai_format.txt"

        file_2 = open("Fichier_test_path2.xls", 'w')
        path_2 = r"C:\Users\pc\OneDrive - EPHEC asbl\Bureau\Cours\Cours 2ème\Dev 2\T201_2TL1-5_L-Epopee-Textuelle_Jeu-d-Aventure-Textuel\lib\Fichier_test_path2.doc"

        path_3 = r"C:\Users\pc\OneDrive - EPHEC asbl\Bureau\Cours\Cours 2ème\Dev 2\T201_2TL1-5_L-Epopee-Textuelle_Jeu-d-Aventure-Textuel\lib"
        path_4 = "Je suis un chemin"
        path_5 = 5
        path_6 = {"nom": "Wayne", "prenom": "Bruce"}
        path_7 = ["Bonjour", 5, ["oui"], path_6]

        result_1 = self.formatage.run(path_1)
        result_2 = self.formatage.run(path_2)
        result_3 = self.formatage.run(path_3)
        result_4 = self.formatage.run(path_4)
        result_5 = self.formatage.run(path_5)
        result_6 = self.formatage.run(path_6)
        result_7 = self.formatage.run(path_7)

        file_2.close()

        self.assertEqual(result_1, None, msg="result_1 assert")
        self.assertEqual(self.formatage.run(path_1), None, msg="2ème appel consécutif avec path_1")
        self.assertEqual(result_2, None, msg="result_2 assert")
        self.assertEqual(result_3, None, msg="result_3 assert")
        self.assertEqual(result_4, None, msg="result_4 assert")
        self.assertEqual(result_5, None, msg="result_5 assert")
        self.assertEqual(result_6, None, msg="result_7 assert")
        self.assertEqual(result_7, None, msg="result_7 assert")


if __name__ == "__main__":
    unittest.main()
