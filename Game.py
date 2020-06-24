import pygame, sys, random, time
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
clock = pygame.time.Clock()

#functions
def ball_anim():
	global ball_speed_x, ball_speed_y,player_score,opponent_score
	ball.x += ball_speed_x
	ball.y += ball_speed_y
	if ball.top <=0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1
		
	if ball.colliderect(player) or ball.colliderect(opponent):
		pygame.mixer.Sound.play(hit_sound)
		ball_speed_x *= -1
		
	if ball.left <=0:
		pygame.mixer.Sound.play(player_sound)
		ball_restart()
		player_score += 1

	if ball.right>=screen_width:
		pygame.mixer.Sound.play(score_sound)
		ball_restart()
		opponent_score += 1

def ball_restart():
	global ball_speed_y,ball_speed_x
	ball.center = (screen_width/2, screen_height/2)
	ball_speed_x *= random.choice((-1,1))
	ball_speed_y *= random.choice((-1,1)) 
	time.sleep(1)

def player_anim():
	player.y += player_speed
	if player.top<=0:
		player.top = 0 
	if player.bottom>=screen_height:
		player.bottom = screen_height

def opponent_ai():
	#CPU player
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height	

#Layout
screen_width = 1280
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Retro Pong')

#elements
ball = pygame.Rect(screen_width/2-14, screen_height/2-14,28,28)
player = pygame.Rect(screen_width-20, screen_height/2-75,10,150)
opponent = pygame.Rect(10, screen_height/2-75,10,150)

#colors
bg_color = pygame.Color('#2F373F')
light_grey = pygame.Color(255,0,0)
bluish = (27,35,43)

#variables
ball_speed_x = 6*random.choice((-1,1))
ball_speed_y = 6*random.choice((-1,1))
player_speed = 0
opponent_speed = 10
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("Font.ttf", 48)
score_font = pygame.font.Font("Font.ttf", 48)
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
player_sound = pygame.mixer.Sound("ping.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

#main loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed +=7
			if event.key == pygame.K_UP:
				player_speed = -7

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -=7
			if event.key == pygame.K_UP:
				player_speed +=7
		
		if player_score - opponent_score >= 10:
			ball_speed_x+=1
			opponent_speed+=5
			player_speed+=2

	#calling some functions
	ball_anim()
	player_anim()
	opponent_ai()

	# Visuals 
	screen.fill(bg_color)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, (255,0,0), opponent)
	pygame.draw.ellipse(screen, (255,255,255), ball)
	pygame.draw.line(screen, bluish, (screen_width/2,110), (screen_width/2,screen_height),5)
	pygame.draw.line(screen, bluish, (screen_width/2,0), (screen_width/2,64),5)

	#displayed text
	text = score_font.render("SCORE",False,(0,255,0))
	screen.blit(text,(screen_width/2-82,70))
	player_text = game_font.render(f"{player_score}",False,(255,255,255))
	screen.blit(player_text,(660,120))
	opponent_text = game_font.render(f"{opponent_score}",False,(255,255,255))
	screen.blit(opponent_text,(600,120))

	#cycles
	pygame.display.flip()
	clock.tick(60)
