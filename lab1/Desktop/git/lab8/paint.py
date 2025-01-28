import pygame
import math

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Extended Paint")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Variables to hold the state
drawing = False
shape_start_pos = None
tool = 'brush'  # Default tool
current_color = BLACK
brush_size = 5

# Set up font for text
font = pygame.font.SysFont('Arial', 20)

# Clear the screen
screen.fill(WHITE)

# Helper functions
def draw_brush(pos):
    pygame.draw.circle(screen, current_color, pos, brush_size)

def draw_rectangle(start_pos, end_pos):
    width = end_pos[0] - start_pos[0]
    height = end_pos[1] - start_pos[1]
    pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], width, height), 1)

def draw_circle(start_pos, end_pos):
    radius = int(math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2))
    pygame.draw.circle(screen, current_color, start_pos, radius, 1)

def draw_eraser(pos):
    pygame.draw.circle(screen, WHITE, pos, brush_size)

def color_palette():
    pygame.draw.rect(screen, RED, (10, 10, 30, 30))
    pygame.draw.rect(screen, GREEN, (50, 10, 30, 30))
    pygame.draw.rect(screen, BLUE, (90, 10, 30, 30))

def show_tools():
    # Display current tool
    tool_text = font.render(f"Tool: {tool}", True, BLACK)
    screen.blit(tool_text, (140, 15))
    # Display current color
    pygame.draw.rect(screen, current_color, (300, 10, 30, 30))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                if 10 <= x <= 40 and 10 <= y <= 40:
                    current_color = RED
                elif 50 <= x <= 80 and 10 <= y <= 40:
                    current_color = GREEN
                elif 90 <= x <= 120 and 10 <= y <= 40:
                    current_color = BLUE
                else:
                    drawing = True
                    shape_start_pos = event.pos
            if event.button == 3:  # Right click to erase
                tool = 'eraser'
                drawing = True

        # Mouse button released
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool == 'rectangle':
                    draw_rectangle(shape_start_pos, event.pos)
                elif tool == 'circle':
                    draw_circle(shape_start_pos, event.pos)
            drawing = False

        # Key press event to change tools
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = 'brush'
            elif event.key == pygame.K_r:
                tool = 'rectangle'
            elif event.key == pygame.K_c:
                tool = 'circle'
            elif event.key == pygame.K_e:
                tool = 'eraser'

    # Drawing while moving the mouse with a pressed button
    if drawing:
        if tool == 'brush':
            draw_brush(pygame.mouse.get_pos())
        elif tool == 'eraser':
            draw_eraser(pygame.mouse.get_pos())

    # Update display
    color_palette()
    show_tools()
    pygame.display.update()

# Quit pygame
pygame.quit()
