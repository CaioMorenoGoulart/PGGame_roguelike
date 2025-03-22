import pygame
import math

def generate_corner_curve(p1, p2, radius=50, num_points=20):
    radius = max(0, min(radius, 100)) / 100  # Normaliza entre 0 e 1
    
    # Define os pontos de início e fim da curva
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return [p1, p2]
    
    # Define o raio baseado na distância entre os pontos
    r = dist * radius
    
    # Define o centro do arco
    cx = p1[0] + dx / 2
    cy = p1[1] + dy / 2
    
    # Define o ângulo de início e fim
    start_angle = math.atan2(p1[1] - cy, p1[0] - cx)
    end_angle = math.atan2(p2[1] - cy, p2[0] - cx)
    
    if end_angle < start_angle:
        start_angle, end_angle = end_angle, start_angle
    
    # Gera os pontos do arco
    curve = []
    for t in range(num_points + 1):
        angle = start_angle + (end_angle - start_angle) * (t / num_points)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        curve.append((x, y))
    
    return curve

def draw_rounded_corner(screen, p1, p2, radius=50):
    curve = generate_corner_curve(p1, p2, radius)
    for i in range(len(curve) - 1):
        pygame.draw.line(screen, (255, 255, 255), curve[i], curve[i + 1], 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    
    rect = pygame.Rect(300, 200, 200, 200)
    radius = 100
    
    while running:
        screen.fill((0, 0, 0))
        
        # Define os quatro cantos
        corners = [
            (rect.topleft, rect.midtop),
            (rect.midtop, rect.topright),
            (rect.topright, rect.midright),
            (rect.midright, rect.bottomright),
            (rect.bottomright, rect.midbottom),
            (rect.midbottom, rect.bottomleft),
            (rect.bottomleft, rect.midleft),
            (rect.midleft, rect.topleft),
        ]
        
        for p1, p2 in corners:
            draw_rounded_corner(screen, p1, p2, radius)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
