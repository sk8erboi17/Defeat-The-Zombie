import pygame

from network.socket_packets import packets


class Gui:
    # Class attributes defining the screen dimensions, the presence of the player's name, and the user input text
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    NAME_PRESENT = False
    user_text = ''

    def __init__(self, screen):
        # Initialize the GUI with a reference to the game screen
        self.screen = screen

    @staticmethod
    def initialize_icon(icon_image_path):
        # Load and set the window icon from the specified image path
        icon = pygame.image.load(icon_image_path)
        pygame.display.set_icon(icon)

    @staticmethod
    def set_title(title):
        # Set the window title
        pygame.display.set_caption(title)

    @staticmethod
    def create_input_box(screen):
        # Create an input box on the screen where the user can enter their name
        usr_inp_rect = pygame.Rect(250, Gui.SCREEN_HEIGHT // 2, 320, 50)
        color = pygame.Color('white')
        pygame.draw.rect(screen, color, usr_inp_rect)

        # draw the text into box
        base_font = pygame.font.Font(None, 32)
        txt_surface = base_font.render(Gui.user_text, True, (0, 0, 0))
        screen.blit(txt_surface, (usr_inp_rect.x + 10, usr_inp_rect.y + 10))

        pygame.draw.rect(screen, color, usr_inp_rect, 2)  # Draw a border around the input box

        # draw the text
        font = pygame.font.SysFont(None, 24)
        text = font.render("Insert a name", False, (255, 255, 255))
        text_rect = text.get_rect(center=(300, 280))
        screen.blit(text, text_rect)

    @staticmethod
    def handle_input_events(screen, player: 'Player', event, client_socket):
        # Handle user input events, especially for entering the player's name
        if not Gui.NAME_PRESENT:
            # If the player hasn't entered their name yet, show the input box
            Gui.create_input_box(screen)
            pygame.display.update()

            if event.type == pygame.KEYDOWN:
                # Handle different key presses
                if event.key == pygame.K_BACKSPACE:
                    Gui.user_text = Gui.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    Gui.NAME_PRESENT = True
                    player.set_name(Gui.user_text)  # Set the player's name based on the input

                    byte_mark = packets.JOIN_PACKET_OUT.byte_mark
                    join_message = packets.JOIN_PACKET_OUT.message

                    # Send the formatted join message to the server with the player's name and position
                    client_socket.send_message(byte_mark, join_message.format(player.name, player.player_x,
                                                                              player.player_y).encode('utf-8'))
                else:
                    # For any other key, add the typed character to the user input
                    Gui.user_text += event.unicode
            pygame.display.flip()  # Refresh the display after handling the input
