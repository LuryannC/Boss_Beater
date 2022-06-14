import pyasge

from game.gameobjects.Location.location import Location
from game.gameobjects.Location.location import WorldLocations
from game.gameobjects.Entities.player import Player


class SpecialMap(Location):

    def __init__(self, player: Player, renderer: pyasge.Renderer, tmx_file: str):
        super().__init__(player, renderer, tmx_file)

        self.map_id = WorldLocations.SPECIAL_MAP
        self.next_map = self.map_id
        self.cleared = True
        self.capy = []
        self.fps = 0.3
        self.frame = 0

        self.unlocked = False
        self.special_on = False
        self.can_exit = False

        for i in range(12):
            self.capy.append(pyasge.Sprite())
        self.init()

    def init(self):
        self.entity_number = 1
        self.entities.append(self.player)

        for i in range(len(self.capy)):
            self.capy[i].x = self.map.spawns[i][0]
            self.capy[i].y = self.map.spawns[i][1]

        for i in range(len(self.capy)):
            if i < 6:
                self.capy[i].loadTexture("./data/sprites/capy-left.png")
                self.capy[i].scale = 2.3
                self.capy[i].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                self.capy[i].src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 32
                self.capy[i].width = 32
                self.capy[i].height = 32
                self.capy[i].y -= self.capy[i].height * 2
                self.capy[i].x -= self.capy[i].width
            else:
                self.capy[i].loadTexture("./data/sprites/capy.png")
                self.capy[i].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
                self.capy[i].src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 32
                self.capy[i].width = 32
                self.capy[i].y -= self.capy[i].height * 2
                self.capy[i].x -= self.capy[i].width + 16
                self.capy[i].scale = 2.3

    def reset(self) -> None:
        self.reset_location((14, 1))

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        self.idle_click(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_ENTER:
            print("Enter")
            for box in self.map.exit_zones:
                if box[0] < self.player.midpoint.x < box[0] + box[2] and \
                        box[1] < self.player.midpoint.y < box[1] + box[3] and len(self.player.destination) == 0:

                    if box[4] == "leave" and self.can_exit:
                        self.special_on = True

    def controller_handler(self, event: pyasge.Point2D, game_data) -> None:
        self.square_update(event)

        self.idle_controller(event, game_data)

    def update(self, game_time: pyasge.GameTime, data) -> WorldLocations:
        if data.special:
            self.play_animation(game_time)
            self.can_exit = True

        if data.special and self.special_on:
            data.special_exit = True

        return super().update(game_time, data)

    def render(self, renderer: pyasge.Renderer, data) -> None:
        super().render(renderer, data)

        if data.special:
            for cap in self.capy:
                data.renderer.shader = data.shaders["damage"]
                renderer.render(cap)
        self.map.render(renderer)
        data.renderer.shader = None

    def play_animation(self, game_time: pyasge.GameTime):
        self.fps -= game_time.fixed_timestep
        if self.fps < 0:
            self.fps = 0.1
            self.frame += 1
        if self.frame > 4:
            self.frame = 0

        for cap in self.capy:
            cap.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = self.frame * cap.width
