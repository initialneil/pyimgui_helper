import imgui
from .window_widget import WindowWidget

# parent class for layout
# default border is 0x0
# do not draw border line
class Layout(WindowWidget):
    def __init__(self, name=None, parent=None, 
                 border=imgui.Vec2(0,0),
                 max_sz=imgui.Vec2(0,0)):
        super().__init__(name, parent, border, max_sz)

        self.stretch_weights = []
        self.class_name = 'Layout'
    
    @property
    def num_stretch_weights(self):
        return len(self.stretch_weights)

    def set_layout_streth(self, weights):
        self.stretch_weights = weights

    def get_stretch_weight(self, idx):
        if idx >= 0 and idx < self.num_stretch_weights:
            return self.stretch_weights[idx]
        else:
            return 1.0

    def get_total_stretch(self, child_idxs=None):
        s = 0
        if child_idxs is None:
            for w in self.stretch_weights:
                s += w
        else:
            for idx in child_idxs:
                s += self.get_stretch_weight(idx)
        return s
    
    def get_children_extent(self, total_extent:int, border:int, child_idxs=None):
        if child_idxs is None:
            return None 
        
        num = len(child_idxs)
        if num == 0:
            return []
        
        total_stretch = self.get_total_stretch(child_idxs)
        if total_stretch == 0:
            sub_val = 1
        else:
            sub_val = max((total_extent - border * (num + 1)) / total_stretch, 1)

        sum_extent = 0
        sz_list = []
        for idx in child_idxs:
            extent = sub_val * self.get_stretch_weight(idx)
            sz_list.append(extent)
            sum_extent += extent

        # fix the last
        sz_list[-1] += total_extent - sum_extent

        return sz_list
