import pygame
import time
from random import randrange, randint


def rand_blocks():
    rand = randint(1, 3)
    color_list = [(randrange(30, 256), randrange(30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]
    if rand == 1:
        block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
    elif rand == 2:
        block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(0, 10, 2) for j in range(0, 4, 1)]
    else:
        block_list = ([pygame.Rect(10 + 120 * i, 10, 100, 50) for i in range(10)] +
                     [pygame.Rect(10 + 120 * i, 10 + 70, 100, 50) for i in range(1, 9)] +
                     [pygame.Rect(10 + 120 * i, 10 + 70 * 2, 100, 50) for i in range(2, 8)] +
                     [pygame.Rect(10 + 120 * i, 10 + 70 * 3, 100, 50) for i in range(3, 7)])

    return block_list, color_list   


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def main():

    WIDTH, HEIGHT = 1200, 800
    fps = 60

    paddle_w = 330
    paddle_h = 35
    paddle_speed = 15
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

    ball_radius = 20
    ball_speed = 6
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(randrange(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1

    pygame.init()

    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    img_rand = randint(1, 5)
    img = pygame.image.load(f'photo\\fon{str(img_rand)}.jpg').convert()

    bl = rand_blocks()

    f = pygame.font.Font(None, 36)
    loser = f.render("Game Over! Wait 3 seconds...", True, (0, 180, 0))
    winner = f.render("You Won! Wait 3 seconds...", True, (0, 180, 0))

    count = 0 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.blit(img, (0, 0))

        [pygame.draw.rect(sc, bl[1][color], block) for color, block in enumerate(bl[0])]
        pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

        if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx

        if ball.centery < ball_radius:
            dy = -dy

        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)

        hit_index = ball.collidelist(bl[0])
        if hit_index != -1:
            hit_rect = bl[0].pop(hit_index)
            hit_color = bl[1].pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)

            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, hit_color, hit_rect)
            count += 1
            if count == 10:
                fps -= 15
                count = 0
            else:
                fps += 3

        pygame.display.update()
        if ball.bottom > HEIGHT:
            sc.blit(loser, (450, 350))
            pygame.display.update()
            time.sleep(3)
            main()
        elif not len(bl[0]):
            sc.blit(winner, (450, 350))
            pygame.display.update()
            time.sleep(3)
            main()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
