import imgui

def get_relative_mouse_position():
    rect_tl = imgui.get_item_rect_min()
    rect_br = imgui.get_item_rect_max()
    pos = imgui.get_mouse_pos()

    relative_pos = imgui.Vec2(
        (pos.x - rect_tl.x) / (rect_br.x - rect_tl.x),
        (pos.y - rect_tl.y) / (rect_br.y - rect_tl.y))
    return relative_pos

class IOHandler(object):
    def __init__(self):
        pass

        # callbacks
        # naming after https://www.w3schools.com/jsref/obj_mouseevent.asp
        self.callbacks = {}

    ##################################################
    def handle_io(self):
        if not hasattr(self, 'callbacks'):
            self.callbacks = {}

        if not imgui.core.is_item_hovered():
            return

        io = imgui.get_io()
        mouse_pos = get_relative_mouse_position()

        if 'onclick' in self.callbacks and imgui.core.is_mouse_clicked(0):
            self.callbacks['onclick'](mouse_pos)

            # print(f'is_any_item_focused = {imgui.core.is_any_item_focused()}')
            # print(f'is_item_focused = {imgui.core.is_item_focused()}')
            # print(f'is_item_hovered = {imgui.core.is_item_hovered()}')
            # print(f'is_item_visible = {imgui.core.is_item_visible()}')
                
    # register callback functions
    def register_callback(self, name, func):
        if not hasattr(self, 'callbacks'):
            self.callbacks = {}

        self.callbacks[name] = func


