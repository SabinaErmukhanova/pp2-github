import pygame                              # import pygame library for graphics and input handling
from pygame.locals import *                # import constants like QUIT, MOUSEBUTTONDOWN, etc.

pygame.init()                              # initialize all pygame modules

WIDTH = 900                                # set window width
HEIGHT = 600                               # set window height

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # create the main window with given size
pygame.display.set_caption("Paint PRO")    # set window title

clock = pygame.time.Clock()                # create clock object to control FPS

canvas = pygame.Surface((WIDTH, HEIGHT))   # create separate surface for drawing
canvas.fill((255,255,255))                 # fill canvas with white color (background)

palette = [                                # list of available colors
    (255,0,0),                              # red
    (0,255,0),                              # green
    (0,0,255),                              # blue
    (0,0,0),                                # black
    (255,255,0)                             # yellow
]

selected_color = palette[2]                # default selected color is blue

tools = ["brush", "line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus", "eraser"]  # list of drawing tools
selected_tool = "brush"                    # default tool is brush

tool_rects = []                            # list to store tool button rectangles
for i in range(len(tools)):                # loop through all tools
    rect = pygame.Rect(10, 70 + i*50, 40, 40)   # create rectangle for each tool button
    tool_rects.append(rect)                # add rectangle to list

palette_rects = []                         # list to store color button rectangles
for i in range(5):                         # loop for each color
    rect = pygame.Rect(100 + i*50, 10, 40, 40)  # create rectangle for color button
    palette_rects.append(rect)             # add rectangle to list

drawing = False                            # flag to check if user is currently drawing
start_pos = None                           # starting position for shapes

while True:                                # main program loop (runs forever)

    for event in pygame.event.get():       # process all events (mouse, keyboard, etc.)
        if event.type == QUIT:             # if user closes window
            pygame.quit()                  # stop pygame
            exit()                         # exit program

        if event.type == MOUSEBUTTONDOWN:  # when mouse button is pressed

            for i, rect in enumerate(palette_rects):   # check color buttons
                if rect.collidepoint(event.pos):        # if click is inside color rectangle
                    selected_color = palette[i]         # change current drawing color

            for i, rect in enumerate(tool_rects):       # check tool buttons
                if rect.collidepoint(event.pos):        # if click is inside tool rectangle
                    selected_tool = tools[i]            # change current tool

            if event.pos[1] > 60 and event.pos[0] > 60: # ensure click is on drawing area, not UI
                drawing = True                          # start drawing
                start_pos = event.pos                   # save starting position

        if event.type == MOUSEBUTTONUP and drawing:     # when mouse button released
            drawing = False                             # stop drawing
            end_pos = event.pos                         # save end position

            # draw different shapes depending on selected tool
            if selected_tool == "line":
                pygame.draw.line(canvas, selected_color, start_pos, end_pos, 3)

            elif selected_tool == "rect":
                x = min(start_pos[0], end_pos[0])       # calculate top-left corner
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])      # width
                h = abs(start_pos[1] - end_pos[1])      # height
                pygame.draw.rect(canvas, selected_color, (x,y,w,h), 3)

            elif selected_tool == "circle":
                dx = end_pos[0] - start_pos[0]          # difference in x
                dy = end_pos[1] - start_pos[1]          # difference in y
                r = int((dx**2 + dy**2)**0.5)           # calculate radius using distance formula
                pygame.draw.circle(canvas, selected_color, start_pos, r, 3)

            elif selected_tool == "square":
                size = min(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))  # make equal sides
                pygame.draw.rect(canvas, selected_color,
                                 (start_pos[0], start_pos[1], size, size), 3)

            elif selected_tool == "rtriangle":          # right triangle
                x1, y1 = start_pos
                x2, y2 = end_pos
                points = [(x1, y1), (x2, y1), (x1, y2)] # 90 degree triangle points
                pygame.draw.polygon(canvas, selected_color, points, 3)

            elif selected_tool == "etriangle":          # equilateral triangle
                x1, y1 = start_pos
                x2, y2 = end_pos
                base = abs(x2 - x1)                     # base length
                height = int((3**0.5 / 2) * base)       # calculate height using formula
                points = [
                    (x1, y1),
                    (x1 + base, y1),
                    (x1 + base//2, y1 - height)
                ]
                pygame.draw.polygon(canvas, selected_color, points, 3)

            elif selected_tool == "rhombus":            # rhombus shape
                x1, y1 = start_pos
                x2, y2 = end_pos
                cx = (x1 + x2)//2                      # center x
                cy = (y1 + y2)//2                      # center y
                points = [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ]
                pygame.draw.polygon(canvas, selected_color, points, 3)

    if drawing:                                # if user is holding mouse button
        mouse_pos = pygame.mouse.get_pos()     # get current mouse position

        if selected_tool == "brush":           # free drawing
            pygame.draw.circle(canvas, selected_color, mouse_pos, 5)

        elif selected_tool == "eraser":        # erase by drawing white
            pygame.draw.circle(canvas, (255,255,255), mouse_pos, 10)

    screen.blit(canvas, (0,0))                 # draw canvas onto screen

    # preview shape while dragging mouse
    if drawing and selected_tool in ["line","rect","circle","square","rtriangle","etriangle","rhombus"]:
        temp = screen.copy()                   # copy screen for temporary preview
        mouse_pos = pygame.mouse.get_pos()

        if selected_tool == "line":
            pygame.draw.line(temp, selected_color, start_pos, mouse_pos, 2)

        elif selected_tool == "rect":
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = abs(start_pos[0] - mouse_pos[0])
            h = abs(start_pos[1] - mouse_pos[1])
            pygame.draw.rect(temp, selected_color, (x,y,w,h), 2)

        elif selected_tool == "circle":
            dx = mouse_pos[0] - start_pos[0]
            dy = mouse_pos[1] - start_pos[1]
            r = int((dx**2 + dy**2)**0.5)
            pygame.draw.circle(temp, selected_color, start_pos, r, 2)

        elif selected_tool == "square":
            size = min(abs(mouse_pos[0]-start_pos[0]), abs(mouse_pos[1]-start_pos[1]))
            pygame.draw.rect(temp, selected_color,
                             (start_pos[0], start_pos[1], size, size), 2)

        elif selected_tool == "rtriangle":
            x1, y1 = start_pos
            x2, y2 = mouse_pos
            points = [(x1, y1), (x2, y1), (x1, y2)]
            pygame.draw.polygon(temp, selected_color, points, 2)

        elif selected_tool == "etriangle":
            x1, y1 = start_pos
            x2, y2 = mouse_pos
            base = abs(x2 - x1)
            height = int((3**0.5 / 2) * base)
            points = [
                (x1, y1),
                (x1 + base, y1),
                (x1 + base//2, y1 - height)
            ]
            pygame.draw.polygon(temp, selected_color, points, 2)

        elif selected_tool == "rhombus":
            x1, y1 = start_pos
            x2, y2 = mouse_pos
            cx = (x1 + x2)//2
            cy = (y1 + y2)//2
            points = [
                (cx, y1),
                (x2, cy),
                (cx, y2),
                (x1, cy)
            ]
            pygame.draw.polygon(temp, selected_color, points, 2)

        screen.blit(temp, (0,0))               # draw preview

    pygame.draw.rect(screen, (200,200,200), (0,0,WIDTH,60))     # top panel
    pygame.draw.rect(screen, (220,220,220), (0,60,60,HEIGHT))   # left panel

    for i, rect in enumerate(palette_rects):   # draw color buttons
        pygame.draw.rect(screen, palette[i], rect)
        if palette[i] == selected_color:
            pygame.draw.rect(screen, (255,255,255), rect, 3)

    for i, rect in enumerate(tool_rects):      # draw tool buttons
        pygame.draw.rect(screen, (180,180,180), rect)

        if tools[i] == selected_tool:
            pygame.draw.rect(screen, (255,255,255), rect, 3)

        cx, cy = rect.center                   # center of button

        # draw icon depending on tool
        if tools[i] == "brush":
            pygame.draw.circle(screen, (0,0,0), (cx,cy), 5)
        elif tools[i] == "line":
            pygame.draw.line(screen, (0,0,0), (cx-10,cy-10),(cx+10,cy+10),2)
        elif tools[i] == "rect":
            pygame.draw.rect(screen, (0,0,0), (cx-12, cy-8, 24, 16), 2)
        elif tools[i] == "circle":
            pygame.draw.circle(screen, (0,0,0), (cx,cy),10,2)
        elif tools[i] == "square":
            pygame.draw.rect(screen, (0,0,0), (cx-10, cy-10, 20, 20), 2)
        elif tools[i] == "rtriangle":
            pygame.draw.polygon(screen, (0,0,0), [(cx-10,cy+10),(cx+10,cy+10),(cx-10,cy-10)],2)
        elif tools[i] == "etriangle":
            pygame.draw.polygon(screen, (0,0,0), [(cx,cy-10),(cx-10,cy+10),(cx+10,cy+10)],2)
        elif tools[i] == "rhombus":
            pygame.draw.polygon(screen, (0,0,0), [(cx,cy-10),(cx+10,cy),(cx,cy+10),(cx-10,cy)],2)
        elif tools[i] == "eraser":
            pygame.draw.rect(screen, (255,255,255), (cx-10,cy-10,20,20))

    pygame.display.flip()                      # update screen
    clock.tick(60)                            # limit to 60 frames per second