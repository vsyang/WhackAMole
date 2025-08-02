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

    def hide(self):
        self.center_x = -100
        self.center_y = -100
        self.alpha = 0
        self.is_visible = False

# main class that defines what the user will view once everything is loaded and ready
class MainGame(arcade.Window):

    # function will set the stage with empty variables ready to be used
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)

        self.mole_list = None
        self.score = 0
        self.level = 1

        self.spawn_delay = 1.0
        self.display_timer = 2.0
        self.spawn_timer = 0.0
        self.active_timer = 0.0
        self.state = "WAITING"

        self.score_text = None
        self.level_text = None

    # Initialize the game.
    def setup(self):
        self.mole_list = arcade.SpriteList()
        self.score = 0
        self.level = 1
        self.spawn_timer = 0.0
        self.active_timer = 0.0
        self.state = "WAITING"

        for _ in range(12):
            is_real = random.choice([True, False])
            image = MOLE if is_real else BUNNY
            mole = Mole(image, MOLE_SCALE, is_real)
            self.mole_list.append(mole)

        self.score_text = arcade.Text(f"Score: {self.score}", 10, HEIGHT - 30, arcade.color.WHITE, 20)
        self.level_text = arcade.Text(f"Level: {self.level}", 10, HEIGHT - 60, arcade.color.WHITE, 15)

    # Function will show user their score and level
    def on_draw(self):
        self.clear()
        self.score_text.draw()
        self.level_text.draw()
        self.mole_list.draw()

    # Function that checks timing; how long between moles popping out and how long moles are available for user to click before disappearing
    def on_update(self, delta_time):
        if self.state == "WAITING":
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0.0
                self.spawn_random_moles()
                self.state = "VISIBLE"
        elif self.state == "VISIBLE":
            self.active_timer += delta_time
            if self.active_timer >= self.display_timer:
                for mole in self.mole_list:
                    mole.hide()
                self.active_timer = 0.0
                self.state = "WAITING"
                self.update_level()


    # Function for moles/bunnies to randomly pop out of their holes.
    def spawn_random_moles(self):
        for mole in self.mole_list:
            mole.hide()
        
        if self.level >= 15:
            count = 4
        elif self.level >= 10:
            count = 3
        elif self.level >= 5:
            count = 2
        else:
            count = 1

        hidden = [m for m in self.mole_list if not m.is_visible]
        positions = HOLES.copy()
        random.shuffle(hidden)
        random.shuffle(positions)

        for i in range(min(count, len(hidden), len(positions))):
            hidden[i].pop_out(positions[i])


    # function that will increase score when mole is hit or decrease score if bunny is hit
    def on_mouse_press(self, x, y, button, modifiers):
        for mole in self.mole_list:
            if mole.is_visible and mole.collides_with_point((x, y)):
                if mole.is_real:
                    self.score += 1
                else:
                    self.score -= 1
                mole.hide()

        self.score_text.text = f"Score: {self.score}"
        self.level_text.text = f"Level: {self.level}"
    
    # Function that will check level of player and increase challenge
    def update_level(self):
        self.level = self.score // 5 + 1
        self.display_timer = max(1.0, 2.0 - (self.level -1) * 0.1)
# function to start
def main():
    game = MainGame(WIDTH, HEIGHT, TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        