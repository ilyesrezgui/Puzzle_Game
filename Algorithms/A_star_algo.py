from copy import deepcopy
import timeit

etat_final = [[1, 2, 3], [8, 0, 4], [7, 6, 5]] 
operateurs_de_transformations = {"U" : [-1, 0], "D" : [1, 0], "L" : [0, -1], "R" : [0, 1]}

class Taquin :
   
    def __init__(self, matrice_courante, matrice_precedente, g, h, operation) :
        self.matrice_courante = matrice_courante
        self.matrice_precedente = matrice_precedente
        self.g = g 
        self.h = h  
        self.operation = operation

    
    def f(self) :
        return self.g + self.h



def coordonnees(taquin, cellule) :
    for ligne in range(3) :
        if cellule in taquin[ligne] :
            return (ligne, taquin[ligne].index(cellule))


def cout_heuristique(etat_courant) :
    cout = 0
    for ligne in range(3) :
        for col in range(3) :
            if etat_courant[ligne][col] != 0: 
                (ligne_final, col_final) = coordonnees(etat_final, etat_courant[ligne][col]) 
                cout += abs(ligne - ligne_final) + abs(col - col_final) 
    return cout


def appliquer_operations(taquin,open,closed) :
    pos_vide = coordonnees(taquin.matrice_courante, 0)

    for operation in operateurs_de_transformations:
        new_pos = ( pos_vide[0] + operateurs_de_transformations[operation][0], pos_vide[1] + operateurs_de_transformations[operation][1] )
        if 0 <= new_pos[0] <3 and 0 <= new_pos[1] < 3 : 
            new_matrix = deepcopy(taquin.matrice_courante)
           
            new_matrix[pos_vide[0]][pos_vide[1]] = taquin.matrice_courante[new_pos[0]][new_pos[1]]
            new_matrix[new_pos[0]][new_pos[1]] = 0
            if not ( str(new_matrix) in closed.keys() or \
            str(new_matrix) in open.keys() and open[str(new_matrix)].f() < h+g ) :
                open[str(new_matrix)] = Taquin(new_matrix, taquin.matrice_courante,g,h, operation)



def meilleur_taquin(open_liste) :
    first_iter = True

    for taquin in open_liste.values() :
        if first_iter or taquin.f() < bestF :
            first_iter = False
            meilleur_taquin = taquin
            bestF = meilleur_taquin.f()
    return meilleur_taquin

def chemin_solution(closed_liste) :
    taquin = closed_liste[str(etat_final)]
    branche = list()

    while taquin.operation :
        branche.append({
            'operation' : taquin.operation,
            'taquin' : taquin.matrice_courante
        })
        taquin = closed_liste[str(taquin.matrice_precedente)]
    branche.append({
        'operation' : 'taquin initial sans opération de transformation',
        'taquin' : taquin.matrice_courante
    })
    branche.reverse()

    return branche


def main(puzzle_initial) : 

    start_algo=timeit.default_timer() 

    
    open_liste = {str(puzzle_initial) : Taquin(puzzle_initial, puzzle_initial, 0, cout_heuristique(puzzle_initial), "")}

    closed_liste = {}
    i=0
    while True :
        
        taquin_a_traiter = meilleur_taquin(open_liste) 
        closed_liste[str(taquin_a_traiter.matrice_courante)] = taquin_a_traiter 

        if taquin_a_traiter.matrice_courante == etat_final :
            stop_algo=timeit.default_timer()
            time=stop_algo-start_algo
         
            return chemin_solution(closed_liste), len(open_liste)-1+len(closed_liste), format(time, '.8f') 

        appliquer_operations(taquin_a_traiter,open_liste,closed_liste) 
        
    
        del open_liste[str(taquin_a_traiter.matrice_courante)]
        
