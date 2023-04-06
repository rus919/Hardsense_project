import customtkinter as ct
import os
from PIL import Image
ct.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ct.deactivate_automatic_dpi_awareness() # Make sure DPI scale is alwaya 100%, but test later

# sticky = S = south N = north W = west S = south

def create_nav(parent, aim_callback, trigger_callback, visuals_callback, players_callback, misc_callback, panel_callback, settings_callback):
    frame = ct.CTkFrame(master = parent, corner_radius=0)
    
    height = 60
    border_spacing = 10
    corner_radius = 0
    fg_color = 'transparent'
    text_color = ('gray10', 'gray90')
    hover_color = ('gray10')
    anchor = 'w'
    sticky = 'ew'
    image_size = (25, 25)

    frame.grid(row=0, column=0, sticky="nsew")
    
    #Configure row 5 so we can push row 6 to the bottom
    frame.grid_rowconfigure(6, weight=1) 
    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/GUI")
    logo_img = ct.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(50, 45))
    aimbot_img = ct.CTkImage(Image.open(os.path.join(image_path, "aimbot.png")), size = image_size)
    trigger_img = ct.CTkImage(Image.open(os.path.join(image_path, "triggerbot.png")), size=image_size)
    visuals_img = ct.CTkImage(Image.open(os.path.join(image_path, "visuals.png")), size=image_size)
    players_img = ct.CTkImage(Image.open(os.path.join(image_path, "players.png")), size=image_size)
    misc_img = ct.CTkImage(Image.open(os.path.join(image_path, "misc.png")), size = image_size)
    user_img = ct.CTkImage(Image.open(os.path.join(image_path, "user.png")), size = image_size)
    settings_img = ct.CTkImage(Image.open(os.path.join(image_path, "settings.png")), size = image_size)
    
    nav_logo = ct.CTkLabel(frame, text = "", image=logo_img, compound="left")    
    nav_logo.grid(row=0, column=0, pady=10) 

    nav_aimbot = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Aimbot", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor, image = aimbot_img, command = aim_callback).grid(row=1, column=0, sticky= sticky)
    nav_trigger = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Triggerbot", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = trigger_img, command = trigger_callback).grid(row=2, column=0, sticky = sticky)
    nav_visuals = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Visuals", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = visuals_img, command = visuals_callback).grid(row=3, column=0, sticky = sticky)
    nav_players = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Players", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = players_img, command = players_callback).grid(row=4, column=0, sticky = sticky)
    nav_misc = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Misc", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = misc_img, command = misc_callback).grid(row=5, column=0, sticky = sticky)
    nav_user = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="User Panel", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = user_img, command = panel_callback).grid(row=7, column=0, sticky = sticky)
    nav_settings = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Settings", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = settings_img, command = settings_callback).grid(row=8, column=0, sticky = sticky)
    
    return frame

def create_aimbot(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="Aimbot", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    
    return frame

def create_triggerbot(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="Triggerbot", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    
    return frame

def create_visuals(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="Visuals", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    
    return frame

def create_players(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="Players", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

def create_misc(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="Misc", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

def create_user_panel(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="User Panel", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

def create_settings(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
    
    frame.grid(row=0, column=1, sticky="nsew")
    
    test = ct.CTkLabel(frame, text="Settings", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("test") # Random name window to change signatures?
        self.geometry(f"{1000}x{600}") # Default window size
        self.minsize(width = 1000, height = 600)
        
        # set grid layout 1x2 -> nav on left main content on the right
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create navigation menu
        create_nav(self, self.nav_aimbot_callback, self.nav_triggerbot_callback, self.nav_visuals_callback, self.nav_players_callback, self.nav_misc_callhack, self.nav_panel_callback, self.nav_settings_callback)

        
        # # create root settings frame
        # self.settings_frame = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.settings_frame.grid_rowconfigure(1, weight=0)
        # self.settings_frame.grid_columnconfigure(1, weight=0)
        
        
        # self.settings_frame_header_text = ct.CTkLabel(self.settings_frame, text="Settings", anchor="w")
        # self.settings_frame_header_text.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        
        # # create header config frame
        # self.settings_frame_config = ct.CTkFrame(self.settings_frame, corner_radius=0, fg_color="#282929")
        # self.settings_frame_config.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        # self.settings_frame_config.grid_rowconfigure(1, weight=0)
        # self.settings_frame_config.grid_columnconfigure(1, weight=0)
        
        # # Buttom border
        # self.settings_config_border = ct.CTkLabel(self.settings_frame_config, corner_radius=0, fg_color="transparent", text = "_______", text_color="#575757")
        # self.settings_config_border.place(x=10, y=15)
        # # config text
        # self.settings_config_header_text = ct.CTkLabel(self.settings_frame_config, corner_radius=0, text="Config")
        # self.settings_config_header_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # self.settings_frame_btn = ct.CTkButton(self.settings_frame_config, text="123")
        # self.settings_frame_btn.grid(row=2, column=0, padx=10, pady=15)
        
        # self.settings_btn2 = ct.CTkButton(self.settings_frame_config, text="321")
        # self.settings_btn2.grid(row=2, column=1, padx=1, pady=1)

    def nav_aimbot_callback(self):
        self.select_frame_by_name("Aimbot")
    def nav_triggerbot_callback(self):
        self.select_frame_by_name("Triggerbot")
    def nav_visuals_callback(self):
        self.select_frame_by_name("Visuals")
    def nav_players_callback(self):
        self.select_frame_by_name("Players")
    def nav_misc_callhack(self):
        self.select_frame_by_name("Misc")
    def nav_panel_callback(self):
        self.select_frame_by_name("Panel")
    def nav_settings_callback(self):
        self.select_frame_by_name("Settings")

    def select_frame_by_name(self, name):
        if name == 'Aimbot':
            create_aimbot(self)
        elif name == 'Triggerbot':
            create_triggerbot(self)
        elif name == "Visuals":
            create_visuals(self)
            #Change navigation frame color when selected
            # create_nav.nav_aimbot.configure(fg_color=("gray20"))
            # print(create_nav.nav_misc)
        elif name == 'Players':
            create_players(self)
        elif name == 'Misc':
            create_misc(self)
        elif name == 'Panel':
            create_user_panel(self)
        elif name == 'Settings':
            create_settings(self)

if __name__ == "__main__":
    app = App()
    app.iconbitmap("assets/GUI/icon.ico")
    app.mainloop()