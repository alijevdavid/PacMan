#Alijev Dávid-ZIJD8B
import pygame
import palya
import class_reset
import class_pacman
import class_szellem
import objektumok
import random
import time

pygame.init()
#pálya mérete
kijelzo_szeles = 920
kijelzo_magas = 1000

#pályán található négyzetek oldalainak hossza
blockmeret = 40

#kijelző definiálás
screen = pygame.display.set_mode((kijelzo_szeles ,kijelzo_magas))
pygame.display.set_caption("Pacman game")

#programban használt színek
feher = (255, 255, 255)
falakszine = (33,33,255)
fekete = (0,0,0)

#program hátterének folyamatos kitöltése feketével
def kijelzofriss():
    screen.fill(fekete)

#elért pontszám kiírása
def pontszam_mutat(x,y,pontsz,font):
    pont = font.render ("Pontszám: " + str(pontsz), True, feher)
    screen.blit(pont, (x,y))

#fennmaradó életel kiírása
def elet_mutat (x,y,kep,elet):
    helyek_mutat = [(x+40,y), (x+80,y), (x+120,y)]
    for i in range(elet):
        screen.blit(kep, (helyek_mutat[i]))

#fügvvény számos felirat kiírásához
def kiiras (x, y, font, szoveg, engedelyezo):
    if not engedelyezo:
        screen.blit(font.render (szoveg, True, feher), (x,y))

#timer
def idozito(start,mp):
    eltelt = (pygame.time.get_ticks()-start)/1000
    if eltelt < mp and start !=0:
        return eltelt
    else:
        return None

#ha a pontszám meghaladja az eddig elért legnagyobb pontszámot, ez a függvény betölti ezt a text fájlba
def high_score_frissit(high_score,pacman_pontsz):
    if high_score <= pacman_pontsz:
        high_score = pacman_pontsz
        with open ("magaspontsz.txt", "wt", encoding = "utf-8") as f:
            f.write(f"{pacman_pontsz}")

#ciklus amely végigmegy a 2D-s mátrixon
def matrix_beolvas():
    x = y = 0
    for sor in palya.szintek:
        for oszlop in sor:
            if oszlop == "W":
                objektumok.Fal(x, y, blockmeret)
            if oszlop == "*":
                potty = objektumok.Potty(x+(blockmeret/2),y+(blockmeret/2))
                objektumok.pottyok.append (potty)
            if oszlop == "G":
                g = class_szellem.Szellem(palya.szintek, x+(blockmeret//2),y+(blockmeret//2), blockmeret)
                class_szellem.szellemek.append(g)
            if oszlop == ".":
                objektumok.PottyNagy(x+(blockmeret/2),y+(blockmeret/2))
            
            x += blockmeret
        y += blockmeret
        x = 0

#teljes újraindítás
def TeljesRestart(matrix_beolvas):
    objektumok.falak.clear()
    objektumok.pottyok.clear()
    objektumok.nagyobb_pottyok.clear()
    objektumok.cseresznye.clear()
    class_szellem.szellemek.clear()
    matrix_beolvas()

def main():
    #objektumok definiálása
    player = class_pacman.Pacman(2)
    cseresznye = objektumok.Cseresznye (100,100)
    Reset = class_reset.Reset(800, 10)

    matrix_beolvas()
    
    #framerate
    ora = pygame.time.Clock()
    FPS = 60

    #mozgások alaphelyzetbe állítása
    mozg_bal = False
    mozg_jobb = False
    mozg_le = False
    mozg_fel = False

    #main()-függvényben használt változók
    font = pygame.font.Font("freesansbold.ttf",15)
    start = 0
    engedelyezo = False
    nyertes_engedelyezo = True
    
    run = False

    while not run:

        kijelzofriss()
        ora.tick(FPS)

        #változó amely megmondja, hogy Pacman képes-e megenni a szellemeket vagy sem, amúgy mindig False
        szellem_eves = False
        
        #ha a start nem egyenlő None-al, az időzítő elindul
        if idozito(start,10) != None:
            szellem_eves = True
            szellem_kep = g.kep_kek_kicsi
        #falak kirajzolása
        for fal in objektumok.falak:
            pygame.draw.rect(screen, falakszine, fal.rect)
         
        #pöttyök kirajzolása
        for p in objektumok.pottyok:
            #ha elfogyott az össze pötty, a játékos nyert
            if len(objektumok.pottyok) == 1:
                player = class_pacman.Pacman(2)

                TeljesRestart(matrix_beolvas)
                engedelyezo = False
                nyertes_engedelyezo = False
                start = 0
            # ha a player ütközik egy pöttyel
            if p.rect.colliderect(player.rect):
                objektumok.pottyok.remove(p)
                player.pacman_pontsz += 10
                
            else:
                pygame.draw.circle(screen,feher,p.rect[:2],2)

        #cseresznye megjelenítés
        for cs in objektumok.cseresznye:
            #ha nincs cseresznye a kijelzőn, választ magának egy random helyet, és elindítja a timert
            if cs.van_cseresznye == False:
                try:
                    random_potty = cs.RandomValaszt(objektumok.pottyok)
                except:
                    pass
                start_cs = pygame.time.get_ticks()
                felt_cs = 1
                cs.van_cseresznye = True

            #timer elindítása, eddig áll a cseresznye egy helyben, aztán helyzetet változtat
            if idozito(start_cs, 10) != None:
                screen.blit(cs.kep, (random_potty.rect.x-(blockmeret//2),random_potty.rect.y-(blockmeret//2)))
            else:
                #visszarakja a listába az objektumot
                objektumok.cseresznye[0] = cseresznye
                cs.van_cseresznye = False

            #ha pacman megeszi a cseresznyét, kap 100 pontot
            if random_potty.rect.colliderect(player.rect):
                player.pacman_pontsz += 100
                cs.van_cseresznye = False

       #szellemek kirajzolása, és random módon keringés leprogramozása
        for g in class_szellem.szellemek:
            g.Mozgat(palya.szintek, player, engedelyezo, blockmeret)
            if not szellem_eves:
                szellem_kep = g.kep
                g.Mozoghat()
            screen.blit(szellem_kep,g.rect)
            if g.rect.colliderect(player.rect):
                if not szellem_eves:
                    #ilyenkor pacman veszít egy életet
                    player.pacman_elet -= 1

                    player.KozepreVissza()
                    player.Allj()
                    mozg_bal = False
                    mozg_jobb = False
                    mozg_le = False
                    mozg_fel = False
                    player.kep = player.fordit_jobb

                if szellem_eves:
                    #ilyenkor pacman megehti a szellemeket, kap 200 pontot, a szellemek középre kényszerülnek, és egy ideig nem mozoghatnak
                    player.pacman_pontsz += 200
                    g.Kozepre_Vissza()

        #nagypöttyök kirajzolása
        for nagy_potty in objektumok.nagyobb_pottyok:
            if nagy_potty.rect.colliderect(player.rect):
                #ilyenkor a szellemek elfogyasztása lehetővé válik, elindul a timer, a játékos kap 20 pontot
                objektumok.nagyobb_pottyok.remove(nagy_potty)
                player.pacman_pontsz += 20
                start = pygame.time.get_ticks()   
            else:
                pygame.draw.circle(screen,feher,nagy_potty.rect[:2],10)



        #reset gomb kirajzolása
        Reset.Gomb(font, screen, feher)

        #gombnyomásra a karakter az adott irányba elindul és elfordul mindaddig, amíg másik irányt nem kap, vagy falba ütközik
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Reset.rect.collidepoint(event.pos):
                    #ha a reset gombra rákattintunk, a program teljesen újraindul
                    player = class_pacman.Pacman(2)

                    TeljesRestart(matrix_beolvas)
                    engedelyezo = False
                    nyertes_engedelyezo = True
                    start = 0

            #ha az jobb felső "X"-re kattintunk, akkor kilép a programból
            if event.type == pygame.QUIT:
                run = True
                
            if event.type == pygame.KEYDOWN:
                #"ENTER" billentyű lenyomása után a játék elindul
                if event.key == pygame.K_RETURN:
                   engedelyezo = True
                   nyertes_engedelyezo = True
                #különböző nyilak lenyomásának hatására beállítódnak az irányváltozók
                if event.key == pygame.K_LEFT:
                    mozg_bal = True
                    mozg_jobb = False
                    mozg_le = False
                    mozg_fel = False

                if event.key == pygame.K_RIGHT:
                    mozg_jobb = True
                    mozg_bal = False
                    mozg_le = False
                    mozg_fel = False
                    
                if event.key == pygame.K_UP:
                    mozg_fel = True
                    mozg_bal = False
                    mozg_jobb = False
                    mozg_le = False

                if event.key == pygame.K_DOWN:
                    mozg_le = True
                    mozg_fel = False
                    mozg_bal = False
                    mozg_jobb = False

                #ha az "ESCAPE"-re kattintunk, akkor kilép a programból
                if event.key == pygame.K_ESCAPE:
                    run = True
        #pacman mozgatása
        player.Mozgat(palya.szintek, mozg_bal, mozg_jobb, mozg_fel, mozg_le, engedelyezo, blockmeret)
        
        #pacman megjelenítése
        player.Rajzol(screen)

        #ha a játékos az összes életét elveszítette, a program újraindul
        if player.pacman_elet <= 0:
                player = class_pacman.Pacman(2)

                TeljesRestart(matrix_beolvas)
                engedelyezo = False
                nyertes_engedelyezo = True
                start = 0
                
        high_score_frissit(player.high_score,player.pacman_pontsz)

        #különböző információk kiírása a kepernyőre
        pontszam_mutat(40,300,player.pacman_pontsz,font)
        elet_mutat(40,400,player.fordit_jobb, player.pacman_elet)
        kiiras (40,330,font, "Gratulálok, nyertél!", nyertes_engedelyezo)
        kiiras (40,350,font, "Kezdéshez: \"ENTER\"", engedelyezo)
        kiiras(40, 10, font, "High Score: " + str(player.high_score), False)
        
        #képernyő folyamatos frissítése
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
