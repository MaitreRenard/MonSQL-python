#!/usr/bin/env python3
#coding: utf-8

import json

import mysql.connector
from mysql.connector import errorcode


"""
Comment utiliser MonSQL :

ma_configuration = {"utilisateur": "michel", "mot_de_passe": "l4 p0uTr3", "hote": "127.0.0.1", "base_de_donnees": "mabase"}
mon_sql = MonSQL()
ma_connexion = mon_sql.connecte_la_base(ma_configuration)
ma_requete = "sélectionne tout àpartirde mabase"
mon_resultat = ma_connexion.requete_la_base(ma_requete)
mon_sql.ferme()
print(mon_resultat)
"""
class MonSQL:

    """
    TODO: classe Erreur pour gérer les erreur dans un bon français
    """
    class Erreur(Exception):

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
        self.DICTIONNAIRE = {'keywords': {'LARACINEDUCARRÉDE': 'ABS', 'LINTÉGRALITÉDE': 'ALL', 'MODIFIE': 'ALTER', 'AINSIQUE': 'AND', 'LUNDES': 'ANY', 'CONNUSOUSLENOMDE': 'AS', 'INCRÉMENTATIONAUTOMATIQUE': 'AUTO_INCREMENT', 'MOYENNE': 'AVG', 'INTERCALERENTRE': 'BETWEEN', 'CARACTÈRE': 'CHAR', 'VÉRIFIEQUE': 'CHECK', 'COMMETTRE': 'COMMIT', 'ASSEMBLER': 'CONCAT', 'CONTRAINTE': 'CONSTRAINT', 'DÉNOMBRE': 'COUNT', 'CRÉATIONDE': 'CREATE', 'JOINTURECROISÉE': 'CROSS JOIN', 'LABASEDEDONNÉE': 'DATABASE', 'SUPPRIME': 'DELETE', 'SANSDUPLICATIONS': 'DISTINCT', 'DIVISÉPAR': 'DIVIDE', 'JETTE': 'DROP', 'ESTPRÉSENTDANS': 'EXISTS', 'CLEFPASDECHEZNOUS': 'FOREIGN KEY', 'ÀPARTIRDE': 'FROM', 'AUTORISE': 'GRANT', 'LEPLUSGRANDDE': 'GREATEST', 'REGROUPERPAR': 'GROUP BY', 'AYANT': 'HAVING', 'SI': 'IF', 'DEDANS': 'IN', 'JOINTUREDUDEDANS': 'INNER JOIN', 'INSÉRER': 'INSERT', 'ENTIER': 'INT', 'ENTRECOUPEMENT': 'INTERSECT', 'ÀLINTÉRIEUR': 'INTO', 'EST': 'IS', 'LEPLUSPETITDE': 'LEAST', 'JOINTUREGAUCHE': 'LEFT JOIN', 'TAILLEDE': 'LENGTH', 'SEMBLABLEA': 'LIKE', 'MINUSCULER': 'LOWER', 'LECULMINANTDE': 'MAX', 'LEMOINDREDE': 'MIN', 'ÀLADIFFÉRENCEDE': 'MINUS', 'PAS': 'NOT', 'NÉANT': 'NULL', 'NOMBRE': 'NUMBER', 'LORSQUELON': 'ON', 'ORDONNERPAR': 'ORDER BY', 'OUBIEN': 'OR', 'PUISSANCE': 'POWER', 'CLEF': 'PRIMARY KEY', 'EMPÊCHE': 'RESTRICT', 'JOINTUREDROITE': 'RIGHT JOIN', 'RETOURENARRIÈRE': 'ROLLBACK', 'LARRONDIDE': 'ROUND', 'POINTDESAUVEGARDE': 'SAVEPOINT', 'SÉLECTIONNE': 'SELECT', 'DÉFINIT': 'SET', 'DORMIR': 'SLEEP', 'ADDITIONDETOUT': 'SUM', 'LATABLE': 'TABLE', 'LESTABLES': 'TABLES', 'TRONQUE': 'TRUNCATE', 'MISEENCONCUBINAGE': 'UNION', 'METÀJOUR': 'UPDATE', 'MAJUSCULER': 'UPPER', 'UTILISE': 'USE', 'VALEURS': 'VALUES', 'CARACTÈREVARIABLEVERSIONDEUX': 'VARCHAR2', 'VIDE': 'VOID', 'OÙ': 'WHERE', 'MONTREMOI': 'SHOW', 'MAINTENANT': 'SYSDATE'}, 'special_chars': {'CROISILLON': '#', 'ET': ',', 'TOUT': '*', 'VAUT': '=', 'STRICTEMENTINFÉRIEURÀ': '<', 'STRICTEMENTSUPÉRIEURÀ': '>', 'NEVAUTPAS': '<>', 'INFÉRIEUROUVAUT': '<=', 'SUPÉRIEUROUVAUT': '>='}}
        self.configuration = {
            "utilisateur":"utilisateur",
            "mot_de_passe":"mot de passe",
            "hote":"127.0.0.1",
            "base_de_donnees":"basededonnees"
        }
        self.connexion = None
        self.curseur = None


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
    def connecte_la_base(self, configuration=None):
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
        self.curseur = une_connexion.cursor()
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
            self.donne_lerreur(erreur)


    """
    Fait la traduction des erreurs MySQL vers des erreurs en bon français
    """
    def donne_lerreur(self, erreur):
        monsql_erreur = "[Erreur MonSQL] Une erreur est survenue : "

        # Message d'erreur par défaut
        message_derreur = str(erreur)

        if erreur == errorcode.ER_ACCESS_DENIED_ERROR:
            message_derreur = "accès non autorisé à la base de données"
        elif erreur == errorcode.ER_BAD_DB_ERROR:
            message_derreur = "la base de données spécifiée n'existe pas"

        print(monsql_erreur + message_derreur)
        exit(1)


    """
    Réalise la traduction MonSQL vers MySQL
    """
    def traduction(self, requete):
        # TODO: si il n'y a pas de point virgule à la fin de la requête initiale, le traducteur ne prend pas en compte le dernier mot de ladite requête (ie. sélectionne tout àpartirde utilisateurs → select * from)
        arreteurs = "\"'`"
        delimiteurs = " ;" + arreteurs

        traduction = ""
        en_cours = ""
        i = 0
        while i < len(requete):
            c = requete[i]
            if c in delimiteurs:
                if en_cours.upper() in self.DICTIONNAIRE["keywords"].values():
                    raise self.Erreur(en_cours)
                elif en_cours.upper() in self.DICTIONNAIRE["keywords"]:
                    traduction += self.DICTIONNAIRE["keywords"][en_cours.upper()]
                elif en_cours.upper() in self.DICTIONNAIRE["special_chars"]:
                    traduction += self.DICTIONNAIRE["special_chars"][en_cours.upper()]
                else:
                    traduction += en_cours
                traduction += c

                if c in arreteurs:
                    recherche = c
                    i += 1
                    while requete[i] != recherche:
                        traduction += requete[i]
                        i += 1
                    traduction += requete[i]

                en_cours = ''
            else:
                if c in self.DICTIONNAIRE["special_chars"]:
                    en_cours += self.DICTIONNAIRE["special_chars"][c]
                else:
                    en_cours += c
            i += 1

        return traduction


    """
    Réalise la requête donnée avec le curseur associé
    """
    def requete_la_base(self, requete):
        try:
            requete = self.traduction(requete)
            self.curseur.execute(requete)
            return self.curseur
        except Exception as erreur:
            self.donne_lerreur(erreur)

