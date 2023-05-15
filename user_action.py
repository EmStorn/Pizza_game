from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, StringProperty

def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

def on_touch_down(self, touch):

    if touch.x > self.full_width/2:
        # print("left press")
        self.player_x += self.player_movement_speed
    else:
        # print("right press")
        self.player_x -= self.player_movement_speed
    return super(RelativeLayout, self).on_touch_down(touch)

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.player_x -= self.player_movement_speed
        self.player_image = "images/player_standing1.png"
        self.player_image = "images/player_standing2.png"
        self.player_image = "images/player_standing3.png"
        self.player_image = "images/player_standing4.png"
    elif keycode[1] == 'right':
        self.player_x += self.player_movement_speed
        self.player_image = "images/player_standing1.png"
        self.player_image = "images/player_standing4.png"
        self.player_image = "images/player_standing3.png"
        self.player_image = "images/player_standing2.png"
    return True

def on_keyboard_up(self, keyboard, keycode):
    self.player_x += 0
    self.player_image = "images/player_standing1.png"
    return True

def on_touch_up(self, touch):
    # print("up")
    self.player_x += 0
