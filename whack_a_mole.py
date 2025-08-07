import arcade
import random
import math

WIDTH = 800
HEIGHT = 600
TITLE = "Whack A Mole"

MOLE = "./images/mole.png"
BUNNY = "./images/bunny.png"
MALLET_UP = "./images/mallet_up.png"
MALLET_DOWN = "./images/mallet_down.png"
HOLE = "./images/hole.png"
MOLE_SCALE = 0.5
RADIUS = 70
SOUND_EFFECTS = [
    "jump4.wav", "explosion2.wav", "phase1jump.wav"
]
MUSIC = "funkyrobot.mp3"

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
        arcade.set_background_color(arcade.color.CELESTIAL_BLUE)

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

        self.mallet = None
        self.mallet_up = None
        self.mallet_down = None
        self.mouse_pressed = False
        self.set_mouse_visible(False)

        self.plus_point = arcade.load_sound(":resources:sound/jump4.wav")
        self.minus_point = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.just_click = arcade.load_sound(":resources:sounds/phaseJump1.wav")

        self.music = arcade.load_sound(":resources:music/funkyrobot.mp3")
        self.background_music = arcade.play_sound(self.music, looping=True)

    # Set-up and initialize the game.
    def setup(self):
        self.hole_list = arcade.SpriteList()
        for position in HOLES:
            hole = arcade.Sprite(HOLE, MOLE_SCALE)
            hole.center_x, hole.center_y = position
            self.hole_list.append(hole)

        self.mole_list = arcade.SpriteList()
        for _ in range(12):
            is_real = random.choice([True, False])
            image = MOLE if is_real else BUNNY
            mole = Mole(image, MOLE_SCALE, is_real)
            self.mole_list.append(mole)
        
        self.score = 0
        self.level = 1
        self.spawn_timer = 0.0
        self.active_timer = 0.0
        self.state = "WAITING"
        self.score_text = arcade.Text(f"Score: {self.score}", 10, HEIGHT - 50, arcade.color.WHITE, 36)
        self.level_text = arcade.Text(f"Level: {self.level}", 10, HEIGHT - 90, arcade.color.WHITE, 28)

        self.mallet = arcade.Sprite(MALLET_UP, MOLE_SCALE)
        self.mallet.append_texture(arcade.load_texture(MALLET_DOWN))
        self.mallet.center_x = WIDTH // 2
        self.mallet.center_y = HEIGHT // 2
        self.mallet_list = arcade.SpriteList()
        self.mallet_list.append(self.mallet)

        self.message = arcade.Text(
            "Don't Hit The Bunny!\n +1 point = mole\n  -1 point = bunny",
            x=WIDTH - 100,
            y=HEIGHT - 100,
            color=arcade.color.CAMEO_PINK,
            font_size=20,
            anchor_x="center",
            multiline=True,
            width=400
        )


    # Function will show user their score and level, draw holes, draw the moles/bunnies, and the mallets
    def on_draw(self):
        self.clear()
        self.hole_list.draw()
        self.score_text.draw()
        self.level_text.draw()
        self.mole_list.draw()
        self.mallet_list.draw()
        self.message.draw()


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


    # Function for moles/bunnies to randomly pop out of their holes. Attempted to add difficulty as levels go up
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


    # Function that will increase score when mole is hit or decrease score if bunny is hit
    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pressed = True
        self.mallet.set_texture(1) 

        for mole in self.mole_list:
            if mole.is_visible:
                distance = math.hypot(mole.center_x - x, mole.center_y - y)
                if distance <= RADIUS:
                    if mole.is_real:
                        self.score += 1
                    else:
                        self.score -= 1
                    mole.hide()

        self.score_text.text = f"Score: {self.score}"
        self.level_text.text = f"Level: {self.level}"

    # Function for when mouse is clicked then released
    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pressed = False
        self.mallet.set_texture(0)

    # Function for when mouse is in motion
    def on_mouse_motion(self, x, y, dx, dy):
        self.mallet.center_x = x
        self.mallet.center_y = y


    # Function for sound effects if time. I liked the jump4 for mole hit, explosion2 for bunny hit, phaseJump1 for clicking empty space, funkyrobot.mp3 for music
    
    # Function that will check level of player and increase challenge
    def update_level(self):
        self.level = self.score // 5 + 1
        self.display_timer = max(1.0, 2.0 - (self.level -1) * 0.1)
# Function to start
def main():
    game = MainGame(WIDTH, HEIGHT, TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        