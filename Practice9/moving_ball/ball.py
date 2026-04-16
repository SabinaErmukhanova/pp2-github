import pygame
import sys

def run_ball_game():
    # Initialize pygame
    pygame.init()

    # Screen size
    WIDTH = 800
    HEIGHT = 600

    # Create game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")

    # Control frame rate
    timer = pygame.time.Clock()

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Ball settings
    ball_radius = 25
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    move_step = 20

    # Font
    font = pygame.font.SysFont("Arial", 28)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                running = False

            # React only when a key is pressed
            if event.type == pygame.KEYDOWN:
                # Move left
                if event.key == pygame.K_LEFT:
                    # Check if new position stays inside the screen
                    if ball_x - move_step - ball_radius >= 0:
                        ball_x = ball_x - move_step

                # Move right
                elif event.key == pygame.K_RIGHT:
                    if ball_x + move_step + ball_radius <= WIDTH:
                        ball_x = ball_x + move_step

                # Move up
                elif event.key == pygame.K_UP:
                    if ball_y - move_step - ball_radius >= 0:
                        ball_y = ball_y - move_step

                # Move down
                elif event.key == pygame.K_DOWN:
                    if ball_y + move_step + ball_radius <= HEIGHT:
                        ball_y = ball_y + move_step

        # Fill background with white color
        screen.fill(WHITE)

        # Draw the red ball
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        # Show instructions
        text = font.render("Use arrow keys to move the ball", True, BLACK)
        screen.blit(text, (200, 30))

        # Update window
        pygame.display.flip()

        # Smooth frame rate
        timer.tick(60)

    pygame.quit()
    sys.exit()