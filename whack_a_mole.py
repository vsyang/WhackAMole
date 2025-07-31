import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = "Whack A Mole"

MOLE = "./images/mole.png"
BUNNY = "./images/bunny.png"
MALLET = "./images/mallet.png"
HOLES = [
    (150, 150), 
    (400, 150),
    (650, 150),
    (150, 300),
    (400, 300),
    (650, 300) 
]

MOLE_SCALE = 0.5

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
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.mole_list = None
        self.score = 0
        self.level = 1
        self.timer = 0.0
        self.mole_timer = 1.0

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.mole_list = arcade.SpriteList()
        self.score = 0
        self.level = 1
        self.mole_timer = 1.0
        self.game_timer = 0.0

        for _ in range(6):
            is_real = random.choice([True, False])
            image = MOLE if is_real else BUNNY
            mole = Mole(image, MOLE_SCALE, is_real)
            self.mole_list.append(mole)

    def on_draw(self):
        self.clear()

        arcade.draw_text(f"Score: {self.score}", 10, HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Level: {self.score}", 10, HEIGHT - 60, arcade.color.WHITE, 15)

        self.mole_list.draw()

    def update(self, delta_time):
        self.timer += delta_time
        if self.timer >= self.mole_timer:
            self.timer= 0.0
            self.spawn_random_mole()

        if self.score >= self.level * 5:
            self.level += 1
            self.mole_timer = max(0.3, self.mole_timer - 0.1)

    def spawn_random_mole(self):
        for mole in self.mole_list:
            mole.hide()

        mole = random.choice(self.mole_list)
        position = random.choice(HOLES)
        mole.pop_out(position)

    def on_mouse_press(self, x, y, button, modifiers):
        for mole in self.mole_list:
            if mole.is_visible and mole.collides_with_point((x, y)):
                if mole.is_real:
                    self.score += 1
                else:
                    self.score -= 1
                mole.hide()

        self.mole_list[0].pop_out(random.choice(HOLES))
def main():
    game = MainGame(WIDTH, HEIGHT, TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        