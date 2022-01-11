try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from PIL import Image, __version__ as PILLOW_VERSION
except ImportError:
    print("[screenshot.py] Error: PIL module not available. To install"
          " type: pip install Pillow")
from PIL import ImageGrab
import uuid
import os
import logging as _logging
from e_mail.EmailHandler import EmailHandler
logger = _logging.getLogger("tkinter_.py")
SCREENSHOT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'public/screenshots',  str(uuid.uuid4()) +".png"))


class NavigationBar(tk.Frame):

    IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"
    ICO_EXT = ".ico" if tk.TkVersion > 8.5 else ".gif"

    def __init__(self, master):
        # self.back_state = tk.NONE
        # self.forward_state = tk.NONE
        # self.back_image = None
        # self.forward_image = None
        self.reload_image = None

        tk.Frame.__init__(self, master)
        resources = os.path.join(os.path.dirname(__file__), "resources")

        # Back button
        # back_png = os.path.join(resources, "back" + IMAGE_EXT)
        # if os.path.exists(back_png):
        #     self.back_image = tk.PhotoImage(file=back_png)
        # self.back_button = tk.Button(self, image=self.back_image,
        #                              command=self.go_back)
        # self.back_button.grid(row=0, column=0)
        #
        # # Forward button
        # forward_png = os.path.join(resources, "forward" + IMAGE_EXT)
        # if os.path.exists(forward_png):
        #     self.forward_image = tk.PhotoImage(file=forward_png)
        # self.forward_button = tk.Button(self, image=self.forward_image,
        #                                 command=self.go_forward)
        # self.forward_button.grid(row=0, column=1)

        # Reload button
        reload_png = os.path.join(resources, "refresh" + self.IMAGE_EXT)
        if os.path.exists(reload_png):
            self.reload_image = tk.PhotoImage(file=reload_png)
        self.reload_image.zoom(25).subsample(100)
        self.reload_button = tk.Button(self, image=self.reload_image,
                                       command=self.reload)
        self.reload_button.grid(row=0, column=0)

        # print screen button

        print_screen_png = os.path.join(resources, "screenshot" + self.IMAGE_EXT)
        if os.path.exists(print_screen_png):
            self.print_screen_image = tk.PhotoImage(file=print_screen_png)
        self.print_screen_image.zoom(25).subsample(100)
        self.print_screen_button = tk.Button(self, image=self.print_screen_image,command=self.take_screenshot)
        self.print_screen_button.grid(row=0, column=1)

        # Url entry
        self.url_entry = tk.Entry(self)
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        self.url_entry.bind("<Return>", self.on_load_url)
        self.url_entry.bind("<Button-1>", self.on_button1)
        self.url_entry.grid(row=0, column=2,
                            sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        # Update state of buttons
        self.update_state()

    # def go_back(self):
    #     if self.master.get_browser():
    #         self.master.get_browser().GoBack()
    #
    # def go_forward(self):
    #     if self.master.get_browser():
    #         self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def take_screenshot(self):
        bbox = None
        im = ImageGrab.grab(bbox)
        im.save(SCREENSHOT_PATH, "PNG")
        im.close()
        email = EmailHandler()
        email.sendEmail(SCREENSHOT_PATH)

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """For focus problems see Issue #255 and Issue #535. """
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()

        if not browser:
            # if self.back_state != tk.DISABLED:
            #     # self.back_button.config(state=tk.DISABLED)
            #     self.back_state = tk.DISABLED
            # if self.forward_state != tk.DISABLED:
            #     # self.forward_button.config(state=tk.DISABLED)
            #     self.forward_state = tk.DISABLED
            # self.after(100, self.update_state)
            return
        # if browser.CanGoBack():
        #     if self.back_state != tk.NORMAL:
        #         # self.back_button.config(state=tk.NORMAL)
        #         self.back_state = tk.NORMAL
        # else:
        #     if self.back_state != tk.DISABLED:
        #         # self.back_button.config(state=tk.DISABLED)
        #         self.back_state = tk.DISABLED
        # if browser.CanGoForward():
        #     if self.forward_state != tk.NORMAL:
        #         # self.forward_button.config(state=tk.NORMAL)
        #         self.forward_state = tk.NORMAL
        # else:
        #     if self.forward_state != tk.DISABLED:
        #         # self.forward_button.config(state=tk.DISABLED)
        #         self.forward_state = tk.DISABLED
        self.after(100, self.update_state)
