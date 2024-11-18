#!/usr/bin/env python
# coding: utf-8

# Lights Out

import numpy as np
import sympy as sp

import pygame
import sys


# V est une matrice de dimension (k, 1) avec $k = i*j$ (on a k lignes/éléments dans le vecteur colonne)

def Vecteur_Colonne(A):
    # Prend en entrée une matrice et retourne son vecteur colonne associé
    V = []
    
    i = len(A)
    j = 0
    if i != 0:
        j = len(A[0])
        
    for n in range(j):    
        for line in A:
            V.append([line[n]])
        
    return np.array(V)


def Matrice(V):
    # Prend en entrée un vecteur colonne de taille n² 
    # Retourne la matrice carrée n*n associée
    A = []
    
    k = len(V)
    n = int(np.sqrt(k))
    for i in range(n):
        curr_line = []
        for j in range(n):
            curr_line.append(V[i + j*n][0])
        A.append(curr_line)
    
    return np.array(A)


def Croix(i, j, n):
    # Crée la matrice croix de taille (n, n)
    # Remplie de 1 seulement en (i, j) et dans les voisins verticaux et horizontaux
    # Toutes les autres positions sont remplies de 0
    A = np.zeros((n, n), dtype=np.int64)
    
    i1 = i-1
    while i1 <= i+1:
        if i1 >= 0 and i1 < n:
            A[i1][j] = 1
        i1 += 1
    
    j1 = j-1
    while j1 <= j+1:
        if j1 >= 0 and j1 < n:
            A[i][j1] = 1
        j1 += 1
       
    return np.array(A)


def Jeu_Fini(A):
    # Retourne vrai si la matrice n'est remplie que de 0
    # Faux s'il reste des 1 (lumières allumées)
    rows = len(A)
    if rows > 0:
        cols = len(A[0])
    for i in range(rows):
        for j in range(cols):
            if A[i][j] == 1:
                return False
    return True


# Version en ligne de commande de Lights Out ci-dessous.
# A noter qu'on utilise en jeu la notation mathématique avec les lignes et les colonnes numérotées à partir de 1 (là où dans le code Python, notre numérotation commence à 0).

def Lights_Out():
    # Accueil du joueur
    print("----- LIGHTS OUT -----")
    print("Bienvenue dans Lights Out !")
    print("Vous devez transformer tous les 1 en 0 pour éteindre toutes les cases de la matrice.\n")
    print("(Note: on utilise la notation mathématique et commence à numéroter les lignes et colonnes à partir de 1)\n")
    
    # Tirage de la configuration initiale et affichage
    A = np.random.randint(low=0, high=2, size=(3, 3))
    print(A)
    
    # Boucle de jeu
    while not Jeu_Fini(A):
        print("\nSur quelle case voulez-vous appuyer ?")
        i = int(input("Ligne ? : ")) - 1
        j = int(input("Colonne ? : ")) - 1
        
        A = (A + Croix(i, j, 3)) % 2
        print()
        print(A)

    # Fin du jeu
    print("\nBravo ! Vous avez réussi à éteindre toutes les lumières.")


#Lights_Out()



def Matrice_Passage(n):
    # Prend en entrée la dimension n
    # Retourne la matrice dont les vecteurs sont les C(i,j) exprimés dans la base canonique de Mn(F2)
    # On prend les C(i,j) dans le même ordre que les vecteurs E(i,j) de la base canonique
    P = np.zeros((n*n, n*n), dtype=np.int64)

    # On parcourt chaque vecteur colonne de la matrice de passage P
    for j in range(n):
        # Quand i atteint n, on incrémente j et réinitialise i
        for i in range(n):
            C = Croix(i, j, n)
            V = C.flatten('F')    # Fonction numpy pour 'aplatir' notre matrice selon ses colonnes
            P[:, i + j * n] = V   # Notation numpy pour modifier une colonne complète
    
    return P


# Le jeu a une unique solution quelle que soit sa configuration initiale pour les dimensions suivantes (< 11) :
# - dimensions 2 ; 3 ; 6 ; 7 ; 8 ; 10






def Inverse(A):
    # Renvoie l'inverse de la matrice A dans M(F2) grâce à Sympy
    M = sp.Matrix(A)
    inverse_M = M.inv_mod(2)
    return np.array(inverse_M).astype(np.int64)



def Solution(A):
    # Solutionneur en dimension 3
    # Prend une matrice A en 3x3
    # Renvoie la matrice solution S (avec des 1 sur les cases à appuyer, 0 sinon)
    P = Matrice_Passage(3)
    inverse_P = Inverse(P)
    A_column = Vecteur_Colonne(A)
    S_column = np.dot(inverse_P, A_column) % 2
    S = Matrice(S_column)
    return S





def Solution_vers_Config_Init(S, n):
    # Renvoie la configuration initiale associée à une matrice solution de dimension n
    # Produit de la matrice de transition par le vecteur colonne de la solution
    P = Matrice_Passage(n)
    S_column = Vecteur_Colonne(S)
    M_column = np.dot(P, S_column)
    M = Matrice(M_column) % 2
    return M

def Lights_Out_Pygame():

    # Initialisation de pygame
    pygame.init()

    # Taille de la grille modifiable
    n = 3

    # Paramètres de l'interface
    CELL_SIZE = 100
    MARGIN = 5
    BUTTON_HEIGHT = 50
    
    # Paramétrage de la fenêtre
    screen_width = n * (CELL_SIZE + MARGIN) + MARGIN
    screen_height = screen_width + BUTTON_HEIGHT * 2
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Lights Out")

    # Définition des couleurs utilisées
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_ON = (255, 255, 100)
    LIGHT_OFF = (50, 50, 50)
    BUTTON_COLOR = (100, 200, 100)
    RED = (255, 0, 0)

    # Génère une matrice solution et la configuration initiale associée
    S = np.random.randint(low=0, high=2, size=(n, n))
    A = Solution_vers_Config_Init(S, n)
    
    # Fonction pour dessiner la grille de la matrice A
    def dessiner_grille(A):
        for i in range(n):
            for j in range(n):
                if A[i][j] == 1:
                    color = LIGHT_ON  
                else :
                    color = LIGHT_OFF
                pygame.draw.rect(screen, color,
                                 [(MARGIN + CELL_SIZE) * j + MARGIN,
                                  (MARGIN + CELL_SIZE) * i + MARGIN,
                                  CELL_SIZE, CELL_SIZE])
    
    # Fonction pour dessiner le bouton de solution
    def dessiner_bouton():
        bouton_rect = pygame.Rect(MARGIN, n * (CELL_SIZE + MARGIN) + MARGIN, screen_width - 2 * MARGIN, BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, bouton_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Solution", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, bouton_rect.y + 10))
        return bouton_rect

    # Fonction pour dessiner les boutons de sélection de taille
    def dessiner_boutons_taille():
        boutons = []
        tailles = [3, 4, 5]
        for idx, taille in enumerate(tailles):
            bouton_rect = pygame.Rect(MARGIN + idx * (screen_width // 3), 
                                      n * (CELL_SIZE + MARGIN) + MARGIN + BUTTON_HEIGHT + 10, 
                                      screen_width // 3 - MARGIN, 
                                      BUTTON_HEIGHT)
            pygame.draw.rect(screen, BUTTON_COLOR, bouton_rect)
            font = pygame.font.Font(None, 30)
            text = font.render(f"{taille}x{taille}", True, BLACK)
            screen.blit(text, (bouton_rect.x + bouton_rect.width // 2 - text.get_width() // 2, 
                               bouton_rect.y + 10))
            boutons.append((bouton_rect, taille))
        return boutons

    # Fonction pour dessiner les marqueurs rouges dans les cases de la solution
    def dessiner_points_solution(S):
        for i in range(n):
            for j in range(n):
                if S[i][j] == 1:  # Marqueur rouge s'il faut cliquer
                    center_x = (MARGIN + CELL_SIZE) * j + MARGIN + CELL_SIZE // 2
                    center_y = (MARGIN + CELL_SIZE) * i + MARGIN + CELL_SIZE // 2
                    pygame.draw.circle(screen, RED, (center_x, center_y), CELL_SIZE // 6)

    # On dessine la grille de départ
    screen.fill(WHITE)
    dessiner_grille(A)
    bouton_solution = dessiner_bouton()
    boutons_taille = dessiner_boutons_taille()
    show_solution = False

    # Mettre l'affichage à jour
    pygame.display.flip()

    # Boucle de jeu
    while True:
        
        # Récupération des évènements Pygame 
        for event in pygame.event.get():
            
            # Si la croix est cliquée, on quitte le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Si le joueur clique sur une partie de la fenêtre
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
    
                # Vérifie si un carré est cliqué
                i = pos[1] // (CELL_SIZE + MARGIN)
                j = pos[0] // (CELL_SIZE + MARGIN)

                # On ajoute la matrice Croix de la case cliquée à la matrice de jeu
                # On inverse l'indice de cette case dans la matrice solution S
                if i < n and j < n:
                    A = (A + Croix(i, j, n)) % 2
                    S[i][j] = (S[i][j] + 1) % 2

                # Vérifie si le bouton de solution est cliqué
                elif bouton_solution.collidepoint(pos):
                    show_solution = not show_solution
                        
                # Vérifie si un bouton de taille est cliqué
                for bouton, taille in boutons_taille:
                    if bouton.collidepoint(pos):

                        # On réinitialise la fenêtre de jeu si changement de matrice
                        n = taille  
                        screen_width = n * (CELL_SIZE + MARGIN) + MARGIN
                        screen_height = screen_width + BUTTON_HEIGHT * 2
                        screen = pygame.display.set_mode((screen_width, screen_height))

                        # Génère une matrice solution et la configuration initiale associée
                        S = np.random.randint(low=0, high=2, size=(n, n))
                        A = Solution_vers_Config_Init(S, n)

                        show_solution = False
                        break
        
        # On redessine la grille après les changements
        screen.fill(WHITE)
        dessiner_grille(A)
        bouton_solution = dessiner_bouton()
        boutons_taille = dessiner_boutons_taille()

        # Dessine les points rouges si show_solution est activé
        if show_solution:
            dessiner_points_solution(S)

        # Mettre l'affichage à jour
        pygame.display.flip()


# Lancement de la version graphique Pygame de Lights Out ci-dessous : 
# - on affiche une matrice aléatoire 3x3 au lancement
# - le joueur peut à tout moment afficher/cacher la solution qui évolue avec ses actions
# - une fois la grille éteinte ou même avant, le joueur peut relancer une partie dans la dimension de son choix entre 3x3, 4x4 et 5x5

Lights_Out_Pygame()

