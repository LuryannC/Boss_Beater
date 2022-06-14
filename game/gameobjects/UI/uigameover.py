import pyasge


class GameOverUI:
    def __init__(self, is_game_won: bool):
        self.is_game_won = is_game_won

        self.background_size = int

        self.background = pyasge.Sprite()
        self.init_background()

        self.midground = pyasge.Sprite()
        self.init_midground()

        self.foreground = pyasge.Sprite()
        self.init_foreground()

        self.game_over_text = pyasge.Sprite()
        self.init_game_over_text()

        self.scoreboard_base = pyasge.Sprite()
        self.init_scoreboard_base()

        self.scoreboard_damage_taken = None
        self.scoreboard_damage_dealt = None
        self.scoreboard_enemies_defeated = None

        self.press_enter_text = None

    def init_scoreboard_base(self):
        self.scoreboard_base.loadTexture("data/textures/UI Textures/Scoreboard.png")
        self.scoreboard_base.z_order = 4
        self.scoreboard_base.x = (1920 - self.scoreboard_base.width)/2
        self.scoreboard_base.y = (1080 - self.scoreboard_base.height)/2 + 150

    def init_background(self):
        if self.is_game_won:
            self.background.loadTexture("data/textures/UI Textures/Adventurer_AssetPack_Background.png")
            self.background_size = 3840
        else:
            self.background.loadTexture("data/textures/UI Textures/Mushroom_Cave_Background.png")
            self.background_size = 5120

        self.background.z_order = 1
        self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.background.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 1920
        self.background.width = 1920

    def init_midground(self):
        if self.is_game_won:
            self.midground.loadTexture("data/textures/UI Textures/Adventurer_AssetPack_Midground.png")
        else:
            self.midground.loadTexture("data/textures/UI Textures/Mushroom_Cave_Midground.png")

        self.midground.z_order = 2
        self.midground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.midground.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 1920
        self.midground.width = 1920

    def init_foreground(self):
        if self.is_game_won:
            self.foreground.loadTexture("data/textures/UI Textures/Adventurer_AssetPack_Foreground.png")
        else:
            self.foreground.loadTexture("data/textures/UI Textures/Mushroom_Cave_Foreground.png")

        self.foreground.z_order = 3
        self.foreground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.foreground.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 1920
        self.foreground.width = 1920

    def init_game_over_text(self):
        if self.is_game_won:
            self.game_over_text.loadTexture("data/textures/UI Textures/Game Win.png")
        else:
            self.game_over_text.loadTexture("data/textures/UI Textures/Game Loose.png")

        self.game_over_text.z_order = 4
        self.game_over_text.y = 150

    def init_text(self, font: pyasge.Font):
        """ Loads font for GameOverUI texts """
        self.scoreboard_damage_taken = pyasge.Text(font)
        self.scoreboard_damage_dealt = pyasge.Text(font)
        self.scoreboard_enemies_defeated = pyasge.Text(font)

        self.press_enter_text = pyasge.Text(font)
        self.init_press_enter_text()

    def init_scoreboard_damage_taken(self, damage_taken):
        """ Initialize the number for DAMAGE TAKEN in final scoreboard """
        self.scoreboard_damage_taken.string = str(damage_taken)
        self.scoreboard_damage_taken.scale = 3
        self.scoreboard_damage_taken.z_order = 5
        self.scoreboard_damage_taken.x = 723 - self.scoreboard_damage_taken.width/2
        self.scoreboard_damage_taken.y = 770

    def init_scoreboard_damage_dealt(self, damage_dealt):
        """ Initialize the number for DAMAGE DEALT in final scoreboard """
        self.scoreboard_damage_dealt.string = str(damage_dealt)
        self.scoreboard_damage_dealt.scale = 3
        self.scoreboard_damage_dealt.z_order = 5
        self.scoreboard_damage_dealt.x = 963 - self.scoreboard_damage_dealt.width / 2
        self.scoreboard_damage_dealt.y = 770

    def init_scoreboard_enemies_defeated(self, enemies_defeated):
        """ Initialize the number for ENEMIES DEFEATED in final scoreboard """
        self.scoreboard_enemies_defeated.string = str(enemies_defeated)
        self.scoreboard_enemies_defeated.scale = 3
        self.scoreboard_enemies_defeated.z_order = 5
        self.scoreboard_enemies_defeated.x = 1203 - self.scoreboard_enemies_defeated.width/2
        self.scoreboard_enemies_defeated.y = 770

    def init_press_enter_text(self):
        self.press_enter_text.string = "Press ENTER to go back to main menu"
        self.press_enter_text.scale = 2
        self.press_enter_text.z_order = 4
        self.press_enter_text.x = (1920 - self.press_enter_text.width)/2
        self.press_enter_text.y = 950

    def play_animation(self, dt: pyasge.GameTime.fixed_timestep):
        """ Plays background animation for GameOver """
        self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] += dt * 75
        if self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] >= self.background_size - 1920:
            self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0

        self.midground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] += dt * 50
        if self.midground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] >= self.background_size - 1920:
            self.midground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0

        self.foreground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] += dt * 25
        if self.foreground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] >= self.background_size - 1920:
            self.foreground.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0

    def render(self, renderer):
        """ Renders GameOverUI elements """
        renderer.render(self.background)
        renderer.render(self.midground)
        renderer.render(self.foreground)
        renderer.render(self.game_over_text)
        renderer.render(self.scoreboard_base)
        renderer.render(self.scoreboard_damage_taken)
        renderer.render(self.scoreboard_damage_dealt)
        renderer.render(self.scoreboard_enemies_defeated)
        renderer.render(self.press_enter_text)
