from util import *

Foxy : type
class Target:
	_TARGET_LIST_CHUNK_SIZE : int = 10
	target_list : 'list[Target|None]' = [None for _ in range(_TARGET_LIST_CHUNK_SIZE)]
	
	_MIN_SPAWN_TIME : float = .6
	_MAX_SPAWN_TIME : float = 1.0
	
	ID_WAITING_GARBAGE_COLLECTOR : int = -1
	
	def __init__(self, pos : Vector) -> None:
		self._sprite : pygame.Surface = pygame.image.load("../img/target.png")
		self._sprite = pygame.transform.scale_by(self._sprite, .5)  # in the scratch project, their size is also halved
		
		self._mask : pygame.Mask = pygame.mask.from_surface(self._sprite) # https://www.reddit.com/r/pygame/comments/oiknmp/collision_with_rotated_rectangles/
		
		self._pos = pos
		
		self._id = -1
		Target._add_to_target_list(self)
	
	@staticmethod
	def get_target_list() -> 'list[Target|None]':
		return Target.target_list
	
	@staticmethod
	def isset_target_list_index(index : int) -> bool:
		return index < len(Target.target_list) and Target.target_list[index] is not None
	
	@staticmethod
	def _get_empty_chunk() -> list[None]:
		return [None for _ in range(Target._TARGET_LIST_CHUNK_SIZE)]
	
	@staticmethod
	def _add_to_target_list(target : 'Target') -> None:
		"""Add a new target to _target_list and expand it if nescessary."""
		for i, elem in enumerate(Target.target_list):
			if elem is None:
				target._id = i
				Target.target_list[i] = target
				return
		
		# else expand
		target._id = len(Target.target_list)
		Target.target_list += Target._get_empty_chunk()
		Target.target_list[target._id] = target
		
		# Could add a case to free memory but this is already too complicated
	
	
	
	@staticmethod
	def spawn_at_random_pos() -> 'Target':
		return Target(Vector.create_random_pos_in_window())
	
	@property
	def mask(self) -> pygame.Mask:
		return self._mask
	
	@property
	def _dimensions(self) -> Vector:
		rect = self._sprite.get_bounding_rect()
		return Vector(rect.width, rect.height)

	@property
	def _centered_pos(self) -> Vector:
		return self._pos + self._dimensions/2
	
	@_centered_pos.setter
	def _centered_pos(self, val : Vector) -> None:
		self._pos = val - self._dimensions/2
	
	def _center(self) -> None:
		self._centered_pos = self._pos
	
	def die(self) -> None:
		if self._id == Target.ID_WAITING_GARBAGE_COLLECTOR:
			return
	
		assert(0 <= self._id < len(Target.target_list)), f"Incorrect index '{self._id}' for dying Target object."
		Target.target_list[self._id] = None   # the garbage collector should delete self a short time after
		self._id = Target.ID_WAITING_GARBAGE_COLLECTOR
	
	
	def update(self, *args) -> None:
		pass
	def draw(self, surface : pygame.Surface) -> None:
		surface.blit(self._sprite, self._pos.tuple_2D)
	
	def calculate_offset(self, other_point : Vector) -> Vector:
		return self._pos - other_point

class Foxy(Target):
	def __init__(self, pos : Vector) -> None:
		super().__init__(pos)
		self._sprite : pygame.Surface = pygame.image.load("../img/foxy.png")
		self._sprite = pygame.transform.scale(self._sprite, (90, 90))

		self._speed : float = 5

		direction = Vector(0, 100).rotate(self._pos.argument())
		while is_in_bounds(self._pos.tuple_2D):
			self._pos += direction
	
	@staticmethod
	def spawn_at_random_pos() -> 'Target':
		pos : Vector = Vector.create_random_pos_in_window()
		
		if randint(1, 10) == 1:
			return Foxy(pos)
		return Target(pos)
	
	@staticmethod
	def jumpscare():
		pygame.mixer_music.load("jumpscare-sound.mp3")
		pygame.mixer_music.set_volume(1)
		pygame.mixer_music.play()
		
		play_gif("../img/jumpscare/frame_", (0, 0, WIN_WIDTH, WIN_HEIGHT), .1, 0, 13)
		sleep(1)
		pygame.quit()
		exit()
	
	def update(self, player_mask : pygame.Mask) -> None:
		dir : Vector = (SCREEN_CENTER - self._centered_pos).normalize()
		self._pos += dir * self._speed	# type: ignore # Returns an int only if the two factors are vectors
		
		if self._mask.overlap(player_mask, self.calculate_offset(SCREEN_CENTER).tuple_2D):
			Foxy.jumpscare()
