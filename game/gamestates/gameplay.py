import pyasge
from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID

from game.gameobjects.Location.location import WorldLocations
from game.gameobjects.Entities.player import PlayerMode
from game.gameobjects.Weaponry.arrow import Arrow

from game.gameobjects.UI.uigameplay import GameplayUI


def is_inside(bounds, point: pyasge.Point2D):
    if bounds.v1.x < point.x < bounds.v2.x and bounds.v1.y < point.y < bounds.v3.y:
        return True
    return False


class GamePlay(GameState):
    """ The game play state is the core of the game itself.

    The role of this class is to process the game logic, update
    the players positioning and render the resultant game-world.
    The logic for deciding on victory or loss should be handled by
    this class and its update function should return GAME_OVER or
    GAME_WON when the end game state is reached.
    """

    def __init__(self, data: GameData) -> None:
        """ Creates the game world

        Use the constructor to initialise the game world in a "clean"
        state ready for the player. This includes resetting of player's
        health and the enemy positions.

        Args:
            data (GameData): The game's shared data
        """
        super().__init__(data)

        # Set state ID and create return value for swapping between states
        self.id = GameStateID.GAME_PLAY
        self.return_value = GameStateID.GAME_PLAY

        self.data.renderer.setClearColour(pyasge.COLOURS.CORAL)
        # Create sprite to apply Water shader to
        self.water = pyasge.Sprite()
        self.water.width = 4000
        self.water.height = 4000

        self.fog = pyasge.Sprite()
        self.fog.width = 1920
        self.fog.height = 1080
        self.fog.alpha = 0.2

        # sets up gameplay UI
        self.ui = GameplayUI(self.data, 50)
        # The self.data in uigameplay.py does not contain the font for some reason
        self.ui.init_stamina_counter(self.data.fonts["m5x7"])
        self.ui.init_action_order_list(self.data.fonts["m5x7"])

        # sets up the camera and points it at the player
        map_mid = [
            self.data.current_map.map.width * self.data.current_map.map.tile_size[0] * 0.5,
            self.data.current_map.map.height * self.data.current_map.map.tile_size[1] * 0.5
        ]

        self.camera = pyasge.Camera(map_mid, self.data.game_res[0], self.data.game_res[1])
        self.camera.zoom = 1

        # Setup initial player position
        player_pos = pyasge.Point2D(self.data.current_map.map.world((16, 10)))
        self.data.player.position = pyasge.Point2D(player_pos.x - 32, player_pos.y - 32)
        self.data.player.midpoint = pyasge.Point2D(player_pos.x, player_pos.y)
        self.data.player.weapon_move()
        self.next_map = None

        self.transition = pyasge.Sprite()
        self.transition.loadTexture("data/textures/UI Textures/transition overlay.png")
        self.transition.scale = 2
        self.transition.alpha = 0
        self.transition.z_order = 100
        self.fade_in = False
        self.fade_out = False

        self.shader_timer = 0

    def reset(self) -> None:
        self.transition.alpha = 0
        self.fade_in = False
        self.fade_out = False
        self.return_value = self.id

    def click_handler(self, event: pyasge.ClickEvent) -> None:

        self.data.current_map.click_handler(event)

        if event.button is pyasge.MOUSE.MOUSE_BTN1 and \
                event.action is pyasge.MOUSE.BUTTON_PRESSED:

            # Check for clicks with UI buttons
            if self.data.player.your_turn and not self.data.current_map.cleared:
                # Create arrow
                if self.data.player.ranged and self.data.player.in_range:
                    destination = self.data.current_map.map.tile(pyasge.Point2D(event.x, event.y))
                    arrow = Arrow(self.data.player.midpoint, self.data.current_map.map.world(destination))
                    self.data.arrows.append(arrow)
                    self.data.player.ranged = False

                if is_inside(self.ui.button_move.getWorldBounds(), self.to_screen(pyasge.Point2D(event.x, event.y))):
                    self.data.player.movement = True
                    self.data.player.melee = False
                    self.data.player.ranged = False
                if is_inside(self.ui.button_melee.getWorldBounds(), self.to_screen(pyasge.Point2D(event.x, event.y))):
                    self.data.player.melee = True
                    self.data.player.movement = False
                    self.data.player.ranged = False
                    self.data.player.mode = PlayerMode.MELEE
                if is_inside(self.ui.button_ranged.getWorldBounds(), self.to_screen(pyasge.Point2D(event.x, event.y))):
                    self.data.player.ranged = True
                    self.data.player.melee = False
                    self.data.player.movement = False
                    self.data.player.mode = PlayerMode.RANGED
                if is_inside(self.ui.button_end.getWorldBounds(), self.to_screen(pyasge.Point2D(event.x, event.y))):
                    self.data.player.action_points = 0
                    self.data.player.movement = False
                    self.data.player.melee = False
                    self.data.player.ranged = False

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """ Listens for mouse movement events from the game engine """
        self.data.current_map.move_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """ Listens for key events from the game engine """
        # TEMP - swap to game_win state
        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_D \
                and self.data.special and self.data.current_map.map_id == WorldLocations.SPECIAL_MAP:
            self.return_value = GameStateID.GAME_WIN

        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_F:
            print("f")
            self.return_value = GameStateID.GAME_OVER

        # TEMP - Special
        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_P:
            self.data.special = True

        # Allow player to pick for turn based using keys
        # Instead of needing to click them from the UI
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_Q:
                self.data.player.movement = True
                self.data.player.melee = False
                self.data.player.ranged = False

            if event.key == pyasge.KEYS.KEY_W:
                self.data.player.melee = True
                self.data.player.movement = False
                self.data.player.ranged = False
                self.data.player.mode = PlayerMode.MELEE

            if event.key == pyasge.KEYS.KEY_E:
                self.data.player.ranged = True
                self.data.player.movement = False
                self.data.player.melee = False
                self.data.player.mode = PlayerMode.RANGED

            if event.key == pyasge.KEYS.KEY_R:
                self.data.player.action_points = 0
                self.data.player.movement = False
                self.data.player.melee = False
                self.data.player.ranged = False

        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_ENTER:
            if self.data.current_map.map_id == WorldLocations.SPECIAL_MAP:
                self.data.bg_sound_groups.get("special").stop()
                chest_pos = self.data.current_map.map.world((14, 6))
                player_pos = self.data.current_map.map.tile(pyasge.Point2D(self.data.player.position))
                if player_pos == self.data.current_map.map.tile(chest_pos):
                    self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("special"))
                    self.data.bg_audio_channel.volume = self.data.volume * 2
                    self.data.special = True

        self.data.current_map.key_handler(event)

    def controller_handler(self, game_time: pyasge.GameTime) -> None:
        # Move cursor based on joystick movement
        velocity = pyasge.Point2D()
        velocity.x = self.data.inputs.getGamePad().AXIS_LEFT_X * 400
        velocity.y = self.data.inputs.getGamePad().AXIS_LEFT_Y * 400
        self.data.cursor.x += velocity.x * game_time.fixed_timestep
        self.data.cursor.y += velocity.y * game_time.fixed_timestep

        # Stop player moving cursor outside the map
        # As this will crash the game
        view = [32, self.data.current_map.map.width * 64 - 32, 32, self.data.current_map.map.height * 64 - 32]

        if self.data.cursor.x < view[0]:
            self.data.cursor.x = view[0]
        elif self.data.cursor.x > view[1]:
            self.data.cursor.x = view[1]

        if self.data.cursor.y < view[2]:
            self.data.cursor.y = view[2]
        elif self.data.cursor.y > view[3]:
            self.data.cursor.y = view[3]
        # Create fake click event
        event = pyasge.Point2D(self.data.cursor.x, self.data.cursor.y)

        if self.data.gamepad.A and not self.data.prev_gamepad.A:
            if self.data.current_map.map_id == WorldLocations.SPECIAL_MAP:
                self.data.bg_sound_groups.get("special").stop()
                chest_pos = self.data.current_map.map.world((14, 6))
                player_pos = self.data.current_map.map.tile(pyasge.Point2D(self.data.player.position))
                if player_pos == self.data.current_map.map.tile(chest_pos):
                    self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("special"))
                    self.data.bg_audio_channel.volume = self.data.volume * 2
                    self.data.special = True

        # Create arrow
        if self.data.player.ranged and self.data.gamepad.RIGHT_BUMPER and not self.data.prev_gamepad.RIGHT_BUMPER:
            destination = self.data.current_map.map.tile(pyasge.Point2D(event.x, event.y))
            arrow = Arrow(self.data.player.midpoint, self.data.current_map.map.world(destination))
            self.data.arrows.append(arrow)
            print("Clicked Ranged Button")
            self.data.player.ranged = False
            self.data.player.movement = True

        # Allow player to pick for turn based using controller buttons
        # As there is no click for it
        if self.data.gamepad.A and not self.data.prev_gamepad.A and self.data.player.your_turn:
            print("Controller input A")
            self.data.player.movement = True
            self.data.player.melee = False
            self.data.player.ranged = False

        if self.data.gamepad.B and not self.data.prev_gamepad.B and self.data.player.your_turn:
            print("Controller input B")
            self.data.player.melee = True
            self.data.player.movement = False
            self.data.player.ranged = False
            self.data.player.mode = PlayerMode.MELEE

        if self.data.gamepad.X and not self.data.prev_gamepad.X and self.data.player.your_turn:
            print("Controller input Y")
            self.data.player.ranged = True
            self.data.player.melee = False
            self.data.player.movement = False
            self.data.player.mode = PlayerMode.RANGED

        if self.data.gamepad.Y and not self.data.prev_gamepad.Y and self.data.player.your_turn:
            print("Controller input X")
            self.data.player.action_points = 0
            self.data.player.movement = False
            self.data.player.melee = False
            self.data.player.ranged = False

        self.data.current_map.controller_handler(pyasge.Point2D(self.data.cursor.x, self.data.cursor.y), self.data)

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """ Simulates deterministic time steps for the game objects"""
        for arrow in self.data.arrows:
            arrow.fixed_update(game_time)

        self.resolve_arrows()

        self.data.current_map.fixed_update(game_time)

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        """ Updates the game world

        Processes the game world logic. You should handle collisions,
        actions and AI actions here. At present cannonballs are
        updated and so are player collisions with the islands, but
        consider how the ships will react to each other

        Args:
            game_time (pyasge.GameTime): The time between ticks.
        """
        for arrow in self.data.arrows:
            arrow.update(game_time)

        self.next_map = self.data.current_map.update(game_time, self.data)
        if self.next_map != self.data.current_map.map_id:
            self.fade_out = True

        if self.fade_out:
            self.do_fade_out(game_time.fixed_timestep)
        if self.fade_in:
            self.do_fade_in(game_time.fixed_timestep)

        self.update_camera()
        self.controller_handler(game_time)
        self.shader_timer += 1 * game_time.fixed_timestep

        # Initialise shader water shaders values
        if self.data.current_map.map_id == WorldLocations.VILLAGE:
            self.data.shaders["water"].uniform("time").set(self.shader_timer * 0.000009)
        else:
            self.data.shaders["water"].uniform("time").set(self.shader_timer * 0.00003)
        self.data.shaders["fog"].uniform("time").set(self.shader_timer)
        self.data.shaders["sand"].uniform("time").set(self.shader_timer * 0.4)
        self.data.shaders["damage"].uniform("time").set(self.shader_timer * 10.0)
        self.ui.update_health(self.data.player.current_health, self.data.player.max_health)
        self.ui.update_stamina(self.data.player.movement_points)
        self.ui.update_health(self.data.player.current_health, self.data.player.max_health)

        if self.data.player.current_health <= 0:
            self.return_value = GameStateID.GAME_OVER
            self.data.bg_sound_groups.get("default").stop()

        if self.data.game_map["graveyard"].cleared and self.data.game_map["ship"].cleared and \
                self.data.game_map["colosseum"].cleared:
            self.data.game_map["special_map"].unlocked = True

        if self.data.current_map.map_loaded:
            self.ui.update_action_order(self.data.current_map.current_action_order)

        if self.return_value != self.id:
            return self.return_value

        if self.data.special_exit:
            self.return_value = GameStateID.GAME_WIN

        return self.id

    def update_camera(self):
        """ Updates the camera based on gamepad input"""
        self.camera.lookAt(self.data.player.midpoint)

        view = [
            self.data.game_res[0] * 0.5 / self.camera.zoom,
            self.data.current_map.map.width * 64 - self.data.game_res[0] * 0.5 / self.camera.zoom,
            self.data.game_res[1] * 0.5 / self.camera.zoom,
            self.data.current_map.map.height * 64 - self.data.game_res[1] * 0.5 / self.camera.zoom
        ]
        self.camera.clamp(view)

    def render(self, game_time: pyasge.GameTime) -> None:
        """ Renders the game world and the UI """

        self.data.renderer.setViewport(pyasge.Viewport(0, 0, self.data.game_res[0], self.data.game_res[1]))
        self.data.renderer.setProjectionMatrix(self.camera.view)
        self.data.renderer.shader = self.data.shaders["water"]
        self.data.renderer.render(self.water)
        self.data.renderer.shader = None
        for arrow in self.data.arrows:
            arrow.render(self.data.renderer)

        self.data.current_map.render(self.data.renderer, self.data)
        self.render_ui()

    def render_ui(self) -> None:
        """ Render the UI elements and map to the whole window """
        # set a new view that covers the width and height of game
        camera_view = pyasge.CameraView(self.data.renderer.resolution_info.view)
        vp = self.data.renderer.resolution_info.viewport
        self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)

        self.data.renderer.render(self.transition)

        if self.data.current_map.map_id == WorldLocations.WORLD_MAP or self.data.current_map.map_id == WorldLocations.VILLAGE or self.data.current_map.map_id == WorldLocations.SPECIAL_MAP:
            pass
        else:
            self.ui.render(self.data.renderer)
        # this restores the original camera view
        self.data.renderer.setProjectionMatrix(camera_view)

        # renders gameplay ui

    def to_world(self, pos: pyasge.Point2D) -> pyasge.Point2D:
        """
        Converts from screen position to world position
        :param pos: The position on the current game window camera
        :return: Its actual/absolute position in the game world
        """
        view = self.camera.view
        x = (view.max_x - view.min_x) / self.data.game_res[0] * pos.x
        y = (view.max_y - view.min_y) / self.data.game_res[1] * pos.y
        x = view.min_x + x
        y = view.min_y + y

        return pyasge.Point2D(x, y)

    def to_screen(self, pos: pyasge.Point2D) -> pyasge.Point2D:
        """
        Converts from world position to screen position
        """
        view = self.camera.view
        x = pos.x - view.min_x
        y = pos.y - view.min_y

        return pyasge.Point2D(x, y)

    def change_map(self, new_map: WorldLocations):
        if new_map == self.data.current_map.map_id:
            pass
        else:
            if new_map == WorldLocations.WORLD_MAP:
                self.data.bg_sound_groups.get("default").stop()
                self.data.special = False
                print("world")
                self.data.game_map["world_map"].reset()
                self.data.current_map = self.data.game_map.get("world_map")
                self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("world_music"))
                self.data.bg_audio_channel.volume = self.data.volume * 2

            elif new_map == WorldLocations.VILLAGE:
                self.data.bg_sound_groups.get("world_music").stop()
                print("village")
                self.data.game_map["spawn_village"].reset()
                self.data.current_map = self.data.game_map.get("spawn_village")
                self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("default"))
                self.data.bg_audio_channel.volume = self.data.volume * 2

            elif new_map == WorldLocations.GRAVEYARD:
                self.data.bg_sound_groups.get("world_music").stop()
                self.data.game_map["graveyard"].reset()
                self.data.current_map = self.data.game_map.get("graveyard")
                self.data.bg_audio_channel = self.data.audio_system.play_sound(
                    self.data.bg_sound.get("graveyard_music"))
                self.data.bg_audio_channel.volume = self.data.volume * 2

            elif new_map == WorldLocations.COLOSSEUM:
                self.data.bg_sound_groups.get("world_music").stop()
                self.data.game_map["colosseum"].reset()
                self.data.current_map = self.data.game_map.get("colosseum")
                self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("village_music"))
                self.data.bg_audio_channel.volume = self.data.volume * 2

            elif new_map == WorldLocations.SHIP:
                self.data.bg_sound_groups.get("world_music").stop()
                self.data.game_map["ship"].reset()
                self.data.current_map = self.data.game_map.get("ship")
                self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("ship_music"))
                self.data.bg_audio_channel.volume = self.data.volume * 2

            elif new_map == WorldLocations.SPECIAL_MAP:
                self.data.bg_sound_groups.get("world_music").stop()
                self.data.game_map["special_map"].reset()
                self.data.current_map = self.data.game_map.get("special_map")

            self.data.prev_gamepad = self.data.gamepad
            self.data.cursor.x = self.data.player.x
            self.data.cursor.y = self.data.player.y

            self.next_map = None

    def resolve_arrows(self) -> None:
        for arrow in self.data.arrows:
            print("arrows")
            if arrow.position == arrow.destination:
                tile = self.data.current_map.map.tile(arrow.position)
                self.data.player.attack(tile, self.data.current_map.entities)
                print("hit")
                self.data.arrows.remove(arrow)

    def do_fade_out(self, fixed_timestep):
        self.transition.alpha += 3 * fixed_timestep
        if self.transition.alpha >= 2:
            self.transition.alpha = 1
            self.fade_in = True
            self.fade_out = False
            self.change_map(self.next_map)

    def do_fade_in(self, fixed_timestep):
        self.transition.alpha -= 3 * fixed_timestep
        if self.transition.alpha <= 0:
            self.transition.alpha = 0
            self.fade_in = False
