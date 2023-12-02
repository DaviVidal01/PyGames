import pygame
import sys
import os

# Inicialização do Pygame
pygame.init()

# Configurações da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Puzzle Game")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Carregando imagens para o parallax
backgrounds = [
    pygame.image.load(os.path.join("assets", "img", "1.png")),
    pygame.image.load(os.path.join("assets", "img", "2.png")),
    pygame.image.load(os.path.join("assets", "img", "3.png")),
    pygame.image.load(os.path.join("assets", "img", "5.png")),
]

# Ajustar o tamanho das imagens para preencher a tela
backgrounds = [pygame.transform.scale(img, (width, height)) for img in backgrounds]

# Definindo a posição inicial para cada camada
background_positions = [0] * len(backgrounds)

# Velocidades de deslocamento para cada camada
background_speeds = [1, 2, 3]  

# Personagem
class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.items = []

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x < width - self.width:
            self.x += self.speed
            # Atualizar a posição das camadas de parallax junto com o personagem
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed

    def collect_item(self, item):
        self.items.append(item)
        print(f"Item collected: {item}")

# Item
class Item:
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.collected = False

    def draw(self, screen):
        pygame.draw.rect(screen, white, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render("E", True, black)
        screen.blit(text, (self.x + self.width // 2 - 10, self.y - 30))

# Porta
class Door:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.locked = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

# Criando instância do jogador
player = Player(50, height - 50, 50, 50)

# Criando instância de itens
items = [Item(200, height - 70, 30, 30, "Key")]

# Criando instância da porta
door = Door(width - 100, height - 70, 50, 70)

# Loop do jogo
clock = pygame.time.Clock()

while True:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            # Verificar interação com itens próximos
            for item in items:
                if (
                    player.x < item.x + item.width
                    and player.x + player.width > item.x
                    and player.y < item.y + item.height
                    and player.y + player.height > item.y
                ):
                    player.collect_item(item.name)
                    items.remove(item)

            # Verificar interação com a porta
            if (
                not door.locked
                and player.x < door.x + door.width
                and player.x + player.width > door.x
                and player.y < door.y + door.height
                and player.y + player.height > door.y
            ):
                print("Congratulations! You entered the door and finished the game.")
                pygame.quit()
                sys.exit()

    # Verificar se alguma camada ultrapassou o limite esquerdo
    for i in range(len(backgrounds)):
        if background_positions[i] <= -width:
            # Reposicionar a camada para a direita
            background_positions[i] += width

    # Desenhar as camadas de parallax
    for i in range(len(backgrounds)):
        screen.blit(backgrounds[i], (background_positions[i], 0))
        screen.blit(backgrounds[i], (background_positions[i] + width, 0))

    # Desenhar itens
    for item in items:
        item.draw(screen)

    # Desenhar a porta
    door.draw(screen)

    # Desenhar Jogador
    player.move()
    pygame.draw.rect(screen, black, (player.x, player.y, player.width, player.height))

    pygame.display.flip()
    clock.tick(30)