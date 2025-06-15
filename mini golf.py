
import pygame
import math
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Golf - Smart Scoring")

clock = pygame.time.Clock()

# Colors
GRASS_GREEN = (34, 139, 34)
GREEN = (50, 205, 50)
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLORS = [(255, 255, 255), (255, 200, 0), (0, 191, 255), (255, 165, 0), (148, 0, 211)]

# Game variables
ball_pos = [100, 300]
ball_radius = 12
ball_color = random.choice(BALL_COLORS)
ball_velocity = [0, 0]

hole_pos = [700, 300]
hole_radius = 18

dragging = False
power_line_start = None

score = 0
shots_taken = 0
total_shots = 0

particles = []

def draw_grass():
    screen.fill(GRASS_GREEN)
    for i in range(0, WIDTH, 40):
        for j in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, DARK_GREEN, (i, j, 20, 20), border_radius=4)

def draw_course_border():
    pygame.draw.rect(screen, GREEN, (50, 50, 700, 500), border_radius=20)

def draw_hole():
    pygame.draw.circle(screen, BLACK, hole_pos, hole_radius)
    pygame.draw.circle(screen, DARK_GREEN, hole_pos, hole_radius - 5)
    pygame.draw.line(screen, WHITE, (hole_pos[0], hole_pos[1] - 40), (hole_pos[0], hole_pos[1]), 2)
    wave_offset = math.sin(pygame.time.get_ticks() / 200) * 5
    pygame.draw.polygon(screen, (255, 0, 0), [
        (hole_pos[0], hole_pos[1] - 40),
        (hole_pos[0] + 20 + wave_offset, hole_pos[1] - 35),
        (hole_pos[0], hole_pos[1] - 30)
    ])

def draw_ball():
    pygame.draw.ellipse(screen, (0, 0, 0), (ball_pos[0] - 10, ball_pos[1] + 8, 20, 5))
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

def draw_power_line():
    if dragging and power_line_start:
        pygame.draw.line(screen, (255, 0, 0), power_line_start, pygame.mouse.get_pos(), 4)

def update_ball():
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]
    ball_velocity[0] *= 0.98
    ball_velocity[1] *= 0.98

    if abs(ball_velocity[0]) < 0.1:
        ball_velocity[0] = 0
    if abs(ball_velocity[1]) < 0.1:
        ball_velocity[1] = 0

    if ball_pos[0] - ball_radius < 50 or ball_pos[0] + ball_radius > 750:
        ball_velocity[0] *= -1
        ball_pos[0] = max(50 + ball_radius, min(750 - ball_radius, ball_pos[0]))

    if ball_pos[1] - ball_radius < 50 or ball_pos[1] + ball_radius > 550:
        ball_velocity[1] *= -1
        ball_pos[1] = max(50 + ball_radius, min(550 - ball_radius, ball_pos[1]))

def check_hole():
    dist = math.hypot(ball_pos[0] - hole_pos[0], ball_pos[1] - hole_pos[1])
    return dist < hole_radius - 4

def create_particles(pos):
    for _ in range(30):
        particles.append([
            list(pos),
            [random.uniform(-2, 2), random.uniform(-2, 2)],
            random.randint(4, 6),
            random.choice(BALL_COLORS)
        ])

def update_particles():
    for particle in particles[:]:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.2
        if particle[2] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle[3], (int(particle[0][0]), int(particle[0][1])), int(particle[2]))

def show_text(text, x, y, size=30, color=WHITE):
    font = pygame.font.SysFont("Comic Sans MS", size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Main game loop
running = True
while running:
    clock.tick(60)
    draw_grass()
    draw_course_border()
    draw_hole()
    draw_ball()
    draw_power_line()
    update_particles()
    draw_particles()

    show_text(f"Score: {score}", 30, 20)
    show_text(f"Shots: {shots_taken}", 650, 20)
    show_text("🎯 Click & drag from the ball to aim!", 200, 550, 24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            dist = math.hypot(mouse_pos[0] - ball_pos[0], mouse_pos[1] - ball_pos[1])
            if dist < ball_radius + 5:
                dragging = True
                power_line_start = ball_pos[:]

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            end_pos = pygame.mouse.get_pos()
            dx = power_line_start[0] - end_pos[0]
            dy = power_line_start[1] - end_pos[1]
            ball_velocity = [dx / 10, dy / 10]
            power_line_start = None
            shots_taken += 1
            total_shots += 1

    update_ball()

    if check_hole():
        create_particles(hole_pos)
        pygame.display.flip()
        pygame.time.wait(500)

        points = max(1, 10 - (shots_taken - 1))
        score += points

        # Reset
        shots_taken = 0
        ball_pos = [100, random.randint(150, 450)]
        ball_velocity = [0, 0]
        hole_pos = [random.randint(600, 750), random.randint(150, 450)]
        ball_color = random.choice(BALL_COLORS)

    pygame.display.flip()

pygame.quit()
sys.exit()



