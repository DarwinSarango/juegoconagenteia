import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Disparos 2D")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Reloj para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Jugador
player_width, player_height = 100, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 50
player_speed = 5

# Proyectiles
projectiles = []
projectile_width, projectile_height = 5, 10
projectile_speed = -7

# Enemigos
enemies = []
enemy_width, enemy_height = 100, 20
enemy_speed = 2

# Puntuación y vidas
score = 0
lives = 3

# Fuente
font = pygame.font.SysFont(None, 36)

# Cargar imágenes
player_image = pygame.image.load('resources/images/aliado.png')
player_image = pygame.transform.scale(player_image, (player_width, player_height))
enemy_image = pygame.image.load('resources/images/enemigo.png')
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

# Cargar sonidos
shoot_sound = pygame.mixer.Sound('resources/sounds/shoot.mp3')
explosion_sound = pygame.mixer.Sound('resources/sounds/explosion.mp3')
game_over_sound = pygame.mixer.Sound('resources/sounds/game_over.mp3')

# Cargar imágenes de fondo y menú
background_image = pygame.image.load('resources/images/fondo.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
menu_image = pygame.image.load('resources/images/menu/menus.png')
menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-100, -40)
    enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

def show_menu():
    menu_running = True
    difficulty = "Normal"
    while menu_running:
        screen.blit(menu_image, (0, 0))
        draw_text("Juego de Disparos 2D", WIDTH // 2 - 150, HEIGHT // 2 - 100, WHITE)
        draw_text("Presiona ENTER para comenzar", WIDTH // 2 - 200, HEIGHT // 2 - 50, WHITE)
        draw_text(f"Dificultad: {difficulty}", WIDTH // 2 - 150, HEIGHT // 2, WHITE)
        draw_text("Usa las flechas izquierda/derecha para cambiar", WIDTH // 2 - 300, HEIGHT // 2 + 50, WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                elif event.key == pygame.K_LEFT:
                    difficulty = "Fácil" if difficulty == "Normal" else "Normal"
                elif event.key == pygame.K_RIGHT:
                    difficulty = "Difícil" if difficulty == "Normal" else "Normal"

    global enemy_speed
    if difficulty == "Fácil":
        enemy_speed = 1
    elif difficulty == "Difícil":
        enemy_speed = 3
    else:
        enemy_speed = 2

def main():
    global player_x, projectiles, enemies, score, lives
    running = True

    show_menu()

    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(projectiles) < 5:
                projectiles.append(pygame.Rect(player_x + player_width // 2, player_y, projectile_width, projectile_height))
                shoot_sound.play()

        for projectile in projectiles[:]:
            projectile.y += projectile_speed
            if projectile.y < 0:
                projectiles.remove(projectile)

        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                if enemy in enemies:
                    enemies.remove(enemy)
                lives -= 1
            for projectile in projectiles[:]:
                if enemy.colliderect(projectile):
                    if enemy in enemies:
                        enemies.remove(enemy)
                    if projectile in projectiles:
                        projectiles.remove(projectile)
                    score += 1
                    explosion_sound.play()

        if random.randint(1, 20) == 1:
            spawn_enemy()

        screen.blit(player_image, (player_x, player_y))

        for projectile in projectiles:
            pygame.draw.rect(screen, GREEN, projectile)

        for enemy in enemies:
            screen.blit(enemy_image, (enemy.x, enemy.y))

        draw_text(f"Puntuación: {score}", 10, 10)
        draw_text(f"Vidas: {lives}", 10, 50)

        if lives <= 0:
            game_over_sound.play()
            draw_text("¡Juego Terminado!", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED)
            draw_text("Presiona ENTER para volver a jugar", WIDTH // 2 - 200, HEIGHT // 2, WHITE)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting = False

            score = 0
            lives = 3
            enemies.clear()
            projectiles.clear()
            continue

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
