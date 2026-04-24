import pygame          # library for graphics, windows, drawing, etc.
import sys             # used to properly close the program
import os              # used to work with file paths
from datetime import datetime   # to get current system time


# Function to rotate an image and draw it on screen
def blit_rotate_pivot(surface, image, center_pos, angle):
    # Rotate image by given angle (negative for correct direction)
    rotated_image = pygame.transform.rotate(image, -angle)

    # Get rectangle of rotated image and place its CENTER at center_pos
    rotated_rect = rotated_image.get_rect(center=center_pos)

    # Draw (blit) rotated image onto screen
    surface.blit(rotated_image, rotated_rect)


def run_clock():
    import math  # math functions like sin, cos, radians

    pygame.init()  # initialize pygame

    # Window size
    WIDTH = 800
    HEIGHT = 600

    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")

    # Controls FPS (frames per second)
    timer = pygame.time.Clock()

    # Colors (RGB)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Center of the clock
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Radius of clock circle
    clock_radius = 180

    # Path to image file (hand)
    image_path = os.path.join("images", "mickey_hand.png")

    # Check if image exists
    if os.path.exists(image_path):
        # Load image with transparency
        hand_image = pygame.image.load(image_path).convert_alpha()

        # Resize image for minute hand (bigger)
        minute_hand = pygame.transform.scale(hand_image, (200, 300))

        # Resize image for second hand (smaller)
        second_hand = pygame.transform.scale(hand_image, (140, 240))
    else:
        # If image is missing → fallback to simple lines
        minute_hand = None
        second_hand = None

    # Main loop (runs until window is closed)
    running = True
    while running:

        # Handle events (like closing window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background with white
        screen.fill(WHITE)

        # Draw outer clock circle
        pygame.draw.circle(screen, BLACK, (center_x, center_y), clock_radius, 3)

        # Draw 12 dots (hours positions)
        for i in range(12):
            # Convert angle to radians
            angle = math.radians(i * 30 - 90)

            # Calculate x, y position of each dot
            x = center_x + math.cos(angle) * 160
            y = center_y + math.sin(angle) * 160

            # Draw dot
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 6)

        # Draw center dot of clock
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 7)

        # Get current system time
        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        # Convert time to angles
        # 360° / 60 = 6° per unit
        minute_angle = minutes * 6
        second_angle = seconds * 6

        # If images exist → use them
        if minute_hand is not None and second_hand is not None:

            # Draw rotated minute hand
            blit_rotate_pivot(screen, minute_hand, (center_x, center_y), minute_angle)

            # Draw rotated second hand
            blit_rotate_pivot(screen, second_hand, (center_x, center_y), second_angle)

        else:
            # Fallback: draw simple lines

            minute_length = 120
            second_length = 150

            # Convert angles to radians
            minute_radians = math.radians(minute_angle - 90)
            second_radians = math.radians(second_angle - 90)

            # Calculate end point of minute hand
            minute_end_x = center_x + math.cos(minute_radians) * minute_length
            minute_end_y = center_y + math.sin(minute_radians) * minute_length

            # Calculate end point of second hand
            second_end_x = center_x + math.cos(second_radians) * second_length
            second_end_y = center_y + math.sin(second_radians) * second_length

            # Draw minute hand (blue)
            pygame.draw.line(
                screen,
                (0, 0, 255),
                (center_x, center_y),
                (minute_end_x, minute_end_y),
                6
            )

            # Draw second hand (red)
            pygame.draw.line(
                screen,
                (255, 0, 0),
                (center_x, center_y),
                (second_end_x, second_end_y),
                3
            )

        # Create font object
        font = pygame.font.SysFont("Arial", 40)

        # Render digital time text
        time_text = font.render(f"{minutes:02}:{seconds:02}", True, BLACK)

        # Draw text under clock
        screen.blit(time_text, (center_x - 60, center_y + 220))

        # Update display
        pygame.display.flip()

        # Limit to 60 FPS
        timer.tick(60)

    # Quit pygame safely
    pygame.quit()
    sys.exit()