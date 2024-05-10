import pygame

class Pacman(pygame.sprite.Sprite):
    def __init__(self, sebesseg):
        pygame.sprite.Sprite.__init__(self)
        self.sebesseg = sebesseg

        
        kep = pygame.image.load("pac.png")
        self.kep = pygame.transform.scale(kep,(int(kep.get_width()*0.15),int(kep.get_height()*0.15)))
        self.rect = self.kep.get_rect()
        #kezdőértékek
        self.kezdox = 460
        self.kezdoy = 540
        self.x = self.kezdox
        self.y = self.kezdoy
        self.rect.center = (self.x,self.y)

        self.pacman_pontsz = 0
        self.pacman_elet = 3
        
        #fordulási irányok definiálása
        self.fordit_bal = pygame.transform.flip(self.kep, True, False)
        self.fordit_jobb = self.kep
        self.fordit_fel = pygame.transform.rotate(self.kep,90)
        self.fordit_le = pygame.transform.rotate(self.kep,270)

        self.irany = (0, 0)

        self.high_score_betolt()
    #high_score változó beolvasása és eltárolása a szövegfájlból
    def high_score_betolt(self):
        with open ("magaspontsz.txt", "rt", encoding = "utf-8") as f:
            try:
                self.high_score = int(f.read())
            except:
                pass
    #mozgatás
    def Mozgat(self,szint,mozg_bal,mozg_jobb,mozg_fel,mozg_le, engedelyezo, blockmeret):
        if engedelyezo:
            x = self.rect.center[0]
            y = self.rect.center[1]
            ujx = x + self.irany[0]*self.sebesseg
            ujy = y + self.irany[1]*self.sebesseg
            ix = x // blockmeret
            iy = y // blockmeret

            ujirany = None
            blockon = False

            # all, vagy eppen blockon van-e
            all = self.irany[0] == 0 and self.irany[1] == 0
            ugyanazablock = ix == ujx//blockmeret and iy == ujy//blockmeret
            blockkozepe_szele = (x % blockmeret)//(blockmeret/2) != (ujx % blockmeret)//(blockmeret/2) or (y % blockmeret)//(blockmeret/2) != (ujy % blockmeret)//(blockmeret/2)

            # ha pacman áll vagy a folyosó közepe és pacman közepe egybe esik, akkor kér új irányokat
            if all or (ugyanazablock and blockkozepe_szele):
                blockon = True

                # ebbe az iranyba szeretne menni
                if mozg_bal and self.irany[0] != -1:
                    ujirany = (-1, 0)
                if mozg_jobb and self.irany[0] != 1:
                    ujirany = (1, 0)
                if mozg_fel and self.irany[1] != -1:
                    ujirany = (0, -1)
                if mozg_le and self.irany[1] != 1:
                    ujirany = (0, 1)
            else:
                # ellenkezo iranyba barmikor mehet
                if mozg_bal and self.irany[0] == 1:
                    self.irany = (-1, 0)
                if mozg_jobb and self.irany[0] == -1:
                    self.irany = (1, 0)
                if mozg_fel and self.irany[1] == 1:
                    self.irany = (0, -1)
                if mozg_le and self.irany[1] == -1:
                    self.irany = (0, 1)

            # mehet-e az uj iranyba
            if ujirany != None:
                if szint[iy + ujirany[1]][ix + ujirany[0]] != "W":
                    self.irany = ujirany

            # siman falba utkozik
            if blockon:
                if szint[iy + self.irany[1]][ix + self.irany[0]] == "W":
                    self.irany = (0, 0)

                # folyoso kozepere helyezi
                if self.irany[0] == 0:
                    self.rect.center = (ix*blockmeret + (blockmeret/2), self.rect.center[1])
                if self.irany[1] == 0:
                    self.rect.center = (self.rect.center[0], iy*blockmeret + (blockmeret/2))



            # mozgat
            self.rect.x += self.irany[0]*self.sebesseg
            self.rect.y += self.irany[1]*self.sebesseg

    #pacman megjelenítése
    def Rajzol(self, screen):
        if self.irany[0] == -1:
            self.kep = self.fordit_bal
        elif self.irany[0] == 1:
            self.kep = self.fordit_jobb
        elif self.irany[1] == -1:
            self.kep = self.fordit_fel
        elif self.irany[1] == 1:
            self.kep = self.fordit_le

        screen.blit(self.kep, self.rect)

    #mozgás letiltása
    def Allj(self):
        self.irany = (0,0)
        
    #kiindulási helyzet
    def KozepreVissza(self):
        self.rect.x = self.kezdox
        self.rect.y = self.kezdoy
