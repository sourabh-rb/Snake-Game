# -*- coding: utf-8 -*-
"""
SNAKE Game

@author: Sourabh Rajeev Badagandi
"""

import pygame
import sys
import random
import time

pygame.init()

maxWinHeight = 500
maxWinWidth = 500
blockSize = 10

#############################################################################
#CLASSES
#############################################################################
#Snake class to handle behaviour of the snake.
class Snake():
    def __init__(self):
        self.position = [250, 250]
        self.body = [[250,250], [240,250]]
        self.direction = "RIGHT"
        self.changeDirection = self.direction
    
    #Function to update snake head direction.    
    def changeDirectionTo(self, direction):
        if direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if direction == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if direction == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"
            
    # Function to handle snake movement and also grow if food is eaten.    
    def move(self, foodPos):
        if self.direction == "RIGHT":
            self.position[0] += blockSize
        if self.direction == "LEFT":
            self.position[0] -= blockSize
        if self.direction == "UP":
            self.position[1] -= blockSize
        if self.direction == "DOWN":
            self.position[1] += blockSize
            
        self.body.insert(0, list(self.position))
        
        if self.position == foodPos:
            return 1
        else:
            self.body.pop()
            return 0
        
    # Function to check if there is collision at the window boundries or with own snake body.       
    def checkCollision(self):
        if self.position[0] > (maxWinHeight - blockSize) or self.position[0] < 0:
            return 1
        
        if self.position[1] > (maxWinWidth -  blockSize) or self.position[1] < 10:
            return 1  
        #Check excluding first element which is the head.
        for part in self.body[1:]:
            if self.position == part:
                return 1
        #No collision
        return 0
    
    #Function to get the head position of the snake.
    def getHeadPosition(self):
        return self.position
    
    #Function to get the whole snake body.
    def getBody(self):
        return self.body
    

#FoodSpawner class to spawn food randomly on the game window.
class FoodSpawner():
    def __init__(self):
        #Generate position of food randomly.
        self.position = [(random.randrange(1, 50)* 10), (random.randrange(1, 50)* 10)]
        self.present = True
        
    #Function to generate new food location.        
    def spawnFoodPosition(self):
        if self.present == False:
            self.position = [(random.randrange(1, 50)* 10), (random.randrange(1, 50)* 10)]
            self.present = True
        
        return self.position
    
    #Function to update food visibility.
    def foodVisible(self, visibility):
        self.present = visibility

#############################################################################
#HANDLERS
#############################################################################
        
def getTextObject(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def displayMessage(text, font, color, size, posX, posY):
    fontStyle = pygame.font.Font(font, size)    
    textSurface, textRect = getTextObject(text, fontStyle, color)
    textRect.center = (posX, posY)
    window.blit(textSurface, textRect)
  
    
#Game Over Loop    
def gameOver():
    window.fill(pygame.Color(225, 225, 225))
    displayMessage('GAME OVER', 'snake_font.ttf', pygame.Color(0,0,0), 130,(maxWinWidth / 2), (maxWinHeight / 4))
    displayMessage('Press R to Restart', 'snake_font.ttf', pygame.Color(0,0,0), 60,(maxWinWidth / 2), (maxWinHeight - maxWinHeight / 4))
    displayMessage('Press Q to Quit', 'snake_font.ttf', pygame.Color(0,0,0), 60,(maxWinWidth / 2), (maxWinHeight - maxWinHeight / 6))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r :
                    gameLoop()
                if event.key == pygame.K_q:
                    exitGame()
        pygame.display.update()
        fps.tick(15)
        
# Exit Game handler
def exitGame():
    window.fill(pygame.Color(225, 225, 225))
    displayMessage('See you later!', 'snake_font.ttf', pygame.Color(0,0,0), 100,(maxWinWidth / 2), (maxWinHeight / 2))
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    sys.exit()

# Display Score handler.    
def displayScore(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, pygame.Color(0,0,0))
    window.blit(text,(0,0))

# Game Intro Loop
def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
                
        window.fill(pygame.Color(225, 225, 225))
        displayMessage('SNAKE', 'snake_font.ttf', pygame.Color(0,0,0), 220, (maxWinWidth / 2), (maxWinHeight / 4))
        
        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        
        # Ideally we have to create a separate function to create buttons, 
        # I will be using them only here so leaving this code.
        if 50 + 100 > mousePos[0] > 50 and 350 + 50 > mousePos[1] > 350 :
            pygame.draw.rect(window, (0, 0, 0),(46,346,108,58))
            pygame.draw.rect(window, (0, 255, 0),(50,350,100,50))
            pygame.draw.rect(window, (0, 128, 128),(346,346,108,58))
            pygame.draw.rect(window, (225, 0, 0),(350,350,100,50))
            if mouseClick[0] == 1 :
                gameLoop()
        
        elif  350 + 100 > mousePos[0] > 350 and 350 + 50 > mousePos[1] > 350 :
            pygame.draw.rect(window, (0, 128, 128),(46,346,108,58))
            pygame.draw.rect(window, (0, 225, 0),(50,350,100,50))
            pygame.draw.rect(window, (0, 0, 0),(346,346,108,58))
            pygame.draw.rect(window, (255, 0, 0),(350,350,100,50))
            
            if mouseClick[0] == 1 :
                exitGame()
        else:
            pygame.draw.rect(window, (0, 128, 128),(46,346,108,58))
            pygame.draw.rect(window, (0, 225, 0),(50,350,100,50))
            pygame.draw.rect(window, (0, 128, 128),(346,346,108,58))
            pygame.draw.rect(window, (225, 0, 0),(350,350,100,50))
        
        displayMessage('START', 'snake_font.ttf', pygame.Color(0,0,0), 50, (50 + 100 / 2), (350 + 22))
        displayMessage('QUIT', 'snake_font.ttf', pygame.Color(0,0,0), 50, (350 + 52), (350 + 22))
        pygame.display.update()
        fps.tick(15)
    
# Main Game Loop
def gameLoop():
    
    score = 0
    snake = Snake()
    food = FoodSpawner()
    while True:
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                exitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.changeDirectionTo("RIGHT")
                if event.key == pygame.K_LEFT:
                    snake.changeDirectionTo("LEFT")
                if event.key == pygame.K_UP:
                    snake.changeDirectionTo("UP")
                if event.key == pygame.K_DOWN:
                    snake.changeDirectionTo("DOWN")
        
        newFood = food.spawnFoodPosition()
         
        if (snake.move(newFood) == 1):
            score += 1
            food.foodVisible(False)
            
        window.fill(pygame.Color(225, 225, 225))
            
        for snakeBody in snake.getBody():
            pygame.draw.rect(window, pygame.Color(0, 225, 0), pygame.Rect(snakeBody[0], snakeBody[1], 10, 10))
                
        pygame.draw.rect(window, pygame.Color(225, 0, 0), pygame.Rect(newFood[0], newFood[1], 10, 10))
            
        if(snake.checkCollision() == 1):
            gameOver()
         
        displayScore(score)
        
        pygame.display.set_caption("Snake | Score is "+ str(score))
        pygame.display.update()
        
        fps.tick(24)           


# Main 
        
window = pygame.display.set_mode(((maxWinHeight), maxWinWidth))
pygame.display.set_caption("SNAKE")
fps = pygame.time.Clock()

window.fill(pygame.Color(225, 225, 225))

gameIcon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(gameIcon)

gameIntro()

# Code should not reach here !
pygame.quit()
sys.exit()







        
