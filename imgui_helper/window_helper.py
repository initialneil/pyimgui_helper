import imgui

def get_title_bar_height():
    return imgui.get_font_size() + imgui.get_style().frame_padding.y * 2
