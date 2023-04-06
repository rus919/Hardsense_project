import customtkinter as ct
from CTkColorPicker import AskColor
import os
from PIL import Image
ct.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ct.deactivate_automatic_dpi_awareness() # Make sure DPI scale is alwaya 100%, but test later

# sticky = S = south N = north W = west S = south


class state:
    master_switch = 0

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
        
    test = ct.CTkLabel(frame, text="Aimbot", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    
    return frame

def create_triggerbot(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
        
    test = ct.CTkLabel(frame, text="Triggerbot", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    
    return frame

class create_visuals(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color='transparent')
        
        self.container = ct.CTkFrame(self, corner_radius=5, fg_color='#3d3d3d', border_color='#4a4a4a', border_width=2)
        self.container.grid(row=0, column=0, pady=10, padx=10)
        
        # Switch vars
        switch_width = 40
        corner_radius = 10
        button_hover_color = '#58009F'
        fg_color = '#808080' # When disabled
        progress_color = '#808080' # When active
        button_color = '#6c0fb8'
        
        # Drop box vars
        o_width = 55
        o_corner_radius = 5
        o_fg_color = '#3d3d3d'
        o_button_color = '#3d3d3d'
        o_button_hover_color = '#313131'
        o_dropdown_fg_color = '#3d3d3d'
        o_dropdown_hover_color = '#313131'
        o_dropdown_text_color = '#fff' # Inside color
        o_text_color = '#fff' # Outside color
        
        # Color picker vars
        c_width = 25
        c_height = 15
        c_corner_radius = 1
        c_hover_color = '#808080'
        
        self.master_switch_text = ct.CTkLabel(self.container, text='Master Switch')
        self.master_switch_text.grid(row=2, column=0, pady=5, padx=10, sticky='w')
        self.master_switch_separator = ct.CTkLabel(self.container, text='').grid(row=2, column=1, pady=5, padx=50)
        self.master_switch_checkbox = ct.CTkSwitch(self.container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.master_switch_e)
        self.master_switch_checkbox.grid(row=2, column=2, pady=0, padx=3, sticky='e')
        
        self.players_box_text = ct.CTkLabel(self.container, text='Players Box')
        self.players_box_text.grid(row=3, column=0, pady=5, padx=10, sticky='w')       
        self.players_box_option = ct.CTkOptionMenu(self.container, values=['-', '1'], width=o_width, corner_radius=o_corner_radius, fg_color=o_fg_color, button_color=o_button_color, button_hover_color=o_button_hover_color, dropdown_fg_color=o_dropdown_fg_color, dropdown_hover_color=o_dropdown_hover_color, dropdown_text_color=o_dropdown_text_color, text_color=o_text_color)
        self.players_box_option.grid(row=3, column=2, pady=5, padx=3)
        
        # self.players_box_color = ct.CTkButton(self.container, text='', width=c_width, height=c_height, corner_radius=c_corner_radius, hover_color=c_hover_color, command=self.ask_color)
        # self.players_box_color.grid(row=3, column=2, padx=10)
        
        self.players_head_text = ct.CTkLabel(self.container, text='Head Esp')
        self.players_head_text.grid(row=4, column=0, pady=5, padx=10, sticky='w')        
        self.players_head_option = ct.CTkOptionMenu(self.container, values=['-', '1'], width=o_width, corner_radius=o_corner_radius, fg_color=o_fg_color, button_color=o_button_color, button_hover_color=o_button_hover_color, dropdown_fg_color=o_dropdown_fg_color, dropdown_hover_color=o_dropdown_hover_color, dropdown_text_color=o_dropdown_text_color, text_color=o_text_color).grid(row=4, column=2, pady=5, padx=3)
            
    # def ask_color(self):
    #     pick_color = AskColor(width=300) # Open the Color Picker, size of the window can be changed by adjusting width parameter
    #     color = pick_color.get() # Get the color
    #     self.players_box_color.configure(fg_color=color)
    
    def master_switch_e(self):
        if self.master_switch_checkbox.get() == 1:
            state.master_switch = 1
        else:
            state.master_switch = 0

def create_players(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
        
    test = ct.CTkLabel(frame, text="Players", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

def create_misc(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
        
    test = ct.CTkLabel(frame, text="Misc", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

def create_user_panel(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
        
    test = ct.CTkLabel(frame, text="User Panel", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    return frame

def create_settings(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
        
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
        
        self.aimbot_tab = create_aimbot(self)
        self.triggerbot_tab = create_triggerbot(self)
        self.visuals_tab = create_visuals(self)
        self.players_tab = create_players(self)
        self.misc_tab = create_misc(self)
        self.user_panel_tab = create_user_panel(self)
        self.settinsg_tab = create_settings(self)

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
            self.aimbot_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.aimbot_tab.grid_forget()
        if name == 'Triggerbot':
            self.triggerbot_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.triggerbot_tab.grid_forget()
        if name == "Visuals":
            self.visuals_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.visuals_tab.grid_forget()
            #Change navigation frame color when selected
            # create_nav.nav_aimbot.configure(fg_color=("gray20"))
            # print(create_nav.nav_misc)
        if name == 'Players':
            self.players_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.players_tab.grid_forget()
        if name == 'Misc':
            self.misc_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.misc_tab.grid_forget()
        if name == 'Panel':
            self.user_panel_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.user_panel_tab.grid_forget()
        if name == 'Settings':
            self.settinsg_tab.grid(row=0, column=1, sticky="nsew")
        else:
            self.settinsg_tab.grid_forget()