from dataclasses import dataclass
from OpenGL.GL import glPushAttrib, glMatrixMode, glLoadIdentity, glOrtho, glDisable, glEnable, glBlendFunc, glClear, \
    glLineWidth, glBegin, glColor4f, glVertex2f, glColor3f, glEnd, glPointSize, GL_ALL_ATTRIB_BITS, GL_PROJECTION, GL_DEPTH_TEST, \
    GL_TEXTURE_2D, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, GL_LINE_LOOP, GL_POINTS, GL_LINES, GL_QUADS
from math import tan, cos, pi
from OpenGL.GLUT import *

from glfw import init, window_hint, create_window, set_input_mode, make_context_current, swap_interval, swap_buffers, \
    poll_events, set_window_should_close, window_should_close, destroy_window, FLOATING, DECORATED, RESIZABLE, \
    TRANSPARENT_FRAMEBUFFER, SAMPLES, CURSOR, CURSOR_DISABLED

from win32con import WS_EX_LAYERED, GWL_EXSTYLE, WS_EX_TRANSPARENT
from win32gui import FindWindow, GetWindowLong, SetWindowLong

from ctypes import windll
k32 = windll.kernel32

@dataclass
class ScreenSize:
    x = ctypes.windll.user32.GetSystemMetrics(0)
    y = ctypes.windll.user32.GetSystemMetrics(1)

class Overlay:
    def __init__(self, target='Counter-Strike: Global Offensive - Direct3D 9'):
        # init glfw
        init()
        
        # set window hints
        window_hint(FLOATING, True)
        window_hint(DECORATED, False)
        window_hint(RESIZABLE, False)
        window_hint(TRANSPARENT_FRAMEBUFFER, True)
        window_hint(SAMPLES, 8)

        if target == 'Counter-Strike: Global Offensive - Direct3D 9':
            try:
                self.window = create_window(ScreenSize.x - 1, ScreenSize.y - 1, title:='Overlay', None, None)
                
                set_input_mode(self.window, CURSOR, CURSOR_DISABLED)
                make_context_current(self.window)
                swap_interval(1)
                
                # set window attributes
                glPushAttrib(GL_ALL_ATTRIB_BITS)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                glOrtho(0, ScreenSize.x - 1, 0, ScreenSize.y - 1, -1, 1)
                glDisable(GL_DEPTH_TEST)
                glDisable(GL_TEXTURE_2D)
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                # get handle to created window
                self.handle = FindWindow(None, title)
                # self.game_window = FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
                # self.game_window_size = win32gui.GetClientRect(self.game_window)
                # print(self.game_window_size)
                # make window transparent
                exstyle = GetWindowLong(self.handle, GWL_EXSTYLE)
                exstyle |= WS_EX_LAYERED
                exstyle |= WS_EX_TRANSPARENT
                SetWindowLong(self.handle, GWL_EXSTYLE, exstyle)
                SetWindowLong(self.handle, GWL_EXSTYLE,
                                    exstyle | WS_EX_LAYERED)
            except Exception as e: #Error stuff
                print(e)
    
    def refresh(self):
        swap_buffers(self.window)
        glClear(GL_COLOR_BUFFER_BIT)
        poll_events()

    # def update(self):
    #     glfw.swap_buffers(self.window)
    #     glClear(GL_COLOR_BUFFER_BIT)
    #     glfw.poll_events()

    # def close(self):
    #     glfw.set_window_should_close(self.window, True)
    #     glfw.destroy_window(self.window)
    #     glfw.terminate()

    # def overlay_loop(self):
    #     if win32api.GetAsyncKeyState(win32con.VK_F4):
    #         self.running = False
    #         self.close()
    #     self.update()
    #     time.sleep(0.001)
    #     print("updated")
    #     return self.running

    def line(self, x1, y1, x2, y2, width, color):
        glLineWidth(width)
        glBegin(GL_LINES)
        glColor3f(color[0], color[1], color[2])
        glVertex2f(x2, y2)
        glVertex2f(x1, y1)
        glEnd()

    def box(self, x, y, width, height, line_width, color):
        glLineWidth(line_width)
        glBegin(GL_QUADS)
        glColor4f(color[0], color[1], color[2], 155)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + 3)
        # glVertex2f(x + width, y + height)
        glVertex2f(x, y + 3)
        glEnd()

    def _draw_corner(self, x, y, lineW, lineH, width, height):
        glBegin(GL_LINES)
        glVertex2f(x, y)
        glVertex2f(x + lineW, y)
        glVertex2f(x, y)
        glVertex2f(x, y + lineH)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + lineH)
        glVertex2f(x + width, y)
        glVertex2f(x + width - lineW, y)
        glVertex2f(x, y + height)
        glVertex2f(x, y + height - lineH)
        glVertex2f(x, y + height)
        glVertex2f(x + lineW, y + height)
        glVertex2f(x + width, y + height)
        glVertex2f(x + width, y + height - lineH)
        glVertex2f(x + width, y + height)
        glVertex2f(x + width - lineW, y + height)
        glEnd()

    def corner_box(self, x, y, width, height, line_width, color, outline_color):
        lineW = width / 4
        lineH = height / 3
        glLineWidth(line_width + 2)
        glColor3f(*outline_color)
        self._draw_corner(x, y, lineW, lineH, width, height)
        glLineWidth(line_width)
        glColor3f(*color)
        self._draw_corner(x, y, lineW, lineH, width, height)
        # glCallLists(12, GL_UNSIGNED_BYTE, "Red Triangle")

    def draw_empty_circle(self, cx: float, cy: float, r: float, points: int, color):
        # credits to https://stackoverflow.com/, I just edited it for my needs
        glColor4f(color[0], color[1], color[2], 255)
        theta = pi * 2 / float(points)
        tangetial_factor = tan(theta)
        radial_factor = cos(theta)
        x = r
        y = 0
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        
        for i in range(points):
            glVertex2f(x + cx, y + cy)
            tx = -y
            ty = x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor
        glEnd()
    
    def draw_lines(self, start_point_x: float, start_point_y: float, line_width: float):
        glLineWidth(line_width)
        glBegin(GL_LINES)
        glColor4f(255.0, 0.0, 155.0, 255.0)
        glVertex2f(start_point_x, start_point_y + 5)
        glVertex2f(start_point_x, start_point_y - 5)
        glVertex2f(start_point_x - 5, start_point_y)
        glVertex2f(start_point_x + 5, start_point_y)
        glEnd()