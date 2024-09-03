import pygame


class Weapon:
    # Class attributes defining the weapon's dimensions
    WEAPON_WIDTH = 20
    WEAPON_HEIGHT = 20

    def __init__(self, weapon_x: float, weapon_y: float):
        # Initialize the weapon's position
        self.weapon_x = weapon_x
        self.weapon_y = weapon_y

        # Load the images for the sword swing animation frames
        self.frame_files = [f'images/weapon/sword_swing_{i}.png' for i in range(1, 5)]
        self.frames = [pygame.image.load(file).convert_alpha() for file in self.frame_files]

        # Variables to control the animation
        self.current_frame = 0  # Track the current frame in the animation
        self.animation_time = 0  # Control the timing of frame changes
        self.frame_rate = 10  # Set the speed of the animation
        # Scale the initial image to the weapon's dimensions
        self.image = pygame.transform.scale(self.frames[self.current_frame], (self.WEAPON_WIDTH, self.WEAPON_HEIGHT))

        self.is_swinging = False  # Flag to indicate if the weapon is currently swinging

    def start_swing(self):
        # Start the swinging animation
        self.is_swinging = True
        self.current_frame = 0  # Reset to the first frame of the animation
        self.animation_time = 0  # Reset the animation timer

    def update_animation(self, player):
        # Update the animation if the weapon is swinging
        if self.is_swinging:
            self.animation_time += 1  # Increment the animation timer
            if self.animation_time >= self.frame_rate:
                # Advance to the next frame in the animation
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_time = 0  # Reset the timer

                # Scale the current frame image to the weapon's dimensions
                self.image = pygame.transform.scale(self.frames[self.current_frame],
                                                    (self.WEAPON_WIDTH, self.WEAPON_HEIGHT))

                # If the animation cycle is complete, stop swinging the weapon
                if self.current_frame == 0:
                    self.is_swinging = False
                    player.is_attacking = False  # Reset the player's attack state

    def draw(self, screen, right):
        # Draw the weapon on the screen, adjusting its orientation based on direction
        if not right:
            # Draw the weapon in its original orientation
            self.image = pygame.transform.scale(self.frames[self.current_frame],
                                                (self.WEAPON_WIDTH, self.WEAPON_HEIGHT))
        else:
            # Flip the weapon image horizontally if the player is facing right
            image_original = pygame.transform.scale(self.frames[self.current_frame],
                                                    (self.WEAPON_WIDTH, self.WEAPON_HEIGHT))
            self.image = pygame.transform.flip(image_original, True, False)

        # Draw the weapon image at its current position
        screen.blit(self.image, (self.weapon_x, self.weapon_y))

    def check_collision(self, entity_rect):
        # Check for a collision between the swinging weapon and an entity's rectangle
        if self.is_swinging:
            weapon_rect = pygame.Rect(self.weapon_x, self.weapon_y, self.WEAPON_WIDTH, self.WEAPON_HEIGHT)
            return weapon_rect.colliderect(entity_rect)  # Return True if there's a collision
        return False  # Return False if there's no collision or the weapon isn't swinging
