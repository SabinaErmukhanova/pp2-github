import pygame                              # import pygame library
from pygame.locals import *                # import pygame constants like QUIT, MOUSEBUTTONDOWN

pygame.init()                              # initialize pygame

WIDTH = 900                                # window width
HEIGHT = 600                               # window height

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # create main window
pygame.display.set_caption("Paint PRO")    # set window title

clock = pygame.time.Clock()                # create clock to control FPS

canvas = pygame.Surface((WIDTH, HEIGHT))   # create separate drawing surface
canvas.fill((255,255,255))                 # fill canvas with white color

palette = [                                # list of available colors
    (255,0,0),                              # red
    (0,255,0),                              # green
    (0,0,255),                              # blue
    (0,0,0),                                # black
    (255,255,0)                             # yellow
]

selected_color = palette[2]                # selected color is blue by default

tools = ["brush", "line", "rect", "circle", "eraser"]   # list of tools
selected_tool = "brush"                    # selected tool is brush by default

tool_rects = []                            # list for tool button rectangles
for i in range(len(tools)):                # loop through all tools
    rect = pygame.Rect(10, 70 + i*60, 40, 40)   # create button rectangle
    tool_rects.append(rect)                # add button rectangle to list

palette_rects = []                         # list for color button rectangles
for i in range(5):                         # loop for 5 colors
    rect = pygame.Rect(100 + i*50, 10, 40, 40)  # create color rectangle
    palette_rects.append(rect)             # add rectangle to list

drawing = False                            # shows whether user is drawing now
start_pos = None                           # starting position for line/rect/circle

cursor_x, cursor_y = 300, 300              # cursor position variable, not important here

while True:                                # main program loop

    for event in pygame.event.get():       # handle all pygame events
        if event.type == QUIT:             # if window close button is pressed
            pygame.quit()                  # close pygame
            exit()                         # stop program

        if event.type == MOUSEBUTTONDOWN:  # if mouse button is pressed

            for i, rect in enumerate(palette_rects):   # check all palette buttons
                if rect.collidepoint(event.pos):        # if mouse clicked this color
                    selected_color = palette[i]         # change selected color

            for i, rect in enumerate(tool_rects):       # check all tool buttons
                if rect.collidepoint(event.pos):        # if mouse clicked this tool
                    selected_tool = tools[i]            # change selected tool

            if event.pos[1] > 60 and event.pos[0] > 60: # check that click is on canvas, not UI
                drawing = True                          # start drawing
                start_pos = event.pos                   # save starting point

        if event.type == MOUSEBUTTONUP and drawing:     # if mouse button released while drawing
            drawing = False                             # stop drawing
            end_pos = event.pos                         # save ending point

            if selected_tool == "line":                 # if selected tool is line
                pygame.draw.line(canvas, selected_color, start_pos, end_pos, 3)  # draw line

            elif selected_tool == "rect":               # if selected tool is rectangle
                x = min(start_pos[0], end_pos[0])        # left x coordinate
                y = min(start_pos[1], end_pos[1])        # top y coordinate
                w = abs(start_pos[0] - end_pos[0])       # rectangle width
                h = abs(start_pos[1] - end_pos[1])       # rectangle height
                pygame.draw.rect(canvas, selected_color, (x,y,w,h), 3)  # draw rectangle

            elif selected_tool == "circle":             # if selected tool is circle
                dx = end_pos[0] - start_pos[0]           # distance by x
                dy = end_pos[1] - start_pos[1]           # distance by y
                r = int((dx**2 + dy**2)**0.5)            # calculate radius
                pygame.draw.circle(canvas, selected_color, start_pos, r, 3)  # draw circle

    if drawing:                                # if user is drawing now
        mouse_pos = pygame.mouse.get_pos()     # get current mouse position

        if selected_tool == "brush":           # if brush is selected
            pygame.draw.circle(canvas, selected_color, mouse_pos, 5)  # draw small circles

        elif selected_tool == "eraser":        # if eraser is selected
            pygame.draw.circle(canvas, (255,255,255), mouse_pos, 10)  # erase with white

    screen.blit(canvas, (0,0))                 # draw canvas on screen

    if drawing and selected_tool in ["line","rect","circle"]:  # if drawing a shape
        temp = screen.copy()                   # copy screen for preview
        mouse_pos = pygame.mouse.get_pos()     # get current mouse position

        if selected_tool == "line":            # preview line
            pygame.draw.line(temp, selected_color, start_pos, mouse_pos, 2)

        elif selected_tool == "rect":          # preview rectangle
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = abs(start_pos[0] - mouse_pos[0])
            h = abs(start_pos[1] - mouse_pos[1])
            pygame.draw.rect(temp, selected_color, (x,y,w,h), 2)

        elif selected_tool == "circle":        # preview circle
            dx = mouse_pos[0] - start_pos[0]
            dy = mouse_pos[1] - start_pos[1]
            r = int((dx**2 + dy**2)**0.5)
            pygame.draw.circle(temp, selected_color, start_pos, r, 2)

        screen.blit(temp, (0,0))               # show preview on screen

    pygame.draw.rect(screen, (200,200,200), (0,0,WIDTH,60))     # draw top UI panel
    pygame.draw.rect(screen, (220,220,220), (0,60,60,HEIGHT))   # draw left UI panel

    for i, rect in enumerate(palette_rects):   # draw color palette
        pygame.draw.rect(screen, palette[i], rect)  # draw color square
        if palette[i] == selected_color:       # if this color is selected
            pygame.draw.rect(screen, (255,255,255), rect, 3)  # draw white border

    for i, rect in enumerate(tool_rects):      # draw tool buttons
        pygame.draw.rect(screen, (180,180,180), rect)  # draw button background

        if tools[i] == selected_tool:          # if this tool is selected
            pygame.draw.rect(screen, (255,255,255), rect, 3)  # draw white border

        cx, cy = rect.center                   # get center of button for icon

        if tools[i] == "brush":                # draw brush icon
            pygame.draw.circle(screen, (0,0,0), (cx,cy), 5)

        elif tools[i] == "line":               # draw line icon
            pygame.draw.line(screen, (0,0,0), (cx-10,cy-10),(cx+10,cy+10),2)

        elif tools[i] == "rect":               # draw rectangle icon
            pygame.draw.rect(screen, (0,0,0), (cx-10,cy-10,20,20),2)

        elif tools[i] == "circle":             # draw circle icon
            pygame.draw.circle(screen, (0,0,0), (cx,cy),10,2)

        elif tools[i] == "eraser":             # draw eraser icon
            pygame.draw.rect(screen, (255,255,255), (cx-10,cy-10,20,20))

    pygame.display.flip()                      # update the whole display
    clock.tick(60)                             # limit program to 60 FPS