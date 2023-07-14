def draw_text(font, text, surface, x, y, scale, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    width, height = font.size(text)
    x = x * scale - width / 2
    y = y * scale - height / 2
    surface.blit(surf, (x, y))
