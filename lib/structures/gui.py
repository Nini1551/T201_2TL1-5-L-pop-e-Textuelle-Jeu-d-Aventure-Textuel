"""
Fournit l'interface GUI du projet Epopée textuelle.

Par défaut, lance l'aventure tutorielle.
"""
import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from lib.structures.scenario import Aventure


class GuiGrid(GridLayout):
    """
    Fournit la structure de l'interface GUI du projet sous forme de grille d'éléments.
    Configure les différents éléments de l'interface.
    Introduit une aventure et prépare l'interface à son bon déroulement.
    """
    # IDs des widgets
    LABEL_TAG = 'display'
    INPUT_TAG = 'input'

    def __init__(self, aventure: Aventure, **kwargs):
        """
        Initialise l'interface GUI.
        PRE : - aventure: une aventure
        POST : Initialise l'interface GUI constituée de l'attribut suivant :
               - aventure : l'aventure qui sera jouée sur l'interface
               Configure les différents éléments de la page.
               Introduit l'aventure.
        """
        super().__init__(**kwargs)
        self.__aventure = aventure

        self.configure_interface()
        self.start_aventure()

    @property
    def aventure(self) -> Aventure:
        """
        Définit comme propriété l'attribut aventure de l'interface
        PRE : -
        POST : Renvoie l'aventure jouée par l'interface.
        """
        return self.__aventure

    def configure_interface(self):
        """
        Configure l'interface GUI.
        PRE : -
        POST : Définit le nombre de colonnes et de lignes de la structure de l'interface.
               Applique plusieurs widgets à l'interface :
               - Un label qui affichera la narration de l'aventure.
               - Une zone de texte où l'utilisateur pourra fournir ses choix.
                 Les choix seront vérifiés quand il validera sa réponse.
               Définit un dictionnaire des identifiants des widgets de la structure.
        """
        self.rows = 2
        self.cols = 1

        label = Label(size_hint=(1.0, 0.95))
        label.id = self.LABEL_TAG
        self.add_widget(label)

        text_input = TextInput(size_hint=(1.0, 0.05), multiline=False)
        text_input.bind(on_text_validate=self.make_choice)
        text_input.id = self.INPUT_TAG
        self.add_widget(text_input)

        self.ids = {child.id: child for child in self.children}

    def display_text(self, value, end: str = '\n'):
        """
        Affiche sur le label de narration un texte.
        PRE : - value : n'importe quelle valeur pouvant être traduite en chaîne de caractères
              - end : une chaîne de caractères
                      Par défaut, un retour à la ligne.
        POST : Affiche sur le label de narration, à la suite du texte précédent, un texte se clôturant par une expression de fin.
        """
        self.ids[self.LABEL_TAG].text += f"{str(value)}{end}"

    def start_aventure(self):
        """
        Introduit l'aventure sur l'interface GUI.
        PRE : -
        POST : Affiche l'introduction de l'aventure sur le label de narration.
               Active la zone de texte pour l'utilisateur.
        """
        self.display_text(self.aventure, end='\n\n')
        self.set_input_focus()

    def make_choice(self, source: TextInput):
        """
        Définit l'action à la validation de la zone de texte
        PRE : - source : une zone de texte
        POST : Vérifie si la valeur entrée par l'utilisateur est valide.
               Si oui, affiche la suite de la narration.
               Sinon, demande à l'utilisateur une valeur valide.
               Si un choix final est affiché, félicite le joueur.
               Si le dernier choix affiché est final, ferme la page.
               Active la zone de texte pour l'utilisateur.
        """
        if self.aventure.is_final_choice():
            sys.exit(0)

        congratulations = ("Félicitations ! Vous avez terminé l'aventure. \n"
                           "N'hésitez pas à redémarrer le programme pour tester les autres choix disponibles !")
        error_message = "Insérez un nombre entier valide !"

        answer = source.text
        try:
            self.aventure.main_choice = self.aventure.get_new_choice(answer)
            self.display_text(self.aventure, end='\n\n')

            if self.aventure.is_final_choice():
                self.display_text(congratulations)

        except ValueError:
            self.display_text(error_message, end='\n\n')

        source.text = ''
        self.set_input_focus()

    def set_input_focus(self):
        """
        Définit le focus sur la zone de texte de l'interface.
        PRE : -
        POST : Active la zone de texte pour l'utilisateur.
        """
        def _set_focus(instance):
            """
            Fonction anonyme qui définit le focus sur une instance.
            PRE : - instance : un widget
            POST : - Active l'instance pour l'utilisateur.
            """
            instance.focus = True

        source = self.ids[self.INPUT_TAG]
        Clock.schedule_once(lambda dt: _set_focus(source), 0.1)


class GuiApp(App):
    """
    Fournit l'application GUI de l'Epopée textuelle
    """
    def __init__(self, aventure: Aventure, **kwargs):
        """
        Initialise l'application GUI.
        PRE : - aventure: une aventure
        POST : Initialise l'application GUI constituée de l'attribut suivant :
               - aventure : l'aventure qui sera jouée sur l'interface
        """
        super().__init__(**kwargs)
        self.__aventure = aventure

    @property
    def aventure(self) -> Aventure:
        """
        Définit comme propriété l'attribut aventure de l'application.
        PRE : -
        POST : Renvoie l'aventure jouée par l'application.
        """
        return self.__aventure

    def build(self) -> GuiGrid:
        """
        Construit l'application.
        PRE : -
        POST : Définit le titre de l'application.
               Renvoie l'interface GUI de l'application.
        """
        self.title = 'Epopee temporelle'
        return GuiGrid(aventure=self.aventure)


if __name__ == '__main__':
    PATH = '../../rsc/scenarios/tutoriel.json'

    Window.maximize()
    GuiApp(Aventure(PATH)).run()
