import random
import pyasge
import pyfmodex
from pyfmodex.flags import MODE

from game.gamedata import GameData
from game.gameobjects.Location.colosseum import Colosseum
from game.gameobjects.Location.location import WorldLocations
from game.gameobjects.Location.world import World
from game.gameobjects.Location.village import Village
from game.gameobjects.Location.graveyard import Graveyard
from game.gameobjects.Location.ship import Ship
from game.gameobjects.Location.special_map import SpecialMap
from game.gamestates.gameplay import GamePlay
from game.gamestates.gamemenu import GameMenu
from game.gamestates.gamewin import GameWin
from game.gamestates.gameover import GameOver
from game.gamestates.gamemenu import GameStateID
from game.gameobjects.Entities.player import Player


class MyASGEGame(pyasge.ASGEGame):
    """The ASGE Game in Python."""

    def __init__(self, settings: pyasge.GameSettings):
        """
        The constructor for the game.

        The constructor is responsible for initialising all the needed
        subsystems,during the game's running duration. It directly
        inherits from pyasge.ASGEGame which provides the window
        management and standard game loop.

        :param settings: The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.data = GameData()
        self.renderer.setBaseResolution(self.data.game_res[0], self.data.game_res[1], pyasge.ResolutionPolicy.MAINTAIN)
        random.seed(a=None, version=2)

        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        # Load all the shaders
        self.data.shaders["example"] = self.data.renderer.loadPixelShader("/data/shaders/example_rgb.frag")
        self.data.shaders["damage"] = self.data.renderer.loadPixelShader("/data/shaders/damage_shader.frag")
        self.data.shaders["test"] = self.data.renderer.loadPixelShader("/data/shaders/example_rgb.frag")
        self.data.shaders["water"] = self.data.renderer.loadPixelShader("/data/shaders/water_shader.frag")
        self.data.shaders["fog"] = self.data.renderer.loadPixelShader("/data/shaders/fog_shader.frag")
        self.data.shaders["sand"] = self.data.renderer.loadPixelShader("/data/shaders/sand_shader.frag")
        self.data.prev_gamepad = self.data.gamepad = self.inputs.getGamePad()

        self.data.player = Player()
        # Create all the locations within the world
        self.data.game_map["colosseum"] = Colosseum(self.data.player, self.data.renderer, "./data/map/colosseum.tmx")
        self.data.game_map["graveyard"] = Graveyard(self.data.player, self.data.renderer,
                                                    "./data/map/graveyard2.tmx")
        self.data.game_map["spawn_village"] = Village(self.data.player, self.data.renderer,
                                                      "./data/map/Spawn/villagespawn.tmx")
        self.data.game_map["world_map"] = World(self.data.player, self.data.renderer, "./data/map/gameworld.tmx")
        self.data.game_map["ship"] = Ship(self.data.player, self.data.renderer, "./data/map/beach.tmx")
        self.data.game_map["special_map"] = SpecialMap(self.data.player, self.data.renderer,
                                                       "./data/map/Special/Special_mk2.tmx")

        self.data.current_map = self.data.game_map.get("spawn_village")

        self.data.door = pyasge.Sprite()
        self.data.door.loadTexture("data/sprites/door.png")
        self.data.door.width = 64
        self.data.door.height = 64
        self.data.door.z_order = 10
        self.data.door.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.data.door.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 64

        self.font_m5x7 = pyasge.Font()

        # setup the background and load the fonts for the game
        self.init_audio()
        self.init_cursor()
        self.init_fonts()

        # setup transition overlay
        self.transition_overlay = pyasge.Sprite()
        self.transition_overlay.loadTexture("data/textures/UI Textures/transition overlay.png")
        self.transition_overlay.scale = 2
        self.transition_overlay.alpha = 0
        self.transition_overlay.z_order = 100
        self.fade_in = False
        self.fade_out = False

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.key_handler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_handler)
        self.mousemove_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.move_handler)

        self.menu = GameMenu(self.data)
        self.game_play = GamePlay(self.data)

        # start the game in the menu
        self.current_state = self.menu
        self.new_state = None

    def init_cursor(self):
        """Initialises the mouse cursor and hides the OS cursor."""
        self.data.cursor = pyasge.Sprite()
        self.data.cursor.loadTexture("/data/textures/cursors.png")
        self.data.cursor.width = 11
        self.data.cursor.height = 11
        self.data.cursor.src_rect = [0, 0, 11, 11]
        self.data.cursor.scale = 4
        self.data.cursor.setMagFilter(pyasge.MagFilter.NEAREST)
        self.data.cursor.z_order = 100
        self.data.inputs.setCursorMode(pyasge.CursorMode.HIDDEN)

    def init_audio(self) -> None:
        """Set up all background music that could be played during the game
        and put them into sound groups, so they can be stopped/started whenever necessary"""
        self.data.audio_system.init()

        self.data.bg_sound["default"] = self.data.audio_system.create_sound("./data/audio/default_bg.mp3",
                                                                            mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["default"] = self.data.audio_system.create_sound_group("default")
        self.data.bg_sound.get("default").sound_group = self.data.bg_sound_groups.get("default")

        self.data.bg_sound["death"] = self.data.audio_system.create_sound("./data/audio/death.mp3",
                                                                          mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["death"] = self.data.audio_system.create_sound_group("death")
        self.data.bg_sound.get("death").sound_group = self.data.bg_sound_groups.get("death")

        self.data.bg_sound["special"] = self.data.audio_system.create_sound("./data/audio/special_music.mp3",
                                                                            mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["special"] = self.data.audio_system.create_sound_group("special")
        self.data.bg_sound.get("special").sound_group = self.data.bg_sound_groups.get("special")

        self.data.bg_sound["win_music"] = self.data.audio_system.create_sound("./data/audio/win_bg.mp3",
                                                                              mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["win_music"] = self.data.audio_system.create_sound_group("win_music")
        self.data.bg_sound.get("win_music").sound_group = self.data.bg_sound_groups.get("win_music")

        self.data.bg_sound["ship_music"] = self.data.audio_system.create_sound("./data/audio/ship_bg.mp3",
                                                                               mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["ship_music"] = self.data.audio_system.create_sound_group("ship_music")
        self.data.bg_sound.get("ship_music").sound_group = self.data.bg_sound_groups.get("ship_music")

        self.data.bg_sound["village_music"] = self.data.audio_system.create_sound("./data/audio/colosseum_bg.mp3",
                                                                                  mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["village_music"] = self.data.audio_system.create_sound_group("village_music")
        self.data.bg_sound.get("village_music").sound_group = self.data.bg_sound_groups.get("village_music")

        self.data.bg_sound["graveyard_music"] = self.data.audio_system.create_sound("./data/audio/graveyard_music.mp3",
                                                                                    mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["graveyard_music"] = self.data.audio_system.create_sound_group("graveyard_music")
        self.data.bg_sound.get("graveyard_music").sound_group = self.data.bg_sound_groups.get("graveyard_music")

        self.data.bg_sound["world_music"] = self.data.audio_system.create_sound("./data/audio/world_map_bg.mp3",
                                                                                mode=MODE.LOOP_NORMAL)
        self.data.bg_sound_groups["world_music"] = self.data.audio_system.create_sound_group("world_music")
        self.data.bg_sound.get("world_music").sound_group = self.data.bg_sound_groups.get("world_music")

        # Kill it to avoid default being played twice
        # self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("default"))
        # self.data.bg_audio_channel.volume = self.data.volume

    def init_fonts(self) -> None:
        """Loads the game fonts."""
        self.font_m5x7 = self.data.renderer.loadFont("data/fonts/m5x7.ttf", 48)
        self.data.fonts.update({"m5x7": self.font_m5x7})
        pass

    def reset_game(self) -> None:
        self.data.player.reset()
        # Create all the locations within the world
        self.data.game_map["colosseum"] = Colosseum(self.data.player, self.data.renderer, "./data/map/colosseum.tmx")
        self.data.game_map["graveyard"] = Graveyard(self.data.player, self.data.renderer,
                                                    "./data/map/graveyard2.tmx")
        self.data.game_map["spawn_village"] = Village(self.data.player, self.data.renderer,
                                                      "./data/map/Spawn/villagespawn.tmx")
        self.data.game_map["world_map"] = World(self.data.player, self.data.renderer, "./data/map/gameworld.tmx")
        self.data.game_map["ship"] = Ship(self.data.player, self.data.renderer, "./data/map/beach.tmx")
        self.data.game_map["special_map"] = SpecialMap(self.data.player, self.data.renderer,
                                                       "./data/map/Special/Special_mk2.tmx")
        self.data.current_map = self.data.game_map["spawn_village"].reset()
        self.data.current_map = self.data.game_map.get("spawn_village")
        self.data.special = False
        self.data.special_exit = False

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        """Handles the mouse movement and delegates to the active state."""
        self.data.cursor.x = event.x
        self.data.cursor.y = event.y
        self.current_state.move_handler(event)

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        """Forwards click events on to the active state."""
        self.current_state.click_handler(event)

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        """Forwards Key events on to the active state."""
        self.current_state.key_handler(event)
        if event.key == pyasge.KEYS.KEY_ESCAPE:
            self.signalExit()

        if event.key == pyasge.KEYS.KEY_SPACE and event.action == pyasge.KEYS.KEY_PRESSED:
            self.data.bg_sound_groups.get("default").stop()

        if event.action == pyasge.KEYS.KEY_PRESSED and event.key == pyasge.KEYS.KEY_V:
            self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("death"))
            self.data.bg_audio_channel.volume = self.data.volume

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        """Processes fixed updates."""
        self.current_state.fixed_update(game_time)

        if self.data.gamepad.connected and self.data.gamepad.START:
            self.signalExit()

    def update(self, game_time: pyasge.GameTime) -> None:
        self.data.prev_gamepad = self.data.gamepad
        self.data.gamepad = self.inputs.getGamePad()

        if self.data.gamepad.connected:
            self.current_state.controller_handler(game_time)

        self.check_new_state(game_time)

        if self.fade_out:
            self.do_fade_out(game_time.fixed_timestep)
        if self.fade_in:
            self.do_fade_in(game_time.fixed_timestep)

        self.data.audio_system.update()

    def render(self, game_time: pyasge.GameTime) -> None:
        """Renders the game state and mouse cursor"""
        self.current_state.render(game_time)

        self.renderer.render(self.data.cursor)

        self.data.renderer.shader = None
        if self.current_state.id != GameStateID.GAME_PLAY:
            vp = self.data.renderer.resolution_info.viewport
            self.data.renderer.setProjectionMatrix(0, 0, vp.w, vp.h)
        self.renderer.render(self.transition_overlay)

    def check_new_state(self, game_time: pyasge.GameTime):
        self.new_state = self.current_state.update(game_time)
        if self.new_state == self.current_state.id:
            pass
        else:
            self.fade_out = True

    def do_fade_out(self, fixed_timestep):
        self.transition_overlay.alpha += 3 * fixed_timestep
        if self.transition_overlay.alpha >= 2:
            self.transition_overlay.alpha = 1
            self.fade_in = True
            self.fade_out = False
            self.change_state()

    def do_fade_in(self, fixed_timestep):
        self.transition_overlay.alpha -= 3 * fixed_timestep
        if self.transition_overlay.alpha <= 0:
            self.transition_overlay.alpha = 0
            self.fade_in = False

    def change_state(self):
        if self.new_state == GameStateID.GAME_MENU:
            self.reset_game()
            self.menu.reset()
            self.current_state = self.menu
            self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("default"))
            self.data.bg_audio_channel.volume = self.data.volume * 2
        elif self.new_state == GameStateID.GAME_PLAY:
            self.game_play.reset()
            self.current_state = self.game_play
        elif self.new_state == GameStateID.GAME_WIN:
            self.current_state = GameWin(self.data)
            self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("win_music"))
            self.data.bg_audio_channel.volume = self.data.volume * 2
        elif self.new_state == GameStateID.GAME_OVER:
            self.current_state = GameOver(self.data)
            self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("death"))
            self.data.bg_audio_channel.volume = self.data.volume * 2
