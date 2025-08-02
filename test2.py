import arcade
import typing

# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Arcade All Sound Effects Preview"
BUTTON_SIZE = 40

# All available arcade built-in sound effects
SOUND_EFFECTS = [
    "coin1.wav", "coin2.wav", "coin3.wav", "coin4.wav", "coin5.wav",
    "error1.wav", "error2.wav", "error3.wav", "error4.wav", "error5.wav",
    "explosion1.wav", "explosion2.wav",
    "fall1.wav", "fall2.wav", "fall3.wav", "fall4.wav",
    "gameover1.wav", "gameover2.wav", "gameover3.wav", "gameover4.wav", "gameover5.wav",
    "hit1.wav", "hit2.wav", "hit3.wav", "hit4.wav", "hit5.wav",
    "hurt1.wav", "hurt2.wav", "hurt3.wav", "hurt4.wav", "hurt5.wav",
    "jump1.wav", "jump2.wav", "jump3.wav", "jump4.wav", "jump5.wav",
    "laser1.wav", "laser1.ogg", "laser1.mp3", "laser2.wav", "laser3.wav", "laser4.wav", "laser5.wav",
    "lose1.wav", "lose2.wav", "lose3.wav", "lose4.wav", "lose5.wav",
    "phaseJump1.wav", "phaseJump1.ogg",
    "rockHit2.wav", "rockHit2.ogg",
    "secret2.wav", "secret4.wav",
    "upgrade1.wav", "upgrade2.wav", "upgrade3.wav", "upgrade4.wav", "upgrade5.wav"
]

class SoundButton(arcade.SpriteSolidColor):
    def __init__(self, sound_file: str, center_x: float, center_y: float):
        super().__init__(BUTTON_SIZE, BUTTON_SIZE, arcade.color.DARK_BLUE_GRAY)
        self.sound_file = sound_file
        self.center_x = center_x
        self.center_y = center_y
        self.sound = arcade.load_sound(f":resources:sounds/{self.sound_file}")

    def play(self):
        arcade.play_sound(self.sound)

    def draw_label(self):
        arcade.draw_text(
            self.sound_file,
            self.center_x,
            self.center_y + BUTTON_SIZE // 2 + 4,
            arcade.color.WHITE,
            font_size=10,
            anchor_x="center"
        )

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.button_sprites = arcade.SpriteList()

    def setup(self):
        self.button_sprites = arcade.SpriteList()

        # Layout buttons in a grid
        cols = 10
        spacing_x = 110
        spacing_y = 70
        margin_x = 70
        margin_y = 100

        for index, sound_name in enumerate(SOUND_EFFECTS):
            col = index % cols
            row = index // cols
            x = margin_x + col * spacing_x
            y = WINDOW_HEIGHT - (margin_y + row * spacing_y)

            button = SoundButton(sound_name, x, y)
            self.button_sprites.append(button)

    def on_draw(self):
        self.clear()
        self.button_sprites.draw()
        for button in self.button_sprites:
            button.draw_label()

        arcade.draw_text(
            "Click a button to play sound (Arcade built-in sounds)",
            WINDOW_WIDTH // 2,
            20,
            arcade.color.YELLOW,
            font_size=16,
            anchor_x="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        hit_list = arcade.get_sprites_at_point((x, y), self.button_sprites)
        for sprite in hit_list:
            sound_button = typing.cast(SoundButton, sprite)
            if button == arcade.MOUSE_BUTTON_LEFT:
                sound_button.play()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
