import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 15

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)

# Load sound effects
eat_sound = pygame.mixer.Sound("./sounds/eat.mp3")    
game_over_sound = pygame.mixer.Sound("./sounds/game_over.mp3")  

# Load background music
pygame.mixer.music.load("./sounds/bg.mp3")  
pygame.mixer.music.set_volume(0.3)

mute_sound = False  # Variable to track the mute state

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([0, 1, 2, 3])
        self.color = GREEN
        self.score = 0
        self.high_score = self.read_high_score()

    def move(self):
        cur = self.positions[0]
        x, y = cur

        if self.direction == 0:
            y -= GRID_SIZE
        elif self.direction == 1:
            x += GRID_SIZE
        elif self.direction == 2:
            y += GRID_SIZE
        elif self.direction == 3:
            x -= GRID_SIZE

        self.positions.insert(0, (x, y))

        if len(self.positions) > self.length:
            self.positions.pop()

    def change_direction(self, new_direction):
        if new_direction == self.direction or new_direction % 2 == self.direction % 2:
            return
        self.direction = new_direction

    def grow(self):
        self.length += 1
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        # Play eat sound if not muted
        if not mute_sound:
            eat_sound.play()

    def check_collision(self):
        x, y = self.positions[0]
        if (
            x < 0
            or x >= WIDTH
            or y < 0
            or y >= HEIGHT
            or self.positions[0] in self.positions[1:]
        ):
            return True
        return False

    def eats(self, food):
        return self.positions[0] == food.position

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.circle(surface, self.color, (p[0] + GRID_SIZE // 2, p[1] + GRID_SIZE // 2), GRID_SIZE // 2)
            pygame.draw.circle(surface, BLACK, (p[0] + GRID_SIZE // 2, p[1] + GRID_SIZE // 2), GRID_SIZE // 2, 2)

    def read_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.respawn()

    def respawn(self):
        self.position = (
            random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
            random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
        )

    def draw(self, surface):
        food_rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.ellipse(surface, self.color, food_rect)
        pygame.draw.ellipse(surface, BLACK, food_rect, 2)

def draw_text(surface, text, size, x, y, color, align="center"):  
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == "center":
        text_rect.center = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
    elif align == "bottomleft":
        text_rect.bottomleft = (x, y)

    surface.blit(text_surface, text_rect)

def start_menu(window):
    global mute_sound  
    window.fill(GRAY)
    draw_text(window, "Snake Game", 60, WIDTH // 2, HEIGHT // 4, WHITE)
    draw_text(window, "Press Enter to Play", 30, WIDTH // 2, HEIGHT // 2 - 30, WHITE)
    draw_text(window, "Press Q to Quit", 20, WIDTH // 2, HEIGHT // 2 + 30, WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m:  # Toggle mute state on 'M' key press
                    mute_sound = not mute_sound
                    if mute_sound:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

def speed_menu(window):
    window.fill(GRAY)
    draw_text(window, "Select Speed", 50, WIDTH // 2, HEIGHT // 4, WHITE)
    draw_text(window, "1 - Slow", 30, WIDTH // 2, HEIGHT // 2 - 30, WHITE)
    draw_text(window, "2 - Medium", 30, WIDTH // 2, HEIGHT // 2, WHITE)
    draw_text(window, "3 - Fast", 30, WIDTH // 2, HEIGHT // 2 + 30, WHITE)
    draw_text(window, "Press Q to Quit", 20, WIDTH // 2, HEIGHT - 50, WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 8
                elif event.key == pygame.K_2:
                    return 15
                elif event.key == pygame.K_3:
                    return 25
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_over_menu(window, snake):
    window.fill(GRAY)
    draw_text(window, "Game Over", 60, WIDTH // 2, HEIGHT // 4, RED)
    draw_text(window, "Press Enter to Play Again", 30, WIDTH // 2, HEIGHT // 2 - 30, WHITE)
    draw_text(window, "Press Q to Quit", 20, WIDTH // 2, HEIGHT // 2, WHITE)
    draw_text(window, f"Score: {snake.score}", 30, WIDTH // 2, HEIGHT // 2 + 30, WHITE)
    draw_text(window, f"High Score: {snake.high_score}", 30, WIDTH // 2, HEIGHT // 2 + 60, WHITE)
    pygame.display.update()

    # Play game over sound if not muted
    if not mute_sound:
        game_over_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop():
    global mute_sound  
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Play background music in a loop
    pygame.mixer.music.play(-1)

    while True:
        start_menu(window)
        
        snake = Snake()
        food = Food()
        game_over = False

        speed = speed_menu(window)

        mute_sound = False  # Reset mute state at the beginning of each game

        while not game_over:
            clock.tick(speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if game_over and event.key == pygame.K_RETURN:
                        snake = Snake()
                        food = Food()
                        game_over = False
                    elif not game_over:
                        if event.key == pygame.K_UP:
                            snake.change_direction(0)
                        elif event.key == pygame.K_RIGHT:
                            snake.change_direction(1)
                        elif event.key == pygame.K_DOWN:
                            snake.change_direction(2)
                        elif event.key == pygame.K_LEFT:
                            snake.change_direction(3)
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_m:  # Toggle mute state on 'M' key press
                            mute_sound = not mute_sound
                            if mute_sound:
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()

            snake.move()

            if snake.check_collision():
                game_over_menu(window, snake)
                game_over = True

            if snake.eats(food):
                snake.grow()
                food.respawn()

            window.fill(GRAY)
            snake.draw(window)
            food.draw(window)

            draw_text(window, f"Score: {snake.score}", 30, WIDTH // 2, 20, WHITE)
            draw_text(window, f"High Score: {snake.high_score}", 30, WIDTH // 2, 50, WHITE)

            # Display mute/unmute status in bottom-left corner
            mute_text = "Press M to unmute" if mute_sound else "Press M to mute"
            draw_text(window, f"Sound: {mute_text}", 20, 20, HEIGHT - 20, WHITE, align="bottomleft")

            pygame.display.update()

if __name__ == "__main__":
    game_loop()