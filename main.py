import pygame
import random
import sys

# Inicializa o pygame e define algumas constantes
pygame.init()

# Dimensões da tela e cores
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configurações do jogador
player_speed = 10
player_x_min = 229  # Limite mínimo de posição x do jogador
player_x_max = 510  # Limite máximo de posição x do jogador
player_y_min = 100  # Limite superior (frente) para o movimento do jogador
player_y_max = SCREEN_HEIGHT - 10  # Limite inferior (parte de trás da tela)

# Configurações dos carros inimigos
enemy_width = 100
enemy_height = 74
enemy_speed = 5
enemy_x_min = 229  # Limite mínimo de posição x dos obstáculos
enemy_x_max = 510  # Limite máximo de posição x dos obstáculos

# Controle de fases e pontuação
level = 1
score = 0
clock = pygame.time.Clock()

# Fonte de texto
font = pygame.font.SysFont(None, 36)

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Corrida")

# Carrega a imagem de fundo e do carro do jogador
background_image = pygame.image.load("pista.png")
player_image = pygame.image.load("carro.png")
player_rect = player_image.get_rect()  # Retângulo da imagem do jogador
player_rect.centerx = SCREEN_WIDTH // 2  # Posição inicial do jogador no centro
player_rect.bottom = SCREEN_HEIGHT - 10  # Posição inicial do jogador próximo à parte inferior


# Função para mostrar o menu
def show_menu():
    screen.fill(WHITE)
    title_text = font.render("Jogo de Corrida - Pressione Enter para Iniciar",
                             True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                             SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()

    # Espera pelo pressionamento de uma tecla
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


# Função para mostrar a pontuação e nível
def show_score_level():
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    level_text = font.render(f"Nível: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))


# Função para criar uma nova lista de inimigos, garantindo um espaço seguro
def create_enemies():
    enemies = []
    positions = list(
        range(enemy_x_min, enemy_x_max - enemy_width,
              enemy_width + 20))  # Intervalo maior para evitar sobreposição
    random.shuffle(positions)

    # Deixa um espaço para o jogador passar
    safe_spot = random.choice(positions)
    for pos_x in positions:
        if pos_x != safe_spot:
            y = random.randint(-SCREEN_HEIGHT, -enemy_height)
            enemy_rect = pygame.Rect(pos_x, y, enemy_width, enemy_height)
            enemies.append(enemy_rect)

    return enemies


# Função para exibir o menu de pausa
def pause_menu():
    paused = True
    selected_option = 0  # Opção selecionada: 0=Retomar, 1=Reiniciar, 2=Voltar ao Menu
    options = ["Retomar", "Reiniciar", "Voltar ao Menu"]

    while paused:
        screen.fill(WHITE)

        # Desenha o menu de pausa
        pause_text = font.render("PAUSADO", True, BLACK)
        screen.blit(pause_text,
                    (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 150))

        for i, option in enumerate(options):
            color = RED if i == selected_option else BLACK
            option_text = font.render(option, True, color)
            screen.blit(option_text,
                        (SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                         250 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Retomar
                        paused = False
                    elif selected_option == 1:  # Reiniciar
                        main_game()
                    elif selected_option == 2:  # Voltar ao Menu
                        show_menu()
                        return


# Função principal do jogo
def main_game():
    global enemy_speed, level, score

    # Cria os inimigos inicialmente
    enemies = create_enemies()

    # Loop principal do jogo
    running = True
    while running:
        # Desenha o fundo
        screen.blit(background_image, (0, 0))

        # Eventos de controle do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()  # Abre o menu de pausa

        # Controle do personagem (direcional do teclado)
        keys = pygame.key.get_pressed()

        # Movimento horizontal com limites
        if keys[pygame.K_LEFT] and player_rect.left > player_x_min:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < player_x_max:
            player_rect.x += player_speed

        # Movimento vertical com limites
        if keys[pygame.K_UP] and player_rect.top > player_y_min:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < player_y_max:
            player_rect.y += player_speed

        # Atualiza posição dos carros inimigos
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > SCREEN_HEIGHT:
                # Reposiciona o inimigo no topo, garantindo espaço livre
                enemies = create_enemies()
                score += 1

                # Aumenta a velocidade e nível a cada 10 pontos
                if score % 10 == 0:
                    level += 1
                    enemy_speed += 1

        # Checa colisão com o jogador
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                running = False  # Encerra o jogo em caso de colisão

        # Desenha o jogador usando a imagem e os inimigos como retângulos vermelhos
        screen.blit(player_image, player_rect)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Mostra a pontuação e o nível
        show_score_level()

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)


# Mostra o menu e inicia o jogo
show_menu()
while True:
    main_game()
    show_menu()  # Volta para o menu ao perder
