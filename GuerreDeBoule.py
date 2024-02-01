################# IMPORTS #################
from math import sqrt
from time import *
from random import randint
from upemtk import *
import json
################# IMPORTS #################


################# FONCTIONS #################
def touche_ou_non(lst, x, y, r): 
    """
    Renvoie False si le cercle dont on entre les coordonnées est en contact avec un cercle déjà existant et True sinon.
    """
    for i in range(len(lst)):
        if (sqrt(((lst[i][1] - y)**2) +((lst[i][0] - x))**2 ) <= (lst[i][3])+ r ) and sqrt(((lst[i][1] - y)**2) +((lst[i][0] - x))**2 ) > lst[i][3]:
            return False
        else:
            continue
    return True

def clic_interieur_ou_non(lstcoor, x, y): 
    """
    Renvoie le rang du couple de coordonnées dans la liste de coordonnées si le clic du joueur se trouve à l'intérieur d'un cercle déjà posé par son adversaire et None sinon.
    """
    for i in range(len(lstcoor)):
        if sqrt(((lstcoor[i][1] - y)**2) +((lstcoor[i][0] - x))**2 ) > lstcoor[i][3] :
            continue
        else:
            return i
    return None

def dans_aire_de_jeu(x, y, rayon):
    """
    Renvoie True si le cercle se trouve entièrement dans l'aire de jeu et False sinon.
    """
    if x < rayon or x > longueur_fenetre - rayon or y < rayon or y > hauteur_fenetre - rayon or (180 - rayon < x < 420 + rayon and y < 80 + rayon) :
        return False
    else:
        return True

def division_cercle(x, y, lst):
    """
    Renvoie un tuple contenant la position des informations sur le cercle concerné dans la liste prise en paramètre, l'abcisse du centre du cercle tengeant au cercle d'origine et au cercle 
    nouvellement déposé, l'ordonnée de ce même cercle, le rayon de ce cercle et le rayon du cercle nouvellement posé. 
    """
    rang = clic_interieur_ou_non(lst, x, y)                             # Position des informations sur le cercle cliqué dans la liste 
    efface(lst[rang][2])                                                # On efface ce cercle  
    
    d = sqrt((lst[rang][0]-x)**2 + (lst[rang][1]-y1)**2)                
    r1 = lst[rang][3] - d                                               # Rayon du cercle se situant au clic
    xn = 0
    yn = 0
    hypothénuse = sqrt(r1**2+d**2)
    if hypothénuse == 0: 
        return rang, x, y, r1, d
    else :
        cosinus = d / hypothénuse
        sinus = r1 / hypothénuse                                            # Règles trigonométriques qui permettent de trouver la position du centre du cercle qui va se créer

        if lst[rang][0] != x and lst[rang][1] != y:                         # Si on ne clique pas au centre du cercle déjà présent : 
            # Division du cercle en 4 parties et calcul des coordonnées dans chaque cas
            if x > lst[rang][0] and y > lst[rang][1] :
                xn = lst[rang][0] - (r1 * cosinus)
                yn = lst[rang][1] - (r1 * sinus)

            elif x < lst[rang][0] and y < lst[rang][1] :
                xn = lst[rang][0] + (r1 * cosinus)
                yn = lst[rang][1] + (r1 * sinus)

            elif x > lst[rang][0] and y < lst[rang][1] :
                xn = lst[rang][0] - (r1 * cosinus)
                yn = lst[rang][1] + (r1 * sinus) 

            elif x < lst[rang][0] and y > lst[rang][1] :
                xn = lst[rang][0] + (r1 * cosinus)
                yn = lst[rang][1] - (r1 * sinus)
            
            return rang, xn, yn, r1, d 
        else:                                                                   # Sinon, les coordonnées ne son pas changée
            return rang, x, y, r1, d
 
def score(lst):
    """
    Renvoie le score d'un joueur en vérifiant, pour chaque pixel de l'aire de jeu, si il se situe dans un cercle enrengistré dans la liste d'un joueur.
    """
    result = 0
    for x in range(601):
        for y in range(601):
            booleen = True 
            for i in range(len(lst)):
                if (x <= lst[i][0] + lst[i][3] and x >= lst[i][0] - lst[i][3]) and (y <= lst[i][0] + lst[i][3] and y >= lst[i][0] - lst[i][3]) and booleen == True :
                    result += 1
                    booleen = False
    return result 

def ecran_de_fin(score1,score2):
    """
    Affiche un écran de fin selon les différents cas possibles : la victoire du joueur 1, celle du joueur 2 ou une égalité.
    """
    if score1 > score2:
        rectangle(100,225,500,375,remplissage='white', couleur='black')
        texte(300, 300, "VICTOIRE DE "+ joueur1.upper() + ' !',ancrage='center',couleur="black", taille=20, police='Helvetica')
    if score1 < score2:
        rectangle(100,225,500,375,remplissage='white',couleur='black')
        texte(300, 300, "VICTOIRE DE "+ joueur2.upper() + ' !',ancrage='center', couleur="black", taille=20, police='Helvetica')
    if score1 == score2 :
        rectangle(100,225,500,375,remplissage='white',couleur='black')
        texte(300, 300, "ÉGALITÉ !",ancrage='center', couleur="black", taille=20, police='Helvetica')

def perte_tour(motif):
    """
    Permet d'afficher un message en cas de perte d'un tour d'un joueur.
    """
    rectangle(100,225,500,375,remplissage='white',couleur='black', tag='tourperdu')
    texte(300, 280, "TOUR PERDU !",ancrage='center', couleur="black", taille=20, police='Helvetica', tag='tourperdu')
    texte(300, 3000, motif,ancrage='center', couleur="black", taille=18, police='Helvetica', tag='tourperdu')
    texte(300, 360, "Cliquez pour continuer",ancrage='center', couleur="black", taille=15, police='Helvetica', tag='tourperdu')
    attente_clic()
    efface('tourperdu')

def attente_click_jusqua(milliseconds):
    """
    On attend un clic dans un temps imparti en milisecondes, si on clique avant la fonction renvoie les coordonnées aux quelles on a cliqué sinon on retourne
    un tuple à trois éléments None
    """
    t1 = time()+milliseconds/1000
    while time()< t1 :
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "ClicDroit" or type_ev == "ClicGauche" :
            return clic_x(ev), clic_y(ev), type_ev
        mise_a_jour()
    return(None,None,None)

def menu():
    """
    Affiche un menu lorsque l'on lance le jeu et renvoie une valeur selon le clic du joueur.
    """
    # Jouer
    rectangle(0,0,599,200,couleur='black',remplissage='white',tag = 'menu')
    texte(300,100, 'LANCER UNE PARTIE',ancrage='center', taille=30)

    # Règles 
    rectangle(0,200,599,400,couleur='white',remplissage='black',tag = 'menu')
    texte(300, 300, 'RÈGLES DU JEU',couleur='white', ancrage='center', taille=30)

    # Classement 
    rectangle(0,400,599, 599,couleur='black',remplissage='white',tag = 'menu')
    texte(300,500, 'CLASSEMENT DES JOUEURS',ancrage='center', taille=30)
    x,y,w = attente_clic()
    if 0 <= y < 200 :
        efface_tout()
        return 'choixjeu'
        
    elif 200 <= y <400 :
        efface_tout()
        return 're'
    elif 400 <= y < 600 :
        efface_tout()
        return 'class'

def choix_jeu():
    """
    Affiche et renvoie le choix du joueur, soit continuer la dernière partie, soit en commencer une nouvelle.
    """
    rectangle(0,0,600,100,remplissage="black", tag='cj')
    texte(300,50,'SOUHAITEZ VOUS :', taille=20, ancrage='center', couleur='white', tag='cj')
    rectangle(0,100,600,350, remplissage="white", tag='cj')
    texte(300,225, """CONTINUER LA DERNIERE PARTIE
ENRENGISTREE""", taille=20, ancrage='center', tag='cj')
    rectangle(0,350,600,600, remplissage="white", tag='cj')
    texte(300,475, 'COMMENCER UNE NOUVELLE PARTIE', taille=20, ancrage='center', tag='cj')
    a,b,c = attente_clic()
    if 100<=b<=350 :
        efface('cj')
        return "jeusauv"
    elif 350<=b<=600 :
        efface('cj')
        return "jeunv"

def variante(resu):
    """
    Affiche soit les variantes ou les règles du jeu selon la valeur du paramètre. 
    On implémentera un paramètre qui renverra un fichier avec le classement des joueurs.
    Renvoie un tuple de booléens dans un cas ou affiche simplement des informations.
    """
    if resu == 'jeunv':
        rectangle(0,0,599,85,couleur='black',remplissage='black',tag = 'var')
        texte(300,42.5, 'CHOIX DES VARIANTES', couleur='white',ancrage='center', taille=27, tag='var')

        sab = False
        rectangle(0,85,599,170,couleur='black',remplissage='white',tag = 'var')
        texte(300,127.5, 'SABLIER',ancrage='center', taille=20, tag='var')
        texte(300, 147.5, "Chaque joueur a un temps prédéterminé pour jouer à chaque tour ; s’il ne réagit pas à temps, il perd son tour", ancrage='center', taille=8, tag='var')

        sco = False
        rectangle(0,170,599,255,couleur='black',remplissage='white',tag = 'var')
        texte(300,212.5, 'SCORES',ancrage='center', taille=20, tag='var')
        texte(300, 232.5, "Un joueur peut vérifier quelle aire ses boules totalisent à chaque instant en appuyant sur la touche ’s’", ancrage='center', taille=8, tag='var')

        tdb = False
        rectangle(0,255,599,340,couleur='black',remplissage='white',tag = 'var')
        texte(300,287.5, 'TAILLE DES BOULES',ancrage='center', taille=20, tag='var')
        texte(300, 317.5, "Chaque joueur commence avec un certain budget fixé au préalable, et pour chaque boule\n      posée, il choisit son rayon puis son budget diminue du rayon de la boule qu’il pose.", ancrage='center', taille=8, tag='var')

        vdy = False
        rectangle(0,340,599,425,couleur='black',remplissage='white',tag = 'var')
        texte(300,372.5, 'VERSION DYNAMIQUE',ancrage='center', taille=20, tag='var')
        texte(300, 402.5, "Les rayons de toutes les boules s’incrémentent à chaque tour en respectant les règles données,\n         dès que deux boules de couleurs différentes se touchent, elles arrêtent de grandir.", ancrage='center', taille=8, tag='var')

        ter = False
        rectangle(0,425,599,510,couleur='black',remplissage='white',tag = 'var')
        texte(300,467.5, 'TERMINAISON',ancrage='center', taille=20, tag='var')
        texte(300, 487.5, "Chaque joueur peut, quand il souhaite, appuyer sur 'e' et faire en sorte que la partie se termine dans 5 tours.", ancrage='center', taille=8, tag='var')

        obs = False
        rectangle(0,510,599,600,couleur='black',remplissage='white',tag = 'var')
        texte(300,552.5, 'OBSTACLES',ancrage='center', taille=20, tag='var')
        texte(300, 572.5, "le tableau commence avec certains obstacles que les boules ne peuvent pas toucher.", ancrage='center', taille=8, tag='var')

        rectangle(520,0,600,50, couleur='black', remplissage='purple', tag='jouer')
        texte(560,25,'JOUER', taille='17', couleur='white', ancrage='center')


        boo = True
        while boo == True :
            a,y,z = attente_clic()
            if 85 <= y <= 170 :
                sab = not(sab)  
                if sab == False:
                    rectangle(0,85,599,170,couleur='black',remplissage='white',tag = 'var')
                    texte(300,127.5, 'SABLIER',ancrage='center', taille=20, tag='var')
                    texte(300, 147.5, "Chaque joueur a un temps prédéterminé pour jouer à chaque tour ; s’il ne réagit pas à temps, il perd son tour", ancrage='center', taille=8, tag='var')
                else :
                    rectangle(0,85,599,170,couleur='black',remplissage='purple',tag = 'var')
                    texte(300,127.5, 'SABLIER',ancrage='center', taille=20, tag='var')
                    texte(300, 147.5, "Chaque joueur a un temps prédéterminé pour jouer à chaque tour ; s’il ne réagit pas à temps, il perd son tour", ancrage='center', taille=8, tag='var')
            
            if 170 <= y <= 255 :
                    sco = not(sco)  
                    if sco == False:
                        rectangle(0,170,599,255,couleur='black',remplissage='white',tag = 'var')
                        texte(300,212.5, 'SCORES',ancrage='center', taille=20, tag='var')
                        texte(300, 232.5, "Un joueur peut vérifier quelle aire ses boules totalisent à chaque instant en appuyant sur la touche ’s’", ancrage='center', taille=8, tag='var')

                    else :
                        rectangle(0,170,599,255,couleur='black',remplissage='purple',tag = 'var')
                        texte(300,212.5, 'SCORES',ancrage='center', taille=20, tag='var')
                        texte(300, 232.5, "Un joueur peut vérifier quelle aire ses boules totalisent à chaque instant en appuyant sur la touche ’s’", ancrage='center', taille=8, tag='var')

            if 255 <= y <= 340 :
                    tdb = not(tdb)  
                    if tdb == False:
                        rectangle(0,255,599,340,couleur='black',remplissage='white',tag = 'var')
                        texte(300,287.5, 'TAILLE DES BOULES',ancrage='center', taille=20, tag='var')
                        texte(300, 317.5, "Chaque joueur commence avec un certain budget fixé au préalable, et pour chaque boule\n      posée, il choisit son rayon puis son budget diminue du rayon de la boule qu’il pose.", ancrage='center', taille=8, tag='var')

                    else :
                        rectangle(0,255,599,340,couleur='black',remplissage='purple',tag = 'var')
                        texte(300,287.5, 'TAILLE DES BOULES',ancrage='center', taille=20, tag='var')
                        texte(300, 317.5, "Chaque joueur commence avec un certain budget fixé au préalable, et pour chaque boule\n      posée, il choisit son rayon puis son budget diminue du rayon de la boule qu’il pose.", ancrage='center', taille=8, tag='var')

            if 340 <= y <= 425 :
                    vdy = not(vdy)  
                    if vdy == False:
                        rectangle(0,340,599,425,couleur='black',remplissage='white',tag = 'var')
                        texte(300,372.5, 'VERSION DYNAMIQUE',ancrage='center', taille=20, tag='var')
                        texte(300, 402.5, "Les rayons de toutes les boules s’incrémentent à chaque tour en respectant les règles données,\n         dès que deux boules de couleurs différentes se touchent, elles arrêtent de grandir.", ancrage='center', taille=8, tag='var')

                    else :
                        rectangle(0,340,599,425,couleur='black',remplissage='purple',tag = 'var')
                        texte(300,372.5, 'VERSION DYNAMIQUE',ancrage='center', taille=20, tag='var')
                        texte(300, 402.5, "Les rayons de toutes les boules s’incrémentent à chaque tour en respectant les règles données,\n         dès que deux boules de couleurs différentes se touchent, elles arrêtent de grandir.", ancrage='center', taille=8, tag='var')
                        
            if 425 <= y <= 510 :
                    ter = not(ter)  
                    if ter == False:
                        rectangle(0,425,599,510,couleur='black',remplissage='white',tag = 'var')
                        texte(300,467.5, 'TERMINAISON',ancrage='center', taille=20, tag='var')
                        texte(300, 487.5, "Chaque joueur peut, quand il souhaite, appuyer sur 'e' et faire en sorte que la partie se termine dans 5 tours.", ancrage='center', taille=8, tag='var')

                    else :
                        rectangle(0,425,599,510,couleur='black',remplissage='purple',tag = 'var')
                        texte(300,467.5, 'TERMINAISON',ancrage='center', taille=20, tag='var')
                        texte(300, 487.5, "Chaque joueur peut, quand il souhaite, appuyer sur 'e' et faire en sorte que la partie se termine dans 5 tours.", ancrage='center', taille=8, tag='var')

            if 510 <= y <= 600 :
                    obs = not(obs)  
                    if obs == False:
                        rectangle(0,510,599,600,couleur='black',remplissage='white',tag = 'var')
                        texte(300,552.5, 'OBSTACLES',ancrage='center', taille=20, tag='var')
                        texte(300, 572.5, "le tableau commence avec certains obstacles que les boules ne peuvent pas toucher.", ancrage='center', taille=8, tag='var')

                    else :
                        rectangle(0,510,599,600,couleur='black',remplissage='purple',tag = 'var')
                        texte(300,552.5, 'OBSTACLES',ancrage='center', taille=20, tag='var')
                        texte(300, 572.5, "le tableau commence avec certains obstacles que les boules ne peuvent pas toucher.", ancrage='center', taille=8, tag='var')
            if 520 <= a <= 600 and 0 <= y <= 50 :
                efface_tout()
                boo = False

        return sab, sco, tdb, vdy, ter, obs


    if resu == 're' :
        rectangle(10,10,590,590, remplissage='white', tag='reg')
        rectangle(255,15,355,45,couleur='white', remplissage='black', tag='reg')
        rectangle(250,10,350,40,couleur='white', remplissage='black', tag='reg')
        texte(300,25, 'REGLES',couleur='white',ancrage='center', taille=18, tag='reg')

        texte(300,100, 'BALLS GAME !',couleur='purple',ancrage='center', taille=50, police='Eras Bold ITC', tag='reg')

        rectangle(30,150,570,300,couleur='white', remplissage='black', tag='reg')
        texte(35,150, """DEUX JOUEURS JOUENT SUR LA MEME MACHINE
LE BUT EST DE RECOUVRIR UNE PLUS GRANDE SURFACE QUE SON ADVERSAIRE
DEUX CHOIX S'OFFRENT A EUX :
	SOIT ILS POSENT UN CERCLE
CELA PERMET D'AUGMENTER SON SCORE, CAR PLUS IL Y A DE CERCLES, 
PLUS ON GAGNE DE POINT !
	SOIT ILS DIVISENT UN CERCLE ADVERSE
CELA PERMET DE DIMINUER LE SCORE DE L'ADVERSAIRE, AU PERIL DE NE 
PAS AUGMENTER LE SIEN !""",couleur='white',ancrage='nw', taille=10, tag='reg')

        rectangle(30,350,570,500,couleur='white', remplissage='black', tag='reg')
        texte(35,350, """
CHOIX DES VARIANTES : 
	LORSQUE VOUS LANCEZ LE JEU, UN CHOIX S'OFFRE A VOUS, VOUS 
POUVEZ CHOISIR DE JOUER AVEC DES VARIANTES OU NON. 

	CERTAINES VARIANTES NECESSISTENT UNE SAISIE DANS LE TERMINAL, 
A VOUS DE DECIDER COMMENT SE PASSERA VOTRE PARTIE !

BONNE CHANCE !""",couleur='white',ancrage='nw', taille=10, tag='reg')

        rectangle(510,540,590,590,couleur='black',remplissage='black',tag = 'reg')
        polygone([(540,555),(540,575),(560,565)],couleur='green',remplissage='green', tag='reg')
        texte(550,565, 'JOUER',couleur='white',ancrage='center', taille=15, tag='reg')

        

        x, y, z = attente_clic()
        if 510 < x < 590 and 540 < y < 590:
            return 'choixjeu'
    
    
       

def ecran_lancement():
    """
    Affiche un écran de lancement.
    """
    rectangle(0,0,600,600,couleur='purple', remplissage='purple', tag='lancement')
    cercle(300,200,50,'white','white', tag='lancement' )
    cercle(350,150,20,'white','white', tag='lancement')
    texte(600//2,600//2, 'BALLS GAME !',couleur='white',ancrage='center', taille=60, police='Eras Bold ITC', tag='lancement')

def affichage_constant():
    """
    Affiche une interface lors de la partie. 
    """
    rectangle(180,0,420,30, couleur='black', remplissage='purple', tag='aff')
    rectangle(180,30,420,60, couleur='black', remplissage='purple', tag='aff')
    rectangle(180,30,300,60, couleur='black', remplissage=color_joueur1, tag='aff')
    rectangle(300,30,420,60, couleur='black', remplissage=color_joueur2, tag='aff')
    rectangle(180,60,420,80,remplissage='purple',tag='aff')
    texte(300,70, 'PAUSE', taille=10,ancrage='center')
    
def agrandissement_cercles(lst, color): 
    """
    Affiche les cercles qui ont un rayon grandissant de plus en plus (un pixel) à chaque tour. 
    """
    for infos in lst: 
        if 't' not in infos[2]:
            infos[3] += 1
            efface(infos[2])
            cercle(infos[0],infos[1],infos[3],couleur=color, remplissage=color, tag=infos[2]) 

def touche_ou_non_aggrandissement(lst_a_verif, lst_compar) : 
    """
    Permet de savoir si les cercles, lorsqu'ils grandissent, se touchent et de les marquer pour qu'ils ne se touchent plus.
    """
    for i in range(len(lst_a_verif)):
        if touche_ou_non(lst_compar, lst_a_verif[i][0], lst_a_verif[i][1], lst_a_verif[i][3]) == False :
            lst_a_verif[i][2] = lst_a_verif[i][2] + 't'
        
def var_score():
    """
    Si, dans les 1 seconde après que ce soit notre tour, on appuie sur la touche 's', les scores des joueurs sont affichés pendant un petit lapse de temps.
    """
    s = attente_touche_jusqua(1000)
    if s == 's' :
        texte(240,45,str(score(liste_j1)),ancrage='center', tag='sc', taille=12)
        texte(360,45, str(score(liste_j2)),ancrage='center', tag='sc', taille=12)
        mise_a_jour()
        t = time()+ 2
        while time() < t :
            continue
        efface('sc')
        mise_a_jour()
    else :
        pass

def obstacle() :
    """
    Crée des coordonnées pour les obstacles ainsi qu'un rayon. 
    """
    x = randint(50,550)
    y = randint(50,550)
    r = randint(20,50)
    return x, y, r

def choix_nombre_manches():
    """
    Affiche un menu cliquable permettant de choisir le nombre de manches (entre 5 et 25)
    """
    rectangle(0,0,599,100,couleur='black',remplissage='black',tag = 'var')
    texte(300,50, 'CHOIX DU NOMBRE DE TOURS', couleur='white',ancrage='center', taille=27, tag='var')

    rectangle(0,100,599,200,couleur='black',remplissage='white',tag = 'var')
    texte(300,150, '5 TOURS', couleur='black',ancrage='center', taille=27, tag='var')

    rectangle(0,200,599,300,couleur='black',remplissage='white',tag = 'var')
    texte(300,250, '10 TOURS', couleur='black',ancrage='center', taille=27, tag='var')
    
    rectangle(0,300,599,400,couleur='black',remplissage='white',tag = 'var')
    texte(300,350, '15 TOURS', couleur='black',ancrage='center', taille=27, tag='var')

    rectangle(0,400,599,500,couleur='black',remplissage='white',tag = 'var')
    texte(300,450, '20 TOURS', couleur='black',ancrage='center', taille=27, tag='var')

    rectangle(0,500,599,600,couleur='black',remplissage='white',tag = 'var')
    texte(300,550, '25 TOURS', couleur='black',ancrage='center', taille=27, tag='var')

    boo = True
    while boo == True :
        x,y,z = attente_clic()
        if 100<=y<=200 :
            efface_tout()
            return 5
        if 200<=y<=300 : 
            efface_tout()
            return 10
        if 300<=y<=400 : 
            efface_tout()
            return 15
        if 400<=y<=500 : 
            efface_tout()
            return 20
        if 500<=y<=600 : 
            efface_tout()
            return 25

def pause(): 
    """
    Affiche un menu pause et renvoie la décision du joueur suite à son clic, soit reprendre la partie, soit sauvegarder et quitter la partie 
    ou alors quitter sans sauvegarder la partie. 
    """
    rectangle(100,100,500,500,remplissage='white',tag='pause')
    rectangle(200,0,400,100, remplissage="white", tag='pause')
    texte(300, 50, "PAUSE", ancrage="center", taille=20, tag='pause')
    rectangle(100, 150, 500, 250, remplissage='red',epaisseur=4, tag='pause')
    texte(300,200, "REPRENDRE", taille=25, ancrage='center', tag='pause')
    rectangle(100,300,500,400, remplissage="purple",epaisseur=4, tag='pause')
    texte(300,350, 'SAUVER ET QUITTER', taille=23, ancrage='center', tag='pause')
    rectangle(100,450,500,550, remplissage="blue",epaisseur=4, tag='pause')
    texte(300,500, 'QUITTER SANS SAUVER', taille=23, ancrage='center', tag='pause')
    x,y,z = attente_clic()
    if 150<=y<=250 and 100<=x<=500 : 
        efface('pause')
        return 'continuer'
    if 300 <= y <= 400 and 100<=x<=500 :
        efface('pause')
        return 'sauver'
    if 450 <= y <= 550 and 100<=x<=500 :
        efface('pause')       
        return 'quitter'
    

def sauvegarder_partie(lst1, lst2, lst3,nombre_tours,j1,j2, fichier_sauvegarde):
    """
    Met les données à sauvegarder dans un dictionnaire et l'inscrit dans le fichier de sauvegarde en l'encodant en JSON.
    """
    dico_data = {'lst1': lst1,'lst2': lst2,'lst3': lst3,'nombre_tours' : nombre_tours,'j1': j1,'j2': j2}
    with open(fichier_sauvegarde, 'w') as f:
        json.dump(dico_data, f)

def recup_data(fichier_sauvegarde):
    """
    Décode le dictionnaire, inscrit en JSON dans le fichier, et renvoie un tuple contenant toutes les données de ce dictionnaire
    """
    with open(fichier_sauvegarde, 'r') as f:
        dico_data = json.load(f)
    return dico_data['lst1'], dico_data['lst2'], dico_data['lst3'], dico_data['nombre_tours'],dico_data['j1'],dico_data['j2']

def classement(fichier_sc, fichierj, scj1, scj2, nomj1, nomj2):
    """
    Ajoute le score et le nom des deux joueurs dans des fichiés séparés, un pour le joueur un pour le score. 
    Comme cela pour chaque ligne dans chaque texte correspond au score et nom du joueur.
    """
    with open(fichier_sc, 'a') as f1 ,open(fichierj, 'a') as f2:
        f1.write(str(scj1)+'\n')
        f1.write(str(scj2)+'\n')
        f2.write(nomj1+'\n')
        f2.write(nomj2+'\n')

def affiche_classement(fichier_sc, fichierj):
    """
    Permet d'afficher le classement quand on choisit l'option.
    """
    with open(fichier_sc, 'r') as f1 ,open(fichierj, 'r') as f2:
        l_s = [line.strip() for line in f1]
        l_j = [line.strip() for line in f2]
    dico = dict()
    for i in range(len(l_s)):
        if l_s[i] in dico :
            dico[l_s[i]].add(l_j[i])
        else:
            dico[l_s[i]] = {l_j[i]}
    list.sort(l_s)
    list.reverse(l_s)
    if len(l_s) < 5 :
        n = len(l_s)
    else :
        n = 5
    m_s = []
    i = 0
    for i in range(n):
        if l_s[i] not in m_s :
            m_s.append(l_s[i])
        else :
            m_s.append(l_s[i+1])
        
            
    rectangle(0,0,599,100,couleur='black',remplissage='black',tag = 'cl')
    texte(300,50, 'CLASSEMENT DES MEILLEURS SCORE', couleur='white',ancrage='center', taille=22, tag='cl')

    rectangle(0,100,599,200,couleur='black',remplissage='white',tag = 'cl')
    texte(300,150, (str(m_s[0]) + ' : '+ "/".join(map(str, dico[m_s[0]]))), couleur='black',ancrage='center', taille=27, tag='cl')
    texte(50, 150, '1',couleur='black',ancrage='center', taille=27, tag='cl')

    rectangle(0,200,599,300,couleur='black',remplissage='white',tag = 'cl')
    texte(300,250, str(m_s[1]) +' : '+  "/".join(map(str, dico[m_s[1]])), couleur='black',ancrage='center', taille=27, tag='cl')
    texte(50, 250, '2',couleur='black',ancrage='center', taille=27, tag='cl')

    rectangle(0,300,599,400,couleur='black',remplissage='white',tag = 'cl')
    texte(300,350, str(m_s[2]) +' : '+  "/".join(map(str, dico[m_s[2]])), couleur='black',ancrage='center', taille=27, tag='cl')
    texte(50, 350, '3',couleur='black',ancrage='center', taille=27, tag='cl')

    rectangle(0,400,599,500,couleur='black',remplissage='white',tag = 'cl')
    texte(300,450, str(m_s[3]) + ' : '+ "/".join(map(str, dico[m_s[3]])), couleur='black',ancrage='center', taille=27, tag='cl')
    texte(50, 450, '4',couleur='black',ancrage='center', taille=27, tag='cl')


    rectangle(0,500,599,600,couleur='black',remplissage='white',tag = 'cl')
    texte(300,550, str(m_s[4]) + ' : '+ "/".join(map(str, dico[m_s[4]])), couleur='black',ancrage='center', taille=27, tag='cl')  
    texte(50, 550, '5',couleur='black',ancrage='center', taille=27, tag='cl')
################# FONCTIONS #################



################# VALEURS #################
rayon = 30                  # rayon de base
hauteur_fenetre = 600
longueur_fenetre = 600      # taille de la fenetre
booleen = True              # Pour changer de tour
color_joueur1 = 'red'        
color_joueur2 = 'blue'      # couleurs des joueurs
liste_j1 = []               
liste_j2 = []               # listes qui vont comporter les coordonnées des centres, les tags et rayons de chaque rond
tagj1 = 'a'
tagj2 = 'b'                 # lettre correspondant au tag du premier cercle de chaque joueur
reserve_j1 = 300
reserve_j2 = 300            # Reservoir des joueurs (rayons)
liste_obs = []              # Liste des obstacles
sab, sco, tdb, vdy, ter, obs = False,False,False,False,False,False          # Aucune variante à l'initialisation
nombre_tours = 0
bool_pause = False                  # Booléen permettant de savoir si un joueur a cliqué sur pause
################# VALEURS #################


################# EXECUTION #################
if __name__ == '__main__':
    
    cree_fenetre(longueur_fenetre,hauteur_fenetre)
    ecran_lancement()
    attente_clic()

    choix_menu = menu() 
        
    if choix_menu == 're': 
        variante('re')                                                                  # Affichage des règles
        choixj = choix_jeu()

    if choix_menu =='class':
        affiche_classement('fichier_sc.txt','fichierj.txt')
        attente_clic()
        choixj = choix_jeu()
        
    
    if choix_menu == 'choixjeu': 
        choixj = choix_jeu()                                # choix entre reprendre une partie ou en commencer une nouvelle
        if choixj == 'jeunv':
            
            sab, sco, tdb, vdy, ter, obs = variante('jeunv')                                          
            nombre_tours = choix_nombre_manches()
            rectangle(100,225,500,375,remplissage='white',couleur='black', tag='para')
            texte(300, 300, "CHOISISSEZ VOS PARAMETRES\n         DANS LE TERMINAL",ancrage='center', couleur="black", taille=16, police='Helvetica', tag='para')
            joueur1 = input('Entrez le nom du joueur 1 : ')
            while True :                                                                                                    # Choix noms des joueurs, saisies contrôlées
                if len(joueur1) >= 10 : 
                    print('Le nom que vous tentez đ\'entrer est trop long (plus de 10 caractères), soyez plus simple...')
                    joueur1 = input('Entrez le nom du joueur 1 : ')
                else : 
                    break
            joueur2 = input('Entrez le nom du joueur 2 : ')
            while True : 
                if len(joueur2) >= 10 : 
                    print('Le nom que vous tentez đ\'entrer est trop long (plus de 10 caractères), soyez plus simple...')
                    joueur2 = input('Entrez le nom du joueur 2 : ')
                else : 
                    break
            efface('para')
    
        else:                                                                                     # Chargement de la partie sauvegarder
            try:
                with open('sauvegarde.txt', 'r') as f:                  # On est essaie d'ouvrir le fichier
                    if f.read().strip() == '':                          # Si le fichier est vide, on ferme le jeu
                        efface_tout()                               
                        texte(300,300,"Il n'existe aucune sauvegarde, réessayez",taille=20,ancrage='center')
                        attente_clic()
                        ferme_fenetre()
                    else:
                        liste_j1,liste_j2,liste_obs,nombre_tours,joueur1,joueur2 = recup_data('sauvegarde.txt')           # Récupération des données      
                    for i in range(len(liste_j1)):                                                                    # Pose des cercles
                        cercle(liste_j1[i][0],liste_j1[i][1],liste_j1[i][3],remplissage=color_joueur1,couleur=color_joueur1, tag=liste_j1[i][2])
                    for i in range(len(liste_j2)): 
                        cercle(liste_j2[i][0],liste_j2[i][1],liste_j2[i][3],remplissage=color_joueur2,couleur=color_joueur2, tag=liste_j2[i][2])
                    for i in range(len(liste_obs)): 
                        cercle(liste_obs[i][0],liste_obs[i][1],liste_obs[i][3],remplissage='orange', tag=liste_obs[i][2])
                    if len(liste_j1) < len(liste_j2) :                                          # Attribution du Tour
                        booleen = False
            except:                                         # Si le fichier n'existe pas ou n'est pas ouvrable on ferme le jeu
                efface_tout()
                attente_clic()
                texte(300,300,"Le fichier n'est pas ouvrable",taille=20,ancrage='center')
                ferme_fenetre()
            
            
            
            




    if sab == True :
        saisie2 = 0
        while saisie2 !=1 :
            try :
                seconde = int(input("entrez le nombre de secondes pour un tour : ")) # Variante sablier
                saisie2 += 1
            except :
                print("Erreur de saisie, Veuiller entrez un nombre entier")
        
        duree = seconde * 1000 # Car on utilise des ms dans la fonction attente_click_jusqua
################# EXECUTION #################


        #### JEU ####
        

    #On crée les obstacles avant de commencer la partie si la variante est activé.
    if obs == True:
        tagobs = 'o'
        x = randint(3,6)
        for i in range(x):
            x,y,r = obstacle()
            cercle(x,y,r, remplissage='orange', tag = tagobs)
            liste_obs.append([x,y,tagobs,r])
            texte(x,y, 'Obstacle', taille = int(r/2), ancrage= 'center')
            tagobs = tagobs + 'o'

    while nombre_tours != 0 :
        affichage_constant()

        #### TOUR DU JOUEUR 1 ####
        
        if booleen:
            texte(longueur_fenetre//2,15,'Tour '+joueur1,ancrage='center', tag='txtj1', taille=20)
                        


            if sco == True:                                         # Variante score 
                var_score()
            if sab == True :
                x1, y1, w = attente_click_jusqua(duree) 
                if x1 == None and y1 == None and w == None :        # Si on n'a pas cliqué dans le temps imparti
                    perte_tour('Temps écoulé !')                    # On perd son tour et c'est à l'adversaire
                    booleen = False   
            
            else : 
                pause_jeu = "continuer"                     #On initialise une variablepause_jeu à 'continuer'
                x1, y1, w = attente_clic()

                if 180<= x1 <=420 and 60<=y1<=80 :          # Si le joueur décide d'accéder au menu pause
                    pause_jeu = pause()                     # La variable pause_jeu prend la valeur selon le choix du joueur ...
                    bool_pause = True
                    if pause_jeu == "quitter" :     
                        nombre_tours = 0                    # ... et quitte si il décide quitter sans sauvegarder...
                    if pause_jeu == "sauver":
                        sauvegarder_partie(liste_j1, liste_j2, liste_obs,nombre_tours,joueur1,joueur2, 'sauvegarde.txt')        #... ou sauvegarde si il décide de le faire
                        ferme_fenetre()
                if pause_jeu == "continuer":                # Si le joueur clic sur REPRENDRE ou qu'il navait pas cliqué sur pause ...
                    if bool_pause == True :                 # Soit on récupère son nouveau clic (si pause), détécté grace au changement de valeur de bool_pause
                        x1,y1,w = attente_clic()
                        bool_pause = False                  #Soit on récupère son clic de base
                    if clic_interieur_ou_non(liste_j2, x1, y1) != None:             # verification sur la position du cercle posé : interieur ou non à un autre

                        infos_listej2, xnv, ynv, r1, r2 = division_cercle(x1, y1, liste_j2)         # On récupère les informations necéssaires au dépot et à la suppression des cercles
                        
                        liste_j2.pop(infos_listej2)
                        
                        
                        cercle(x1,y1,r1, couleur=color_joueur2, remplissage=color_joueur2, tag=tagj2)
                        tagj2 = tagj2
                        liste_j2.append([x1, y1, tagj2, r1])

                        
                        cercle(xnv,ynv,r2,couleur=color_joueur2, remplissage=color_joueur2, tag=tagj2)
                        tagj2 = tagj2 + 'b'
                        liste_j2.append([xnv, ynv, tagj2, r2])
                        
                
                    elif touche_ou_non(liste_j2, x1, y1, 30) == True :      # vérifications sur la position du cercle posé par rapport aux autres boules qui sont dans la liste du joueur 2 et à la fenetre
                        if tdb == True :                                        # Variante taille des boules
                            rayon = int(input('Entrez la taille du rayon de la boule, votre budget est de ' +str(reserve_j1)+ ' : '))    # On choisit la taille de la boule
                            while True :                                                         
                                if rayon > reserve_j1 :
                                    print('Ah, vous voyez la vie en grand... Votre budget n\'est que de '+str(reserve_j1) + '.')        # Saisie contrôlée (Budget trop faible)
                                    rayon = int(input('Entrez une valeur inférieur à votre budget : '))
                                elif rayon < 1 : 
                                    rayon = int(input('Valeur non valide, réessayez ! : '))                  # Saisie contrôlée (Valeur entrée bien positive)
                                else :
                                    break
                        if dans_aire_de_jeu(x1, y1, rayon) == True and touche_ou_non(liste_j2, x1, y1, rayon) and touche_ou_non(liste_obs, x1, y1, rayon) and not (180<= x1 <=420 and 60<=y1<=80):                  # Vérification que le cercle est bien dans l'aire de jeu et qu'il ne touche pas de cercle ennemi
                            reserve_j1 = reserve_j1 - rayon                                                                     # On baisse le budget
                            cercle(x1 , y1 , rayon, couleur=color_joueur1, remplissage=color_joueur1, tag=tagj1)         # cercle posé 
                            liste_j1.append([x1,y1,tagj1,rayon])            # ajout des coordonnées, du tag et du rayon du cercle dans la liste du joueur 1
                            tagj1 = tagj1 + 'a'
                        else : 
                            perte_tour('Le cercle ne peut pas être posé !')
                    
                    else:
                        perte_tour('Le cercle ne peut pas être posé !')
                    if ter == True and nombre_tours > 5:                                                                # Variante terminaison, on propose au joueur de finir la partie dans 5 manches a chaque tour
                        rectangle(100,225,500,375,remplissage='white',couleur='black', tag='ter')
                        texte(300, 280, "Activer la variante terminaison ?",ancrage='center', couleur="black", taille=20, police='Helvetica', tag='ter')
                        texte(300, 320, "O pour oui",ancrage='center', couleur="black", taille=15, police='Helvetica', tag='ter')
                        texte(300, 340, "N pour non",ancrage='center', couleur="black", taille=15, police='Helvetica', tag='ter')
                        term = attente_touche() 
                        if term == 'o':
                            nombre_tours = 6
                            ter = False
                            efface('ter')
                        if term =='n' :
                            efface('ter')
                            pass
                        
                    booleen = False        # Passage au tour suivant 
                    efface('txtj1')   
                
                if vdy == True :                                    # Variante version dynamique
                    touche_ou_non_aggrandissement(liste_j1, liste_j2)           
                    touche_ou_non_aggrandissement(liste_j2, liste_j1)               # On verifie si des cercles se touchent
                    if obs == True : 
                        touche_ou_non_aggrandissement(liste_j1, liste_obs)
                        touche_ou_non_aggrandissement(liste_j2, liste_obs)
                    agrandissement_cercles(liste_j1, 'red')
                    agrandissement_cercles(liste_j2, 'blue')                        # On aggrandit les cercles concerné                               

        
        #### TOUR DU JOUEUR 2 ####    
        if booleen == False:  
            texte(longueur_fenetre//2,15,'Tour '+joueur2,ancrage='center', tag='txtj2', taille=20)                                                   # On refait la même chose pour le joueur 2 
            

            if sco == True:
                var_score()
            if sab == True :
                x1, y1, w = attente_click_jusqua(duree) 
                if x1 == None and y1 == None and w == None :        # Si on n'a pas cliqué dans le temps imparti
                    perte_tour('Temps écoulé !')                    # On perd son tour et c'est à l'adversaire
                    booleen = False   
            

            else :
                pause_jeu = "continuer"
                x2, y2, w = attente_clic()

                if 180<= x2 <=420 and 60<=y2<=80 :
                    bool_pause = True
                    pause_jeu = pause()
                    if pause_jeu == "quitter" : 
                        ferme_fenetre()
                    if pause_jeu == "sauver":
                        sauvegarder_partie(liste_j1, liste_j2, liste_obs,nombre_tours,joueur1,joueur2, 'sauvegarde.txt')
                        ferme_fenetre()
                if pause_jeu == "continuer":
                    if bool_pause == True : 
                        x2,y2,w = attente_clic()
                        bool_pause = False
                    if clic_interieur_ou_non(liste_j1, x2, y2) != None:
                        
                        
                        infos_listej1, xv, yv, r1, r2 = division_cercle(x2, y2, liste_j1) 
                        
                        liste_j1.pop(infos_listej1)

                        cercle(x2,y2,r1, couleur=color_joueur1, remplissage=color_joueur1, tag=tagj1)
                        tagj1 = tagj1  
                        liste_j1.append([x2, y2, tagj1, r1])

                        cercle(xv,yv,r2,couleur=color_joueur1, remplissage=color_joueur1, tag=tagj1)
                        tagj1 = tagj1 + 'a'
                        liste_j1.append([xv, yv, tagj1, r2])
                        
                
                    elif touche_ou_non(liste_j1, x2, y2, 30) == True :  
                        if tdb == True :
                            rayon = int(input('Entrez la taille du rayon de la boule, votre budget est de  ' +str(reserve_j2)+ ' : '))
                            while True : 
                                if rayon > reserve_j2 :
                                    print('Ah, vous voyez la vie en grand... Votre budget n\'est que de '+str(reserve_j2) + '.')
                                    rayon = int(input('Entrez une valeur inférieur à votre budget : '))
                                elif rayon < 1 : 
                                    rayon = int(input('Allez... Voyez un peu plus grand, ce rayon est trop petit : '))
                                else :
                                    break
                        if dans_aire_de_jeu(x2, y2, rayon) == True and touche_ou_non(liste_j1, x2, y2, rayon) and touche_ou_non(liste_obs, x2, y2, rayon) and not (180<= x2 <=420 and 60<=y2<=80):
                            reserve_j2 = reserve_j2 - rayon    
                            cercle(x2 , y2 , rayon, couleur=color_joueur2, remplissage=color_joueur2, tag=tagj2)
                            liste_j2.append([x2,y2,tagj2,rayon])
                            tagj2 = tagj2 + 'b' 
                            booleen = True
                        else: 
                            perte_tour('Le cercle ne peut pas être posé !')
                            booleen = True
                
                    else:
                        perte_tour('Le cercle ne peut pas être posé !')
                    if ter == True and nombre_tours > 5:
                        rectangle(100,225,500,375,remplissage='white',couleur='black', tag='ter')
                        texte(300, 280, "Activer la variante terminaison ?",ancrage='center', couleur="black", taille=20, police='Helvetica', tag='ter')
                        texte(300, 320, "O pour oui",ancrage='center', couleur="black", taille=15, police='Helvetica', tag='ter')
                        texte(300, 340, "N pour non",ancrage='center', couleur="black", taille=15, police='Helvetica', tag='ter')
                        term = attente_touche() 
                        if term == 'o':
                            nombre_tours = 6
                            ter = False
                            efface('ter')
                        if term =='n' :
                            efface('ter')
                            pass
                    booleen = True
                    efface('txtj2')
                    if vdy == True : 
                        touche_ou_non_aggrandissement(liste_j1, liste_j2)
                        touche_ou_non_aggrandissement(liste_j2, liste_j1)
                        if obs == True : 
                            touche_ou_non_aggrandissement(liste_j1, liste_obs)
                            touche_ou_non_aggrandissement(liste_j2, liste_obs)
                        agrandissement_cercles(liste_j1, 'red')
                        agrandissement_cercles(liste_j2, 'blue')   
        
        nombre_tours -= 1                           # On décrémente la valeur du nombre de tour (jusqu'à nombre_tours == 0, quand la boucle while s'arrête).
            #### JEU ####
    

    

    #### Fin de la partie ####
    with open('sauvegarde.txt','w') as f:
        pass
    ecran_de_fin(score(liste_j1),score(liste_j2))
    classement('fichier_sc.txt', 'fichierj.txt', score(liste_j1), score(liste_j2), joueur1, joueur2) #On ajoute le nom et score de chaque joueur dans chaque fichier texte.
    attente_clic()
    ferme_fenetre()
    #### Fin de la partie ####











