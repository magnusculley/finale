from designer import *
from dataclasses import dataclass

set_window_size(1300, 600)


@dataclass
class Box:
    '''
    Boxes have a rectangle body and an outline DesignerObjects that visually represent the boxes
    the is_colliding and is_selected booleans control the logic
    xspeed and yspeed control movement, grow controls scale
    '''
    body: [DesignerObject]
    xspeed: int
    yspeed: int
    grow: float
    outline: [DesignerObject]
    is_colliding: bool
    is_selected: bool


@dataclass
class Stage:
    '''
    Stages make up the actual level and are made up of blocks, boxes, flag, and title
    this consists of the interactable objects in the world
    '''
    blocks: [DesignerObject]
    boxes: [Box]
    flag: DesignerObject
    title: DesignerObject


@dataclass
class Beam:
    '''
    The beam shoots out from the player and has a body and endpoint DesignerObject for collision detection
    is_colliding controls the logic of the beam
    '''
    body: DesignerObject
    length: float
    is_colliding: bool
    endpoint: DesignerObject


@dataclass
class Player:
    '''
    The player has a body to control as a DesignerObject and many booleans to control the logic of the player
    yspeed and xspeed controls the movement of the body
    Beam is a class that is attached to the Player
    mana, drain, and jump_delay control mechanics of the player
    '''
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
    '''
    The interface is solely cosmetic, is consists of DesignerObjects
    that display information at the top of the screen
    '''
    mana_bar: DesignerObject
    mana_text: DesignerObject
    instructions: DesignerObject


@dataclass
class World:
    '''
    The World data class controls the state of everything in the game.
    Player, Stages, and Interface all exist in the world Class.
    is_clicking and level, are very important logic controllers in the game
    '''
    player: Player
    timer: int
    gravity: int
    stages: [Stage]
    is_clicking: bool
    level: int
    interface: Interface


PRESSED_KEYS = [] #A global list containing keys that are currently pressed
FIRST_JUMP = True #Tracks whether the first jump has occured


def create_world() -> World:
    '''
    This function creates the World class and defines its fields
     when the program starts

    Returns:
        World: the World class that the rest of the game exists on
    '''
    return World(create_player(), 0, 1, create_stages(), False, 0, create_interface())


def create_stages() -> [Stage]:
    '''
    This function creates the list of Stages that contain the interactable objects in the world
    in the order that the levels are played.

    Returns:
        [Stage]: The playable levels
    '''
    #Each stage in the list contains all the elements of a level
    return [Stage([rectangle('black', get_width(), 80, get_width() / 2, get_height() - 40, anchor='midtop'),
                   rectangle('black', 90, 300, 800, get_height() - 250, 0, anchor='midtop')],
                  [Box(rectangle('red', 60, 60, 600, 600, 0, anchor='midbottom'), 0, 0, 1.0,
                       rectangle('purple', 0, 0, 600, 600, 0), False, False)], emoji('🚩', 1100, 540),
                  text("blue", "Level 1: The Basics", 40, 600, 60)),

            Stage([rectangle('black', get_width(), 80, get_width() / 2, get_height() - 840, anchor='midtop'),
                   rectangle('black', 90, 300, 800, get_height() - 1050, 0, anchor='midtop'),
                   rectangle('black', 90, 300, 300, get_height() - 1050, 0, anchor='midtop'),
                   rectangle('black', get_width(), 80, get_width() / 2, 200 - 800, 0, anchor='midtop')],
                  [Box(rectangle('red', 280, 280, 600, 600 - 800, 0, anchor='midbottom'), 0, 0, 1.0,
                       rectangle('purple', 0, 0, 600, 600 - 800, 0), False, False)], emoji('🚩', 1100, 540 - 800),
                  text("blue", "Level 2: Mana Management", 40, 600, 60 - 800)),

            Stage([rectangle('black', get_width(), 80, get_width() / 2, get_height() - 1640, anchor='midtop'),
                   rectangle('black', 90, 400, 800, get_height() - 1850, 0, anchor='midtop')],
                  [Box(rectangle('red', 120, 90, 600, 600 - 1600, 0, anchor='midbottom'), 0, 0, 1.0,
                       rectangle('purple', 0, 0, 600, 600 - 1600, 0), False, False)], emoji('🚩', 1100, 540 - 1600),
                  text("blue", "Level 3: High Gravity", 40, 600, 60 - 1600)),

            Stage([rectangle('black', get_width(), 80, get_width() / 2, get_height() - 2440, anchor='midtop')],
                  [Box(rectangle('red', 120, 120, 600, 600 - 2400, 0, anchor='midbottom'), 0, 0, 1.0,
                       rectangle('purple', 0, 0, 600, 600 - 2400, 0), False, False)], emoji('🚩', -100,0),
                  text("blue", "You Won :D", 40, 600, 60 - 2400))
            ]


def create_player() -> Player:
    '''
    This function creates the player and defines all its field

    Returns:
        Player: The player that the user controls
    '''
    return Player(emoji("🔴", 20, 600, anchor='midbottom'), False, False, False, 3, 0.0, 0,
                  Beam(line('black', 0, 0, 0, 0), 0.0, False, circle('purple', 0, 0, 0)), 100, 0)


def create_interface() -> Interface:
    '''
       This function creates the interface and defines all its field

       Returns:
           Interface: The text and bar at the top
    '''
    controls = group(text("black", "Controls:", 20, 1100, 20),
                     text("black", "A, D: Movement", 20, 1100, 40),
                     text("black", "Space: Jump", 20, 1100, 60),
                     text("black", "R: Reset Level", 20, 1100, 80),
                     text("black", "Z / X: Grow / Shrink", 20, 1100, 100),
                     text("black", "Mouse: Move Box", 20, 1100, 120))
    return Interface(rectangle('green', 200, 50, 40, 40, 0, anchor='midleft'),
                     text("black", "Mana Remaining:", 20, 120, 80), controls)


def clicked(world: World):
    '''
    This function sets the world.is_clicking boolean to True
    when the user is holding down the mouse button

    Args:
        world (World): The current state of the world

    Returns:
        None
    '''
    world.is_clicking = True


def unclicked(world: World):
    '''
    This function sets the world.is_clicking boolean to False
    when the user lifts the mouse button

    Args:
        world (World): The current state of the world

    Returns:
        None
    '''
    world.is_clicking = False


def key_pressed(world: World, key: str):
    '''
    Update game state based on the key pressed.

    Args:
    world (World): The current state of the World
    key (str): The key that was pressed

    Returns:
    None

    Global Variables:
        FIRST_JUMP (bool): Tracks whether the first jump has occurred
        PRESSED_KEYS (list): A global list containing keys that are currently pressed
    '''
    global FIRST_JUMP
    PRESSED_KEYS.append(key)
    #'a' and 'd' control movement
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
    #'z' and 'x' control scaling of the box
    if key == 'z':
        world.stages[world.level].boxes[0].grow = 1.035
        world.player.drain = 1
    if key == 'x':
        world.stages[world.level].boxes[0].grow = .965
        world.player.drain = 1
    if key == 'r':
        reset_level(world)


def key_released(world: World, key: str):
    '''
    Update game state when a key is released.

    Args:
        world (World): The game world containing player, stages, and other elements.
        key (str): The key that was released.

    Returns:
    None

    Global Variables:
        PRESSED_KEYS (list): A global list containing keys that are currently pressed
    '''
    #prevents the player from moving continuously after the key is released
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
    #player and ground block collision
    if colliding(world.player.body, world.stages[world.level].blocks[0]):
        world.player.colliding_with_ground = True
    else:
        world.player.colliding_with_ground = False

    #goes through every box in a level and checks collision with player, beam, and ground
    for box in world.stages[world.level].boxes:
        if colliding(world.player.body, box.body):
            world.player.colliding_with_box = True
        else:
            world.player.colliding_with_box = False

        if colliding(world.player.beam.endpoint, box.body) and world.is_clicking:
            world.player.beam.is_colliding = True
            box.is_selected = True
        else:
            box.is_selected = False

        if colliding(box.body, world.stages[world.level].blocks[0]):
            box.is_colliding = True
        else:
            box.is_colliding = False


def physics(world: World):
    '''
    This is the main function of the game that calls other important functions such as
    the player movement and the beam, depending on conditions. It is called every frame.

    Args:
        world (World): The current state of the World

    Returns:
        None
    '''
    world.timer += 1
    floor = world.stages[world.level].blocks[0].y
    if not world.player.colliding_with_ground:
        gravity(world.player, world)
    else:
        push_out(world.player, floor)
    if world.player.is_moving:
        player_movement(world)
    #creates line when clicking and destroys when not clicking
    if world.is_clicking:
        line_creation(world)
        if world.player.beam.is_colliding and world.player.mana > 0:
            scale(world)
    else:
        clear_beam(world)
    if world.player.beam.is_colliding:
        move_box(world)
    for box in world.stages[world.level].boxes:
        if not box.is_colliding:
            gravity(box, world)
        else:
            push_out(box, floor)

    if world.player.colliding_with_box:
        box_player_interaction(world)

    #interactions for all blocks against the player and every box
    for block_index in range(len(world.stages[world.level].blocks)):
        if colliding(world.player.body, world.stages[world.level].blocks[block_index]):
            player_block_interaction(world, block_index)
        for box in world.stages[world.level].boxes:
            if colliding(box.body, world.stages[world.level].blocks[block_index]):
                box_block_interaction(world, block_index)


def next_level(world: World):
    '''
    This function advances the level when the player reaches the flag.
    It also resets player position and mana. It is called every frame.

    Args:
        world (World): The current state of the World

    Returns:
        None
    '''
    #Basically every level exists at the same time in a conveyor belt and the
    #next level is shifted up to you upon completing a level
    if colliding(world.stages[world.level].flag, world.player.body):
        world.level += 1
        world.player.mana = 100
        for stage in world.stages:
            for box in stage.boxes:
                box.body.y += 800
            for block in stage.blocks:
                block.y += 800
            stage.flag.y += 800
            stage.title.y += 800
            world.player.body.x = 20
            world.player.body.y = 500


def reset_level(world: World):
    '''
    This function resets the box, and player when the r key is pressed

    Args:
        world (World): The current state of the World

    Returns:
        None
    '''
    player = world.player
    box = world.stages[world.level].boxes
    player.body.x = 20
    player.body.y = 600
    player.mana = 100
    if world.level == 0:
        box[0].body.x = 600
        box[0].body.y = 600
        box[0].body.width = 60
        box[0].body.height = 60
    elif world.level == 1:
        box[0].body.x = 600
        box[0].body.y = 600
        box[0].body.width = 200
        box[0].body.height = 200
    elif world.level == 2:
        box[0].body.x = 600
        box[0].body.y = 600
        box[0].body.width = 60
        box[0].body.height = 60


def push_out(object, floor: int):
    '''
    This function keeps an object above an integer floor

    Args:
        object (Class): The object being pushed up
        floor (int): The y value that the object is being kept above

    Returns:
        None
    '''
    if object.body.y > floor + 1:
        object.body.y = floor + 1
    object.yspeed = 0


def gravity(object, world):
    '''
    This function applies gravity to an object by constantly increasing the yspeed and y position

    Args:
        object (Class): The object that gravity is applied to
        world (World): The current state of the World

    Returns:
          None
    '''
    if world.level == 2:
        world.gravity = 2
    else:
        world.gravity = 1
    object.yspeed += world.gravity
    object.body.y += object.yspeed


def player_movement(world: World):
    '''
    This function handles the movement of the player by adding the players xspeed to their position

    Args:
        world (World): The current state of the World\

    Returns:
        None
    '''
    body = world.player.body
    if body.x > 10 and body.x < get_width():
        body.x += world.player.xspeed
    elif body.x <= 10:
        body.x += 1
    elif body.x >= get_width():
        body.x -= 1


def line_creation(world: World):
    '''
    This function creates and destroys the beam of the player to where the mouse is

    Args:
         world (World): The current state of the World

    Returns:
        None
    '''
    beam = world.player.beam
    destroy(beam.body)
    destroy(beam.endpoint)
    beam.body = line('blue', world.player.body.x, world.player.body.y - 15, get_mouse_x(), get_mouse_y(), 2)
    beam.endpoint = circle('purple', 3, get_mouse_x(), get_mouse_y())


def update_interface(world: World):
    '''
    This function updates the mana bar and text to represent the current value

    Args:
        world (World): The current state of the World

    Returns:
        None
    '''
    interface = world.interface
    mana = world.player.mana
    destroy(interface.mana_bar)
    destroy(interface.mana_text)
    interface.mana_bar = rectangle('green', mana * 2, 50, 40, 40, 0, anchor='midleft')
    interface.mana_text = text("black", "Mana Remaining:" + str(mana), 20, 120, 80)


def scale(world: World):
    '''
     This function scales the size of the selected box

     Args:
         world (World): The current state of the World

    Returns:
        None
     '''
    grow = world.stages[world.level].boxes[0].grow
    world.player.mana -= world.player.drain
    for box in world.stages[world.level].boxes:
        if box.is_selected:
            box.body.height = int(box.body.height * grow)
            box.body.width = int(box.body.width * grow)
            box.outline.height = int(box.outline.height * grow)
            box.outline.width = int(box.outline.width * grow)


def jump(world: World):
    '''
     This function gives the player a negative yspeed acting as a jump
     FIRST_JUMP and world.timer are used in conjuction to prevent the player from jumping without delay

     Args:
         world (World): The current state of the World

     Returns:
         None

     Global Variables:
        FIRST_JUMP (bool): Tracks if the player has taken their first jump
     '''
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
    '''
     This function clears the beam when the user is not pressing the mouse

     Args:
        world (World): The current state of the world

     Returns:
        None
     '''
    hide(world.player.beam.body)
    hide(world.player.beam.endpoint)
    world.player.beam.is_colliding = False
    for box in world.stages[world.level].boxes:
        if not box.is_selected:
            hide(box.outline)


def move_box(world: World):
    '''
     This function moves the selected box to the mouse when the user is clicking

     Args:
        world (World): The current state of the world

     Returns:
        None
     '''
    for box in world.stages[world.level].boxes:
        if box.is_selected and world.is_clicking:
            box.body.x = get_mouse_x()
            box.body.y = get_mouse_y() + (box.body.height / 2)
            box.yspeed = 0
            destroy(box.outline)
            box.outline = rectangle('purple', box.body.width, box.body.height, box.body.x, box.body.y, 5,
                                    anchor='midbottom')


def box_player_interaction(world: World):
    '''
     This function handles the collision between the boxes and the player

     Args:
         world (World): The current state of the World

     Returns:
         None
     '''
    unclicked(world)
    world.player.colliding_with_box = True
    player = world.player.body
    for box in world.stages[world.level].boxes:
        boxtop = box.body.y - box.body.height
        boxleft = box.body.x - (box.body.width / 2)
        boxright = box.body.x + (box.body.width / 2)
        if player.x > boxleft and player.x < boxright and player.y > boxtop:
            push_out(world.player, boxtop)
        if player.x <= boxleft and player.y > boxtop + 10:  # +10 allows the player to glide over the edge
            player.x -= 10
            player.xspeed = 0
            world.player.colliding_with_box = False
        if player.x >= boxright and player.y > boxtop + 10:
            player.x += 10
            player.xspeed = 0
            world.player.colliding_with_box = False


def box_block_interaction(world: World, number: int):
    '''
     This function handles the collision between the boxes and the blocks

     Args:
         world (World): The current state of the World
         number (int): Which block the box is colliding with

     Returns:
         None
     '''
    block = world.stages[world.level].blocks[number]
    for box in world.stages[world.level].boxes:
        if box.body.y - box.body.height >= block.y + block.height - (box.body.height / 3):
            unclicked(world)
        elif box.body.y > block.y + 20:  # +20 allows the box to glide over the corner of the block
            if box.body.x < block.x:
                box.body.x = block.x - (block.width / 2) - (box.body.width / 2)
                unclicked(world)
            else:
                box.body.x = block.x + (block.width / 2) + (box.body.width / 2)
                unclicked(world)
        else:
            push_out(box, block.y)


def player_block_interaction(world: World, number: int):
    '''
     This function handles the collision between the player and the blocks

     Args:
         world (World): The current state of the World
         number (int): Which block the player is colliding with
     '''
    player = world.player.body
    block = world.stages[world.level].blocks[number]
    if player.y - player.height >= block.y + block.height - (player.height / 3):
        player.y = block.y + block.height + player.height
    elif player.y > block.y + 20:
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
