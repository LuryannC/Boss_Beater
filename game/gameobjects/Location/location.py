import pyasge
from enum import Enum
from abc import ABC, abstractmethod

from game.gameobjects.Entities.player import Player
from game.gameobjects.gamemap import GameMap
from game.gamefunctions.pathfinding import world_move
from game.gamefunctions.pathfinding import can_world_move
from game.gamefunctions.pathfinding import can_reach
from game.gamefunctions.pathfinding import attack_range
from game.gamefunctions.pathfinding import resolve


class WorldLocations(Enum):
    # Enum for different map locations - system works similarly to game state machine
    LOCATION = 0
    WORLD_MAP = 1
    VILLAGE = 2
    GRAVEYARD = 3
    COLOSSEUM = 4
    SHIP = 5
    SPECIAL_MAP = 6


class Location(ABC):

    @abstractmethod
    def __init__(self, player: Player, renderer: pyasge.Renderer, tmx_file: str):
        self.player = player
        self.enemies = []
        self.map = GameMap(renderer, tmx_file)
        self.entity_number = 0
        self.entities = []
        self.tile_positions = []
        self.map_id = WorldLocations.LOCATION
        self.next_map = None

        self.map_loaded = False

        self.current_action_order = [None] * 5

        self.tile_ind = pyasge.Sprite()
        self.tile_ind.z_order = 20

        # self.tile_ind.midpoint = pyasge.Point2D(data.cursor.x, data.cursor.y)
        self.tile_ind.loadTexture("data/sprites/tile_mk2.png")
        self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 32
        self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = 32
        self.tile_ind.width = 64
        self.tile_ind.height = 64

        self.cleared = False
        self.unlocked = True

    @abstractmethod
    def init(self):
        pass

    def reset_location(self, new_pos) -> None:
        # Prepare player for new combat
        self.player.combat_reset()
        player_pos = pyasge.Point2D(self.map.world(new_pos))
        self.player.position = pyasge.Point2D(player_pos.x - 32, player_pos.y - 32)
        self.player.midpoint = pyasge.Point2D(player_pos.x, player_pos.y)
        self.player.tile = self.map.tile(self.player.position)
        self.player.weapon_move()

        # Reset map return value
        self.next_map = self.map_id

    def where_everyone(self) -> None:
        self.tile_positions = []
        for entity in self.entities:
            entity.tile = self.map.tile(entity.position)
            self.tile_positions.append(entity.tile_pos)

    def check_life(self) -> None:
        for enemy in self.enemies:
            if enemy.current_health <= 0:
                self.entities.remove(enemy)
                self.enemies.remove(enemy)
                self.entity_number -= 1

    def battle_click(self, event: pyasge.ClickEvent) -> None:
        click_pos = pyasge.Point2D(event.x, event.y)

        if event.button is pyasge.MOUSE.MOUSE_BTN1 and event.action is pyasge.MOUSE.BUTTON_PRESSED:
            if self.player.your_turn:
                if len(self.player.destination) == 0 and self.player.movement:
                    self.player.move_entity(resolve(click_pos, self.map, self.player))
                    self.player.movement = False

                if self.player.melee and self.player.in_range:
                    tile = self.map.tile(click_pos)
                    self.player.attack(tile, self.entities)
                    self.player.melee = False

    def turn_based_system(self) -> None:
        if len(self.enemies) != 0:
            temp_entities = self.entity_number
            for i in range(self.entity_number):
                if self.entities[i].your_turn:
                    if self.entities[i].action_points <= 0 and len(self.entities[i].destination) == 0:
                        # This stops the game breaking if 2 enemies are killed within the same turn
                        # Need the break because otherwise there are less entities in the list than expected
                        # And the program crashes
                        self.check_life()
                        if temp_entities != self.entity_number:
                            break

                        self.entities[i].your_turn = False
                        self.entities[i].action_points = 2
                        self.entities[i].movement_points += 5
                        if self.entities[i].movement_points > 8:
                            self.entities[i].movement_points = 8
                        if i + 1 == self.entity_number:
                            self.entities[0].your_turn = True

                            # Updates the action order
                            self.check_dead_enemy()
                            for index in range(self.entity_number):
                                self.current_action_order[index] = str(type(self.entities[index]).__name__)

                        else:
                            self.entities[i + 1].your_turn = True

                            # Updates the action order
                            self.check_dead_enemy()
                            index = i + 1

                            for x in range(self.entity_number):
                                self.current_action_order[x] = str(type(self.entities[index]).__name__)
                                if index < (self.entity_number - 1):
                                    index += 1
                                else:
                                    index = 0

        else:
            # If all enemies are dead, change the map
            self.cleared = True
            self.next_map = WorldLocations.WORLD_MAP

    def idle_click(self, event: pyasge.ClickEvent):
        if event.button is pyasge.MOUSE.MOUSE_BTN1 and event.action is pyasge.MOUSE.BUTTON_PRESSED:
            self.move(pyasge.Point2D(event.x, event.y))

    def move(self, event: pyasge.Point2D):
        if len(self.player.destination) == 0:
            self.player.move_entity(world_move(pyasge.Point2D(event.x, event.y), self.map, self.player))

    def square_update(self, event: pyasge.Point2D):
        square_pos = self.map.world(self.map.tile(pyasge.Point2D(event.x, event.y)))
        self.tile_ind.x = square_pos.x - 32
        self.tile_ind.y = square_pos.y - 32

        if not self.cleared:
            if self.player.movement:
                self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = 0
                if can_reach(pyasge.Point2D(event.x, event.y), self.map, self.player):
                    self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                else:
                    self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 32
            if self.player.ranged:
                self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = 32
                if attack_range(pyasge.Point2D(event.x, event.y), self.map, self.player):
                    self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                    self.player.in_range = True
                else:
                    self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 32
                    self.player.in_range = False

            if self.player.melee:
                self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = 64
                if attack_range(pyasge.Point2D(event.x, event.y), self.map, self.player):
                    self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                    self.player.in_range = True
                else:
                    self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 32
                    self.player.in_range = False

        else:
            if can_world_move(pyasge.Point2D(event.x, event.y), self.map):
                self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
            else:
                self.tile_ind.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 32

    def leave_area(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_ENTER:
            self.in_exit_zone()

    def in_exit_zone(self):
        for box in self.map.exit_zones:
            if box[0] < self.player.midpoint.x < box[0] + box[2] and \
                    box[1] < self.player.midpoint.y < box[1] + box[3] and len(self.player.destination) == 0:
                self.next_map = WorldLocations.WORLD_MAP

    def check_dead_enemy(self):
        if self.entity_number < 5:
            number_of_dead = 5 - self.entity_number
            print("Number of Dead : " + str(number_of_dead))
            for index in range(number_of_dead):
                print("Index" + str(4 - index))
                self.current_action_order[4 - index] = "DEAD"

    def idle_controller(self, event: pyasge.Point2D, game_data):
        if game_data.gamepad.RIGHT_BUMPER and not game_data.prev_gamepad.RIGHT_BUMPER:
            self.move(event)

        if game_data.gamepad.LEFT_BUMPER and not game_data.prev_gamepad.LEFT_BUMPER:
            self.in_exit_zone()

    def combat_controller(self, event: pyasge.Point2D, game_data):
        if self.player.your_turn:
            if game_data.gamepad.RIGHT_BUMPER and not game_data.prev_gamepad.RIGHT_BUMPER:
                if len(self.player.destination) == 0 and self.player.movement:
                    self.player.move_entity(resolve(event, self.map, self.player))
                    self.player.movement = False
                if self.player.melee and self.player.in_range:
                    tile = self.map.tile(event)
                    self.player.attack(tile, self.entities)
                    self.player.melee = False
                if self.player.ranged and self.player.in_range:
                    tile = self.map.tile(event)
                    self.player.attack(tile, self.entities)
                    self.player.ranged = False

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def click_handler(self, event: pyasge.ClickEvent) -> None:
        pass

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        self.square_update(event)

    @abstractmethod
    def key_handler(self, event: pyasge.KeyEvent) -> None:
        pass

    @abstractmethod
    def controller_handler(self, event: pyasge.Point2D, game_data) -> None:
        pass

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        self.player.fixed_update(game_time)

        for enemy in self.enemies:
            enemy.fixed_update(game_time)

    @abstractmethod
    def update(self, game_time: pyasge.GameTime, data) -> WorldLocations:
        if not self.cleared:
            self.turn_based_system()
            self.map_loaded = True

        self.player.update(game_time, data)
        for enemy in self.enemies:
            enemy.update(game_time, data)

        self.check_life()
        self.where_everyone()

        # If next map has been changed, then return the new map
        # Lock the current map, so it cannot be re-entered
        if self.next_map != self.map_id:
            self.unlocked = False
            return self.next_map

        return self.map_id

    @abstractmethod
    def render(self, renderer: pyasge.Renderer, data) -> None:
        self.player.render(renderer)

        for enemy in self.enemies:
            enemy.render(renderer)

        if self.player.movement or self.player.melee or self.player.ranged:
            renderer.render(self.tile_ind)
