# функции загрузки окон

import pygame

from config import LEVEL, MONEY, POINTS, BOARD, MUSIC
from config import screen, width, height, clock, fps, tile_width, tile_height
from config import all_sprites, tiles_group, evil_group, npc_group, \
    bullet_group, lose_group, stop_bullet_group
from config import sound_main, sound_start, sound_characters
from helpers import terminate, get_cell, save_result, get_results, print_text
from classes import Tile, Cop, Sotochka, Sign, Gop, Drunk, Beggar, Lose, \
    StopBullet, Еxcavator
from levels import levels
from images import fon_images, evil_images, npc_images, tile_images


# стартовое окно
def start_screen():
    print("[!] открытие стартового окна")
    intro_text = ["Добро пожаловать на УРАЛМАШ", "",
                  "Выбрать уровень — «1», «2», «3»",
                  "Управление — «F1»",
                  "Статистика — «F2»",
                  "Введение в сюжет — «F3»",
                  "Персонажи — «F4»", "",
                  "Приятной игры!"]

    # музыка
    if not MUSIC[0] and MUSIC[1]:
        sound_start[0] = pygame.mixer.Sound('data/start.mp3')
        sound_start[0].set_volume(0.2)
        sound_start[0].play(-1)
        MUSIC[0] = True

    fon = pygame.transform.scale(fon_images['start'], (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    LEVEL[0] = 1
                    print('[!] выбран 1 уровень')
                elif event.key == pygame.K_2:
                    LEVEL[0] = 2
                    print('[!] выбран 2 уровень')
                elif event.key == pygame.K_3:
                    LEVEL[0] = 3
                    print('[!] выбран 3 уровень')
                elif event.key == pygame.K_F1:
                    guide_screen()
                elif event.key == pygame.K_F2:
                    results_screen()
                elif event.key == pygame.K_F3:
                    story_screen()
                elif event.key == pygame.K_F4:
                    sound_start[0].stop()
                    MUSIC[0] = False
                    characters_screen()
                if event.key == pygame.K_SPACE:
                    if MUSIC[1]:
                        MUSIC[1] = False
                        MUSIC[0] = False
                        sound_start[0].stop()
                    elif not MUSIC[1]:
                        MUSIC[1] = True
                        MUSIC[0] = True
                        sound_start[0].play(-1)
            if LEVEL[0]:
                sound_start[0].stop()
                MUSIC[0] = False
                game_screen()  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


# окно управления
def guide_screen():
    print("[!] открытие окна управления")
    intro_text = ["УПРАВЛЕНИЕ", "",
                  "Выбрать NPC — «1», «2», «3»",
                  "Поставить NPC — «ЛКМ»",
                  "Вкл/выкл музыку — «ПРОБЕЛ»",
                  "Вернуться в меню/завершить игру — «ESC»"]

    fon = pygame.transform.scale(fon_images['manual'], (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                if event.key == pygame.K_SPACE:
                    if MUSIC[1]:
                        MUSIC[1] = False
                        MUSIC[0] = False
                        sound_start[0].stop()
                    elif not MUSIC[0]:
                        MUSIC[1] = True
                        MUSIC[0] = True
                        sound_start[0].play(-1)
        pygame.display.flip()
        clock.tick(fps)


# окно окончания игры
def end_screen():
    print("[!] открытие окна окончания игры")
    intro_text = ["ВЫ ПРОИГРАЛИ", "",
                  "Посмотреть результаты — «ЛКМ»",
                  "Перейти в меню — «ПРОБЕЛ»"]

    fon = pygame.transform.scale(fon_images['end'], (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    results_screen()
        pygame.display.flip()
        clock.tick(fps)


# окно отображения результатов
def results_screen():
    print("[!] открытие окна отображения результатов")

    res1, res2, res3, res_last = get_results()

    intro_text = ["ИГРОВЫЕ РЕКОРДЫ", "",
                  f"1 уровень — {res1}",
                  f"2 уровень — {res2}",
                  f"3 уровень — {res3}",
                  f"Последняя игра — {res_last[1]}",
                  f"    *{res_last[0]} уровень, {res_last[2]} место", "",
                  f"Вернуться в меню — «ESC»"]

    fon = pygame.transform.scale(fon_images['results'], (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                if event.key == pygame.K_SPACE:
                    if MUSIC[0]:
                        MUSIC[1] = False
                        MUSIC[0] = False
                        sound_start[0].stop()
                    elif not MUSIC[0]:
                        MUSIC[1] = True
                        MUSIC[0] = True
                        sound_start[0].play(-1)
        pygame.display.flip()
        clock.tick(fps)


# окно введения в сюжет
def story_screen():
    print("[!] открытие окна введение в сюжет")
    intro_text = ["ВВЕДЕНИЕ В СЮЖЕТ", "",
                  "Уралмаш... Он возник на заре Советского Союза",
                  "как соцгород будущего. Процветающий район,",
                  "что расположился у «завода заводов» УЗТМ.",
                  "Но на закате СССР его территория стала вотчиной",
                  "одной из самых страшных преступных группировок.",
                  "Говорят, стрельба по ночам была в те годы обычным",
                  "делом. И хоть в наше время обстановка немного",
                  "улучшилась и стабилизировалась, однако о резком",
                  "спаде преступности утверждать ещё рано..."]

    fon = pygame.transform.scale(fon_images['story'], (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 24)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                if event.key == pygame.K_SPACE:
                    if MUSIC[0]:
                        MUSIC[1] = False
                        MUSIC[0] = False
                        sound_start[0].stop()
                    elif not MUSIC[0]:
                        MUSIC[1] = True
                        MUSIC[0] = True
                        sound_start[0].play(-1)
        pygame.display.flip()
        clock.tick(fps)


# окно описания персонажей
def characters_screen():
    print("[!] открытие окна описания персонажей")
    intro_text = ["ПЕРСОНАЖИ", "",
                  "«1» — полицейский",
                  "«2» — соточка",
                  "«3» — ремонт дороги", "",
                  "«4» — гопник",
                  "«5» — попрошайка",
                  "«6» — пьяница", "",
                  "«7» — экскаватор"]
    cop_text = ["ПОЛИЦЕЙСКИЙ", "", "", "",
                "Здоровье: 3, Урон пулей: 1, Урон: 2", "",
                "Каждый полицейский в районе старается",
                "добросовестно выполнять свою нелёгкую работу.",
                "Следует уважать их труд.", "",
                "«0» — вернуться к списку персонажей"]
    sotochka_text = ["СОТОЧКА", "", "", "",
                     "Здоровье: 0, Урон: 0", "",
                     "Деньги на полу не валяются... Но, может, если мы",
                     "оставим на дороге хотя бы соточку, это отвлечёт их?",
                     "", "",
                     "«0» — вернуться к списку персонажей"]
    sign_text = ["РЕМОНТ ДОРОГИ", "", "", "",
                 "Здоровье: 7, Урон: 0", "",
                 "Чтобы задержать толпу, нужно перекрыть дороги!",
                 "Хотя, возможно, этим мы лишь оправдываем себя...",
                 "", "",
                 "«0» — вернуться к списку персонажей"]
    gop_text = ["ГОПНИК", "", "", "",
                "Здоровье: 5, Урон: 1", "",
                "Крайне не рекомендую связываться с ними.",
                "Хоть их влиянию подвержена большая часть ",
                "населения Уралмаша, не стоит вступать в их ряды.", "",
                "«0» — вернуться к списку персонажей"]
    beggar_text = ["ПОПРОШАЙКА", "", "", "",
                   "Здоровье: 3, Урон: 1", "",
                   "Не доверя...",
                   "...",
                   "...", "",
                   "«0» — вернуться к списку персонажей"]
    drunk_text = ["ПЬЯНИЦА", "", "", "",
                  "Здоровье: 10, Урон: 1", "",
                  "Он же «Синяк». Обладатель подозрительной",
                  "везучести. Много пьёт и всегда простужен.",
                  "Характер скверный. Не женат.", "",
                  "«0» — вернуться к списку персонажей"]
    excavator_text = ["ЭКСКАВАТОР", "", "", "",
                      "Здоровье: <...>, Урон: <...>", "",
                      "Не забывайте, что недалеко УЗТМ.",
                      "Кто-нибудь выяснил, что там производят?",
                      "Я слышал, что шага...", "",
                      "«0» — вернуться к списку персонажей"]

    # музыка
    sound_characters[0] = pygame.mixer.Sound('data/characters.mp3')
    sound_characters[0].set_volume(0.2)
    if not MUSIC[0] and MUSIC[1]:
        sound_characters[0].play(-1)
        MUSIC[0] = True

    fon = pygame.transform.scale(fon_images['characters'], (width, height))
    screen.blit(fon, (0, 0))
    print_text(intro_text)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound_characters[0].stop()
                    MUSIC[0] = False
                    start_screen()
                if event.key == pygame.K_1:  # полицейский
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(npc_images['cop0'], (30, 100))
                    print_text(cop_text)
                if event.key == pygame.K_2:  # соточка
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(npc_images['sotochka'], (30, 100))
                    print_text(sotochka_text)
                if event.key == pygame.K_3:  # ремонт дороги
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(npc_images['sign'], (30, 100))
                    print_text(sign_text)
                if event.key == pygame.K_4:  # гопник
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(evil_images['gop0'], (30, 100))
                    print_text(gop_text)
                if event.key == pygame.K_5:  # попрошайка
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(evil_images['beggar0'], (30, 100))
                    print_text(beggar_text)
                if event.key == pygame.K_6:  # пьяница
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(evil_images['drunk0'], (30, 100))
                    print_text(drunk_text)
                if event.key == pygame.K_7:  # экскаватор
                    screen.blit(fon, (0, 0))
                    screen.blit(tile_images['level1'], (30, 100))
                    screen.blit(evil_images['excavator'], (30, 100))
                    print_text(excavator_text)
                if event.key == pygame.K_0:  # интро
                    screen.blit(fon, (0, 0))
                    print_text(intro_text)
                if event.key == pygame.K_SPACE:
                    if MUSIC[0]:
                        MUSIC[1] = False
                        MUSIC[0] = False
                        sound_characters[0].stop()
                    elif not MUSIC[0]:
                        MUSIC[1] = True
                        MUSIC[0] = True
                        sound_characters[0].play(-1)
        pygame.display.flip()
        clock.tick(fps)


# игровое окно
def game_screen():
    # генерация уровня
    print('[#] генерация уровня')
    for y in range(5):
        for x in range(9):
            if LEVEL[0] == 1:
                Tile('level1', x, y + 2)
            elif LEVEL[0] == 2:
                Tile('level2', x, y + 2)
            elif LEVEL[0] == 3:
                Tile('level3', x, y + 2)

    # генерация врагов
    print('[#] генерация врагов')
    for y in range(5):
        for x in range(23):
            if LEVEL[0] == 1:
                if levels['level1'][y][x] == 1:
                    Gop(x + 9, y + 2)
                elif levels['level1'][y][x] == 2:
                    Beggar(x + 9, y + 2)
                elif levels['level1'][y][x] == 3:
                    Drunk(x + 9, y + 2)
            elif LEVEL[0] == 2:
                if levels['level2'][y][x] == 1:
                    Gop(x + 9, y + 2)
                elif levels['level2'][y][x] == 2:
                    Beggar(x + 9, y + 2)
                elif levels['level2'][y][x] == 3:
                    Drunk(x + 9, y + 2)
            elif LEVEL[0] == 3:
                if levels['level3'][y][x] == 1:
                    Gop(x + 9, y + 2)
                elif levels['level3'][y][x] == 2:
                    Beggar(x + 9, y + 2)
                elif levels['level3'][y][x] == 3:
                    Drunk(x + 9, y + 2)

    print('[#] генерация ограничительных линий')
    for y in range(5):
        for x in range(9):
            Lose(-1, y + 2)  # линия проигрыша
            StopBullet(9, y + 2)  # стоп пулям в конце поля

    # музыка
    sound_main[0] = pygame.mixer.Sound('data/main.mp3')
    sound_main[0].set_volume(0.2)
    if not MUSIC[0] and MUSIC[1]:
        sound_main[0].play(-1)
        MUSIC[0] = True

    running = True
    apocalypse = False  # вызов министра
    cache = 'cop'  # выбранный NPC
    image_panel = ['data/cop_blur.png', 'data/sotochka.png', 'data/sign.png']
    BOARD[:] = [[0] * 9 for x in range(5)]  # NPC на поле
    font = pygame.font.Font(None, 20)
    text_300 = font.render("300", True, [0, 0, 0])
    text_100 = font.render("100", True, [0, 0, 0])
    MONEY[0] = 3000
    text_of_money = font.render("ВАЛЮТА:", True, [0, 0, 0])
    POINTS[0] = 0
    text_of_points = font.render("ОЧКИ:", True, [0, 0, 0])
    print('[!] начало игры')
    while running:
        # отрисовка игровой панели
        screen.fill((128, 128, 128))
        screen.blit(pygame.image.load(image_panel[0]), (tile_width * 3, 10))
        screen.blit(pygame.image.load(image_panel[1]), (tile_width * 4, 10))
        screen.blit(pygame.image.load(image_panel[2]), (tile_width * 5, 10))
        screen.blit(text_300, (tile_width * 3 + 13, tile_height * 1 + 20))
        screen.blit(text_100, (tile_width * 4 + 13, tile_height * 1 + 20))
        screen.blit(text_300, (tile_width * 5 + 13, tile_height * 1 + 20))
        screen.blit(text_of_money, (tile_width * 1 - 5, tile_height * 0 + 35))
        text_money = font.render(str(MONEY[0]), True, [0, 0, 0])
        screen.blit(text_money, (tile_width * 1 + 10, tile_height * 1 + 20))
        screen.blit(text_of_points, (tile_width * 7 + 3, tile_height * 0 + 35))
        text_points = font.render(str(POINTS[0] // 10), True, [0, 0, 0])
        screen.blit(text_points, (tile_width * 7 + 5, tile_height * 1 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print('[#] выбор `cop`')
                    cache = 'cop'  # 1
                    image_panel[0] = 'data/cop_blur.png'
                    image_panel[1] = 'data/sotochka.png'
                    image_panel[2] = 'data/sign.png'
                if event.key == pygame.K_2:
                    print('[#] выбор `sotochka`')
                    cache = 'sotochka'  # 2
                    image_panel[0] = 'data/cop0.png'
                    image_panel[1] = 'data/sotochka_blur.png'
                    image_panel[2] = 'data/sign.png'
                if event.key == pygame.K_3:
                    print('[#] выбор `sign`')
                    cache = 'sign'  # 3
                    image_panel[0] = 'data/cop0.png'
                    image_panel[1] = 'data/sotochka.png'
                    image_panel[2] = 'data/sign_blur.png'
                if event.key == pygame.K_SPACE:
                    if MUSIC[0]:
                        MUSIC[1] = False
                        MUSIC[0] = False
                        sound_main[0].stop()
                    elif not MUSIC[0]:
                        MUSIC[1] = True
                        MUSIC[0] = True
                        sound_main[0].play(-1)
                if event.key == pygame.K_ESCAPE:
                    for sprite in all_sprites:
                        sprite.kill()

                    # сохранение результата
                    save_result()

                    sound_main[0].stop()
                    MUSIC[0] = False

                    LEVEL[0] = 0
                    print("[!] конец игры")
                    end_screen()
                    return  # остановка

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if get_cell(event.pos):
                        x, y = get_cell(event.pos)
                        if BOARD[y][x] == 0:
                            if cache == 'cop' and MONEY[0] >= 300:
                                print(f'[#] `cop` установлен на ({x}, {y})')
                                BOARD[y][x] = 1
                                MONEY[0] -= 300
                                Cop(x, y + 2)
                            elif cache == 'sotochka' and MONEY[0] >= 100:
                                print(
                                    f'[#] `sotochka` установлен на ({x}, {y})')
                                BOARD[y][x] = 2
                                MONEY[0] -= 100
                                Sotochka(x, y + 2)
                            elif cache == 'sign' and MONEY[0] >= 300:
                                print(f'[#] `sign` установлен на ({x}, {y})')
                                BOARD[y][x] = 3
                                MONEY[0] -= 300
                                Sign(x, y + 2)

        # вызов министра
        if not evil_group:
            excavator = Еxcavator(9, 4)
            apocalypse = True

        # столкновения
        bullet_collide = pygame.sprite.groupcollide(bullet_group, evil_group,
                                                    False, False)
        npc_collide = pygame.sprite.groupcollide(npc_group, evil_group,
                                                 False, False)
        lose_collide = pygame.sprite.groupcollide(lose_group, evil_group,
                                                  False, False)
        stop_bullet_collide = pygame.sprite.groupcollide(bullet_group,
                                                         stop_bullet_group,
                                                         False, False)
        if apocalypse:
            pygame.sprite.spritecollide(excavator, npc_group, True)

        # обработка столкновений
        for key, value in bullet_collide.items():
            key.kill()
            value[0].damage('bullet')

        for key, value in npc_collide.items():
            key.damage()
            if key.get_name() == 'cop':
                value[0].damage('cop')
            elif key.get_name() == 'sotochka':
                value[0].damage('sotochka')
            elif key.get_name() == 'sign':
                value[0].damage('sign')

        for key in stop_bullet_collide.keys():
            key.kill()

        if lose_collide:
            for sprite in all_sprites:
                sprite.kill()

            # сохранение результата
            save_result()

            sound_main[0].stop()
            MUSIC[0] = False

            LEVEL[0] = 0
            print("[!] конец игры")
            end_screen()
            return  # остановка

        all_sprites.update()
        tiles_group.draw(screen)
        npc_group.draw(screen)
        bullet_group.draw(screen)
        evil_group.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
