from Bullet import *

class Player:
	def __init__(self):
		self._pos	: Vector = Vector(WIN_WIDTH // 2, WIN_HEIGHT // 2)	# preceding underscore to mark as private
		self._sprite : pygame.Surface = pygame.image.load("img/character.png")
		self._active_bullets : list[Bullet] = []
	
	@property
	def _mouse_dir(self) -> Vector:
		direction = self._pos - Vector(*pygame.mouse.get_pos())
		return direction.normalize()	# so the norm is 1


	def draw(self, surface : pygame.Surface) -> None:
		for bullet in self._active_bullets:
			bullet.draw(surface)
		
		surface.blit(*rotate_img_center(self._sprite, self._pos.tuple_2D, (-self._mouse_dir).argument() + 10))
	
	def update(self) -> None:
		for i, bullet in enumerate(self._active_bullets):
			bullet.update()
			if bullet.to_destroy:
				self._active_bullets.pop(i)
	
	def shoot(self) -> None:
		self._active_bullets.append(
			Bullet(self._mouse_dir, self._pos)
		)