from random import random
from time import sleep
import tkinter as tk

def new_grille(largeur,hauteur):
    """permet de créer une grille ville vide
    :param:(int) dimensions de la grille, largeur et hauteur
    :return:(list)
    >>> new_grille(3,2)
    [[0, 0, 0], [0, 0, 0]]
    """
    return [[0]*largeur for i in range(hauteur)]
    

def hauteur(grille):
    """donne la hauteur d'une grille
    :param:(list) une matrice sous forme de liste de listes
    :return:(int)
    >>> hauteur([[0,0,0],[0,0,0]])
    2
    """
    return len(grille)
    

def largeur(grille):
    """donne la largeur d'une grille
    :param:(list) une matrice sous forme de liste de listes
    :return:(int)
    >>> largeur([[0,0,0],[0,0,0]])
    3
    """
    return len(grille[0])
    

def grille_initiale(largeur,hauteur,proba=0.5):
    """crée une grille avec des cellules vivantes
    :param largeur:(int) largeur de la grille
    :param hauteur:(int) hauteur de la grille
    :param proba:(float) probabilité qu'une case contienne une cellule, vaut 0.5 par défaut
    :CU: proba est compris entre 0 et 1
    >>> grille_initiale(3,2,1)
    [[1, 1, 1], [1, 1, 1]]
    >>> grille_initiale(2,3,0)
    [[0, 0], [0, 0], [0, 0]]
    """
    grille = new_grille(largeur, hauteur)
    for y in range(hauteur):
        for x in range(largeur):
            if random() < proba:
                grille[y][x] = 1
    return grille
    

def afficheur(grille):
    """
    Affichage très rapide de la grille Game of Life.
    La grille est centrée et adaptée automatiquement à l'écran.
    """
    haut = hauteur(grille)
    large = largeur(grille)

    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()
    
    zoom = min(largeur_ecran // large, hauteur_ecran // haut)
    if zoom < 1: zoom = 1

    largeur_aff = large * zoom
    hauteur_aff = haut * zoom

    # création image si premiere fois
    if not hasattr(afficheur, "img"):
        afficheur.img = tk.PhotoImage(width=large, height=haut)
        x0 = (largeur_ecran - largeur_aff) // 2
        y0 = (hauteur_ecran - hauteur_aff) // 2
        afficheur.img_id = canvas.create_image(x0, y0, anchor="nw")

    couleurs = {0: "#000", 1: "#fff"}
    lignes = ["{" + " ".join(couleurs[v] for v in row) + "}" for row in grille]
    afficheur.img.put(" ".join(lignes))

    if zoom > 1:
        img_zoom = afficheur.img.zoom(zoom)
        canvas.itemconfig(afficheur.img_id, image=img_zoom)
        afficheur.img_zoom = img_zoom
    else:
        canvas.itemconfig(afficheur.img_id, image=afficheur.img)

def voisins(grille,x,y):
    """donne le contenu des cases voisines
    :param grille:(list) liste de listes du jeu de la vie
    :param x:(int) abscisse d'une case de la grille
    :param y:(int) ordonnée d'une case de la grille
    >>> grille=[[0,1,0], [1,0,0], [1,1,1]]
    >>> voisins(grille, 1, 1)
    [0, 1, 0, 1, 0, 1, 1, 1]
    >>> voisins(grille, 2, 2)
    [0, 0, 1]
    >>> voisins(grille, 0, 2)
    [1, 0, 1]
    """
    M=[]
    haut = hauteur(grille)
    large = largeur(grille)
    for h in range(y-1, y+2):
        for l in range(x-1, x+2):
            if((h != y or l != x) and h >= 0 and h < haut and l >= 0 and l < large):
                M.append(grille[h][l])
    return M

def nb_cellules_voisines(grille,x,y):
    """donne les nombre de cellules à proximité
    :param grille:(list) liste de listes du jeu de la vie
    :param x:(int) abscisse d'une case de la grille
    :param y:(int) ordonnée d'une case de la grille
    >>> grille=[[0,1,0], [1,0,0], [1,1,1]]
    >>> nb_cellules_voisines(grille, 1, 1)
    5
    >>> nb_cellules_voisines(grille, 2, 2)
    1
    """
    return sum(voisins(grille, x, y))

def generation_suivante(grille):
    """génère la grille du jeu de la vie suivante
    :param:(list)liste de listes du jeu de la vie
    :param:(list)liste d elistes du jeu de la vie
    >>> grille=[[0,1,0], [1,0,0], [1,1,1]]
    >>> generation_suivante(grille)
    [[0, 0, 0], [1, 0, 1], [1, 1, 0]]
    >>> generation_suivante([[0, 0, 0], [1, 0, 1], [1, 1, 0]])
    [[0, 0, 0], [1, 0, 0], [1, 1, 0]]
    """
    haut=hauteur(grille)
    large=largeur(grille)
    grille_bis=new_grille(large, haut)
    for y in range(haut):
        for x in range(large):
            nb = nb_cellules_voisines(grille, x, y)
            if(nb == 3):
                grille_bis[y][x]=1
            elif(nb < 2 or nb > 3):
                grille_bis[y][x]=0
            else:
                grille_bis[y][x]=grille[y][x]
    return grille_bis

def lancer_jeu_de_la_vie(grille, n, delay = 50):
    """fait évoluer la grille sur n générations
    >>> #lancer_jeu_de_la_vie(grille_initiale(800, 500), 5)
    """
    generation = 0

    def boucle():
        nonlocal grille, generation
        if n is None or generation < n:
            afficheur(grille)
            grille = generation_suivante(grille)
            generation += 1
            fenetre.after(delay, boucle)  # prochaine génération
    boucle()

planeur = new_grille(25, 25)
planeur[2][0]=1
planeur[2][1]=1
planeur[2][2]=1
planeur[1][2]=1
planeur[0][1]=1

fenetre = tk.Tk()
fenetre.update()
fenetre.title("The Game of Life")
fenetre.attributes("-fullscreen", True)
canvas = tk.Canvas(fenetre, bg="black")
canvas.pack(fill="both", expand=True)
fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

grille = grille_initiale(244, 192)
lancer_jeu_de_la_vie(grille, None, delay = 10)
fenetre.mainloop()

import doctest
doctest.testmod(verbose=False)