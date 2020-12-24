#!/usr/bin/env python3
# coding: utf-8

# On importe le module
from monsql import *

# On utilise une variable pour plus de simplicité
m = MonSQL()

# Notre configuration à la base de données au format JSON
c = '{"utilisateur": "root", "mot_de_passe": "passwd", "hote": "172.17.0.2", "base_de_donnees":"mabase"}'

# On établi la connexion
conn = m.connecte_la_base(configuration=c)

# On fait une requête
req = "sélectionne id et nom et motdepasse àpartirde utilisateurs;"

# On l'exécute
r = m.requete_la_base(req)

# On affiche les résultats
print(f"Résultat de la requête :")
for (id, nom, motdepasse) in r:
    print(f"Utilisateur [{id}] : {nom} {motdepasse}")

# On ferme la connexion quand on n'en a plus besoin
m.ferme()
