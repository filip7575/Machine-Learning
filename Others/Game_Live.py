# -*- coding: utf-8 -*-

import sys, pygame
import numpy as np
import time

size = width, height = 500, 500

nxC = 60
nyC = 60

#dimension celda
dimCW = (width-1)  / nxC
dimCH = (height-1) / nyC

bg = 25, 25, 25

screen = pygame.display.set_mode(size)

screen.fill(bg)

gameState = np.zeros((nxC, nyC))

gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

print(gameState)
while 1:
    
    screen.fill(bg)
    
    new_gameState = np.copy(gameState)
    
    for y in range(0, nyC):
        for x in range(0, nxC):
            
            n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                      gameState[(x) % nxC, (y - 1) % nyC] + \
                      gameState[(x+1) % nxC, (y - 1) % nyC] + \
                      gameState[(x-1) % nxC, (y) % nyC] + \
                      gameState[(x+1) % nxC, (y) % nyC] + \
                      gameState[(x-1) % nxC, (y+1) % nyC] + \
                      gameState[(x) % nxC, (y + 1) % nyC] + \
                      gameState[(x+1) % nxC, (y + 1) % nyC] 
                   
            # Una celula muerta con exactamente 3 celulas vecinas viva "nace"
            #print(n_neigh)
            if gameState[x,y] == 0 and n_neigh == 3:
               new_gameState[x,y] = 1
            elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
               new_gameState[x,y] = 0
            
            poly = [((x) * dimCW, (y) * dimCH),
                    ((x+1) * dimCW, (y) * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]
            
            pygame.draw.polygon(screen,(128,128,128,128),poly, int(abs(1 - new_gameState[x,y])))
    
    gameState = new_gameState
    time.sleep(0.2)
    pygame.display.flip()
    
    

