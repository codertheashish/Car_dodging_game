import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dodging Game")

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Car properties
car_width = 50
car_height = 80
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 6

# Obstacle list (3 cars at a time)
obstacles = []
obs_width = 50
obs_height = 80
obs_speed = 5

for _ in range(3):
    x = random.randint(0, WIDTH - obs_width)
    y = random.randint(-600, -100)
    obstacles.append([x, y])

# Score
score = 0

def game_over_screen():
    while True:
        screen.fill(BLACK)
        over_text = font.render("GAME OVER!", True, RED)
        score_text = font.render(f"Score: {score}", True, YELLOW)
        retry_text = font.render("Press R to Restart", True, WHITE)
        exit_text = font.render("Press ESC to Exit", True, WHITE)

        screen.blit(over_text, (170, 200))
        screen.blit(score_text, (190, 250))
        screen.blit(retry_text, (150, 310))
        screen.blit(exit_text, (155, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move player car
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
        car_x += car_speed

    # Move obstacles
    for obs in obstacles:
        obs[1] += obs_speed

        # Respawn if goes off screen
        if obs[1] > HEIGHT:
            obs[0] = random.randint(0, WIDTH - obs_width)
            obs[1] = random.randint(-300, -100)
            score += 1

            # AUTO SPEED INCREASE ✅
            if score % 5 == 0:
                obs_speed += 1

        # Collision check
        if (car_x < obs[0] + obs_width and
            car_x + car_width > obs[0] and
            car_y < obs[1] + obs_height and
            car_y + car_height > obs[1]):
            game_over_screen()
            # Reset game
            car_x = WIDTH // 2 - car_width // 2
            obstacles = []
            for _ in range(3):
                x = random.randint(0, WIDTH - obs_width)
                y = random.randint(-600, -100)
                obstacles.append([x, y])
            score = 0
            obs_speed = 5

    # Draw everything
    screen.fill(BLUE)

    pygame.draw.rect(screen, YELLOW, (car_x, car_y, car_width, car_height))

    for obs in obstacles:
        pygame.draw.rect(screen, RED, (obs[0], obs[1], obs_width, obs_height))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
