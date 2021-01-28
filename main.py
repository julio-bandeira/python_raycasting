import pygame
import math
import ctypes

pygame.init()


user32 = ctypes.windll.user32
window_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

game_size = [320, 200] #window_size (640, 400) or (320,200) #resolution 

window = pygame.display.set_mode(window_size, pygame.FULLSCREEN)
display = pygame.Surface(game_size)

clock = pygame.time.Clock()

# Mapa 10x10
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

opened = True

camera_pos = pygame.math.Vector2(x=5, y=5)
camera_dir = pygame.math.Vector2(x=0, y=-1)
camera_plane = pygame.math.Vector2(x=0.66, y=0)


def render_draw():
    """
    Função responsavel por renderizar todos os objeto dentro do game
    """
    display.fill((190, 190, 255))
    pygame.draw.rect(display, (130, 130, 130), (0, game_size[1]/2, game_size[0], game_size[1]/2))

    for pixel in range(0, game_size[0]):
        multiplier = 2*(pixel/game_size[0])-1
        camera_pixel = camera_plane*multiplier

        ray_dir = camera_dir + camera_pixel


        if ray_dir.x == 0:
            delta_dist_x = 1
            delta_dist_y = 0
        else:
            if ray_dir.y != 0:
                delta_dist_x = abs(1/ray_dir.x)

        if ray_dir.y == 0:
            delta_dist_x = 0
            delta_dist_y = 1
        else:
            if ray_dir.x != 0:
                delta_dist_y = abs(1/ray_dir.y)

        map_pos = pygame.math.Vector2(int(math.floor(camera_pos.x)), int(math.floor(camera_pos.y)))
        
        if ray_dir.x < 0:
            dist_to_side_x = (camera_pos.x - map_pos.x) * delta_dist_x
            step_x = -1
        else:
            dist_to_side_x = (map_pos.x + 1 - camera_pos.x) * delta_dist_x
            step_x = 1
        if ray_dir.y < 0:
            dist_to_side_y = (camera_pos.y - map_pos.y) * delta_dist_y
            step_y = -1
        else:
            dist_to_side_y = (map_pos.y + 1 - camera_pos.y) * delta_dist_y
            step_y = 1

        hit = False

        dda_line_size_x = dist_to_side_x
        dda_line_size_y = dist_to_side_y
        wall_map_pos = pygame.math.Vector2(map_pos.x, map_pos.y)

        while hit == False:
            if dda_line_size_x < dda_line_size_y:
                wall_map_pos.x += step_x
                dda_line_size_x += delta_dist_x
                hit_side = 0
            else:
                wall_map_pos.y += step_y
                dda_line_size_y += delta_dist_y
                hit_side = 1
            
            if (game_map[int(wall_map_pos.x)][int(wall_map_pos.y)]) > 0:
                hit = True

        if hit_side == 0:
            perpendicular_dist = abs((wall_map_pos.x - camera_pos.x + ((1-step_x)/2))/ray_dir.x)
        else:
            perpendicular_dist = abs((wall_map_pos.y - camera_pos.y + ((1-step_y)/2))/ray_dir.y)

        wall_line_height = game_size[1]/perpendicular_dist

        line_start_y = (game_size[1]/2) - (wall_line_height/2)
        line_end_y = (game_size[1]/2) +  (wall_line_height/2)

        if hit_side == 0:
            pygame.draw.line(display, (128,0,0), (pixel, line_start_y), (pixel, line_end_y))
        else:
            pygame.draw.line(display, (255,0,0), (pixel, line_start_y), (pixel, line_end_y))
        
    window.blit(pygame.transform.smoothscale(display, window_size), (0, 0))
    pygame.display.update()


while opened:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            opened = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        opened = False
    if keys[pygame.K_UP]:
        camera_pos += camera_dir*0.05
    if keys[pygame.K_DOWN]:
        camera_pos -= camera_dir*0.05
    if keys[pygame.K_LEFT]:
        camera_dir.rotate_ip(-1.5)
        camera_plane.rotate_ip(-1.5)
    if keys[pygame.K_RIGHT]:
        camera_dir.rotate_ip(1.5)
        camera_plane.rotate_ip(1.5)

    render_draw()
    clock.tick(60)

pygame.quit()