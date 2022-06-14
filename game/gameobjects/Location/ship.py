import pyasge

from game.gameobjects.Entities.player import Player
from game.gameobjects.Entities.Enemies.thief import ThiefEnemy
from game.gameobjects.Entities.Enemies.boss_pirate import PirateBoss

from game.gameobjects.Location.location import Location
from game.gameobjects.Location.location import WorldLocations


class Ship(Location):

    def __init__(self, player: Player, renderer: pyasge.Renderer, tmx_file: str):
        super().__init__(player, renderer, tmx_file)

        self.map_id = WorldLocations.SHIP
        self.next_map = self.map_id
        self.init()

    def init(self):
        # Add enemies to list
        self.enemies.append(PirateBoss())
        self.enemies.append(ThiefEnemy())
        self.enemies.append(ThiefEnemy())
        self.enemies.append(ThiefEnemy())

        # Position enemies accordingly
        enemy_pos = pyasge.Point2D(self.map.world((14, 15)))
        self.enemies[0].position = pyasge.Point2D(enemy_pos.x - 32, enemy_pos.y - 32)
        self.enemies[0].midpoint = pyasge.Point2D(enemy_pos.x, enemy_pos.y)

        enemy_pos = pyasge.Point2D(self.map.world((25, 10)))
        self.enemies[1].position = pyasge.Point2D(enemy_pos.x - 32, enemy_pos.y - 32)
        self.enemies[1].midpoint = pyasge.Point2D(enemy_pos.x, enemy_pos.y)

        enemy_pos = pyasge.Point2D(self.map.world((20, 10)))
        self.enemies[2].position = pyasge.Point2D(enemy_pos.x - 32, enemy_pos.y - 32)
        self.enemies[2].midpoint = pyasge.Point2D(enemy_pos.x, enemy_pos.y)

        enemy_pos = pyasge.Point2D(self.map.world((18, 12)))
        self.enemies[3].position = pyasge.Point2D(enemy_pos.x - 32, enemy_pos.y - 32)
        self.enemies[3].midpoint = pyasge.Point2D(enemy_pos.x, enemy_pos.y)

        # Add all entities to list for combat
        self.entity_number = len(self.enemies) + 1

        self.entities.append(self.player)
        for enemy in self.enemies:
            self.entities.append(enemy)

        # Updates the action order for FIRST turn
        for index in range(5):
            self.current_action_order[index] = str(type(self.entities[index]).__name__)

    def reset(self) -> None:
        self.reset_location((25, 7))

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
            data.bg_sound_groups.get("ship_music").stop()
            self.map_loaded = False

        return super().update(game_time, data)

    def render(self, renderer: pyasge.Renderer, data) -> None:
        super().render(renderer, data)

        self.map.render(renderer)

