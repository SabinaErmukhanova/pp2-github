import pygame
import sys
import os
from datetime import datetime

def blit_rotate_pivot(surface, image, center_pos, angle):
    rotated_image = pygame.transform.rotate(image, -angle)
    rotated_rect = rotated_image.get_rect(center=center_pos)
    surface.blit(rotated_image, rotated_rect)

def run_clock():
    import math
    pygame.init()

    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    timer = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    clock_radius = 180

    image_path = os.path.join("images", "mickey_hand.png")

    if os.path.exists(image_path):
        hand_image = pygame.image.load(image_path).convert_alpha()
        minute_hand = pygame.transform.scale(hand_image, (200, 300))
        second_hand = pygame.transform.scale(hand_image, (140, 240))
    else:
        minute_hand = None
        second_hand = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        pygame.draw.circle(screen, BLACK, (center_x, center_y), clock_radius, 3)
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x = center_x + math.cos(angle) * 160
            y = center_y + math.sin(angle) * 160
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 6)
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 7)

        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = minutes * 6
        second_angle = seconds * 6

        if minute_hand is not None and second_hand is not None:
            blit_rotate_pivot(screen, minute_hand, (center_x, center_y), minute_angle)
            blit_rotate_pivot(screen, second_hand, (center_x, center_y), second_angle)
        else:
            import math

            minute_length = 120
            second_length = 150

            minute_radians = math.radians(minute_angle - 90)
            second_radians = math.radians(second_angle - 90)

            minute_end_x = center_x + math.cos(minute_radians) * minute_length
            minute_end_y = center_y + math.sin(minute_radians) * minute_length

            second_end_x = center_x + math.cos(second_radians) * second_length
            second_end_y = center_y + math.sin(second_radians) * second_length

            pygame.draw.line(screen, (0, 0, 255), (center_x, center_y), (minute_end_x, minute_end_y), 6)
            pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (second_end_x, second_end_y), 3)

        font = pygame.font.SysFont("Arial", 40)
        time_text = font.render(f"{minutes:02}:{seconds:02}", True, BLACK)
        screen.blit(time_text, (center_x - 60, center_y + 220))

        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()