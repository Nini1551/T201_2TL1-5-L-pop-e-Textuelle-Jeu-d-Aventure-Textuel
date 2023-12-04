"""
En tant que joueur débutant ou chevronné, Partez à l'aventure.
Le joueur va parcourir l'aventure tutorielle jusqu'à ce qu'il finisse.
Lorsqu'il termine, le joueur est félicité et est invité à recommencer l'aventure pour essayer de nouveau choix.

Auteurs : 2TL1-5
"""
import argparse
from lib.structures.scenario import Aventure

if __name__ == '__main__':
    DEFAULT_PATH = './rsc/scenarios/tutoriel.json'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path_scenario',
        help='le chemin du fichier JSON du scénario',
        nargs='?',
        default=DEFAULT_PATH
    )
    parser.add_argument(
        '--gui',
        help='Exécute le programme via une interface graphique utilisateur.',
        action='store_true'
    )
    args = parser.parse_args()

    aventure = Aventure(args.path_scenario)
    if args.gui:
        from kivy.core.window import Window
        from lib.structures.gui import GuiApp

        Window.maximize()
        GuiApp(aventure).run()
    else:
        aventure.run()
