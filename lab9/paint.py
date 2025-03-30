import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

TOOL_PENCIL = "PENCIL"
TOOL_ERASER = "ERASER"
TOOL_RECTANGLE = "RECTANGLE"
TOOL_SQUARE = "SQUARE"
TOOL_CIRCLE = "CIRCLE"
TOOL_RIGHT_TRIANGLE = "RIGHT_TRIANGLE"
TOOL_EQUILATERAL_TRIANGLE = "EQUILATERAL_TRIANGLE"
TOOL_RHOMBUS = "RHOMBUS"

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

current_color = COLOR_BLACK
current_tool = TOOL_PENCIL
brush_size = 5

drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(COLOR_WHITE)

start_pos = None

font = pygame.font.SysFont(None, 24)

def draw_text(surface, text, x, y, color=COLOR_BLACK):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def draw_right_triangle(surface, color, start_pos, end_pos, width=1):
    x1, y1 = start_pos
    x2, y2 = end_pos
    pygame.draw.line(surface, color, (x1, y1), (x2, y1), width)
    pygame.draw.line(surface, color, (x2, y1), (x2, y2), width)
    pygame.draw.line(surface, color, (x2, y2), (x1, y1), width)

def draw_equilateral_triangle(surface, color, start_pos, end_pos, width=1):
    x1, y1 = start_pos
    x2, y2 = end_pos
    h = abs(y2 - y1)
    if h == 0:
        return
    s = (2 * h) / math.sqrt(3)
    direction = -1 if y2 < y1 else 1
    xA = x2
    yA = y2
    xB = x1 - s/2
    yB = y1
    xC = x1 + s/2
    yC = y1
    if direction == 1:
        xA = x1
        yA = y1
        xB = x2 - s/2
        yB = y2
        xC = x2 + s/2
        yC = y2
    pygame.draw.line(surface, color, (xA, yA), (xB, yB), width)
    pygame.draw.line(surface, color, (xB, yB), (xC, yC), width)
    pygame.draw.line(surface, color, (xC, yC), (xA, yA), width)

def draw_rhombus(surface, color, start_pos, end_pos, width=1):
    x1, y1 = start_pos
    x2, y2 = end_pos
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    top = (cx, y1)
    right = (x2, cy)
    bottom = (cx, y2)
    left = (x1, cy)
    pygame.draw.line(surface, color, top, right, width)
    pygame.draw.line(surface, color, right, bottom, width)
    pygame.draw.line(surface, color, bottom, left, width)
    pygame.draw.line(surface, color, left, top, width)

def draw_current_shape(temp_surface, shape_color, tool, start_pos, current_pos):
    if not start_pos:
        return
    x1, y1 = start_pos
    x2, y2 = current_pos
    if tool == TOOL_RECTANGLE:
        rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(temp_surface, shape_color, rect, 1)
    elif tool == TOOL_SQUARE:
        side = max(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side, side)
        if x2 < x1: 
            rect.x = x1 - side
        if y2 < y1:
            rect.y = y1 - side
        pygame.draw.rect(temp_surface, shape_color, rect, 1)
    elif tool == TOOL_CIRCLE:
        radius = int(math.dist(start_pos, current_pos))
        pygame.draw.circle(temp_surface, shape_color, start_pos, radius, 1)
    elif tool == TOOL_RIGHT_TRIANGLE:
        draw_right_triangle(temp_surface, shape_color, start_pos, current_pos, 1)
    elif tool == TOOL_EQUILATERAL_TRIANGLE:
        draw_equilateral_triangle(temp_surface, shape_color, start_pos, current_pos, 1)
    elif tool == TOOL_RHOMBUS:
        draw_rhombus(temp_surface, shape_color, start_pos, current_pos, 1)

def main():
    global current_color, current_tool, brush_size, start_pos

    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    current_tool = TOOL_PENCIL
                elif event.key == pygame.K_e:
                    current_tool = TOOL_ERASER
                elif event.key == pygame.K_r:
                    current_tool = TOOL_RECTANGLE
                elif event.key == pygame.K_s:
                    current_tool = TOOL_SQUARE
                elif event.key == pygame.K_c:
                    current_tool = TOOL_CIRCLE
                elif event.key == pygame.K_t:
                    current_tool = TOOL_RIGHT_TRIANGLE
                elif event.key == pygame.K_v:
                    current_tool = TOOL_EQUILATERAL_TRIANGLE
                elif event.key == pygame.K_h:
                    current_tool = TOOL_RHOMBUS
                elif event.key == pygame.K_1:
                    current_color = COLOR_BLACK
                elif event.key == pygame.K_2:
                    current_color = COLOR_RED
                elif event.key == pygame.K_3:
                    current_color = COLOR_GREEN
                elif event.key == pygame.K_4:
                    current_color = COLOR_BLUE
                elif event.key == pygame.K_5:
                    current_color = COLOR_WHITE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = mouse_pos
                    if current_tool == TOOL_PENCIL:
                        pygame.draw.circle(drawing_surface, current_color, mouse_pos, brush_size)
                    elif current_tool == TOOL_ERASER:
                        pygame.draw.circle(drawing_surface, COLOR_WHITE, mouse_pos, brush_size)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if current_tool in [TOOL_RECTANGLE, TOOL_SQUARE, TOOL_CIRCLE,
                                        TOOL_RIGHT_TRIANGLE, TOOL_EQUILATERAL_TRIANGLE, TOOL_RHOMBUS] and start_pos:
                        temp_surface = drawing_surface.copy()
                        draw_current_shape(temp_surface, current_color, current_tool, start_pos, mouse_pos)
                        drawing_surface.blit(temp_surface, (0, 0))
                    start_pos = None

        if pygame.mouse.get_pressed()[0]:
            if current_tool == TOOL_PENCIL:
                pygame.draw.line(drawing_surface, current_color, mouse_pos, mouse_pos, brush_size)
            elif current_tool == TOOL_ERASER:
                pygame.draw.line(drawing_surface, COLOR_WHITE, mouse_pos, mouse_pos, brush_size)

        win.fill(COLOR_WHITE)
        win.blit(drawing_surface, (0, 0))

        if start_pos and pygame.mouse.get_pressed()[0]:
            temp_surface = win.copy()
            draw_current_shape(temp_surface, current_color, current_tool, start_pos, mouse_pos)
            win.blit(temp_surface, (0, 0))

        draw_text(win, "Инструменты: [P] Карандаш, [E] Ластик, [R] Прямоугольник, [S] Квадрат, [C] Окружность,", 10, 10)
        draw_text(win, " [T] Прям. треугольник, [V] Равностор. треугольник, [H] Ромб", 10, 30)
        draw_text(win, "Цвета: [1] Чёрный, [2] Красный, [3] Зелёный, [4] Синий, [5] Белый", 10, 50)
        draw_text(win, f"Текущий инструмент: {current_tool}", 10, 70)
        draw_text(win, f"Текущий цвет: {current_color}", 10, 90)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
