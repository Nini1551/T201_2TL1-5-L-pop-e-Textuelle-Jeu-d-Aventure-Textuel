"""
En tant que joueur débutant ou chevronné, Partez à l'aventure.
Le joueur va parcourir l'aventure tutorielle jusqu'à ce qu'il finisse.
Lorsqu'il termine, le joueur est félicité et est invité à recommencer l'aventure pour essayer de nouveau choix.

Auteurs : 2TL1-5
"""
from lib.structures.scenario import Aventure


if __name__ == '__main__':
    path_scenario = './rsc/scenarios/tutoriel.json'
    aventure = Aventure(path_scenario)
    aventure.run()
