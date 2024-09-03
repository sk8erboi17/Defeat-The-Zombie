import pygame

from entity.enemy import Enemy
from entity.player import Player
from network.client_socket import ClientSocket
from network.socket_packets import packets


class World:
    CHUNK_SIZE = 8  # Dimensione di un singolo chunk in termini di numero di tile
    GRAVITY = 1.4  # Gravity force applied to the player
    TILE_SIZE = 16  # Size of each tile in pixels

    def __init__(self):
        self.players = []
        self.enemies = []
        self.weapons = []
        self.game_map = {}

    def remove_player(self, player):
        self.players.remove(player)

    def spawn_player(self, player: 'Player'):
        self.players.append(player)
        self.weapons.append(player.weapon)

    def draw_weapon(self, screen, image):
        for weapon in self.weapons:
            screen.blit(image, (weapon.weapon_x, weapon.weapon_y))

    # Uses global coordinates (x, y) to determine the chunk's position in the world grid.
    # These are the coordinates of the chunk in the world grid.
    # These coordinates are in terms of chunks, not tiles.
    def generate_chunk(self, x, y):
        chunk_data = []
        # Local Chunk: Focuses on the internal details of a single chunk, using local tile coordinates.
        # Uses local coordinates (x_pos, y_pos) within the chunk. These coordinates are independent of where the chunk is globally.
        # refers to the data or elements that are stored within a specific chunk of the game world
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                # target_x and target_y translate those local positions into global positions,
                # allowing you to see where each tile from the chunk fits into the overall game world.
                # Chunk Positioning in the World Grid:
                # The value x * CHUNK_SIZE gives you the x-coordinate of the starting position of the chunk in the global coordinate system.
                # once you know where the chunk starts globally, you need to find the specific global position of each tile within that chunk.
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
                tile_type = 0  # nothing
                if target_y > 32:
                    tile_type = 2  # dirt
                elif target_y == 32:
                    tile_type = 1  # grass
                if tile_type != 0:
                    chunk_data.append([[target_x, target_y], tile_type])
        return chunk_data

    def draw_chunk(self, display, grass, dirt):

        # Iterate through nearby chunks (visible on screen)
        # num_chunks_y = SCREEN_HEIGHT // (CHUNK_SIZE * TILE_SIZE) + 2
        for y in range(6):
            for x in range(8):
                target_x = x
                target_y = y
                target_chunk = str(target_x) + ';' + str(target_y)

                # Generate chunk data if not already in the game map
                if target_chunk not in self.game_map:
                    self.game_map[target_chunk] = self.generate_chunk(target_x, target_y)

                # Draw tiles within the chunk
                for tile in self.game_map[target_chunk]:
                    tile_pos = tile[0]
                    tile_type = tile[1]
                    # Calculate the position of the tile on the screen
                    screen_x = tile_pos[0] * self.TILE_SIZE
                    screen_y = tile_pos[1] * self.TILE_SIZE

                    # Draw the tile image based on tile type
                    if tile_type == 1:
                        display.blit(grass, (screen_x, screen_y))
                    else:
                        display.blit(dirt, (screen_x, screen_y))

    def apply_gravity(self, player):
        """Apply gravity to the player and check for collision with tiles."""
        # Increase the player's y position due to gravity
        player.player_y += self.GRAVITY

        # Create a rectangle for the player to check for collisions
        player_rect = pygame.Rect(player.player_x, player.player_y, Player.PLAYER_WIDTH, Player.PLAYER_HEIGHT)

        # Check for collision with tiles
        for chunk_key, chunk_data in self.game_map.items():
            for tile in chunk_data:
                tile_pos = tile[0]
                tile_type = tile[1]

                if tile_type != 0:  # Skip empty tiles
                    # Calculate the tile's rectangle in global coordinates
                    tile_rect = pygame.Rect(tile_pos[0] * self.TILE_SIZE, tile_pos[1] * self.TILE_SIZE, self.TILE_SIZE,
                                            self.TILE_SIZE)
                    player.weapon.weapon_y = player.player_y + 15
                    if player_rect.colliderect(tile_rect):
                        # If a collision is detected, stop the player from falling through the tile
                        player.player_y = tile_rect.top - Player.PLAYER_HEIGHT
                        player.is_jumping = False
                        break

    def check_collisions(self, main_player: 'Player', client: 'ClientSocket'):
        for weapon in self.weapons:
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.enemy_x, enemy.enemy_y, Enemy.ENEMY_WIDTH, Enemy.ENEMY_HEIGHT)
                if weapon.check_collision(enemy_rect):
                    self.enemies.remove(enemy)
                    print(f"Enemy at {enemy.enemy_x}, {enemy.enemy_y} was hit by the weapon.")
                    client.send_message(packets.KILL_PACKET_OUT.byte_mark,
                                        packets.KILL_PACKET_OUT.message.format(main_player.name, enemy.uuid).encode(
                                            'utf-8'))
                    break

    def remove_enemy(self, uuid):
        for enemy in self.enemies[:]:
            if enemy.uuid == uuid:
                self.enemies.remove(enemy)
                print("Removed")

    def spawn_enemy(self, uuid, x, y):
        new_enemy = Enemy(uuid, x, y)
        if x < 15:
            new_enemy.is_moving_right = True
            new_enemy.is_moving_left = False
        if x > 15:
            new_enemy.is_moving_right = False
            new_enemy.is_moving_left = True
        self.enemies.append(new_enemy)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update_animation()

    def draw_enemies(self, screen, image):
        for enemy in self.enemies:
            screen.blit(image, (enemy.enemy_x, enemy.enemy_y))

    def draw_players(self, screen):
        for player in self.players:
            player.draw(screen)

    def update_players(self):
        for player in self.players:
            player.update_animation()
            self.apply_gravity(player)
