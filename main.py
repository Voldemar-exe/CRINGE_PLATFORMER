"""
Platformer Game
"""

import arcade
import os

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.6
CHARACTER_SCALING = TILE_SCALING * 0.4
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 128
PLAYER_START_Y = 128

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
	"""
    Load a texture pair, with the second being a mirror image.
    """
	return [
		arcade.load_texture(filename),
		arcade.load_texture(filename, flipped_horizontally=True)
	]


class PlayerCharacter(arcade.Sprite):
	""" Player Sprite"""

	def __init__(self):

		# Set up parent class
		super().__init__()

		# Default to face-right
		self.character_face_direction = RIGHT_FACING

		# Used for flipping between image sequences
		self.cur_texture = 0
		self.scale = CHARACTER_SCALING

		# Track our state
		self.jumping = False
		self.climbing = False
		self.is_on_ladder = False

		# --- Load Textures ---
		main_path = "Images/anon"

		# Load textures for idle standing
		self.idle_texture_pair = load_texture_pair(f"{main_path}idle.png")
		self.jump_texture_pair = load_texture_pair(f"{main_path}jump.png")
		self.fall_texture_pair = load_texture_pair(f"{main_path}fall.png")

		# Load textures for walking
		self.walk_textures = []
		for i in range(1, 5):
			texture = load_texture_pair(f"{main_path}move{i}.png")
			self.walk_textures.append(texture)

		# Set the initial texture
		self.texture = self.idle_texture_pair[0]

		# Hit box will be set based on the first image used. If you want to specify
		# a different hit box, you can do it like the code below.
		# self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
		self.set_hit_box(self.texture.hit_box_points)

	def update_animation(self, delta_time: float = 1 / 60):

		# Figure out if we need to flip face left or right
		if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
			self.character_face_direction = LEFT_FACING
		elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
			self.character_face_direction = RIGHT_FACING

		# Climbing animation
		if self.is_on_ladder:
			self.climbing = True
		if not self.is_on_ladder and self.climbing:
			self.climbing = False
		if self.climbing and abs(self.change_y) > 1:
			self.cur_texture += 1
			if self.cur_texture > 7:
				self.cur_texture = 0
		if self.climbing:
			self.texture = self.climbing_textures[self.cur_texture // 4]
			return

		# Jumping animation
		if self.change_y > 0 and not self.is_on_ladder:
			self.texture = self.jump_texture_pair[self.character_face_direction]
			return
		elif self.change_y < 0 and not self.is_on_ladder:
			self.texture = self.fall_texture_pair[self.character_face_direction]
			return

		# Idle animation
		if self.change_x == 0:
			self.texture = self.idle_texture_pair[self.character_face_direction]
			return

		# Walking animation
		self.cur_texture += 1
		if self.cur_texture > 3:
			self.cur_texture = 0
		self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class Wolf(arcade.Sprite):
	""" Player Sprite"""

	def __init__(self):

		# Set up parent class
		super().__init__()

		# Default to face-right
		self.character_face_direction = RIGHT_FACING

		# Used for flipping between image sequences
		self.cur_texture = 0
		self.scale = CHARACTER_SCALING

		# Track our state
		self.jumping = False
		self.climbing = False
		self.is_on_ladder = False

		# --- Load Textures ---
		main_path = "Images/wolf"

		# Load textures for idle standing
		self.idle_texture_pair = load_texture_pair(f"{main_path}move2.png")
		# Load textures for walking
		self.walk_textures = []
		for i in range(1, 5):
			texture = load_texture_pair(f"{main_path}move{i}.png")
			self.walk_textures.append(texture)

		# Set the initial texture
		self.texture = self.idle_texture_pair[0]

		# Hit box will be set based on the first image used. If you want to specify
		# a different hit box, you can do it like the code below.
		# self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
		self.set_hit_box(self.texture.hit_box_points)

	def update_animation(self, delta_time: float = 1 / 60):

		# Figure out if we need to flip face left or right
		if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
			self.character_face_direction = LEFT_FACING
		elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
			self.character_face_direction = RIGHT_FACING

		# Walking animation
		self.cur_texture += 1
		if self.cur_texture > 3:
			self.cur_texture = 0
		self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class Socol(arcade.Sprite):
	""" Player Sprite"""

	def __init__(self):

		# Set up parent class
		super().__init__()

		# Default to face-right
		self.character_face_direction = RIGHT_FACING

		# Used for flipping between image sequences
		self.cur_texture = 0
		self.scale = CHARACTER_SCALING

		# Track our state
		self.jumping = False
		self.climbing = False
		self.is_on_ladder = False

		# --- Load Textures ---
		main_path = "Images/sokol"

		# Load textures for idle standing
		self.idle_texture_pair = load_texture_pair(f"{main_path}move2.png")
		# Load textures for walking
		self.walk_textures = []
		for i in range(1, 5):
			texture = load_texture_pair(f"{main_path}move{i}.png")
			self.walk_textures.append(texture)

		# Set the initial texture
		self.texture = self.idle_texture_pair[0]

		# Hit box will be set based on the first image used. If you want to specify
		# a different hit box, you can do it like the code below.
		# self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
		self.set_hit_box(self.texture.hit_box_points)

	def update_animation(self, delta_time: float = 1 / 60):

		# Figure out if we need to flip face left or right
		if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
			self.character_face_direction = LEFT_FACING
		elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
			self.character_face_direction = RIGHT_FACING

		# Walking animation
		self.cur_texture += 1
		if self.cur_texture > 3:
			self.cur_texture = 0
		self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class MyGame(arcade.Window):
	"""
    Main application class.
    """

	def __init__(self):
		"""
        Initializer for the game
        """

		# Call the parent class and set up the window
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

		# Set the path to start with this program
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)

		# Track the current state of what key is pressed
		self.left_pressed = False
		self.right_pressed = False
		self.up_pressed = False
		self.down_pressed = False
		self.jump_needs_reset = False

		# These are 'lists' that keep track of our sprites. Each sprite should
		# go into a list.
		self.coin_list = None
		self.wall_list = None
		self.background_list = None
		self.background = None
		self.ladder_list = None
		self.player_list = None
		self.enemy_list = None
		self.enemy = None
		self.enemy1 = None

		# Separate variable that holds the player sprite
		self.player_sprite = None

		# Our 'physics' engine
		self.physics_engine = None
		self.physics_engine_enemy = None

		# Used to keep track of our scrolling
		self.view_bottom = 0
		self.view_left = 0

		self.end_of_map = 0

		# Keep track of the score
		self.score = 0

	# Load sounds

	def setup(self):
		""" Set up the game here. Call this function to restart the game. """

		# Used to keep track of our scrolling
		self.view_bottom = 0
		self.view_left = 0

		# Keep track of the score
		self.score = 0

		# Create the Sprite lists
		self.player_list = arcade.SpriteList()
		self.wall_list = arcade.SpriteList()
		self.enemy_list = arcade.SpriteList()

		# Set up the player, specifically placing it at these coordinates.
		self.player_sprite = PlayerCharacter()

		self.player_sprite.center_x = PLAYER_START_X
		self.player_sprite.center_y = PLAYER_START_Y
		self.player_list.append(self.player_sprite)
		# enemy
		self.enemy = Wolf()
		self.enemy.bottom = SPRITE_PIXEL_SIZE * 3
		self.enemy.left = SPRITE_PIXEL_SIZE
		self.enemy.boundary_right = 1000
		self.enemy.boundary_left = 0
		# Set enemy initial speed
		self.enemy.change_x = 4
		self.enemy_list.append(self.enemy)
		self.enemy1 = Socol()
		self.enemy1.bottom = SPRITE_PIXEL_SIZE * 3
		self.enemy1.left = SPRITE_PIXEL_SIZE
		self.enemy1.boundary_right = 1000
		self.enemy1.boundary_left = 0
		# Set enemy initial speed
		self.enemy1.change_x = 8
		self.enemy_list.append(self.enemy1)

		# Name of the layer in the file that has our platforms/walls
		platforms_layer_name = 'Ground'

		# Name of the layer that has items for pick-up
		coins_layer_name = 'Collectable_Items'

		# Map name
		map_name = "Tiles/MAP0.tmx"

		# Read in the tiled map
		my_map = arcade.tilemap.read_tmx(map_name)

		# Calculate the right edge of the my_map in pixels
		self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

		# -- Platforms
		self.wall_list = arcade.tilemap.process_layer(my_map,
		                                              platforms_layer_name,
		                                              TILE_SCALING,
		                                              use_spatial_hash=True)

		# -- Moving Platforms

		# -- Background objects

		# -- Background objects

		# -- Coins
		self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name,
		                                              TILE_SCALING,
		                                              use_spatial_hash=True)

		# --- Other stuff
		# Set the background
		self.background = arcade.load_texture("Tiles/forest_background.png")
		# Create the 'physics engine'
		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
		                                                     self.wall_list,
		                                                     gravity_constant=GRAVITY)
		self.physics_engine_enemy = arcade.PhysicsEnginePlatformer(self.enemy,
		                                                     self.wall_list,
		                                                     gravity_constant=GRAVITY)


	def on_draw(self):
		""" Render the screen. """

		# Clear the screen to the background color
		arcade.start_render()
		# Draw our sprites
		# Draw the background texture
		arcade.draw_lrwh_rectangle_textured(self.view_left, self.view_bottom,
		                                    SCREEN_WIDTH, SCREEN_HEIGHT,
		                                    self.background)
		self.wall_list.draw()
		self.coin_list.draw()
		self.enemy_list.draw()
		self.player_list.draw()
		self.player_sprite.draw_hit_box((255, 0, 0), 5)

		# Draw our score on the screen, scrolling it with the viewport
		score_text = f"Score: {self.score}"
		arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
		                 arcade.csscolor.BLACK, 18)

	# Draw hit boxes.
	# for wall in self.wall_list:
	#     wall.draw_hit_box(arcade.color.BLACK, 3)
	#
	# self.player_sprite.draw_hit_box(arcade.color.RED, 3)

	def process_keychange(self):
		"""
        Called when we change a key up/down or we move on/off a ladder.
        """
		# Process up/down
		if self.up_pressed and not self.down_pressed:
			if self.physics_engine.is_on_ladder():
				self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
			elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
				self.player_sprite.change_y = PLAYER_JUMP_SPEED
				self.jump_needs_reset = True
		elif self.down_pressed and not self.up_pressed:
			if self.physics_engine.is_on_ladder():
				self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

		# Process up/down when on a ladder and no movement
		if self.physics_engine.is_on_ladder():
			if not self.up_pressed and not self.down_pressed:
				self.player_sprite.change_y = 0
			elif self.up_pressed and self.down_pressed:
				self.player_sprite.change_y = 0

		# Process left/right
		if self.right_pressed and not self.left_pressed:
			self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
		elif self.left_pressed and not self.right_pressed:
			self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
		else:
			self.player_sprite.change_x = 0

	def on_key_press(self, key, modifiers):
		"""Called whenever a key is pressed. """

		if key == arcade.key.UP or key == arcade.key.W:
			self.up_pressed = True
		elif key == arcade.key.DOWN or key == arcade.key.S:
			self.down_pressed = True
		elif key == arcade.key.LEFT or key == arcade.key.A:
			self.left_pressed = True
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.right_pressed = True

		self.process_keychange()

	def on_key_release(self, key, modifiers):
		"""Called when the user releases a key. """

		if key == arcade.key.UP or key == arcade.key.W:
			self.up_pressed = False
			self.jump_needs_reset = False
		elif key == arcade.key.DOWN or key == arcade.key.S:
			self.down_pressed = False
		elif key == arcade.key.LEFT or key == arcade.key.A:
			self.left_pressed = False
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.right_pressed = False

		self.process_keychange()

	def on_update(self, delta_time):
		""" Movement and game logic """

		# Move the player with the physics engine
		self.physics_engine.update()
		self.physics_engine_enemy.update()
		self.enemy.update()
		self.enemy1.update()
		# reset the images when they go past the screen
		# Update animations
		if self.physics_engine.can_jump():
			self.player_sprite.can_jump = False
		else:
			self.player_sprite.can_jump = True

		if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
			self.player_sprite.is_on_ladder = True
			self.process_keychange()
		else:
			self.player_sprite.is_on_ladder = False
			self.process_keychange()

		self.coin_list.update_animation(delta_time)
		self.enemy_list.update_animation(delta_time)
		self.player_list.update_animation(delta_time)

		# Update walls, used with moving platforms

		# See if we hit any coins

		# Loop through each coin we hit (if any) and remove it
		for enemy in self.enemy_list:
			# If the enemy hit a wall, reverse
			if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
				enemy.change_x *= -1
			# If the enemy hit the left boundary, reverse
			elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
				enemy.change_x *= -1
			# If the enemy hit the right boundary, reverse
			elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
				enemy.change_x *= -1

		# Track if we need to change the viewport
		changed_viewport = False

		# --- Manage Scrolling ---

		# Scroll left
		left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
		if self.player_sprite.left < left_boundary:
			self.view_left -= left_boundary - self.player_sprite.left
			changed_viewport = True

		# Scroll right
		right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
		if self.player_sprite.right > right_boundary:
			self.view_left += self.player_sprite.right - right_boundary
			changed_viewport = True

		# Scroll up
		top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
		if self.player_sprite.top > top_boundary:
			self.view_bottom += self.player_sprite.top - top_boundary
			changed_viewport = True

		# Scroll down
		bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
		if self.player_sprite.bottom < bottom_boundary:
			self.view_bottom -= bottom_boundary - self.player_sprite.bottom
			changed_viewport = True

		if changed_viewport:
			# Only scroll to integers. Otherwise we end up with pixels that
			# don't line up on the screen
			self.view_bottom = int(self.view_bottom)
			self.view_left = int(self.view_left)

			# Do the scrolling
			arcade.set_viewport(self.view_left,
			                    SCREEN_WIDTH + self.view_left,
			                    self.view_bottom,
			                    SCREEN_HEIGHT + self.view_bottom)
		if self.player_sprite.center_y < -1000:
			self.view_bottom = 0
			self.view_left = 0
			self.player_sprite.center_y = 128
			self.player_sprite.center_x = 128
		if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
			pass


def main():
	""" Main method """
	window = MyGame()
	window.setup()
	arcade.run()


if __name__ == "__main__":
	main()
