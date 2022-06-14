import pyasge
import pyfmodex
from game.gameobjects.gamemap import GameMap
from game.gameobjects.Location.location import Location


class GameData:
    """
    GameData stores the data that needs to be shared

    When using multiple states in a game, you will find that
    some game data needs to be shared. GameData can be used to
    share access to data that the game and any running states may
    need.
    """

    def __init__(self) -> None:
        self.cursor = None
        self.fonts = {}
        self.game_map: dict[str, Location] = {}
        self.current_map = None
        self.game_res = [1920, 1080]
        self.inputs = None
        self.gamepad = None
        self.prev_gamepad = None
        self.renderer = None
        self.shaders: dict[str, pyasge.Shader] = {}
        self.player = None
        self.audio_system = pyfmodex.System()
        self.sound_group = self.audio_system.create_sound_group("test")
        self.bg_audio = None
        self.bg_audio_channel = None
        self.arrows = []
        self.bg_sound: dict[str, pyfmodex.sound] = {}
        self.bg_sound_groups: dict[str, pyfmodex.sound_group] = {}
        self.volume = 0.3
        self.special = False
        self.special_exit = False

        self.door = None
