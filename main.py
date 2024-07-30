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
custom_font = pygame.font.Font(custom_font_path, 12)

clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

highscore = load_highscore()

# Storing the selected bird type (testing, I might remove this later)
selected_bird = 'galo'


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    print(f"Creating bird {selected_bird}") #check which type the program got.
    return Bird(selected_bird, sprites), GameStartMessage(sprites)


bird, game_start_message = create_sprites()
score = None

# reset function that allows the sprite change
def reset_game():
    global bird, game_start_message, score
    sprites.empty()
    bird, game_start_message = create_sprites()
    score = None


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                score = Score(sprites)
                pygame.time.set_timer(column_create_event, 1500)
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                score = None
                bird, game_start_message = create_sprites()
            # selecting different birds
            if event.key == pygame.K_1:
                selected_bird = 'galo'
                print(f"selected bird: {selected_bird}")
                if not gamestarted:
                    reset_game()
            if event.key == pygame.K_2:
                selected_bird = 'redbird'
                print(f"selected bird: {selected_bird}")
                if not gamestarted:
                    reset_game()

        if not gameover:
            bird.handle_event(event)

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

    if not gamestarted and not gameover:
        # Displaying the high score on the screen
        highscore_text = custom_font.render(f"High Score: {highscore}", True, (255, 255, 255))
        screen.blit(highscore_text, (10, 10))

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
