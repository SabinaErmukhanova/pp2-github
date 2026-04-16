import pygame
import os
import sys

def run_player():
    # Initialize pygame and mixer for music
    pygame.init()
    pygame.mixer.init()

    # Window settings
    WIDTH = 900
    HEIGHT = 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    # Frame rate controller
    timer = pygame.time.Clock()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 100, 255)
    GREEN = (0, 180, 0)
    RED = (220, 0, 0)

    # Fonts
    title_font = pygame.font.SysFont("Arial", 36)
    text_font = pygame.font.SysFont("Arial", 28)
    small_font = pygame.font.SysFont("Arial", 22)

    # Folder with music
    music_folder = os.path.join("music", "sample_tracks")

    # Playlist
    playlist = []

    # Read all wav and mp3 files from folder
    if os.path.exists(music_folder):
        for file_name in os.listdir(music_folder):
            if file_name.endswith(".wav") or file_name.endswith(".mp3"):
                playlist.append(os.path.join(music_folder, file_name))

    # Sort list so files stay in fixed order
    playlist.sort()

    # Current track index
    current_index = 0

    # Flags
    playing = False
    music_loaded = False

    # Load first track if available
    if len(playlist) > 0:
        pygame.mixer.music.load(playlist[current_index])
        music_loaded = True

    # Function to load current track
    def load_current_track():
        nonlocal music_loaded
        if len(playlist) > 0:
            pygame.mixer.music.load(playlist[current_index])
            music_loaded = True
        else:
            music_loaded = False

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Q = quit
                if event.key == pygame.K_q:
                    running = False

                # P = play
                elif event.key == pygame.K_p:
                    if music_loaded:
                        pygame.mixer.music.play()
                        playing = True

                # S = stop
                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    playing = False

                # N = next track
                elif event.key == pygame.K_n:
                    if len(playlist) > 0:
                        current_index = (current_index + 1) % len(playlist)
                        load_current_track()
                        pygame.mixer.music.play()
                        playing = True

                # B = previous track
                elif event.key == pygame.K_b:
                    if len(playlist) > 0:
                        current_index = (current_index - 1) % len(playlist)
                        load_current_track()
                        pygame.mixer.music.play()
                        playing = True

        # Fill background
        screen.fill(WHITE)

        # Title
        title_text = title_font.render("Music Player with Keyboard Controller", True, BLACK)
        screen.blit(title_text, (120, 30))

        # Current track info
        if len(playlist) > 0:
            current_track_name = os.path.basename(playlist[current_index])
        else:
            current_track_name = "No tracks found"

        track_text = text_font.render(f"Current track: {current_track_name}", True, BLUE)
        screen.blit(track_text, (80, 120))

        # Player status
        if playing:
            status_text = text_font.render("Status: Playing", True, GREEN)
        else:
            status_text = text_font.render("Status: Stopped", True, RED)
        screen.blit(status_text, (80, 180))

        # Current playlist position
        if len(playlist) > 0:
            position_text = text_font.render(
                f"Track position: {current_index + 1}/{len(playlist)}",
                True,
                BLACK
            )
        else:
            position_text = text_font.render("Track position: 0/0", True, BLACK)

        screen.blit(position_text, (80, 240))

        # Controls
        controls_title = text_font.render("Controls:", True, BLACK)
        screen.blit(controls_title, (80, 320))

        c1 = small_font.render("P = Play", True, BLACK)
        c2 = small_font.render("S = Stop", True, BLACK)
        c3 = small_font.render("N = Next track", True, BLACK)
        c4 = small_font.render("B = Previous track", True, BLACK)
        c5 = small_font.render("Q = Quit", True, BLACK)

        screen.blit(c1, (100, 360))
        screen.blit(c2, (100, 390))
        screen.blit(c3, (250, 360))
        screen.blit(c4, (250, 390))
        screen.blit(c5, (480, 360))

        # Note about folder
        note_text = small_font.render(
            "Put .wav or .mp3 files inside music/sample_tracks",
            True,
            BLACK
        )
        screen.blit(note_text, (80, 440))

        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()