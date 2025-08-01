import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = "Whack A Mole"

MOLE = "./images/mole.png"
BUNNY = "./images/bunny.png"
MALLET = "./images/mallet.png"
MOLE_SCALE = 0.5

HOLES = [
    (150, 150), 
    (400, 150),
    (650, 150),
    (150, 300),
    (400, 300),
    (650, 300) 
]

# class to define mole attributes like size, being visible when it pops out, and being hidden
class Mole(arcade.Sprite):
    def __init__(self, image, scale, is_real=True):
        super().__init__(image, scale)
        self.is_real = is_real
        self.is_visible = False
        self.hide()

    def pop_out(self, position):
        self.center_x, self.center_y = position
        self.alpha = 255
        self.is_visible = True
        self.visible_time = 0.0

    def hide(self):
        self.center_x = -100
        self.center_y = -100
        self.alpha = 0
        self.is_visible = False
        self.visible_time = 0.0

# main class that defines what the user will view once everything is loaded and ready
class MainGame(arcade.Window):

    # function will set the stage, and control when the next Sprite will pop out
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)

        self.mole_list = None
        self.score = 0
        self.level = 1

        self.waiting_to_spawn = False
        self.spawn_delay = 2.0
        self.time_since_click = 0.0
        self.mole_time = 2.0

    # Initialize the game. This function will create 6 random Sprite appearances
    def setup(self):
        self.mole_list = arcade.SpriteList()
        self.score = 0
        self.level = 1
        self.spawn_delay = 2.0
        self.mole_time = 2.0

        for _ in range(6):
            is_real = random.choice([True, False])
            image = MOLE if is_real else BUNNY
            mole = Mole(image, MOLE_SCALE, is_real)
            self.mole_list.append(mole)

        self.spawn_random_mole()

    # Function will show user their score and level
    def on_draw(self):
        self.clear()

        arcade.draw_text(f"Score: {self.score}", 10, HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Level: {self.level}", 10, HEIGHT - 60, arcade.color.WHITE, 15)

        self.mole_list.draw()

    # Function that checks timing
    def on_update(self, delta_time):
        if self.waiting_to_spawn:
            self.time_since_click += delta_time
            if self.time_since_click >= self.spawn_delay:
                self.waiting_to_spawn = False
                self.time_since_click = 0.0
                self.spawn_random_mole()
                self.check_level()

    # Function that will check level of player and increase challenge
    def check_level(self):
        new_level = self.score // 4 + 1
        if new_level > self.level:
            self.level = new_level
            
            self.spawn_delay = max(0.5, self.spawn_delay - 0.2)

    # function for moles/bunnies to randomly pop out of their holes. If a bunny pops up, a mole will also pop out so user does not lose points being forced to click bunny
    def spawn_random_mole(self):
        for mole in self.mole_list:
            mole.hide()

        first = random.choice(self.mole_list)
        first_position = random.choice(HOLES)
        first.pop_out(first_position)

        if not first.is_real:
            moles_hidden = [m for m in self.mole_list if m.is_real and not m.is_visible]

            if moles_hidden:
                second = random.choice(moles_hidden)

                new_positions = [np for np in HOLES if np != first_position]
                second_position = random.choice(new_positions)
                second.pop_out(second_position)

    # function that will increase score when mole is hit or decrease score if bunny is hit
    def on_mouse_press(self, x, y, button, modifiers):
        for mole in self.mole_list:
            if mole.is_visible and mole.collides_with_point((x, y)):
                if mole.is_real:
                    self.score += 1
                else:
                    self.score -= 1
                mole.hide()
                self.waiting_to_spawn = True
                self.time_since_click = 0.0
                break

# function to start
def main():
    game = MainGame(WIDTH, HEIGHT, TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        