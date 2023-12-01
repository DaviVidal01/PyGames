import pygame
import sys
import os
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("IconBros!")

# Cores
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0,0,0)

# Carregando imagens para o parallax
backgrounds = [
    pygame.image.load(os.path.join("assets", "img", "5.png")),
    pygame.image.load(os.path.join("assets", "img", "4.png")),
    pygame.image.load(os.path.join("assets", "img", "3.png")),
    pygame.image.load(os.path.join("assets", "img", "2.png")),
    pygame.image.load(os.path.join("assets", "img", "1.png")),
]

# Ajustar o tamanho das imagens para preencher a tela
backgrounds = [pygame.transform.scale(img, (width, height)) for img in backgrounds]

# Definindo a posição inicial para cada camada
background_positions = [0, 0, 0, 0, 0]

# Velocidades de deslocamento para cada camada
background_speeds = [1, 2, 3, 4, 5]

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.jump = False
        self.jump_count = 10
        self.gravity = 9
        self.image = pygame.image.load(os.path.join("assets", "img", "personagem.jpg"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def push_npc(self, npc):
        # Define a força de empurrar NPCs
        push_force = 20

        # Calcula a direção do empurrão com base na posição relativa do NPC em relação ao jogador
        direction_x = npc.x - self.x
        direction_y = npc.y - self.y
        distance = max(1, (direction_x**2 + direction_y**2)**0.5)  # Evita divisão por zero

        # Normaliza a direção
        direction_x /= distance
        direction_y /= distance

        # Aplica a força ao NPC
        npc.x += push_force * direction_x
        npc.y += push_force * direction_y

    def jump_logic(self):
        if not self.jump:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.jump = True
        else:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10

    def apply_gravity(self):
        if self.y < height - self.height:
            self.y += self.gravity
        elif self.jump_count < 10:
            self.y -= (self.jump_count ** 2) * 0.5
            self.jump_count -= 2
        else:
            self.y = height - self.height

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x < width - self.width:
            self.x += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# NPC
class NPC:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = random.randint(3, 5)
        self.jump = False
        self.jump_count = 10
        self.gravity = 9
        self.image = pygame.image.load(os.path.join("assets", "img", "npc.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def jump_logic(self):
        if not self.jump and random.randint(0, 100) < 1:  # Adiciona aleatoriedade ao pulo
            self.jump = True

    def apply_gravity(self):
        if self.y < height - self.height:
            self.y += self.gravity
        elif self.jump_count < 10:
            self.y -= (self.jump_count ** 2) * 0.5
            self.jump_count -= 2
        else:
            self.y = height - self.height

    def move(self):
        self.x += self.speed
        if self.x > width:
            self.x = 0
            self.y = random.randint(50, height - self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Plataformas
platforms = [
    pygame.Rect(0, height - 20, width, 20),           # Chão
    pygame.Rect(200, height - 120, 150, 20),          # Plataforma simples
    pygame.Rect(400, height - 220, 100, 20),          # Plataforma móvel
    pygame.Rect(600, height - 320, 120, 20),          # Plataforma voadora
]

platform_speed = 2
moving_platform_direction = 1

# Criando instâncias do jogador e NPCs
player = Player(50, height - 50, 50, 50)
npcs = [NPC(random.randint(0, width), random.randint(50, height - 50), 50, 50) for _ in range(3)]

# Loop do jogo
clock = pygame.time.Clock()

while True:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Verificar entrada de teclado
    keys = pygame.key.get_pressed()

    # Verifica se a tecla "espaço" ou "seta para cima" foi pressionada
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        # Certifica-se de que o jogador está no chão antes de permitir um novo pulo
        if not player.jump:
            player.jump = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        # Para cada NPC, empurra o NPC se estiver próximo ao jogador
        for npc in npcs:
            distance_to_npc = ((player.x - npc.x)**2 + (player.y - npc.y)**2)**0.5
            if distance_to_npc < 100:  # Ajuste o valor conforme necessário
                player.push_npc(npc)

    # Atualizar a posição das camadas de parallax junto com o jogador
    for i in range(len(backgrounds)):
        background_positions[i] -= background_speeds[i]
        if background_positions[i] < -width:
            background_positions[i] = 0

    # Atualizar jogador
    player.jump_logic()
    player.apply_gravity()
    player.move()

    # Atualizar NPCs
    for npc in npcs:
        npc.jump_logic()
        npc.apply_gravity()
        npc.move()

    # Atualizar a posição da plataforma móvel
    platforms[2].x += platform_speed * moving_platform_direction
    if platforms[2].x <= 0 or platforms[2].x >= width - 100:
        moving_platform_direction *= -1

    # Verificar colisões do jogador com as plataformas
    for platform in platforms:
        if platform.colliderect((player.x, player.y, player.width, player.height)):
            player.y = platform.y - player.height
            player.jump_count = 10  # Reinicia o contador de pulo

    # Verificar colisões dos NPCs com as plataformas
    for npc in npcs:
        for platform in platforms:
            if platform.colliderect((npc.x, npc.y, npc.width, npc.height)):
                npc.y = platform.y - npc.height
                npc.jump_count = 10  # Reinicia o contador de pulo

    # Desenhar as camadas de parallax
    for i in range(len(backgrounds)):
        screen.blit(backgrounds[i], (background_positions[i], 0))
        screen.blit(backgrounds[i], (background_positions[i] + width, 0))

    # Desenhar plataformas
    for platform in platforms:
        pygame.draw.rect(screen, black, platform)

    # Desenhar Jogador
    player.draw(screen)

    # Desenhar NPCs
    for npc in npcs:
        npc.draw(screen)

    pygame.display.flip()
    clock.tick(30)