import pyasge

from game.gamedata import GameData
from game.gamestates.gamestate import GameState
from game.gamestates.gamestate import GameStateID
from game.gameobjects.UI.uigameover import GameOverUI


class GameOver(GameState):

    def __init__(self, data: GameData):
        super().__init__(data)
        self.id = GameStateID.GAME_OVER
        self.ui = GameOverUI(False)
        self.transition = False
        self.data.bg_audio_channel = self.data.audio_system.play_sound(self.data.bg_sound.get("death"))
        self.data.bg_audio_channel.volume = self.data.volume * 2

        self.init()

    def init(self):
        self.ui.init_text(self.data.fonts["m5x7"])

        # Temporary values for scoreboard
        self.ui.init_scoreboard_damage_taken(int(self.data.player.damage_taken))
        self.ui.init_scoreboard_damage_dealt(int(self.data.player.damage_dealt))
        self.ui.init_scoreboard_enemies_defeated(int(self.data.player.enemies_killed))

    def reset(self) -> None:
        pass

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
        self.ui.play_animation(game_time.fixed_timestep)
        self.data.bg_sound_groups.get("graveyard_music").stop()
        self.data.bg_sound_groups.get("village_music").stop()
        self.data.bg_sound_groups.get("ship_music").stop()

        if self.transition:
            return GameStateID.GAME_MENU

        return self.id

    def render(self, game_time: pyasge.GameTime) -> None:
        self.ui.render(self.data.renderer)
