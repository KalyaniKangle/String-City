import pygame
import sys

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 1100
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STRING CITY - Python String Adventure")

clock = pygame.time.Clock()

# ============================================================
# COLORS
# ============================================================

BG = (25, 18, 45)
PANEL = (43, 31, 70)
PANEL_LIGHT = (57, 42, 88)

PURPLE = (145, 95, 220)
LIGHT_PURPLE = (190, 145, 255)

WHITE = (245, 245, 250)
GRAY = (175, 170, 190)

GREEN = (80, 210, 130)
RED = (230, 85, 100)
YELLOW = (245, 205, 80)

DARK = (18, 13, 32)

# ============================================================
# FONTS
# ============================================================

TITLE_FONT = pygame.font.Font(None, 64)
BIG_FONT = pygame.font.Font(None, 45)
FONT = pygame.font.Font(None, 30)
SMALL_FONT = pygame.font.Font(None, 24)

# ============================================================
# GAME VARIABLES
# ============================================================

current_screen = "city"

selected_challenge = None

xp = 0
lives = 5

input_text = ""

feedback = ""
feedback_color = WHITE

challenge_index = 0
hint_used = False

boss_index = 0

completed = {
    "Character Hunt": False,
    "Password Gate": False,
    "Search Quest": False,
    "Slice Street": False
}

# ============================================================
# CHALLENGES
# ============================================================

character_questions = [
    ("PYTHON", 1, "What character is at index 1?"),
    ("PYTHON", 4, "What character is at index 4?"),
    ("CODING", 2, "What character is at index 2?"),
    ("PYTHON", 5, "What character is at index 5?")
]

password_questions = [
    ("PYTHON", [0, 2, 5]),
    ("CODING", [1, 3, 5]),
    ("COMPUTER", [0, 3, 6]),
    ("PROGRAM", [1, 4, 6])
]

search_questions = [
    ("PYTHON", "P", True),
    ("PYTHON", "Z", False),
    ("I LOVE CODING", "CODE", True),
    ("PYTHON PROGRAMMING", "JAVA", False)
]

slice_questions = [
    ("PYTHON", 0, 3),
    ("PYTHON", 2, 5),
    ("CODING", 1, 4),
    ("PROGRAM", 3, 7)
]

boss_questions = [
    ("index", "PYTHON", 1, "Y"),
    ("in", "PYTHON", "T", "YES"),
    ("slice", "PYTHON", 2, 5, "THO"),
    ("in", "PYTHON PROGRAMMING", "JAVA", "NO"),
    ("slice", "CODING", 0, 3, "COD")
]

# ============================================================
# FUNCTIONS
# ============================================================

def draw_text(text, x, y, font=FONT, color=WHITE):
    image = font.render(str(text), True, color)
    screen.blit(image, (x, y))


def draw_center_text(text, x, y, font=FONT, color=WHITE):
    image = font.render(str(text), True, color)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)


def draw_wrapped_text(text, x, y, width, font=SMALL_FONT, color=GRAY):
    words = text.split()
    line = ""
    line_y = y

    for word in words:
        test_line = line + word + " "

        if font.size(test_line)[0] <= width:
            line = test_line
        else:
            draw_text(line, x, line_y, font, color)
            line = word + " "
            line_y += font.get_height() + 4

    if line:
        draw_text(line, x, line_y, font, color)

    return line_y + font.get_height()


def draw_button(rect, text, active=False):
    if active:
        pygame.draw.rect(screen, LIGHT_PURPLE, rect, border_radius=12)
        text_color = DARK
    else:
        pygame.draw.rect(screen, PANEL_LIGHT, rect, border_radius=12)
        text_color = WHITE

    pygame.draw.rect(screen, PURPLE, rect, 2, border_radius=12)

    draw_center_text(
        text,
        rect.centerx,
        rect.centery,
        FONT,
        text_color
    )


def draw_city_background():
    screen.fill(BG)

    # Moon
    pygame.draw.circle(screen, (235, 220, 170), (930, 100), 45)

    # Buildings
    buildings = [
        (40, 370, 130, 280),
        (190, 300, 120, 350),
        (330, 390, 140, 260),
        (500, 330, 120, 320),
        (650, 380, 150, 270),
        (830, 290, 130, 360),
        (980, 390, 90, 260)
    ]

    for x, y, w, h in buildings:
        pygame.draw.rect(screen, DARK, (x, y, w, h))

        # Windows
        for wx in range(x + 15, x + w - 10, 30):
            for wy in range(y + 20, y + h - 15, 40):
                pygame.draw.rect(
                    screen,
                    (105, 75, 145),
                    (wx, wy, 10, 15)
                )

    # Ground
    pygame.draw.rect(screen, (16, 11, 28), (0, 650, WIDTH, 50))


def draw_hud():
    # XP
    pygame.draw.rect(screen, PANEL, (25, 20, 220, 55), border_radius=12)
    draw_text("XP: " + str(xp), 45, 34, FONT, YELLOW)

    # Lives
    pygame.draw.rect(screen, PANEL, (265, 20, 220, 55), border_radius=12)
    draw_text("Lives: " + str(lives), 285, 34, FONT, RED)

    # Progress
    total_completed = 0

    for value in completed.values():
        if value:
            total_completed += 1

    draw_text(
        "Progress: " + str(total_completed) + "/4",
        870,
        34,
        FONT,
        WHITE
    )


def get_password_answer(word, indices):
    answer = ""

    for index in indices:
        answer += word[index]

    return answer


def get_current_question():
    if selected_challenge == "Character Hunt":
        return character_questions[challenge_index]

    if selected_challenge == "Password Gate":
        return password_questions[challenge_index]

    if selected_challenge == "Search Quest":
        return search_questions[challenge_index]

    if selected_challenge == "Slice Street":
        return slice_questions[challenge_index]

    return None


def check_answer():
    global xp
    global lives
    global feedback
    global feedback_color
    global challenge_index
    global input_text
    global hint_used
    global current_screen

    user_answer = input_text.strip().upper()

    correct = False

    # --------------------------------------------------------
    # CHARACTER HUNT
    # --------------------------------------------------------

    if selected_challenge == "Character Hunt":

        word, index, question = character_questions[challenge_index]

        correct_answer = word[index].upper()

        if user_answer == correct_answer:
            correct = True

    # --------------------------------------------------------
    # PASSWORD GATE
    # --------------------------------------------------------

    elif selected_challenge == "Password Gate":

        word, indices = password_questions[challenge_index]

        correct_answer = get_password_answer(
            word,
            indices
        ).upper()

        if user_answer == correct_answer:
            correct = True

    # --------------------------------------------------------
    # SEARCH QUEST
    # --------------------------------------------------------

    elif selected_challenge == "Search Quest":

        word, search_value, expected = search_questions[challenge_index]

        correct_answer = "YES" if expected else "NO"

        if user_answer == correct_answer:
            correct = True

    # --------------------------------------------------------
    # SLICE STREET
    # --------------------------------------------------------

    elif selected_challenge == "Slice Street":

        word, start, end = slice_questions[challenge_index]

        correct_answer = word[start:end].upper()

        if user_answer == correct_answer:
            correct = True

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if correct:

        xp += 25

        feedback = "Correct! Great job!"
        feedback_color = GREEN

        challenge_index += 1
        input_text = ""
        hint_used = False

        # Challenge completed
        if challenge_index >= 4:

            completed[selected_challenge] = True

            feedback = "Challenge Complete!"

            current_screen = "city"

            challenge_index = 0

    else:

        lives -= 1

        feedback = "Wrong answer. Try again!"
        feedback_color = RED

        input_text = ""

        if lives <= 0:
            current_screen = "game_over"


def check_boss_answer():
    global xp
    global lives
    global boss_index
    global feedback
    global feedback_color
    global input_text
    global current_screen

    user_answer = input_text.strip().upper()

    question = boss_questions[boss_index]

    correct_answer = ""

    if question[0] == "index":

        word = question[1]
        index = question[2]

        correct_answer = word[index]

    elif question[0] == "in":

        correct_answer = question[3]

    elif question[0] == "slice":

        word = question[1]
        start = question[2]
        end = question[3]

        correct_answer = word[start:end]

    if user_answer == correct_answer.upper():

        xp += 50

        feedback = "Boss question correct!"
        feedback_color = GREEN

        boss_index += 1
        input_text = ""

        if boss_index >= len(boss_questions):

            current_screen = "complete"

    else:

        lives -= 1

        feedback = "Wrong! The String Boss got you!"
        feedback_color = RED

        input_text = ""

        if lives <= 0:
            current_screen = "game_over"


# ============================================================
# CITY SCREEN
# ============================================================

def draw_city_screen():

    draw_city_background()

    draw_center_text(
        "STRING CITY",
        WIDTH // 2,
        105,
        TITLE_FONT,
        WHITE
    )

    draw_center_text(
        "Master Python Strings",
        WIDTH // 2,
        150,
        FONT,
        LIGHT_PURPLE
    )

    draw_hud()

    # Intro panel
    intro = pygame.Rect(180, 185, 740, 80)

    pygame.draw.rect(
        screen,
        PANEL,
        intro,
        border_radius=15
    )

    draw_center_text(
        "Complete all four areas and face the final String Boss!",
        intro.centerx,
        intro.centery,
        FONT,
        WHITE
    )

    # Challenge cards
    cards = [
        (
            "Character Hunt",
            "String Indexing",
            "Find a character using its position.",
            70,
            300
        ),

        (
            "Password Gate",
            "Indexing",
            "Use character positions to unlock a password.",
            545,
            300
        ),

        (
            "Search Quest",
            "Using IN",
            "Check whether a word exists inside a string.",
            70,
            465
        ),

        (
            "Slice Street",
            "String Slicing",
            "Take a selected part of a string.",
            545,
            465
        )
    ]

    mouse_pos = pygame.mouse.get_pos()

    for name, topic, description, x, y in cards:

        rect = pygame.Rect(x, y, 415, 135)

        active = rect.collidepoint(mouse_pos)

        if active:
            pygame.draw.rect(
                screen,
                PANEL_LIGHT,
                rect,
                border_radius=15
            )
        else:
            pygame.draw.rect(
                screen,
                PANEL,
                rect,
                border_radius=15
            )

        pygame.draw.rect(
            screen,
            PURPLE,
            rect,
            2,
            border_radius=15
        )

        draw_text(
            name,
            x + 20,
            y + 15,
            BIG_FONT,
            WHITE
        )

        draw_text(
            topic,
            x + 20,
            y + 52,
            SMALL_FONT,
            LIGHT_PURPLE
        )

        draw_wrapped_text(
            description,
            x + 20,
            y + 78,
            370,
            SMALL_FONT,
            GRAY
        )

        if completed[name]:

            draw_text(
                "COMPLETED",
                x + 300,
                y + 15,
                SMALL_FONT,
                GREEN
            )

    # Boss button
    all_done = True

    for value in completed.values():
        if not value:
            all_done = False

    if all_done:

        boss_rect = pygame.Rect(
            390,
            615,
            320,
            55
        )

        active = boss_rect.collidepoint(mouse_pos)

        draw_button(
            boss_rect,
            "START STRING BOSS",
            active
        )


# ============================================================
# CHALLENGE SCREEN
# ============================================================

def draw_challenge_screen():

    screen.fill(BG)

    draw_hud()

    draw_center_text(
        selected_challenge,
        WIDTH // 2,
        110,
        TITLE_FONT,
        WHITE
    )

    draw_center_text(
        "Round " + str(challenge_index + 1) + " / 4",
        WIDTH // 2,
        160,
        FONT,
        LIGHT_PURPLE
    )

    panel = pygame.Rect(150, 200, 800, 330)

    pygame.draw.rect(
        screen,
        PANEL,
        panel,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        PURPLE,
        panel,
        2,
        border_radius=20
    )

    # --------------------------------------------------------
    # QUESTION CONTENT
    # --------------------------------------------------------

    if selected_challenge == "Character Hunt":

        word, index, question = character_questions[challenge_index]

        draw_center_text(
            word,
            WIDTH // 2,
            260,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            "Index: " + str(index),
            WIDTH // 2,
            305,
            FONT,
            WHITE
        )

        draw_center_text(
            question,
            WIDTH // 2,
            350,
            FONT,
            WHITE
        )

        draw_center_text(
            "Example: PYTHON[1] gives Y",
            WIDTH // 2,
            395,
            SMALL_FONT,
            GRAY
        )

    elif selected_challenge == "Password Gate":

        word, indices = password_questions[challenge_index]

        draw_center_text(
            word,
            WIDTH // 2,
            260,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            "Indexes: " + str(indices),
            WIDTH // 2,
            310,
            FONT,
            WHITE
        )

        draw_center_text(
            "Enter the hidden password:",
            WIDTH // 2,
            365,
            FONT,
            WHITE
        )

        draw_center_text(
            "Use the characters at those indexes.",
            WIDTH // 2,
            405,
            SMALL_FONT,
            GRAY
        )

    elif selected_challenge == "Search Quest":

        word, search_value, expected = search_questions[challenge_index]

        draw_center_text(
            '"' + word + '"',
            WIDTH // 2,
            260,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            'Does "' + search_value + '" exist in the string?',
            WIDTH // 2,
            330,
            FONT,
            WHITE
        )

        draw_center_text(
            "Type YES or NO",
            WIDTH // 2,
            380,
            SMALL_FONT,
            GRAY
        )

    elif selected_challenge == "Slice Street":

        word, start, end = slice_questions[challenge_index]

        draw_center_text(
            word,
            WIDTH // 2,
            260,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            "Take: [" + str(start) + ":" + str(end) + "]",
            WIDTH // 2,
            315,
            FONT,
            WHITE
        )

        draw_center_text(
            "Enter the resulting string:",
            WIDTH // 2,
            370,
            FONT,
            WHITE
        )

    # --------------------------------------------------------
    # INPUT BOX
    # --------------------------------------------------------

    input_box = pygame.Rect(330, 455, 440, 55)

    pygame.draw.rect(
        screen,
        DARK,
        input_box,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        LIGHT_PURPLE,
        input_box,
        2,
        border_radius=10
    )

    draw_center_text(
        input_text,
        input_box.centerx,
        input_box.centery,
        FONT,
        WHITE
    )

    # Submit
    submit = pygame.Rect(455, 535, 190, 50)

    mouse_pos = pygame.mouse.get_pos()

    draw_button(
        submit,
        "SUBMIT",
        submit.collidepoint(mouse_pos)
    )

    # Hint
    hint_rect = pygame.Rect(250, 535, 150, 50)

    draw_button(
        hint_rect,
        "HINT",
        hint_rect.collidepoint(mouse_pos)
    )

    # Back
    back_rect = pygame.Rect(670, 535, 150, 50)

    draw_button(
        back_rect,
        "BACK",
        back_rect.collidepoint(mouse_pos)
    )

    # Feedback
    if feedback:

        draw_center_text(
            feedback,
            WIDTH // 2,
            610,
            FONT,
            feedback_color
        )


# ============================================================
# BOSS SCREEN
# ============================================================

def draw_boss_screen():

    screen.fill((35, 15, 25))

    draw_hud()

    draw_center_text(
        "STRING BOSS",
        WIDTH // 2,
        110,
        TITLE_FONT,
        RED
    )

    draw_center_text(
        "Final Challenge",
        WIDTH // 2,
        160,
        FONT,
        YELLOW
    )

    panel = pygame.Rect(150, 205, 800, 325)

    pygame.draw.rect(
        screen,
        PANEL,
        panel,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        RED,
        panel,
        2,
        border_radius=20
    )

    question = boss_questions[boss_index]

    if question[0] == "index":

        word = question[1]
        index = question[2]

        draw_center_text(
            word,
            WIDTH // 2,
            270,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            "What is at index " + str(index) + "?",
            WIDTH // 2,
            330,
            FONT,
            WHITE
        )

    elif question[0] == "in":

        word = question[1]
        value = question[2]

        draw_center_text(
            '"' + word + '"',
            WIDTH // 2,
            270,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            'Is "' + value + '" in the string?',
            WIDTH // 2,
            330,
            FONT,
            WHITE
        )

        draw_center_text(
            "Type YES or NO",
            WIDTH // 2,
            375,
            SMALL_FONT,
            GRAY
        )

    elif question[0] == "slice":

        word = question[1]
        start = question[2]
        end = question[3]

        draw_center_text(
            word,
            WIDTH // 2,
            270,
            BIG_FONT,
            YELLOW
        )

        draw_center_text(
            "Find: [" + str(start) + ":" + str(end) + "]",
            WIDTH // 2,
            330,
            FONT,
            WHITE
        )

    # Input
    input_box = pygame.Rect(330, 425, 440, 55)

    pygame.draw.rect(
        screen,
        DARK,
        input_box,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        RED,
        input_box,
        2,
        border_radius=10
    )

    draw_center_text(
        input_text,
        input_box.centerx,
        input_box.centery,
        FONT,
        WHITE
    )

    submit = pygame.Rect(455, 500, 190, 50)

    mouse_pos = pygame.mouse.get_pos()

    draw_button(
        submit,
        "SUBMIT",
        submit.collidepoint(mouse_pos)
    )

    if feedback:

        draw_center_text(
            feedback,
            WIDTH // 2,
            590,
            FONT,
            feedback_color
        )

    draw_center_text(
        "Boss Round " + str(boss_index + 1) + " / 5",
        WIDTH // 2,
        635,
        SMALL_FONT,
        GRAY
    )


# ============================================================
# COMPLETE SCREEN
# ============================================================

def draw_complete_screen():

    screen.fill(BG)

    draw_center_text(
        "STRING CITY COMPLETE!",
        WIDTH // 2,
        220,
        TITLE_FONT,
        GREEN
    )

    draw_center_text(
        "You defeated the String Boss!",
        WIDTH // 2,
        285,
        BIG_FONT,
        WHITE
    )

    draw_center_text(
        "Final XP: " + str(xp),
        WIDTH // 2,
        350,
        FONT,
        YELLOW
    )

    draw_center_text(
        "You are now a Python String Master.",
        WIDTH // 2,
        400,
        FONT,
        LIGHT_PURPLE
    )

    restart = pygame.Rect(420, 485, 260, 60)

    mouse_pos = pygame.mouse.get_pos()

    draw_button(
        restart,
        "PLAY AGAIN",
        restart.collidepoint(mouse_pos)
    )


# ============================================================
# GAME OVER SCREEN
# ============================================================

def draw_game_over_screen():

    screen.fill((30, 12, 20))

    draw_center_text(
        "GAME OVER",
        WIDTH // 2,
        240,
        TITLE_FONT,
        RED
    )

    draw_center_text(
        "You ran out of lives.",
        WIDTH // 2,
        310,
        BIG_FONT,
        WHITE
    )

    draw_center_text(
        "XP: " + str(xp),
        WIDTH // 2,
        365,
        FONT,
        YELLOW
    )

    restart = pygame.Rect(420, 450, 260, 60)

    mouse_pos = pygame.mouse.get_pos()

    draw_button(
        restart,
        "TRY AGAIN",
        restart.collidepoint(mouse_pos)
    )


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global current_screen
    global selected_challenge
    global xp
    global lives
    global input_text
    global feedback
    global challenge_index
    global boss_index
    global hint_used

    current_screen = "city"

    selected_challenge = None

    xp = 0
    lives = 5

    input_text = ""

    feedback = ""

    challenge_index = 0
    boss_index = 0

    hint_used = False

    for key in completed:
        completed[key] = False


# ============================================================
# HINTS
# ============================================================

def show_hint():

    global feedback
    global feedback_color
    global hint_used

    if hint_used:
        feedback = "Hint already used for this round."
        feedback_color = YELLOW
        return

    hint_used = True

    feedback_color = YELLOW

    if selected_challenge == "Character Hunt":

        feedback = "Remember: string indexes start from 0."

    elif selected_challenge == "Password Gate":

        feedback = "Take each character using the given indexes."

    elif selected_challenge == "Search Quest":

        feedback = 'Use YES if the value exists, otherwise NO.'

    elif selected_challenge == "Slice Street":

        feedback = "Slicing uses string[start:end]."

# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

while running:

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if current_screen in [
                    "challenge",
                    "boss"
                ]:
                    current_screen = "city"
                    input_text = ""
                    feedback = ""

            elif event.key == pygame.K_BACKSPACE:

                input_text = input_text[:-1]

            elif event.key == pygame.K_RETURN:

                if current_screen == "challenge":
                    check_answer()

                elif current_screen == "boss":
                    check_boss_answer()

            else:

                if len(input_text) < 25:

                    # Only accept normal characters
                    if event.unicode.isprintable():
                        input_text += event.unicode

        # ----------------------------------------------------
        # MOUSE CLICK
        # ----------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_pos = event.pos

                # =================================================
                # CITY SCREEN
                # =================================================

                if current_screen == "city":

                    cards = [
                        (
                            "Character Hunt",
                            pygame.Rect(70, 300, 415, 135)
                        ),
                        (
                            "Password Gate",
                            pygame.Rect(545, 300, 415, 135)
                        ),
                        (
                            "Search Quest",
                            pygame.Rect(70, 465, 415, 135)
                        ),
                        (
                            "Slice Street",
                            pygame.Rect(545, 465, 415, 135)
                        )
                    ]

                    for name, rect in cards:

                        if rect.collidepoint(mouse_pos):

                            selected_challenge = name

                            current_screen = "challenge"

                            challenge_index = 0

                            input_text = ""

                            feedback = ""

                            hint_used = False

                    # Boss
                    all_done = True

                    for value in completed.values():

                        if not value:
                            all_done = False

                    boss_rect = pygame.Rect(
                        390,
                        615,
                        320,
                        55
                    )

                    if all_done and boss_rect.collidepoint(mouse_pos):

                        current_screen = "boss"

                        boss_index = 0

                        input_text = ""

                        feedback = ""

                # =================================================
                # CHALLENGE SCREEN
                # =================================================

                elif current_screen == "challenge":

                    submit = pygame.Rect(
                        455,
                        535,
                        190,
                        50
                    )

                    hint_rect = pygame.Rect(
                        250,
                        535,
                        150,
                        50
                    )

                    back_rect = pygame.Rect(
                        670,
                        535,
                        150,
                        50
                    )

                    if submit.collidepoint(mouse_pos):
                        check_answer()

                    elif hint_rect.collidepoint(mouse_pos):
                        show_hint()

                    elif back_rect.collidepoint(mouse_pos):

                        current_screen = "city"

                        input_text = ""

                        feedback = ""

                # =================================================
                # BOSS SCREEN
                # =================================================

                elif current_screen == "boss":

                    submit = pygame.Rect(
                        455,
                        500,
                        190,
                        50
                    )

                    if submit.collidepoint(mouse_pos):

                        check_boss_answer()

                # =================================================
                # COMPLETE SCREEN
                # =================================================

                elif current_screen == "complete":

                    restart = pygame.Rect(
                        420,
                        485,
                        260,
                        60
                    )

                    if restart.collidepoint(mouse_pos):

                        reset_game()

                # =================================================
                # GAME OVER SCREEN
                # =================================================

                elif current_screen == "game_over":

                    restart = pygame.Rect(
                        420,
                        450,
                        260,
                        60
                    )

                    if restart.collidepoint(mouse_pos):

                        reset_game()

    # ========================================================
    # DRAW CURRENT SCREEN
    # ========================================================

    if current_screen == "city":

        draw_city_screen()

    elif current_screen == "challenge":

        draw_challenge_screen()

    elif current_screen == "boss":

        draw_boss_screen()

    elif current_screen == "complete":

        draw_complete_screen()

    elif current_screen == "game_over":

        draw_game_over_screen()

    # ========================================================
    # VERY IMPORTANT
    # ========================================================
    # This updates the window and fixes the black-screen issue.
    # ========================================================

    pygame.display.flip()

    clock.tick(60)


# ============================================================
# EXIT
# ============================================================

pygame.quit()
sys.exit()