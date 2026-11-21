import pygame
import os
import random
import math
import asyncio

pygame.mixer.init()

pygame.font.init()

scrx, scry = 1534, 810
scrn = pygame.display.set_mode((scrx, scry))
pygame.display.set_caption("Rocket Shooter Game! (Points: 0)")


score = 0

fps = 60

ship_scale_x = 150
ship_scale_y = 150


barrier = 200


ship_x = (scrx / 2) - (ship_scale_x / 2)
ship_y = 650

bullet_width, bullet_height = 30, 70

ship_speed = 10

bullet_speed = 14
bullets = []

asteroids = []

bullet_hit = pygame.USEREVENT

asteroid_speed = 10
sat_speed = 12


def randfloat(min, max, decs):  # Copy this
    min2 = math.floor(min * (10 ** decs))
    max2 = math.floor(max * (10 ** decs))
    rand = (random.randint(min2, max2))
    return rand / (10 ** decs)


def create_asteroid(x, y, asteroid_width, asteroid_height):
    asteroid = pygame.Rect(x, y, asteroid_width, asteroid_height)
    asteroids.append(asteroid)


def draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size):
    scrn.blit(space_img, (0, 0))
    score_text = font.render("Score: " + str(score), 1, (255, 255, 255))
    for bullet in bullets:
        scrn.blit(bullet_fix, (bullet.x, bullet.y))
    for asteroid in asteroids:
        scrn.blit(asteroid_img, (asteroid.x, asteroid.y))
    for sat in sats:
        scrn.blit(sat_img, (sat.x, sat.y))
    scrn.blit(ship_size, (ship.x - (ship.width / 2), ship.y - (ship.height / 2)))
    scrn.blit(score_text, (scrx / 2 - (score_text.get_width() / 2), 0))
    pygame.display.update()


async def main():
    pygame.display.set_icon(pygame.image.load(os.path.join("Assets", "Rocket.png")))

    # Load all the files...
    shoot = pygame.mixer.Sound("Assets/shoot.wav")
    hit = pygame.mixer.Sound("Assets/hit.wav")
    lose = pygame.mixer.Sound(os.path.join("Assets", "lose.wav"))
    pygame.mixer.music.load(os.path.join("Assets", "music.wav"))
    pygame.mixer.music.set_volume(0.1)

    pygame.mixer.Sound.set_volume(shoot, 0.2)
    pygame.mixer.Sound.set_volume(hit, 0.1)
    pygame.mixer.Sound.set_volume(lose, 0.2)

    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont("comicsans", 80)
    big_font = pygame.font.SysFont("comicsans", 150)

    space_img = pygame.image.load(os.path.join("Assets", "space.jpg"))

    asteroid_width, asteroid_height = 160, 100
    asteroid_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "asteroid.png"))
                                          , (asteroid_width, asteroid_height))
    sat_wid, sat_hit = 150, 150
    sat_img = pygame.transform.scale((pygame.image.load(os.path.join("assets", "satelite.png"))), (sat_wid, sat_hit))

    bullet_fix = pygame.transform.rotate((pygame.transform.scale
                                          ((pygame.image.load(os.path.join("Assets", "bullets.png"))), (80, 80))), 90)

    ship_image = pygame.image.load(os.path.join("Assets", "Rocket.png"))
    ship_size = pygame.transform.scale(ship_image, (ship_scale_x, ship_scale_y))

    ###############################################

    paused = False
    max_sat_chance = 50
    sat_chance = 5
    score = 0
    asteroid_speed = 10
    max_ast_wait, last_ast, wait_decs = 4, 1, 2
    time_to_asteroid = randfloat(last_ast, max_ast_wait + last_ast, wait_decs)
    running = True
    timer = 0
    bullets_frames = []
    sats = []  # satellites list
    ship = pygame.Rect(ship_x, ship_y, 70, 30)
    draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)
    while running:
        clock = pygame.time.Clock()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(ship.x,
                                         ship.y - 50, bullet_width, bullet_height)
                    bullets.append(bullet)
                    bullets_frames.append(-1)
                    shoot.play()
                if event.key == pygame.K_p:
                    paused = True
                    pygame.mixer.music.pause()
                    pause_text = big_font.render("Paused", 1, (255, 255, 255))
                    scrn.blit(pause_text, ((scrx / 2) - (pause_text.get_width() / 2),
                                           (scry / 2) - (pause_text.get_height() / 1)))
                    pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship.x -= ship_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship.x += ship_speed

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                        pygame.mixer.music.unpause()
                        draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)
                        pause_text = big_font.render("3", 1, (255, 255, 255))
                        scrn.blit(pause_text, ((scrx / 2) - (pause_text.get_width() / 2),
                                               (scry / 2) - (pause_text.get_height() / 1)))
                        pygame.display.update()
                        await asyncio.sleep(1)
                        draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)
                        pause_text = big_font.render("2", 1, (255, 255, 255))
                        scrn.blit(pause_text, ((scrx / 2) - (pause_text.get_width() / 2),
                                               (scry / 2) - (pause_text.get_height() / 1)))
                        pygame.display.update()
                        await asyncio.sleep(1)
                        draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)
                        pause_text = big_font.render("1", 1, (255, 255, 255))
                        scrn.blit(pause_text, ((scrx / 2) - (pause_text.get_width() / 2),
                                               (scry / 2) - (pause_text.get_height() / 1)))
                        pygame.display.update()
                        await asyncio.sleep(1)

            await asyncio.sleep(1 / 60)

        if ship.x < barrier:
            ship.x += ship_speed
        if ship.x > scrx - barrier:
            ship.x -= ship_speed
        # handling bullets & asteroids & satellites
        for asteroid in asteroids:
            asteroid.y += asteroid_speed  # move all asteroids
            for bullet in bullets:
                if asteroid.colliderect(bullet):
                    if asteroid in asteroids:
                        asteroids.remove(asteroid)
                        hit.play()
                        score = score + 1
                        asteroid_speed += 1 / 3
                        sat_chance = sat_chance * 1.1
                        bullets_frames[bullets.index(bullet)] = 10
                        if sat_chance > max_sat_chance:
                            sat_chance = max_sat_chance
        for bullet in bullets:
            bullet.y -= bullet_speed  # move all bullets
            bullets_frames[bullets.index(bullet)] -= 1
            if bullets_frames[bullets.index(bullet)] == 0:
                bullets_frames.pop(bullets.index(bullet))
                bullets.remove(bullet)
        for sat in sats:
            sat.y += sat_speed
            for bullet in bullets:
                if sat.colliderect(bullet):
                    new_lose = pygame.mixer.Sound(os.path.join("assets", "satelite break.wav"))
                    new_lose.play()
                    pygame.mixer.music.stop()
                    sat_break_text = big_font.render("You broke a Satellite!", 1, (255, 255, 255))
                    draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)
                    scrn.blit(sat_break_text, ((scrx / 2) - (sat_break_text.get_width() / 2),
                                               (scry / 2) - (sat_break_text.get_height() / 2)))
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                        await asyncio.sleep(1 / 60)
        draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)

        timer += 1 / fps  # for getting time (secs) since run or gamestart

        if timer >= time_to_asteroid:
            time_to_asteroid = randfloat(last_ast, max_ast_wait + last_ast, wait_decs)
            create_asteroid(randfloat(barrier, scrx - asteroid_width - barrier, wait_decs), asteroid_height * -1, asteroid_width, asteroid_height)
            last_ast = timer
            rand = randfloat(1, 100, 5)
            if rand <= sat_chance:
                satellite = pygame.Rect(randfloat(barrier, scrx - barrier - sat_wid, 2), 0 - sat_hit - 10, sat_wid,
                                        sat_hit)
                sats.append(satellite)
        for asteroid in asteroids:
            if asteroid.colliderect(ship):
                thing = True
                pygame.mixer.music.stop()
                lose.play()
                text = big_font.render("You Lost!", 1, (255, 255, 255))
                draw(ship, bullets, asteroids, sats, score, font, space_img, asteroid_img, sat_img, bullet_fix, ship_size)
                scrn.blit(text, ((scrx / 2) - (text.get_width() / 2), (scry / 2) - (text.get_height() / 2)))
                pygame.display.update()

                while thing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            thing = False

                running = False

        pygame.display.set_caption("Rocket Shooter Game!!! (Points: " + str(score) + ")")
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
