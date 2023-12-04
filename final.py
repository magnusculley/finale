from designer import *
from dataclasses import dataclass

set_window_size(1300, 600)


@dataclass
class Box:
    body: [DesignerObject]
    xspeed: int
    yspeed: int
    grow: float
    outline: [DesignerObject]
    is_colliding: bool


@dataclass
class Stage:
    blocks: [DesignerObject]
    boxes: [Box]
    flag: DesignerObject
    title: DesignerObject


@dataclass
class Beam:
    body: DesignerObject
    length: float
    is_colliding: bool
    endpoint: DesignerObject


@dataclass
class Player:
    body: DesignerObject
    is_moving: bool
    colliding_with_ground: bool
    colliding_with_box: bool
    xspeed: int
    yspeed: float
    jump_delay: int
    beam: Beam
    mana: int
    drain: int

@dataclass
class Interface:
    mana_bar: DesignerObject
    mana_text: DesignerObject
    instructions: DesignerObject

@dataclass
class World:
    player: Player
    timer: int
    stages: [Stage]
    is_clicking: bool
    level: int
    interface: Interface


PRESSED_KEYS = []
FIRST_JUMP = True


def create_world() -> World:
    '''
    This function creates the World class and defines its fields
     when the program starts

    Returns:
        World: the World class that the rest of the game exists on
    '''
    return World(create_player(), 0, create_stages(), False, 0, create_interface())


def create_stages() -> [Stage]:
    '''
    This function creates the list of Stages that contain the interactable objects in the world
    in the order that the levels are played.

    Returns:
        [Stage]: The playable levels
    '''
    return [Stage([rectangle('black', get_width(), 80, get_width() / 2, get_height() - 40, anchor='midtop'),
    rectangle('black', 90, 300, 800, get_height() - 250, 0, anchor='midtop')],
    [Box(rectangle('red', 60, 60, 600, 600, 0, anchor='midbottom'), 0, 0,1.0,
    rectangle('purple', 0, 0, 600, 600, 0), False)], emoji('🚩', 1100, 540),
    text("blue", "Level 1: The Basics", 40,600,60)),
    Stage([rectangle('black', get_width(), 80, get_width() / 2, get_height() - 840, anchor='midtop'),
    rectangle('black', 90, 300, 800, get_height() - 1050, 0, anchor='midtop'),
    rectangle('black', 90, 300, 300, get_height() - 1050, 0, anchor='midtop'),
    rectangle('black', get_width(), 80, get_width() / 2, 200 - 800, 0, anchor='midtop')],
    [Box(rectangle('red', 200, 200, 600, 600 - 800, 0, anchor='midbottom'), 0, 0, 1.0,
    rectangle('purple', 0, 0, 600, 600 - 800, 0), False)], emoji('🚩', 1100, 540 - 800),
    text("blue", "Level 2: Mana Management", 40,600,60-800))]


def create_player() -> Player:
    '''
    This function creates the player and defines all its field

    Returns:
        Player: The player that the user controls
    '''
    return Player(emoji("🔴", 20, 600, anchor='midbottom'), False, False, False, 3, 0.0, 0,
    Beam(line('black', 0, 0, 0, 0), 0.0, False, circle('purple', 0, 0, 0)), 100, 0)


def create_interface() -> Interface:
    controls=group(text("black", "Controls:", 20, 1100,20),
                   text("black", "A, S: Movement", 20, 1100,40),
                   text("black", "Space: Jump", 20, 1100,60),
                   text("black", "R: Reset Level", 20, 1100,80),
                   text("black", "Z / X: Grow / Shrink", 20, 1100,100),
                   text("black", "Mouse: Move Box", 20, 1100,120))
    return Interface(rectangle('green', 200, 50, 40, 40, 0, anchor='midleft'),
    text("black","Mana Remaining:", 20,120,80),controls)


def clicked(world: World):
    '''
    This function sets the world.is_clicking boolean to True
    when the user is holding down the mouse button

    Args:
        world (World): The current state of the world
    '''
    world.is_clicking = True


def unclicked(world: World):
    '''
    This function sets the world.is_clicking boolean to False
    when the user lifts the mouse button

    Args:
        world (World): The current state of the world
    '''
    world.is_clicking = False


def key_pressed(world: World, key: str):
    global FIRST_JUMP
    PRESSED_KEYS.append(key)
    if 'a' in PRESSED_KEYS and 'd' in PRESSED_KEYS:
        world.player.xspeed = 0
    elif 'a' in PRESSED_KEYS:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'd' in PRESSED_KEYS:
        world.player.is_moving = True
        world.player.xspeed = 10
    if key == 'space':
        jump(world)
        FIRST_JUMP = False
    if key == 'z':
        world.stages[world.level].boxes[0].grow = 1.035
        world.player.drain = 1
    if key == 'x':
        world.stages[world.level].boxes[0].grow = .965
        world.player.drain = 1
    if key == 'r':
        reset_level(world)


def key_released(world: World, key: str):
    if key in PRESSED_KEYS:
        PRESSED_KEYS.remove(key)
    if 'a' in PRESSED_KEYS:
        world.player.is_moving = True
        world.player.xspeed = -10
    elif 'd' in PRESSED_KEYS:
        world.player.is_moving = True
        world.player.xspeed = 10
    else:
        world.player.is_moving = False
        world.player.xspeed = 0
        world.stages[world.level].boxes[0].grow = 1
        world.player.drain = 0


def colliding_state(world: World):
    '''
    This function is called when the game updates, it handles the
    collision states of the objects in the game

    Args:
        world (World): The current state of the world
    '''
    if colliding(world.player.body, world.stages[world.level].blocks[0]):
        world.player.colliding_with_ground = True
    else:
        world.player.colliding_with_ground = False
    if colliding(world.player.body, world.stages[world.level].boxes[0].body):
        world.player.colliding_with_box = True
    else:
        world.player.colliding_with_box = False
    if colliding(world.stages[world.level].boxes[0].body, world.stages[world.level].blocks[0]):
        world.stages[world.level].boxes[0].is_colliding = True
    else:
        world.stages[world.level].boxes[0].is_colliding = False


def physics(world: World):
    '''
    This is the main function of the game that calls other important functions such as
    the player movement and the beam, depending on conditions. It is called every frame.

     Args:
        world (World): The current state of the World
    '''
    world.timer += 1
    floor = world.stages[world.level].blocks[0].y
    if not world.player.colliding_with_ground:
        gravity(world.player)
    else:
        push_out(world.player, floor)
    if world.player.is_moving:
        player_movement(world)
    if world.is_clicking:
        line_creation(world)
        if world.player.beam.is_colliding and world.player.mana > 0:
            scale(world)
    else:
        clear_beam(world)
    if world.player.beam.is_colliding:
        move_box(world)
    if not world.stages[world.level].boxes[0].is_colliding:
        gravity(world.stages[world.level].boxes[0])
    else:
        push_out(world.stages[world.level].boxes[0], floor)

    if world.player.colliding_with_box:
        box_player_interaction(world)

    for block_index in range(len(world.stages[world.level].blocks)):
        if colliding(world.player.body, world.stages[world.level].blocks[block_index]):
            player_block_interaction(world, block_index)
        if colliding(world.stages[world.level].boxes[0].body, world.stages[world.level].blocks[block_index]):
            box_block_interaction(world, block_index)


def next_level(world: World):
    '''
    This function advances the level when the player reaches the flag.
    It also resets player position and mana. It is called every frame.

    Args:
        world (World): The current state of the World
    '''
    if colliding(world.stages[world.level].flag, world.player.body):
        world.level += 1
        world.player.mana=100
        for stage in world.stages:
            for box in stage.boxes:
                box.body.y += 800
            for block in stage.blocks:
                block.y += 800
            stage.flag.y += 800
            stage.title.y +=800
            world.player.body.x = 20
            world.player.body.y = 500


def reset_level(world:World):
    player=world.player
    box=world.stages[world.level].boxes
    player.body.x=20
    player.body.y=600
    player.mana=100
    if world.level==0:
        box[0].body.x=600
        box[0].body.y=600
        box[0].body.width=60
        box[0].body.height=60
    elif world.level == 1:
        box[0].body.x = 600
        box[0].body.y = 600
        box[0].body.width = 200
        box[0].body.height = 200


def push_out(object, floor: int):
    '''
    This function keeps an object above an integer floor

    Args:
        object(Class): The object being pushed up
        floor (int): The y value that the object is being kept above
    '''
    if object.body.y > floor + 1:
        object.body.y = floor + 1
    object.yspeed = 0


def gravity(object):
    object.yspeed += 1
    object.body.y += object.yspeed


def player_movement(world: World):
    body = world.player.body
    if body.x > 10 and body.x < get_width():
        body.x += world.player.xspeed
    elif body.x <= 10:
        body.x += 1
    elif body.x >= get_width():
        body.x -= 1


def line_creation(world: World):
    destroy(world.player.beam.body)
    destroy(world.player.beam.endpoint)
    world.player.beam.body = line('blue', world.player.body.x, world.player.body.y - 15, get_mouse_x(), get_mouse_y(),
                                  2)
    world.player.beam.endpoint = circle('purple', 3, get_mouse_x(), get_mouse_y())
    if colliding(world.player.beam.endpoint, world.stages[world.level].boxes[0].body):
        world.player.beam.is_colliding = True


def update_interface(world: World):
   interface=world.interface
   mana=world.player.mana
   destroy(interface.mana_bar)
   destroy(interface.mana_text)
   interface.mana_bar = rectangle('green', mana*2, 50, 40, 40, 0, anchor='midleft')
   interface.mana_text = text("black","Mana Remaining:"+str(mana), 20,120,80)


def scale(world: World):
    world.stages[world.level].boxes[0].body.height = int(
        world.stages[world.level].boxes[0].body.height * world.stages[world.level].boxes[0].grow)
    world.stages[world.level].boxes[0].body.width = int(
        world.stages[world.level].boxes[0].body.width * world.stages[world.level].boxes[0].grow)
    world.stages[world.level].boxes[0].outline.height = int(
        world.stages[world.level].boxes[0].outline.height * world.stages[world.level].boxes[0].grow)
    world.stages[world.level].boxes[0].outline.width = int(
        world.stages[world.level].boxes[0].outline.width * world.stages[world.level].boxes[0].grow)
    world.player.mana -= world.player.drain


def jump(world: World):
    time = world.timer
    if FIRST_JUMP & world.player.colliding_with_ground:
        world.player.body.y = world.player.body.y - 1
        world.player.yspeed = -16
        world.player.jump_delay = time
        world.player.colliding_with_ground = False
    elif time - world.player.jump_delay > 10 and world.player.colliding_with_ground or world.player.colliding_with_box and time - world.player.jump_delay > 10:
        world.player.body.y = world.player.body.y - 1
        world.player.yspeed = -16
        world.player.jump_delay = time
        world.player.colliding_with_ground = False


def clear_beam(world: World):
    hide(world.player.beam.body)
    hide(world.stages[world.level].boxes[0].outline)
    hide(world.player.beam.endpoint)
    world.player.beam.is_colliding = False


def move_box(world: World):
    world.stages[world.level].boxes[0].body.x = get_mouse_x()
    world.stages[world.level].boxes[0].body.y = get_mouse_y() + (world.stages[world.level].boxes[0].body.height / 2)
    world.stages[world.level].boxes[0].yspeed = 0
    destroy(world.stages[world.level].boxes[0].outline)
    world.stages[world.level].boxes[0].outline = rectangle('purple', world.stages[world.level].boxes[0].body.width,
                                                           world.stages[world.level].boxes[0].body.height,
                                                           world.stages[world.level].boxes[0].body.x,
                                                           world.stages[world.level].boxes[0].body.y, 5,
                                                           anchor='midbottom')


def box_player_interaction(world: World):
    unclicked(world)
    world.player.colliding_with_box = True
    player = world.player.body
    boxtop = world.stages[world.level].boxes[0].body.y - world.stages[world.level].boxes[0].body.height
    boxleft = world.stages[world.level].boxes[0].body.x - (world.stages[world.level].boxes[0].body.width / 2)
    boxright = world.stages[world.level].boxes[0].body.x + (world.stages[world.level].boxes[0].body.width / 2)
    if player.x > boxleft and player.x < boxright and player.y > boxtop:
        push_out(world.player, boxtop)
    if player.x <= boxleft and player.y > boxtop + 10:
        player.x -= 10
        player.xspeed = 0
        world.player.colliding_with_box = False
    if player.x >= boxright and player.y > boxtop + 10:
        player.x += 10
        player.xspeed = 0
        world.player.colliding_with_box = False


def box_block_interaction(world: World, num: int):
    box = world.stages[world.level].boxes[0].body
    block = world.stages[world.level].blocks[num]
    if box.y - box.height >= block.y + block.height-(box.height/3):
        unclicked(world)
    elif box.y > block.y + 20:
        if box.x < block.x:
            box.x = block.x - (block.width / 2) - (box.width / 2)
            unclicked(world)
        else:
            box.x = block.x + (block.width / 2) + (box.width / 2)
            unclicked(world)
    else:
        push_out(world.stages[world.level].boxes[0], block.y)


def player_block_interaction(world: World, num: int):
    player = world.player.body
    block = world.stages[world.level].blocks[num]
    if player.y > block.y + 20:
        if player.x < block.x:
            player.x = block.x - (block.width / 2) - (player.width / 2)
        else:
            player.x = block.x + (block.width / 2) + (player.width / 2)
    else:
        world.player.colliding_with_ground = True
        push_out(world.player, block.y)


when('input.mouse.down', clicked)
when('input.mouse.up', unclicked)
when('starting', create_world)
when('updating', next_level)
when('updating', colliding_state)
when('updating', physics)
when('updating', update_interface)
when('typing', key_pressed)
when('done typing', key_released)
start()
