from gui.gui import Gui

# boundaries
x_right_boundary = Gui.SCREEN_WIDTH - 20
x_left_boundary = -4
y_top_boundary = -42
y_bottom_boundary = Gui.SCREEN_HEIGHT - 100


class Boundaries:
    @staticmethod
    def check_boundaries_player(player):
        if player.player_x >= x_right_boundary:
            player.player_x = x_right_boundary
        elif player.player_x < x_left_boundary:
            player.player_x = x_left_boundary

        if player.player_y >= y_bottom_boundary:
            player.player_y = y_bottom_boundary
        elif player.player_y < y_top_boundary:
            player.player_y = y_top_boundary

    @staticmethod
    def check_boundaries_weapon(weapon):
        if weapon.weapon_x >= x_right_boundary:
            return True
        elif weapon.weapon_x < x_left_boundary:
            return True

        if weapon.weapon_y >= y_bottom_boundary:
            return True
        elif weapon.weapon_y < y_top_boundary:
            return True
