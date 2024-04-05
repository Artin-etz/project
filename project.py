import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arrow Shooting Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Define player properties
player_width, player_height = 50, 50
player_speed = 5

# Define arrow properties
arrow_width, arrow_height = 10, 5
arrow_speed = 10

# Define obstacle properties
obstacle_width, obstacle_height = 0, 0

# Define player classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
        self.score = 0

    def update(self, keys):
        if self == player1:
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= player_speed
            if keys[pygame.K_s] and self.rect.bottom < height:
                self.rect.y += player_speed
            if keys[pygame.K_a] and self.angle > -90:
                self.angle -= 5
            if keys[pygame.K_d] and self.angle < 90:
                self.angle += 5
        elif self == player2:
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= player_speed
            if keys[pygame.K_DOWN] and self.rect.bottom < height:
                self.rect.y += player_speed
            if keys[pygame.K_LEFT] and self.angle > 90:
                self.angle += 5
            if keys[pygame.K_RIGHT] and self.angle < 270:
                self.angle -= 5

    def shoot(self):
        arrow = Arrow(self.rect.centerx, self.rect.centery, self.angle, self == player1)
        arrows.add(arrow)

# Define arrow class
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, is_player1):
        super().__init__()
        self.image = pygame.Surface((arrow_width, arrow_height))
        self.image.fill(red if is_player1 else blue)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = math.radians(angle)
        self.dx = arrow_speed * math.cos(self.angle)
        self.dy = arrow_speed * math.sin(self.angle)
        self.is_player1 = is_player1

    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.dy

        if self.rect.left > width or self.rect.right < 0 or self.rect.top > height or self.rect.bottom < 0:
            self.kill()

        if pygame.sprite.collide_rect(self, player2 if self.is_player1 else player1):
            player1.score += 1 if self.is_player1 else 0
            player2.score += 1 if not self.is_player1 else 0
            self.kill()

        if pygame.sprite.collide_rect(self, obstacle):
            obstacle.arrow_count += 1
            if obstacle.arrow_count >= 3:
                obstacle.reset()
            self.dx = random.choice([-1, 1]) * arrow_speed
            self.dy = random.choice([-1, 1]) * arrow_speed
# Define obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.arrow_count = 0

    def reset(self):
        self.arrow_count = 0
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

# Create sprite groups
players = pygame.sprite.Group()
arrows = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Create players
player1 = Player(50, height // 2 - player_height // 2, red)
player2 = Player(width - 50 - player_width, height // 2 - player_height // 2, blue)
players.add(player1, player2)

# Create obstacle
obstacle_width = 100
obstacle_height = 100
obstacle_x = width // 2 - obstacle_width // 2
obstacle_y = height // 2 - obstacle_height // 2
obstacle = Obstacle(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
obstacles.add(obstacle)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.shoot()
            elif event.key == pygame.K_RETURN:
                player2.shoot()

    # Update game objects
    keys = pygame.key.get_pressed()
    players.update(keys)
    arrows.update()

    # Draw game objects
    screen.fill(white)
    players.draw(screen)
    arrows.draw(screen)
    obstacles.draw(screen)

    # Draw scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Player 1: {player1.score}  Player 2: {player2.score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()