# IA_Framework_DefiIA


Link to the kaggle:
https://www.kaggle.com/competitions/defi-ia-2023/overview/description
## Commandes Docker

Vous pouvez directement créer une image Docker contenant tous les fichiers et requirements nécessaires pour lancer l'application gradio ou entrainer nos modèles. Après avoir cloné le repository sur votre machine, construisez une image puis un container en effectuant les commandes suivantes :

```
docker build -t [my_image_name] .
docker run -it --name [my_container_name] [my_image_name]
```

Pour lancer l'application gradio, faites la commande ```python app.py```. Un lien va s'afficher pour pouvoir ouvrir le gradio dans votre navigateur.
Pour entraîner le modèle de XGBoost, lancez ```python analysis/train.py```. Pour le modèle CatBoost lancez ```python analysis/train_catboost.py```.

Les 2 fichiers train enregistrent les prédictions dans ```data/submit/submit_from_train.csv``` pour XGBoost et ```data/submit/catboost.csv```. Les poids des modèles sont enregistrés dans ```model_from_train```et ```model_catboost``` dans le répertoire courant 


## Notre Projet

### Introduction

Dans ce rapport nous allons brièvement expliquer notre démarche et nos méthodes pour générer nos données, les traiter et effectuer des prédictions pour le Defi IA 2023 de Kaggle 


### Extraction

Notre objectif était dès le début de biaiser nos données pour coller au test\_set et ainsi avoir la meilleure prédiction possible sur celui-ci. Notre objectif premier était donc de s'inspirer de la distribution des données. Nous avons donc généré des requêtes suivant la distribution du test\_set, par exemple : si dans le test\_set 80\% des requêtes concernent un français alors on va nous aussi effectuer 80\% de nos requêtes sur des français.

Au fil des extractions nous avons mixé cette méthode avec de l'exploration pour combler les zones de vide. Pour cela nous avons d'abord fait quelques requêtes de manières complètement aléatoire puis nous avons regardé les zones encore peu ou pas explorées et nous avons créé des requêtes en partant des éléments manquants.

Pour tester notre statégie nous avons mis en place une méthode adversariale, celle ci consiste à labéliser les données comme appartenant au dataset test ou au dataset train et à essayer de prédire le dataset avec un algorithme simple. Si nous n'arrivons pas à prédire avec exactitude à quel dataset appartiennent les données alors elles sont similaires, sinon on a une différence notable. Malheureusement nous avons découvert cette technique assez tard et nous n'avons pas pu améliorer nos requêtes en nous basant là dessus. Nous arrivons à detecter les éléments du train dans 85\% des cas, ce qui est plutôt mauvais.

### Transformation

Nous avons essayé de trouver des informations qui pourraient être intéressantes pour la prédiction. Nous avons tout d'abord géré les variables qualitatives grâce à l'aide de 2 méthodes : le one hot encoding et le target encoding. Pour le target encoding nous avons considéré plusieurs fonctions pour encoder les données. Nous avons arrété notre choix à 3 fonctions : $mean$, $var$ et additive_smoothing. Cette dernière étant définie par $N\frac{x_i + \alpha}{N + d \alpha}$ avec $d = max(x) - min(x)$ et $\alpha$ le paramètre de smoothing.


Etude de l'importance de la langue :  
Lorsque l'on considère la langue comme une variable qualitative on observe qu'elle n'est pas très utile et qu'elle n'influe pas énormément sur le modèle. Nous avons en revanche remarqué que la langue influait de manière certaine mais sous une condition particulière. En effet, en moyenne un utilisateur qui fait une requête dans le pays de sa langue (un français en France par exemple) paie 2\% moins cher qu'un autre utilisateur. Le problème est que c'est une moyenne et nous ne pouvons pas simplement diminuer le prix des hôtels de 2\% après la prédiction. Nous avons donc créé un dictionnaire qui lie les langues au pays correspondant, ainsi nous avons pu créer une variable binaire valant 1 lorsque l'utilisateur demande un hôtel dans le pays de sa langue.


### Modèle

Nous avons utilisé des modèles prédictifs classiques tels que XGboost, LightGBM, GradientBoosting, RandomForest. Nous avons ensuite créé des ensembles de modèles en faisant la moyenne entre les différentes prédictions de nos meilleurs algorithmes.

## Packages

Tous les packages utiles pour le projet sont dans le fichier : requirements.txt

## Gradio

Vous pouvez utiliser une interface gradio pour essayer de faire des requêtes pour chercher un hotel. Sur la gauche, vous pouvez modifier les différents paramètres, vous observez ensuite le résultat de votre recherche dans le panneau de droite. Vous pouvez cliquer sur les boutons en bas pour essayer différents exemples.
