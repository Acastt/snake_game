import sys, pygame, random
from pygame.math import Vector2
from settings import Window
from pygame.locals import *

pygame.init()

font = pygame.font.SysFont(None, 23)
pygame.display.set_caption('Snake Game')

class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * Window.cell_size, self.pos.y * Window.cell_size, Window.cell_size, Window.cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, Window.cell_number - 1)
        self.y = random.randint(0, Window.cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
    
        self.head_up = pygame.image.load('Graphics/snake/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/snake/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/snake/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/snake/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/snake/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/snake/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/snake/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/snake/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/snake/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/snake/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/snake/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/snake/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/snake/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/snake/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * Window.cell_size)
            y_pos = int(block.y * Window.cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, Window.cell_size, Window.cell_size)
            
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                     screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                    
    def update_head_graphics(self):
        head_pos_relation = self.body[1] - self.body[0]
        if head_pos_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_pos_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_pos_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_pos_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_pos_relation = self.body[-2] - self.body[-1]
        if tail_pos_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_pos_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_pos_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_pos_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.crunch_sound.play().set_volume(0.4)
        
    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.game_pause = False

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        
    def menu_draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < Window.cell_number or not 0 <= self.snake.body[0].y < Window.cell_number:
            self.game_over()
            # self.main_menu()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(Window.cell_number):
            if row % 2 == 0: 
                for col in range(Window.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * Window.cell_size,row * Window.cell_size,Window.cell_size,Window.cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(Window.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * Window.cell_size,row * Window.cell_size,Window.cell_size,Window.cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)	
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(Window.cell_size * Window.cell_number - 60)
        score_y = int(Window.cell_size * Window.cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 8, apple_rect.height)

        pygame.draw.rect(screen,(164, 209, 61), bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen,(56,74,12), bg_rect,2)

    def draw_text(text, font, color, surface, x, y):
        text_object = font.render(text, 1, color)
        text_rect = text_object.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_object, text_rect)

    def draw_menu(self):
        
        screen.blit(main_menu,main_menu_rect)
        screen.blit(options,options_rect)
        screen.blit(resume, resume_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_game.game_pause = False
                    main_menu_rect.center = (120, 80)
                    options_rect.center = (100, 160)
                    resume_rect.center = (100, 240)
                    return False
           


    def draw_options_menu(self):
        running = True
        print('menu opçoes')
        options_rect.center = (120, 80)
        screen.blit(options,options_rect)
        while running:
            m_x, m_y = pygame.mouse.get_pos()
            m_click = False            
        # screen.blit(main_menu,main_menu_rect)
            if main_game.game_pause == False:                
                return False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        main_menu_rect.center = (120, 80)
                        options_rect.center = (100, 160)
                        resume_rect.center = (100, 240)
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        m_click = True
                if resume_rect.collidepoint((m_x, m_y)):
                    if m_click:
                        running = False
                        main_game.game_pause = False
                        print('exit')
                
            # Main.draw_text('Main menu', font, (255, 255, 255), screen, 25, 28)
            screen_overlay.fill((175,215,70, 128))
            screen.blit(screen_overlay, (0,0))     
            screen.blit(options,options_rect)
            screen.blit(video, video_rect)
            screen.blit(sound, sound_rect)
            resume_rect.center = (100, 320)
            screen.blit(resume, resume_rect)
            pygame.display.update()
            clock.tick(60)
            main_game.draw_elements()

    def main_menu(self):
        while True:
            
            m_x, m_y = pygame.mouse.get_pos()
            m_click = False         
            if main_game.game_pause == False:
                return False
            if main_game.game_pause:
                main_menu_rect.center = (120, 80)
                options_rect.center = (100, 160)
                resume_rect.center = (100, 240)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        main_game.game_pause = False
                        main_menu_rect.center = (120, 80)
                        options_rect.center = (100, 160)
                        resume_rect.center = (100, 240)
                        return False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        m_click = True
                
                

            # if main_menu_rect.collidepoint((m_x, m_y)):
            #     if m_click:
            #         menu_state = 'main'
            #         m_click =False
            #         main_game.draw_menu()
                
            if options_rect.collidepoint((m_x, m_y)):
                if m_click:
                    menu_state = 'options'
                    m_click =False
                    main_game.draw_options_menu()
                    # FULLSCREEN_TOGGLE
                                
            if resume_rect.collidepoint((m_x, m_y)):
                if m_click:
                    menu_state = '0'
                    m_click =False
                    print('exit')
                    return False

            screen_overlay.fill((175,215,70, 128))
            screen.blit(screen_overlay, (0,0))            
            main_game.draw_menu() 
            pygame.display.update()
            main_game.draw_elements()
            clock.tick(60)
        
            


pygame.init()
info = pygame.display.Info()
print(info)
# screen_width, screen_height = info.current_w, info.current_h
# Window.width, Window.height = screen_width - 10, screen_height - 440
# window_x = (screen_width - Window.width) // 2
# window_y = (screen_height - Window.height) // 2
# screen = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN)
# FULLSCREEN_TOGGLE = pygame.display.toggle_fullscreen()
screen = pygame.display.set_mode((Window.width, Window.height))
screen_overlay = pygame.Surface((Window.width, Window.height), pygame.SRCALPHA)


clock = pygame.time.Clock()


apple = pygame.image.load('Graphics/apple/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)


menu_state = '0'

main_menu = pygame.image.load('Graphics/menu/main_menu.png').convert_alpha()
main_menu_rect = main_menu.get_rect()
main_menu_rect.center = (120, 80)
options = pygame.image.load('Graphics/menu/options.png').convert_alpha()
options_rect = options.get_rect()
options_rect.center = (100, 160)
resume = pygame.image.load('Graphics/menu/resume.png').convert_alpha()
resume_rect = resume.get_rect()
resume_rect.center = (100, 240)
video = pygame.image.load('Graphics/menu/video.png').convert_alpha()
video_rect = video.get_rect()
video_rect.center = (100, 160)
sound = pygame.image.load('Graphics/menu/sound.png').convert_alpha()
sound_rect = sound.get_rect()
sound_rect.center = (100, 240)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

m_click = False

main_game = Main()

while True:
    fps = clock.get_fps()   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_state = 'main'
                main_game.game_pause = True
                main_game.main_menu()
            if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        m_click = True
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

            if main_game.game_pause == False:
                main_menu_rect.center = (120, 80)
                options_rect.center = (100, 160)
                resume_rect.center = (100, 240)
    screen.fill((175,215,70))
    main_game.draw_elements()
    Main.draw_text(f'FPS={fps:.2f}', font, (255, 255, 255), screen, 680, 20)
    pygame.display.update()
    clock.tick(60)