# les heures sont faites pour le tronc commun EM-TC 1BF
# V1.3
import datetime
import os, sys
import time
import socket
from threading import Thread
import json

def recupHoraires() -> dict:
    """
    Récupère les horaires de la journée depuis le fichier horaires.json
    Retourne un dictionnaire
    """
    try:
        with open("horaires.json", "r") as fichier:
            data = json.load(fichier)
    except:
        data = {"horaires":{
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
        }}
    return data["horaires"]

def joursOuvrables() -> list[int]:
    try:
        with open("horaires.json", "r") as fichier:
                data = json.load(fichier)
    except:
        data = {"jours-ouvrables" : [0, 1, 2, 3, 4]}

    return data["jours-ouvrables"]

def getMidi() -> str:
    try:
        with open("horaires.json", "r") as fichier:
                data = json.load(fichier)
    except:
        data = {"midi" : "12:00:00"}

    return data["midi"]

def estConnecte()-> bool:
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

    # détecter si on est la semaine
    if jourdelasemaine not in jourouvrables:
        msg = "Il n'y a pas d'école aujourd'hui"
        heureRestante = 0
    elif jourdelasemaine == 3: # si c'est jeudi
        msg = "T'es en matu"
        heureRestante = 0
    else: # jours normaux
        # detecter si on est le matin ou l'après-midi et donnez le temps en conséquence
        if recolteH.heureActuelle > '12:00:00':
            heureRestante = recolteH.finAP-recolteH.now
        else:
        
            heureRestante = recolteH.finMatin-recolteH.now
    return heureRestante

def h_avantP_calcul() -> datetime.timedelta:
    """
    Calcul le temps avant la pause
    Partage variables avec recoltH
    Retourne l'heure avant la pause
    """
    jourdelasemaine = datetime.datetime.today().weekday()
    jourouvrables = joursOuvrables()

    if jourdelasemaine not in jourouvrables:
        h_avantP = 0

    else:
        if recolteH.heureActuelle < getMidi(): # si c'est le matin
            if recolteH.heureActuelle < recupHoraires()["matin"]["pause"]:
                h_avantP = recolteH.pauseMatin - recolteH.now
            else :
                h_avantP = 0
           
        elif recolteH.heureActuelle > getMidi(): # si c'est l'après-midi
            if recolteH.heureActuelle < recupHoraires()["apres-midi"]["pause"]:
                h_avantP = recolteH.pauseAP - recolteH.now
            else :
                h_avantP = 0
       

    return h_avantP
    

# affiche le temps restant
def recolteH():
    """
    Recolte les heures les formatte et les affiche
    """
    horaires = recupHoraires()

    pauseMatin = horaires["matin"]["pause"]
    finMatin = horaires["matin"]["fin"]

    pauseAPmidi = horaires["apres-midi"]["pause"]
    finAPmidi = horaires["apres-midi"]["fin"]

    # récolter les heures
    recolteH.heureActuelle = str(datetime.datetime.now().time().strftime('%H:%M:%S'))

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

    # Le montrer à l'utilisateur
    try:
        font = 'digital'
        f=Figlet(font)
        msg = f.renderText('Il reste : ' + str(heureRestante))
        msg = msg + f.renderText('Et ' + str(h_avantP) + ' avant la pause')
    except:
        msg = 'Il reste : '+str(heureRestante)
        msg = msg + '\nEt ' + str(h_avantP) + ' avant la pause'
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
    if estConnecte():
        try:
            from pyfiglet import Figlet
        except ModuleNotFoundError:
            os.system("pip install pyfiglet" if sys.platform == "Win32" or "win32" or "win64" or "Win64" else "sudo apt install python3-pyfiglet")
            from pyfiglet import Figlet
    main()