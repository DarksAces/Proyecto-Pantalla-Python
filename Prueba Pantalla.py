import pygame
import sys
import pyperclip

pygame.init()

# Configuración ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Editor Avanzado - Pantalla Negra")

BLACK = (0,0,0)
WHITE = (255,255,255)
font = pygame.font.SysFont(None, 36)
LINE_HEIGHT = font.get_height() + 5

# Colores por nombre
COLOR_NAMES = {
    "blanco": WHITE,
    "negro": BLACK,
    "rojo": (255,0,0),
    "verde": (0,255,0),
    "azul": (0,0,255),
    "amarillo": (255,255,0),
}

# Lista de líneas, cada línea es [texto, color]
lines = [["", WHITE]]

cursor_row = 0
cursor_col = 0
current_color = WHITE

def draw_screen():
    screen.fill(BLACK)
    y = 0
    for row, (text, color) in enumerate(lines):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (5, y))
        # Cursor
        if row == cursor_row:
            cursor_x = 5 + font.size(text[:cursor_col])[0]
            cursor_y = y
            pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + font.get_height()), 2)
        y += LINE_HEIGHT

def parse_color_name(word):
    """Devuelve color por nombre o None"""
    return COLOR_NAMES.get(word.lower(), None)

while True:
    draw_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            line_text, line_color = lines[cursor_row]
            if event.key == pygame.K_BACKSPACE:
                if cursor_col > 0:
                    # Borrar carácter antes del cursor
                    lines[cursor_row][0] = line_text[:cursor_col-1] + line_text[cursor_col:]
                    cursor_col -= 1
                elif cursor_row > 0:
                    # Unir con línea anterior
                    prev_text, prev_color = lines[cursor_row-1]
                    cursor_col = len(prev_text)
                    lines[cursor_row-1][0] = prev_text + line_text
                    lines.pop(cursor_row)
                    cursor_row -= 1
            elif event.key == pygame.K_RETURN:
                # Salto de línea
                new_line = [line_text[cursor_col:], line_color]
                lines[cursor_row][0] = line_text[:cursor_col]
                lines.insert(cursor_row+1, new_line)
                cursor_row += 1
                cursor_col = 0
            elif event.key == pygame.K_LEFT:
                if cursor_col > 0:
                    cursor_col -= 1
                elif cursor_row > 0:
                    cursor_row -= 1
                    cursor_col = len(lines[cursor_row][0])
            elif event.key == pygame.K_RIGHT:
                if cursor_col < len(line_text):
                    cursor_col += 1
                elif cursor_row < len(lines)-1:
                    cursor_row += 1
                    cursor_col = 0
            elif event.key == pygame.K_UP:
                if cursor_row > 0:
                    cursor_row -= 1
                    cursor_col = min(cursor_col, len(lines[cursor_row][0]))
            elif event.key == pygame.K_DOWN:
                if cursor_row < len(lines)-1:
                    cursor_row += 1
                    cursor_col = min(cursor_col, len(lines[cursor_row][0]))
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Pegar portapapeles
                paste_text = pyperclip.paste()
                lines[cursor_row][0] = line_text[:cursor_col] + paste_text + line_text[cursor_col:]
                cursor_col += len(paste_text)
            else:
                # Escribir carácter
                char = event.unicode
                if char:
                    lines[cursor_row][0] = line_text[:cursor_col] + char + line_text[cursor_col:]
                    cursor_col += 1
                    # Comprobar si el último "palabra" es color
                    words = lines[cursor_row][0].split()
                    last_word = words[-1]
                    color = parse_color_name(last_word)
                    if color:
                        current_color = color
                        lines[cursor_row][1] = current_color
                        # Borrar la palabra de color del texto
                        lines[cursor_row][0] = " ".join(words[:-1])
                        
    pygame.display.flip()