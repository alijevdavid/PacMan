import pygame
import random

szellemek = []
class Szellem:
    def __init__(self, szint, x, y, blockmeret):
        self.sebesseg = 1
        kep = pygame.image.load("szellem.png")
        kep_kek = pygame.image.load("szellem_kek.png")
        self.kep_kek_kicsi = pygame.transform.scale(kep_kek, (int(kep_kek.get_width() * 0.15), int(kep_kek.get_height() * 0.15)))
        self.kep = pygame.transform.scale(kep, (int(kep.get_width() * 0.15), int(kep.get_height() * 0.15)))
        self.rect = self.kep.get_rect()
        self.rect.center = (x, y)
        self.kezdo = (x, y)
        
        #irányítási függvény folyamatos meghívása
        self.irany = self.UjRandomIrany(szint, x//blockmeret, y//blockmeret)


    #random irányok eltárolása a lehetséges helyekre
    def UjRandomIrany(self, szint, ix, iy):
        ujirany = []
        if szint[iy][ix-1] != "W":
            ujirany.append((-1, 0))
        if szint[iy][ix+1] != "W":
            ujirany.append((1, 0))
        if szint[iy-1][ix] != "W":
            ujirany.append((0, -1))
        if szint[iy+1][ix] != "W":
            ujirany.append((0, 1))

        if (len(ujirany) == 0):
            return None
        else:
            #random listaindex
            return ujirany[random.randint(0, len(ujirany)-1)]

    #a lehetséges irényok közül kiválasztja azt amelyekkel közelebb kerülhet Pacmanhez
    def UjIranyPlayerFele(self, szint, ix, iy, player):
        ujirany = []
        if player.rect.center[0] < self.rect.center[0] and self.irany[0] == 0:
            if szint[iy][ix-1] != "W":
                ujirany.append((-1, 0))
        if player.rect.center[0] > self.rect.center[0] and self.irany[0] == 0:
            if szint[iy][ix+1] != "W":
                ujirany.append((1, 0))
        if player.rect.center[1] < self.rect.center[1] and self.irany[1] == 0:
            if szint[iy-1][ix] != "W":
                ujirany.append((0, -1))
        if player.rect.center[1] > self.rect.center[1] and self.irany[1] == 0:
            if szint[iy+1][ix] != "W":
                ujirany.append((0, 1))

        if (len(ujirany) == 0):
            return None
        else:
            return ujirany[random.randint(0, len(ujirany)-1)]

    #mozgatás
    def Mozgat(self, szint, player, engedelyezo, blockmeret):
        if engedelyezo:
            x = self.rect.center[0]
            y = self.rect.center[1]
            ujx = x + self.irany[0]*self.sebesseg
            ujy = y + self.irany[1]*self.sebesseg
            
            #mátrix aktuális indexei
            ix = x // blockmeret
            iy = y // blockmeret

            # eppen blockon van-e
            ugyanazablock = ix == ujx//blockmeret and iy == ujy//blockmeret
            blockkozepe_szele = (x % blockmeret)//(blockmeret/2) != (ujx % blockmeret)//(blockmeret/2) or (y % blockmeret)//(blockmeret/2) != (ujy % blockmeret)//(blockmeret/2)

            
            if blockkozepe_szele and ugyanazablock:
                ujirany = self.UjIranyPlayerFele(szint, ix, iy, player)
                if ujirany == None:
                    if szint[iy + self.irany[1]][ix + self.irany[0]] == "W":
                        ujirany = self.UjRandomIrany(szint, ix, iy)

                if ujirany != None:
                    self.irany = ujirany
                    # block kozepere helyezi
                    self.rect.center = (ix*blockmeret + (blockmeret/2), iy*blockmeret + (blockmeret/2))

            # mozgat
            self.rect.x += self.irany[0]*self.sebesseg
            self.rect.y += self.irany[1]*self.sebesseg

    #középre helyezi, mozgás letiltása
    def Kozepre_Vissza (self):
        self.rect.center = (460,460)
        self.sebesseg = 0
    #mozoghat
    def Mozoghat (self):
        self.sebesseg = 1
