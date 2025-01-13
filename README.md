# UnicGuard

UnicGuard is a small utility library for unicurses applications. It provides a context manager for unicurses applications and a text style class.

## Installation

To install UnicGuard, simply run:

```bash
git submodule add https://github.com/derDere/unicguard.git
```

## Usage

### UnicursesGuard

The `UnicursesGuard` class is a context manager for unicurses applications. It initializes the screen and handles exceptions.

Use with a 'with' statement to ensure the screen is properly initialized and closed.

```python
from unicguard import UnicursesGuard

with UnicursesGuard() as stdscr:
  # Your code here
```

#### Options

- `start_color` (bool): Starts color mode to allow for custom colors. Defaults to True.
- `noecho` (bool): Turns off echoing of keys. Defaults to True.
- `hide_cursor` (bool): Hides the cursor. Defaults to True.
- `keypad` (bool): Allows for special keys to be read. Defaults to True.
- `show_exceptions` (bool): If True, exceptions will be printed to the console. Defaults to False.

### TextStyle

The `TextStyle` class defines a text style for a ncurses application, containing the font color, background color and additional attributes.

```python
from unicguard import TextStyle

style = TextStyle(uc.COLOR_WHITE, uc.COLOR_BLUE, uc.A_BOLD)

style.on(stdscr)
stdscr.addstr("Hello, World!")
style.off(stdscr)
```

## Unicurses

This project uses the [unicurses](https://sourceforge.net/projects/pyunicurses/files/) library.

### Install Unicurses

Within this repository, you can find the `install_unicurses.sh` script. Run it to install unicurses.

```bash
sudo ./install_unicurses.sh
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

This project was created by [derDere](https://github.com/derDere)
