import sys
sys.path.insert(0, 'package/')

import os, pygame, sys, time, random, copy
from recordtype import recordtype

os.environ['SDL_AUDIODRIVER'] = 'dsp'

Position = recordtype('Position', ['x', 'y'])

BLACK = (0, 0, 0)
FPS = 120
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SCORE_COLOR = (255, 255, 255)
SCORE_HEIGHT = 50

JUMP_HEIGHT = 8
GRAVITY = 0.3

COLUMN_SPACE = 175
COLUMN_WIDTH = 52
COLUMN_BUFFER = 400

CLICK_MESSAGE_COLOR = (255, 128, 0)

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont("monospace", 20)
bg_img = pygame.transform.scale(pygame.image.load("resources/bg.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
bird_up_img = pygame.image.load("resources/bird_up.png").convert()
bird_normal_img = pygame.image.load("resources/bird_normal.png").convert()
bird_down_img = pygame.image.load("resources/bird_down.png").convert()
column_img = pygame.image.load("resources/column.png").convert()
clock = pygame.time.Clock()

def drawScore(columns_passed):
    text = f"Score: {len(columns_passed)}"
    label = font.render(text, True, SCORE_COLOR)
    window.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, SCORE_HEIGHT))

def drawBird(bird):
    global bird_img
    window.blit(bird_img, bird.center)

    if bird_img == bird_up_img:
        bird_img = bird_down_img
    elif bird_img == bird_down_img:
        bird_img = bird_normal_img

def generateInitialColumns():
    x = 800
    y1 = 0
    h1_col1 = random.randint(100, 325)
    y2_col1 = h1_col1 + COLUMN_SPACE
    h2_col1 = SCREEN_HEIGHT - y2_col1

    h1_col2 = random.randint(100, 325)
    y2_col2 = h1_col2 + COLUMN_SPACE
    h2_col2 = SCREEN_HEIGHT - y2_col2

    column1_img1 = pygame.transform.rotate(pygame.transform.scale(column_img, (COLUMN_WIDTH, h1_col1)), 180)
    column1_rect1 = column1_img1.get_rect()
    column1_rect1.topleft = (x, y1)

    column1_img2 = pygame.transform.scale(column_img, (COLUMN_WIDTH, h2_col1))
    column1_rect2 = column1_img2.get_rect()
    column1_rect2.topleft = (x, y2_col1)

    column2_img1 = pygame.transform.rotate(pygame.transform.scale(column_img, (COLUMN_WIDTH, h1_col2)), 180)
    column2_rect1 = column2_img1.get_rect()
    column2_rect1.topleft = (x + COLUMN_BUFFER, y1)

    column2_img2 = pygame.transform.scale(column_img, (COLUMN_WIDTH, h2_col2))
    column2_rect2 = column2_img2.get_rect()
    column2_rect2.topleft = (x + COLUMN_BUFFER, y2_col2)

    return [{"column1": (column1_img1, column1_rect1), "column2": (column1_img2, column1_rect2)},
        {"column1": (column2_img1, column2_rect1), "column2": (column2_img2, column2_rect2)}]

def generateColumn():
    x = 800
    y1 = 0
    h1 = random.randint(100, 325)
    y2 = h1 + COLUMN_SPACE
    h2 = SCREEN_HEIGHT - y2

    column_img1 = pygame.transform.rotate(pygame.transform.scale(column_img, (COLUMN_WIDTH, h1)), 180)
    column_rect1 = column_img1.get_rect()
    column_rect1.topleft = (x, y1)

    column_img2 = pygame.transform.scale(column_img, (COLUMN_WIDTH, h2))
    column_rect2 = column_img2.get_rect()
    column_rect2.topleft = (x, y2)

    return [{"column1": (column_img1, column_rect1), "column2": (column_img2, column_rect2)}]

def drawColumn(columns):
    for column in columns:
        column["column1"][1].centerx -= 1
        column["column2"][1].centerx -= 1
        window.blit(column["column1"][0], column["column1"][1].topleft)
        window.blit(column["column2"][0], column["column2"][1].topleft)

def checkCollision(bird, columns):
    bird_hitbox = copy.deepcopy(bird)
    bird_hitbox.centerx += 15
    bird_hitbox.centery += 10
    for column in columns:
        if bird_hitbox.colliderect(column["column1"][1]) or bird_hitbox.colliderect(column["column2"][1]):
            return True

    return False

def drawGameOver(score):
    font = pygame.font.SysFont("monospace", 50)
    text = f"Score: {score}"
    label = font.render(text, False, SCORE_COLOR)
    window.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, (SCREEN_HEIGHT - label.get_height()) / 2))

    font = pygame.font.SysFont("monospace", 20, True)
    message = "Click to continue..."
    label = font.render(message, False, CLICK_MESSAGE_COLOR)
    window.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, SCREEN_HEIGHT - 100))

def start():
    while True:
        global movement, bird_img
        window.fill(BLACK)
        window.blit(bg_img, (0, 0))
        drawBird(bird)
        drawScore(columns_passed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    movement -= JUMP_HEIGHT
                    bird_img = bird_up_img
                    return

        pygame.display.update()
        clock.tick(FPS)

def game():
    global bird, columns_passed, movement, bird_img
    columns = generateInitialColumns()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    movement = 0
                    movement -= JUMP_HEIGHT
                    bird_img = bird_up_img

        movement += GRAVITY
        bird.centery += movement

        window.fill(BLACK)
        window.blit(bg_img, (0, 0))
        drawBird(bird)
        drawColumn(columns)
        drawScore(columns_passed)
        pygame.display.update()
        clock.tick(FPS)

        if bird.topleft[1] <= 0 or bird.bottomleft[1] >= SCREEN_HEIGHT or checkCollision(bird, columns):
            time.sleep(1)
            return

        elif columns[0]["column1"][1].topright[0] < 0:
            columns.pop(0)
            columns.extend(generateColumn())

        elif columns[0] not in columns_passed and bird.bottomleft[0] > columns[0]["column1"][1].topright[0]:
            columns_passed.append(columns[0])

def gameOver():
    global columns_passed
    while True:
        window.fill(BLACK)
        drawGameOver(len(columns_passed))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or event.type == pygame.KEYDOWN:
                return

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        bird_img = bird_normal_img
        bird = bird_img.get_rect()
        bird.centerx = SCREEN_WIDTH * 0.3
        bird.centery = SCREEN_HEIGHT / 2
        columns_passed = []
        movement = 0
        start()
        game()
        gameOver()
