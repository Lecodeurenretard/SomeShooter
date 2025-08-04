from Player import *

EVENT_CREATE_TARGET : int = pygame.USEREVENT + 1	# new event type

player = Player()

clock : pygame.time.Clock = pygame.time.Clock()

def set_timer() -> None:
	"""
	Sets a timer to trigger the target creation event.
	"""
	pygame.time.set_timer(
		EVENT_CREATE_TARGET,
		round(random_number(Target._MIN_SPAWN_TIME, Target._MAX_SPAWN_TIME) * 1000)	# seconds to milliseconds convertion
	)

def draw_frame() -> None:
	window.fill(0xFFFFFF)
	player.draw(window)
	
	for target in Target.get_target_list():
		if target is None:
			continue
		target.draw(window)
	
	window.blit(
		# 
		pygame.font.SysFont(None, 25).render(f"score: {includes.score}", False, 0x000),
		(10, 5)
	)
	
	pygame.display.flip()	# let the frame to be displayed to the screen

set_timer()

# The main loop: everything in the game is executed from here
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		
		if event.type == EVENT_CREATE_TARGET:	# custom events: fires when it's time to create a new target
			Target.spawn_at_random_pos()
			set_timer()
	
	# if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
	if True in pygame.mouse.get_pressed():
		player.shoot()
	player.update()
	
	draw_frame()
	clock.tick(60)