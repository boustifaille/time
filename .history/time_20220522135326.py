# les heures sont faites pour le tronc commun EM-TC 1BF
# V2.0
import datetime
import os, sys
import time
import socket
import tkinter as tk
from threading import Thread
import json

def recupHoraires():
    try:
        with open("time.json", "r") as fichier:
            data = json.load(fichier)
    except:
        data = {"horaires":{
            "matin":{
                "debut":"08:00",
                "fin":"12:00"
            },
            "aprem":{
                "debut":"14:00",
                "fin":"18:00"
            }
        }}
    return data["horaires"]


def estConnecte():
    """
    Retourne simplement si on est connecté à un reseau ou non.
    Retourne un booléen
    """
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
       pass
    return False

# si pyfiglet n'est pas installé le faire
if estConnecte():
    try:
        from pyfiglet import Figlet
    except ModuleNotFoundError:
        os.system("pip install pyfiglet" if sys.platform == "Win32" or "win32" or "win64" or "Win64" else "sudo apt install python3-pyfiglet")
        from pyfiglet import Figlet

def h_restantCalcul():
    """
    Détecte le jour ou on est et l'heure et retourne le temps restant en conséquence
    Partage des variables avec recolteH()
    Retourne une variable contenant le temps restant formaté proprement(heureRestante)
    
    """

    jourdelasemaine = datetime.datetime.today().weekday()
    jourouvrables = [0, 1, 2, 3, 4]

    # détecter si on est la semaine
    if jourdelasemaine not in jourouvrables:
        msg = "Il n'y a pas d'école aujourd'hui"
        os.system("exit()")
        heureRestante = 0
    # changer la fin des cours en fonction du jour de la semaine
    elif jourdelasemaine == 1: # si c'est mardi
        if recolteH.heureActuelle < '12:00:00': # si c'est le matin
            heureRestante = recolteH.d2-recolteH.d1
        elif recolteH.heureActuelle < '14:20:00': # si on est en elecnum
            heureRestante = recolteH.d4-recolteH.d1
        else:
            heureRestante = recolteH.d3-recolteH.d1 # l'après-midi
    elif jourdelasemaine == 3: # si c'est jeudi
        msg = "T'es en matu"
        heureRestante = 0
    else: # jours normaux
        # detecter si on est le matin ou l'après-midi et donnez le temps en conséquence
        if recolteH.heureActuelle > '12:00:00':
            heureRestante = recolteH.d3-recolteH.d1
        else:
        
            heureRestante = recolteH.d2-recolteH.d1
    return heureRestante

def h_avantP_calcul():
    """
    Calcul le temps avant la pause
    Partage variables avec recoltH
    Retourne l'heure avant la pause
    """
    
    jourdelasemaine = datetime.datetime.today().weekday()

    if recolteH.heureActuelle < '12:00:00': # si c'est le matin
        if jourdelasemaine in [2, 4]:#pratique
            h_avantP = recolteH.d5 - recolteH.d1
        elif jourdelasemaine in [0, 1]:#théorie
            h_avantP = recolteH.d5 - recolteH.d1
        else:
            h_avantP = 0
    elif recolteH.heureActuelle > '12:00:00': # si c'est l'après-midi
        if jourdelasemaine == 2:#pratique
            h_avantP = recolteH.d7 - recolteH.d1
        elif jourdelasemaine in [0, 1, 4]:#théorie
            h_avantP = recolteH.d7 - recolteH.d1
        else:
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
    recolteH.d1 = datetime.datetime.strptime(recolteH.heureActuelle, '%H:%M:%S')# maintenat
    recolteH.d2 = datetime.datetime.strptime(finMatin, '%H:%M:%S')    # fin matinée
    recolteH.d3 = datetime.datetime.strptime(finAPmidi, '%H:%M:%S')    # fin après midi

    recolteH.d5 = datetime.datetime.strptime(pauseMatin, '%H:%M:%S')    # Matin
    recolteH.d7 = datetime.datetime.strptime(pauseAPmidi, '%H:%M:%S')    # Après-midi

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
    while True:
        msg = recolteH()
        time.sleep(1)
        os.system("cls")
        print(msg)
        

if __name__ == '__main__':
    main()