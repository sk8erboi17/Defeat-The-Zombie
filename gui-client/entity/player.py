import pygame
import string
from entity.weapon import Weapon

class Player:
    # Class attributes defining the player's dimensions
    PLAYER_WIDTH = 32
    PLAYER_HEIGHT = 40

    def __init__(self, name: string, player_x: float, player_y: float, is_jumping: bool, is_attacking: bool, is_dead: bool):
        # Initialize player's position, state flags, and name
        self.player_x = player_x
        self.player_y = player_y
        self.is_jumping = is_jumping
        self.is_attacking = is_attacking
        self.is_dead = is_dead
        self.name = name

        # Load the images for the animation frames when moving left
        self.frame_files_left = [f'images/character/player/walk_left_{i}.png' for i in range(1, 5)]
        self.frames_left = [pygame.image.load(file).convert_alpha() for file in self.frame_files_left]

        # Create the images for moving right by flipping the left movement frames
        self.frames_right = [pygame.transform.flip(frame, True, False) for frame in self.frames_left]

        # Load the image for the idle state
        self.idle_image = pygame.image.load('images/character/player/player_idle.png').convert_alpha()

        # Variables to control the animation
        self.current_frame = 0  # Track the current frame in the animation
        self.animation_time = 0  # Control the timing of frame changes
        self.frame_rate = 10  # Set the speed of the animation
        self.image = self.idle_image  # Set the initial image of the player

        # Movement state flags
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_idle = True

        # Initialize the weapon for the player (e.g., a sword)
        self.weapon = Weapon(self.player_x, self.player_y)

    def move_x(self, player_x_change):
        # Handle horizontal movement and update weapon position accordingly
        if player_x_change < 0:
            # Moving left
            self.is_moving_left = True
            self.is_moving_right = False
            self.is_idle = False
            self.weapon.weapon_x = self.player_x - 2.5 - 15
        elif player_x_change > 0:
            # Moving right
            self.is_moving_left = False
            self.is_moving_right = True
            self.is_idle = False
            self.weapon.weapon_x = self.player_x + 2.5 + 25
        else:
            # Not moving
            self.is_moving_left = False
            self.is_moving_right = False
            self.is_idle = True

        self.player_x += player_x_change  # Update player's x position
        self.update_animation()  # Update the player's animation based on movement
        return self.player_x

    def move_y(self, player_y_change):
        # Handle vertical movement and update weapon position accordingly
        self.player_y += player_y_change
        self.weapon.weapon_y = self.player_y + 15
        return self.player_y

    def jump(self, player_jump_change):
        # Handle jumping
        if not self.is_jumping:
            self.player_y += player_jump_change
            self.is_jumping = True

    def attack(self):
        # Start the attack animation for the weapon
        self.weapon.start_swing()

    def set_name(self, name: string):
        # Set the player's name
        self.name = name
        return self.name

    def update_animation(self):
        # Update the player's animation based on movement direction
        if self.is_moving_left:
            # Update animation if moving left
            self.animation_time += 1
            if self.animation_time >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames_left)
                self.animation_time = 0
                self.image = pygame.transform.scale(self.frames_left[self.current_frame], (self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
                # Reset movement state if the animation cycle is complete
                if self.current_frame == len(self.frames_left) - 1:
                    self.is_moving_left = False
                    self.is_idle = True
        elif self.is_moving_right:
            # Update animation if moving right
            self.animation_time += 1
            if self.animation_time >= self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames_right)
                self.animation_time = 0
                self.image = pygame.transform.scale(self.frames_right[self.current_frame], (self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
                # Reset movement state if the animation cycle is complete
                if self.current_frame == len(self.frames_right) - 1:
                    self.is_moving_right = False
                    self.is_idle = True
        elif self.is_idle:
            # Set idle image if the player is not moving
            self.image = pygame.transform.scale(self.idle_image, (self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
            self.current_frame = 0
            self.animation_time = 0

        # Update the animation for the player's weapon
        self.weapon.update_animation(self)

    def draw(self, screen):
        # Draw the player's current image on the screen
        screen.blit(self.image, (self.player_x, self.player_y))

        # Draw the weapon on the screen, adjusting its position based on movement direction
        self.weapon.draw(screen, self.is_moving_right)

        # Draw the player's name above their image on the screen
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.name, True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(self.player_x + self.PLAYER_WIDTH // 2, self.player_y - 10))
        screen.blit(text, text_rect)
