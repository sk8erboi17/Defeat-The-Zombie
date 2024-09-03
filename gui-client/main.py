import threading
import pygame
import uuid

from entity.player import Player
from gui.gui import Gui
from network.client_socket import ClientSocket
from network.socket_packets import packets
from textures.textures_loader import TextureLoader
from world.world import World


class Game:
    def __init__(self):
        # Initialize the game and all necessary components
        self._initialize_pygame()
        self._initialize_network()
        self._initialize_screen()
        self._load_textures()
        self._initialize_entities()

    def _initialize_pygame(self):
        # Initialize pygame and set up the clock for framerate control
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

    def _initialize_network(self):
        # Initialize the connection to the server and start a thread for continuous message reception
        self.client_socket = ClientSocket(self)
        self.client_socket.connect()

        # Create and start a daemon thread to handle incoming messages from the server
        self.receive_thread = threading.Thread(target=self.client_socket.receive_response_continuously, daemon=True)
        self.receive_thread.start()

    def _initialize_screen(self):
        # Set up the game window and the GUI
        self.screen = pygame.display.set_mode((800, 600))
        Gui.initialize_icon("images/icon/ico.png")
        Gui.set_title("Game")

    def _load_texture(self, path, width, height):
        # Load a texture from a specified path and print its details
        texture_loader = TextureLoader(path, width, height)
        print(f"Loaded texture {path} with size: {width} x {height}")
        return texture_loader.load()

    def _load_textures(self):
        # Load all necessary textures for the game
        self.player_texture = self._load_texture('images/character/player/player_idle.png', Player.PLAYER_WIDTH,
                                                 Player.PLAYER_HEIGHT)
        self.grass_texture = self._load_texture('images/world/grass.png', 16, 16)
        self.dirt_texture = self._load_texture('images/world/dirt.png', 16, 16)
        self.bg_scaled = self._scale_image("images/background.png", (Gui.SCREEN_WIDTH, Gui.SCREEN_HEIGHT // 1.12))
        self.tree = self._scale_image("images/world/tree.png", (198, 198))

    def _scale_image(self, path, size):
        # Load and resize an image to the specified dimensions
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def _initialize_entities(self):
        # Initialize game entities like the main player and the game world
        self.main_player = Player(Gui.user_text, 300, 480, False, False, False)
        self.world = World()
        self.world.spawn_player(self.main_player)

    def _handle_player_movement(self):
        # Handle player movement based on user input
        x_change = 0
        keys = pygame.key.get_pressed()

        # Handle horizontal movement (left/right)
        if keys[pygame.K_d]:
            x_change += 2.5
        elif keys[pygame.K_a]:
            x_change -= 2.5

        # Handle vertical movement (up/down) and jumping
        if keys[pygame.K_s]:
            self.main_player.move_y(2.5)
        elif keys[pygame.K_w]:
            if not self.main_player.is_jumping:
                self.main_player.move_y(-40)
            self.main_player.is_jumping = True

        # Handle player attack
        if keys[pygame.K_SPACE]:
            if not self.main_player.is_attacking:
                self.main_player.attack()
                self.main_player.is_attacking = True

        # Apply the position change to the player
        self.main_player.move_x(x_change)

        # If the player moved, send a message to the server to update the position
        if x_change != 0:
            movement_message = packets.MOVEMENT_PACKET_OUT.message.format(self.main_player.name,
                                                                          self.main_player.player_x,
                                                                          self.main_player.player_y)
            self.client_socket.send_message(packets.MOVEMENT_PACKET_OUT.byte_mark, movement_message)

    def handle_events(self):
        # Handle user input events and other system events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit the game if the window is closed
            Gui.handle_input_events(self.screen, self.main_player, event, self.client_socket)

        # If the player name is set, handle player movement
        if Gui.NAME_PRESENT:
            self._handle_player_movement()

    def update(self):
        # Update the state of the game world (enemies, collisions, players)
        self.world.update_enemies()
        self.world.check_collisions(self.main_player, self.client_socket)
        self.world.update_players()

    def draw(self):
        # Draw all game elements on the screen
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        self.screen.blit(self.bg_scaled, (0, 0))  # Draw the background
        self.screen.blit(self.tree, (200, 320))  # Draw a tree

        # Draw enemies
        for enemy in self.world.enemies:
            enemy.draw(self.screen)

        # Draw world blocks (e.g., dirt, grass) and players
        self.world.draw_chunk(self.screen, self.grass_texture, self.dirt_texture)
        self.world.draw_players(self.screen)

        pygame.display.flip()  # Update the display with everything drawn

    def _handle_player_joined(self, message):
        # Handle a new player joining the game
        parts = message.split(":")
        name, x_cord, y_cord = parts[1], float(parts[2]), float(parts[3])
        print(f"Joined new player: {name}, {x_cord}, {y_cord}")
        new_player = Player(name, x_cord, y_cord, False, False, False)
        self.world.spawn_player(new_player)
        new_player.draw(self.screen)

    def _handle_movement(self, message):
        # Handle another player's movement received from the server
        parts = message.split(":")
        name = parts[1]
        try:
            x_cord, y_cord = float(parts[2]), float(parts[3])
        except ValueError:
            return

        for player in self.world.players:
            if player.name == self.main_player.name:
                continue
            if player.name == name:
                player.move_x(x_cord - player.player_x)
                player.player_y = y_cord
                self.world.update_players()

    def _handle_spawn_enemy(self, message):
        # Handle the spawning of an enemy in the game world
        parts = message.split(":")
        uuid_from_string, x_cord, y_cord = uuid.UUID(parts[1]), float(parts[2]), float(parts[3])
        self.world.spawn_enemy(uuid_from_string, x_cord, y_cord)
        self.world.update_enemies()

    def _handle_remove_enemy(self, message):
        # Handle the removal of an enemy from the game world
        parts = message.split(":")
        uuid_from_string = uuid.UUID(parts[1])
        self.world.remove_enemy(uuid_from_string)

    def _handle_move_enemy(self, message):
        # Handle the movement of an enemy in the game world
        parts = message.split(":")
        uuid_from_string, x_cord, y_cord, is_right = uuid.UUID(parts[1]), float(parts[2]), float(parts[3]), bool(
            parts[4])
        for enemy in self.world.enemies:
            if enemy.uuid == uuid_from_string:
                if is_right:
                    enemy.enemy_x = x_cord
                    enemy.enemy_y = y_cord
        self.world.update_enemies()

    def handle_messages(self, message):
        # Handle messages received from the server and call the appropriate handlers
        if message.startswith("player_joined:"):
            self._handle_player_joined(message)
        elif message.startswith("movement:"):
            self._handle_movement(message)
        elif message.startswith("spawn_enemy:"):
            self._handle_spawn_enemy(message)
        elif message.startswith("remove_enemy:"):
            self._handle_remove_enemy(message)
        elif message.startswith("move_enemy:"):
            self._handle_move_enemy(message)

    def run(self):
        # Main method that runs the game loop
        while self.running:
            self.handle_events()  # Handle events
            if Gui.NAME_PRESENT:
                self.update()  # Update the game state
                self.draw()  # Draw the game state on the screen
                self.clock.tick(60)  # Keep the framerate at 60 FPS

        # Close the connection and the receiving thread when the game ends
        self.client_socket.close()
        self.receive_thread.join()


if __name__ == "__main__":
    Game().run()  # Start the game
