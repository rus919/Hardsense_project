import customtkinter as ct
from CTkColorPicker import AskColor
import os
from PIL import Image
from engine.state import state
from engine.process import  Windll
from tools.entity_parse import getPlayerInfo, playersInfo
import requests

import webbrowser as web
import json

ct.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
ct.deactivate_automatic_dpi_awareness() # Make sure DPI scale is alwaya 100%, but test later

# sticky = N = north E = East W = west S = south

app_colors = {
    'nav': {
        'bg_clr': 'transparent'
    },
    'players': {
        'bg_clr': '#1a1a1a',
        'header_btn': {
            'bg_clr': '#4a4a4a',
            'selected': '#39314A',
            'unselected': '#202020',
            'hover': '#282828' # Add border color too
            },
        'container': {
            'bg_clr': '#202020',
            'border_clr': '#4a4a4a',
            'header_text': {
                'bg_clr': '#202020',
                'f_size': 12,
                'f_weight': 'bold'
            },
            'content': {
                'bg_clr': '#202020',
                't_clr': 'red',
                'ct_clr': 'blue',
                'spec_clr': 'gray',
                'bot_clr': 'black',
            }
        }
    }
}

def create_nav(parent, aim_callback, trigger_callback, visuals_callback, players_callback, misc_callback, panel_callback, settings_callback):
    frame = ct.CTkFrame(master = parent, corner_radius=0)
    
    height = 60
    border_spacing = 10
    corner_radius = 0
    fg_color = app_colors['nav']['bg_clr']
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
    nav_players = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Players", fg_color = fg_color, text_color = text_color, hover_color = hover_color, anchor = anchor,image = players_img, command = players_callback)
    nav_players.grid(row=4, column=0, sticky = sticky)
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
        
        # container
        f_fg_color = '#282828'
        f_border_color = '#4a4a4a'
        
        self.player_esp_container = ct.CTkFrame(self, corner_radius=5, fg_color=f_fg_color, border_color=f_border_color, border_width=1, width=250)
        self.player_esp_container.grid(row=1, column=0, pady=0, padx=10)
        self.player_esp_label = ct.CTkLabel(self, text='Player ESP', fg_color='#202020', width=260, corner_radius=5)
        self.player_esp_label.grid(row=0, column=0, pady=5, padx=10)
        
        self.local_esp_container = ct.CTkFrame(self, corner_radius=5, fg_color=f_fg_color, border_color=f_border_color, border_width=1, width=250)
        self.local_esp_container.grid(row=1, column=1, pady=0, padx=0, sticky='n')
        self.local_esp_label = ct.CTkLabel(self, text='Local ESP', fg_color='#202020', width=260, corner_radius=5)
        self.local_esp_label.grid(row=0, column=1, pady=5, padx=10)
        
        self.other_esp_container = ct.CTkFrame(self, corner_radius=5, fg_color=f_fg_color, border_color=f_border_color, border_width=1, width=250)
        self.other_esp_container.grid(row=1, column=2, pady=0, padx=10, sticky='n')
        self.other_esp_label = ct.CTkLabel(self, text='Other ESP', fg_color='#202020', width=260, corner_radius=5)
        self.other_esp_label.grid(row=0, column=2, pady=5, padx=10)
        
        
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
        
        l_font_size = 13
        l_font_weight = 'bold'
        container_pady = 10
        container_padx = 10
        
        # Players ESP
        
        self.master_switch_text = ct.CTkLabel(self.player_esp_container, text='Master switch', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.master_switch_text.grid(row=2, column=0, pady=container_pady, padx=container_padx, sticky='w')
        
        self.separator = ct.CTkLabel(self.player_esp_container, text='').grid(row=2, column=1, pady=5, padx=50) # To make space between items
        
        self.master_switch_checkbox = ct.CTkSwitch(self.player_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.master_switch_e)
        self.master_switch_checkbox.grid(row=2, column=2, pady=10, padx=3, sticky='e')
        
        self.players_box_text = ct.CTkLabel(self.player_esp_container, text='Players box', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.players_box_text.grid(row=3, column=0, pady=container_pady, padx=container_padx, sticky='w')      
        
        self.players_box_option = ct.CTkOptionMenu(self.player_esp_container, values=['None', 'Normal', 'Large', 'Corner'], width=o_width, corner_radius=o_corner_radius, fg_color=o_fg_color, button_color=o_button_color, button_hover_color=o_button_hover_color, dropdown_fg_color=o_dropdown_fg_color, dropdown_hover_color=o_dropdown_hover_color, dropdown_text_color=o_dropdown_text_color, text_color=o_text_color, command=self.players_box_e)
        
        self.players_box_enable_checkbox = ct.CTkSwitch(self.player_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.players_box_enable_e)
        self.players_box_enable_checkbox.grid(row=3, column=2, pady=10, padx=3, sticky='e')
        
        # self.players_box_color = ct.CTkButton(self.container, text='', width=c_width, height=c_height, corner_radius=c_corner_radius, hover_color=c_hover_color, command=self.ask_color)
        # self.players_box_color.grid(row=3, column=2, padx=10)
        
        self.players_head_text = ct.CTkLabel(self.player_esp_container, text='Head esp', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.players_head_text.grid(row=4, column=0, pady=container_pady, padx=container_padx, sticky='w')       
        
        self.players_head_option = ct.CTkOptionMenu(self.player_esp_container, values=['None', 'Circle', 'Square'], width=o_width, corner_radius=o_corner_radius, fg_color=o_fg_color, button_color=o_button_color, button_hover_color=o_button_hover_color, dropdown_fg_color=o_dropdown_fg_color, dropdown_hover_color=o_dropdown_hover_color, dropdown_text_color=o_dropdown_text_color, text_color=o_text_color, command=self.players_head_e)
        self.players_head_enable_checkbox = ct.CTkSwitch(self.player_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.players_head_enable_e)
        self.players_head_enable_checkbox.grid(row=4, column=2, pady=10, padx=3, sticky='e')
        
        self.players_names_text = ct.CTkLabel(self.player_esp_container, text='Name esp', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.players_names_text.grid(row=5, column=0, pady=container_pady, padx=container_padx, sticky='w')  
             
        self.players_names_checkbox = ct.CTkSwitch(self.player_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.players_names_enable_e)
        self.players_names_checkbox.grid(row=5, column=2, pady=10, padx=3, sticky='e')
        
        self.players_health_text = ct.CTkLabel(self.player_esp_container, text='Health esp', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.players_health_text.grid(row=6, column=0, pady=container_pady, padx=container_padx, sticky='w')
        
        self.players_health_option = ct.CTkOptionMenu(self.player_esp_container, values=['None', 'Image', 'Text'], width=o_width, corner_radius=o_corner_radius, fg_color=o_fg_color, button_color=o_button_color, button_hover_color=o_button_hover_color, dropdown_fg_color=o_dropdown_fg_color, dropdown_hover_color=o_dropdown_hover_color, dropdown_text_color=o_dropdown_text_color, text_color=o_text_color, command=self.players_head_e)
        
        self.players_health_checkbox = ct.CTkSwitch(self.player_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.players_health_enable_e)
        self.players_health_checkbox.grid(row=6, column=2, pady=10, padx=3, sticky='e')
        
        self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Weapon esp', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.players_weapon_text.grid(row=7, column=0, pady=container_pady, padx=container_padx, sticky='w')
        
        self.players_weapon_option = ct.CTkOptionMenu(self.player_esp_container, values=['None', 'Image', 'Text'], width=o_width, corner_radius=o_corner_radius, fg_color=o_fg_color, button_color=o_button_color, button_hover_color=o_button_hover_color, dropdown_fg_color=o_dropdown_fg_color, dropdown_hover_color=o_dropdown_hover_color, dropdown_text_color=o_dropdown_text_color, text_color=o_text_color, command=self.players_head_e)
        
        self.players_weapon_checkbox = ct.CTkSwitch(self.player_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.players_health_enable_e)
        self.players_weapon_checkbox.grid(row=7, column=2, pady=10, padx=3, sticky='e')
        
        # self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Players 1', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        # self.players_weapon_text.grid(row=8, column=0, pady=10, padx=10, sticky='w')
        # self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Players 2', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        # self.players_weapon_text.grid(row=9, column=0, pady=10, padx=10, sticky='w')
        # self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Players 3', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        # self.players_weapon_text.grid(row=10, column=0, pady=10, padx=10, sticky='w')
        # self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Players 4', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        # self.players_weapon_text.grid(row=10, column=0, pady=10, padx=10, sticky='w')
        # self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Players 5', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        # self.players_weapon_text.grid(row=11, column=0, pady=10, padx=10, sticky='w')
        # self.players_weapon_text = ct.CTkLabel(self.player_esp_container, text='Players 6', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        # self.players_weapon_text.grid(row=12, column=0, pady=10, padx=10, sticky='w')
        
        # Local ESP
        
        self.spectator_text = ct.CTkLabel(self.local_esp_container, text='Specator List', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.spectator_text.grid(row=2, column=0, pady=container_pady, padx=container_padx, sticky='w')
        self.separator = ct.CTkLabel(self.local_esp_container, text='').grid(row=2, column=1, pady=5, padx=40) # To make space between itemsR
        self.spectator_checkbox = ct.CTkSwitch(self.local_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.spectator_e)
        self.spectator_checkbox.grid(row=2, column=2, pady=0, padx=3, sticky='e')
        
        self.bomb_text = ct.CTkLabel(self.local_esp_container, text='Bomb Info', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.bomb_text.grid(row=3, column=0, pady=container_pady, padx=container_padx, sticky='w')
        self.bomb_checkbox = ct.CTkSwitch(self.local_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.bomb_info_e)
        self.bomb_checkbox.grid(row=3, column=2, pady=0, padx=3, sticky='e')
        
        self.crosshair_text = ct.CTkLabel(self.local_esp_container, text='Sniper Crosshair', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.crosshair_text.grid(row=4, column=0, pady=container_pady, padx=container_padx, sticky='w')
        self.crosshair_checkbox = ct.CTkSwitch(self.local_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.crosshair_e)
        self.crosshair_checkbox.grid(row=4, column=2, pady=0, padx=3, sticky='e')
        
        self.recoil_text = ct.CTkLabel(self.local_esp_container, text='Recoil Crosshair', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.recoil_text.grid(row=5, column=0, pady=container_pady, padx=container_padx, sticky='w')
        self.recoil_checkbox = ct.CTkSwitch(self.local_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.recoil_e)
        self.recoil_checkbox.grid(row=5, column=2, pady=0, padx=3, sticky='e')
                
        self.weapon_esp_text = ct.CTkLabel(self.other_esp_container, text='Weapon ESP', font=ct.CTkFont(size= l_font_size, weight=l_font_weight), compound='center')
        self.weapon_esp_text.grid(row=2, column=0, pady=container_pady, padx=container_padx, sticky='w')
        self.separator = ct.CTkLabel(self.other_esp_container, text='').grid(row=2, column=1, pady=5, padx=50) # To make space between itemsR
        self.weapon_esp_checkbox = ct.CTkSwitch(self.other_esp_container, text='', width=2, switch_width=switch_width, border_width=4, border_color='transparent', corner_radius=corner_radius, button_hover_color=button_hover_color, fg_color=fg_color, progress_color=progress_color, button_color=button_color, command = self.master_switch_e)
        self.weapon_esp_checkbox.grid(row=2, column=2, pady=0, padx=3, sticky='e')

            
    # def ask_color(self):
    #     pick_color = AskColor(width=300) # Open the Color Picker, size of the window can be changed by adjusting width parameter
    #     color = pick_color.get() # Get the color
    #     self.players_box_color.configure(fg_color=color)
    
    def master_switch_e(self):
        if self.master_switch_checkbox.get() == 1:
            state.master_switch = 1
        else:
            state.master_switch = 0
    
    def players_box_enable_e(self):
        if self.players_box_enable_checkbox.get() == 1:
            self.players_box_option.grid(row=3, column=1, pady=5, padx=3)
            state.players_box_enabled = 1
        else:
            self.players_box_option.grid_forget()
            state.players_box_enabled = 0
            
    def players_box_e(self, e):#
        if e == str('None'):
            state.players_box_type = 'None'
        elif e == str('Normal'):
            state.players_box_type = 'Normal'
            
    def players_head_enable_e(self):
        if self.players_head_enable_checkbox.get() == 1:
            self.players_head_option.grid(row=4, column=1, pady=5, padx=3)
            state.players_head_enabled = 1
        else:
            self.players_head_option.grid_forget()
            state.players_head_enabled = 0
            
    def players_head_e(self, e):#
        if e == str('None'):
            state.players_head_type = 'None'
            
        elif e == str('Circle'):
            state.players_head_type = 'Circle'
            
    def players_names_enable_e(self):
        if self.players_names_checkbox.get() == 1:
            state.players_names_enabled = 1
        else:
            state.players_names_enabled = 0
        
    def players_health_enable_e(self):
        if self.players_health_checkbox.get() == 1:
            state.players_health_enabled = 1
        else:
            state.players_health_enabled = 0
            
    def spectator_e(self):
        if self.spectator_checkbox.get() == 1:
            state.spectator_enabled = 1
            print(state.spectator_enabled)
        else:
            state.spectator_enabled = 0
            print(state.spectator_enabled)
            
    def bomb_info_e(self):
        if self.bomb_checkbox.get() == 1:
            state.bomb_info_enabled = 1
        else:
            state.bomb_info_enabled = 0
            
    def crosshair_e(self):
        if self.crosshair_checkbox.get() == 1:
            state.sniper_crosshair_enabled = 1
        else:
            state.sniper_crosshair_enabled = 0
    def recoil_e(self):
        if self.recoil_checkbox.get() == 1:
            state.recoil_crosshair_enabled = 1
        else:
            state.recoil_crosshair_enabled = 0

class create_players(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color=app_colors['players']['bg_clr'])
        
        # header btns 
        # colors
        self.header_btn_fg_color = app_colors['players']['header_btn']['bg_clr']
        self.header_btn_selected = app_colors['players']['header_btn']['selected']
        self.header_btn_unselected = app_colors['players']['header_btn']['unselected']
        self.header_btn_hover_clr = app_colors['players']['header_btn']['hover']
        # Dimensions
        self.header_btn_height = 30
        self.header_btn_border_width = 1
        self.header_btn_corner_radius = 5
        # Grid
        self.header_btn_pady = 5
        self.header_btn_padx = 10
        self.header_btn_sticky = 'news'
        
        # Container frame
        # Colors
        self.frame_fg_color = app_colors['players']['container']['bg_clr']
        self.frame_border_color = app_colors['players']['container']['border_clr']
        # Dimensions
        self.frame_corner_radius = 5
        self.frame_border_width = 1
        # Grid
        self.frame_pady = 10
        self.frame_padx = 10
        self.frame_sticky = 'news'
        # header text
        self.frame_header_text_fg_color = app_colors['players']['container']['header_text']['bg_clr']
        self.frame_header_text_f_size = app_colors['players']['container']['header_text']['f_size']
        self.frame_header_text_f_weight = app_colors['players']['container']['header_text']['f_weight']
        # header grid
        self.frame_header_text_pady = 5
        self.frame_header_text_padx = 5
        self.frame_header_text_sticky = 'ew'
        # Main content
        self.frame_content_t_color = app_colors['players']['container']['content']['t_clr']
        self.frame_content_ct_color = app_colors['players']['container']['content']['ct_clr']
        self.frame_content_spectator_color = app_colors['players']['container']['content']['spec_clr']
        self.frame_content_bot_color = app_colors['players']['container']['content']['bot_clr']
        self.frame_content_fg_color = app_colors['players']['container']['content']['bg_clr']
        # Dimensions
        self.frame_content_rank_img_size = (60, 25)
        self.frame_content_faceit_img_size = (35, 35)
        # Grid
        self.frame_content_fg_pady = 4
        self.frame_content_fg_sticky = 'news'
        
        self.grid_columnconfigure(0, weight=1) # Make the first column width 100%
        self.grid_rowconfigure(1, weight=1)
        
        self.player_header_btn_general = ct.CTkSegmentedButton(self, values=["Main", "Advanced", "Stats"], height=self.header_btn_height, fg_color=self.header_btn_fg_color, border_width=self.header_btn_border_width, corner_radius=self.header_btn_corner_radius, unselected_color=self.header_btn_unselected, selected_color=self.header_btn_selected, selected_hover_color=self.header_btn_selected, unselected_hover_color=self.header_btn_hover_clr, command=self.player_header_btn_e)
        self.player_header_btn_general.grid(row=0, column=0, pady=self.header_btn_pady, padx=self.header_btn_padx, sticky=self.header_btn_sticky)
        
    def player_header_btn_e(self, e):
        if e == 'Main':
            self.player_main_container = ct.CTkScrollableFrame(self, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
            self.player_main_container.grid_columnconfigure((0,1,2,3), weight=1) # Push header items right and left

            # Create container header text
            self.header_name = self.create_headar_text('NAME', 0)
            self.header_rank = self.create_headar_text('RANK', 1)
            self.header_wins = self.create_headar_text('WINS', 2)
            self.header_faceit = self.create_headar_text('FACEIT', 3)
            
            getPlayerInfo() # Get and update array of data
            
            self.name_list = [0,1] # start from 3rd row
            self.rank_list = [0,1]
            self.wins_list = [0,1]
            self.faceit_list = [0,1]    

            sort_players_info = lambda arr_item: (arr_item[2]) # Create a function that will sort the item 2 which is teams in order
            sorted_players_info = sorted(playersInfo, key=sort_players_info) # Create our shadow copy of the main array and use this sorted array
        
            for i in range(0,len(sorted_players_info)): # For each element in playersInfo
                # [0] = Player ID - [1] = Player name - [2] = Player team - [3] = Player rank - [4] = Player wins - [5] = Player steam ID
                self.add_player_names(self.player_main_container, sorted_players_info[i][1], sorted_players_info[i][2], sorted_players_info[i][5])
                self.add_player_rank(self.player_main_container, sorted_players_info[i][3])
                self.add_player_wins(sorted_players_info[i][4])
                self.add_player_faceit(self.player_main_container, sorted_players_info[i][5])
                self.player_main_container.update()
            
            self.player_main_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.player_main_container.grid_forget()
            
    def create_headar_text(self, text, column):
        header_text = ct.CTkLabel(self.player_main_container, text=text, fg_color=self.frame_header_text_fg_color, font=ct.CTkFont(size= self.frame_header_text_f_size, weight=self.frame_header_text_f_weight), corner_radius=0,)
        header_text.grid(row=1, column=column, pady=self.frame_header_text_pady, padx=self.frame_header_text_padx, sticky=self.frame_header_text_sticky)
        
    def add_player_names(self, container, text, team, steam_ID):
        if team == 2: # T
            name_text_color = self.frame_content_t_color
        elif team == 3: # CT
            name_text_color = self.frame_content_ct_color
        else: # Spectators
            name_text_color = self.frame_content_spectator_color
        
        if steam_ID == 'BOT': # If player is a bot
            name = ct.CTkButton(container, text=text, fg_color=self.frame_content_fg_color, hover_color=self.frame_content_fg_color, text_color=self.frame_content_bot_color)
        else:
            name = ct.CTkButton(container, text=text, fg_color=self.frame_content_fg_color, hover_color=self.frame_content_fg_color, text_color=name_text_color, command=lambda: self.player_names_e(steam_ID)) # Anonymous in-line function to pass steam_ID to player_names_e

        name.grid(row=len(self.name_list), column=0, pady=self.frame_content_fg_pady, sticky=self.frame_content_fg_sticky)        
        self.name_list.append(name)
    
    def player_names_e(self, steam_ID):
        web.open(f'https://steamcommunity.com/profiles/{steam_ID}', new=2)
        
    def add_player_rank(self, container, rank_num):
        rank_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/Ranks")
        rank_show = rank_num
        
        if rank_num != 0 and rank_num > 18:
            rank_show = 0
            
        rank_img = ct.CTkImage(Image.open(os.path.join(rank_path, f'{rank_num}.png')), size=self.frame_content_rank_img_size) # Dynamically getting correct rank image depending on rank
        rank = ct.CTkButton(container, text='', image = rank_img, fg_color=self.frame_content_fg_color, hover_color=self.frame_content_fg_color, state="disabled", corner_radius=0, border_spacing=0)
        rank.grid(row=len(self.rank_list), column=1, pady=self.frame_content_fg_pady, sticky=self.frame_content_fg_sticky)
        self.rank_list.append(rank)

    def add_player_wins(self, text):
        wins = ct.CTkLabel(self.player_main_container, text=text)
        wins.grid(row=len(self.wins_list), column=2, pady=self.frame_content_fg_pady, sticky=self.frame_content_fg_sticky)
        self.wins_list.append(wins)
        
    def add_player_faceit(self, container, steam_ID):
        faceit_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/Faceit")
        
        faceit_lvl = '0'
        
        faceit_url = f'https://api.faceit.com/search/v1/?query={steam_ID}' # get Json faceit data
        faceit_json = requests.get(faceit_url).json()
        if len(faceit_json["payload"]['players']['results']) > 0: # Checking if player has faceit acc
            if len(faceit_json["payload"]['players']['results'][0]['games']) > 0: # Checking if player has any game on faceit acc
                game = faceit_json["payload"]['players']['results'][0]['games']
                for games in game:
                    if games['name'] == 'csgo':
                        faceit_lvl = games['skill_level']
        faceit_lvl_img = ct.CTkImage(Image.open(os.path.join(faceit_path, f'{faceit_lvl}.png')), size=self.frame_content_faceit_img_size) # Dynamically getting correct rank image depending on rank
        faceit = ct.CTkButton(container, text='', fg_color=self.frame_content_fg_color, hover_color=self.frame_content_fg_color, command=lambda: self.player_faceit_e(steam_ID, faceit_lvl), image=faceit_lvl_img, corner_radius=0, border_spacing=0)
        faceit.grid(row=len(self.faceit_list), column=3, pady=self.frame_content_fg_pady, sticky=self.frame_content_fg_sticky)     
        self.faceit_list.append(faceit)
            
    def player_faceit_e(self, steam_ID, faceit_lvl):
        if steam_ID == 'BOT' or faceit_lvl == 0:
            pass
        else:
            web.open(f'https://www.faceitfinder.app/user?id={steam_ID}', new=2)
         
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
        self.title("test2") # Random name window to change signatures?
        
        w = 1000 # apps width
        h = 600 # apps height

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the CTk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.minsize(width = 1000, height = 600) # Minimum size of the window
        
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


if __name__ == "__main__":
    app = App()
    app.iconbitmap("assets/GUI/icon.ico")
    app.mainloop()