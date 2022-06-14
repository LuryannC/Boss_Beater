import pyasge
import math
ARROW_SPEED = 7


class Arrow:

    def __init__(self, spawn: pyasge.Point2D, dest: pyasge.Point2D) -> None:
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("data/sprites/arrow.png")
        self.sprite.width = 32
        self.sprite.height = 15
        self.sprite.x = spawn.x
        self.sprite.y = spawn.y
        self.sprite.z_order = 50
        self.angled = False
        self.destination = pyasge.Point2D(dest.x - self.sprite.width * 0.5, dest.y - self.sprite.height * 0.5)

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        self.sprite.x += (self.destination.x - self.sprite.x) * ARROW_SPEED * game_time.fixed_timestep
        self.sprite.y += (self.destination.y - self.sprite.y) * ARROW_SPEED * game_time.fixed_timestep

    def update(self, game_time: pyasge.GameTime) -> None:
        if self.destination.distance([self.sprite.x, self.sprite.y]) < 5:
            self.sprite.z_order = -5
            self.sprite.x = self.destination.x
            self.sprite.y = self.destination.y

        if abs(self.destination.x - self.sprite.x) < 0.5:
            self.sprite.x = self.destination.x

        if abs(self.destination.y - self.sprite.y) < 0.5:
            self.sprite.y = self.destination.y

        # Angle the arrow on spawn
        if not self.angled:
            v1 = self.position
            v2 = self.destination
            dx = v2.x - v1.x
            dy = v2.y - v1.y

            angle = math.atan2(dy, dx) - 1.5708
            self.sprite.rotation = angle + (90 * (math.pi / 180))
            self.angled = True

    def render(self, renderer: pyasge.Renderer):
        renderer.render(self.sprite)

    @property
    def position(self) -> pyasge.Point2D:
        return pyasge.Point2D(self.sprite.x, self.sprite.y)
