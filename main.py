
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, Clock, ObjectProperty, ReferenceListProperty, ListProperty
from kivy.metrics import dp, sp
from kivy import platform
import random


class MainWidget(RelativeLayout):

    from user_action import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_up, on_touch_down

    player_x = NumericProperty(Window.width / 2)
    player_y = NumericProperty(Window.height / 8)
    player_size = NumericProperty(dp(100))
    player_movement_speed = 15
    player_image = StringProperty("images/player_standing1.png")

    FALLING_SLICES_NUMBER = 7
    FALLING_SLICE_DIMENSION = dp(50)
    falling_slice_speed = 1.5

    increment = Window.width/FALLING_SLICES_NUMBER
    middle_increment = increment/2

    falling_slices_x_values = []
    falling_slices_y_values = []

    block_definitions = ListProperty()

    points_counter = 0
    text_points_counter = StringProperty("Score: 0")

    life_counter = 3
    text_life_counter = StringProperty("Lives: 3")



    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.start_button = ObjectProperty(None)

        self.game_running = False

        self.slices_coordinates_generation()
        with self.canvas:
            for index in range(self.FALLING_SLICES_NUMBER):
                self.block_definitions.append(
                    Rectangle(
                        pos=(self.falling_slices_x_values[index] , self.falling_slices_y_values[index]),
                        size=(self.FALLING_SLICE_DIMENSION, self.FALLING_SLICE_DIMENSION),
                        source="images/pizza_slice_2.png"
                    )
                )

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    # generate the starting coordinates of the slices
    def slices_coordinates_generation(self):
        for index in range(self.FALLING_SLICES_NUMBER):
            self.falling_slices_x_values.append(self.middle_increment + self.increment * index)
            self.falling_slices_y_values.append(Window.height * 0.8  + random.randint(200, 600))

    def is_desktop(self):
        if platform in ("linux", "win", "macosx"):
            return True
        return False

    def on_numeric_property(self, instance, new_numeric_property):
        instance.pos = new_numeric_property

    # handle the falling movement of the slices and checks if the slices reached the bottom, defined by replacement trigger
    # it aslo triggers the function slice?captured when the slice collide with the player
    def slices_movement(self, slice, time_factor):
        replacement_trigger = self.player_y-self.FALLING_SLICE_DIMENSION+5
        player_height = self.player_y + self.player_size
        player_width = self.player_x + self.player_size - self.player_size/2
        if self.falling_slices_y_values[slice] >= replacement_trigger:
            item = self.block_definitions[slice]
            x = self.falling_slices_x_values[slice]
            self.falling_slices_y_values[slice] -= self.falling_slice_speed * time_factor
            y = self.falling_slices_y_values[slice]
            moving = x, y
            self.on_numeric_property(item, moving)
            if replacement_trigger < self.falling_slices_y_values[slice] < player_height and self.player_x - self.player_size/2 < self.falling_slices_x_values[slice] < self.player_x + self.player_size/2:             
                print(self.block_definitions[slice].source)                
                if self.block_definitions[slice].source.endswith("rotten_pizza_slice_2.png"):
                    rotten = 1
                    self.slice_captured(rotten)
                else:
                    rotten = 0
                    self.slice_captured(rotten)
                self.falling_slices_y_values[slice] = Window.height * 0.8  + random.randint(200, 300)
                self.block_definitions[slice].source == "images/pizza_slice_2.png"
                randomizer = random.randint(0,5)
                if randomizer == 0:
                    self.rottenator(self.block_definitions[slice])
        else:
            self.falling_slices_y_values[slice] = Window.height * 0.8  + random.randint(200, 300)
            self.block_definitions[slice].source == "images/pizza_slice_2.png"
            randomizer = random.randint(0,3)
            if randomizer == 0:
                self.rottenator(self.block_definitions[slice])

    # handles the logic of the capture of the slices, by reducing lives, adding points
    def slice_captured(self, rotten_slice):
        if rotten_slice == 0:
            self.points_counter += 1
        else:
            self.points_counter -= 1
            self.life_counter -= 1

        self.text_points_counter = "Score: " + str(self.points_counter)
        self.text_life_counter = "Lives: " + str(self.life_counter)

    # change image of the slice to rotten_slice
    def rottenator(self, slice):
        slice.source="images/rotten_pizza_slice_2.png"

    def update(self, dt):
        if self.game_running:
            #self.lines_test()
            time_factor = dt * 60
            for i in range(0,7):
                self.slices_movement(i, time_factor)
            self.check_game_status()  
            self.falling_slice_speed += 0.0005 #gradually increase speed of falling slices 

    # check if game is running and hide/show buttons and game over
    def check_game_status(self):
        if self.life_counter == 0:
            self.game_running = False
            self.ids.game_over_label.opacity = 1  # Make the label visible
            self.add_widget(self.start_button) # Make start button visble again
        else:
            self.ids.game_over_label.opacity = 0  # Hide the label           

    # start the game by modifying game_running variable
    def start_game(self, instance):
        self.remove_widget(self.start_button)
        self.reset_starting_point()
        self.game_running = True

    # reset to starting values all the variables used to make the game moving    
    def reset_starting_point(self):
        self.player_x = Window.width / 2
        self.player_y = Window.height / 8
        self.player_movement_speed = 15
        
        self.falling_slice_speed = 1.5

        self.falling_slices_x_values = []
        self.falling_slices_y_values = []

        self.slices_coordinates_generation()

        self.points_counter = 0
        self.text_points_counter = "Score: 0"

        self.life_counter = 3
        self.text_life_counter = "Lives: 3"


class Pizza(App):
    pass


Pizza().run()
