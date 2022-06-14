import pyasge

from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gameobjects.UI.uigamemenu import GameMenuUI


class GameMenu(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.GAME_MENU
        self.ui = GameMenuUI()
        self.transition = False
        self.init()
        data.bg_audio_channel = data.audio_system.play_sound(data.bg_sound.get("default"))
        data.bg_audio_channel.volume = data.volume * 2

    def init(self):
        self.ui.init_title_text(self.data.fonts["m5x7"])

    def reset(self):
        self.transition = False

    def click_handler(self, event: pyasge.ClickEvent) -> None:
        pass

    def key_handler(self, event: pyasge.KeyEvent) -> None:
        if event.action == pyasge.KEYS.KEY_PRESSED:
            if event.key == pyasge.KEYS.KEY_ENTER:
                self.transition = True

    def move_handler(self, event: pyasge.MoveEvent) -> None:
        pass

    def controller_handler(self, game_time: pyasge.GameTime) -> None:
        if self.data.gamepad.RIGHT_BUMPER and not self.data.prev_gamepad.RIGHT_BUMPER:
            self.transition = True

    def fixed_update(self, game_time: pyasge.GameTime) -> None:
        pass

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        self.data.bg_sound_groups.get("win_music").stop()
        self.data.bg_sound_groups.get("death").stop()
        self.ui.play_animation(game_time.fixed_timestep)
        self.data.bg_sound_groups.get("win_music").stop()
        self.data.bg_sound_groups.get("death").stop()

        if self.transition:
            return GameStateID.GAME_PLAY

        return self.id

    def render(self, game_time: pyasge.GameTime) -> None:
        self.ui.render(self.data.renderer)
        pass
