#---Importing all the necessary modules---
import time, pygame, random, sys, math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Tank Mayhem")

#---Sprite Class---
class block(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super(block,self).__init__()
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()      
    def position(self,x,y):
        self.rect.x = x
        self.rect.y = y      
    def load(self,picture):
        self.image = pygame.image.load(picture)
        
#---Function for trigonometry---
def trig(angle, gun_x, gun_y):
    x = gun_x + math.cos(math.radians(angle)) * line_length
    y = gun_y + math.sin(math.radians(angle)) * line_length
    return (x,y)

#---Creates some colours that will be used---
white        = (255,255,255)
black        = (0,0,0)
grey         = (140,140,140)
other_grey   = (101,101,101)
light_grey   = (191,191,191)
grass_green  = (5,138,22)
army_green   = (42,80,43)
dark_blue    = (42,39,91)
royal_blue   = (62,35,236)
blue         = (0,0,255)
light_blue   = (114,223,245)
other_blue   = (79,147,249)
brown        = (124,73,21)
light_yellow = (228,214,96)

#---Variables for the start screen---
pointer              = pygame.image.load("New Game Pointer.png").convert_alpha()
start_background     = pygame.image.load("New Game Background.png").convert_alpha()
title_y              = -60
button_y             = 640
control_button_y     = 620
mousePressed         = False
title_animation_done = False
pygame.mouse.set_visible(False)

#---Loads game background---
background = pygame.image.load("New Game Background.png").convert()

#---Creates the groups---
tank_group        = pygame.sprite.Group()
tank_P2_group     = pygame.sprite.Group()
shell_group       = pygame.sprite.Group()
shell_P2_group    = pygame.sprite.Group()
tank_gun_group    = pygame.sprite.Group()
tank_gun_P2_group = pygame.sprite.Group()
health_box_group  = pygame.sprite.Group()
speed_box_group   = pygame.sprite.Group()
invis_box_group   = pygame.sprite.Group()

#---Variables related to speed---
speed_box            = block(15,30)
speed_timer          = 0
P2_speed_timer       = 0
speed_tick           = -30
P2_speed_tick        = -30
speed_box_y          = -30
speed_bar_length     = 100
P2_speed_bar_length  = -100
speed_drop           = False
tank_hit_speed       = False
tank_P2_hit_speed    = False
reset_speed_box      = False
P2_speed_timer_start = False
speed_timer_start    = False
speed_box.load("New Game Speed Box.png")

#---Variables related to invisibility---
invis_box            = block(15,30)
invis_timer          = 0
P2_invis_timer       = 0
invis_tick           = -30
P2_invis_tick        = -30
invis_box_y          = -30
invis_bar_length     = 100
P2_invis_bar_length  = -100
invis_drop           = False
tank_hit_invis       = False
tank_P2_hit_invis    = False
reset_invis_box      = False
invis_timer_start    = False
P2_invis_timer_start = False
invis_box.load("New Game Invisibility Box.png")

#---Variables related to health---
health_box         = block(15,30)
health_box_y       = -30
health_length      = 100
P2_health_length   = -100
tank_hit_health    = False
tank_P2_hit_health = False
reset_health_box   = False
health_drop        = False
health_box.load("New Game Health Box.png")

#---Variables related to the tank---
tank          = block(75,35)
tank_x        = 5
tank_num      = 1
tank_speed    = 5
tank.load("New Game Tank1.png")

#---Variables related to the P2 tank---
tank_P2          = block(75,35)
tank_P2_x        = 700
tank_num_P2      = 1
tank_P2_speed    = 5
tank_P2.load("New Game Tank1 P2.png")

#---Variables related to the shell---
shell            = block(15,15)
shell_x          = tank_x + 15
shell_y          = 390
drop_speed       = 0.7
horizontal_speed = 6
no_repeat        = True
shell.load("New Game Tank Shell.png")

#---Variables related to the P2 shell---
shell_P2            = block(15,15)
shell_P2_x          = tank_P2_x + 5
shell_P2_y          = 390
drop_speed_P2       = 0.7
horizontal_speed_P2 = 6
no_repeat_P2        = True
shell_P2.load("New Game Tank Shell P2.png")

#---Variables related to launching---
launch_height          = 1
start_launch_height    = launch_height
launch_height_P2       = 1
start_launch_height_P2 = launch_height_P2
launch_P2              = False
launch                 = False

#---Variables related to collisions---
tank_P2_health = 10
tank_health    = 10
tank_hit       = False
tank_P2_hit    = False
explode        = False
explode_P2     = False
explosion      = pygame.image.load("New Game Explosion.png").convert_alpha()

#---Variables related to the tank gun---
start_y = 397
angle   = 0

#---Variables related to the tank P2 gun---
start_P2_y = 397
angle_P2   = 180

#---Fonts---
hit_font            = pygame.font.SysFont("calibri", 20)
game_over_font      = pygame.font.SysFont("mongolianbaiti", 50)
title_font          = pygame.font.SysFont("mongolianbaiti", 50)
title               = title_font.render("TANK MAYHEM", 1, black)
game_over           = game_over_font.render("GAME OVER", 1, black)
tank_P2_health_font = hit_font.render("HEALTH", 1, black)
tank_health_font    = hit_font.render("HEALTH", 1, black)
tank_speed_font     = hit_font.render("SPEED x2", 1, other_blue)
tank_P2_speed_font  = hit_font.render("SPEED x2", 1, other_blue)
tank_invis_font     = hit_font.render("INVISIBLE", 1, black)
tank_P2_invis_font  = hit_font.render("INVISIBLE", 1, black)

#---Other variables---
line_length  = 30
tank_win     = False
tank_P2_win  = False
restart_menu = False
spacePressed = False
enterPressed = False
control_menu = False
check        = False
done         = False
start_menu   = True

#---Variables for controls screen---
control_screen = pygame.image.load("New Game Controls Screen.png").convert_alpha()

#---Start menu loop---
while start_menu:
    if check:
        pygame.mouse.set_pos((400,300))
        check = False
    mouse_pos = pygame.mouse.get_pos()
    hover = False
    control_hover = False
    screen.blit(start_background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_menu = False
            done = True
                
    screen.blit(title, (200,title_y))

    #---Title animation---
    title_y += 20
    if title_y > 100:
        title_y = 100
        title_animation_done = True   
    if title_animation_done:
        button_y -= 20
        control_button_y -= 20
    if button_y < 450:
        button_y = 450
    if control_button_y < 300:
        control_button_y = 300

    #---Play button hover detection---
    if mouse_pos[0] > 299 and mouse_pos[0] < 492 and mouse_pos[1] > 450 and mouse_pos[1] < 535:
        hover = True
        
    if hover:
        play_button = pygame.image.load("New Game Play Button Clicked.png").convert_alpha()
        screen.blit(play_button, (300,button_y))
    else:
        play_button = pygame.image.load("New Game Play Button Not Clicked.png").convert_alpha()
        screen.blit(play_button, (300,button_y))

    #---Control button hover detection---
    if mouse_pos[0] > 299 and mouse_pos[0] < 492 and mouse_pos[1] > 299 and mouse_pos[1] < 382:
        control_hover = True

    if control_hover:
        control_button = pygame.image.load("New Game Instructions Button Clicked.png").convert_alpha() 
        screen.blit(control_button, (300, control_button_y))
    else:
        control_button = pygame.image.load("New Game Instructions Button Not Clicked.png").convert_alpha()
        screen.blit(control_button, (300, control_button_y))
        
    if hover:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False
        if mousePressed:
            start_menu = False
    if control_hover:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False
        if mousePressed:
            control_menu = True
            check = True
            
    while control_menu:
        back_hover = False
        mousePressed = False
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(control_screen, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                control_menu = False
                start_menu = False
                done = True
                
        if mouse_pos[0] > 299 and mouse_pos[0] < 492 and mouse_pos[1] > 450 and mouse_pos[1] < 535:
            back_hover = True
            
        if back_hover:
            back_button = pygame.image.load("New Game Back Button Clicked.png").convert_alpha()
        else:
            back_button = pygame.image.load("New Game Back Button Not Clicked.png").convert_alpha()
        screen.blit(back_button, (300,450))

        if back_hover:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
            if mousePressed:
                control_menu = False
                title_y              = -60
                button_y             = 640
                control_button_y     = 620
                mousePressed         = False
                title_animation_done = False
        
        screen.blit(pointer, mouse_pos)
        pygame.display.flip()
        clock.tick(60)
            
    screen.blit(pointer, mouse_pos)
    pygame.display.flip()
    clock.tick(60)

#---Main Game Loop---
tick = 0
while not done:
    tick += 1
    
    mousePressed = False
    
    tank.position(tank_x,390)
    tank_P2.position(tank_P2_x, 390)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            spacePressed = True
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            spacePressed = False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            enterPressed = True
        if event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            enterPressed = False

    #---Controls the tanks movement---
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        tank_x -= tank_speed      
        #---Tank animation---
        if tick % 7 == 0:
            tick = 0
            tank.load("New Game Tank" + str(tank_num) + ".png")
            if tank_num == 1:
                tank_num = 2
            else:
                tank_num = 1
            
    if pressed[pygame.K_d]:
        tank_x += tank_speed        
        #---Tank animation---
        if tick % 7 == 0:
            tick = 0
            tank.load("New Game Tank" + str(tank_num) + ".png")
            if tank_num == 1:
                tank_num = 2
            else:
                tank_num = 1

    if pressed[pygame.K_LEFT]:
        tank_P2_x -= tank_P2_speed
        #---Tank animation---
        if tick % 7 == 0:
            tick = 0
            tank_P2.load("New Game Tank" + str(tank_num_P2) + " P2.png")
            if tank_num_P2 == 1:
                tank_num_P2 = 2
            else:
                tank_num_P2 = 1
    if pressed[pygame.K_RIGHT]:
        tank_P2_x += tank_P2_speed
        #---Tank animation---
        if tick % 7 == 0:
            tick = 0
            tank_P2.load("New Game Tank" + str(tank_num_P2) + " P2.png")
            if tank_num_P2 == 1:
                tank_num_P2 = 2
            else:
                tank_num_P2 = 1

    #---Left and right boundaries of the tanks---
    if tank_x < 5:
        tank_x = 5
    if tank_x > 330:
        tank_x = 330

    if tank_P2_x < 420:
        tank_P2_x = 420
    if tank_P2_x > 730:
        tank_P2_x = 730

    #---Controls the height of the shot---
    if pressed[pygame.K_w] and not launch:
        launch_height += 0.5
        angle -= 1.55
    if pressed[pygame.K_s] and not launch:
        launch_height -= 0.5
        angle += 1.55

    if pressed[pygame.K_UP] and not launch_P2:
        launch_height_P2 += 0.5
        angle_P2 += 1.55
    if pressed[pygame.K_DOWN] and not launch_P2:
        launch_height_P2 -= 0.5
        angle_P2 -= 1.55

        
    #---Boundaries of the angle of the gun---
    if angle > -10.85 :
        angle = -10.85
    if angle < -72.85:
        angle = -72.85

    if angle_P2 > 242:
        angle_P2 = 242
    if angle_P2 < 180:
        angle_P2 = 180

    #---Limit of the launching height---
    if launch_height > 20:
        launch_height = 20
    if launch_height_P2 > 20:
        launch_height_P2 = 20
              
    #---Resets the launch height---
    if launch_height < 1 and not launch:
        launch_height = 1
    if launch_height_P2 < 1 and not launch_P2:
        launch_height_P2 = 1

    #---Controls the shooting function of the tank
    if spacePressed and no_repeat:
        start_launch_height = launch_height
        tank_now            = tank_x + 10
        spacePressed        = False
        no_repeat           = False
        launch              = True

    if enterPressed and no_repeat_P2:
        start_launch_height_P2 = launch_height_P2
        tank_now_P2            = tank_P2_x + 10
        no_repeat_P2           = False
        launch_P2              = True
        enterPressed           = False

    #---Collision Detections---

    #---Tank to bullet collisions---
        
    if pygame.sprite.groupcollide(tank_group, shell_P2_group, False, True):
        tank_hit = True
        
    if pygame.sprite.groupcollide(tank_P2_group, shell_group, False, True):
        tank_P2_hit = True
        
    #---Tank to health box collisions---
        
    if pygame.sprite.groupcollide(health_box_group, shell_group, True, True):
        tank_hit_health = True        
    if pygame.sprite.groupcollide(health_box_group, shell_P2_group, True, True):
        tank_P2_hit_health = True

    if pygame.sprite.groupcollide(tank_group, health_box_group, False, True):
        tank_hit_health = True
    if pygame.sprite.groupcollide(tank_P2_group, health_box_group, False, True):
        tank_P2_hit_health = True
        
    #---Tank to speed box collisions---
        
    if pygame.sprite.groupcollide(speed_box_group, shell_group, True, True):
        tank_hit_speed = True        
    if pygame.sprite.groupcollide(speed_box_group, shell_P2_group, True, True):
        tank_P2_hit_speed = True

    if pygame.sprite.groupcollide(tank_group, speed_box_group, False, True):
        tank_hit_speed = True
    if pygame.sprite.groupcollide(tank_P2_group, speed_box_group, False, True):
        tank_P2_hit_speed = True

    explode = False
    explode_P2 = False

    #---Tank to invisibility box collisions---
    if pygame.sprite.groupcollide(invis_box_group, shell_group, True, True):
        tank_hit_invis = True        
    if pygame.sprite.groupcollide(invis_box_group, shell_P2_group, True, True):
        tank_P2_hit_invis = True

    if pygame.sprite.groupcollide(tank_group, invis_box_group, False, True):
        tank_hit_invis = True
    if pygame.sprite.groupcollide(tank_P2_group, invis_box_group, False, True):
        tank_P2_hit_invis = True

    #---Tank to tank collisions---
    if tank_hit:
        tank_health     -= 1
        health_length   -= 10
        shell_P2_y       = 390
        shell_P2_x       = tank_P2_x + 10
        launch_height_P2 = start_launch_height_P2
        explode          = True
        no_repeat_P2     = True
        launch_P2        = False
        tank_hit         = False
        
    if tank_P2_hit:       
        tank_P2_health   -= 1
        P2_health_length += 10
        shell_y           = 390
        shell_x           = tank_x + 10
        launch_height     = start_launch_height
        no_repeat         = True
        explode_P2        = True
        launch            = False
        tank_P2_hit       = False

    #---When the shell hits the ground, all variables associated with shooting reset---
    if shell_y > 410:
        shell_y       = 390
        shell_x       = tank_x + 10
        launch_height = start_launch_height
        no_repeat     = True
        launch        = False
        
    if shell_P2_y > 410:
        shell_P2_y       = 390
        shell_P2_x       = tank_P2_x + 10
        launch_height_P2 = start_launch_height_P2
        no_repeat_P2     = True
        launch_P2        = False

    #---Resets health score when it reaches zero---
    if tank_P2_health == 0:
        tank_win = True
    if tank_health == 0:
        tank_P2_win = True

    #---Health Increases when health box hit---
    if tank_hit_health:
        tank_health     += 1
        health_length   += 10
        tank_hit_health  = False
        reset_health_box = True
        
    if tank_P2_hit_health:
        tank_P2_health    += 1
        P2_health_length  -= 10
        tank_P2_hit_health = False
        reset_health_box   = True

    if tank_health > 10:
        tank_health   = 10
        health_length = 100
    if tank_P2_health > 10:
        tank_P2_health   = 10
        P2_health_length = 100

    #---Speed increases when speed box hit---
    if tank_hit_speed:
        speed_timer       = 0
        speed_bar_length  = 100
        tank_speed        = 10
        tank_hit_speed    = False
        reset_speed_box   = True
        speed_timer_start = True
        
    if tank_P2_hit_speed:
        P2_speed_timer       = 0
        tank_P2_speed        = 10
        P2_speed_bar_length  = -100
        tank_P2_hit_speed    = False
        reset_speed_box      = True
        P2_speed_timer_start = True

    #---Invisibility when invisibility box hit---
    if tank_hit_invis:
        invis_timer = 0
        invis_bar_length = 100
        tank_hit_invis = False
        reset_invis_box = True
        invis_timer_start = True

    if tank_P2_hit_invis:
        P2_invis_timer = 0
        P2_invis_bar_length = -100
        tank_P2_hit_invis = False
        reset_invis_box = True
        P2_invis_timer_start = True

    if invis_timer_start:
        invis_timer += 1

    if P2_invis_timer_start:
        P2_invis_timer += 1

    if invis_timer == 1200:
        invis_timer = 0
        invis_timer_start = False

    if P2_invis_timer == 1200:
        P2_invis_timer = 0
        P2_invis_timer_start = False
        
    if speed_timer_start:
        speed_timer += 1
        
    if P2_speed_timer_start:
        P2_speed_timer += 1

    if speed_timer == 1200:
        speed_timer       = 0
        tank_speed        = 5
        speed_timer_start = False
     
    if P2_speed_timer == 1200:
        P2_speed_timer       = 0
        tank_P2_speed        = 5
        P2_speed_timer_start = False

    #---Resets health box---
    if reset_health_box:
        health_box_y     = -30
        health_drop      = False
        reset_health_box = False

    #---Resets speed box---
    if reset_speed_box:
        speed_box_y     = -30
        speed_drop      = False
        reset_speed_box = False

    #---Resets invisibility box---
    if reset_invis_box:
        invis_box_y     = -30
        invis_drop      = False
        reset_invis_box = False

    #---Controls when health box drops---
    if not health_drop:
        health_drop_num = random.randint(1,5000)
        health_box_x    = random.randint(120,680)
        if health_drop_num == 1:
            health_drop = True
    if health_drop:
        health_box_y += 0.5
    if health_box_y > 390:
        health_box_y = 390

    #---Controls when speed box drops---                                                         
    if not speed_drop and not (invis_drop or invis_timer_start or P2_invis_timer_start):
        speed_drop_num = random.randint(1,5000)
        speed_box_x    = random.randint(120,660)
        if speed_drop_num == 1:
            speed_drop = True
    if speed_drop:
        speed_box_y += 0.5
    if speed_box_y > 390:
        speed_box_y = 390

    #---Controls when invisibility box drops---
    if not invis_drop and not (speed_drop or speed_timer_start or P2_speed_timer_start):
        invis_drop_num = random.randint(1,5000)
        invis_box_x    = random.randint(120,660)
        if invis_drop_num == 1:
            invis_drop = True
    if invis_drop:
        invis_box_y += 0.5
    if invis_box_y > 390:
        invis_box_y = 390
       
    #---Drawing everything---
    screen.blit(background, (0,0))

    pygame.draw.polygon(screen, brown, ((125,91),(106,110),(0,110),(0,0),(125,0)), 2)
    pygame.draw.polygon(screen, light_yellow, ((123,91),(104,108),(2,108),(2,2),(123,2)))

    pygame.draw.polygon(screen, brown, ((675,91),(694,110),(798,110),(798,0), (675,0)), 2)
    pygame.draw.polygon(screen, light_yellow, ((696,108),(677,91),(677,2),(796,2),(796,108)))

    screen.blit(tank_health_font, (8,10))
    screen.blit(tank_P2_health_font, (732,10))

    pygame.draw.rect(screen, black, (8,28,104,14))
    pygame.draw.rect(screen, grey, (10,30,100,10))
    pygame.draw.rect(screen, grass_green, (10,30,health_length,10))

    pygame.draw.rect(screen, black, (792, 28, -104, 14))
    pygame.draw.rect(screen, grey, (790,30,-100,10))
    pygame.draw.rect(screen, royal_blue, (790,30,P2_health_length,10))

    if speed_timer_start:
        speed_tick += 1
        screen.blit(tank_speed_font, (9,50))
        pygame.draw.rect(screen, black, (8,68,104,14))
        pygame.draw.rect(screen, grey, (10,70,100,10))
        if speed_tick > 0:
            pygame.draw.rect(screen, light_blue, (10,70,speed_bar_length,10))
        else:
            pygame.draw.rect(screen, other_blue, (10,70,speed_bar_length,10))
        if speed_tick == 30:
            speed_tick = -30
        speed_bar_length -= 0.0833
        
    if P2_speed_timer_start:
        P2_speed_tick += 1
        screen.blit(tank_P2_speed_font, (708, 50))
        pygame.draw.rect(screen, black, (792,68,-104,14))
        pygame.draw.rect(screen, grey, (790,70,-100,10))
        if P2_speed_tick > 0:
            pygame.draw.rect(screen, light_blue, (790, 70, P2_speed_bar_length,10))
        else:
            pygame.draw.rect(screen, other_blue, (790, 70, P2_speed_bar_length,10))
        if P2_speed_tick == 30:
            P2_speed_tick = -30
        P2_speed_bar_length += 0.0833

    if invis_timer_start:
        invis_tick += 1
        screen.blit(tank_invis_font, (9,50))
        pygame.draw.rect(screen, black, (8,68,104,14))
        pygame.draw.rect(screen, grey, (10,70,100,10))
        if invis_tick > 0:
            pygame.draw.rect(screen, light_grey, (10,70,invis_bar_length,10))
        else:
            pygame.draw.rect(screen, other_grey, (10,70,invis_bar_length,10))
        if invis_tick == 30:
            invis_tick = -30
        invis_bar_length -= 0.0833

    if P2_invis_timer_start:
        P2_invis_tick += 1
        screen.blit(tank_P2_invis_font, (715,50))
        pygame.draw.rect(screen, black, (792,68,-104,14))
        pygame.draw.rect(screen, grey, (790,70,-100,10))
        if P2_invis_tick > 0:
            pygame.draw.rect(screen, light_grey, (790,70,P2_invis_bar_length,10))
        else:
            pygame.draw.rect(screen, other_grey, (790,70,P2_invis_bar_length,10))
        if P2_invis_tick == 30:
            P2_invis_tick = -30
        P2_invis_bar_length += 0.0833
    
    #---Ending the game---
    if tank_win:
        tank_win_font = game_over_font.render("WINNER", 1, black)
        tank_P2_lose_font = game_over_font.render("LOSER", 1, black)
        screen.blit(tank_win_font, (50,200))
        screen.blit(tank_P2_lose_font, (500,200))
        restart_menu = True

    if tank_P2_win and not tank_win:
        tank_lose_font = game_over_font.render("LOSER", 1, black)
        tank_P2_win_font = game_over_font.render("WINNER", 1, black)
        screen.blit(tank_lose_font, (50,200))
        screen.blit(tank_P2_win_font, (500,200))
        restart_menu = True
        
    #---Drawing the shell---
    if launch:
        shell.position(tank_now + 30, shell_y)
        tank_now += horizontal_speed
        shell_y -= launch_height
        launch_height -= drop_speed
        
        shell_group.add(shell)
        shell_group.draw(screen)
        
    if launch_P2:
        shell_P2.position(tank_now_P2 + 3, shell_P2_y)
        tank_now_P2 -= horizontal_speed_P2
        shell_P2_y -= launch_height_P2
        launch_height_P2 -= drop_speed_P2
        
        shell_P2_group.add(shell_P2)
        shell_P2_group.draw(screen)

    #---Draws the tank---
    if not invis_timer_start:
        tank_group.add(tank)
        tank_group.draw(screen)
    if not P2_invis_timer_start:
        tank_P2_group.add(tank_P2)
        tank_P2_group.draw(screen)

    #---Draws the tank's gun---    
    start_x = tank_x + 35
    start_P2_x = tank_P2_x + 23

    line_start_1 = (start_x, start_y)
    line_start_2 = (start_x, start_y - 5)

    line_P2_start_1 = (start_P2_x, start_P2_y)
    line_P2_start_2 = (start_P2_x, start_P2_y - 5)

    line_end_1 = trig(angle, start_x, start_y)
    line_end_2 = trig(angle + 10, start_x, start_y)

    line_P2_end_1 = trig(angle_P2, start_P2_x, start_P2_y)
    line_P2_end_2 = trig(angle_P2 + 10, start_P2_x, start_P2_y)
    
    if not invis_timer_start:
        pygame.draw.polygon(screen, army_green, (line_start_1, line_start_2, line_end_1, line_end_2))
    if not P2_invis_timer_start:
        pygame.draw.polygon(screen, dark_blue, (line_P2_start_2, line_P2_start_1, line_P2_end_1, line_P2_end_2))


    #---Draws the health box---
    if health_drop:
        health_box.position(health_box_x, health_box_y)
        health_box_group.add(health_box)
        health_box_group.draw(screen)

    #---Draws the speed box---
    if speed_drop:
        speed_box.position(speed_box_x, speed_box_y)
        speed_box_group.add(speed_box)
        speed_box_group.draw(screen)

    #---Draws the invisibility box---
    if invis_drop:
        invis_box.position(invis_box_x, invis_box_y)
        invis_box_group.add(invis_box)
        invis_box_group.draw(screen)
    
    #---Draws the explosions---
    if explode:
        screen.blit(explosion, (tank_x - 10, 370))
    if explode_P2:
        screen.blit(explosion, (tank_P2_x - 10, 370))

    #---Removes the shells from the groups as a safety precaution---
    if not launch:
        for i in shell_group:
            shell_group.remove(i)
    if not launch_P2:
        for i in shell_P2_group:
            shell_P2_group.remove(i)

    pygame.display.flip()
    clock.tick(60)

    #---Pauses the game for two seconds so the players can see who won and who lost---
    if restart_menu:
        time.sleep(2)

    #---Restart menu---
    while restart_menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart_menu = False
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
                
        restart_clicked = False
        screen.blit(background, (0,0))

        screen.blit(game_over, (250,250))
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > 299 and mouse_pos[0] < 492 and mouse_pos[1] > 450 and mouse_pos[1] < 535:
            restart_clicked = True
            
        if not restart_clicked:
            restart_button = pygame.image.load("New Game Restart Button Not Clicked.png").convert_alpha()
        else:
            restart_button = pygame.image.load("New Game Restart Button Clicked.png").convert_alpha()
            
        screen.blit(restart_button, (300,450))
        screen.blit(pointer, mouse_pos)
            
        if mousePressed and restart_clicked:
            restart_menu = False

            #---Loads game background---
            background = pygame.image.load("New Game Background.png").convert()

            #---Removes everything from the groups---
            for i in tank_group:
                tank_group.remove(i)                
            for i in tank_P2_group:
                tank_P2_group.remove(i)
            for i in shell_group:
                shell_group.remove(i)
            for i in shell_P2_group:
                shell_P2_group.remove(i)
            for i in invis_box_group:
                invis_box_group.remove(i)
            for i in health_box_group:
                health_box_group.remove(i)
            for i in speed_box_group:
                speed_box_group.remove(i)

            #---Resets all the variables when the game restarts---
            tank = block(75,35)
            tank_x = 5
            tank.load("New Game Tank.png")
            health_length = 100

            tank_P2 = block(75,35)
            tank_P2_x = 700
            tank_P2.load("New Game Tank P2.png")
            P2_health_length = -100
            
            start_y = 397

            start_P2_y = 397

            shell = block(15,15)
            shell_x = tank_x + 15
            shell_y = 390
            shell.load("New Game Tank Shell.png")

            shell_P2 = block(15,15)
            shell_P2_x = tank_P2_x + 5
            shell_P2_y = 390
            shell_P2.load("New Game Tank Shell P2.png")

            launch_height = 1
            launch = False
            start_launch_height = launch_height

            launch_height_P2 = 1
            start_launch_height_P2 = launch_height_P2
            launch_P2 = False

            angle = 0
            angle_P2 = 180

            spacePressed = False

            no_repeat = True
            no_repeat_P2 = True

            drop_speed = 0.7
            drop_speed_P2 = 0.7

            enterPressed = False

            tank_hit = False
            tank_P2_hit = False
            tank_P2_health = 10
            tank_health = 10

            tank_win = False
            tank_P2_win = False

            speed_box = block(15,30)
            speed_box.load("New Game Speed Box.png")
            speed_drop = False
            speed_box_y = -30
            tank_hit_speed = False
            tank_P2_hit_speed = False
            reset_speed_box = False
            speed_timer = 0
            speed_timer_start = False
            P2_speed_timer = 0
            P2_speed_timer_start = False
            speed_bar_length = 100
            P2_speed_bar_length = -100
            speed_tick = -30
            P2_speed_tick = -30
            tank_speed = 5
            tank_P2_speed = 5

            health_box = block(15,30)
            health_box.load("New Game Health Box.png")
            health_drop = False
            health_box_y = -30
            tank_hit_health = False
            tank_P2_hit_health = False
            reset_health_box = False

            invis_box = block(15,30)
            invis_box.load("New Game Invisibility Box.png")
            invis_timer = 0
            P2_invis_timer = 0
            invis_tick = -30
            P2_invis_tick = -30
            invis_box_y = -30
            invis_bar_length = 100
            P2_invis_bar_length = -100
            invis_drop = False
            tank_hit_invis = False
            tank_P2_hit_invis = False
            reset_invis_box = False
            invis_timer_start = False
            P2_invis_timer_start = False           
                    
        pygame.display.flip()
        clock.tick(60)
        
pygame.display.quit()
sys.exit()
 
