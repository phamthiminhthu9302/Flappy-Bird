import pygame, sys, random
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
screen= pygame.display.set_mode((432,768))
pygame.display.set_caption("Flappy Bird")
fps=60
clock = pygame.time.Clock()
game_font = pygame.font.Font('FileGame/04B_19.ttf',60)
score_font = pygame.font.Font('FileGame/04B_19.ttf',35)
#Tạo các biến cho trò chơi
gravity = 0.4
bird_movement = 0
game_active = 1
game_start = 1
score = 0
high_score = 0
count_start=0
#load button images
start_img = pygame.image.load('FileGame/assets/start_btn.png').convert_alpha()
exit_img = pygame.image.load('FileGame/assets/exit_btn.png').convert_alpha()
#chèn background
bg = pygame.image.load('FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#chèn sàn
floor = pygame.image.load('FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,360))
#tạo timer cho bird
birdflap = pygame.USEREVENT+1
pygame.time.set_timer(birdflap,200)
#tạo ống
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
pipe_pass =[]
pipe_height = [300,400,500]
#tạo timer
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 2000)
#Tạo màn hình bắt đầu
repare_surface = (pygame.image.load('FileGame/assets/flappybird.png').convert_alpha())
repare_rect = repare_surface.get_rect(center=(216,250))
start_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png').convert_alpha())
start_rect = start_surface.get_rect(center=(216,300))
score_surface_ =(pygame.image.load('FileGame/assets/panel_score.png').convert_alpha())
score_rect_ = score_surface_.get_rect(center=(216,330))
game_message_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png').convert_alpha())
game_messager_rect = game_message_surface.get_rect(center=(216,384))
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,200))
replay = pygame.transform.scale2x(pygame.image.load('FileGame/assets/button_ok.png').convert_alpha())
#Chèn âm thanh
start_sound = pygame.mixer.Sound('FileGame/sound/sfx_swooshing.wav')
flap_sound = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('FileGame/sound/sfx_point.wav')
die_sound = pygame.mixer.Sound('FileGame/sound/sfx_die.wav')
#Tạo hàm cho trò chơi
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()/2
		height = image.get_height()/2
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action
start_button = Button(150, 450, start_img, 0.8)
play_button = Button(100, 420, replay, 1)
exit_bt = Button(250, 420, exit_img, 0.67)
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-660))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes :
		pipe.centerx -= 3
	return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 : 
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pi in pipes:
        if  bird_rect.colliderect(pi):
            hit_sound.play()
            return 1
        if  bird_rect.centery>= 610 :
            hit_sound.play()  
            return 2
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*5,1)
	return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def display(game_state):  
    if game_state =='repare game':
        screen.blit(repare_surface,repare_rect)
    if game_state =='start game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
        screen.blit(start_surface,start_rect)
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        screen.blit(game_over_surface,game_over_rect)
        screen.blit(score_surface_,score_rect_)
        score_surface = score_font.render(f' {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (300,313))
        screen.blit(score_surface,score_rect)
        high_score_surface = score_font.render(f'{int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (308,366))
        screen.blit(high_score_surface,high_score_rect)
def count_score(pipes,pipe_pass):
    global score
    for pipe in pipes:
        if pipe not in pipe_pass:
            if pipe.right < bird_rect.left:
                pipe_pass.append(pipe)
                score += 0.5  
                score_sound.play()       
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
#while loop của trò chơi
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if  event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]==True:
                    if  game_active==2 :
                        bird_movement =-6
                        flap_sound.play()    
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap and game_start==2 or game_active==2 :
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0 
            bird, bird_rect = bird_animation() 
    screen.blit(bg,(0,0))
    if game_start==1 :
        display('repare game')
        if start_button.draw(screen):
            game_start=2
            start_sound.play()
    if game_start==2 :
        display('start game')
        screen.blit( bird,bird_rect)
        if pygame.mouse.get_pressed()[0]==True:
            count_start+=1
            if(8<count_start<15):
                game_active=2
                count_start=0
                game_start=3   
    if game_active==2 :
        screen.blit(bg,(0,0))
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        bird_movement += gravity
        bird_rect.centery += bird_movement+gravity*0.5
        if bird_rect.centery>=590:
                rotated_bird=pygame.transform.rotozoom(bird,-90,1)
        else:
                rotated_bird = rotate_bird(bird)
        screen.blit( rotated_bird ,bird_rect)
        if check_collision(pipe_list)==1 or check_collision(pipe_list)==2:
            if check_collision(pipe_list)==1:
                game_active=3
            else:
                game_active=4
        count_score(pipe_list,pipe_pass)
        display('main game')
    if game_active==3 :
        draw_pipe(pipe_list)
        bird_movement += gravity
        bird_rect.centery += bird_movement+gravity*0.5
        screen.blit(pygame.transform.rotozoom(bird,-90,1), bird_rect)
        if(bird_rect.centery>=pipe_surface.get_height()):
                die_sound.play()
        if(bird_rect.centery>=610):
                music_count=0
                game_active=4
    if game_active==4 :
            draw_pipe(pipe_list)
            display('game over')
            if play_button.draw(screen):
                game_start=1
                game_active=1
                pipe_list.clear()
                pipe_pass.clear()
                start_sound.play()
                score = 0
                bird_rect.center = (100,360) 
                bird_movement =0
                music_count=0
                screen.blit(bg,(0,0))
            if exit_bt.draw(screen):
                pygame.quit()
                sys.exit() 
            screen.blit(pygame.transform.rotozoom(bird,-90,1), bird_rect)
            high_score = update_score(score,high_score)
    
    floor_x_pos -= 3
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0
    pygame.display.update()
    clock.tick(fps)