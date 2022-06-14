import pyasge
from game.gamedata import GameData
from game.gameobjects.Entities.player import Player
from game.gameobjects.Entities.entity import Entity
from game.gameobjects.gamemap import GameMap
from game.gamefunctions.pathfinding import world_move

from game.gameobjects.Location.location import Location
from game.gameobjects.Location.location import WorldLocations


class Village(Location):

    def __init__(self, player: Player, renderer: pyasge.Renderer, tmx_file: str):
        super().__init__(player, renderer, tmx_file)

        self.map_id = WorldLocations.VILLAGE
        self.next_map = self.map_id
        self.cleared = True

        self.init()

    def init(self):
        self.entity_number = 1
        self.entities.append(self.player)

    def reset(self) -> None:
        self.reset_location((16, 10))

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        self.idle_click(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        self.leave_area(event)

    def controller_handler(self, event: pyasge.Point2D, game_data) -> None:
        self.square_update(event)

        self.idle_controller(event, game_data)

    def update(self, game_time: pyasge.GameTime, data) -> WorldLocations:
        return super().update(game_time, data)

    def render(self, renderer: pyasge.Renderer, data) -> None:
        super().render(renderer, data)

        self.map.render(renderer)
