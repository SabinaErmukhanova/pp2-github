import pygame   # import pygame to use drawing functions and surface operations


# function to draw all shapes depending on selected tool
def draw_shape(surface, tool, color, start, end, size):

    # draw a straight line between two points
    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)

    # draw a rectangle using two opposite corners
    elif tool == "rect":
        x = min(start[0], end[0])   # left coordinate
        y = min(start[1], end[1])   # top coordinate
        w = abs(start[0] - end[0])  # width of rectangle
        h = abs(start[1] - end[1])  # height of rectangle
        pygame.draw.rect(surface, color, (x, y, w, h), size)

    # draw a circle where start is center and distance defines radius
    elif tool == "circle":
        dx = end[0] - start[0]      # horizontal distance
        dy = end[1] - start[1]      # vertical distance
        r = int((dx**2 + dy**2) ** 0.5)   # calculate radius using distance formula
        pygame.draw.circle(surface, color, start, r, size)

    # draw a square with equal width and height
    elif tool == "square":
        s = min(abs(end[0] - start[0]), abs(end[1] - start[1]))  # side length
        pygame.draw.rect(surface, color, (start[0], start[1], s, s), size)

    # draw a right triangle using three points
    elif tool == "rtriangle":
        x1, y1 = start
        x2, y2 = end
        pygame.draw.polygon(surface, color,
                            [(x1, y1), (x2, y1), (x1, y2)], size)

    # draw an equilateral triangle
    elif tool == "etriangle":
        x1, y1 = start
        x2, y2 = end
        base = abs(x2 - x1)   # base length
        height = int((3 ** 0.5 / 2) * base)   # height based on geometry formula
        pygame.draw.polygon(surface, color,
                            [(x1, y1),
                             (x1 + base, y1),
                             (x1 + base // 2, y1 - height)], size)

    # draw a rhombus shape using center-based points
    elif tool == "rhombus":
        x1, y1 = start
        x2, y2 = end
        cx = (x1 + x2) // 2   # center x coordinate
        cy = (y1 + y2) // 2   # center y coordinate
        pygame.draw.polygon(surface, color,
                            [(cx, y1),    # top
                             (x2, cy),    # right
                             (cx, y2),    # bottom
                             (x1, cy)], size)   # left


# flood fill algorithm to fill an area with a color
def flood_fill(surface, pos, new_color):

    target_color = surface.get_at(pos)   # get color at clicked position

    # if the new color is the same as the target color, do nothing
    if target_color == new_color:
        return

    stack = [pos]   # use stack to store pixels to process

    # loop until all connected pixels are filled
    while stack:
        x, y = stack.pop()   # get last pixel from stack

        # skip if pixel is outside surface boundaries
        if x < 0 or x >= surface.get_width():
            continue
        if y < 0 or y >= surface.get_height():
            continue

        # skip if pixel color is not the target color
        if surface.get_at((x, y)) != target_color:
            continue

        # change pixel color to new color
        surface.set_at((x, y), new_color)

        # add neighboring pixels to stack
        stack.append((x + 1, y))   # right
        stack.append((x - 1, y))   # left
        stack.append((x, y + 1))   # down
        stack.append((x, y - 1))   # up