#!/usr/bin/env python3
#coding: utf-8

import json, mysql.connector
from mysql.connector import errorcode


class MonSQL:

    """
    TODO: classe Erreur pour gérer les erreur dans un bon français
    """
    class Erreur:


        def __init__(self, *args):
            self.message = None
            if args:
                self.message = args[0]


        def __str__(self):
            if self.message:
                return f"Erreur MonSQL : {self.message}"
            else:
                return "Erreur MonSQL inconnue"


    """
    __init__ de la classe MonSQL
    """
    def __init__(self):
        print("MonSQL")
        self.configuration = {
            "utilisateur":"utilisateur",
            "mot_de_passe":"mot de passe",
            "hote":"127.0.0.1",
            "base_de_donnees":"basededonnees"
        }
        self.connexion = None


    """
    __str__ de la classe MonSQL
    """
    def __str__(self):
        return f"""Connexion à une base de données en MonSQL :
            hote : {self.configuration.hote}
            utilisateur : {self.configuration.utilisateur}
            base de donnees : {self.configuration.base_de_donnees}
            """
        

    """
    Réalise la connexion à la base de données par défaut,
    sinon utilise les données de connexion transmises
    """
    def connexion(self, configuration=None):
        une_connexion = None
        try:
            # configuration = '{"utilisateur":"","mot_de_passe":"","hote":"","base_de_donnees":""}'
            if configuration:
                self.configuration = json.loads(configuration)

            une_connexion = self.connecte_moi(
                                utilisateur = self.configuration["utilisateur"],
                                mot_de_passe = self.configuration["mot_de_passe"],
                                hote = self.configuration["hote"],
                                base_de_donnees = self.configuration["base_de_donnees"]
                            )
        except Exception as erreur:
            self.donne_lerreur(erreur)
        
        self.connexion = une_connexion
        return self.connexion


    """
    Essaie de se connecter à la base de données
    """
    def connecte_moi(self, utilisateur, mot_de_passe, hote, base_de_donnees):
        try:
            return mysql.connector.connect(
                        user = utilisateur,
                        password = mot_de_passe,
                        host = hote,
                        database = base_de_donnees
                    )
        except Exception as erreur:
            self.donne_lerreur(erreur)




    """
    Clos la connexion à la base de données
    """
    def ferme(self):
        try:
            self.connexion.close()
        except Exception as erreur:
            donne_lerreur(erreur)


    """
    TODO: traduire les requêtes MonSQL vers MySQL pour les exécuter
    Réalise la requête à la base de données
    """
    def requete_la_base(self, requete):
        pass


    """
    Fait la traduction des erreurs MySQL vers des erreurs en bon français
    """
    def donne_lerreur(self, erreur):
        monsql_erreur = "[Erreur MonSQL] Une erreur est survenue : "

        # Message d'erreur par défaut
        message_derreur = erreur

        if erreur.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            message_derreur = "accès non autorisé à la base de données"
        elif erreur.errno == errorcode.ER_BAD_DB_ERROR:
            message_derrur = "la base de données spécifiée n'existe pas"
    
        print(monsql_erreur + message_derreur)
        exit(1)

    
    """
    Réalise la requpete donnée avec le curseur donné
    """
    def requete_moi_ca(curseur, requete):
        try:
            return curseur.execute(requete)
        except Exception as erreur:
            self.donne_lerreur(erreur)


