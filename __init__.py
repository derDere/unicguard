"""UnicGuard is a small utility library for unicurses applications. It provides a context manager for unicurses applications and a text style class.
"""


import unicurses as uc


MAX_COLOR_PAIR_COUNT = 256


_global_styles = {}
_global_color_id_counter = 255


def color_unified_256(font_color:int, back_color:int):
  """ Defines a fixed color pair for the given font- and background colors.
  Initializes the color pair if it does not exist yet.

  Args:
      font_color (int): 256 Color code for the font color (0-255)
      back_color (int): 256 Color code for the background color (0-255)

  Returns:
      int: The color pair id
  """

  global _global_styles, _global_color_id_counter

  id = "f%03i;b%03i" % (font_color, back_color)
  if id in _global_styles:
    return _global_styles[id]

  pair_number = _global_color_id_counter
  if pair_number >= MAX_COLOR_PAIR_COUNT:
    raise Exception("Maximum number of color pairs reached.")
  _global_color_id_counter += 1

  uc.init_pair(pair_number, font_color, back_color)
  _global_styles[id] = pair_number
  return pair_number


class TextStyle:
  """Defines a text style for a ncurses application, containing the font color, background color and additional attributes.
  """

  _id:int
  fg:int
  bg:int
  additional_attributes:list[int]

  def __init__(self, fg:int, bg:int=uc.COLOR_BLACK, *additional_attributes:int):
    """Initializes a new TextStyle object.

    Args:
        fg (int): 256 Color code for the font color (0-255)
        bg (int, optional): 256 Color code for the background color (0-255). Defaults to uc.COLOR_BLACK.
        *additional_attributes (int): Additional attributes for the text style. Can be any of the unicurses attributes.
    """
    self.fg = fg
    self.bg = bg
    self.additional_attributes = additional_attributes
    self._id = color_unified_256(fg, bg)

  def on(self, screen):
    """Turns on the text style for the given window.
    """
    screen.attron(uc.color_pair(self._id))
    for attr in self.additional_attributes:
      screen.attron(attr)

  def off(self, screen):
    """Turns off the text style for the given window.
    """
    screen.attroff(uc.color_pair(self._id))
    for attr in self.additional_attributes:
      screen.attroff(attr)


class UnicursesGuard:
  """A context manager for unicurses applications. Initializes the screen and handles exceptions.

  Use with a 'with' statement to ensure the screen is properly initialized and closed.

  Optons:
    start_color (bool): Starts color mode to allow for custom colors. Defaults to True.
    noecho (bool): Turns off echoing of keys. Defaults to True.
    hide_cursor (bool): Hides the cursor. Defaults to True.
    keypad (bool): Allows for special keys to be read. Defaults to True.
    show_exceptions (bool): If True, exceptions will be printed to the console. Defaults to False.
  """

  start_color:bool = True
  noecho:bool = True
  hide_cursor:bool = True
  keypad:bool = True
  show_exceptions:bool = False
  screen = None

  def __init__(self, start_color:bool=True, noecho:bool=True, hide_cursor:bool=True, keypad:bool=True, show_exceptions:bool=False):
    self.start_color = start_color
    self.noecho = noecho
    self.hide_cursor = hide_cursor
    self.keypad = keypad
    self.show_exceptions = show_exceptions

  def __enter__(self):
    self.screen = uc.initscr() # Initialize the screen
    if self.start_color: uc.start_color() # Starts color mode to allow for custom colors
    if self.noecho: uc.noecho() # Turns off echoing of keys
    if self.hide_cursor: uc.curs_set(False) # Hides the cursor
    if self.keypad: uc.keypad(self.screen, True) # Allows for special keys to be read
    return self.screen

  def __exit__(self, type, value, traceback):
    uc.endwin()
    if type is not None:
      if self.show_exceptions:
        print("UnicursesGuard got exited because of an exception:\n")
        print(type.__name__)
        print("")
        print(" - " + value)
        print("")
        print(traceback.format_exc())
        print("")
      return False
    return True


def main():
  """Main function for testing the library.
  """
  with UnicursesGuard() as stdscr:
    style = TextStyle(uc.COLOR_WHITE, uc.COLOR_BLUE, uc.A_BOLD)
    style.on(stdscr)
    stdscr.addstr("Hello, World!")
    style.off(stdscr)
    stdscr.addstr("\n\nPress any key to exit...\n\n")
    stdscr.refresh()
    uc.getch()


if __name__ == "__main__":
  main()
