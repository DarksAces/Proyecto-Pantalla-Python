import pygame
import sys
import pyperclip

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Editor de texto")
font = pygame.font.SysFont("Consolas", 24)
clock = pygame.time.Clock()

# Cada línea es una lista de fragmentos [(texto, color), ...] y un flag editable
lines = [
    [[("Linea fija, no editable", (200, 200, 200))], False],  # línea fija
    [[("", (255, 255, 255))], True]                           # línea editable
]


cursor_row, cursor_col = 1, 0  # Empezar en línea editable

# Colores predefinidos
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203)
}

def parse_color_name(word):
    """Devuelve el color RGB si la palabra es un nombre de color válido"""
    return COLORS.get(word.lower())

def get_line_text(line_fragments):
    """Obtiene el texto completo de una línea a partir de sus fragmentos"""
    return "".join([fragment[0] for fragment in line_fragments])

def get_cursor_fragment_info(line_fragments, cursor_col):
    """Obtiene información sobre el fragmento donde está el cursor"""
    current_pos = 0
    for i, (text, color) in enumerate(line_fragments):
        if current_pos + len(text) >= cursor_col:
            return i, cursor_col - current_pos, color
        current_pos += len(text)
    # Si el cursor está al final, usar el último fragmento
    if line_fragments:
        return len(line_fragments) - 1, len(line_fragments[-1][0]), line_fragments[-1][1]
    return 0, 0, (255, 255, 255)

def draw_screen():
    screen.fill((30, 30, 30))
    y = 10
    for idx, (line_fragments, editable) in enumerate(lines):
        x = 10
        full_text = ""
        
        # Dibujar cada fragmento con su color
        for text, color in line_fragments:
            display_text = text.replace("\t", "    ")
            full_text += display_text
            if display_text:  # Solo renderizar si hay texto
                img = font.render(display_text, True, color)
                screen.blit(img, (x, y))
                x += img.get_width()
        
        # Dibujar cursor solo en líneas editables
        if idx == cursor_row and editable:
            cursor_x = 10 + font.size(full_text[:cursor_col])[0]
            pygame.draw.line(screen, (200, 200, 200), (cursor_x, y), (cursor_x, y + font.get_height()))
        y += font.get_height() + 5
    
    pygame.display.flip()

def find_next_editable_line(start_row, direction):
    """Encuentra la siguiente línea editable en la dirección especificada"""
    if direction == 1:  # hacia abajo
        for i in range(start_row + 1, len(lines)):
            if lines[i][1]:  # si es editable
                return i
    else:  # hacia arriba
        for i in range(start_row - 1, -1, -1):
            if lines[i][1]:  # si es editable
                return i
    return start_row  # si no encuentra, mantener posición actual

while True:
    draw_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            line_fragments, editable = lines[cursor_row]
            line_text = get_line_text(line_fragments)

            # Navegación con flechas - SIEMPRE permitida
            if event.key == pygame.K_LEFT:
                if cursor_col > 0:
                    cursor_col -= 1
                else:
                    # Buscar línea editable anterior
                    prev_editable = find_next_editable_line(cursor_row, -1)
                    if prev_editable != cursor_row:
                        cursor_row = prev_editable
                        cursor_col = len(get_line_text(lines[cursor_row][0]))
                        
            elif event.key == pygame.K_RIGHT:
                if cursor_col < len(line_text):
                    cursor_col += 1
                else:
                    # Buscar línea editable siguiente
                    next_editable = find_next_editable_line(cursor_row, 1)
                    if next_editable != cursor_row:
                        cursor_row = next_editable
                        cursor_col = 0
                        
            elif event.key == pygame.K_UP:
                prev_editable = find_next_editable_line(cursor_row, -1)
                if prev_editable != cursor_row:
                    cursor_row = prev_editable
                    cursor_col = min(cursor_col, len(get_line_text(lines[cursor_row][0])))
                    
            elif event.key == pygame.K_DOWN:
                next_editable = find_next_editable_line(cursor_row, 1)
                if next_editable != cursor_row:
                    cursor_row = next_editable
                    cursor_col = min(cursor_col, len(get_line_text(lines[cursor_row][0])))

            # Solo permitir edición en líneas editables
            if not editable:
                continue

            # Obtener información del fragmento actual
            frag_idx, frag_col, current_color = get_cursor_fragment_info(line_fragments, cursor_col)

            # Backspace
            if event.key == pygame.K_BACKSPACE:
                if cursor_col > 0:
                    # Eliminar carácter del fragmento actual
                    if frag_col > 0:
                        # Eliminar dentro del fragmento
                        old_text = line_fragments[frag_idx][0]
                        new_text = old_text[:frag_col-1] + old_text[frag_col:]
                        line_fragments[frag_idx] = (new_text, line_fragments[frag_idx][1])
                    else:
                        # Eliminar del fragmento anterior
                        if frag_idx > 0:
                            prev_text = line_fragments[frag_idx-1][0]
                            line_fragments[frag_idx-1] = (prev_text[:-1], line_fragments[frag_idx-1][1])
                    cursor_col -= 1
                    
                    # Limpiar fragmentos vacíos
                    lines[cursor_row][0] = [(text, color) for text, color in line_fragments if text]
                    if not lines[cursor_row][0]:
                        lines[cursor_row][0] = [("", (255, 255, 255))]
                else:
                    # Unir con línea anterior
                    prev_editable = find_next_editable_line(cursor_row, -1)
                    if prev_editable != cursor_row:
                        prev_fragments = lines[prev_editable][0]
                        cursor_col = len(get_line_text(prev_fragments))
                        lines[prev_editable][0].extend(line_fragments)
                        lines.pop(cursor_row)
                        cursor_row = prev_editable

            # Suprimir (Delete)
            elif event.key == pygame.K_DELETE:
                if cursor_col < len(line_text):
                    # Eliminar carácter después del cursor
                    if frag_col < len(line_fragments[frag_idx][0]):
                        old_text = line_fragments[frag_idx][0]
                        new_text = old_text[:frag_col] + old_text[frag_col+1:]
                        line_fragments[frag_idx] = (new_text, line_fragments[frag_idx][1])
                    else:
                        # Eliminar del siguiente fragmento
                        if frag_idx + 1 < len(line_fragments):
                            next_text = line_fragments[frag_idx+1][0]
                            if next_text:
                                line_fragments[frag_idx+1] = (next_text[1:], line_fragments[frag_idx+1][1])
                    
                    # Limpiar fragmentos vacíos
                    lines[cursor_row][0] = [(text, color) for text, color in line_fragments if text]
                    if not lines[cursor_row][0]:
                        lines[cursor_row][0] = [("", (255, 255, 255))]
                else:
                    # Unir con siguiente línea
                    next_editable = find_next_editable_line(cursor_row, 1)
                    if next_editable != cursor_row:
                        next_fragments = lines[next_editable][0]
                        lines[cursor_row][0].extend(next_fragments)
                        lines.pop(next_editable)

            # Enter
            elif event.key == pygame.K_RETURN:
                # Dividir fragmento en la posición del cursor
                if frag_col < len(line_fragments[frag_idx][0]):
                    old_text = line_fragments[frag_idx][0]
                    first_part = old_text[:frag_col]
                    second_part = old_text[frag_col:]
                    
                    line_fragments[frag_idx] = (first_part, line_fragments[frag_idx][1])
                    new_fragments = [(second_part, current_color)] + line_fragments[frag_idx+1:]
                else:
                    new_fragments = [("", current_color)]
                
                lines[cursor_row][0] = line_fragments[:frag_idx+1]
                lines.insert(cursor_row+1, [new_fragments, True])
                cursor_row += 1
                cursor_col = 0

            # Tab
            elif event.key == pygame.K_TAB:
                tab_spaces = "    "
                old_text = line_fragments[frag_idx][0]
                new_text = old_text[:frag_col] + tab_spaces + old_text[frag_col:]
                line_fragments[frag_idx] = (new_text, line_fragments[frag_idx][1])
                cursor_col += len(tab_spaces)

            # Pegar del portapapeles
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                try:
                    paste_text = pyperclip.paste()
                    old_text = line_fragments[frag_idx][0]
                    new_text = old_text[:frag_col] + paste_text + old_text[frag_col:]
                    line_fragments[frag_idx] = (new_text, line_fragments[frag_idx][1])
                    cursor_col += len(paste_text)
                except:
                    pass  # Ignorar errores de portapapeles

            # Texto normal
            else:
                char = event.unicode
                if char and char.isprintable() and char not in ["\r", "\n"]:
                    old_text = line_fragments[frag_idx][0]
                    new_text = old_text[:frag_col] + char + old_text[frag_col:]
                    line_fragments[frag_idx] = (new_text, line_fragments[frag_idx][1])
                    cursor_col += 1
                    
                    # Verificar si se completó una palabra de color
                    words = new_text.split()
                    if words:
                        last_word = words[-1]
                        if last_word in COLORS:
                            # Cambiar color del fragmento y eliminar la palabra de color
                            new_color = COLORS[last_word]
                            text_without_color = new_text[:-len(last_word)].rstrip()
                            line_fragments[frag_idx] = (text_without_color, new_color)
                            cursor_col -= len(last_word)
                            if text_without_color and cursor_col > 0:
                                cursor_col -= 1  # Ajustar por el espacio eliminado
                                pygame.display.flip()  
                                clock.tick(60) 
