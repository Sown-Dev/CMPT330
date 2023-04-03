# NAME:
# FILENAME:
# SUMMARY:

# pug art: https://opengameart.org/content/pug-rework
# cheese art: https://opengameart.org/content/free-rpg-icons-2
# carpet tile texture: https://opengameart.org/content/carpet-texture-red-seamless-texture-with-normalmap
# defeat_cat fanfare: https://opengameart.org/content/5-soundsshort-melodies
# bgm: https://opengameart.org/content/funny-chase-8-bit-chiptune
# barking and eating: https://opengameart.org/content/80-cc0-creature-sfx
# rat: https://opengameart.org/content/rodents-rat-rework
# cats: https://opengameart.org/content/lpc-cats-and-dogs
# game over music: https://opengameart.org/content/generic-8-bit-jrpg-soundtrack

import pygame.sprite
from os.path import exists

from grid import *
from sprites import *
from textures import *


def game():
    pygame.init()
    pygame.mixer.music.play()
    disp_w, disp_h = (TILE_SIZE + 1) * GRID_W, (TILE_SIZE + 1) * GRID_H + SCORE_MARGIN
    # bg = pygame.display.set_mode((disp_w, disp_h), pygame.SRCALPHA, 32)
    bg = pygame.display.set_mode((disp_w, disp_h), pygame.SRCALPHA, 32)
    bg_texture = Texture(join('assets', 'carpet_tile.jpg'), TILE_SIZE + 1)  # creates texture object of right size
    bg_img = bg_texture.tiled(SCREEN_W, SCREEN_H)  # stores background carpet texture

    grid = Grid(GRID_W, GRID_H, TILE_SIZE)  # creates grid object (where game pieces go)
    if DEBUG:
        grid.toggle_visible()

    cheese_tiles, dog_tiles = grid.import_map('map.csv')  # loads in CSV with wall, cheese, dog info

    clock = pygame.time.Clock()
    sprite_groups = {gp: pygame.sprite.Group() for gp in ['all', 'cats', 'items', 'pc']}
    pc = Mouse(grid.get_tile((13, 11)))  # sets starting spot to approximately center map
    sprite_groups['all'].add(pc)  # adds player to 'all' and 'pc' sprite_group
    sprite_groups['pc'].add(pc)
    for ct in cheese_tiles:  # adds each cheese sprite to 'all' and 'items' sprite_groups
        curr_cheese = Cheese(ct)
        sprite_groups['all'].add(curr_cheese)
        sprite_groups['items'].add(curr_cheese)
    for dt in dog_tiles:  # adds each dog to 'all' and 'items' sprite_groups
        curr_cheese = Dog(dt)
        sprite_groups['all'].add(curr_cheese)
        sprite_groups['items'].add(curr_cheese)
    cats = [BrownCat(grid.get_tile(BROWN_START), grid),  # creates list of cat objects
            BlackCat(grid.get_tile(BLACK_START), grid),
            OrangeCat(grid.get_tile(ORANGE_START), grid),
            WhiteCat(grid.get_tile(WHITE_START), grid)]
    for cat in cats:  # adds cats to 'cats' and 'all' sprite_groups
        sprite_groups['cats'].add(cat)
        sprite_groups['all'].add(cat)

    font = pygame.font.Font(None, 48)
    cheese_score = 0
    best_score = 0
    if exists('high_score.txt'):  # creates save game (basic txt file)
        with open('high_score.txt', 'r') as f:
            file_contents = f.read()
            best_score = int(file_contents) if file_contents != '' else 0

    while True:
        bg.fill((0, 0, 0))
        bg.blit(bg_img, (0, SCORE_MARGIN))  # puts carpet under the score margin
        bg.blit(grid.get_surf(), (0, SCORE_MARGIN))  # puts grid "on top" of the carpet
        grid.refresh()  # refreshes the grid to prevent smearing of sprites
        time_inc = clock.tick(FPS)  # guarantees up to 30 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pc.update(pygame.key.get_pressed(), grid, time_inc)  # update mouse based on keys, walls, and time
        for cat in sprite_groups['cats']:
            cheese_score += cat.update(grid, pc, time_inc)  # update cheese based on mouse, time
            # update function for cat returns 100 if a cat was defeated
        for item in sprite_groups['items']:  # update items (just cheese right now)
            cheese_score += item.update(pc, time_inc)  # if cheese is picked up, give player 1 point

        if not pc.alive() and not DEBUG:  # end game screen if player is killed by cat
            pygame.mixer.music.play(game_over)
            bg.fill((0, 0, 0))  # make black screen
            game_over = font.render(f'GAME OVER', True, (230, 230, 230))
            if cheese_score > best_score:  # short bit of code to save
                best_score = cheese_score
                with open('high_score.txt', 'w') as f:
                    f.write(str(cheese_score))
            score_printout = font.render(f'Final Score: {cheese_score}', True, (230, 230, 230))
            pr_printout = font.render(f'Personal Best: {best_score}', True, (230, 230, 230))
            bg.blit(game_over, ((SCREEN_W / 2) - (game_over.get_width() / 2),
                                (SCREEN_H / 2) - (game_over.get_height() / 2)))  # draws text in top center of screen
            bg.blit(score_printout, ((SCREEN_W / 2) - (score_printout.get_width() / 2),
                                     (SCREEN_H / 2) - (score_printout.get_height() / 2) + 100))
            bg.blit(pr_printout, ((SCREEN_W / 2) - (pr_printout.get_width() / 2),
                                  (SCREEN_H / 2) - (pr_printout.get_height() / 2) + 200))
            pygame.display.update()
            pygame.time.delay(3500)
            exit()

        score_printout = font.render(f'Score: {cheese_score}', True, (230, 230, 230))
        pr_printout = font.render(f'Personal Best: {best_score}', True, (230, 230, 230))
        bg.blit(score_printout, (5, 5))
        bg.blit(pr_printout, ((SCREEN_W - pr_printout.get_width() - 5), 5))
        sprite_groups['all'].draw(grid.get_surf())  # drawing updated sprites on screen

        pygame.display.update()  # updating screen


def main():
    game()


if __name__ == '__main__':
    main()
