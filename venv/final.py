from designer import *
from dataclasses import dataclass

@dataclass
class Player:
    obj: DesignerObject
    is_moving: bool
    xspeed: int
    yspeed: float

@dataclass
class World:
    player: Player
    timer: int

pressed_keys = []

def create_world() -> World:
    return World(create_player(), 0)

def advance_the_timer(world: World):
    world.timer += 1

def create_player() -> Player:
    return Player(emoji("man"), False, 3, 0)

def key_pressed(world: World, key: str):
    pressed_keys.append(key)
    if 'left' in pressed_keys and 'right' in pressed_keys:
        world.player.xspeed = 0
    elif 'left' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'right' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10

def key_released(world: World, key: str):
    if key in pressed_keys:
        pressed_keys.remove(key)
    if 'left' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'right' in pressed_keys:
        world.player.is_moving = True
        world.player.xspeed = 10
    else:
        world.player.is_moving = False
        world.player.xspeed = 0

def player_movement(world: World):
    if world.player.is_moving:
        world.player.obj.x += world.player.xspeed

when('updating', player_movement)
when('typing', key_pressed)
when('done typing', key_released)
when('updating', advance_the_timer)
when('starting', create_world)
start()