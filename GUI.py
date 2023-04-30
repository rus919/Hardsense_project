import os, sys, requests
import customtkinter as ct
import configparser as cp
import webbrowser as web
from PIL import Image
from engine.gui_communication import app_state, state, item_clr, trigger_state
from tools.entity_parse import getPlayerInfo, playersInfo

ct.set_appearance_mode("Dark")
ct.set_default_color_theme("dark-blue")

# sticky = N = north E = East W = west S = south

# def resource_path(relative_path):
#     base_path = getattr(
#         sys,
#         '_MEIPASS',
#         os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

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

if not os.path.exists('config'):
    os.makedirs('config')

THEME_CFG = 'config/theme.ini'
if not os.path.exists(THEME_CFG):
    theme_cfg = cp.ConfigParser()

    theme_cfg["APP"] = {
        'bg_clr': '#1a1a1a',
        'bg_clr_accent': '#212121',
        'border_clr': '#4a4a4a',
        'nav_text_clr': '#c1c1c1',
        'nav_hover_clr': '#1a1a1a',
        'header_btn_clr': '#4a4a4a',
        'header_btn_selected_clr': '#39314A',
        'header_btn_unselected_clr': '#202020',
        'header_btn_hover_clr': '#282828',
        'checkbox_border': '#4a4a4a',
        'checkbox_hover': '#30293D',
        'checkbox_checkmark_clr': '#fff',
        'checkbox_fg_clr': '#39314A',
        'checkbox_font_sz': '13',
        'combobox_fg_clr': '#202020',
        'combobox_border_clr': '#4a4a4a',
        'combobox_button_clr': '#39314A',
        'combobox_button_hover_clr': '#30293D',
        'combobox_dropdown_fg_clr': '#202020',
        'combobox_dropdown_hover_clr': '#1C1C1C',
        'combobox_font_sz': '13',
        
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
    
    config["VISUALS GLOBAL"] = {
        'enabled': 1,
        'watermark': 1,
        'watermark clr': [255,255,255,255],
    }
    
    config["VISUALS PLAYER"] = {
        'box': 0,
        'box type': 'normal',
        'box clr': [255,255,255,255],
        'head esp': 1,
        'head esp type': 'circle',
        'head esp clr': [255,255,255,255],
        'health': 1,
        'health type': 'icon',
        'health clr': [255,255,255,255],
        'name': 1,
        'name clr': [255,255,255,255],
        'weapon': 1,
        'weapon type': 'icon',
        'weapon clr': [255,255,255,255],
        'sniper crosshair': 1,
        'sniper crosshair type': 'cross',
        'sniper crosshair clr': [255,255,255,255],
        'recoil crosshair': 1,
        'recoil crosshair type': 'cross',
        'recoil crosshair clr': [255,255,255,255],
        'spectator list': 1,
        'spectator list clr': [255,255,255,255],
        'bomb info': 1,
    }
    
    config['TRIGGERBOT'] = {
        'enabled': 1,
        'key': 5,
        'advanced': 1,
    }

    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
else:
    # If the configuration file exists, read the values from it
    config = cp.ConfigParser()
    config.read(CONFIG_FILE)

keys_list = {
    'Mouse 3': 0x04,
    'Mouse 4': 0x05,
    'Mouse 5': 0x06,
    'SHIFT': 0x10,
    'CTRL': 0x11,
    'ALT': 0x12,
    'C': 0x43, 
    'T': 0x54, 
    'V': 0x56, 
    'X': 0x58, 
    'Z': 0x5A, 
}

# load guns images which i will use in different classes
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/images")
pistols_img = ct.CTkImage(Image.open(os.path.join(image_path, "4.png")), size=(20, 15))
smg_img = ct.CTkImage(Image.open(os.path.join(image_path, "19.png")), size=(35, 15))
heavy_img = ct.CTkImage(Image.open(os.path.join(image_path, "28.png")), size=(40, 15))
rifles_img = ct.CTkImage(Image.open(os.path.join(image_path, "7.png")), size=(40, 12))
snipers_img = ct.CTkImage(Image.open(os.path.join(image_path, "9.png")), size=(40, 11))
zeus_img = ct.CTkImage(Image.open(os.path.join(image_path, "31.png")), size=(20, 15))

glock_img = ct.CTkImage(Image.open(os.path.join(image_path, "4.png")), size=(20, 15))
usp_s_img = ct.CTkImage(Image.open(os.path.join(image_path, "61.png")), size=(30, 15))
p2000_img = ct.CTkImage(Image.open(os.path.join(image_path, "32.png")), size=(20, 15))
dual_berettas_img = ct.CTkImage(Image.open(os.path.join(image_path, "2.png")), size=(30, 15))
p250_img = ct.CTkImage(Image.open(os.path.join(image_path, "36.png")), size=(20, 15))
five_seven_img = ct.CTkImage(Image.open(os.path.join(image_path, "3.png")), size=(20, 15))
tec_9_img = ct.CTkImage(Image.open(os.path.join(image_path, "30.png")), size=(20, 15))
cz75_img = ct.CTkImage(Image.open(os.path.join(image_path, "63.png")), size=(20, 15))
deagle_img = ct.CTkImage(Image.open(os.path.join(image_path, "1.png")), size=(20, 15))
nova_img = ct.CTkImage(Image.open(os.path.join(image_path, "35.png")), size=(30, 13))
xm1014_img = ct.CTkImage(Image.open(os.path.join(image_path, "25.png")), size=(30, 13))
mag_7_img = ct.CTkImage(Image.open(os.path.join(image_path, "27.png")), size=(25, 15))
sawed_off_img = ct.CTkImage(Image.open(os.path.join(image_path, "29.png")), size=(30, 13))
m249_img = ct.CTkImage(Image.open(os.path.join(image_path, "14.png")), size=(30, 15))
negev_img = ct.CTkImage(Image.open(os.path.join(image_path, "28.png")), size=(30, 15))
mp9_img = ct.CTkImage(Image.open(os.path.join(image_path, "34.png")), size=(30, 15))
mac_10_img = ct.CTkImage(Image.open(os.path.join(image_path, "17.png")), size=(20, 15))
mp5_img = ct.CTkImage(Image.open(os.path.join(image_path, "23.png")), size=(30, 15))
mp7_img = ct.CTkImage(Image.open(os.path.join(image_path, "33.png")), size=(20, 15))
ump_img = ct.CTkImage(Image.open(os.path.join(image_path, "24.png")), size=(30, 15))
p90_img = ct.CTkImage(Image.open(os.path.join(image_path, "19.png")), size=(30, 15))
bizon_img = ct.CTkImage(Image.open(os.path.join(image_path, "26.png")), size=(30, 15))
famas_img = ct.CTkImage(Image.open(os.path.join(image_path, "10.png")), size=(20, 15))
galil_img = ct.CTkImage(Image.open(os.path.join(image_path, "13.png")), size=(20, 15))
m4a4_img = ct.CTkImage(Image.open(os.path.join(image_path, "16.png")), size=(20, 15))
m4a1_s_img = ct.CTkImage(Image.open(os.path.join(image_path, "60.png")), size=(20, 15))
ak_47_img = ct.CTkImage(Image.open(os.path.join(image_path, "7.png")), size=(20, 15))
ssg_img = ct.CTkImage(Image.open(os.path.join(image_path, "40.png")), size=(20, 15))
sg553_img = ct.CTkImage(Image.open(os.path.join(image_path, "39.png")), size=(20, 15))
aug_img = ct.CTkImage(Image.open(os.path.join(image_path, "8.png")), size=(20, 15))
awp_img = ct.CTkImage(Image.open(os.path.join(image_path, "9.png")), size=(20, 15))
scar_img = ct.CTkImage(Image.open(os.path.join(image_path, "38.png")), size=(20, 15))
g3sg1_img = ct.CTkImage(Image.open(os.path.join(image_path, "11.png")), size=(20, 15))

def key_handler(key: str) -> int:
    return keys_list.get(key)

class app_config:
    fg_color = theme_cfg["APP"]['bg_clr_accent']
    
    nav_text_color = theme_cfg["APP"]['nav_text_clr']
    nav_hover_color = theme_cfg["APP"]['nav_hover_clr']
    
    header_btn_fg_color = theme_cfg["APP"]['header_btn_clr']
    header_btn_selected = theme_cfg["APP"]['header_btn_selected_clr']
    header_btn_unselected = theme_cfg["APP"]['header_btn_unselected_clr']
    header_btn_hover_clr = theme_cfg["APP"]['header_btn_hover_clr']

def header_btn(self, row, column, values, callback):
    
    self.header_btn = ct.CTkSegmentedButton(
        self, 
        values = values, 
        height = 30,
        fg_color =app_config.header_btn_fg_color, 
        border_width = 1, 
        corner_radius = 5, 
        unselected_color = app_config.header_btn_unselected, 
        selected_color = app_config.header_btn_selected, 
        selected_hover_color = app_config.header_btn_selected, 
        unselected_hover_color = app_config.header_btn_hover_clr, 
        command = callback
    )
    
    self.header_btn.grid(row = row, column = column, pady = 5, padx = 10, sticky = 'news')
    return header_btn

def create_nav(parent, aim_callback, trigger_callback, visuals_callback, players_callback, misc_callback, panel_callback, settings_callback):
    frame = ct.CTkFrame(master = parent, corner_radius=0)
        
    height = 60
    border_spacing = 10
    corner_radius = 0
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

    nav_aimbot = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Aimbot", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor, image = aimbot_img, command = aim_callback).grid(row=1, column=0, sticky= sticky)
    nav_trigger = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Triggerbot", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor,image = trigger_img, command = trigger_callback).grid(row=2, column=0, sticky = sticky)
    nav_visuals = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Visuals", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor,image = visuals_img, command = visuals_callback).grid(row=3, column=0, sticky = sticky)
    nav_players = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Players", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor,image = players_img, command = players_callback)
    nav_players.grid(row=4, column=0, sticky = sticky)
    nav_misc = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Misc", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor,image = misc_img, command = misc_callback).grid(row=5, column=0, sticky = sticky)
    nav_user = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="User Panel", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor,image = user_img, command = panel_callback).grid(row=7, column=0, sticky = sticky)
    nav_settings = ct.CTkButton(frame, corner_radius = corner_radius, height = height, border_spacing = border_spacing, text="Settings", fg_color = app_config.fg_color, text_color = app_config.nav_text_color, hover_color = app_config.nav_hover_color, anchor = anchor,image = settings_img, command = settings_callback).grid(row=8, column=0, sticky = sticky)
    
    return frame

def create_aimbot(parent):
    frame = ct.CTkFrame(master = parent, corner_radius=0, fg_color='transparent')
        
    test = ct.CTkLabel(frame, text="Aimbot", anchor="w")
    test.grid(row=0, column=0, pady=10, padx = 10)
    
    return frame

class create_triggerbot(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color=theme_cfg['APP']['bg_clr'])
        
        self.frame_fg_color = theme_cfg['APP']['bg_clr_accent']
        self.frame_border_color = theme_cfg['APP']['border_clr']
        self.frame_corner_radius = 5
        self.frame_border_width = 1
        self.frame_pady = 10
        self.frame_padx = 10
        self.frame_sticky = 'n'
        
        self.grid_columnconfigure(0, weight=1) # Make the first column width 100%
        self.grid_rowconfigure(1, weight=1) # Make the first column width 100%
        
        # Header btns
        self.header_btn = header_btn(self, 0, 0, ["Global", "Configure",], self.header_btn_e)
        
        # Create global frame to add items to
        self.global_frame = ct.CTkFrame(self, corner_radius=0, fg_color=app_colors['app']['bg_clr'])
        self.global_frame.grid(row=1, column=0, sticky='news')
        
        self.global_container = self.create_frame()
        self.configure_select_group_container = self.create_frame()
        
        self.configure_each_weapon_container_pistols = self.create_frame()
        self.configure_each_weapon_container_smg = self.create_frame()
        self.configure_each_weapon_container_heavy = self.create_frame()
        self.configure_each_weapon_container_rifles = self.create_frame()
        self.configure_each_weapon_container_snipers = self.create_frame()
        self.configure_each_weapon_container_other = self.create_frame()
        
        self.configure_each_weapon_container = self.create_frame()
        
        self.global_enabled = self.item_checkbox(self.global_container, 1, 1, 'Enabled', self.global_enabled_e)
        
        self.trigger_label = self.item_label(self.global_container, 2, 1, 'Trigger key')
        self.trigger_key = self.item_comboBox(self.global_container, 150, 2, 2, tuple(keys_list.keys()), self.trigger_key_e)
        
        self.pistols_trigger = self.weapon_btn(self.configure_select_group_container, 1, 0, 'Pistols', pistols_img, self.pistols_trigger_e)
        self.smg_trigger = self.weapon_btn(self.configure_select_group_container, 1, 1, 'SMG', smg_img, self.smg_trigger_e)
        self.heavy_trigger = self.weapon_btn(self.configure_select_group_container, 1, 2, 'Heavy', heavy_img, self.heavy_trigger_e)
        self.rifles_trigger = self.weapon_btn(self.configure_select_group_container, 1, 3, 'Rifles', rifles_img, self.rifles_trigger_e)
        self.snipers_trigger = self.weapon_btn(self.configure_select_group_container, 1, 4, 'Snipers', snipers_img, self.snipers_trigger_e)
        self.other_trigger = self.weapon_btn(self.configure_select_group_container, 1, 5, 'Other', zeus_img, self.other_trigger_e)
                
        self.config = cp.ConfigParser()
        self.update_from_config()
    
    def header_btn_e(self, e):
        if e == 'Global':
            self.global_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.global_container.grid_forget()
            
        if e == 'Configure':
            self.configure_select_group_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky='ew')
            self.global_frame.rowconfigure(3, weight=1)
        else:
            self.configure_select_group_container.grid_forget()
            self.configure_each_weapon_container_pistols.grid_forget()
            self.configure_each_weapon_container_smg.grid_forget()
            self.configure_each_weapon_container_heavy.grid_forget()
            self.configure_each_weapon_container_rifles.grid_forget()
            self.configure_each_weapon_container_snipers.grid_forget()
            self.configure_each_weapon_container_other.grid_forget()
            
            self.configure_each_weapon_container.grid_forget()
            
    def update_from_config(self):
        self.config.read(CONFIG_FILE)
        
        # Global Enable
        if self.config['TRIGGERBOT']['enabled'] == '1':
            self.global_enabled.select()
            self.global_enabled_e()
        else:
            self.global_enabled.deselect()
            self.global_enabled_e()
            
        # trigger key
        self.trigger_key.set(list(keys_list.keys())[list(keys_list.values()).index(int(self.config['TRIGGERBOT']['key']))]) # Get the value from dict and find the key it's attached to
        trigger_state.trigger_key = int(self.config['TRIGGERBOT']['key']) # Update our trigger key when loaded
            
    def create_frame(self):
        self.frame = ct.CTkFrame(self.global_frame, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        return self.frame
            
    def item_checkbox(self, container, row, column, text, callback):
        self.checkbox_fg_color = theme_cfg['APP']['checkbox_fg_clr']
        self.checkbox_border_color = theme_cfg['APP']['checkbox_border']
        self.checkbox_hover_color = theme_cfg['APP']['checkbox_hover']
        self.checkbox_checkmark_color = theme_cfg['APP']['checkbox_checkmark_clr']
        self.checkbox_font_size = theme_cfg['APP']['checkbox_font_sz']
        
        checkbox = ct.CTkCheckBox(container, text=text, checkbox_width=25, checkbox_height=25, corner_radius=5, border_width=1, border_color=self.checkbox_border_color, hover_color=self.checkbox_hover_color, checkmark_color=self.checkbox_checkmark_color, fg_color=self.checkbox_fg_color, font=ct.CTkFont(size=int(self.checkbox_font_size)), command=callback)
        checkbox.grid(row=row, column=column, pady=10, padx=10, sticky='w')
        return checkbox

    def item_comboBox(self, container, width, row, column, text, callback):
        self.combobox_fg_color = theme_cfg['APP']['combobox_fg_clr']
        self.combobox_border_color = theme_cfg['APP']['combobox_border_clr']
        self.combobox_button_color = theme_cfg['APP']['combobox_button_clr']
        self.combobox_button_hover_color = theme_cfg['APP']['combobox_button_hover_clr']
        self.combobox_dropdown_fg_color = theme_cfg['APP']['combobox_dropdown_fg_clr']
        self.combobox_dropdown_hover_color = theme_cfg['APP']['combobox_dropdown_hover_clr']
        self.combobox_font_size = theme_cfg['APP']['combobox_font_sz']
        
        comboBox = ct.CTkComboBox(container, values=text, border_width=1, border_color=self.combobox_border_color, corner_radius=5, fg_color=self.combobox_fg_color, width=width, height=25, button_color=self.combobox_button_color, button_hover_color=self.combobox_button_hover_color, dropdown_fg_color=self.combobox_dropdown_fg_color, dropdown_hover_color=self.combobox_dropdown_hover_color, dropdown_font=ct.CTkFont(size=int(self.combobox_font_size)), command=callback)
        comboBox.grid(row=row, column=column, pady=10, padx=10, sticky='w')
        return comboBox

    def item_label(self, container, row, column, text):
        label = ct.CTkLabel(container, text=text, font=ct.CTkFont(size=13))
        label.grid(row=row, column=column, pady=10, padx=40, sticky='w')
        return label

    def weapon_btn(self, container, row, column, text, image, callback, width=140, f_size=13):
        weapon_btn = ct.CTkButton(container, text=text, image=image, fg_color='transparent', height=36, border_color=theme_cfg['APP']['border_clr'], border_width=1, command=callback, width=width, font=ct.CTkFont(size=f_size))
        weapon_btn.grid(row=row, column=column, sticky='ew')
        return weapon_btn

    def global_enabled_e(self):
        if self.global_enabled.get() == 1:
            trigger_state.enabled = 1
        else:
            trigger_state.enabled = 0
    
    def trigger_key_e(self, e):
        print(e)
        trigger_state.trigger_key = key_handler(e)
        
    # Configure tab
    def test(self):
        print('hello')
        
    def pistols_trigger_e(self):
        self.configure_each_weapon_container_smg.grid_forget()
        self.configure_each_weapon_container_heavy.grid_forget()
        self.configure_each_weapon_container_rifles.grid_forget()
        self.configure_each_weapon_container_snipers.grid_forget()
        self.configure_each_weapon_container_other.grid_forget()
        
        self.configure_each_weapon_container_pistols.grid(row=2, column=0, pady=self.frame_pady, padx=self.frame_padx)

        self.glock = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 0, 'Glock', glock_img, self.glock_e, 92, 12)
        self.usp_s = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 1, 'Usp', usp_s_img, self.test, 92, 12)
        self.p2000 = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 2, 'P2000', p2000_img, self.test, 92, 12)
        self.dual_berettas = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 3, 'DB', dual_berettas_img, self.test, 92, 12)
        self.p250 = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 4, 'P250', p250_img, self.test, 92, 12)
        self.five_seven = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 5, 'FS', five_seven_img, self.test, 92, 12)
        self.tec_9 = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 6, 'Tec', tec_9_img, self.test, 92, 12)
        self.cz75 = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 7, 'Cz75', cz75_img, self.test, 92, 12)
        self.deagle = self.weapon_btn(self.configure_each_weapon_container_pistols, 1, 8, 'Deagle', deagle_img, self.test, 92, 12)
        
    def smg_trigger_e(self):
        self.configure_each_weapon_container_pistols.grid_forget()
        self.configure_each_weapon_container_heavy.grid_forget()
        self.configure_each_weapon_container_rifles.grid_forget()
        self.configure_each_weapon_container_snipers.grid_forget()
        self.configure_each_weapon_container_other.grid_forget()
        
        self.configure_each_weapon_container_smg.grid(row=2, column=0, pady=self.frame_pady, padx=self.frame_padx,)
        
        self.mp9 = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 0, 'Mp9', mp9_img, self.test, 118, 12)
        self.mac_10 = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 1, 'Mac', mac_10_img, self.test, 118, 12)
        self.mp5 = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 2, 'Mp5', mp5_img, self.test, 118, 12)
        self.mp7 = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 3, 'Mp7', mp7_img, self.test, 118, 12)
        self.ump = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 4, 'Ump', ump_img, self.test, 118, 12)
        self.p90 = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 5, 'P90', p90_img, self.test, 118, 12)
        self.bizon = self.weapon_btn(self.configure_each_weapon_container_smg, 1, 6, 'Bizon', bizon_img, self.test, 118, 12)
        
    def heavy_trigger_e(self):
        self.configure_each_weapon_container_pistols.grid_forget()
        self.configure_each_weapon_container_smg.grid_forget()
        self.configure_each_weapon_container_rifles.grid_forget()
        self.configure_each_weapon_container_snipers.grid_forget()
        self.configure_each_weapon_container_other.grid_forget()
        
        self.configure_each_weapon_container_heavy.grid(row=2, column=0, pady=self.frame_pady, padx=self.frame_padx,)
        
        self.nova = self.weapon_btn(self.configure_each_weapon_container_heavy, 1, 0, 'Nova', nova_img, self.test, 137.5, 12)
        self.xm1014 = self.weapon_btn(self.configure_each_weapon_container_heavy, 1, 1, 'Xm1014', xm1014_img, self.test, 137.5, 12)
        self.mag_7 = self.weapon_btn(self.configure_each_weapon_container_heavy, 1, 2, 'Mag 7', mag_7_img, self.test, 137.5, 12)
        self.sawed_off = self.weapon_btn(self.configure_each_weapon_container_heavy, 1, 3, 'Sawed Off', sawed_off_img, self.test, 137.5, 12)
        self.m249 = self.weapon_btn(self.configure_each_weapon_container_heavy, 1, 4, 'M249', m249_img, self.test, 137.5, 12)
        self.negev = self.weapon_btn(self.configure_each_weapon_container_heavy, 1, 5, 'Negev', negev_img, self.test, 137.5, 12)
        
    def rifles_trigger_e(self):
        self.configure_each_weapon_container_pistols.grid_forget()
        self.configure_each_weapon_container_heavy.grid_forget()
        self.configure_each_weapon_container_smg.grid_forget()
        self.configure_each_weapon_container_snipers.grid_forget()
        self.configure_each_weapon_container_other.grid_forget()
        
        self.configure_each_weapon_container_rifles.grid(row=2, column=0, pady=self.frame_pady, padx=self.frame_padx,)
        
        self.famas = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 0, 'Famas', famas_img, self.test, 118, 12)
        self.galil = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 1, 'Galil', galil_img, self.test, 118, 12)
        self.ak_47 = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 2, 'Ak47', ak_47_img, self.test, 118, 12)
        self.m4a4 = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 3, 'M4a4', m4a4_img, self.test, 118, 12)
        self.m4a1_s = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 4, 'M4a1', m4a1_s_img, self.test, 118, 12)
        self.sg553 = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 5, 'Sg553', sg553_img, self.test, 118, 12)
        self.aug = self.weapon_btn(self.configure_each_weapon_container_rifles, 1, 6, 'AUG', aug_img, self.test, 118, 12)
        
    def snipers_trigger_e(self):
        self.configure_each_weapon_container_pistols.grid_forget()
        self.configure_each_weapon_container_heavy.grid_forget()
        self.configure_each_weapon_container_rifles.grid_forget()
        self.configure_each_weapon_container_smg.grid_forget()
        self.configure_each_weapon_container_other.grid_forget()
        
        self.configure_each_weapon_container_snipers.grid(row=2, column=0, pady=self.frame_pady, padx=self.frame_padx,)
        
        self.ssg = self.weapon_btn(self.configure_each_weapon_container_snipers, 1, 0, 'SSG', ssg_img, self.test, 140, 12)
        self.awp = self.weapon_btn(self.configure_each_weapon_container_snipers, 1, 1, 'AWP', awp_img, self.test, 140, 12)
        self.scar = self.weapon_btn(self.configure_each_weapon_container_snipers, 1, 2, 'SCAR', scar_img, self.test, 140, 12)
        self.g3sg1 = self.weapon_btn(self.configure_each_weapon_container_snipers, 1, 3, 'G3SG1', g3sg1_img, self.test, 140, 12)
            
    def other_trigger_e(self):
        self.configure_each_weapon_container_pistols.grid_forget()
        self.configure_each_weapon_container_heavy.grid_forget()
        self.configure_each_weapon_container_rifles.grid_forget()
        self.configure_each_weapon_container_smg.grid_forget()
        self.configure_each_weapon_container_snipers.grid_forget()
        print('hello')
    
    def create_weapon_frame(self):
        self.frame = ct.CTkFrame(self.configure_select_group_container, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        return self.frame
    
    def glock_e(self):
        self.configure_each_weapon_container.grid(row=3, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky='news')
        self.label = ct.CTkLabel(self.configure_each_weapon_container, text='Glock')
        self.label.grid(row=0, column=0)
        
class create_visuals(ct.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color=app_colors['app']['bg_clr'])
        # Colors
        self.frame_fg_color = theme_cfg["APP"]['bg_clr_accent']
        self.frame_border_color = theme_cfg["APP"]['border_clr']
        # Dimensions
        self.frame_corner_radius = 5
        self.frame_border_width = 1
        # Grid
        self.frame_pady = 10
        self.frame_padx = 10
        self.frame_sticky = 'n'
        
        self.grid_columnconfigure(0, weight=1) # Make the first column width 100%
        self.grid_rowconfigure(1, weight=1) # Make the first column width 100%
        
        self.header_btn = header_btn(self, 0, 0, ["Global", "Player", "Local", "Other"], self.header_btn_e)
        
        # To place items inside global frame, this will make the header on its own and addint columns to items will not bother header
        self.global_frame = ct.CTkFrame(self, corner_radius=0, fg_color=app_colors['app']['bg_clr'])
        self.global_frame.grid(row=1, column=0, sticky='news')
        
        self.global_container = ct.CTkFrame(self.global_frame, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.global_container.grid_columnconfigure(1, pad=25)
        self.global_container.grid_columnconfigure(2, pad=25)
        
        self.global_master = self.item_checkbox(self.global_container, 0, 1, 'Enable', self.global_master_e)
        
        self.global_watermark = self.item_checkbox(self.global_container, 1, 1, 'Watermark', self.global_watermark_e)
        self.watermark_color = self.color_picker(self.global_container, 1, 3, self.watermark_color_e)
                
        self.player_container = ct.CTkFrame(self.global_frame, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.player_container.grid_columnconfigure(1, pad=25)
        
        self.player_box_esp_name = self.item_checkbox(self.player_container, 2, 0, 'Box', self.player_box_esp_name_e)
        self.player_box_esp = self.item_comboBox(self.player_container, 2, 1, ['normal', 'filled'], self.player_box_esp_e)
        self.player_box_esp_color = self.color_picker(self.player_container, 2, 2, self.player_box_esp_color_e)
        
        self.player_head_esp_name = self.item_checkbox(self.player_container, 3, 0, 'Head ESP', self.player_head_esp_name_e)
        self.player_head_esp = self.item_comboBox(self.player_container, 3, 1, ['circle'], self.player_head_esp_e)
        self.player_head_esp_color = self.color_picker(self.player_container, 3, 2, self.player_head_esp_color_e)
        
        
        self.player_health_esp_name = self.item_checkbox(self.player_container, 4, 0, 'Health', self.player_health_esp_name_e)
        self.player_health_esp = self.item_comboBox(self.player_container, 4, 1, ['icon', '-'], self.player_health_esp_e)
        self.player_health_esp_color = self.color_picker(self.player_container, 4, 2, self.player_health_esp_color_e)
        
        
        self.player_name_esp_name = self.item_checkbox(self.player_container, 5, 0, 'Name', self.player_name_esp_name_e)
        self.player_name_esp_color = self.color_picker(self.player_container, 5, 2, self.player_name_esp_color_e)
        
        
        self.player_weapon_esp_name = self.item_checkbox(self.player_container, 6, 0, 'Weapon', self.player_weapon_esp_name_e)
        self.player_weapon_esp = self.item_comboBox(self.player_container, 6, 1, ['icon', '-'], self.player_weapon_esp_e)
        self.player_weapon_esp_color = self.color_picker(self.player_container, 6, 2, self.player_weapon_esp_color_e)
        
        
        self.local_container = ct.CTkFrame(self.global_frame, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.local_container.grid_columnconfigure(1, pad=25)
        self.local_container.grid_columnconfigure(2, pad=25)
        
        self.local_crosshair_name = self.item_checkbox(self.local_container, 1, 0, 'Sniper Crosshair', self.local_crosshair_name_e)
        self.local_crosshair = self.item_comboBox(self.local_container, 1, 1, ['cross'], self.local_crosshair_e)
        self.local_crosshair_color = self.color_picker(self.local_container, 1, 2, self.local_crosshair_color_e)
        
        
        self.local_recoil_name = self.item_checkbox(self.local_container, 2, 0, 'Recoil Crosshair', self.local_recoil_name_e)
        self.local_recoil = self.item_comboBox(self.local_container, 2, 1, ['cross'], self.local_recoil_e)
        self.local_recoil_color = self.color_picker(self.local_container, 2, 2, self.local_recoil_color_e)
        
        
        self.local_spectator_name = self.item_checkbox(self.local_container, 3, 0, 'Spectator List', self.local_spectator_name_e)
        self.local_spectator_color = self.color_picker(self.local_container, 3, 2, self.local_spectator_color_e)
        
        
        self.other_container = ct.CTkFrame(self.global_frame, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
        self.other_container.grid_columnconfigure(1, pad=25)
        self.other_container.grid_columnconfigure(2, pad=25)
        
        self.other_bomb_info_name = self.item_checkbox(self.other_container, 1, 0, 'Bomb Info', self.other_bomb_info_name_e)
        
        # Reading our config file 
        self.config = cp.ConfigParser()
        self.config.read(CONFIG_FILE)
        # Calling our update function once when the app is loaded
        self.update_from_config()
        
        self.color_choose = None
        
    def header_btn_e(self, e):
        if e == 'Global':
            self.global_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.global_container.grid_forget()
            # Make sure to close color picker when tab is changed
            if self.color_choose is not None:
                self.color_choose.grid_forget()
            self.color_choose = None
        if e == 'Player':
            self.player_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.player_container.grid_forget()
            if self.color_choose is not None:
                self.color_choose.grid_forget()
            self.color_choose = None
        if e == 'Local':
            self.local_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.local_container.grid_forget()
            if self.color_choose is not None:
                self.color_choose.grid_forget()
            self.color_choose = None
        if e == 'Other':
            self.other_container.grid(row=1, column=0, pady=self.frame_pady, padx=self.frame_padx, sticky=self.frame_sticky)
        else:
            self.other_container.grid_forget()
            if self.color_choose is not None:
                self.color_choose.grid_forget()
            self.color_choose = None

    def item_checkbox(self, container, row, column, text, callback):
        checkbox = ct.CTkCheckBox(container, text=text, checkbox_width=25, checkbox_height=25, corner_radius=5, border_width=1, border_color='#4a4a4a', hover_color='#30293D', checkmark_color='white', fg_color='#39314A', font=ct.CTkFont(size=13), command=callback)
        checkbox.grid(row=row, column=column, pady=10, padx=10, sticky='w')
            
        return checkbox
    
    def item_comboBox(self, container, row, column, text, callback):
        comboBox = ct.CTkComboBox(container, values=text, border_width=1, border_color='#4a4a4a' ,corner_radius=5, fg_color='#202020', width=111, height=25, button_color='#39314A', button_hover_color='#30293D', dropdown_fg_color='#202020', dropdown_hover_color='#1C1C1C', dropdown_font=ct.CTkFont(size=14), command=callback)
        
        comboBox.grid(row=row, column=column, pady=10, padx=10, sticky='w')
        
        return comboBox
    
    def color_picker(self, container, row, column, callback):
        button = ct.CTkButton(container, text='', corner_radius=5, width=25, height=25, command=callback, fg_color='#242424')
        button.grid(row=row, column=column, pady=10, padx=10)
        return button

    def player_box_esp_e(self, e):
        if e == 'normal':
            state.players_box_type = 'normal'
        if e == 'filled':
            state.players_box_type = 'filled'
            
    def player_head_esp_e(self, e):
        if e == 'circle':
            state.players_head_type = 'circle'
            
    def player_health_esp_e(self, e):
        if e == 'icon':
            state.players_health_type = 'icon'
            
    def player_weapon_esp_e(self, e):
        if e == 'icon':
            state.players_weapon_type = 'icon'
            
    def local_crosshair_e(self, e):
        if e == 'cross':
            state.sniper_crosshair_type = 'cross'
            
    def local_recoil_e(self, e):
        if e == 'cross':
            state.recoil_crosshair_type = 'cross'

    def update_from_config(self):
        self.config.read(CONFIG_FILE)
        
        # Enable
        if self.config['VISUALS GLOBAL']['enabled'] == '1':
            self.global_master.select()
            self.global_master_e()
        else:
            self.global_master.deselect()
            self.global_master_e()
        
        
        # Watermark
        if self.config['VISUALS GLOBAL']['watermark'] == '1':
            self.global_watermark.select()
            self.global_watermark_e()
        else:
            self.global_watermark.deselect()
            self.global_watermark_e()

        self.get_clr_from_config(self.config['VISUALS GLOBAL']['watermark clr'], item_clr.watermark, self.watermark_color)
        

        # BOX 
        if self.config['VISUALS PLAYER']['box'] == '1':
            self.player_box_esp_name.select()
            self.player_box_esp_name_e()
        else:
            self.player_box_esp_name.deselect()
            self.player_box_esp_name_e()
        
        if self.config['VISUALS PLAYER']['box type'] == 'normal':
            state.players_box_type = 'normal'
            self.player_box_esp.set('normal')
        elif self.config['VISUALS PLAYER']['box type'] == 'filled':
            state.players_box_type = 'filled'
            self.player_box_esp.set('filled')

        self.get_clr_from_config(self.config['VISUALS PLAYER']['box clr'], item_clr.box_esp, self.player_box_esp_color)
        
        
        # Head esp 
        if self.config['VISUALS PLAYER']['head esp'] == '1':
            self.player_head_esp_name.select()
            self.player_head_esp_name_e()
        else:
            self.player_head_esp_name.deselect()
            self.player_head_esp_name_e()
    
        if self.config['VISUALS PLAYER']['head esp type'] == 'circle':
            state.players_head_type = 'circle'
            self.player_head_esp.set('circle')

        self.get_clr_from_config(self.config['VISUALS PLAYER']['head esp clr'], item_clr.head_esp, self.player_head_esp_color)
        

        # Health ESP
        if self.config['VISUALS PLAYER']['health'] == '1':
            self.player_health_esp_name.select()
            self.player_health_esp_name_e()
        else:
            self.player_health_esp_name.deselect()
            self.player_health_esp_name_e()
        
        if self.config['VISUALS PLAYER']['head esp type'] == 'icon':
            state.players_health_type = 'icon'
            self.player_head_esp.set('icon')

        self.get_clr_from_config(self.config['VISUALS PLAYER']['head esp clr'], item_clr.health_esp, self.player_health_esp_color)
            
            
        # Name ESP
        if self.config['VISUALS PLAYER']['name'] == '1':
            self.player_name_esp_name.select()
            self.player_name_esp_name_e()
        else:
            self.player_name_esp_name.deselect()
            self.player_name_esp_name_e()

        self.get_clr_from_config(self.config['VISUALS PLAYER']['name clr'], item_clr.name_esp, self.player_name_esp_color)
            
            
        # Weapon ESP
        if self.config['VISUALS PLAYER']['weapon'] == '1':
            self.player_weapon_esp_name.select()
            self.player_weapon_esp_name_e()
        else:
            self.player_weapon_esp_name.deselect()
            self.player_weapon_esp_name_e()
            
        if self.config['VISUALS PLAYER']['weapon type'] == 'icon':
            state.players_weapon_type = 'icon'
            self.player_weapon_esp.set('icon')
            
        self.get_clr_from_config(self.config['VISUALS PLAYER']['weapon clr'], item_clr.weapon_esp, self.player_weapon_esp_color)
        
        
        # Sniper Crosshair
        if self.config['VISUALS PLAYER']['sniper crosshair'] == '1':
            self.local_crosshair_name.select()
            self.local_crosshair_name_e()
        else:
            self.local_crosshair_name.deselect()
            self.local_crosshair_name_e()
             
        if self.config['VISUALS PLAYER']['sniper crosshair type'] == 'cross':
            state.sniper_crosshair_type = 'cross'
            self.local_crosshair.set('cross')
            
        self.get_clr_from_config(self.config['VISUALS PLAYER']['sniper crosshair clr'], item_clr.sniper_crosshair, self.local_crosshair_color)
        
        # Recoil crosshair
        if self.config['VISUALS PLAYER']['recoil crosshair'] == '1':
            self.local_recoil_name.select()
            self.local_recoil_name_e()
        else:
            self.local_recoil_name.deselect()
            self.local_recoil_name_e()
            
        if self.config['VISUALS PLAYER']['recoil crosshair type'] == 'cross':
            state.recoil_crosshair_type = 'cross'
            self.local_recoil.set('cross')
            
        self.get_clr_from_config(self.config['VISUALS PLAYER']['recoil crosshair clr'], item_clr.recoil_crosshair, self.local_recoil_color)
        
        
        # Spectator list
        if self.config['VISUALS PLAYER']['spectator list'] == '1':
            self.local_spectator_name.select()
            self.local_spectator_name_e()
        else:
            self.local_spectator_name.deselect()
            self.local_spectator_name_e()
            
        self.get_clr_from_config(self.config['VISUALS PLAYER']['spectator list clr'], item_clr.spectator_list, self.local_spectator_color)
        
            
        # Bomb Info
        if self.config['VISUALS PLAYER']['bomb info'] == '1':
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
    
    def hex_to_rgb(self, hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    def get_clr_from_item(self, btn):
        r = int(self.red_scale.get())
        g = int(self.green_scale.get())
        b = int(self.blue_scale.get())

        rgb = f'{r},{g},{b}'
        code = "#%02x%02x%02x" % (r, g, b)
        btn.configure(fg_color=code)

    def set_gui_comm_clr(self, gui_comm_clr):
        r = int(self.red_scale.get())
        g = int(self.green_scale.get())
        b = int(self.blue_scale.get())
        
        gui_comm_clr[0] = r
        gui_comm_clr[1] = g
        gui_comm_clr[2] = b

    def get_clr_from_config(self, config_clr, gui_comm_clr, btn):
        clr = config_clr.replace('[', '').replace(']', '').replace(',', '').split()
        r = int(clr[0])
        g = int(clr[1])
        b = int(clr[2])
        gui_comm_clr[0] = r
        gui_comm_clr[1] = g
        gui_comm_clr[2] = b
        code = "#%02x%02x%02x" % (r, g, b)
        btn.configure(fg_color=code)
    
    def display_clr_frame(self, get_btn_clr, apply_btn_callback):
        if self.color_choose is None:
            btn_clr = get_btn_clr.cget('fg_color')
            btn_clr_hex = btn_clr.replace('#', '')
            btn_clr_rbg = self.hex_to_rgb(btn_clr_hex)
            
            self.color_choose = ct.CTkFrame(self.global_frame, corner_radius=self.frame_corner_radius, fg_color=self.frame_fg_color, border_color=self.frame_border_color, border_width=self.frame_border_width)
            self.color_choose.grid(row = 1, column=2, padx=5, pady=10, sticky='n')
            self.color_choose.columnconfigure(1, weight=1)
            
            self.red_scale = ct.CTkSlider(self.color_choose, from_=0, to=255, number_of_steps=255, command=self.display_color_e, border_width=3, button_color='#ff1100', button_hover_color='#9c0d03')
            self.red_scale.grid(row = 1, column=1, padx=5, pady=10)
            self.red_scale.set(btn_clr_rbg[0])
            
            self.green_scale = ct.CTkSlider(self.color_choose, from_=0, to=255, number_of_steps=255, command=self.display_color_e, border_width=3, button_color='#03fc2c', button_hover_color='#018f19')
            self.green_scale.grid(row = 2, column=1, padx=5, pady=10)
            self.green_scale.set(btn_clr_rbg[1])
            
            self.blue_scale = ct.CTkSlider(self.color_choose, from_=0, to=255, number_of_steps=255, command=self.display_color_e, border_width=3, button_color='#0213fa', button_hover_color='#00098a')
            self.blue_scale.grid(row = 3, column=1, padx=5, pady=10)
            self.blue_scale.set(btn_clr_rbg[2])
            
            self.apply_btn = ct.CTkButton(self.color_choose, text='Apply', fg_color='black', text_color='black' ,command=apply_btn_callback)
            self.get_clr_from_item(self.apply_btn)
            self.apply_btn.grid(row=4, column=1, pady=5)
        else:
            self.color_choose.grid_forget()
            self.color_choose = None
    
    def display_color_e(self, value):
        self.get_clr_from_item(self.apply_btn)
    
    def watermark_color_e(self):
        self.display_clr_frame(self.watermark_color, self.watermark_color_apply_e)
        
    def watermark_color_apply_e(self):
        self.get_clr_from_item(self.watermark_color)
        self.set_gui_comm_clr(item_clr.watermark)
        
        self.color_choose.grid_forget()
        self.color_choose = None


    # BOX
    def player_box_esp_name_e(self):
        if self.player_box_esp_name.get() == 1:
            state.players_box_enabled = 1
        else:
            state.players_box_enabled = 0
            
    def player_box_esp_color_e(self):
        self.display_clr_frame(self.player_box_esp_color, self.player_box_esp_color_apply_e)

    def player_box_esp_color_apply_e(self):
        self.get_clr_from_item(self.player_box_esp_color)
        self.set_gui_comm_clr(item_clr.box_esp)
        
        self.color_choose.grid_forget()
        self.color_choose = None


    # HEAD ESP       
    def player_head_esp_name_e(self):
        if self.player_head_esp_name.get() == 1:
            state.players_head_enabled = 1
        else:
            state.players_head_enabled = 0
    
    def player_head_esp_color_e(self):
        self.display_clr_frame(self.player_head_esp_color, self.player_head_esp_color_apply_e)
    
    def player_head_esp_color_apply_e(self):
        self.get_clr_from_item(self.player_head_esp_color)
        self.set_gui_comm_clr(item_clr.head_esp)
        
        self.color_choose.grid_forget()
        self.color_choose = None
            
            
    # Health ESP
    def player_health_esp_name_e(self):
        if self.player_health_esp_name.get() == 1:
            state.players_health_enabled = 1
        else:
            state.players_health_enabled = 0

    def player_health_esp_color_e(self):
        self.display_clr_frame(self.player_health_esp_color, self.player_health_esp_color_apply_e)
    
    def player_health_esp_color_apply_e(self):
        self.get_clr_from_item(self.player_health_esp_color)
        self.set_gui_comm_clr(item_clr.health_esp)
        
        self.color_choose.grid_forget()
        self.color_choose = None
            
    
    # Name ESP
    def player_name_esp_name_e(self):
        if self.player_name_esp_name.get() == 1:
            state.players_names_enabled = 1
        else:
            state.players_names_enabled = 0
    
    def player_name_esp_color_e(self):
        self.display_clr_frame(self.player_name_esp_color, self.player_name_esp_color_apply_e)
    
    def player_name_esp_color_apply_e(self):
        self.get_clr_from_item(self.player_name_esp_color)
        self.set_gui_comm_clr(item_clr.name_esp)
        
        self.color_choose.grid_forget()
        self.color_choose = None
    
    # Weapon ESP
    def player_weapon_esp_name_e(self):
        if self.player_weapon_esp_name.get() == 1:
            state.players_weapon = 1
        else:
            state.players_weapon = 0
            
    def player_weapon_esp_color_e(self):
        self.display_clr_frame(self.player_weapon_esp_color, self.player_weapon_esp_color_apply_e)
    
    def player_weapon_esp_color_apply_e(self):
        self.get_clr_from_item(self.player_weapon_esp_color)
        self.set_gui_comm_clr(item_clr.weapon_esp)
        
        self.color_choose.grid_forget()
        self.color_choose = None
    
    
    # Sniper crosshair
    def local_crosshair_name_e(self):
        if self.local_crosshair_name.get() == 1:
            state.sniper_crosshair_enabled = 1
        else:
            state.sniper_crosshair_enabled = 0
            
    def local_crosshair_color_e(self):
        self.display_clr_frame(self.local_crosshair_color, self.local_crosshair_color_apply_e)
    
    def local_crosshair_color_apply_e(self):
        self.get_clr_from_item(self.local_crosshair_color)
        self.set_gui_comm_clr(item_clr.sniper_crosshair)
        
        self.color_choose.grid_forget()
        self.color_choose = None

    # Recoil crosshair
    def local_recoil_name_e(self):
        if self.local_recoil_name.get() == 1:
            state.recoil_crosshair_enabled = 1
        else:
            state.recoil_crosshair_enabled = 0
    
    def local_recoil_color_e(self):
        self.display_clr_frame(self.local_recoil_color, self.local_recoil_color_apply_e)
    
    def local_recoil_color_apply_e(self):
        self.get_clr_from_item(self.local_recoil_color)
        self.set_gui_comm_clr(item_clr.recoil_crosshair)
        
        self.color_choose.grid_forget()
        self.color_choose = None        
            
            
    # Spectator list
    def local_spectator_name_e(self):
        if self.local_spectator_name.get() == 1:
            state.spectator_enabled = 1
        else:
            state.spectator_enabled = 0
            
    def local_spectator_color_e(self):
        self.display_clr_frame(self.local_spectator_color, self.local_spectator_color_apply_e)
    
    def local_spectator_color_apply_e(self):
        self.get_clr_from_item(self.local_spectator_color)
        self.set_gui_comm_clr(item_clr.spectator_list)
        
        self.color_choose.grid_forget()
        self.color_choose = None 
    
    # Bomb info
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
        
        self.header_btn = header_btn(self, 0, 0, ["Main", "-"], self.player_header_btn_e)

        
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
                self.player_main_container.update_idletasks()
            
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
        
        self.grid_columnconfigure(0, weight=1) # Make the first column width 100%
        
        self.header_btn = header_btn(self, 0, 0, ["Config", "-"], self.header_btn_e)
        
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
        
        self.overrideredirect(True)
        self.attributes("-alpha",0.99)
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
        
        # self.after(100, self.mainloop())
    
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
        self.triggerbot_tab.update_from_config()
        self.visuals_tab.update_from_config()

    # Make our function to save config. This is done here because the App can communicate with other classes
    def save_trigger(self):
        self.config['TRIGGERBOT']['enabled'] = f'{self.triggerbot_tab.global_enabled.get()}'
        
        self.config['TRIGGERBOT']['key'] = f'{key_handler(self.triggerbot_tab.trigger_key.get())}' # Get our key 'Mouse 5' and convert to its value eg. 6
    
    def save_config_btn_e(self):
        self.save_trigger()
        
        self.config['VISUALS GLOBAL']['enabled'] = f'{self.visuals_tab.global_master.get()}'
        self.config['VISUALS GLOBAL']['watermark'] = f'{self.visuals_tab.global_watermark.get()}'
        self.config['VISUALS GLOBAL']['watermark clr'] = f'{item_clr.watermark}'
        
        self.config['VISUALS PLAYER']['box'] = f'{self.visuals_tab.player_box_esp_name.get()}'
        self.config['VISUALS PLAYER']['box clr'] = f'{item_clr.box_esp}'
        self.config['VISUALS PLAYER']['box type'] = f'{self.visuals_tab.player_box_esp.get()}'
        
        self.config['VISUALS PLAYER']['head esp'] = f'{self.visuals_tab.player_head_esp_name.get()}'
        self.config['VISUALS PLAYER']['head esp clr'] = f'{item_clr.head_esp}'
        self.config['VISUALS PLAYER']['head esp type'] = f'{self.visuals_tab.player_head_esp.get()}'
        
        self.config['VISUALS PLAYER']['health'] = f'{self.visuals_tab.player_health_esp_name.get()}'
        # clr
        # type
        
        self.config['VISUALS PLAYER']['name'] = f'{self.visuals_tab.player_name_esp_name.get()}'
        self.config['VISUALS PLAYER']['name clr'] = f'{item_clr.name_esp}'
        
        self.config['VISUALS PLAYER']['weapon'] = f'{self.visuals_tab.player_weapon_esp_name.get()}'
        self.config['VISUALS PLAYER']['weapon clr'] = f'{item_clr.weapon_esp}'
        self.config['VISUALS PLAYER']['weapon type'] = f'{self.visuals_tab.player_weapon_esp.get()}'
        
        self.config['VISUALS PLAYER']['sniper crosshair'] = f'{self.visuals_tab.local_crosshair_name.get()}'
        self.config['VISUALS PLAYER']['sniper crosshair clr'] = f'{item_clr.sniper_crosshair}'
        self.config['VISUALS PLAYER']['sniper crosshair type'] = f'{self.visuals_tab.local_crosshair.get()}'
        
        self.config['VISUALS PLAYER']['recoil crosshair'] = f'{self.visuals_tab.local_recoil_name.get()}'
        self.config['VISUALS PLAYER']['recoil crosshair clr'] = f'{item_clr.recoil_crosshair}'
        self.config['VISUALS PLAYER']['recoil crosshair type'] = f'{self.visuals_tab.local_recoil.get()}'
        
        self.config['VISUALS PLAYER']['spectator list'] = f'{self.visuals_tab.local_spectator_name.get()}'
        self.config['VISUALS PLAYER']['spectator clr'] = f'{item_clr.spectator_list}'
        
        self.config['VISUALS PLAYER']['bomb info'] = f'{self.visuals_tab.other_bomb_info_name.get()}'
        
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)
        
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
