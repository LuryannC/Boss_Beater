import pyasge

from game.gameobjects.Entities.player import Player
from game.gameobjects.Entities.Enemies.assassin import AssassinsEnemy
from game.gameobjects.Entities.Enemies.boss_minotaur import MinotaurBoss

from game.gameobjects.Location.location import Location
from game.gameobjects.Location.location import WorldLocations


class Colosseum(Location):

    def __init__(self, player: Player, renderer: pyasge.Renderer, tmx_file: str):
        super().__init__(player, renderer, tmx_file)

        self.map_id = WorldLocations.COLOSSEUM
        self.next_map = self.map_id
        self.init()

    def init(self):
        # Add enemies to list
        self.enemies.append(AssassinsEnemy())
        self.enemies.append(AssassinsEnemy())
        self.enemies.append(AssassinsEnemy())
        self.enemies.append(MinotaurBoss())

        # Position enemies accordingly
        self.enemies[0].position = pyasge.Point2D(self.map.world((10, 20)))
        self.enemies[0].position = pyasge.Point2D(self.enemies[0].x + 32, self.enemies[0].y + 32)

        self.enemies[1].position = pyasge.Point2D(self.map.world((30, 20)))
        self.enemies[1].position = pyasge.Point2D(self.enemies[1].x + 32, self.enemies[1].y + 32)

        self.enemies[2].position = pyasge.Point2D(self.map.world((20, 20)))
        self.enemies[2].position = pyasge.Point2D(self.enemies[2].x + 32, self.enemies[2].y + 32)

        self.enemies[3].position = pyasge.Point2D(self.map.world((18, 10)))
        self.enemies[3].position = pyasge.Point2D(self.enemies[3].x + 32, self.enemies[3].y + 32)

        # Add entities to list for combat
        self.entity_number = len(self.enemies) + 1

        self.entities.append(self.player)
        for enemy in self.enemies:
            self.entities.append(enemy)

        # Updates the action order for FIRST turn
        for index in range(5):
            self.current_action_order[index] = str(type(self.entities[index]).__name__)

    def reset(self) -> None:
        self.reset_location((20, 35))

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        if self.cleared:
            self.idle_click(event)
        else:
            self.battle_click(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if self.cleared:
            self.leave_area(event)

    def controller_handler(self, event: pyasge.Point2D, game_data) -> None:
        self.square_update(event)

        if self.cleared:
            self.idle_controller(event, game_data)
        else:
            self.combat_controller(event, game_data)

    def update(self, game_time: pyasge.GameTime, data) -> WorldLocations:
        if self.cleared:
            data.bg_sound_groups.get("village_music").stop()
            self.map_loaded = False

        return super().update(game_time, data)

    def render(self, renderer: pyasge.Renderer, data) -> None:
        super().render(renderer, data)

        data.renderer.shader = data.shaders["sand"]
        self.map.render(renderer)
        data.renderer.shader = None

