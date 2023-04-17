import os, requests
import customtkinter as ct
import configparser as cp
import webbrowser as web
from CTkColorPicker import AskColor
from PIL import Image
from engine.gui_communication import *
from tools.entity_parse import getPlayerInfo, playersInfo

ct.set_appearance_mode("Dark")
ct.set_default_color_theme("dark-blue")

# sticky = N = north E = East W = west S = south

app_colors = {
    'app': {
        'bg_clr': '#1a1a1a',
        'frame_bg_clr': '#202020',
        'border_clr': '#4a4a4a',
    },
    'nav': {
        'bg_clr': 'transparent'
    },
    'header_btn': {
        'bg_clr': '#4a4a4a',
        'selected': '#39314A',
        'unselected': '#202020',
        'hover': '#282828' # Add border color too
    },
    'visuals': {
        'bg_clr': '#1a1a1a',
    },
    'players': {
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
    },
}

THEME_CFG = 'config/theme.ini'
if not os.path.exists(THEME_CFG):
    theme_cfg = cp.ConfigParser()
    
    theme_cfg["APP"] = {
        'bg_clr': '#1a1a1a',
        'bg_clr_accent': '#212121',
    }
    
    with open(THEME_CFG, 'w') as f:
        theme_cfg.write(f)
else:
    theme_cfg = cp.ConfigParser()
    theme_cfg.read(THEME_CFG)



CONFIG_FILE = 'config/default.ini'
if not os.path.exists(CONFIG_FILE):
    # If the configuration file doesn't exist, create it with default values
    config = cp.ConfigParser()
    
    config["VISUALS"] = {
        'enabled': 1,
        'watermark': 1,
        'box': 1,
        'head esp': 1,
        'health': 1,
        'name': 1,
        'weapon': 1,
        'sniper crosshair': 1,
        'recoil crosshair': 1,
        'spectator list': 1,
        'bomb info': 1,
    }
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
else:
    # If the configuration file exists, read the values from it
    config = cp.ConfigParser()
    config.read(CONFIG_FILE)

def create_nav(parent, aim_callback, trigger_callback, visuals_callback, players_callback, misc_callback, panel_callback, settings_callback):
    frame = ct.CTkFrame(master = parent, corner_radius=0)
        
    height = 60
    border_spacing = 10
    corner_radius = 0
    fg_color = theme_cfg["APP"]['bg_clr_accent']
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
        super().__init__(master = parent, fg_color=app_colors['app']['bg_clr'])
        # header btns 
        # colors
        self.header_btn_fg_color = app_colors['header_btn']['bg_clr']
        self.header_btn_selected = app_colors['header_btn']['selected']
        self.header_btn_unselected = app_colors['header_btn']['unselected']
        self.header_btn_hover_clr = app_colors['header_btn']['hover']
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
        self.frame_fg_color = app_colors['app']['frame_bg_clr']
        self.frame_border_color = app_colors['app']['border_clr']
        # Dimensions
        self.frame_corner_radius = 5
        self.frame_border_width = 1
        # Grid
        self.frame_pady = 10
        self.frame_padx = 10
        self.frame_sticky = 'w'

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
        
        self.header_btn = ct.CTkSegmentedButton(self, values=["Global", "Player", "Local", "Other"], height=self.header_btn_height, fg_color=self.header_btn_fg_color, border_width=self.header_btn_border_width, corner_radius=self.header_btn_corner_radius, unselected_color=self.header_btn_unselected, selected_color=self.header_btn_selected, selected_hover_color=self.header_btn_selected, unselected_hover_color=self.header_btn_hover_clr, command=self.header_btn_e)
        self.header_btn.grid(row=0, column=0, pady=self.header_btn_pady, padx=self.header_btn_padx, sticky=self.header_btn_sticky)
        
        self.global_container = ct.CTkFrame(self, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.global_container.grid_columnconfigure(1, pad=25)
        self.global_container.grid_columnconfigure(2, pad=25)
        
        self.global_master = self.item_checkbox(self.global_container, 0, 1, 'Enable', self.global_master_e)
        
        self.global_watermark = self.item_checkbox(self.global_container, 1, 1, 'Watermark', self.global_watermark_e)
        self.watermark_color = self.color_picker(self.global_container, 1, 2, self.watermark_color_e)
        
        self.player_container = ct.CTkFrame(self, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.player_container.grid_columnconfigure(1, pad=25)
        self.player_container.grid_columnconfigure(2, pad=25)
        
        self.player_box_esp_name = self.item_checkbox(self.player_container, 1, 0, 'Box', self.player_box_esp_name_e)
        self.player_box_esp = self.item_comboBox(self.player_container, 1, 1, ['Normal', 'Filled'])
        # player_box_esp_color =
        
        self.player_head_esp_name = self.item_checkbox(self.player_container, 3, 0, 'Head ESP', self.player_head_esp_name_e)
        self.player_head_esp = self.item_comboBox(self.player_container, 3, 1, ['Circle'])
        
        self.player_health_esp_name = self.item_checkbox(self.player_container, 4, 0, 'Health', self.player_health_esp_name_e)
        self.player_health_esp = self.item_comboBox(self.player_container, 4, 1, ['Simple', 'Advanced'])
        
        self.player_name_esp_name = self.item_checkbox(self.player_container, 5, 0, 'Name', self.player_name_esp_name_e)
        
        self.player_weapon_esp_name = self.item_checkbox(self.player_container, 6, 0, 'Weapon', self.player_weapon_esp_name_e)
        self.player_weapon_esp = self.item_comboBox(self.player_container, 6, 1, ['Text', 'Icon'])
        
        self.local_container = ct.CTkFrame(self, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.local_container.grid_columnconfigure(1, pad=25)
        self.local_container.grid_columnconfigure(2, pad=25)
        
        self.local_crosshair_name = self.item_checkbox(self.local_container, 1, 0, 'Sniper Crosshair', self.local_crosshair_name_e)
        self.local_crosshair = self.item_comboBox(self.local_container, 1, 1, ['Cross'])
        
        self.local_recoil_name = self.item_checkbox(self.local_container, 2, 0, 'Recoil Crosshair', self.local_recoil_name_e)
        self.local_recoil = self.item_comboBox(self.local_container, 2, 1, ['Cross'])
        
        self.local_spectator_name = self.item_checkbox(self.local_container, 3, 0, 'Spectator List', self.local_spectator_name_e)
        
        self.other_container = ct.CTkFrame(self, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.other_container.grid_columnconfigure(1, pad=25)
        self.other_container.grid_columnconfigure(2, pad=25)
        
        self.other_bomb_info_name = self.item_checkbox(self.other_container, 1, 0, 'Bomb Info', self.other_bomb_info_name_e)
        
        # Reading our config file 
        self.config = cp.ConfigParser()
        self.config.read(CONFIG_FILE)
        # Calling our update function once when the app is loaded
        self.update_from_config()
        
    def header_btn_e(self, e):
        if e == 'Global':
            self.global_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.global_container.grid_forget()
        if e == 'Player':
            self.player_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.player_container.grid_forget()
        if e == 'Local':
            self.local_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.local_container.grid_forget()
        if e == 'Other':
            self.other_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.other_container.grid_forget()

    def item_checkbox(self, container, row, column, text, callback):
        checkbox = ct.CTkCheckBox(container, text=text, checkbox_width=25, checkbox_height=25, corner_radius=5, border_width=1, border_color='#4a4a4a', hover_color='#30293D', checkmark_color='white', fg_color='#39314A', font=ct.CTkFont(size=13), command=callback)
        checkbox.grid(row=row, column=column, pady=10, padx=10, sticky='w')
            
        return checkbox
    
    def item_comboBox(self, container, row, column, text):
        comboBox = ct.CTkComboBox(container, values=text, border_width=1, border_color='#4a4a4a' ,corner_radius=5, fg_color='#202020', width=111, height=25, button_color='#39314A', button_hover_color='#30293D', dropdown_fg_color='#202020', dropdown_hover_color='#1C1C1C', dropdown_font=ct.CTkFont(size=14))
        
        comboBox.grid(row=row, column=column, pady=10, padx=10, sticky='w')
    
    def color_picker(self, container, row, column, callback):
        button = ct.CTkButton(container, text='', corner_radius=5, width=25, height=25, command=callback, fg_color='white')
        button.grid(row=row, column=column, pady=10, padx=10)
            
    def update_from_config(self):
        self.config.read(CONFIG_FILE)
        if self.config['VISUALS']['enabled'] == '1':
            self.global_master.select()
            self.global_master_e()
        else:
            self.global_master.deselect()
            self.global_master_e()
            
        if self.config['VISUALS']['watermark'] == '1':
            self.global_watermark.select()
            self.global_watermark_e()
        else:
            self.global_watermark.deselect()
            self.global_watermark_e()
            
        if self.config['VISUALS']['box'] == '1':
            self.player_box_esp_name.select()
            self.player_box_esp_name_e()
        else:
            self.player_box_esp_name.deselect()
            self.player_box_esp_name_e()
            
        if self.config['VISUALS']['head esp'] == '1':
            self.player_head_esp_name.select()
            self.player_head_esp_name_e()
        else:
            self.player_head_esp_name.deselect()
            self.player_head_esp_name_e()
    
        if self.config['VISUALS']['health'] == '1':
            self.player_health_esp_name.select()
            self.player_health_esp_name_e()
        else:
            self.player_health_esp_name.deselect()
            self.player_health_esp_name_e()
            
        if self.config['VISUALS']['name'] == '1':
            self.player_name_esp_name.select()
            self.player_name_esp_name_e()
        else:
            self.player_name_esp_name.deselect()
            self.player_name_esp_name_e()
            
        if self.config['VISUALS']['weapon'] == '1':
            self.player_weapon_esp_name.select()
            self.player_weapon_esp_name_e()
        else:
            self.player_weapon_esp_name.deselect()
            self.player_weapon_esp_name_e()
        
        if self.config['VISUALS']['sniper crosshair'] == '1':
            self.local_crosshair_name.select()
            self.local_crosshair_name_e()
        else:
            self.local_crosshair_name.deselect()
            self.local_crosshair_name_e()
            
        if self.config['VISUALS']['recoil crosshair'] == '1':
            self.local_recoil_name.select()
            self.local_recoil_name_e()
        else:
            self.local_recoil_name.deselect()
            self.local_recoil_name_e()
            
        if self.config['VISUALS']['spectator list'] == '1':
            self.local_spectator_name.select()
            self.local_spectator_name_e()
        else:
            self.local_spectator_name.deselect()
            self.local_spectator_name_e()
            
        if self.config['VISUALS']['bomb info'] == '1':
            self.other_bomb_info_name.select()
            self.other_bomb_info_name_e()
        else:
            self.other_bomb_info_name.deselect()
            self.other_bomb_info_name_e()
    
    def global_master_e(self):
        if self.global_master.get() == 1:
            state.master_switch = 1
        else:
            state.master_switch = 0
            
    def global_watermark_e(self):
        if self.global_watermark.get() == 1:
            state.watermark = 1
        else:
            state.watermark = 0
    
    def watermark_color_e(self):
        pick_color = AskColor()
        color = pick_color.get()
        colors.watermark = f'{color}'
            
    def player_box_esp_name_e(self):
        if self.player_box_esp_name.get() == 1:
            state.players_box_enabled = 1
        else:
            state.players_box_enabled = 0
            
    def player_head_esp_name_e(self):
        if self.player_head_esp_name.get() == 1:
            state.players_head_enabled = 1
        else:
            state.players_head_enabled = 0
            
    def player_health_esp_name_e(self):
        if self.player_health_esp_name.get() == 1:
            state.players_health_enabled = 1
        else:
            state.players_health_enabled = 0
            
    def player_name_esp_name_e(self):
        if self.player_name_esp_name.get() == 1:
            state.players_names_enabled = 1
        else:
            state.players_names_enabled = 0
            
    def player_weapon_esp_name_e(self):
        if self.player_weapon_esp_name.get() == 1:
            state.players_weapon = 1
        else:
            state.players_weapon = 0
            
    def local_crosshair_name_e(self):
        if self.local_crosshair_name.get() == 1:
            state.sniper_crosshair_enabled = 1
        else:
            state.sniper_crosshair_enabled = 0
            
    def local_recoil_name_e(self):
        if self.local_recoil_name.get() == 1:
            state.recoil_crosshair_enabled = 1
        else:
            state.recoil_crosshair_enabled = 0
            
    def local_spectator_name_e(self):
        if self.local_spectator_name.get() == 1:
            state.spectator_enabled = 1
        else:
            state.spectator_enabled = 0
            
    def other_bomb_info_name_e(self):
        if self.other_bomb_info_name.get() == 1:
            state.bomb_info_enabled = 1
        else:
            state.bomb_info_enabled = 0
            
    def config_return(self):
        return self.global_master.get()
              
class create_players(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color=app_colors['app']['bg_clr'], corner_radius=10)
        
        # header btns 
        # colors
        self.header_btn_fg_color = app_colors['header_btn']['bg_clr']
        self.header_btn_selected = app_colors['header_btn']['selected']
        self.header_btn_unselected = app_colors['header_btn']['unselected']
        self.header_btn_hover_clr = app_colors['header_btn']['hover']
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
        
        self.player_header_btn_general = ct.CTkSegmentedButton(self, values=["Main", "-"], height=self.header_btn_height, fg_color=self.header_btn_fg_color, border_width=self.header_btn_border_width, corner_radius=self.header_btn_corner_radius, unselected_color=self.header_btn_unselected, selected_color=self.header_btn_selected, selected_hover_color=self.header_btn_selected, unselected_hover_color=self.header_btn_hover_clr, command=self.player_header_btn_e)
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
                self.add_player_ranks(self.player_main_container, sorted_players_info[i][3], sorted_players_info[i][5])
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
        
    def add_player_ranks(self, container, rank_num, steam_ID):
        rank_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/Ranks")
        rank_show = rank_num
        
        if rank_num != 0 and rank_num > 18:
            rank_show = 0
            
        rank_img = ct.CTkImage(Image.open(os.path.join(rank_path, f'{rank_show}.png')), size=self.frame_content_rank_img_size) # Dynamically getting correct rank image depending on rank
        rank = ct.CTkButton(container, text='', image = rank_img, fg_color=self.frame_content_fg_color, hover_color=self.frame_content_fg_color, command= lambda: self.player_ranks_e(steam_ID), corner_radius=0, border_spacing=0)
        rank.grid(row=len(self.rank_list), column=1, pady=self.frame_content_fg_pady, sticky=self.frame_content_fg_sticky)
        self.rank_list.append(rank)

    def player_ranks_e(self, steam_ID):
        if not steam_ID == 'BOT':
            web.open(f'https://csgostats.gg/player/{steam_ID}', new=2)
    
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
        faceit = ct.CTkButton(container, text='', fg_color=self.frame_content_fg_color, hover_color=self.frame_content_fg_color, command=lambda: self.player_faceit_e(steam_ID, int(faceit_lvl)), image=faceit_lvl_img, corner_radius=0, border_spacing=0)
        faceit.grid(row=len(self.faceit_list), column=3, pady=self.frame_content_fg_pady, sticky=self.frame_content_fg_sticky)     
        self.faceit_list.append(faceit)
            
    def player_faceit_e(self, steam_ID, faceit_lvl):
        print(type(faceit_lvl))
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

class create_settings(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color=app_colors['app']['bg_clr'])
        
        # header btns 
        # colors
        self.header_btn_fg_color = app_colors['header_btn']['bg_clr']
        self.header_btn_selected = app_colors['header_btn']['selected']
        self.header_btn_unselected = app_colors['header_btn']['unselected']
        self.header_btn_hover_clr = app_colors['header_btn']['hover']
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
        self.frame_fg_color = app_colors['app']['frame_bg_clr']
        self.frame_border_color = app_colors['app']['border_clr']
        # Dimensions
        self.frame_corner_radius = 5
        self.frame_border_width = 1
        # Grid
        self.frame_pady = 10
        self.frame_padx = 10
        self.frame_sticky = 'w'

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
        
        self.header_btn = ct.CTkSegmentedButton(self, values=["Config", "-"], height=self.header_btn_height, fg_color=self.header_btn_fg_color, border_width=self.header_btn_border_width, corner_radius=self.header_btn_corner_radius, unselected_color=self.header_btn_unselected, selected_color=self.header_btn_selected, selected_hover_color=self.header_btn_selected, unselected_hover_color=self.header_btn_hover_clr, command=self.header_btn_e)
        self.header_btn.grid(row=0, column=0, pady=self.header_btn_pady, padx=self.header_btn_padx, sticky=self.header_btn_sticky)
        
        
        self.config_container = ct.CTkFrame(self, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.config_container.grid_columnconfigure(1, pad=25)
        self.config_container.grid_columnconfigure(2, pad=25)
    
    def header_btn_e(self, e):
        if e == 'Config':
            self.config_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.config_container.grid_forget()

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
        
        # Reading our config file
        self.config = cp.ConfigParser()
        self.config.read(CONFIG_FILE)
        
        # Create buttons inside settings_tab
        self.load_config_btn = ct.CTkButton(self.settinsg_tab.config_container, text='load', command=self.load_config_btn_e)
        self.load_config_btn.grid(row=1, column=0, pady=10, padx=10)
        
        self.save_config_btn = ct.CTkButton(self.settinsg_tab.config_container, text='save', command=self.save_config_btn_e)
        self.save_config_btn.grid(row=1, column=1, pady=10, padx=10)
    
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

    def load_config_btn_e(self):
        self.config.read(CONFIG_FILE)
        self.visuals_tab.update_from_config()

    # Make our function to save config. This is done here because the App can communicate with other classes
    def save_config_btn_e(self):
        self.config['VISUALS']['enabled'] = f'{self.visuals_tab.global_master.get()}'
        
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)
        
if __name__ == "__main__":
    app = App()
    app.iconbitmap("assets/GUI/icon.ico")
    app.mainloop()
