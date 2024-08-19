import pygame

import assets
import configs
from highscore import load_highscore, save_highscore
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Galo de Calça")

img = pygame.image.load('assets/icons/galo-downflap.png')
pygame.display.set_icon(img)

custom_font_path = 'assets/fonts/PublicPixelFont/PublicPixel-E447g.ttf'
custom_font = pygame.font.Font(custom_font_path, 11)

# Load background image (it will be used on the selection screen)
background_image = pygame.image.load('assets/sprites/background.png')
# Load the bird preview images
galo_de_calca_image = pygame.image.load('assets/sprites/galo-downflap.png')
red_bird_image = pygame.image.load('assets/sprites/redbird-downflap.png')

clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False
show_selection_screen = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

highscore = load_highscore()

selected_bird = 'galo'


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(selected_bird, sprites), GameStartMessage(sprites)


bird, game_start_message = create_sprites()
score = None


# reset function that allows the sprite change
def reset_game():
    global bird, game_start_message, score
    sprites.empty()
    bird, game_start_message = create_sprites()
    score = None


# BIRD SELECTION SCREEN
def display_selection_screen():
    screen.blit(background_image, (0, 0))

    selection_text = custom_font.render("Select your bird", True, (255, 255, 255))
    screen.blit(selection_text, (configs.SCREEN_WIDTH // 2 - selection_text.get_width() // 2, 50))

    # Alignement do adjust all bird names based on the 'select your bird' message
    alignment = (configs.SCREEN_WIDTH // 2 - selection_text.get_width() // 2) + 30

    galo_de_calca_text = custom_font.render("1: Galo de Calça", True, (255, 255, 255))
    screen.blit(galo_de_calca_text, (alignment, 120))
    screen.blit(galo_de_calca_image, (45, 112))

    red_bird_text = custom_font.render("2: Red Bird", True, (255, 255, 255))
    screen.blit(red_bird_text, (alignment, 160))
    screen.blit(red_bird_image, (45, 152))

    esc_text = custom_font.render("Press ESC to go back", True, (255, 255, 255))
    screen.blit(esc_text, (configs.SCREEN_WIDTH // 2 - esc_text.get_width() // 2, 440))

    pygame.display.flip()


# MAIN LOOP HERE
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover and not show_selection_screen:
                gamestarted = True
                game_start_message.kill()
                score = Score(sprites)
                pygame.time.set_timer(column_create_event, 1500)
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                reset_game()

            # SELECTION SCREEN CONDITIONALS:
            if event.key == pygame.K_s and not gamestarted:
                # Open Selection Screen
                show_selection_screen = True
            if event.key == pygame.K_1 and show_selection_screen:
                selected_bird = 'galo'
                show_selection_screen = False
                reset_game()
            if event.key == pygame.K_2 and show_selection_screen:
                selected_bird = 'redbird'
                show_selection_screen = False
                reset_game()
            if event.key == pygame.K_ESCAPE and show_selection_screen:
                # Closes Selection Screen if the user does not want to do anything
                gameover = False
                gamestarted = False
                show_selection_screen = False
                reset_game()

        if not gameover:
            bird.handle_event(event)

    if show_selection_screen:
        display_selection_screen()
        continue

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

        # checking score
        if score and score.value > highscore:
            highscore = score.value
            save_highscore(highscore)

    if score is not None:
        for sprite in sprites:
            if type(sprite) is Column and sprite.is_passed():
                score.value += 1
                assets.play_audio("point")

    if not gamestarted and not gameover and not show_selection_screen:
        # Displaying the high score on the screen
        highscore_text = custom_font.render(f"High Score: {highscore}", True, (255, 255, 255))
        screen.blit(highscore_text, (configs.SCREEN_WIDTH // 2 - highscore_text.get_width() // 2, 50))

        # Text on the main screen:
        selection_button_text = custom_font.render("Press 'S' to select birds", True, (83, 138, 33))
        screen.blit(selection_button_text, (configs.SCREEN_WIDTH // 2 - selection_button_text.get_width() // 2, 450))

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
