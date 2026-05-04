import pygame                          # import pygame library for graphics, events and input
from pygame.locals import *            # import constants like QUIT, KEYDOWN, MOUSEBUTTONDOWN
from tools import draw_shape, flood_fill  # import external drawing functions

pygame.init()                          # initialize pygame modules (graphics, input, etc.)

# WINDOW SETTINGS
WIDTH, HEIGHT = 900, 600              # window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
pygame.display.set_caption("Paint PRO")  # set window title

clock = pygame.time.Clock()           # controls FPS (frame rate)

# DRAWING SURFACE
canvas = pygame.Surface((WIDTH, HEIGHT))  # separate surface for drawing
canvas.fill((255,255,255))                # fill with white background

# COLOR PALETTE
palette = [
    (255,0,0),      # red
    (0,255,0),      # green
    (0,0,255),      # blue
    (0,0,0),        # black
    (255,255,0)     # yellow
]

selected_color = palette[2]            # default color = blue

# TOOLS LIST
tools = [
    "brush","line","rect","circle","square",
    "rtriangle","etriangle","rhombus",
    "eraser","fill","text"
]

selected_tool = "brush"                # default tool

# BRUSH SETTINGS
brush_sizes = [2,5,10]                 # available brush thickness
brush_index = 1                        # default index (medium)
brush_size = brush_sizes[brush_index]  # current size

# UI BUTTON AREAS
tool_rects = [pygame.Rect(10,70+i*50,40,40) for i in range(len(tools))]
# left panel tools

palette_rects = [pygame.Rect(100+i*50,10,40,40) for i in range(len(palette))]
# top panel colors

size_rects = [
    pygame.Rect(400,10,40,40),
    pygame.Rect(450,10,40,40),
    pygame.Rect(500,10,40,40)
]
# brush size buttons

# DRAW STATE VARIABLES
drawing = False                        # True when mouse is dragging
start_pos = None                       # start position for shapes
last_pos = None                        # previous mouse position (for smooth lines)

# TEXT TOOL VARIABLES
font = pygame.font.SysFont(None, 42)   # text size increased to 42

typing = False                         # True when user is typing text
text_input = ""                        # typed text buffer
text_pos = (0,0)                       # where text will appear


while True:                            # main game loop (runs forever)

    for event in pygame.event.get():   # handle all events

        # WINDOW CLOSE
        if event.type == QUIT:
            pygame.quit()
            exit()

        # KEYBOARD INPUT
        if event.type == KEYDOWN:

            # change brush size using 1,2,3 keys
            if event.key == K_1:
                brush_index = 0
            elif event.key == K_2:
                brush_index = 1
            elif event.key == K_3:
                brush_index = 2

            brush_size = brush_sizes[brush_index]  # apply new size

            # SAVE IMAGE (Ctrl + S)
            if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                import datetime
                name = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, name)

            # TEXT TYPING MODE
            if typing:
                if event.key == K_RETURN:
                    # finalize text and draw it
                    text_surface = font.render(text_input, True, selected_color)
                    canvas.blit(text_surface, text_pos)
                    typing = False
                    text_input = ""

                elif event.key == K_ESCAPE:
                    # cancel typing
                    typing = False
                    text_input = ""

                elif event.key == K_BACKSPACE:
                    # delete last character
                    text_input = text_input[:-1]

                else:
                    # add typed character
                    text_input += event.unicode

        # MOUSE CLICK
        if event.type == MOUSEBUTTONDOWN:

            clicked_ui = False   # IMPORTANT: track if user clicked UI instead of canvas

            # COLOR SELECTION
            for i,r in enumerate(palette_rects):
                if r.collidepoint(event.pos):
                    selected_color = palette[i]
                    clicked_ui = True

            # TOOL SELECTION
            for i,r in enumerate(tool_rects):
                if r.collidepoint(event.pos):
                    selected_tool = tools[i]
                    clicked_ui = True

            # BRUSH SIZE SELECTION
            for i,r in enumerate(size_rects):
                if r.collidepoint(event.pos):
                    brush_index = i
                    brush_size = brush_sizes[i]
                    clicked_ui = True

            # STOP DRAWING if clicked UI
            if clicked_ui:
                drawing = False
                start_pos = None
                last_pos = None

            # DRAW ONLY INSIDE CANVAS (NOT UI)
            if not clicked_ui and event.pos[1] > 60 and event.pos[0] > 60:

                if selected_tool == "fill":
                    # flood fill replaces area color
                    flood_fill(canvas, event.pos, selected_color)

                elif selected_tool == "text":
                    # start typing mode
                    typing = True
                    text_input = ""
                    text_pos = event.pos

                else:
                    # start drawing (dragging)
                    drawing = True
                    start_pos = event.pos
                    last_pos = None   # prevents instant dot

        # MOUSE RELEASE
        if event.type == MOUSEBUTTONUP:

            # draw shapes ONLY if we were actually drawing
            if drawing:
                if selected_tool not in ["brush","eraser","fill","text"]:
                    draw_shape(canvas, selected_tool, selected_color, start_pos, event.pos, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    # CONTINUOUS DRAWING (runs every frame)
    if drawing and pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()   # current mouse position

        if selected_tool == "brush":
            # draw smooth line from last position
            if last_pos is not None:
                pygame.draw.line(canvas, selected_color, last_pos, mouse_pos, brush_size)
            last_pos = mouse_pos

        elif selected_tool == "eraser":
            # erase using white color
            if last_pos is not None:
                pygame.draw.line(canvas, (255,255,255), last_pos, mouse_pos, brush_size*2)
            last_pos = mouse_pos

    # DRAW CANVAS ON SCREEN
    screen.blit(canvas,(0,0))

    # SHAPE PREVIEW (temporary while dragging)
    if drawing and selected_tool not in ["brush","eraser","fill","text"]:
        temp = screen.copy()
        mouse_pos = pygame.mouse.get_pos()
        draw_shape(temp, selected_tool, selected_color, start_pos, mouse_pos, brush_size)
        screen.blit(temp,(0,0))

    # TEXT PREVIEW
    if typing:
        temp_text = font.render(text_input, True, selected_color)
        screen.blit(temp_text, text_pos)

    # DRAW UI PANELS
    pygame.draw.rect(screen,(200,200,200),(0,0,WIDTH,60))   # top panel
    pygame.draw.rect(screen,(220,220,220),(0,60,60,HEIGHT)) # left panel

    # DRAW COLOR PALETTE
    for i,r in enumerate(palette_rects):
        pygame.draw.rect(screen,palette[i],r)

        # highlight selected color
        if palette[i] == selected_color:
            pygame.draw.rect(screen,(255,255,255),r,3)

    # DRAW BRUSH SIZE BUTTONS
    for i,r in enumerate(size_rects):
        pygame.draw.rect(screen,(180,180,180),r)

        if i == brush_index:
            pygame.draw.rect(screen,(255,255,255),r,3)

        cx,cy = r.center
        pygame.draw.circle(screen,(0,0,0),(cx,cy),brush_sizes[i])

    # DRAW TOOL ICONS
    for i,r in enumerate(tool_rects):
        pygame.draw.rect(screen,(180,180,180),r)

        if tools[i] == selected_tool:
            pygame.draw.rect(screen,(255,255,255),r,3)

        cx,cy = r.center

        # each tool has its own icon
        if tools[i] == "brush":
            pygame.draw.circle(screen,(0,0,0),(cx,cy),5)

        elif tools[i] == "line":
            pygame.draw.line(screen,(0,0,0),(cx-10,cy-10),(cx+10,cy+10),2)

        elif tools[i] == "rect":
            pygame.draw.rect(screen,(0,0,0),(cx-12,cy-8,24,16),2)

        elif tools[i] == "circle":
            pygame.draw.circle(screen,(0,0,0),(cx,cy),10,2)

        elif tools[i] == "square":
            pygame.draw.rect(screen,(0,0,0),(cx-10,cy-10,20,20),2)

        elif tools[i] == "rtriangle":
            pygame.draw.polygon(screen,(0,0,0),[(cx-10,cy+10),(cx+10,cy+10),(cx-10,cy-10)],2)

        elif tools[i] == "etriangle":
            pygame.draw.polygon(screen,(0,0,0),[(cx,cy-10),(cx-10,cy+10),(cx+10,cy+10)],2)

        elif tools[i] == "rhombus":
            pygame.draw.polygon(screen,(0,0,0),[(cx,cy-10),(cx+10,cy),(cx,cy+10),(cx-10,cy)],2)

        elif tools[i] == "eraser":
            pygame.draw.rect(screen,(255,255,255),(cx-10,cy-10,20,20))

        elif tools[i] == "fill":
            pygame.draw.circle(screen,(0,0,0),(cx,cy),6,2)

        elif tools[i] == "text":
            txt = font.render("T", True, (0,0,0))
            screen.blit(txt,(cx-5,cy-8))

    pygame.display.flip()   # update screen
    clock.tick(60)          # limit FPS to 60