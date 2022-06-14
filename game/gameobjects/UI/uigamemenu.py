import pyasge


class GameMenuUI:
    def __init__(self):
        self.background = pyasge.Sprite()
        self.init_background()

        self.cloud = pyasge.Sprite()
        self.init_cloud()

        self.foreground = pyasge.Sprite()
        self.init_foreground()

        self.title = pyasge.Sprite()
        self.init_title()

        self.title_text = None

    def init_background(self):
        self.background.loadTexture("data/textures/UI Textures/Background.png")
        self.background.z_order = 1
        self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.background.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 1920
        self.background.width = 1920

    def init_cloud(self):
        self.cloud.loadTexture("data/textures/UI Textures/Cloud.png")
        self.cloud.z_order = 2
        self.cloud.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.cloud.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 1920
        self.cloud.width = 1920

    def init_foreground(self):
        self.foreground.loadTexture("data/textures/UI Textures/Foreground.png")
        self.foreground.z_order = 3

    def init_title(self):
        self.title.loadTexture("data/textures/UI Textures/Logo.png")
        self.title.z_order = 4
        self.title.x = 960 - self.title.width / 2
        self.title.y = 200

    def init_title_text(self, font: pyasge.Font):
        """ Loads font for tittle text """
        self.title_text = pyasge.Text(font)
        self.title_text.string = "Press ENTER to start"
        self.title_text.scale = 2
        self.title_text.z_order = 4
        self.title_text.x = 960 - self.title_text.width / 2
        self.title_text.y = 800

    def play_animation(self, dt: pyasge.GameTime.fixed_timestep):
        """ Plays background animation for GameMenu """
        self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] += dt * 100
        if self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] >= 1920:
            self.background.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0

        self.cloud.src_rect[pyasge.Sprite.SourceRectIndex.START_X] += dt * 75
        if self.cloud.src_rect[pyasge.Sprite.SourceRectIndex.START_X] >= 1920:
            self.cloud.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0

    def render(self, renderer):
        """ Renders GameMenuUI elements """
        renderer.render(self.background)
        renderer.render(self.cloud)
        renderer.render(self.foreground)
        renderer.render(self.title)
        renderer.render(self.title_text)
