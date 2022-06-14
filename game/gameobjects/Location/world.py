import pyasge
from game.gamedata import GameData
from game.gameobjects.Entities.player import Player
from game.gameobjects.Entities.entity import Entity
from game.gameobjects.gamemap import GameMap
from game.gamefunctions.pathfinding import world_move
from game.gamefunctions.pathfinding import can_world_move
from game.gamefunctions.pathfinding import walk_there

from game.gameobjects.Location.location import Location
from game.gameobjects.Location.location import WorldLocations


class World(Location):

    def __init__(self, player: Player, renderer: pyasge.Renderer, tmx_file: str):
        super().__init__(player, renderer, tmx_file)

        self.map_id = WorldLocations.WORLD_MAP
        self.next_map = self.map_id
        self.cleared = True

        self.last_spot = [28, 6]
        self.init()
        self.in_place = False
        self.current_place = None

    def init(self):
        self.entity_number = 1
        self.entities.append(self.player)

    def reset(self) -> None:
        # Puts the player in the last spot they were in when they swapped maps.
        # Means player will spawn outside landmark they entered
        self.reset_location(self.last_spot)

    def world_location(self) -> WorldLocations:
        for box in self.map.exit_zones:
            if box[0] < self.player.midpoint.x < box[0] + box[2] and \
                    box[1] < self.player.midpoint.y < box[1] + box[3] and len(self.player.destination) == 0:

                if box[4] == "village":
                    return WorldLocations.VILLAGE
                elif box[4] == "graveyard":
                    return WorldLocations.GRAVEYARD
                elif box[4] == "colosseum":
                    return WorldLocations.COLOSSEUM
                elif box[4] == "ship":
                    return WorldLocations.SHIP
                elif box[4] == "special_map":
                    return WorldLocations.SPECIAL_MAP


        # for bound in self.map.exit_zones:
        #     """
        #     bound is a list of 4 things
        #     bound [0] - left side
        #     bound [1] - top
        #     bound [2] - width
        #     bound [3] - height
        #
        #     point2d(bound[0], bound[1]) - top left of the square
        #     point2d(bound[0] + bound[2], bound[1] + bound[3]) - bottom right of the square
        #     """
#
        #     plr_bounds = [self.player.sprite.x, self.player.sprite.y, self.player.sprite.getWorldBounds().v3,
        #                     self.player.sprite.getWorldBounds().v4]
#
        #     """
        #     Find out what side u hit
        #     """
        #     x_pen = 0
        #     y_pen = 0
        #     right = False
        #     bottom = False
#
        #     # RIGHT
        #     if bound[0] < plr_bounds[0] < bound[0] + bound[2]:
        #         x_pen = (bound[0] + bound[2]) - plr_bounds[0]
        #         right = True
        #     # LEFT
        #     elif bound[0] < plr_bounds[0] + plr_bounds[2] < bound[0] + bound[2]:
        #         x_pen = (plr_bounds[0] + plr_bounds[2]) - bound[0]
        #     # BOTTOM
        #     if bound[1] < plr_bounds[1] < bound[1] + bound[3]:
        #         bottom = True
        #         y_pen = (bound[1] + bound[3]) - plr_bounds[1]
        #     # TOP
        #     elif bound[1] < plr_bounds[1] + plr_bounds[3] < bound[1] + bound[3]:
        #         y_pen = (plr_bounds[1] + plr_bounds[3]) - bound[1]
#
        #     # NO COLLISION
        #     if x_pen == 0 or y_pen == 0:
        #         return False
        #     # COLLISION
        #     else:
        #         # Whichever pen is smaller, is whether it was left/right or top/bottom
        #         if x_pen < y_pen:
        #             # Set position accordingly
        #             if right:
        #                 self.player.sprite.x = bound[0] + bound[2]
        #             else:
        #                 self.player.sprite.x = bound[0] - self.player.sprite.getWorldBounds().v3
        #         else:
        #             # Set position accordingly
        #             if bottom:
        #                 self.player.sprite.y = bound[1] + bound[3]
        #             else:
        #                 self.player.sprite.y = bound[1] - self.player.sprite.getWorldBounds().v4
        #         return True

        return WorldLocations.WORLD_MAP





    def door_handler(self, data) -> bool:
        self.current_place = self.world_location()

        if self.current_place is not WorldLocations.WORLD_MAP:
            self.in_place = True
            data.door.x = self.player.x
            data.door.y = self.player.y - 64
            if self.current_place == WorldLocations.VILLAGE:
                data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                return True
            elif self.current_place == WorldLocations.GRAVEYARD:
                if data.game_map.get("graveyard").unlocked:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                    return True
                else:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 64
                    return False
            elif self.current_place == WorldLocations.COLOSSEUM:
                if data.game_map.get("colosseum").unlocked:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                    return True
                else:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 64
                    return False
            elif self.current_place == WorldLocations.SHIP:
                if data.game_map.get("ship").unlocked:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                    return True
                else:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 64
                    return False
            elif self.current_place == WorldLocations.SPECIAL_MAP:

                if data.game_map.get("special_map").unlocked:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                    return True
                else:
                    data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 64
                    return False
        else:
            self.in_place = False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        self.idle_click(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_ENTER:
            print("enter")
            self.next_map = self.world_location()

    def controller_handler(self, event: pyasge.Point2D, game_data) -> None:
        self.square_update(event)

        if game_data.gamepad.RIGHT_BUMPER and not game_data.prev_gamepad.RIGHT_BUMPER:
            self.move(event)

        if game_data.gamepad.LEFT_BUMPER and not game_data.prev_gamepad.LEFT_BUMPER:
            self.next_map = self.world_location()

    def update(self, game_time: pyasge.GameTime, data) -> WorldLocations:
        self.player.update(game_time, data)
        self.where_everyone()

        # Only swap if location is unlocked
        if self.door_handler(data):
            if self.next_map != self.map_id:
                print("switch")
                self.last_spot = self.player.tile
                return self.next_map
        else:
            self.next_map = self.map_id

        return self.map_id

    def render(self, renderer: pyasge.Renderer, data) -> None:
        super().render(renderer, data)

        if self.in_place:
            renderer.render(data.door)

        self.map.render(renderer)
