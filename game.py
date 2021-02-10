
# Authors: Wafa Salah (wss9fb) and Valee Hefner (vlh6xg)
# Code last Modified: December 2019

import pygame
import gamebox  # gamebox is the work of Luther Tychonievich;
                #                        Assistant Professor at UVA, Computer Science Department
camera = gamebox.Camera(760, 600)



# Description of the game:
                # The goal of the game is to clear all the brick found towards the top of the screen without the
                # ball exiting from the bottom of the screen. The way to prevent this ball from going below the screen
                # is by using the platform at the bottom as a landing spot for the ball. The ball, when it hits the platform
                # the left side, the right side, or top of the screen, it will bounce back; when it hits the bricks, it will
                # bounce off of the brick it touches while making it disappear. The player will have three lives per level, where
                # he/she loses a life, if the ball goes below the screen. The player will have an opportunity to win more lives with
                #the gold coins scattered throughout the bricks.


# Required Features

# 1) User Input: the bar in the bottom will be controlled by the player through the arrow keys on the keyboard.
#               This bar will be able to move left and right to save the ball from going below the screen.
# 2) Graphics/Images: bricks will be aligned at the top of the screen, a yellow bar in the bottom that will serve
#                       to keep the ball in play, and an image of a basketball that will be used to break bricks (make them disappear).
#                       A gray brick will appear in the higher levels to act as an obstacle.
# 3) Start Screen: Game Name: Brick Breaker
#                   Student Names: Wafa Salah (wss9fb) and Valee Hefner (vlh6xg)
#                   Game Instructions: Use left and Right Arrow keys to move the platform
#                                      to prevent the ball from falling off of the screen. Use the ball to break the bricks
#                                      until there are none left. You get three tries. Good Luck!





# Optional Features

# 1) Health Bar: You get three lives to clear the screen of the bricks;
#                each time the ball goes below the bottom of the screen, you lose a life

# 2) Enemy/Obstacle: An obstacle brick moving left to right and disrupting the direction of movement (levels 2 and 3)

# 3) Multiple Levels: The game will have three levels, each level gets progressively harder (ball moves faster,
#                        an obstacle comes in, one additional life is given per the level)

# 4) Save points: the player will restart the game on the level that he/she lost.


ball_velocity = -10
platform_velocity = 20
game_on = False
start_screen = True
lives = 3
timer = 0
level_2 = False
level2_game_on = False
level_3 = False
level3_game_on = False


# Drawn Things

wall_right = gamebox.from_color(760, 588, 'yellow', 0.5, 2000)
wall_left = gamebox.from_color(0, 588, 'yellow', 0.5, 2000)
platform = gamebox.from_color(380, 588, 'yellow', 200, 25)
ball = gamebox.from_image(380,300, 'basketball.image.png')
enemy_platform = gamebox.from_color(380,220, "darkgray", 100, 40)
ball.scale_by(0.125)

brick_x = 50    # the x-coordinate for where the brick will be on the screen
brick_y = 20    # the y-coordinate for where the brick will be on the screen
bricks1 = []

# Draws the bricks on the screen
while brick_y < 180:
    for int in range (0,7):
        bricks1.append(gamebox.from_color(brick_x, brick_y, "darkred", 100, 40))
        brick_x += 110
    brick_x = 50
    brick_y += 50

bricks2 = []
bricks3 = []
bricks4 = []

ball_lives = [gamebox.from_image(15,10, 'basketball.image.png'),
              gamebox.from_image(45,10, 'basketball.image.png'),
              gamebox.from_image(75,10, 'basketball.image.png'),
              gamebox.from_image(105,10, 'basketball.image.png'),
              gamebox.from_image(135,10, 'basketball.image.png'),
              gamebox.from_image(165,10, 'basketball.image.png')]

# GRAPHICS / SCENERY
def scale_balls():
    '''
    scales the ball to a smaller size
    '''

    for ball in ball_lives:
        ball.scale_by(0.1)
scale_balls()

def start():
    '''
    creates the start screen, gives instructions for the game, and displays authors' names
    '''

    camera.clear('black')
    title = gamebox.from_text(380, 100, "Brick Breaker", 100, ' red' )
    instructions = [gamebox.from_text(380, 250, " Use left and Right Arrow keys to move the platform to", 35, 'yellow'),
                    gamebox.from_text(380, 300, "prevent the ball from falling off of the screen. ", 35, 'yellow'),
                    gamebox.from_text(380, 350, "Use the ball to break the bricks until there are none left.", 35, 'yellow'),
                    gamebox.from_text(380, 400,"You get three tries. Good Luck!", 35, 'yellow'),
                    gamebox.from_text(380, 500,"Press SPACE to Start", 35, 'yellow')]
    names = gamebox.from_text(530, 570, "Wafa Salah (wss9fb) and Valee Hefner (vlh6xg)", 25, 'white' )
    camera.draw(title)
    for instruction in instructions:
        camera.draw(instruction)
    camera.draw(names)

    camera.display()

def draw():
    '''
    enables gamebox to draw the specified items
    '''
    camera.draw(platform)
    camera.draw(ball)
    camera.draw(wall_right)
    camera.draw(wall_left)
    for item in bricks1:
        camera.draw(item)



# MOVEMENTS / INTERACTION

ball.xspeed = ball_velocity
ball.yspeed = ball_velocity
def ball_movement(keys):
    '''
    controls the ball's movements and instructs what it should do when it tries to leave the vicinity of the screen/camera
    '''
    global ball, platform, lives, game_on, ball_velocity
    if game_on:
        ball.move_speed()
        if ball.bottom_touches(platform):
            ball.yspeed = ball_velocity
            ball.move_speed()
        if ball.x >= 760:
            ball.xspeed = ball_velocity
            ball.move_speed()
        if ball.x <= 0:
            ball.xspeed = -ball_velocity
            ball.move_speed()
        if ball.y <= 0:
            ball.yspeed = -ball_velocity
            ball.move_speed()
        if ball.y >= 600:
            lives -= 1
            game_on = False
            ball.x = (380)
            ball.y = (300)
            ball.yspeed = ball_velocity


def platform_movement(keys):
    '''
    gives movement for platform and the specified keys to make the platform move
    '''
    global platform_velocity
    if game_on:
        if pygame.K_RIGHT in keys:
            platform.x += platform_velocity
            platform.move_to_stop_overlapping(wall_right)

        if pygame.K_LEFT in keys:
            platform.x -=platform_velocity
            platform.move_to_stop_overlapping(wall_left)


# SCORE RULES
def brick_dissapear():
    '''
    makes the bricks disappear if the ball touches them by moving the bricks to a new list;
    when/if the current list eventually becomes empty, it moves the game to level 2
    '''

    global level_2, ball_velocity, lives, level_3, bricks2, bricks3
    if not level_2 and not level_3:
        for item in bricks1:
            if ball.touches(item):
                ball.yspeed = -ball_velocity
                ball.move_speed()
                bricks2.append(item)
                bricks1.remove(item)
    if len(bricks1) == 0 and not level2_game_on and not level_3:
        ball.x = 380
        ball.y = 300
        level_2 = True
        platform.x,y = 380, 588
        ball.x,y = 380, 300
        ball_velocity = -15
        lives = 4


#  LEVEL 2 FUNCTIONS
def level_2_function():
    '''
    allows the game to draw the specified items in the game for level 2
    '''

    global ball_velocity, lives
    camera.draw(platform)
    camera.draw(ball)
    camera.draw(wall_right)
    camera.draw(wall_left)
    for item in bricks2:
        camera.draw(item)

def brick_dissapear2():
    '''
    appends the bricks, when hit by the ball, into a new list for the third level
    and removes them from the current one so as to make them disappear;
    when/if the current list eventually becomes empty, it moves the game to level 3
    '''

    global level_2, level_3, ball_velocity, lives, level2_game_on, ball
    if level2_game_on:
        for item in bricks2:
            if ball.touches(item):
                ball.yspeed = -ball_velocity
                ball.move_speed()
                bricks3.append(item)
                bricks2.remove(item)
        if len(bricks2) == 0 and not level3_game_on:
            level_2 = False
            level2_game_on = False
            level_3 = True
            ball.x = 380
            ball.y = 300
            platform.x, y = 380, 588
            ball_velocity = -20
            lives = 5

enplaform_speed2 = 5
enemy_platform.xspeed = enplaform_speed2

def enemy_movement2():
    '''
    defines the movement of the enemy platform for level 2
    instructs the ball to bounce off enemy
    '''
    global enemy_platform, ball, enplaform_speed2
    enemy_platform.move_speed()
    if enemy_platform.touches(wall_right):
        enemy_platform.move_to_stop_overlapping(wall_right)
        enemy_platform.xspeed = -enplaform_speed2
        enemy_platform.move_speed()
    if enemy_platform.touches(wall_left):
        enemy_platform.xspeed = enplaform_speed2
        enemy_platform.move_speed()
    if ball.bottom_touches(enemy_platform):
        ball.yspeed = ball_velocity
        ball.xspeed = -ball_velocity
        ball.move_speed()
    if ball.touches(enemy_platform):
        ball.yspeed = -ball_velocity
        ball.xspeed = -ball_velocity
        ball.move_speed()

def restart_level2():
    '''
    restarts level 2 if player in level 2 and loses
    '''

    global bricks2, bricks3
    platform.x, y = 380, 558
    if len(bricks3) != 0:
        for brick in bricks3:
            bricks2.append(brick)
        bricks3 = []



# LEVEL 3 Functions

def level_3_function():
    '''
    instructs gamebox to draw the specified items for level 3
    '''

    global ball_velocity
    camera.draw(platform)
    camera.draw(ball)
    camera.draw(wall_right)
    camera.draw(wall_left)
    for item in bricks3:
        camera.draw(item)

def brick_dissapear3():
    '''
     appends the bricks, when hit by the ball, into a new list so that the camera stops drawing them;
    when/if the current list eventually becomes empty, the player wins and a message is displayes
    '''

    global ball_velocity, lives, game_on, ball
    if level3_game_on:
        for item in bricks3:
            if ball.touches(item):
                ball.yspeed = -ball_velocity
                ball.move_speed()
                bricks4.append(item)
                bricks3.remove(item)
        if len(bricks3) == 0:
            winning_text = gamebox.from_text(380, 300, "YOU WON!", 100, 'white')  # ADD MORE animation of celebration
            camera.draw(winning_text)  # Start drawing the NEXT level
            ball.x = 1000
            ball.y = 1000
            game_on = False

enplaform_speed3 = 8
enemy_platform.xspeed = enplaform_speed3

def enemy_movement3():
    '''
    defines the movement of the enemy platform for level 3
    instructs the ball to bounce off enemy
    '''

    global enemy_platform, ball, enplaform_speed3
    enemy_platform.move_speed()
    if enemy_platform.touches(wall_right):
        enemy_platform.move_to_stop_overlapping(wall_right)
        enemy_platform.xspeed = -enplaform_speed3
        enemy_platform.move_speed()
    if enemy_platform.touches(wall_left):
        enemy_platform.xspeed = enplaform_speed3
        enemy_platform.move_speed()
    if ball.bottom_touches(enemy_platform):
        ball.yspeed = ball_velocity
        ball.xspeed = -ball_velocity
        ball.move_speed()
    if ball.touches(enemy_platform):
        ball.yspeed = -ball_velocity
        ball.xspeed = -ball_velocity
        ball.move_speed()

def restart_level3():
    '''
     restarts level 3 if player in level 2 and loses
    '''
    global bricks4, bricks3, lives, platform
    lives = 5
    platform.x,y = 380,558
    if len(bricks4) != 0:
        for brick in bricks4:
            bricks3.append(brick)
        bricks4 = []



def tick(keys):
    '''
    specifies the keys to start the game, start the different levels,
    and call all the other functions to make the game run smoothly
    '''

    global platform, ball, game_on, lives, life_text, start_screen, level_2, level2_game_on, ball_velocity, level_3, level3_game_on, restart_level_2
    camera.clear('black')
    if start_screen and not pygame.K_SPACE in keys:
        start()
    else:
        start_screen = False
    if not start_screen and not level_2 and not level_3:
        draw()
        ball_movement(keys)
    if pygame.K_SPACE in keys and not game_on and not start_screen:
        game_on = True
    platform_movement(keys)
    brick_dissapear()


# LEVEL 2 THINGS #
    if level_2 and not level2_game_on:
        level2_text = [gamebox.from_text(380, 250, "LEVEL 2", 100, 'White'),
                       gamebox.from_text(380, 400, "Press SPACE to Start", 60, 'White')]
        for text in level2_text:
            camera.draw(text)

    if lives == 0 and level2_game_on and len(bricks2) != 0:
        restart_level2()
        level2_game_on = False

    if level_2 and pygame.K_SPACE in keys:
        level2_game_on = True


    if level2_game_on:
        level_2_function()
        camera.draw(enemy_platform)
        enemy_movement2()
        ball_movement(keys)
    brick_dissapear2()


# LEVEL 3 THINGS #
    if level_3 and not level3_game_on:
        #camera.clear('black')
        level3_text = [gamebox.from_text(380, 250, "LEVEL 3", 100, 'White'),
                       gamebox.from_text(380, 400, "Press SPACE to Start", 60, 'White')]
        for text in level3_text:
            camera.draw(text)

    if lives == 0 and level3_game_on and len(bricks3) != 0:
        restart_level3()
        level3_game_on = False


    if level_3 and pygame.K_SPACE in keys:
        level3_game_on = True


    if level3_game_on:
        level_3_function()
        ball_movement(keys)
        camera.draw(enemy_platform)
        enemy_movement3()
        ball_movement(keys)
    brick_dissapear3()

    if not start_screen or level2_game_on or level3_game_on:
        for i in range(lives):
            camera.draw(ball_lives[i])

    if lives == 0 and not level_2 and not level_3:
        game_over_text = gamebox.from_text(380, 300, "YOU LOST!", 100, 'pink')
        camera.draw(game_over_text)
        gamebox.pause()


    camera.display()




gamebox.timer_loop(40, tick)
