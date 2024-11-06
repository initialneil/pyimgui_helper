import imgui
from .imgui_math import *
from .window_helper import get_title_bar_height
from .layout import Layout

class LayoutHorizontal(Layout):
    def __init__(self, name=None, parent=None, 
                 border=imgui.Vec2(0,0),
                 max_sz=imgui.Vec2(0,0)):
        super().__init__(name, parent, border, max_sz)

        self.class_name = 'LayoutHorizontal'

    def show_func(self, win_pos, win_sz):
        if self.num_children == 0:
            return
        
        total_width = win_sz.x
        child_idxs = [i for i in range(self.num_children)]
        width_list = self.get_children_extent(total_width, self.border.x, child_idxs)

        # update by min/max resolution of children
        child_idxs = []
        for i, child in enumerate(self.children):
            if child.max_width > 0:
                width_list[i] = min(width_list[i], child.max_width)
                total_width -= width_list[i]
            else:
                child_idxs.append(i)
        
        # post update
        if len(child_idxs) != self.num_children:
            updated_width = self.get_children_extent(total_width, self.border.x, child_idxs)
            for i, w in zip(child_idxs, updated_width):
                width_list[i] = w
        
        # show window
        x0 = win_pos.x
        for i, child in enumerate(self.children):
            x = x0 + self.border.x
            y = win_pos.y + self.border.y
            w = width_list[i]
            h = win_sz.y - self.border.y * 2
            child.show(imgui.Vec2(x, y), imgui.Vec2(w, h))

            x0 += w

