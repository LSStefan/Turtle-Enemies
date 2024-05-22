import sys

import pygame
import random
from pygame import mixer
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 1366,695
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Turtle Enemies")
background = pygame.transform.scale(pygame.image.load(".\Assets\Background.png"),(1366,695))
ball = pygame.transform.scale(pygame.image.load(".\Assets\Ball.png"),(150,150))
pos = pygame.Rect(600,250,150,150)  #ball position
enemy_pos = pygame.Rect(0,330,130,70)
frog = pygame.transform.scale(pygame.image.load(".\Assets\Enemy.png"),(130,70))
frog2 = pygame.transform.scale(pygame.image.load(".\Assets\Enemy2.png"),(130,70))
enemy_states = [frog,frog2] #for walking animation
enemys = []
lines = [100,330,550]
up = False
down = False
middle = True
state = 0
SCORE_FONT = pygame.font.SysFont('comicsans',16)
FONT = pygame.font.SysFont('calibri',200)
FONT2 = pygame.font.SysFont('calibri',80)
score = 0
broscoi = pygame.transform.scale(pygame.image.load('.\Assets\Broscoi.jpg'),(WIDTH,HEIGHT))
frog_vel = 10
lives  = 2
music = mixer.Sound(".\Audio\The Sky.mp3")
music.set_volume(0.4)
music.play()
lifeup_sound = mixer.Sound(".\Audio\Lifeup.wav")
hit_sounds = []
for index in range(0,14):
    hit_sounds.append(mixer.Sound(f".\Audio\Turtle ({index + 1}).wav"))
lose_sound = mixer.Sound(".\Audio\Lose.wav")

def draw():
    global score
    global state
    global frog_vel,lives
    #print the two states of the frog for the animation
    if state == 0:
        state = 1
    else:
        state = 0
    screen.blit(background, (0, 0))
    screen.blit(ball, (pos.x,pos.y))
    for enemy_pos in enemys:   #print each enemy
        screen.blit(enemy_states[state], (enemy_pos.x, enemy_pos.y))
    Score_Text = SCORE_FONT.render('SCORE:' + str(score), 100, (255, 255, 255))
    Frog_Speed = SCORE_FONT.render('FROG SPEED:' + str(frog_vel), 100, (255, 255, 255))
    Lives_Text = SCORE_FONT.render('LIVES:' + str(lives), 100, (255, 255, 255))
    screen.blit(Score_Text,(50,10))
    screen.blit(Frog_Speed,(200,10))
    screen.blit(Lives_Text, (400, 10))
    pygame.display.update()
    pygame.time.delay(30)



def move(keys_pressed):
    global up,down,middle
    if keys_pressed[pygame.K_a] and pos.x - 20  >= 500:
        pos.x -= 12
    if keys_pressed[pygame.K_d] and pos.x + 20 + 150 <= WIDTH:
        pos.x += 12

def collision(enemys,pos):
    global score,frog_vel,hit_sounds,lives
    for enemy_pos in enemys:
        if enemy_pos.colliderect(pos) and pos.x > enemy_pos.x: #to be able to only hit a frog from right
            enemys.remove(enemy_pos)
            score += 1
            sound = random.choice(hit_sounds)
            sound.play()
            if score % 10 == 0:
                frog_vel += 2
            if score % 100 == 0:
                lives += 1
                text = FONT2.render("+1 lives", 100, (255, 255, 255))
                screen.blit(text,(text.get_rect(center = screen.get_rect().center)))
                pygame.display.update()
                lifeup_sound.play()
                pygame.time.delay(500)




def restart_game():
    global run, score, frog_vel, lives,enemys
    run = True
    score = 0
    frog_vel = 10
    enemys.clear()
    lives = 2
    music.play()
    main()


def end_screen(score):
    run = False
    music.stop()
    lose_sound.play()
    while 1:
        screen.fill((118, 7, 216)) #purple background
        text = FONT.render("SCORE:" + str(score), 100, (0, 0, 0))
        screen.blit(text, text.get_rect(center=screen.get_rect().center))
        restart = FONT2.render(("Press r to restart"),100,(0,0,0))
        screen.blit(restart,(restart.get_rect(center = screen.get_rect().center).x,400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN: #restart game
                if event.key == pygame.K_r:
                    restart_game()

def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
        screen.fill((118, 7, 216))
        text = FONT2.render("Press esc again to continue",100,(255,255,255))
        screen.blit(text,(text.get_rect(center = screen.get_rect().center)))
        pygame.display.update()

def main():
    global up,middle,down,score,frog_vel,lives
    current_time,set_time = 0,0
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #moving ball between the 3 lines
                if event.key == pygame.K_w and middle == True:
                    pos.y = 20
                    up = True
                    middle = False
                    down = False
                if event.key == pygame.K_s and middle == True:
                    pos.y = 470
                    up = False
                    middle = False
                    down = True
                if event.key == pygame.K_w and down == True:
                    pos.y = 250
                    up = False
                    middle = True
                    down = False
                if event.key == pygame.K_s and up == True:
                    pos.y = 250
                    up = False
                    middle = True
                    down = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause()
        keys_pressed = pygame.key.get_pressed()
        move(keys_pressed)
        current_time = pygame.time.get_ticks()
        if current_time - set_time > 500:   #create new frog
            set_time = current_time
            enemy_pos = pygame.Rect(-10,0,130,70)
            line = random.choice(lines)
            enemy_pos.y = line
            enemys.append(enemy_pos)
        #increment on x axis for every frog
        for enemy_pos in enemys:
            enemy_pos.x += frog_vel
            if enemy_pos.x >= WIDTH - 100:  #checking for enemys passing over the border
                enemys.remove(enemy_pos)
                lives -= 1
                text = FONT2.render("-1 lives", 100, (255, 255, 255))
                screen.blit(text, (text.get_rect(center=screen.get_rect().center)))
                pygame.display.update()
                pygame.time.delay(300)

        collision(enemys,pos)
        draw()
        if lives == 0:
            run = False
            end_screen(score)

main()
