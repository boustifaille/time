# les heures sont faites pour le tronc commun EM-TC 1BF
# V1.3
import datetime
import os, sys
import time
import socket
import json

"""
TODO 
- gestion des erreurs genre si la pause est deja passée
- trouver un meilleure moyen de passer les variables que avec 'recolteH.'
"""

def getHoraires() -> dict:
    """
    Récupère les horaires de la journée depuis le fichier horaires.json
    Retourne un dictionnaire
    """
    try:
        with open("horaires.json", "r") as fichier:
            data = json.load(fichier)["horaires"]
    except:
        data = {
            "matin":{
                "debut":"08:00:00",
                "pause":"10:00:00",
                "fin":"12:00:00"
            },
            "apres-midi":{
                "debut":"14:00:00",
                "pause":"16:00:00",
                "fin":"18:00:00"
            }
        }
    return data

def joursOuvrables() -> list[int]:
    try:
        with open("horaires.json", "r") as fichier:
                data = json.load(fichier)["jours-ouvrables"]
    except:
        data = [0, 1, 2, 3, 4]

    return data

def getMidi() -> str:
    try:
        with open("horaires.json", "r") as fichier:
                data = json.load(fichier)["midi"]
    except:
        data = "12:00:00"

    return data

def estConnecte() -> bool:
    """
    Retourne simplement si on est connecté à internet ou non.
    Retourne un booléen
    """
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
       pass
    return False

def h_restantCalcul() -> datetime.timedelta: 
    """
    Détecte le jour ou on est et l'heure et retourne le temps restant en conséquence
    Partage des variables avec recolteH()
    Retourne une variable contenant le temps restant formaté proprement(heureRestante)
    
    """

    jourdelasemaine = datetime.datetime.today().weekday()
    jourouvrables = joursOuvrables()
   
    heureRestante = '00:00:00'

    # détecter si on est la semaine
    if jourdelasemaine not in jourouvrables:
        msg = "Il n'y a pas d'école aujourd'hui"
    elif jourdelasemaine == 2: # si c'est mercredi
        msg = "T'es en matu"
    else: # jours normaux
        # detecter si on est le matin ou l'après-midi et donnez le temps en conséquence
        if recolteH.heureActuelle > getMidi() and recolteH.heureActuelle < horaires["apres-midi"]["fin"]:
            heureRestante = recolteH.finAP - recolteH.now
        elif recolteH.heureActuelle < getMidi() and recolteH.heureActuelle > horaires["matin"]["fin"]:
            heureRestante = recolteH.finMatin - recolteH.now
            
    return heureRestante

def h_avantP_calcul() -> str:
    """
    Calcul le temps avant la pause
    Partage variables avec recoltH
    Retourne l'heure avant la pause
    TODO trouver un moyen d'afficher les erreurs pour l'instant retourne '00:00:00'
    """
    jourdelasemaine = datetime.datetime.today().weekday()
    jourouvrables = joursOuvrables()

    if jourdelasemaine not in jourouvrables:
        # TODO trouver un moyen d'afficher les erreurs
        return '00:00:00'


    if recolteH.heureActuelle < getMidi(): # si c'est le matin
        if recolteH.heureActuelle > horaires["matin"]["pause"]: # la pause est deja passée
            return '00:00:00'
        
        # c'est un timedelta il faut le convertir en datetime
        h_avantP = recolteH.pauseMatin - recolteH.now
        h_avantP = datetime.datetime.strptime(str(h_avantP), "%H:%M:%S")
        h_avantP = h_avantP.strftime("%H:%M:%S")
        
    else : # si c'est l'après-midi
        if recolteH.heureActuelle > horaires["apres-midi"]["pause"]: # la pause est deja passée
            return '00:00:00'
        
        # c'est un timedelta il faut le convertir en datetime
        h_avantP = recolteH.pauseAP - recolteH.now
        h_avantP = datetime.datetime.strptime(str(h_avantP), "%H:%M:%S")
        h_avantP = h_avantP.strftime("%H:%M:%S")

    return h_avantP
    

# affiche le temps restant
def recolteH() -> str:
    """
    Recolte les heures et les formatte
    """

    pauseMatin = horaires["matin"]["pause"]
    finMatin = horaires["matin"]["fin"]

    pauseAPmidi = horaires["apres-midi"]["pause"]
    finAPmidi = horaires["apres-midi"]["fin"]

    # récolter les heures
    recolteH.heureActuelle = datetime.datetime.now().time().strftime('%H:%M:%S')
    

    # formater proprement les heures
    recolteH.now = datetime.datetime.strptime(recolteH.heureActuelle, '%H:%M:%S')# maintenat
    recolteH.finMatin = datetime.datetime.strptime(finMatin, '%H:%M:%S')    # fin matinée
    recolteH.finAP = datetime.datetime.strptime(finAPmidi, '%H:%M:%S')    # fin après midi

    recolteH.pauseMatin = datetime.datetime.strptime(pauseMatin, '%H:%M:%S')    # Matin
    recolteH.pauseAP = datetime.datetime.strptime(pauseAPmidi, '%H:%M:%S')    # Après-midi

    # défini le temps restant
    heureRestante = h_restantCalcul()
    # temps restant avant la pause
    h_avantP = h_avantP_calcul()

    # Le formatter dans une string
    try:
        font = 'digital'
        f=Figlet(font)
        msg = f.renderText('Il reste : ' + str(heureRestante))
        msg += f.renderText('Et ' + str(h_avantP) + ' avant la pause')
    except:
        msg = 'Il reste : '+str(heureRestante)
        msg += '\nEt ' + str(h_avantP) + ' avant la pause'

    return msg
        
def main():
    """
    Fonction principale
    """
    while True:
        msg = recolteH()
        time.sleep(1)
        os.system("cls")
        print(msg)
        

if __name__ == '__main__':
    # si pyfiglet n'est pas installé le faire
    try:
        from pyfiglet import Figlet
    except ModuleNotFoundError:
        if estConnecte():
            os.system("pip install pyfiglet")
            from pyfiglet import Figlet
    horaires = getHoraires()
    main()
