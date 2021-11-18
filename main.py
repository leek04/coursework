import pygame
import sys
import math
import random

pygame.init()

display = pygame.display.set_mode((800,600)) #sets size of the window
clock = pygame.time.Clock()

playerwalk = [pygame.image.load("player.png"),pygame.image.load("playerwalk1.png"),pygame.image.load("playerwalk2.png"),pygame.image.load("playerwalk3.png")] #loads the images used for the player walking

pygame.display.set_caption("Ben's Game") #sets what the game is called


backgroundImage = pygame.image.load("background.jpg").convert() #loads the background of the title screen
backgroundImage = pygame.transform.scale(backgroundImage,(800,600)).convert()

myfont = pygame.font.SysFont('Comic Sans MS', 25) #creates a text font and size to be used in the game
textsurface = myfont.render("BEN'S GAME PROTOTYPE 1 (you are the solid guy)", False, (255, 255, 255)) #creates an area on the screen where text can be shown

def intro(): #defines what the title screen looks like, including the button to start the game, where the text and the button is located on the screen, and the colour of the text and button
  intro = True
  while intro:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      display.blit(backgroundImage, [0,0]) #creates the title of the game
      largeText = pygame.font.Font("freesansbold.ttf", 75)
      textSurf, textRect = text_objects("Ben's Game", largeText)
      textRect.center = ((400), (150))
      display.blit(textSurf, textRect)

      button('Start Game', 400,400,100,50, (0,0,0), (0,0,255), gameloop)       #positions where the button is an what it says

      pygame.display.update()
      clock.tick(60)

def button(msg,x,y,w,h,ic,ac,action = None): #defines the button, including what sort of font it uses, what colour it is when not pressed, and what colour it in when it is pressed
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  pygame.draw.rect(display, ic,(x,y,w,h))

  if x+w > mouse[0] > x and y+h > mouse[1] > y:
    pygame.draw.rect(display, ac,(x,y,w,h))
    if click [0] == 1 and action !=None:
      action()

  else:
    pygame.draw.rect(display, ac,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display.blit(textSurf, textRect)

def text_objects(text, font):
  screen = font.render(text, True, (255,255,255))
  return screen, screen.get_rect()

def gameloop(): #defines what happens when the game starts. this whole def function includes the player, the bullets that the player shoots on spacebar press, and the single enemy (as of prototype 1)
  class Player: #define the player, including where it is on the screen and its animations when moving left and right
    def __init__(self, x, y, width, height):
      self.x = x 
      self.y = y
      self.width = width
      self.height = height
      self.animation_count = 0
      self.moving_right = False
      self.moving_left = False
      self.hitbox = (self.x, self.y,32,32)

    def main(self, display):
      if self.animation_count + 1 >= 16:
        self.animation_count = 0

      self.animation_count += 1

      if self.moving_right:
        display.blit(pygame.transform.scale(playerwalk[self.animation_count//4], (32,32)), (self.x, self.y))

      elif self.moving_left:
        display.blit(pygame.transform.scale(pygame.transform.flip(playerwalk[self.animation_count//4],True, False), (32,32)), (self.x, self.y))  

      else:
        display.blit(pygame.transform.scale(playerwalk[0], (32,32)), (self.x, self.y))
      self.moving_right = False
      self.moving_left = False
      self.hitbox = (self.x, self.y, 32, 32)
      pygame.draw.rect(display, (255,0,0), self.hitbox,2)

  class PlayerBullet: #defines the bullet that the player shoots, including where it travels, how it is drawn, the colour of the bullet and its velocity
    def __init__(self, x, y, mouse_x, mouse_y):
      self.x = x
      self.y = y
      self.mouse_x = mouse_x
      self.mouse_y = mouse_y
      self.speed = 15
      self.angle = math.atan2(y - mouse_y, x - mouse_x)
      self.x_vel = math.cos(self.angle) * self.speed
      self.y_vel = math.sin(self.angle) * self.speed
      self.hitbox = (self.x, self.y,16,16)
    def main(self, display):
      self.x -= int(self.x_vel)
      self.y -= int(self.y_vel)

      pygame.draw.circle(display, (60,172,215), (self.x, self.y), 5)

  class GhostEnemy: #defines the single enemy (as of prototype 1), including its animations and its movement patterns, adn where it is on the screen
    def __init__ (self, x, y):
      self.x = x
      self.y = y
      self.animation_images = [pygame.image.load("christmas past.png"),pygame.image.load("christmas past walk1.png"),pygame.image.load("christmas past walk2.png"),pygame.image.load("christmas past walk3.png")]
      self.animation_count = 0
      self.reset_offset = 0
      self.offset_x = random.randrange(-150, 150)
      self.offset_y = random.randrange(-150, 150)
      self.hitbox = (self.x,self.y,32,32)

    def main(self, display):
      if self.animation_count + 1 == 16:
        self.animation_count  = 0
      self.animation_count += 1

      self.hitbox = (self.x,self.y,32,32)
      pygame.draw.rect(display,(255,0,0),self.hitbox,2)

      if self.reset_offset == 0: #makes the enemy move towards the player but with added randomness
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)
        self.reset_offset = random.randrange(120, 150)
      else:
        self.reset_offset -= 1

      if player.x + self.offset_x > self.x-display_scroll[0]:
        self.x += 1
      elif player.x + self.offset_x < self.x-display_scroll[0]:
        self.x -= 1

      if player.y + self.offset_y > self.y-display_scroll[0]:
        self.y += 1
      elif player.y + self.offset_y < self.y-display_scroll[0]:
        self.y -= 1

      display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4],(32,32)),(self.x-display_scroll[0], self.y-display_scroll[1]))

    def hit(self):
      print('hit')
    
  enemies = [GhostEnemy(400,400)] #adds the enemies to an list that lists all of the different enemies and where they spawn on the screen

  player = Player(400, 300, 32, 32) #spawns the player on the screen with a certain size

  display_scroll = [0,0]

  player_bullet = []

  while True:
    display.fill((65, 102, 57)) #creates the background of the game with a certain colour
    display.blit(textsurface,(0,0)) #creates the surface of text on the screen
    
    mouse_x, mouse_y = pygame.mouse.get_pos() #constantly find the position of the mouse

    for event in pygame.event.get(): #creates the ability to quit the game
      if event.type == pygame.QUIT:
        sys.exit()
        pygame.QUIT
  
      if event.type == pygame.KEYDOWN: #shoots a bullet when spacebar is pressed
        if event.key == pygame.K_SPACE:
          player_bullet.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    #for bullet in player_bullet:
      #if bullet.x == GhostEnemy.x:
        #if bullet.y == GhostEnemy.y:
          #GhostEnemy.hit()

    keys = pygame.key.get_pressed() #constantly checks what keys are being pressed

    pygame.draw.rect(display, (255, 255, 0), (100 - display_scroll[0] ,100 - display_scroll[1],16 ,16 ))

    if keys[pygame.K_a]: #sets which direction the player character moves on a key press and created spread for bullets if the player is moving and shooting
      display_scroll[0] -= 5
      player.moving_left = True

      for bullet in player_bullet:
        bullet.x += 5

    if keys[pygame.K_d]:
      display_scroll[0] += 5
      player.moving_right = True

      for bullet in player_bullet:
        bullet.x -= 5
        
    if keys[pygame.K_w]:
      display_scroll[1] -= 5

      for bullet in player_bullet:
        bullet.y += 5
        
    if keys[pygame.K_s]:
      display_scroll[1] += 5

      for bullet in player_bullet:
        bullet.y -= 5
        
    player.main(display)

    for bullet in player_bullet:
      bullet.main(display)

    for enemy in enemies:
      enemy.main(display)

    clock.tick(60)
    pygame.display.update()

intro()