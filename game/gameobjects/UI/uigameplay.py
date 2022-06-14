import pyasge
from game.gamedata import GameData


class GameplayUI:

    def __init__(self, game_data, z_order):
        self.data = game_data
        self.min_z_order = z_order

        self.data = GameData()

        self.base = pyasge.Sprite()
        self.init_base()

        self.health_empty = pyasge.Sprite()
        self.init_health_empty()

        self.health_full = pyasge.Sprite()
        self.init_health_full()

        self.stamina = pyasge.Sprite()
        self.init_stamina()

        self.stamina_counter = None

        self.button_move = pyasge.Sprite()
        self.init_button_move()

        self.button_melee = pyasge.Sprite()
        self.init_button_melee()
        
        self.button_ranged = pyasge.Sprite()
        self.init_button_ranged()
        
        self.button_end = pyasge.Sprite()
        self.init_button_end()

        self.action_order = pyasge.Sprite()
        self.init_action_order()

        self.action_order_text = [None] * 5

        self.action_order_icon = [None] * 5
        self.init_action_order_icon()

        # self.damage_text = None
        # self.init_damage_visu(game_data, self.data.player.current_health)

    def init_base(self):
        self.base.loadTexture("data/textures/UI Textures/Base.png")
        self.base.z_order = self.min_z_order + 2
        self.base.scale = 0.75
        self.base.x = self.data.game_res[0] / 2 - self.base.width / 3
        self.base.y = self.data.game_res[1] - self.base.height / 4 - self.base.height / 2

    def init_health_empty(self):
        self.health_empty.loadTexture("data/textures/UI Textures/Health Empty.png")
        self.health_empty.z_order = self.min_z_order
        self.health_empty.scale = 0.75
        self.health_empty.x = self.base.x + 53
        # self.health_empty.x = 565
        self.health_empty.y = self.base.y + 37

    def init_health_full(self):
        self.health_full.loadTexture("data/textures/UI Textures/Health Full.png")
        self.health_full.z_order = self.min_z_order + 1
        self.health_full.scale = 0.75
        self.health_full.x = self.base.x + 53

    def init_stamina(self):
        self.stamina.loadTexture("data/textures/UI Textures/Spritesheet Stamina 240x150.png")
        self.stamina.z_order = self.min_z_order + 3
        self.stamina.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
        self.stamina.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 240
        self.stamina.scale = 0.75
        self.stamina.width = 240
        self.stamina.x = self.base.x + 24
        self.stamina.y = self.base.y + 7

    def init_stamina_counter(self, font: pyasge.Font):
        self.stamina_counter = pyasge.Text(font)
        self.stamina_counter.z_order = self.min_z_order + 3
        self.stamina_counter.scale = 1
        self.stamina_counter.x = self.base.x + 20
        self.stamina_counter.y = self.base.y + 150

    def init_button_move(self):
        self.button_move.loadTexture("data/textures/UI Textures/Button_Move.png")
        self.button_move.z_order = self.min_z_order + 4
        self.button_move.scale = 0.75
        self.button_move.x = self.base.x + self.base.width / 4 - 10
        self.button_move.y = self.base.y + 80

    def init_button_melee(self):
        self.button_melee.loadTexture("data/textures/UI Textures/Button_Melee.png")
        self.button_melee.z_order = self.min_z_order + 4
        self.button_melee.scale = 0.75
        self.button_melee.x = self.base.x + self.base.width / 2 - 10
        self.button_melee.y = self.base.y + 80

    def init_button_ranged(self):
        self.button_ranged.loadTexture("data/textures/UI Textures/Button_Ranged.png")
        self.button_ranged.z_order = self.min_z_order + 4
        self.button_ranged.scale = 0.75
        self.button_ranged.x = self.base.x + self.base.width / 4 - 10
        self.button_ranged.y = self.base.y + 145

    def init_button_end(self):
        self.button_end.loadTexture("data/textures/UI Textures/Button_EndTurn.png")
        self.button_end.z_order = self.min_z_order + 4
        self.button_end.scale = 0.75
        self.button_end.x = self.base.x + self.base.width / 2 - 10
        self.button_end.y = self.base.y + 145

    def init_action_order(self):
        self.action_order.loadTexture("data/sprites/Action Bar.png")
        self.action_order.z_order = self.min_z_order
        self.action_order.scale = 1
        self.action_order.x = self.data.game_res[0] - self.action_order.width
        self.action_order.y = 150

    def init_action_order_list(self, font: pyasge.Font):
        for index in range(5):
            self.action_order_text[index] = pyasge.Text(font)
            self.action_order_text[index].z_order = self.min_z_order + 1
            self.action_order_text[index].scale = 1
            self.action_order_text[index].x = self.action_order.x + 110
            self.action_order_text[index].y = self.action_order.y + 65 + (index * 75)
            self.action_order_text[index].colour = pyasge.COLOURS.BLACK

    def init_action_order_icon(self):
        for index in range(5):
            self.action_order_icon[index] = pyasge.Sprite()
            self.action_order_icon[index].loadTexture("data/sprites/Entity Icons.png")
            self.action_order_icon[index].width = 100
            self.action_order_icon[index].scale = 0.75
            self.action_order_icon[index].z_order = self.min_z_order + 1
            self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
            self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 100
            self.action_order_icon[index].x = self.action_order.x + 12

        self.action_order_icon[0].scale = 0.9
        self.action_order_icon[0].x = self.action_order.x + 5

        self.action_order_icon[0].y = self.action_order.y
        self.action_order_icon[1].y = self.action_order.y + 95
        self.action_order_icon[2].y = self.action_order.y + 170
        self.action_order_icon[3].y = self.action_order.y + 245
        self.action_order_icon[4].y = self.action_order.y + 320

        # def init_damage_visu(self, data, damage: int):
    #     self.damage_text = pyasge.Text(self.data.renderer.getDefaultFont(), str(damage), 10, 50)

    def update_health(self, current_hp: int, max_hp: int):
        """ Updates the HP display in gameplay UI """
        self.health_full.y = self.base.y - (180 * current_hp / max_hp) + 180 + 30

    def render(self, renderer: pyasge.Renderer):
        renderer.render(self.base)
        renderer.render(self.health_empty)
        renderer.render(self.health_full)
        renderer.render(self.stamina)
        renderer.render(self.stamina_counter)
        renderer.render(self.button_move)
        renderer.render(self.button_melee)
        renderer.render(self.button_ranged)
        renderer.render(self.button_end)
        renderer.render(self.action_order)

        for index in range(5):
            renderer.render(self.action_order_icon[index])
            renderer.render(self.action_order_text[index])

    def update_stamina(self, current_stamina: int):
        """ Updates the Stamina bar in gameplay UI """
        self.stamina.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = current_stamina * 240
        self.stamina_counter.string = str(current_stamina)

    def update_action_order(self, current_action_order: list):
        for index in range(5):
            current_entity = str(current_action_order[index])
            if current_entity == "Player":
                self.action_order_text[index].string = "Player"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 0
            elif current_entity == "AssassinsEnemy":
                self.action_order_text[index].string = "Assassin"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 100
            elif current_entity == "GhostEnemies":
                self.action_order_text[index].string = "Ghost"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 200
            elif current_entity == "ThiefEnemy":
                self.action_order_text[index].string = "Thief"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 300
            elif current_entity == "MinotaurBoss":
                self.action_order_text[index].string = "Minotaur"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 400
            elif current_entity == "PirateBoss":
                self.action_order_text[index].string = "Pirate"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 500
            elif current_entity == "SkeletonBoss":
                self.action_order_text[index].string = "Leshen"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 600
            elif current_entity == "DEAD":
                self.action_order_text[index].string = "Dead"
                self.action_order_icon[index].src_rect[pyasge.Sprite.SourceRectIndex.START_X] = 700

