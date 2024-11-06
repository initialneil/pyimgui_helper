import imgui
from .imgui_math import *
from .window_helper import get_title_bar_height
from .layout import Layout

class LayoutVertical(Layout):
    def __init__(self, name=None, parent=None, 
                 border=imgui.Vec2(0,0),
                 max_sz=imgui.Vec2(0,0)):
        super().__init__(name, parent, border, max_sz)

        self.class_name = 'LayoutVertical'

    def show_func(self, win_pos, win_sz):
        if self.num_children == 0:
            return
        
        total_height = win_sz.y
        child_idxs = [i for i in range(self.num_children)]
        height_list = self.get_children_extent(total_height, self.border.y, child_idxs)

        # update by min/max resolution of children
        child_idxs = []
        for i, child in enumerate(self.children):
            if child.max_height > 0:
                height_list[i] = min(height_list[i], child.max_height)
                total_height -= height_list[i]
            else:
                child_idxs.append(i)
        
        # post update
        if len(child_idxs) != self.num_children:
            updated_height = self.get_children_extent(total_height, self.border.y, child_idxs)
            for i, h in zip(child_idxs, updated_height):
                height_list[i] = h
        
        # show window
        y0 = win_pos.y
        for i, child in enumerate(self.children):
            x = win_pos.x + self.border.x
            y = y0 + self.border.y
            w = win_sz.x - self.border.x * 2
            h = height_list[i]
            child.show(imgui.Vec2(x, y), imgui.Vec2(w, h))

            y0 += h

