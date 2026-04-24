import pygame
from pygame.locals import *

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint PRO")

clock = pygame.time.Clock()

# холст
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))

#  COLORS 
palette = [
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (0,0,0),
    (255,255,0)
]

selected_color = palette[2]

# TOOLS 
tools = ["brush", "line", "rect", "circle", "eraser"]
selected_tool = "brush"

# позиции кнопок инструментов
tool_rects = []
for i in range(len(tools)):
    rect = pygame.Rect(10, 70 + i*60, 40, 40)
    tool_rects.append(rect)

# позиции палитры
palette_rects = []
for i in range(5):
    rect = pygame.Rect(100 + i*50, 10, 40, 40)
    palette_rects.append(rect)

drawing = False
start_pos = None

cursor_x, cursor_y = 300, 300

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        #  MOUSE 
        if event.type == MOUSEBUTTONDOWN:

            # выбор цвета
            for i, rect in enumerate(palette_rects):
                if rect.collidepoint(event.pos):
                    selected_color = palette[i]

            # выбор инструмента
            for i, rect in enumerate(tool_rects):
                if rect.collidepoint(event.pos):
                    selected_tool = tools[i]

            # начать рисовать
            if event.pos[1] > 60 and event.pos[0] > 60:
                drawing = True
                start_pos = event.pos

        if event.type == MOUSEBUTTONUP and drawing:
            drawing = False
            end_pos = event.pos

            if selected_tool == "line":
                pygame.draw.line(canvas, selected_color, start_pos, end_pos, 3)

            elif selected_tool == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(canvas, selected_color, (x,y,w,h), 3)

            elif selected_tool == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                r = int((dx**2 + dy**2)**0.5)
                pygame.draw.circle(canvas, selected_color, start_pos, r, 3)

    #  DRAWING 
    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if selected_tool == "brush":
            pygame.draw.circle(canvas, selected_color, mouse_pos, 5)

        elif selected_tool == "eraser":
            pygame.draw.circle(canvas, (255,255,255), mouse_pos, 10)

    #  RENDER 
    screen.blit(canvas, (0,0))

    #  PREVIEW 
    if drawing and selected_tool in ["line","rect","circle"]:
        temp = screen.copy()
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

        screen.blit(temp, (0,0))

    # UI BACKGROUND 
    pygame.draw.rect(screen, (200,200,200), (0,0,WIDTH,60))
    pygame.draw.rect(screen, (220,220,220), (0,60,60,HEIGHT))

    # DRAW PALETTE 
    for i, rect in enumerate(palette_rects):
        pygame.draw.rect(screen, palette[i], rect)
        if palette[i] == selected_color:
            pygame.draw.rect(screen, (255,255,255), rect, 3)

    for i, rect in enumerate(tool_rects):
        pygame.draw.rect(screen, (180,180,180), rect)

        if tools[i] == selected_tool:
            pygame.draw.rect(screen, (255,255,255), rect, 3)

        # простые иконки
        cx, cy = rect.center

        if tools[i] == "brush":
            pygame.draw.circle(screen, (0,0,0), (cx,cy), 5)

        elif tools[i] == "line":
            pygame.draw.line(screen, (0,0,0), (cx-10,cy-10),(cx+10,cy+10),2)

        elif tools[i] == "rect":
            pygame.draw.rect(screen, (0,0,0), (cx-10,cy-10,20,20),2)

        elif tools[i] == "circle":
            pygame.draw.circle(screen, (0,0,0), (cx,cy),10,2)

        elif tools[i] == "eraser":
            pygame.draw.rect(screen, (255,255,255), (cx-10,cy-10,20,20))

    pygame.display.flip()
    clock.tick(60)