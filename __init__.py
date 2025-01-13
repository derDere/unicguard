import unicurses as uc


#KEY_ESC = 27
#KEY_ESCAPE = KEY_ESC


_global_color_number = 1;
_global_styles = {}


def color_unified_256(font_color, back_color):
  global _global_styles

  if (font_color, back_color) in global_styles:
    return global_styles[(font_color, back_color)]

  style = global_color_number
  uc.init_pair(style, font_color, back_color)
  global_styles[(font_color, back_color)] = style

  global_color_number += 1
  return style


class Color:

  id:int
  key:str
  fg:int
  bg:int
  additional_attributes:list[int]

  def __init__(self, fg:int, bg:int=uc.COLOR_BLACK, *additional_attributes:int):
    global _global_color_number, _global_styles
    self.fg = fg
    self.bg = bg
    self.additional_attributes = additional_attributes
    self.key = f"f{fg};b{bg};a{','.join(map(str, additional_attributes))}"
    self.id = _global_color_number
    _global_color_number += 1
    uc.init_pair(self.id, fg, bg)
    _global_styles[self.key] = self.id


class UnicursesGuard:

  show_exceptions:bool = False
  screen:uc.WINDOW = None

  def __enter__(self, start_color:bool=True, noecho:bool=True, hide_cursor:bool=True, keypad:bool=True, show_exceptions:bool=False):
    self.show_exceptions = show_exceptions
    self.screen = uc.initscr() # Initialize the screen
    if start_color: uc.start_color() # Starts color mode to allow for custom colors
    if noecho: uc.noecho() # Turns off echoing of keys
    if hide_cursor: uc.curs_set(False) # Hides the cursor
    if keypad: uc.keypad(self.screen, True) # Allows for special keys to be read
    return self.screen

  def __exit__(self, type, value, traceback):
    uc.endwin()
    if type is not None:
      if self.show_exceptions:
        print(type)
        print(value)
        print(traceback)
      return False
    return True
