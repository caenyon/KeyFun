# -*- coding: utf-8 -*-
"""
GUI contains a graphical user interface that can display keyboard layouts
"""
from Tkinter import *
import logging
import threading

import Constants


grid_size = 40
bound_size = 3
text_size = 8
key_color = "#555555"
line_color = "#333333"
text_color = "#eeeeee"
background_color = "#c9c9c9"
physical_highlight_color = "#164f7b"
virtual_highlight_color = '#b01818'
both_highlight_color = '#137e1d'
font = ('Calibri', text_size)


class KeyboardLayout(object):
    """
    Contains an abstract description of a keyboard layout.
    """

    def __init__(self):
        self.keys = {}

    def draw(self, canvas):
        """
        Draws every key in self.keys onto the Tkinter canvas canvas.

        :param canvas: Canvas to draw on.
        """
        for key in self.keys:
            self.keys[key].draw(canvas)

    def get_key(self, vkey_id):
        """
        Returns the Key object with the id vkey_id

        :param vkey_id: the virtual key code
        :type vkey_id: int
        :return: Key object
        :rtype: Key
        """
        vkey = Constants.id_to_vkey(vkey_id)
        if vkey not in self.keys:
            logging.warning("Key {} not in KeyboardLayout.".format(vkey))
        else:
            return self.keys[vkey]


class Key(object):
    """
    Holds information of a key which is part of a KeyboardLayout.

    :param x: the x value of the key
    :type x: float
    :param y: the y value of the key
    :type y: float
    :param vkey: virtual key name
    :type vkey: str
    """

    def __init__(self, x, y, vkey):
        self.vkey = vkey
        self.x = x
        self.y = y
        self.shape = None
        self.text = None
        self.physical_highlight = False
        self.virtual_highlight = False

    def draw(self, c):
        """
        Draws itself onto the canvas c

        :param c: Tkinter canvas
        """
        pass


class RectKey(Key):
    """
    Holds information of a rectangular key which is part of a KeyboardLayout.

    :param x: the x value of the key
    :type x: float
    :param y: the y value of the key
    :type y: float
    :param vkey: virtual key name
    :type vkey: str
    :param length: the length of the key
    :type length: float
    :param height: the height of the key
    :type height: float
    """

    def __init__(self, x, y, vkey, length=1, height=1):
        Key.__init__(self, x, y, vkey)
        self.length = length
        self.height = height

    def draw(self, c):
        """
        Draws itself onto the canvas c

        :param c: Tkinter canvas
        """
        x1 = self.x * grid_size + bound_size
        y1 = self.y * grid_size + bound_size
        x2 = (self.x + self.length) * grid_size - bound_size
        y2 = (self.y + self.height) * grid_size - bound_size

        self.shape = c.create_rectangle(x1, y1, x2, y2, outline=line_color, fill=key_color)
        self.text = c.create_text((x1 + x2) / 2, (y1 + y2) / 2, font=font, text=Constants.id_to_symbol(self.vkey),
                                  fill=text_color)


class BigEnterKey(Key):
    """
    Holds information of a special big return key which is part of a KeyboardLayout.

    :param x: the x value of the key
    :type x: float
    :param y: the y value of the key
    :type y: float
    :param vkey: virtual key name
    :type vkey: str
    """

    def __init__(self, x, y, vkey):
        Key.__init__(self, x, y, vkey)

    def draw(self, c):
        """
            Draws itself onto the canvas c

            :param c: Tkinter canvas
        """
        # An enter key needs three different values for x and y.
        x_left = self.x * grid_size + bound_size
        x_middle = (self.x + .25) * grid_size + bound_size
        x_right = (self.x + 1.5) * grid_size - bound_size

        y_top = self.y * grid_size + bound_size
        y_middle = (self.y + 1) * grid_size - bound_size
        y_bottom = (self.y + 2) * grid_size - bound_size

        self.shape = c.create_polygon(x_left, y_top, x_right, y_top, x_right, y_bottom, x_middle, y_bottom, x_middle,
                                      y_middle, x_left, y_middle, fill=key_color, outline=line_color)
        self.text = c.create_text((x_right + x_middle) / 2, (y_top + y_bottom) / 2, font=font,
                                  text=Constants.id_to_symbol(self.vkey), fill=text_color)


class ISO105Layout(KeyboardLayout):
    """
    Represents a german keyboard layout with 105 keys
    """

    def __init__(self):
        KeyboardLayout.__init__(self)

        self.grid_length = 15
        self.grid_height = 5

        self.generate_keys()

    def generate_keys(self):
        """
        Generates the keys of the keyboard.
        """
        keys = []

        # Generate Number-Row
        strings = ['OEM_5'] + [str(i) for i in range(1, 10)] + ['0', 'OEM_4', 'OEM_6']
        for i in range(len(strings)):
            keys.append(RectKey(i, 0, 'VK_' + strings[i]))

        # Generate first letter row
        strings = ['Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'OEM_1', 'OEM_PLUS']
        for i in range(len(strings)):
            keys.append(RectKey(i + 1.5, 1, 'VK_' + strings[i]))

        # Generate second letter row
        strings = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'OEM_3', 'OEM_7', 'OEM_2']
        for i in range(len(strings)):
            keys.append(RectKey(i + 1.75, 2, 'VK_' + strings[i]))

        # Generate third letter row
        strings = ['OEM_102', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', 'OEM_COMMA', 'OEM_PERIOD', 'OEM_MINUS']
        for i in range(len(strings)):
            keys.append(RectKey(i + 1.25, 3, 'VK_' + strings[i]))

        # Generate bigger keys
        keys.append(RectKey(13, 0, 'VK_BACK', 2))
        keys.append(RectKey(0, 1, 'VK_TAB', 1.5))
        keys.append(RectKey(0, 2, 'VK_CAPITAL', 1.75))
        keys.append(RectKey(0, 3, 'VK_LSHIFT', 1.25))
        keys.append(RectKey(12.25, 3, 'VK_RSHIFT', 2.75))
        keys.append(RectKey(3.75, 4, 'VK_SPACE', 6.25))
        keys.append(BigEnterKey(13.5, 1, 'VK_RETURN'))

        # Generate left bottom keys
        strings = ['LCONTROL', 'LWIN', 'LMENU']
        for i in range(len(strings)):
            keys.append(RectKey(i * 1.25, 4, 'VK_' + strings[i], 1.25))

        # Generate right bottom keys
        strings = ['RMENU', 'RWIN', 'APPS', 'RCONTROL']
        for i in range(len(strings)):
            keys.append(RectKey(i * 1.25 + 10, 4, 'VK_' + strings[i], 1.25))

        for key in keys:
            self.keys[key.vkey] = key


class TiproLayout(KeyboardLayout):
    """
    Represents a custom tipro layout with 128 keys
    """

    def __init__(self):
        KeyboardLayout.__init__(self)

        self.grid_length = 16
        self.grid_height = 8

        self.generate_keys()

    def generate_keys(self):
        """
        Generates the keys of the keyboard.
        """
        keys = []

        s1 = ['F13', 'F14', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'SNAPSHOT',
              'SCROLL']
        s2 = ['F15', 'F16', 'NUMPAD1', 'NUMPAD2', 'NUMPAD3', 'NUMPAD4', 'NUMPAD5', 'BROWSER_BACK', 'BROWSER_FORWARD',
              'NUMPAD6', 'NUMPAD7', 'NUMPAD8', 'NUMPAD9', 'NUMPAD0', 'PAUSE', 'NUMLOCK']
        s3 = ['DECIMAL', 'VOLUME_MUTE', 'VOLUME_DOWN', 'VOLUME_UP', 'MEDIA_PLAY_PAUSE', 'MEDIA_STOP',
              'MEDIA_PREV_TRACK', 'MEDIA_NEXT_TRACK']
        s4 = ['ESCAPE', 'OEM_5', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'OEM_4', 'OEM_6']
        s5 = ['TAB', 'ADD', 'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'OEM_1', 'OEM_PLUS']
        s6 = ['CAPITAL', 'SUBTRACT', 'A', 'S', 'D', 'F', 'G', 'HOME', 'END', 'H', 'J', 'K', 'L', 'OEM_3', 'OEM_7',
              'OEM_2']
        s7 = ['LSHIFT', 'OEM_102', 'Y', 'X', 'C', 'V', 'B', 'INSERT', 'PRIOR', 'N', 'M', 'OEM_COMMA', 'OEM_PERIOD',
              'OEM_MINUS', 'DIVIDE', 'RSHIFT']
        s8 = ['LCONTROL', 'LWIN', 'LMENU', 'LEFT', 'DOWN', 'UP', 'RIGHT', 'DELETE', 'NEXT', 'SPACE', 'MULTIPLY',
              'NRETURN', 'RMENU', 'RWIN', 'APPS', 'RCONTROL']
        for i in range(len(s1)):
            keys.append(RectKey(i, 0, 'VK_' + s1[i]))
            keys.append(RectKey(i, 1, 'VK_' + s2[i]))
            if i % 2 == 0:
                keys.append(RectKey(i, 2, 'VK_' + s3[int(i / 2)], 2))
            offset = 0 if i <= 6 else 2
            if i < len(s1) - 2:
                keys.append(RectKey(i + offset, 3, 'VK_' + s4[i]))
                keys.append(RectKey(i + offset, 4, 'VK_' + s5[i]))
            keys.append(RectKey(i, 5, 'VK_' + s6[i]))
            keys.append(RectKey(i, 6, 'VK_' + s7[i]))
            keys.append(RectKey(i, 7, 'VK_' + s8[i]))

        keys.append(RectKey(7, 3, 'VK_RETURN', height=2))
        keys.append(RectKey(8, 3, 'VK_BACK', height=2))

        for key in keys:
            self.keys[key.vkey] = key


class KeyboardGUI(object):
    """
    Represents a Tkinter graphical user interface that shows a keyboard layout.

    :param highlight_keys: a queue containing
    :type highlight_keys:
    :param reset_highlight_keys:
    :type reset_highlight_keys:
    :param pause_flag:
    :type pause_flag:
    """

    def __init__(self, highlight_keys, reset_highlight_keys, simulated_keys, pause_flag):
        self.root = Tk()
        self.root.wm_attributes('-alpha', .0)
        self.keyboard_layout = TiproLayout()  # ISO105Layout()

        grid_length = self.keyboard_layout.grid_length
        grid_height = self.keyboard_layout.grid_height

        self.w = Canvas(self.root, width=grid_size * grid_length + 1, height=grid_size * grid_height + 1,
                        background=background_color, highlightthickness=0)

        self.root.bind("<FocusIn>", self.focus_in)
        self.root.bind("<FocusOut>", self.focus_out)

        self.w.pack()
        self.root.wm_attributes('-topmost', True)
        self.root.wm_attributes('-toolwindow', True)
        self.root.protocol("WM_DELETE_WINDOW", self.handle_close)

        self.root.minsize(grid_size * grid_length + 1, grid_size * grid_height + 1)

        self.keyboard_layout.draw(self.w)

        self.highlight_keys = highlight_keys
        self.reset_highlight_keys = reset_highlight_keys
        self.simulated_keys = simulated_keys

        self.exit_flag = threading.Event()
        self.pause_flag = pause_flag

        w_workspace, h_workspace = self.get_workspace_size()
        border_left, border_top, w, h = self.calc_frame()

        x = int((w_workspace - w - 2 * border_left) / 2)
        y = int(h_workspace - border_top - border_left - h)
        self.root.geometry("{}x{}+{}+{}".format(w, h, x, y))
        self.root.update()
        self.root.maxsize(grid_size * grid_length + 1, grid_size * grid_height + 1)
        self.root.wm_attributes('-alpha', 1.0)

    def focus_in(self, _):
        """
        Method callback if window gets focused.

        :param _: Event
        """
        self.pause_flag.set()

    def focus_out(self, _):
        """
        Method callback if window loses focused.

        :param _: Event
        """
        self.pause_flag.clear()

    def handle_close(self):
        """
        Callback method for window exit.
        """
        logging.debug('Exit GUI')
        self.exit_flag.set()
        self.root.destroy()

    @staticmethod
    def get_workspace_size():
        """
        Retrieves the size of the workspace by creating a transparent maximized window and different size variables.

        :return: tuple (x, y) containing the width and height of the workspace
        :rtype: (int, int)
        """
        r = Tk()
        r.wm_attributes('-alpha', .0)
        r.wm_state('zoomed')
        r.update()
        rx = r.winfo_rootx()
        ry = r.winfo_rooty()
        geo = Constants.parse_geometry(r.wm_geometry())
        r.destroy()
        return geo[0] + rx, geo[1] + ry

    def calc_frame(self):
        """
        Calculates the size of the outer window frame.

        :return: tuple containing the left and top border and the size of the self.root window
        :rtype: (int, int, int, int)
        """
        self.root.update()
        w, h, x, y = Constants.parse_geometry(self.root.wm_geometry())

        border_left = self.root.winfo_rootx() - x
        border_top = self.root.winfo_rooty() - y

        return border_left, border_top, w, h

    def run(self):
        """
        Method that enters the gui event loop. This method is blocking, so it should be started in a thread.
        """
        self.highlight()
        self.root.mainloop()

    def highlight(self):
        """
        Method that handles highlighting of single key shapes.
        """
        self.root.after(50, self.highlight)

        while not self.highlight_keys.empty():
            i = self.keyboard_layout.get_key(self.highlight_keys.get_nowait())

            if i is not None:
                i.physical_highlight = True
                if i.virtual_highlight:
                    self.w.itemconfigure(i.shape, fill=both_highlight_color)
                else:
                    self.w.itemconfigure(i.shape, fill=physical_highlight_color)


        while not self.reset_highlight_keys.empty():
            key = self.reset_highlight_keys.get_nowait()
            i = self.keyboard_layout.get_key(key)
            i.physical_highlight = False

            self.root.after(100, self.reset_highlight, key)

        while not self.simulated_keys.empty():
            key, highlight_flag = self.simulated_keys.get_nowait()
            i = self.keyboard_layout.get_key(key)

            if i is not None:
                i.virtual_highlight = highlight_flag

                if highlight_flag and i.physical_highlight:
                    self.w.itemconfigure(i.shape, fill=both_highlight_color)
                elif highlight_flag:
                    self.w.itemconfigure(i.shape, fill=virtual_highlight_color)
                else:
                    self.root.after(100, self.reset_highlight(key))


    def reset_highlight(self, vkey):
        """
        Resets the color of the key with the virtual key code vkey

        :param vkey: virtual key code
        :type vkey: int
        """
        i = self.keyboard_layout.get_key(vkey)
        if i is not None:
            if i.virtual_highlight and i.physical_highlight:
                self.w.itemconfigure(i.shape, fill=both_highlight_color)
            elif i.virtual_highlight:
                self.w.itemconfigure(i.shape, fill=physical_highlight_color)
            elif i.physical_highlight:
                self.w.itemconfigure(i.shape, fill=virtual_highlight_color)
            else:
                self.w.itemconfigure(i.shape, fill=key_color)
