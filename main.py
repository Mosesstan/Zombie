import pygame
import os
from pygame import mixer

# initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((707,500))
game_on = True
station = True
# game name
pygame.display.set_caption("Zombie hunter")
red = (244, 187, 103)
# game texts
font = pygame.font.Font(None, 30)
game_font = pygame.font.Font(None, 50)
game_surf = game_font.render("Zombie Hunter", False, red)
game_rect = game_surf.get_rect(center=(350, 50))
lose_surf = game_font.render(" you lose press ' r ' to restart", False, red)
lose_rect = game_surf.get_rect(center=(250, 300))
# game background
background = pygame.image.load(os.path.join("images", "bgg.png"))
# background music
mixer.music.load(os.path.join("sounds", "bg.mp3"))
mixer.music.play(-1)
# icon
G_icon = pygame.image.load(os.path.join("images", "icon.png"))
pygame.display.set_icon(G_icon)

# game player
player = pygame.image.load(os.path.join("images", "idle.png")).convert_alpha()
# animating player movement
right_player = [pygame.image.load(os.path.join("Run", "r1.png")),
                pygame.image.load(os.path.join("Run", "r2.png")),
                pygame.image.load(os.path.join("Run", "r3.png")),
                pygame.image.load(os.path.join("Run", "r4.png")),
                pygame.image.load(os.path.join("Run", "r5.png")),
                pygame.image.load(os.path.join("Run", "r6.png"))]
left_player = [pygame.transform.flip(pygame.image.load(os.path.join("Run", "r1.png")), True, False),
               pygame.transform.flip(pygame.image.load(os.path.join("Run", "r2.png")),  True, False),
               pygame.transform.flip(pygame.image.load(os.path.join("Run", "r3.png")),  True, False),
               pygame.transform.flip(pygame.image.load(os.path.join("Run", "r4.png")),  True, False),
               pygame.transform.flip(pygame.image.load(os.path.join("Run", "r5.png")),  True, False),
               pygame.transform.flip(pygame.image.load(os.path.join("Run", "r6.png")),  True, False)]
player_rect = player.get_rect(midbottom=(100, 420))
player_gravity = 0
# game enemy
enemy = pygame.image.load(os.path.join("images", "zombie_left.png")).convert_alpha()
# animating enemy
left_enemy = [pygame.image.load(os.path.join("enemy", "L1E.png")),
              pygame.image.load(os.path.join("enemy", "L2E.png")),
              pygame.image.load(os.path.join("enemy", "L3E.png")),
              pygame.image.load(os.path.join("enemy", "L4E.png")),
              pygame.image.load(os.path.join("enemy", "L5E.png")),
              pygame.image.load(os.path.join("enemy", "L6E.png"))]
enemy_rect = enemy.get_rect(bottomright=(720, 420))
# grave
grave = pygame.image.load(os.path.join("images", "grave.png"))
grave_rect = grave.get_rect(midbottom=(677, 420))
# health
player_health = 100
enemy_health = 100
# bullet and shooting
bullet = pygame.image.load(os.path.join("images", "bullet.png")).convert_alpha()
bullet_rect = bullet.get_rect(center=(100, 405))
bullet_move = 0
shoot = False
face_left = False
face_right = False
step_index = 0

# player function


def draw_player():
    global step_index
    if step_index >= 24:
        step_index = 0
    if face_right:
        screen.blit(right_player[step_index//4], player_rect)
        step_index += 1
    elif face_left:
        screen.blit(left_player[step_index//4], player_rect)
        step_index += 1
    else:
        screen.blit(player, player_rect)


def draw_enemy():
    global step_index, enemy_dead, enemy_health
    if step_index >= 12:
        step_index = 0
    if not enemy_dead:
        # enemy movement
        screen.blit(left_enemy[step_index//2], enemy_rect)
        step_index += 1
        enemy_rect.x -= 3
        if enemy_rect.right <= 0:
            enemy_rect.left = 707
    else:
        enemy_rect.x = 707
        enemy_health = 100
        if enemy_health == 100:
            enemy_dead = False


def shooting():
    global shoot
    shoot = True
    screen.blit(bullet, bullet_rect)


# points

points = 0
# checking if enemy is dead or alive
enemy_dead = False

# kills
kills = 0
width = 707
i = 0
cloud = pygame.image.load(os.path.join("images", "bgg.png"))
# game loop
run = True
while run:
    if game_on:
        # adding looping background
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(cloud, (i, 0))
        screen.blit(cloud, (width + i, 0))

        i -= 1
        if i == -width:
            screen.blit(cloud, (width + i, 0))
            i = 0
        # end of background loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if game_on:

            # keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 420:
                    player_gravity = -25
                    player = pygame.image.load(os.path.join("images", "jump.png")).convert_alpha()
                if event.key == pygame.K_SPACE and bullet_rect.bottom == 405 and player_rect.bottom == 420:
                    bullet_move = -25

                # player movement
                if event.key == pygame.K_RIGHT:
                    player_rect.x += 15
                    bullet_rect.x += 15
                    face_left = False
                    face_right = True
                    station = False
                if event.key == pygame.K_LEFT:
                    player_rect.x -= 15
                    bullet_rect.x -= 15
                    face_left = True
                    face_right = False
                    station = False

                    # bullet

                if event.key == pygame.K_f:
                    shooting()
                    bullet_sound = mixer.Sound(os.path.join("sounds", "gunshot.wav"))
                    bullet_sound.play()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_on = True
            player_health = 100
            enemy_health = 100
            player_rect.x = 100
            bullet_rect.right = player_rect.x + 20
            # making sure when the game restarts the time continues from 0
            start_time = int(pygame.time.get_ticks() / 1000)
            kills = 0
            points = 0

    # game on
    if game_on:
        # bullet
        screen.blit(bullet, bullet_rect)
        draw_enemy()
        screen.blit(grave, grave_rect)
        draw_player()

        # bullet movement and direction
        bullet_move += 1
        bullet_rect.y += bullet_move
        if bullet_rect.bottom >= 405:
            bullet_rect.bottom = 405
        # bullet boundary
        if bullet_rect.left <= 0:
            bullet_rect.left = player_rect.x + 20
        if bullet_rect.right >= 665:
            bullet_rect.right = player_rect.x + 20
        # bullet moving
        if shoot and face_right:
            bullet_rect.x += 8
            if bullet_rect.left >= enemy_rect.x:
                bullet_rect.right = player_rect.x + 20
                shoot = False

        if shoot and face_left:
            bullet_rect.x -= 8
            if bullet_rect.left <= 0:
                bullet_rect.right = player_rect.x + 20
                shoot = False

        # player jumping
        player_gravity += 1
        player_rect.y += player_gravity
        # creating boundary for player
        if player_rect.bottom >= 420:
            player_rect.bottom = 420
        if player_rect.right >= 665:
            player_rect.right = 665
        elif player_rect.left <= 0:
            player_rect.left = 0
        # player and enemy collision
        if enemy_rect.colliderect(player_rect):
            player_health -= 1
            # collide_sound = mixer.Sound(os.path.join("sounds", "collide.mp3"))
            # collide_sound.play()
            if player_health <= 0:
                game_on = False
            # bullet and enemy collision
        if enemy_rect.colliderect(bullet_rect):
            enemy_health -= 2
            points += 1
            bullet_rect.right = player_rect.x + 20
            if enemy_health <= 0:
                kills += 1
                enemy_dead = True

    else:
        screen.fill("Black")
        screen.blit(lose_surf, lose_rect)
        screen.blit(score_text, score_text_rect)
       # station = True

    if station:
        enemy_rect.x = 720
        # pygame.draw.rect(screen, "White", game_rect)
        screen.blit(game_surf, game_rect)
        # instruction
        instruct = game_font.render("1. Press 'space bar' to jump ", False, "white")
        instruct_rect = instruct.get_rect(center=(350, 200))
        instruct2 = game_font.render("2. Press 'f key' to shoot ", False, "white")
        instruct_rect2 = instruct2.get_rect(center=(350, 250))
        instruct3 = game_font.render("3. Avoid collision with the zombie ", False, "white")
        instruct_rect3 = instruct3.get_rect(center=(350, 290))
        screen.blit(instruct, instruct_rect)
        screen.blit(instruct2, instruct_rect2)
        screen.blit(instruct3, instruct_rect3)
    if not station:
        # header bg
        pygame.draw.rect(screen, (136, 0, 27, 200), (0, 0, 707, 50))
        # drawing player health
        pygame.draw.rect(screen, "Red", (10, 30, 100, 5))
        pygame.draw.rect(screen, "Green", (10, 30, player_health, 5))
        # enemy health
        pygame.draw.rect(screen, "Red", (600, 30, 100, 5))
        pygame.draw.rect(screen, "Green", (600, 30, enemy_health, 5))

        # score_text
        total_score = points + kills
        score_text = game_font.render(f' Your score is : {total_score}', False, red)
        score_text_rect = score_text.get_rect(center=(350, 400))
        # kills text
        kills_text = font.render(f' kills:   {kills}', False, "white")
        kills_text_rect = kills_text.get_rect(center=(450, 20))
        screen.blit(kills_text, kills_text_rect)
        # points text
        points_text = font.render(f' points:   {points}', False, "white")
        points_text_rect = points_text.get_rect(center=(220, 20))
        screen.blit(points_text, points_text_rect)

        # player health text
        player_health_text = font.render(str("my live"), False, "white")
        player_health_text_rect = player_health_text.get_rect(center=(48, 15))
        screen.blit(player_health_text, player_health_text_rect)

    pygame.display.update()
    clock.tick(60)
