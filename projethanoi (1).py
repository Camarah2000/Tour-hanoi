import turtle
from copy import deepcopy
from time import localtime
from operator import itemgetter

# Partie A

def init(n):
    """ Initialisation du plateau """
    liste = [[],[],[]]
    for i in range(n,0,-1):
        liste[0].append(i)
    return liste

def nbDisques(plateau, numtour):
    """ Renvoie le nombre de disques sur une tour """
    return len(plateau[numtour])

def disqueSup(plateau, numtour):
    """ Renvoie le numéro du disque supérieur """
    if nbDisques(plateau,numtour) == 0:
        return -1
    else:
        return plateau[numtour][-1]

def posDisque(plateau, numdisque):
    """ Renvoie la tour sur laquelle est un disque """
    for i in plateau:
        if numdisque in i:
            return plateau.index(i)

def verifDepl(plateau, nt1, nt2):
    """ Vérifie si un déplacement de la tour nt1 vers la tour nt2 est autorisé """
    supnt2 = disqueSup(plateau, nt2)
    if len(plateau[nt1]) != 0:
        if supnt2 == -1 or plateau[nt1][-1] < supnt2:
            return True
    return False

def verifVictoire(plateau,n):
    """ Vérifie si c'est gagné """
    if len(plateau[-1]) == n:
        b = list(plateau[-1])
        b.sort(reverse = True)
        if b == plateau[-1]:
            return True
    return False
        
# Partie B

def rectangle(x,y,long,larg,colfill = False,color = "white"):
    turtle.teleport(x,y)
    if colfill == True:
        turtle.begin_fill()
        turtle.fillcolor(color)
        turtle.color(color)
    for i in range(2):
        turtle.forward(long)
        turtle.right(90)
        turtle.forward(larg)
        turtle.right(90)
    turtle.end_fill()

def dessinePlateau(n):
    turtle.setup(width=1200,height=600)
    turtle.color("black")
    turtle.speed(0)
    rectangle(-350,-200,700,50)
    rectangle(-70-30*(n-1),(n+1)*30-200,10,(n+1)*30)
    rectangle(-5,(n+1)*30-200,10,(n+1)*30)
    rectangle(60+30*(n-1),(n+1)*30-200,10,(n+1)*30)

def dessineDisque(nd,plateau,n,delete = False,colfill = True):
    dicolor = {0:"yellow",1:"orange",2:"blue",3:"green",4:"purple",5:"red",6:"pink",7:"white"}
    posx = posDisque(plateau,nd)
    posy = plateau[posx].index(nd)
    xnd = (65+30*(n-1))*(posx-1)-(30+15*(nd-1))
    ynd = -200+30*(posy+1)
    if delete == True:
        rectangle(xnd,ynd,60+30*(nd-1),29,True)
        turtle.color("black")
        turtle.teleport(-5+(65+30*(n-1))*(posx-1),ynd)
        turtle.right(90)
        turtle.forward(30)
        turtle.teleport(5+(65+30*(n-1))*(posx-1),ynd)
        turtle.forward(30)
        turtle.left(90)
    else:
        rectangle(xnd,ynd,60+30*(nd-1),29,colfill,dicolor[nd%(len(dicolor))])
    
def effaceDisque(nd,plateau,n):
    dessineDisque(nd,plateau,n,True)

def dessineConfig(plateau,n):
    for i in plateau:
        for j in i:
            dessineDisque(j,plateau,n)

def effaceTout(plateau,n):
    for i in plateau:
        for j in i:
            effaceDisque(j,plateau,n)

def effaceTours(n):
    turtle.color("white")
    rectangle(-70-30*(n-1),(n+1)*30-200,10,(n+1)*30)
    rectangle(-5,(n+1)*30-200,10,(n+1)*30)
    rectangle(60+30*(n-1),(n+1)*30-200,10,(n+1)*30)

# Partie C
def filtre(mot):
    entree = i
    
def lireCoords(plateau):
    while True:
        tourdep= 3
        while tourdep not in (-1,0,1,2):
            tourdep = int(input("Tour de départ ?"))
        if tourdep == -1:
            rep = input("Tu souhaites abandonner (o/n)? ")
            if rep == "o":
                return -1
        elif nbDisques(plateau,tourdep) == 0:
            print("Invalide, tour vide")
        else:   
            tourarr = 3
            while tourarr not in (0,1,2):
                tourarr = int(input("Tour de d'arrivée ?"))
            if verifDepl(plateau,tourdep,tourarr) == True:
                return tourdep,tourarr
            else:
                print("Invalide, disque plus petit.")

def jouerUnCoup(plateau,n):
    deplacement = lireCoords(plateau)
    if deplacement == -1:
        return True
    else:
        disque = disqueSup(plateau,deplacement[0])
        effaceDisque(disque,plateau,n)
        plateau[deplacement[1]].append(disque)
        del plateau[deplacement[0]][-1]
        dessineDisque(disque,plateau,n)
        return False

# Partie D

def dernierCoup(coups):
    lastcoup = max(list(coups.keys()))
    lastconfig = coups[lastcoup]
    befconfig = coups[lastcoup-1]
    tdep = 0
    tarr = 0
    for i in range(3):
        if len(lastconfig[i])-len(befconfig[i]) == -1:
            tdep = i
        elif len(lastconfig[i])-len(befconfig[i]) == 1:
            tarr = i
    return tdep,tarr

def annulerDernierCoup(coups,plateau,n):
    last = dernierCoup(coups)
    print(last)
    disque = disqueSup(plateau,last[1])
    effaceDisque(disque,plateau,n)
    plateau[last[0]].append(disque)
    del plateau[last[1]][-1]
    dessineDisque(disque,plateau,n)
    del coups[max(list(coups.keys()))]
    
def boucleJeu(coups,plateau,n):
    maxcoups = 2**n+n**2
    nbcoups = 0
    sortie = False
    while nbcoups <= maxcoups and verifVictoire(plateau,n) == False and sortie == False:
        nbcoups += 1
        print("Coup numéro",nbcoups)
        if len(coups) > 1:
            m = input("Souhaitez-vous annuler votre coup ?")
            if m == "o":
                annulerDernierCoup(coups,plateau,n)
                nbcoups -= 1
        sortie = jouerUnCoup(plateau,n)
        if sortie == False:
            coups[nbcoups] = deepcopy(plateau)
    if verifVictoire(plateau,n) == True:
        return "1",nbcoups
    elif sortie == True:
        return "0",nbcoups-1
    else:
        return "2"

# Partie E

def calcultemps(dep,arr):
    print(dep)
    print(arr)
    return (arr[0]-dep[0])*3600 + (arr[1]-dep[1])*60 + (arr[2]-dep[2])

def sauvScore(dico,nom,nbd,nbc,temps):
    if len(dico) == 0:
        dico[0] = (nom,nbd,nbc,temps)
    else:
        dico[max(dico.keys())+1] = (nom,nbd,nbc,temps)

def afficheScores(dico):
    if len(dico) != 0:
        listetriee = list(sorted(dico.values(), key=itemgetter(1,2)))
        for i in listetriee:
            print("Table des scores")
            print(i[0]," - ",i[1],"disque(s) - ",i[2],"coup(s) - ",i[3],"seconde(s)")
    else:
        print("Il n'y a pas encore de score")

def afficheChronos(dico):
    if len(dico) != 0:
        listetriee = list(sorted(dico.values(), key=itemgetter(3)))
        for i in listetriee:
            print("Table des temps")
            print(i[0]," - ",i[1],"secondes")
    else:
        print("Il n'y a pas encore de score")

def reflexionMoy(dico):
    if len(dico) != 0:
        d = {}
        d2 = {}
        for i in dico:
            if dico[i][0] not in d:
                d[dico[i][0]] = [(dico[i][2],dico[i][3])]
            else:
                d[dico[i][0]].append((dico[i][2],dico[i][3]))
        for i in d:
            sommetemps = 0
            sommenbc = 0
            for j in d[i]:
                sommetemps += j[1]
                sommenbc += j[0]
            d2[i] = round(sommetemps/sommenbc,2)
        return d2

def fastest(dico):
    if len(dico) != 0:
        newdico = reflexionMoy(dico)
        listetriee = list(sorted(newdico.items(), key=itemgetter(1)))
        for i in listetriee:
            print(i[0]," - ",i[1],"secondes par coup")
    else:
        print("Il n'y a pas encore de score")

# Partie F

def autoResol(nbd):
    autoplat = init(nbd)
    d = []
    if nbd%2 == 0:
        while verifVictoire(autoplat,nbd) == False:
            # Coup 1
            tdep = posDisque(autoplat,1)
            if tdep == 2:
                tarr = 0
            else:
                tarr = tdep+1
            d.append((tdep,tarr))
            autoplat[tarr].append(1)
            del autoplat[tdep][-1]
            # Coup 2
            l = [0,1,2]
            l.remove(posDisque(autoplat,1))
            derniercoup = (0,0)
            for i in l:
                for j in l:
                    if verifDepl(autoplat,i,j) == True:
                        derniercoup = (i,j)
                        d.append((i,j))
            autoplat[derniercoup[1]].append(disqueSup(autoplat,derniercoup[0]))
            del autoplat[derniercoup[0]][-1]               
    else:
        while verifVictoire(autoplat,nbd) == False:
            # Coup 1
            tdep = posDisque(autoplat,1)
            if tdep == 0:
                tarr = 2
            else:
                tarr = tdep-1
            d.append((tdep,tarr))
            autoplat[tarr].append(1)
            del autoplat[tdep][-1]
            # Coup 2
            l = [0,1,2]
            l.remove(posDisque(autoplat,1))
            derniercoup = (0,0)
            for i in l:
                for j in l:
                    if verifDepl(autoplat,i,j) == True:
                        derniercoup = (i,j)
                        d.append((i,j))
            autoplat[derniercoup[1]].append(disqueSup(autoplat,derniercoup[0]))
            del autoplat[derniercoup[0]][-1]
    return d

def autoanim(dico,plateau,n):
    for i in dico:
        disque = disqueSup(plateau,i[0])
        effaceDisque(disque,plateau,n)
        plateau[i[1]].append(disque)
        del plateau[i[0]][-1]
        dessineDisque(disque,plateau,n)

dicoScores = {}
dicochoix = {"1":"afficheScores(dicoScores)","2":"afficheChronos(dicoScores)","3":"fastest(dicoScores)"}
joue = True
while joue:
    print("Bienvenue dans les Tours de Hanoi")
    nbdisques = 0
    print("1- Classement des scores")
    print("2- Classement des temps")
    print("3- Classement des temps de réaction")
    print("4- Rien")
    choix = input("Entrez votre choix (1-2-3-4): ")
    if choix.strip() in ("1","2","3"):
        exec(dicochoix[choix])
    while nbdisques<1:
        nbdisques = int(input("Combien de disques ? "))
    plat = init(nbdisques)
    dicocoups = {}
    dicocoups[0] = deepcopy(plat)
    dessinePlateau(nbdisques)
    dessineConfig(plat,nbdisques)
    auto = input("Voulez-vous la résolution automatique du jeu ?: ")
    if auto.strip() in ("oui","o","Oui","O"):   
        hanoiResolu = autoResol(nbdisques)
        autoanim(hanoiResolu,plat,nbdisques)
    else:
        tempsdep = list(localtime())[3:6]
        fin = boucleJeu(dicocoups,plat,nbdisques)
        if fin[0] == "0":
            print("Abandon de la partie après",fin[1],"coups.\n")
        elif fin[0] == "1":
            tempsarr = list(localtime())[3:6]
            temps = calcultemps(tempsdep,tempsarr)
            print("Gagné")
            nom = input("Entrez votre nom : ")
            sauvScore(dicoScores,nom,nbdisques,fin[1],temps)
        else:
            print("perdu(trop de coups)")
    reponsejoue = input("Voulez-vous rejouer ?: ")
    if reponsejoue not in ("oui","o","Oui","O"):
        joue = False
    else:
        effaceTout(plat,nbdisques)
        effaceTours(nbdisques)
print("Au revoir")
