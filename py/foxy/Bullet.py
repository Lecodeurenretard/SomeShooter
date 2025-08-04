from Target import *

class Bullet:
	_WIDTH = 1
	_HEIGHT = 75
	_SPEED = 15
	
	def __init__(self, dir : Vector, pos : Vector):
		assert(compare_floats(dir.norm(), 1)), "Normalize the direction vector"		# always a pleasure to compare floats

		self._direction = dir
		self._pos = pos
		self._request_destruction : bool = False
		
		self._sprite : pygame.Surface = pygame.Surface((Bullet._WIDTH, Bullet._HEIGHT), pygame.SRCALPHA)
		self._sprite.fill((0, 255, 243, 255))
		self._sprite = rotate_img_center(self._sprite, self._centered_pos.tuple_2D, self._direction.argument())[0]

	@property
	def _mask(self) -> pygame.Mask:	# access with self._mask
		return pygame.mask.from_surface(self._sprite)

	@property
	def to_destroy(self) -> bool:
		"""If the parent object should destroy the bullet."""
		bad_x : bool = not 0 <= self._pos.x < WIN_WIDTH
		bad_y : bool = not 0 <= self._pos.y < WIN_HEIGHT

		return self._request_destruction or bad_x or bad_y
	
	@property
	def _centered_pos(self) -> Vector:
		return self._pos - Vector(self._sprite.get_rect().width, self._sprite.get_rect().height) / 2
	
	def _handle_target_collision(self) -> None:
		for target in Target.get_target_list():
			if target is None:
				continue
			if self._mask.overlap(target._mask, target.calculate_offset(self._pos).tuple_2D) is not None:	# Check for collisions with a target
				includes.score += 20
				target.die()
				self._request_destruction = True
	
	def update(self) -> None:
		self._pos -= self._direction * Bullet._SPEED	# no delta time bc can't bother
		self._handle_target_collision()
	
	def draw(self, surface : pygame.Surface) -> None:
		surface.blit(self._sprite, (self._centered_pos).tuple_2D)