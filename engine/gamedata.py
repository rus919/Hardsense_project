import pyMeow as meow
import ctypes as ctypes 
from engine.process import Windll


def GetWindowText(handle, length=100):
    window_text = ctypes.create_string_buffer(length)
    Windll.u32.GetWindowTextA(
        handle,
        ctypes.byref(window_text),
        length
    )
    return window_text.value

class Colors:
    orange = meow.get_color("orange")
    black = meow.get_color("black")
    purple = meow.get_color("purple")
    white = meow.get_color("white")
    cyan = meow.get_color("cyan")
    red = meow.get_color("red")
    green = meow.get_color("green")
    pink = meow.get_color("pink")
    crosshair = meow.new_color(255, 0, 255, 255)
    recoil = meow.new_color(0, 0, 255, 155)