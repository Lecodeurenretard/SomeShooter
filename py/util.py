from vector import *

def rotate_img(image : pygame.Surface, pos : tuple[int, int], pivot_center_pos : tuple[float, float], angle : float) -> tuple[pygame.Surface, pygame.rect.Rect]:
	"""original function at https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame#upvote-btn-54714144 """
	# offset from pivot to center
	image_rect = image.get_rect(topleft = (pos[0] - pivot_center_pos[0], pos[1]-pivot_center_pos[1]))
	offset_center_to_pivot = Vector(*pos) - Vector(*image_rect.center)
	
	# roatated offset from pivot to center
	rotated_offset = offset_center_to_pivot.rotate(-angle)
	
	# roatetd image center
	rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
	
	# get a rotated image
	rotated_image = pygame.transform.rotate(image, angle)
	rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
	
	return (rotated_image, rotated_image_rect)

def rotate_img_center(image : pygame.Surface, pos : tuple[int, int], angle : float) -> tuple[pygame.Surface, pygame.rect.Rect]:
	return rotate_img(image, pos, image.get_rect().center, angle)

def compare_floats(f1 : float, f2 : float, epsilon : float = .001) -> bool:
	return -epsilon < f1-f2 < epsilon