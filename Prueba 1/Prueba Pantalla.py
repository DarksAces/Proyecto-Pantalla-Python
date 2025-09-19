import pygame
import sys
import pyperclip

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Editor de texto")
font = pygame.font.SysFont("Consolas", 24)

# Cada línea es [texto, color]
lines = [["hola mundo", (255,255,255)]]

cursor_row, cursor_col = 0, 0
current_color = (255, 255, 255)

def parse_color_name(word):
    colors = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
    }
    return colors.get(word.lower())

def draw_screen():
    screen.fill((30, 30, 30))
    y = 10
    for idx, (text, color) in enumerate(lines):
        display_text = text.replace("\t", "    ")  # mostrar tabs como 4 espacios
        img = font.render(display_text, True, color)
        screen.blit(img, (10, y))
        if idx == cursor_row:
            cursor_x = 10 + font.size(display_text[:cursor_col])[0]
            pygame.draw.line(screen, (200, 200, 200), (cursor_x, y), (cursor_x, y + font.get_height()))
        y += font.get_height() + 5

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
                    lines[cursor_row][0] = line_text[:cursor_col-1] + line_text[cursor_col:]
                    cursor_col -= 1
                elif cursor_row > 0:
                    prev_text, prev_color = lines[cursor_row-1]
                    cursor_col = len(prev_text)
                    lines[cursor_row-1][0] = prev_text + line_text
                    lines.pop(cursor_row)
                    cursor_row -= 1
                elif event.key == pygame.K_DELETE:
                    if cursor_col < len(line_text):
                        lines[cursor_row][0] = line_text[:cursor_col] + line_text[cursor_col+1:]

            elif event.key == pygame.K_RETURN:
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
                paste_text = pyperclip.paste()
                lines[cursor_row][0] = line_text[:cursor_col] + paste_text + line_text[cursor_col:]
                cursor_col += len(paste_text)

            else:
                char = event.unicode
                if char not in ["\r", "\n"]:  # evitar duplicado en Enter
                    if char == "\t":
                        tab_spaces = "    "
                        lines[cursor_row][0] = line_text[:cursor_col] + tab_spaces + line_text[cursor_col:]
                        cursor_col += len(tab_spaces)
                    else:
                        lines[cursor_row][0] = line_text[:cursor_col] + char + line_text[cursor_col:]
                        cursor_col += 1

                    # Detectar color solo si el último token es palabra real
                    words = lines[cursor_row][0].strip().split(" ")
                    if words and words[-1]:
                        color = parse_color_name(words[-1])
                        if color:
                            current_color = color
                            lines[cursor_row][1] = current_color
                            # Eliminar palabra de color del texto
                            lines[cursor_row][0] = " ".join(words[:-1])
                            cursor_col = len(lines[cursor_row][0])

    pygame.display.flip()
