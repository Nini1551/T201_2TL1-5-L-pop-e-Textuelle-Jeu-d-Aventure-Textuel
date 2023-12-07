# T201_2TL1-5-Lépopée-Textuelle-Jeu-d-Aventure-Textuel
T201 : Développement informatique II (Pratique) : Projet  
Groupe 2TL1-5 : DETILLEUX Bruno ; HUYBRECHTS Louis ; VERVAEREN Lucien  
  
L'Epopée textuelle est un système de narration où vous décidez quels seront les choix de votre personnage.  
Le prototype vous permet de parcourir une aventure tutorielle afin de bien comprendre les tenants et les aboutissants du concept.  

## Mode d'emploi : Partie formatage pour MJ
Afin de pouvoir ajouter un nouveau scénario/une nouvelle histoire il est impératif de respecter certaines normes de syntaxe.

Une histoire commence toujours par une introduction suivis de différents choix et sous-choix,etc.

¤ Pour le bloc introductif il faut respecter les règles suivantes :
- qui est représenter par un '.' suivi d'un espace et du nom de l'introduction)
- Ensuite après un retour à la ligne le texte introductif peut-être écrit.
- Un retour à la ligne peut être fait dans le texte.
ATTENTION : Pas plusieurs retour à la ligne d'affilé !


¤ Pour les blocs de choix cela fonctionne sur le principe de :
- Un numero de choix commence par un '.', termine par un '.' et à un '.' entre chaque 
chiffre composant le numéro de choix.
(ex: <<.2.>> Est le choix numéro 2 ; ex: <<.3.1.>> Est le sous-choix numéro 1 du choix numéro 3)
- Après le numéro de choix et un espace peut y avoir le nom de choix/sous-choix/sous-sous-choix/...
- Après un petit retour à la ligne, le texte du choix (ou sous-choix,...) peut être écrit
avec des retours à la ligne dans le texte ou non.
(comme pour l'introduction il ne peut pas y avoir plusieurs retour à la ligne d'affilé
  sinon fin de bloc)

¤ Pour terminer n'importe quel bloc (introductif ou choix ou sous-choix,...) il suffit de faire
  2 retours à la ligne d'affilé.

    Exemple de scénario s'intégrant bien :

    . Introduction
    Ceci est une introduction
    Et ici une phrase supplémentaire.

    .1. Choix 1
    Ceci est le premier choix
    Et ici une phrase supplémentaire.

    .2. Choix 2
    Ceci est le deuxième choix
    Et ici une phrase supplémentaire.

    .2.1. Sous-choix 1
    Ceci est le premier sous choix du choix 2
    Et ici une phrase supplémentaire.

    .2.2. Sous-choix 2
    Ceci est le deuxième sous choix du choix 2
    Et ici une phrase supplémentaire.

    .2.2.1. Sous-sous-choix
    Ceci est le premier sous choix du deuxième sous choix du choix 2
    Et ici une phrase supplémentaire.

    .3. Choix 3
    Ceci est le troisième choix
    Et ici une phrase supplémentaire.	
