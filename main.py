import pygame
import os
pygame.font.init()

HEIGHT = 550
WIDTH = 900

BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('sansserif', 40)
WIN_FONT = pygame.font.SysFont('sansserif', 100)

SPEED = 15
PEW_SPEED = 20
MAX_BULLETS = 7
#SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
space = pygame.image.load(os.path.join('Assets', 'space.png'))
space = pygame.transform.scale(space, (WIDTH, HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

global red_health
global yellow_health

pygame.display.set_caption("POGGERSSSSSSSSSS!!!!!!!!!!! >:D") #before main func -> has to pop up b4 window appears

def redraw_ships(red, yellow, rbullet, ybullet, red_health, yellow_health):
    WIN.blit(space, (0, 0))
   # WIN.fill((200, 12, 12))
    WIN.blit(redship, (red.x, red.y))
    WIN.blit(yelship, (yellow.x, yellow.y))
    pygame.draw.rect(WIN, (0, 0, 0), BORDER)

    for bullet in rbullet:
        pygame.draw.rect(WIN, (255, 0, 0), bullet)
    for bullet in ybullet:
        pygame.draw.rect(WIN, (255, 255, 0), bullet)

    red_health_text = HEALTH_FONT.render("Health " + str(red_health), 1, (0, 255, 0))
    yellow_health_text = HEALTH_FONT.render("Health " + str(yellow_health), 1, (0, 255, 0))
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width(), 10))
    WIN.blit(yellow_health_text, (WIDTH-yellow_health_text.get_width() - 500, 10))

    #if game_over == False:
    pygame.display.update()

def y_ship_movement (keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y > SPEED:
        yellow.y -= SPEED
    if keys_pressed[pygame.K_s] and yellow.y + SPEED + yellow.height < HEIGHT:
        yellow.y += SPEED
    if keys_pressed[pygame.K_a] and yellow.x > SPEED:
        yellow.x -= SPEED
    if keys_pressed[pygame.K_d] and yellow.x + SPEED + yellow.width < BORDER.x:
        yellow.x += SPEED

def r_ship_movement (keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y > SPEED:  
        red.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and red.y + SPEED + red.height < HEIGHT:
        red.y += SPEED
    if keys_pressed[pygame.K_LEFT] and red.x - SPEED > BORDER.x:
        red.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and red.x + SPEED + red.width < WIDTH:
        red.x += SPEED

def handle_bullets(ybullet, rbullet, yellow, red):
    for bullet in ybullet:
        bullet.x += PEW_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            ybullet.remove(bullet)
        elif bullet.x > WIDTH:
            ybullet.remove(bullet)

    for bullet in rbullet:
        bullet.x -= PEW_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            rbullet.remove(bullet)
        elif bullet.x < 0:
            rbullet.remove(bullet)

def game_reset():
    red_health = 1
    yellow_health = 1
    #game_over = False

def main():
    pygame.init()
    game_reset()
    clock = pygame.time.Clock()
    run = True #initializing
    
    while run: #stuff happening while this is true
        clock.tick(FPS) #internal system time interval
#        print(pygame.event.get())
        for event in pygame.event.get(): #indefinite loop until condition is reached (event type is quit)
            if event.type == pygame.QUIT: #quit is event that occurs
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c and len(ybullet) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    ybullet.append(bullet)

                if event.key == pygame.K_l and len(rbullet) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    rbullet.append(bullet)

                if event.key == pygame.K_r:
                    game_reset()

            if event.type == RED_HIT:
                global red_health 
                red_health -= 1 
            if event.type == YELLOW_HIT:
                global yellow_health
                yellow_health -= 1

            if red_health < 1:
                print("Game Over!! Yellow wins!!")
                #game_over = True
                yellow_win_text = WIN_FONT.render("YELLOW WINS!!!!", 1, (255, 255, 0))
     
                WIN.blit(yellow_win_text, (WIDTH//2, HEIGHT//2))
                pygame.display.update()
                #run = False

            elif yellow_health < 1:
                print("Game over!! Red wins!!")
                game_over = True
                red_win_text = WIN_FONT.render("RED WINS!!", 1, (255, 0, 0))
                WIN.blit(red_win_text, (WIDTH//2, HEIGHT//2))
                pygame.display.update()
                #run = False

        keys_pressed = pygame.key.get_pressed()
        y_ship_movement(keys_pressed, yellow)
        r_ship_movement(keys_pressed, red)

        handle_bullets(ybullet, rbullet, yellow, red)

        global red_health
        global yellow_health
        if red_health > 0 and yellow_health > 0:
            redraw_ships(red, yellow, rbullet, ybullet, red_health, yellow_health)
 
    pygame.quit()

redship = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
redship = pygame.transform.scale(redship, (55,40))
redship = pygame.transform.rotate(redship, 90)

yelship = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yelship = pygame.transform.scale(yelship, (55,40))
yelship = pygame.transform.rotate (yelship, 270)

red = pygame.Rect(800, 100, 50, 50)
yellow = pygame.Rect(100, 100, 50, 50)
rbullet = []
ybullet = []

FPS = 60

if __name__ == "__main__":
    
    main() #calls the main func