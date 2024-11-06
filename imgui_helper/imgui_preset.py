import imgui
from enum import Enum

def imgui_color(R, G, B, A):
    return imgui.Vec4(R / 255, G / 255, B / 255, A / 255)

class ImGuiColor(Enum):
    # hsv sample
    COLOR_GARNET = 0	# dark red
    COLOR_BROWN = 1	    # dark yellow
    COLOR_OLIVE = 2	    # dark green
    COLOR_AQUA = 3		# blue green
    COLOR_SKY = 4		# sky blue
    COLOR_PURPLE = 5
    COLOR_PINK = 6

    # manually set
    COLOR_RED = 7
    COLOR_GREEN = 8
    COLOR_BLUE = 9
    COLOR_ORANGE = 10
    COLOR_GREY = 11

    # slider bar
    COLOR_BAR_KEYFRAME = 100
    COLOR_BAR_KEYFRAME_SELECT = 101
    COLOR_BAR_TRACKED = 102
    COLOR_BAR_TRACKED_SELECT = 103
    COLOR_BAR_FRAME = 104
    COLOR_BAR_FRAME_SELECT = 105

# preset: color, color_hovered, color_active
def get_color_preset(preset: ImGuiColor):
    if preset.value < 7:
        color = imgui.color_convert_hsv_to_rgb(preset.value / 7.0, 0.6, 0.6)
        color_hovered = imgui.color_convert_hsv_to_rgb(preset.value / 7.0, 0.7, 0.7)
        color_active = imgui.color_convert_hsv_to_rgb(preset.value / 7.0, 0.8, 0.8)

    elif preset == ImGuiColor.COLOR_RED:
        color = imgui_color(255, 140, 140, 255)
        color_hovered = imgui_color(255, 100, 100, 255)
        color_active = imgui_color(255, 0, 0, 255)

    elif preset == ImGuiColor.COLOR_GREEN:
        color = imgui_color(94, 255, 134, 255)
        color_hovered = imgui_color(43, 255, 96, 255)
        color_active = imgui_color(0, 255, 64, 255)

    elif preset == ImGuiColor.COLOR_BLUE:
        color = imgui_color(0, 180, 255, 255)
        color_hovered = imgui_color(0, 140, 255, 255)
        color_active = imgui_color(0, 0, 255, 255)

    elif preset == ImGuiColor.COLOR_ORANGE:
        color = imgui_color(255, 170, 85, 255)
        color_hovered = imgui_color(255, 160, 66, 255)
        color_active = imgui_color(255, 128, 0, 255)

    elif preset == ImGuiColor.COLOR_GREY:
        color = imgui_color(127, 127, 127, 255)
        color_hovered = imgui_color(200, 200, 200, 255)
        color_active = imgui_color(175, 175, 175, 255)


    elif preset == ImGuiColor.COLOR_BAR_KEYFRAME:
        color = imgui_color(255, 128, 0, 255)
        color_hovered = imgui_color(255, 200, 0, 255)
        color_active = imgui_color(255, 255, 255, 255)

    elif preset == ImGuiColor.COLOR_BAR_KEYFRAME_SELECT:
        color = imgui_color(255, 200, 128, 255)
        color_hovered = imgui_color(255, 255, 128, 255)
        color_active = imgui_color(255, 255, 255, 255)

    elif preset == ImGuiColor.COLOR_BAR_TRACKED:
        color = imgui_color(0, 128, 0, 255)
        color_hovered = imgui_color(0, 200, 0, 255)
        color_active = imgui_color(255, 255, 255, 255)

    elif preset == ImGuiColor.COLOR_BAR_TRACKED_SELECT:
        color = imgui_color(0, 220, 0, 255)
        color_hovered = imgui_color(0, 240, 0, 255)
        color_active = imgui_color(255, 255, 255, 255)

    elif preset == ImGuiColor.COLOR_BAR_FRAME:
        color = imgui_color(128, 128, 128, 255)
        color_hovered = imgui_color(200, 200, 200, 255)
        color_active = imgui_color(255, 255, 255, 255)

    elif preset == ImGuiColor.COLOR_BAR_FRAME_SELECT:
        color = imgui_color(220, 220, 220, 255)
        color_hovered = imgui_color(240, 240, 240, 255)
        color_active = imgui_color(255, 255, 255, 255)

    else:
        color = imgui_color(220, 220, 220, 255)
        color_hovered = imgui_color(240, 240, 240, 255)
        color_active = imgui_color(255, 255, 255, 255)

    return color, color_hovered, color_active

def button_preset(label, preset=None, size=imgui.Vec2(0,0), disable_ui=False):
    if preset is None:
        return imgui.button(label, width=size.x, height=size.y)

    color, color_hovered, color_active = get_color_preset(preset)

    imgui.push_style_color(imgui.COLOR_BUTTON, *color)
    if not disable_ui:
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *color_hovered)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *color_active)
    else:
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *color)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *color)

    click = imgui.button(label, width=size.x, height=size.y)

    imgui.pop_style_color(3)
    return click

# ##################################################
# class KEY_MAP(object):
#     @classproperty
#     def KEY_A(self):
#         return imgui.get_key_index(imgui.KEY_A)
    
#     KEY_A = imgui.get_key_index(imgui.KEY_A)
#     KEY_D = KEY_A + ord('d') - ord('a')
#     KEY_W = KEY_A + ord('w') - ord('a')
#     KEY_S = KEY_A + ord('s') - ord('a')
#     KEY_Q = KEY_A + ord('q') - ord('a')
#     KEY_E = KEY_A + ord('e') - ord('a')
#     KEY_LEFT_ARROW = imgui.get_key_index(imgui.KEY_LEFT_ARROW)
#     KEY_RIGHT_ARROW = imgui.get_key_index(imgui.KEY_RIGHT_ARROW)
#     KEY_UP_ARROW = imgui.get_key_index(imgui.KEY_UP_ARROW)
#     KEY_DOWN_ARROW = imgui.get_key_index(imgui.KEY_DOWN_ARROW)
