
import turtle
from copy import deepcopy
from time import localtime
from operator import itemgetter

# =========================
# PARTIE A
# =========================

def init(n):
    """Initialisation du plateau"""
    liste = [[], [], []]
    for i in range(n, 0, -1):
        liste[0].append(i)
    return liste


def nbDisques(plateau, numtour):
    return len(plateau[numtour])


def disqueSup(plateau, numtour):
    if nbDisques(plateau, numtour) == 0:
        return -1
    else:
        return plateau[numtour][-1]


def posDisque(plateau, numdisque):
    for i in plateau:
        if numdisque in i:
            return plateau.index(i)


def verifDepl(plateau, nt1, nt2):
    supnt2 = disqueSup(plateau, nt2)

    if len(plateau[nt1]) != 0:
        if supnt2 == -1 or plateau[nt1][-1] < supnt2:
            return True

    return False


def verifVictoire(plateau, n):
    if len(plateau[-1]) == n:
        b = list(plateau[-1])
        b.sort(reverse=True)

        if b == plateau[-1]:
            return True

    return False


# =========================
# PARTIE B
# =========================

def move_to(x, y):
    """Remplace turtle.teleport()"""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()


def rectangle(x, y, long, larg, colfill=False, color="white"):

    move_to(x, y)

    if colfill:
        turtle.begin_fill()
        turtle.fillcolor(color)
        turtle.color(color)

    for i in range(2):
        turtle.forward(long)
        turtle.right(90)

        turtle.forward(larg)
        turtle.right(90)

    if colfill:
        turtle.end_fill()


def dessinePlateau(n):

    turtle.setup(width=1200, height=600)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.bgcolor("black")
    turtle.color("white")

    rectangle(-350, -200, 700, 50, True, "white")

    rectangle(-70 - 30 * (n - 1),
              (n + 1) * 30 - 200,
              10,
              (n + 1) * 30,
              True,
              "white")

    rectangle(-5,
              (n + 1) * 30 - 200,
              10,
              (n + 1) * 30,
              True,
              "white")

    rectangle(60 + 30 * (n - 1),
              (n + 1) * 30 - 200,
              10,
              (n + 1) * 30,
              True,
              "white")


def dessineDisque(nd, plateau, n, delete=False, colfill=True):

    dicolor = {
        0: "yellow",
        1: "orange",
        2: "blue",
        3: "green",
        4: "purple",
        5: "red",
        6: "pink",
        7: "white"
    }

    posx = posDisque(plateau, nd)
    posy = plateau[posx].index(nd)

    xnd = (65 + 30 * (n - 1)) * (posx - 1) - (30 + 15 * (nd - 1))
    ynd = -200 + 30 * (posy + 1)

    if delete:

        rectangle(xnd, ynd,
                  60 + 30 * (nd - 1),
                  29,
                  True,
                  "black")

        turtle.color("white")

        move_to(-5 + (65 + 30 * (n - 1)) * (posx - 1), ynd)
        turtle.right(90)
        turtle.forward(30)

        move_to(5 + (65 + 30 * (n - 1)) * (posx - 1), ynd)
        turtle.forward(30)

        turtle.left(90)

    else:

        rectangle(
            xnd,
            ynd,
            60 + 30 * (nd - 1),
            29,
            colfill,
            dicolor[nd % len(dicolor)]
        )


def effaceDisque(nd, plateau, n):
    dessineDisque(nd, plateau, n, True)


def dessineConfig(plateau, n):
    for i in plateau:
        for j in i:
            dessineDisque(j, plateau, n)


def effaceTout(plateau, n):
    for i in plateau:
        for j in i:
            effaceDisque(j, plateau, n)


def effaceTours(n):

    turtle.color("black")

    rectangle(-70 - 30 * (n - 1),
              (n + 1) * 30 - 200,
              10,
              (n + 1) * 30,
              True,
              "black")

    rectangle(-5,
              (n + 1) * 30 - 200,
              10,
              (n + 1) * 30,
              True,
              "black")

    rectangle(60 + 30 * (n - 1),
              (n + 1) * 30 - 200,
              10,
              (n + 1) * 30,
              True,
              "black")


# =========================
# PARTIE C
# =========================

def lireCoords(plateau):

    while True:

        tourdep = 3

        while tourdep not in (-1, 0, 1, 2):
            tourdep = int(input("Tour de départ ? "))

        if tourdep == -1:

            rep = input("Tu souhaites abandonner (o/n) ? ")

            if rep == "o":
                return -1

        elif nbDisques(plateau, tourdep) == 0:

            print("Invalide, tour vide")

        else:

            tourarr = 3

            while tourarr not in (0, 1, 2):
                tourarr = int(input("Tour d'arrivée ? "))

            if verifDepl(plateau, tourdep, tourarr):
                return tourdep, tourarr

            else:
                print("Invalide, disque plus petit.")


def jouerUnCoup(plateau, n):

    deplacement = lireCoords(plateau)

    if deplacement == -1:
        return True

    disque = disqueSup(plateau, deplacement[0])

    effaceDisque(disque, plateau, n)

    plateau[deplacement[1]].append(disque)
    del plateau[deplacement[0]][-1]

    dessineDisque(disque, plateau, n)

    return False


# =========================
# PARTIE D
# =========================

def boucleJeu(coups, plateau, n):

    maxcoups = 2 ** n + n ** 2
    nbcoups = 0
    sortie = False

    while nbcoups <= maxcoups and not verifVictoire(plateau, n) and not sortie:

        nbcoups += 1

        print("Coup numéro", nbcoups)

        sortie = jouerUnCoup(plateau, n)

        if not sortie:
            coups[nbcoups] = deepcopy(plateau)

    if verifVictoire(plateau, n):
        return "1", nbcoups

    elif sortie:
        return "0", nbcoups - 1

    else:
        return "2"


# =========================
# PARTIE E
# =========================

def calcultemps(dep, arr):

    return (
        (arr[0] - dep[0]) * 3600
        + (arr[1] - dep[1]) * 60
        + (arr[2] - dep[2])
    )


def sauvScore(dico, nom, nbd, nbc, temps):

    if len(dico) == 0:
        dico[0] = (nom, nbd, nbc, temps)

    else:
        dico[max(dico.keys()) + 1] = (nom, nbd, nbc, temps)


def afficheScores(dico):

    if len(dico) != 0:

        listetriee = list(sorted(dico.values(), key=itemgetter(1, 2)))

        print("\n===== TABLE DES SCORES =====")

        for i in listetriee:
            print(
                i[0],
                "-",
                i[1],
                "disque(s) -",
                i[2],
                "coup(s) -",
                i[3],
                "seconde(s)"
            )

    else:
        print("Il n'y a pas encore de score")


# =========================
# PROGRAMME PRINCIPAL
# =========================

dicoScores = {}

joue = True

while joue:

    print("\nBienvenue dans les Tours de Hanoi")

    nbdisques = 0

    while nbdisques < 1:
        nbdisques = int(input("Combien de disques ? "))

    plat = init(nbdisques)

    dicocoups = {}
    dicocoups[0] = deepcopy(plat)

    turtle.clear()

    dessinePlateau(nbdisques)
    dessineConfig(plat, nbdisques)

    tempsdep = list(localtime())[3:6]

    fin = boucleJeu(dicocoups, plat, nbdisques)

    if fin[0] == "0":

        print("Abandon de la partie après", fin[1], "coups.")

    elif fin[0] == "1":

        tempsarr = list(localtime())[3:6]

        temps = calcultemps(tempsdep, tempsarr)

        print("Gagné !")

        nom = input("Entrez votre nom : ")

        sauvScore(
            dicoScores,
            nom,
            nbdisques,
            fin[1],
            temps
        )

    else:

        print("Perdu (trop de coups)")

    reponsejoue = input("Voulez-vous rejouer ? (o/n) : ")

    if reponsejoue.lower() not in ("oui", "o"):
        joue = False

print("Au revoir")

turtle.done()

