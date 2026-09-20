import pygame
import random
import sys

pygame.init()

# ==================================================
# FULL SCREEN
# ==================================================
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
except:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("CAR RUSH - MISSIONS")

clock = pygame.time.Clock()

# ==================================================
# COLORS
# ==================================================
BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
ROAD = (55, 55, 55)
GRASS = (45, 145, 55)

RED = (220, 50, 50)
BLUE = (45, 100, 220)
GREEN = (45, 180, 80)
YELLOW = (240, 200, 40)
CYAN = (30, 200, 220)
PURPLE = (160, 70, 200)

# ==================================================
# FONTS
# ==================================================
font_size = max(24, int(WIDTH * 0.035))
big_size = max(45, int(WIDTH * 0.07))

font = pygame.font.SysFont(None, font_size)
big_font = pygame.font.SysFont(None, big_size)

# ==================================================
# ROAD
# ==================================================
ROAD_LEFT = int(WIDTH * 0.20)
ROAD_RIGHT = int(WIDTH * 0.80)

LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // 3

# ==================================================
# CAR
# ==================================================
CAR_W = int(WIDTH * 0.075)

if CAR_W < 50:
    CAR_W = 50

CAR_H = int(CAR_W * 1.65)

player_y = HEIGHT - CAR_H - int(HEIGHT * 0.12)

player_x = float(WIDTH // 2 - CAR_W // 2)
target_x = player_x

car_color = BLUE

# ==================================================
# GAME DATA
# ==================================================
coins = 0
score = 0
high_score = 0

game_speed = max(5, int(HEIGHT / 100))

enemies = []
enemy_timer = 0
enemy_delay = 65

line_offset = 0

game_over = False
paused = False

# ==================================================
# MENUS
# ==================================================
MENU = 0
GAME = 1
MISSIONS = 2
CARS = 3

screen_mode = MENU

# ==================================================
# MISSION DATA
# ==================================================
mission_distance = 0
mission_coins = 0

mission1_done = False
mission2_done = False
mission3_done = False

# ==================================================
# BUTTON HELPERS
# ==================================================
def make_button(x, y, w, h):
    return pygame.Rect(int(x), int(y), int(w), int(h))


menu_w = int(WIDTH * 0.50)
menu_h = max(60, int(HEIGHT * 0.10))

play_button = make_button(
    WIDTH // 2 - menu_w // 2,
    int(HEIGHT * 0.34),
    menu_w,
    menu_h
)

mission_button = make_button(
    WIDTH // 2 - menu_w // 2,
    int(HEIGHT * 0.47),
    menu_w,
    menu_h
)

cars_button = make_button(
    WIDTH // 2 - menu_w // 2,
    int(HEIGHT * 0.60),
    menu_w,
    menu_h
)

back_button = make_button(
    int(WIDTH * 0.04),
    int(HEIGHT * 0.04),
    int(WIDTH * 0.20),
    max(55, int(HEIGHT * 0.08))
)

button_w = max(130, int(WIDTH * 0.18))
button_h = max(55, int(HEIGHT * 0.10))

left_button = make_button(
    int(WIDTH * 0.04),
    HEIGHT - button_h - int(HEIGHT * 0.04),
    button_w,
    button_h
)

right_button = make_button(
    WIDTH - button_w - int(WIDTH * 0.04),
    HEIGHT - button_h - int(HEIGHT * 0.04),
    button_w,
    button_h
)

restart_button = make_button(
    WIDTH // 2 - menu_w // 2,
    HEIGHT // 2 + 45,
    menu_w,
    menu_h
)

# ==================================================
# DRAW TEXT
# ==================================================
def text_center(txt, y, color=WHITE, fnt=font):

    img = fnt.render(txt, True, color)

    screen.blit(
        img,
        (
            WIDTH // 2 - img.get_width() // 2,
            int(y)
        )
    )


# ==================================================
# DRAW BUTTON
# ==================================================
def draw_button(rect, label, color=(35, 35, 35)):

    pygame.draw.rect(
        screen,
        color,
        rect
    )

    img = font.render(
        label,
        True,
        WHITE
    )

    screen.blit(
        img,
        (
            rect.x + rect.width // 2 - img.get_width() // 2,
            rect.y + rect.height // 2 - img.get_height() // 2
        )
    )


# ==================================================
# DRAW CAR
# ==================================================
def draw_car(x, y, color):

    x = int(x)
    y = int(y)

    # body
    pygame.draw.rect(
        screen,
        color,
        (x, y, CAR_W, CAR_H)
    )

    # roof
    pygame.draw.polygon(
        screen,
        color,
        [
            (x + int(CAR_W * .15), y + int(CAR_H * .32)),
            (x + int(CAR_W * .27), y + int(CAR_H * .10)),
            (x + int(CAR_W * .73), y + int(CAR_H * .10)),
            (x + int(CAR_W * .85), y + int(CAR_H * .32))
        ]
    )

    # windshield
    pygame.draw.polygon(
        screen,
        (80, 180, 220),
        [
            (x + int(CAR_W * .27), y + int(CAR_H * .28)),
            (x + int(CAR_W * .34), y + int(CAR_H * .15)),
            (x + int(CAR_W * .66), y + int(CAR_H * .15)),
            (x + int(CAR_W * .73), y + int(CAR_H * .28))
        ]
    )

    # front glass
    pygame.draw.rect(
        screen,
        (100, 190, 230),
        (
            x + int(CAR_W * .25),
            y + int(CAR_H * .36),
            int(CAR_W * .50),
            int(CAR_H * .17)
        )
    )

    # headlights
    pygame.draw.rect(
        screen,
        YELLOW,
        (
            x + int(CAR_W * .08),
            y + int(CAR_H * .07),
            int(CAR_W * .18),
            int(CAR_H * .10)
        )
    )

    pygame.draw.rect(
        screen,
        YELLOW,
        (
            x + int(CAR_W * .74),
            y + int(CAR_H * .07),
            int(CAR_W * .18),
            int(CAR_H * .10)
        )
    )

    # grill
    pygame.draw.rect(
        screen,
        BLACK,
        (
            x + int(CAR_W * .32),
            y + int(CAR_H * .72),
            int(CAR_W * .36),
            int(CAR_H * .10)
        )
    )

    # wheels
    wheel_w = max(6, int(CAR_W * .15))
    wheel_h = max(18, int(CAR_H * .25))

    positions = [
        (x - wheel_w // 2, y + int(CAR_H * .25)),
        (x + CAR_W - wheel_w // 2, y + int(CAR_H * .25)),
        (x - wheel_w // 2, y + int(CAR_H * .68)),
        (x + CAR_W - wheel_w // 2, y + int(CAR_H * .68))
    ]

    for wx, wy in positions:
        pygame.draw.rect(
            screen,
            BLACK,
            (wx, wy, wheel_w, wheel_h)
        )


# ==================================================
# BACKGROUND
# ==================================================
def draw_background():

    screen.fill(GRASS)

    pygame.draw.rect(
        screen,
        ROAD,
        (
            ROAD_LEFT,
            0,
            ROAD_RIGHT - ROAD_LEFT,
            HEIGHT
        )
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (ROAD_LEFT, 0, 5, HEIGHT)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (ROAD_RIGHT - 5, 0, 5, HEIGHT)
    )

    for lane in range(1, 3):

        x = ROAD_LEFT + lane * LANE_WIDTH
        y = -75 + line_offset

        while y < HEIGHT:

            pygame.draw.rect(
                screen,
                WHITE,
                (x - 3, int(y), 6, 38)
            )

            y += 75


# ==================================================
# CREATE ENEMY
# ==================================================
def create_enemy():

    lane = random.randint(0, 2)

    x = ROAD_LEFT + lane * LANE_WIDTH
    x += (LANE_WIDTH - CAR_W) // 2

    colors = [
        RED,
        YELLOW,
        GREEN,
        CYAN
    ]

    enemies.append([
        float(x),
        float(-CAR_H - 20),
        random.choice(colors)
    ])


# ==================================================
# RESET GAME
# ==================================================
def reset_game():

    global player_x
    global target_x
    global enemies
    global score
    global game_speed
    global enemy_timer
    global line_offset
    global game_over
    global mission_distance
    global mission_coins

    player_x = float(WIDTH // 2 - CAR_W // 2)
    target_x = player_x

    enemies = []

    score = 0
    game_speed = max(5, int(HEIGHT / 100))

    enemy_timer = 0
    line_offset = 0

    mission_distance = 0
    mission_coins = 0

    game_over = False


# ==================================================
# COMPLETE MISSION
# ==================================================
def check_missions():

    global coins
    global mission1_done
    global mission2_done
    global mission3_done

    # Mission 1
    # Score 10
    if score >= 10 and not mission1_done:

        mission1_done = True
        coins += 50

    # Mission 2
    # Score 25
    if score >= 25 and not mission2_done:

        mission2_done = True
        coins += 100

    # Mission 3
    # Collect 10 coins
    if mission_coins >= 10 and not mission3_done:

        mission3_done = True
        coins += 150


# ==================================================
# MAIN MENU
# ==================================================
def draw_menu():

    screen.fill((25, 35, 55))

    text_center(
        "CAR RUSH",
        int(HEIGHT * .12),
        CYAN,
        big_font
    )

    text_center(
        "MISSIONS EDITION",
        int(HEIGHT * .23),
        WHITE,
        font
    )

    draw_button(
        play_button,
        "PLAY GAME",
        BLUE
    )

    draw_button(
        mission_button,
        "MISSIONS",
        (100, 70, 170)
    )

    draw_button(
        cars_button,
        "CARS",
        (170, 100, 60)
    )

    coin_text = font.render(
        "COINS: " + str(coins),
        True,
        YELLOW
    )

    screen.blit(
        coin_text,
        (
            WIDTH // 2 - coin_text.get_width() // 2,
            int(HEIGHT * .76)
        )
    )


# ==================================================
# MISSIONS SCREEN
# ==================================================
def draw_missions():

    screen.fill((25, 35, 55))

    draw_button(
        back_button,
        "BACK"
    )

    text_center(
        "MISSIONS",
        int(HEIGHT * .12),
        YELLOW,
        big_font
    )

    missions = [
        ("Score 10", "Reward: 50 Coins", mission1_done),
        ("Score 25", "Reward: 100 Coins", mission2_done),
        ("Collect 10 Coins", "Reward: 150 Coins", mission3_done)
    ]

    start_y = int(HEIGHT * .30)

    for i in range(3):

        title, reward, done = missions[i]

        box = make_button(
            int(WIDTH * .12),
            start_y + i * int(HEIGHT * .16),
            int(WIDTH * .76),
            int(HEIGHT * .12)
        )

        pygame.draw.rect(
            screen,
            (45, 45, 45),
            box
        )

        t1 = font.render(
            title,
            True,
            WHITE
        )

        t2 = font.render(
            reward,
            True,
            YELLOW
        )

        screen.blit(
            t1,
            (box.x + 20, box.y + 12)
        )

        screen.blit(
            t2,
            (box.x + 20, box.y + 45)
        )

        if done:

            done_text = font.render(
                "DONE",
                True,
                GREEN
            )

            screen.blit(
                done_text,
                (
                    box.right -
                    done_text.get_width() - 20,
                    box.y + 28
                )
            )

    text_center(
        "COINS: " + str(coins),
        int(HEIGHT * .84),
        YELLOW,
        font
    )


# ==================================================
# CAR SCREEN
# ==================================================
def draw_cars():

    screen.fill((25, 35, 55))

    draw_button(
        back_button,
        "BACK"
    )

    text_center(
        "CAR SELECT",
        int(HEIGHT * .12),
        CYAN,
        big_font
    )

    colors = [
        ("BLUE", BLUE),
        ("RED", RED),
        ("GREEN", GREEN),
        ("YELLOW", YELLOW),
        ("PURPLE", PURPLE)
    ]

    start_x = int(WIDTH * .10)
    gap = int(WIDTH * .16)

    for i in range(len(colors)):

        name, color = colors[i]

        cx = start_x + i * gap

        if cx + CAR_W > WIDTH - 20:
            continue

        draw_car(
            cx,
            int(HEIGHT * .32),
            color
        )

        label = font.render(
            name,
            True,
            WHITE
        )

        screen.blit(
            label,
            (
                cx + CAR_W // 2 -
                label.get_width() // 2,
                int(HEIGHT * .57)
            )
        )

    text_center(
        "Tap a car to select",
        int(HEIGHT * .70),
        WHITE,
        font
    )

    text_center(
        "COINS: " + str(coins),
        int(HEIGHT * .82),
        YELLOW,
        font
    )


# ==================================================
# GAME SCREEN
# ==================================================
def draw_game():

    draw_background()

    for enemy in enemies:

        draw_car(
            enemy[0],
            enemy[1],
            enemy[2]
        )

    draw_car(
        player_x,
        player_y,
        car_color
    )

    # score
    s = font.render(
        "Score: " + str(score),
        True,
        WHITE
    )

    screen.blit(
        s,
        (
            int(WIDTH * .03),
            int(HEIGHT * .03)
        )
    )

    # coins
    c = font.render(
        "Coins: " + str(coins),
        True,
        YELLOW
    )

    screen.blit(
        c,
        (
            int(WIDTH * .03),
            int(HEIGHT * .08)
        )
    )

    # buttons
    draw_button(
        left_button,
        "< LEFT"
    )

    draw_button(
        right_button,
        "RIGHT >"
    )

    # game over
    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(180)
        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        text_center(
            "GAME OVER",
            HEIGHT // 2 - 100,
            RED,
            big_font
        )

        text_center(
            "Score: " + str(score),
            HEIGHT // 2 - 30,
            WHITE,
            font
        )

        draw_button(
            restart_button,
            "RESTART",
            BLUE
        )


# ==================================================
# MAIN LOOP
# ==================================================
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            if event.key == pygame.K_p:

                if screen_mode == GAME:
                    paused = not paused

            if event.key == pygame.K_r:

                if screen_mode == GAME and game_over:
                    reset_game()

        # ------------------------------------------
        # TOUCH / MOUSE
        # ------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = event.pos

            # MAIN MENU
            if screen_mode == MENU:

                if play_button.collidepoint(mx, my):

                    reset_game()
                    screen_mode = GAME

                elif mission_button.collidepoint(mx, my):

                    screen_mode = MISSIONS

                elif cars_button.collidepoint(mx, my):

                    screen_mode = CARS

            # MISSIONS
            elif screen_mode == MISSIONS:

                if back_button.collidepoint(mx, my):

                    screen_mode = MENU

            # CARS
            elif screen_mode == CARS:

                if back_button.collidepoint(mx, my):

                    screen_mode = MENU

                else:

                    # Select car by position
                    colors = [
                        BLUE,
                        RED,
                        GREEN,
                        YELLOW,
                        PURPLE
                    ]

                    start_x = int(WIDTH * .10)
                    gap = int(WIDTH * .16)

                    for i in range(len(colors)):

                        cx = start_x + i * gap

                        car_rect = pygame.Rect(
                            cx - 10,
                            int(HEIGHT * .28),
                            CAR_W + 20,
                            int(HEIGHT * .25)
                        )

                        if car_rect.collidepoint(mx, my):

                            car_color = colors[i]

            # GAME
            elif screen_mode == GAME:

                if game_over:

                    if restart_button.collidepoint(mx, my):

                        reset_game()

                elif not paused:

                    # ONE TAP = SMOOTH MOVE
                    if left_button.collidepoint(mx, my):

                        target_x -= LANE_WIDTH

                    elif right_button.collidepoint(mx, my):

                        target_x += LANE_WIDTH

    # ==================================================
    # GAME UPDATE
    # ==================================================
    if screen_mode == GAME and not game_over and not paused:

        # limit target
        min_x = ROAD_LEFT + 10
        max_x = ROAD_RIGHT - CAR_W - 10

        if target_x < min_x:
            target_x = min_x

        if target_x > max_x:
            target_x = max_x

        # smooth steering
        difference = target_x - player_x

        player_x += difference * 0.14

        if abs(difference) < 0.5:

            player_x = target_x

        # road
        line_offset += game_speed

        if line_offset >= 75:

            line_offset = 0

        # enemy spawn
        enemy_timer += 1

        if enemy_timer >= enemy_delay:

            create_enemy()
            enemy_timer = 0

        # enemies
        for enemy in enemies:

            enemy[1] += game_speed

        # remove enemies
        remaining = []

        for enemy in enemies:

            if enemy[1] < HEIGHT + CAR_H:

                remaining.append(enemy)

            else:

                score += 1
                mission_distance += 1

                # small coin reward
                if score % 5 == 0:

                    coins += 5
                    mission_coins += 1

        enemies = remaining

        # speed
        game_speed = max(
            5,
            int(HEIGHT / 100)
        ) + score // 10

        if game_speed > 13:

            game_speed = 13

        # collision
        player_rect = pygame.Rect(
            int(player_x + CAR_W * .12),
            int(player_y + CAR_H * .10),
            int(CAR_W * .76),
            int(CAR_H * .80)
        )

        for enemy in enemies:

            enemy_rect = pygame.Rect(
                int(enemy[0] + CAR_W * .12),
                int(enemy[1] + CAR_H * .10),
                int(CAR_W * .76),
                int(CAR_H * .80)
            )

            if player_rect.colliderect(enemy_rect):

                game_over = True

                if score > high_score:

                    high_score = score

        check_missions()

    # ==================================================
    # DRAW SCREEN
    # ==================================================
    if screen_mode == MENU:

        draw_menu()

    elif screen_mode == GAME:

        draw_game()

    elif screen_mode == MISSIONS:

        draw_missions()

    elif screen_mode == CARS:

        draw_cars()

    pygame.display.flip()

    clock.tick(60)


pyg