#!/usr/bin/env python3
"""
Snail – a harmless process that just waits to be killed.

Now the banner scrolls horizontally across the terminal using asciimatics.
A SIGTERM handler prints “killed by Salt” before exiting.
"""

import os
import sys
import time
import signal
from typing import NoReturn

# ----------------------------------------------------------------------
# asciimatics imports
# ----------------------------------------------------------------------
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent

# ----------------------------------------------------------------------
# Banner text (feel free to edit)
# ----------------------------------------------------------------------
BANNER_TEXT = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣦⠀⢀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣿⣿⣷⣶⣦⣄⠀⠀⠀⠀⠀⠀⢰⡟⠈⠁⣰⣿⡗⠀
⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⢸⡇⠀⢠⡟⠀⠀⠀
⠀⠀⠀⣰⣿⣿⣿⣿⠟⠋⣉⣉⣉⠙⠻⣿⣿⣿⣷⡀⠀⠀⢸⡇⠀⢸⠃⠀⠀⠀
⠀⠀⢀⣿⣿⣿⣿⡇⢠⣿⣿⣿⢿⣿⣆⠘⣿⣿⣿⣷⡀⠀⢸⣧⠀⢸⡇⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⡇⠸⣿⣿⣿⠆⣿⣿⡄⢸⣿⣿⣿⣧⠀⣼⣿⣿⣿⣇⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣦⣈⣉⣁⣴⣿⣿⠁⣼⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⣰⣿⣿⣿⣿⡿⠀⣿⣿⣿⣿⡿⠀⠀⠀
⠀⠀⠀⠀⠈⠻⠿⣿⣿⣿⠿⠟⠋⠀⠾⢿⣿⣿⠿⠟⢁⣼⣿⣿⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⣀⣤⣤⣤⣤⣤⣤⣶⣿⣷⣦⣤⣤⣤⣴⣾⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀
⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# ----------------------------------------------------------------------
# Signal handling
# ----------------------------------------------------------------------
def _sigterm_handler(signum, frame):
    """
    Called when the process receives SIGTERM (e.g. from Salt).
    Prints a friendly message and exits with status 0.
    """
    # Using `print` ensures the message appears on the terminal even if
    # asciimatics has taken over the screen.
    print("\nkilled by Salt", flush=True)
    time.sleep(5)
    sys.exit(0)


# Register the handler as soon as the module is imported.
signal.signal(signal.SIGTERM, _sigterm_handler)


# ----------------------------------------------------------------------
# Rendering logic
# ----------------------------------------------------------------------
def _draw_scrolling_banner(screen: Screen) -> None:
    """
    Render ``BANNER_TEXT`` moving across the terminal.
    Exits cleanly on ESC or Ctrl‑C (KeyboardInterrupt).
    """
    height = screen.height
    width = screen.width

    banner_lines = BANNER_TEXT.strip("\n").split("\n")
    banner_height = len(banner_lines)
    banner_width = max(len(line) for line in banner_lines)

    # Start fully off‑screen to the left.
    col = -banner_width
    # Vertically centre the banner (adjust if you prefer a different row).
    row_offset = max((height - banner_height) // 2, 0)

    while True:
        # Clear previous frame.
        screen.clear_buffer(Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLACK)

        # Draw each line at the current horizontal offset.
        for i, line in enumerate(banner_lines):
            visible_part = line[max(0, -col) : width - col]
            if visible_part:
                screen.print_at(
                    visible_part,
                    max(col, 0),
                    row_offset + i,
                    colour=Screen.COLOUR_GREEN,
                )

        screen.refresh()

        # Advance one column each frame.
        col += 1
        if col > width:
            col = -banner_width

        # Control speed – smaller = faster.
        time.sleep(0.05)

        # Detect ESC or Ctrl‑C.
        ev = screen.get_event()
        if isinstance(ev, KeyboardEvent):
            if ev.key_code in (Screen.KEY_ESCAPE, 3):  # 3 == Ctrl‑C
                raise KeyboardInterrupt


def main() -> NoReturn:
    """
    Entry point – wraps the animation in asciimatics' screen manager.
    """
    try:
        Screen.wrapper(_draw_scrolling_banner)
    except KeyboardInterrupt:
        # Graceful exit for manual interruption.
        print("\nSnail crawled away.", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
