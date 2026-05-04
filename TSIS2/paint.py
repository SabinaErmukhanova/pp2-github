import pygame                          # import pygame library for graphics, events and input
from pygame.locals import *            # import constants like QUIT, KEYDOWN, MOUSEBUTTONDOWN
from tools import draw_shape, flood_fill  # import functions from tools.py

pygame.init()                          # initialize all pygame modules

WIDTH, HEIGHT = 900, 600              # set window width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # create main window
pygame.display.set_caption("Paint PRO")  # set window title

clock = pygame.time.Clock()           # create clock to control FPS

canvas = pygame.Surface((WIDTH, HEIGHT))  # create separate drawing surface
canvas.fill((255,255,255))                # fill canvas with white background

palette = [                             # list of available colors
    (255,0,0),                          # red
    (0,255,0),                          # green
    (0,0,255),                          # blue
    (0,0,0),                            # black
    (255,255,0)                         # yellow
]

selected_color = palette[2]            # default selected color is blue

tools = [                              # list of drawing tools
    "brush","line","rect","circle","square",
    "rtriangle","etriangle","rhombus",
    "eraser","fill","text"
]

selected_tool = "brush"                # default selected tool

brush_sizes = [2,5,10]                 # available brush sizes
brush_index = 1                        # index of current brush size
brush_size = brush_sizes[brush_index]  # current brush thickness

tool_rects = [pygame.Rect(10,70+i*50,40,40) for i in range(len(tools))]
# create rectangles for tool buttons on left panel

palette_rects = [pygame.Rect(100+i*50,10,40,40) for i in range(len(palette))]
# create rectangles for color palette buttons

size_rects = [                         # rectangles for brush size buttons
    pygame.Rect(400,10,40,40),
    pygame.Rect(450,10,40,40),
    pygame.Rect(500,10,40,40)
]

drawing = False                        # indicates whether user is currently drawing
start_pos = None                       # starting position for shapes
last_pos = None                        # last mouse position for smooth drawing

font = pygame.font.SysFont(None, 24)   # font for text tool

typing = False                         # indicates whether user is typing text
text_input = ""                        # stores typed text
text_pos = (0,0)                       # position where text will appear


while True:                            # main program loop

    for event in pygame.event.get():   # process all events

        if event.type == QUIT:         # if window is closed
            pygame.quit()              # close pygame
            exit()                     # exit program

        if event.type == KEYDOWN:      # handle keyboard input

            if event.key == K_1: brush_index = 0   # select small brush
            elif event.key == K_2: brush_index = 1 # select medium brush
            elif event.key == K_3: brush_index = 2 # select large brush

            brush_size = brush_sizes[brush_index]  # update brush size

            if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                # if Ctrl + S pressed, save canvas to file
                import datetime
                name = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, name)

            if typing:                 # if text mode is active

                if event.key == K_RETURN:
                    # finalize text and draw it on canvas
                    text_surface = font.render(text_input, True, selected_color)
                    canvas.blit(text_surface, text_pos)
                    typing = False
                    text_input = ""

                elif event.key == K_ESCAPE:
                    # cancel typing
                    typing = False
                    text_input = ""

                elif event.key == K_BACKSPACE:
                    # remove last character
                    text_input = text_input[:-1]

                else:
                    # add typed character
                    text_input += event.unicode

        if event.type == MOUSEBUTTONDOWN:   # handle mouse click

            for i,r in enumerate(palette_rects):
                if r.collidepoint(event.pos):
                    selected_color = palette[i]  # select color

            for i,r in enumerate(tool_rects):
                if r.collidepoint(event.pos):
                    selected_tool = tools[i]     # select tool

            for i,r in enumerate(size_rects):
                if r.collidepoint(event.pos):
                    brush_index = i              # select brush size
                    brush_size = brush_sizes[i]

            if event.pos[1] > 60 and event.pos[0] > 60:
                # ensure drawing happens only inside canvas area

                if selected_tool == "fill":
                    flood_fill(canvas, event.pos, selected_color)
                    # apply flood fill tool

                elif selected_tool == "text":
                    typing = True
                    text_input = ""
                    text_pos = event.pos
                    # start typing mode

                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                    # start drawing

        if event.type == MOUSEBUTTONUP:  # when mouse released
            drawing = False
            last_pos = None

            if selected_tool not in ["brush","eraser","fill","text"]:
                # draw shape only for shape tools
                draw_shape(canvas, selected_tool, selected_color, start_pos, event.pos, brush_size)

    if drawing:                          # if user is drawing
        mouse_pos = pygame.mouse.get_pos()

        if selected_tool == "brush":
            # draw smooth line by connecting previous and current points
            if last_pos:
                pygame.draw.line(canvas, selected_color, last_pos, mouse_pos, brush_size)
            last_pos = mouse_pos

        elif selected_tool == "eraser":
            # erase by drawing white lines
            if last_pos:
                pygame.draw.line(canvas, (255,255,255), last_pos, mouse_pos, brush_size*2)
            last_pos = mouse_pos

    screen.blit(canvas,(0,0))            # draw canvas on screen

    if drawing and selected_tool not in ["brush","eraser","fill","text"]:
        # show preview of shapes while dragging
        temp = screen.copy()
        mouse_pos = pygame.mouse.get_pos()
        draw_shape(temp, selected_tool, selected_color, start_pos, mouse_pos, brush_size)
        screen.blit(temp,(0,0))

    if typing:
        # show text preview while typing
        temp_text = font.render(text_input, True, selected_color)
        screen.blit(temp_text, text_pos)

    pygame.draw.rect(screen,(200,200,200),(0,0,WIDTH,60))
    pygame.draw.rect(screen,(220,220,220),(0,60,60,HEIGHT))
    # draw UI panels

    for i,r in enumerate(palette_rects):
        pygame.draw.rect(screen,palette[i],r)
        if palette[i] == selected_color:
            pygame.draw.rect(screen,(255,255,255),r,3)
    # draw color palette and highlight selected color

    for i,r in enumerate(size_rects):
        pygame.draw.rect(screen,(180,180,180),r)

        if i == brush_index:
            pygame.draw.rect(screen,(255,255,255),r,3)

        cx,cy = r.center
        pygame.draw.circle(screen,(0,0,0),(cx,cy),brush_sizes[i])
    # draw brush size buttons

    for i,r in enumerate(tool_rects):
        pygame.draw.rect(screen,(180,180,180),r)

        if tools[i] == selected_tool:
            pygame.draw.rect(screen,(255,255,255),r,3)

        cx,cy = r.center

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
    # draw tool icons

    pygame.display.flip()               # update entire screen
    clock.tick(60)                     # limit program to 60 FPS