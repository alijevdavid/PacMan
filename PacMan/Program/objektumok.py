import pygame
import random

falak = []
class Fal(object):
    def __init__(self, x, y, blockmeret):
        #listához hozzáadja az objektumot
        falak.append(self)
        self.rect = pygame.Rect(x, y, blockmeret, blockmeret)

pottyok = []
class Potty:
    def __init__(self, x, y):
        #listához hozzáadja az objektumot
        pottyok.append(self)
        self.rect = pygame.Rect(x, y, 1, 1)

nagyobb_pottyok = []
class PottyNagy:
    def __init__(self, x, y):
        #listához hozzáadja az objektumot
        nagyobb_pottyok.append(self)
        self.rect = pygame.Rect(x, y, 1, 1)

cseresznye = []
class Cseresznye:
    def __init__(self ,x, y):
        #kép betöltése, listához hozzáadja az objektumot
        cseresznye.append(self)
        kep = pygame.image.load("cseresznye.png")
        self.kep = pygame.transform.scale(kep,(int(kep.get_width()*0.06),int(kep.get_height()*0.06)))
        self.rect = self.kep.get_rect()
        self.rect.center = (x, y)
        self.van_cseresznye = False
    #választ random egy helyzetet
    def RandomValaszt (self, ertek):
        return random.choice(ertek)
