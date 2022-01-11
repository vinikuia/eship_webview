from cefpython3 import cefpython as cef
import ctypes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from PIL import Image, __version__ as PILLOW_VERSION
except ImportError:
    print("[screenshot.py] Error: PIL module not available. To install"
          " type: pip install Pillow")

import sys
import os
import platform
import logging as _logging
import uuid

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"
ICO_EXT = ".ico" if tk.TkVersion > 8.5 else ".gif"
# Config
SCREENSHOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               str(uuid.uuid4())+".png")
VIEWPORT_SIZE = (900, 640)
class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete
            sys.stdout.write(os.linesep)
            # print("[screenshot.py] Web page loading is complete")
            # print("[screenshot.py] Will save screenshot in 2 seconds")
            # # Give up to 2 seconds for the OnPaint call. Most of the time
            # # it is already called, but sometimes it may be called later.
            # cef.PostDelayedTask(cef.TID_UI, 2000, save_screenshot, browser)

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())
