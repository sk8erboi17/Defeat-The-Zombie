import pygame  # Importing the pygame module for handling graphics and animations

class Enemy:
    # Class attributes defining the enemy's dimensions
    ENEMY_WIDTH = 45
    ENEMY_HEIGHT = 55

    def __init__(self, uuid, enemy_x, enemy_y):
        # Initialize the enemy's unique ID, position, and load animation frames
        self.uuid = uuid  # Unique identifier for the enemy
        self.enemy_x = enemy_x  # X-coordinate of the enemy
        self.enemy_y = enemy_y  # Y-coordinate of the enemy

        # Load the images for the animation frames when moving left
        self.frame_files_left = [f'images/character/enemy/orc_enemy_walk_{i}.png' for i in range(1, 4)]
        self.frames_left = [pygame.image.load(file).convert_alpha() for file in self.frame_files_left]

        # Create the images for moving right by flipping the left movement frames
        self.frames_right = [pygame.transform.flip(frame, True, False) for frame in self.frames_left]

        # Load the image for the idle state
        self.idle_image = pygame.image.load('images/character/enemy/orc_enemy_idle.png').convert_alpha()

        # Variables to control the animation
        self.current_frame = 0  # Track the current frame in the animation
        self.animation_time = 0  # Control the timing of frame changes
        self.frame_rate = 10  # Set the speed of the animation
        self.image = self.idle_image  # Set the initial image of the enemy

        # Movement state flags
        self.is_moving_left = False  # Is the enemy moving left?
        self.is_moving_right = False  # Is the enemy moving right?

    def move_x(self, enemy_x_change):
        # Handle horizontal movement and update movement state flags
        if enemy_x_change < 0:
            # Moving left
            self.is_moving_left = True
            self.is_moving_right = False
        elif enemy_x_change > 0:
            # Moving right
            self.is_moving_left = False
            self.is_moving_right = True
        else:
            # Not moving
            self.is_moving_left = False
            self.is_moving_right = False

        # Update the enemy's x position
        self.enemy_x = self.enemy_x + enemy_x_change
        return self.enemy_x

    def update_animation(self):
        # Update the enemy's animation based on movement direction
        if self.is_moving_left:
            # Update animation if moving left
            self.animation_time += 1
            if self.animation_time >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames_left)
                self.animation_time = 0
                self.image = pygame.transform.scale(self.frames_left[self.current_frame],
                                                    (self.ENEMY_WIDTH, self.ENEMY_HEIGHT))
        elif self.is_moving_right:
            # Update animation if moving right
            self.animation_time += 1
            if self.animation_time >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames_right)
                self.animation_time = 0
                self.image = pygame.transform.scale(self.frames_right[self.current_frame],
                                                    (self.ENEMY_WIDTH, self.ENEMY_HEIGHT))
        else:
            # Set idle image if the enemy is not moving
            self.image = pygame.transform.scale(self.idle_image, (self.ENEMY_WIDTH, self.ENEMY_HEIGHT))

    def draw(self, screen):
        # Draw the enemy's current image on the screen at its position
        screen.blit(self.image, (self.enemy_x, self.enemy_y))
