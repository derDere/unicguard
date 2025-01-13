"""UnicGuard is a small utility library for unicurses applications. It provides a context manager for unicurses applications and a text style class.
"""


import unicurses as uc


_global_styles = {}


def color_unified_256(font_color:int, back_color:int):
  """ Defines a fixed color pair for the given font- and background colors.
  Initializes the color pair if it does not exist yet.

  Args:
      font_color (int): 256 Color code for the font color (0-255)
      back_color (int): 256 Color code for the background color (0-255)

  Returns:
      int: The color pair id
  """

  global _global_styles

  id = font_color << 8 | back_color
  if id in _global_styles:
    return id

  uc.addstr(f"Initializing color pair {id} with font color {font_color} and background color {back_color}\n")
  uc.init_pair(id, font_color, back_color)
  _global_styles[id] = True
  return id


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

  show_exceptions:bool = False
  screen = None

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


def main():
  """Main function for testing the library.
  """
  with UnicursesGuard() as stdscr:
    uc.init_pair(256, uc.COLOR_WHITE, uc.COLOR_BLUE)
    #style = TextStyle(uc.COLOR_WHITE, uc.COLOR_BLUE, uc.A_BOLD)
    #style.on(stdscr)
    uc.attron(uc.color_pair(256))
    stdscr.addstr("Hello, World!")
    uc.attroff(uc.color_pair(256))
    #style.off(stdscr)
    stdscr.addstr("\n\nPress any key to exit...\n\n")
    stdscr.refresh()
    uc.getch()


if __name__ == "__main__":
  main()
