
# Application de Suivi de Dépenses

L'application permet de gérer ses dépenses grâce à plusieurs graphiques et un tableau de dépenses afin de toujours garder un oeil sur son argent.

## Lancement

Pour lancer le projet, il suffit d'exécuter le fichier **main.py**

## Structure du Projet

- `main.py` : Point d'entrée principal de l'application. Initialise la base de données, configure la session, les thèmes (mode sombre / clair), la navigation, et redirige vers les différentes pages.
- `dashboard.py` : Gère la page principale du tableau de bord. Affiche les graphiques (camembert et barres) des dépenses par catégorie et dans le temps. Intègre aussi des filtres dynamiques par année, semaine, et catégorie. Adapté aux mobiles avec responsive design.
- `expenses.py` : Page listant toutes les dépenses. Contient des filtres par date (année, semaine), et catégorie. Présente les données dans un tableau interactif avec actions de modification et suppression.
- `edit_expenses.py` : Contient les pages pour ajouter, modifier, et supprimer une dépense individuelle. Chaque opération est réalisée via des formulaires avec validation.
- `categories.py` : Génère un graphique en camembert basé sur la répartition des dépenses par catégorie. Fournit une vue analytique dédiée à la gestion des catégories.
- `db.py` : Définit les modèles de base de données (Expense, Category) via SQLModel, ainsi que les fonctions utilitaires de lecture agrégée (ex : groupement par date, total par catégorie).
- `layout.py` *(optionnel)* : Servait à encapsuler une structure commune (barre de navigation, layout général). Peut être supprimé si plus utilisé.
- `budget.db` Fichier SQLite contenant les données persistantes des dépenses et des catégories. Généré automatiquement si absent.

## Technologies

- [Flet](https://flet.dev) pour l’interface utilisateur
- [Matplotlib](https://matplotlib.org/) pour les graphiques
- [SQLModel](https://sqlmodel.tiangolo.com/) pour la base de données SQLite
- Python 3.13

## Bugs de l'application
Il y a certains bugs que je n'ai pas réussi à résoudre:
1. On ne peut pas scroller horizontalement dans le tableau du fichier **expenses.py** ce qui gène l'affichage en cas de petit écran.
2. Quand on utilise les filtres, la barre en haut disparaît. Pour la faire réapparaître, il faut descendre en bas et appuyer, sur le bouton **Voir catégorie** ou **Retour**. Le fichier **layout.py** avait pour objectif de résoudre ce problème mais je n'ai pas réussi à le mettre correctment en place.
3. Quand on supprime une catégorie, il faut changer de page pour que le changement prenne effet.