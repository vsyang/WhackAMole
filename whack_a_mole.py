import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = "Whack A Mole"

MOLE = "mole.png"
BUNNY = "bunny.png"
MALLET = "mallet.png"
HOLES = [
    (150, 150), 
    (400, 150),
    (650, 150),
    (150, 300),
    (400, 300),
    (650, 300) 
]

MOLE_SCALE = 0.5

