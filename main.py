import pygame
import random
import sys

pygame.init()

# Dimensões da tela e cores
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Configurações do jogador
player_speed = 10
player_x_min = 417
player_x_max = 1519
player_y_min = 100
player_y_max = SCREEN_HEIGHT - 10

# Configurações dos carros inimigos
enemy_width = 100
enemy_height = 180
enemy_speed = 6
enemy_x_min = player_x_min
enemy_x_max = player_x_max

# Controle de fases e pontuação
level = 1
score = 0
clock = pygame.time.Clock()

# Configuração de dificuldade
difficulty = "Normal"
difficulty_settings = {
    "Fácil": {
        "enemy_speed": 4,
        "level_up_score": 4
    },
    "Normal": {
        "enemy_speed": 6,
        "level_up_score": 8
    },
    "Difícil": {
        "enemy_speed": 8,
        "level_up_score": 12
    },
}
level_up_score = difficulty_settings[difficulty]["level_up_score"]

# Fonte de texto
font = pygame.font.SysFont(None, 36)

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Overdrive")

# Carrega as imagens
background_image = pygame.image.load("pista.jpg")
background_y = 0
background_speed = 5

player_image = pygame.image.load("carro.png")
player_rect = player_image.get_rect()
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.bottom = SCREEN_HEIGHT - 10

enemy_images = [
    pygame.image.load("inimigo.png"),
    pygame.image.load("inimigo2.png"),
]


def show_menu():
    global difficulty, enemy_speed, level_up_score

    screen.fill(WHITE)
    title_text = font.render("Overdrive", True, BLACK)
    prompt_text = font.render("Pressione Enter para continuar", True, BLUE)
    objective_text = font.render(
        "Objetivo: Ultrapasse o maior número de carros sem causar acidentes",
        True, RED)

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                             SCREEN_HEIGHT // 2 - 150))
    screen.blit(objective_text,
                (SCREEN_WIDTH // 2 - objective_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 - 50))
    screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

    difficulties = ["Fácil", "Normal", "Difícil"]
    selected_option = difficulties.index(difficulty)

    while True:
        screen.fill(WHITE)
        difficulty_title = font.render("Selecione a Dificuldade", True, BLACK)
        screen.blit(difficulty_title,
                    (SCREEN_WIDTH // 2 - difficulty_title.get_width() // 2,
                     SCREEN_HEIGHT // 2 - 150))

        for i, diff in enumerate(difficulties):
            color = RED if i == selected_option else BLACK
            difficulty_text = font.render(diff, True, color)
            screen.blit(
                difficulty_text,
                (SCREEN_WIDTH // 2 - difficulty_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 + i * 50),
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    difficulty = difficulties[selected_option]
                    enemy_speed = difficulty_settings[difficulty][
                        "enemy_speed"]
                    level_up_score = difficulty_settings[difficulty][
                        "level_up_score"]
                    return


def show_score():
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    difficulty_text = font.render(f"Dificuldade: {difficulty}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(difficulty_text, (10, 50))


def create_enemies():
    enemies = []
    positions = []

    while len(positions) < 5:
        x = random.randint(enemy_x_min, enemy_x_max - enemy_width)
        y = random.randint(-SCREEN_HEIGHT, -enemy_height)

        overlap = any(
            abs(x - pos[0]) < enemy_width +
            7 and abs(y - pos[1]) < enemy_height + 7 for pos in positions)
        if not overlap:
            positions.append((x, y))

    for x, y in positions:
        enemy_rect = pygame.Rect(x, y, enemy_width, enemy_height)
        enemy_image = random.choice(enemy_images)
        enemies.append({"rect": enemy_rect, "image": enemy_image})

    return enemies


def main_game():
    global enemy_speed, level, score, background_y

    enemies = create_enemies()

    # Inicialize a pontuação e o nível ao começar o jogo
    score = 0
    level = 1
    background_y = 0

    running = True
    while running:
        background_y += background_speed
        if background_y >= SCREEN_HEIGHT:
            background_y = 0

        screen.blit(background_image, (0, background_y))
        screen.blit(background_image, (0, background_y - SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_rect.left > player_x_min:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < player_x_max:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > player_y_min:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < player_y_max:
            player_rect.y += player_speed

        for enemy in enemies:
            enemy["rect"].y += enemy_speed
            if enemy["rect"].y > SCREEN_HEIGHT:
                enemy["rect"].y = random.randint(-SCREEN_HEIGHT, -enemy_height)
                enemy["rect"].x = random.randint(enemy_x_min,
                                                 enemy_x_max - enemy_width)
                score += 1

                if score % level_up_score == 0:
                    level += 1
                    enemy_speed += 1

        # Verifica colisão com os inimigos
        for enemy in enemies:
            if player_rect.colliderect(enemy["rect"]):
                running = False  # O jogador morre, reiniciando o jogo

        screen.blit(player_image, player_rect)
        for enemy in enemies:
            screen.blit(enemy["image"], enemy["rect"])

        show_score()

        pygame.display.flip()
        clock.tick(30)


show_menu()
while True:
    main_game()
    show_menu()