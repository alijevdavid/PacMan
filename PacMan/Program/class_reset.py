import pygame
import random

#reset gomb kirajzolása
class Reset:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 20)

    def Gomb(self,font, screen, feher):
        teglalap = self.rect
        pygame.draw.rect(screen, feher, teglalap, 3)
        reset_sz = font.render ("Restart", True, feher)
        screen.blit(reset_sz, (teglalap.x + 14, teglalap.y + 3))



        



    

    

