import imgui
from .imgui_math import *
from .window_helper import get_title_bar_height

# nested window widgets
# default border is 8x8
# draw border line for visualization
class WindowWidget(object):
    def __init__(self, name=None, parent=None, 
                 border=imgui.Vec2(8,8),
                 max_sz=imgui.Vec2(0,0)):
        if name is None:
            if parent is not None:
                name = f'{parent.name}.{parent.num_children}'
            else:
                import uuid
                name = str(uuid.uuid4()).split('-')[0]
        self.name = name
        self.class_name = 'WindowWidget'

        self.parent = parent
        if parent is not None:
            parent.add_child(self)

        self.children = []
        self.border = border
        self.max_sz = max_sz

    def __repr__(self):
        repr = f'[{self.class_name}] {self.name}'
        if self.parent is not None:
            repr += f'\n[{self.class_name}] parent = {self.parent.name}'
        if self.num_children > 0:
            repr += f'\n[{self.class_name}] num_children = {self.num_children}'
        return repr
    
    @property
    def num_children(self):
        return len(self.children)
    
    @property
    def max_width(self):
        return self.max_sz.x
    
    @property
    def max_height(self):
        return self.max_sz.y
    
    def release(self):
        for child in self.children:
            child.release()
    
    def __del__(self):
        self.release()

    ##################################################
    def add_child(self, child):
        self.children.append(child)

    def get_child(self, idx=None, name=None):
        if idx is None and name is None:
            return None
        
        if idx is not None:
            if idx >= 0 and idx < self.num_children:
                return self.children[idx]
        
        else:
            for child in self.children:
                if child.name == name:
                    return child
        
        return None

    ##################################################
    def show(self, win_pos, win_sz):
        self.show_func(win_pos, win_sz)

    def show_func(self, win_pos, win_sz):
        if not self.parent:
            self.show_as_full_window(win_pos, win_sz)
        else:
            self.show_as_child_window(win_pos, win_sz)

    def content_func(self, win_pos, win_sz):
        pass

    def show_as_full_window(self, win_pos, win_sz):
        flags = imgui.WINDOW_NO_MOVE + imgui.WINDOW_NO_COLLAPSE
        flags += imgui.WINDOW_NO_RESIZE + imgui.WINDOW_ALWAYS_AUTO_RESIZE
        flags += imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS

        imgui.set_next_window_position(win_pos.x, win_pos.y)
        imgui.set_next_window_size(win_sz.x, win_sz.y)
        imgui.begin(self.name, True, flags=flags)
        
        # draw current content
        self.content_func(win_pos, win_sz)

        # draw children
        child_pos = vec2_add(win_pos, imgui.Vec2(self.border.x, self.border.y + get_title_bar_height()))
        child_sz = vec2_sub(
            win_sz, imgui.Vec2(self.border.x * 2, self.border.y * 2 + get_title_bar_height()))
                
        for child in self.children:
            child.show(child_pos, child_sz)

        imgui.end()

    def show_as_child_window(self, win_pos, win_sz):
        imgui.set_next_window_position(win_pos.x, win_pos.y)
        imgui.set_next_window_size(win_sz.x, win_sz.y)

        imgui.begin_child(self.name, win_sz.x, win_sz.y, True)

        # draw children  
        child_pos = vec2_add(win_pos, self.border)
        child_sz = vec2_sub(win_sz, vec2_scale(self.border, 2))

        # draw current content
        self.content_func(child_pos, child_sz)

        # ImGui::PopStyleVar();
        for child in self.children:
            child.show(child_pos, child_sz)
            
        imgui.end_child()
