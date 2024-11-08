import imgui
import uuid

def get_relative_mouse_position():
    rect_tl = imgui.get_item_rect_min()
    rect_br = imgui.get_item_rect_max()
    pos = imgui.get_mouse_pos()

    relative_pos = imgui.Vec2(
        (pos.x - rect_tl.x) / (rect_br.x - rect_tl.x),
        (pos.y - rect_tl.y) / (rect_br.y - rect_tl.y))
    return relative_pos

class IOHandler(object):
    """
    - io_args: args passed to io function
    - user_data: user data to be passed to callbacks
    - return:
      - uid: used for unregister
    
    examples:
    1. register left mouse button click:
      > handler = IOHandler()
      > handler.register_callback('onclick', onclick_func)
    
    2. register right mouse button click:
      > handler.register_callback('onclick', onclick_func, io_args={'button': 1})
    
    3. register right mouse button click with user data:
      > handler.register_callback('onclick', onclick_func, io_args={'button': 1}, user_data={'button': 1})
    
    4. register and unregister:
      > uid = handler.register_callback('onclick', onclick_func)
      > handler.unregister_callback(uid)
    """
    def __init__(self):
        # callbacks
        # naming after https://www.w3schools.com/jsref/obj_mouseevent.asp
        self.callbacks = []

    ##################################################
    def handle_io(self):
        if not hasattr(self, 'callbacks'):
            self.callbacks = []

        if not imgui.core.is_item_hovered():
            return

        io = imgui.get_io()
        mouse_pos = get_relative_mouse_position()

        for callback in self.callbacks:
            if callback['name'] == 'onclick':
                io_func = imgui.core.is_mouse_clicked
                
            callback_func = callback['func']
            io_args = callback['io_args']
            user_data = callback['user_data']
            if io_func(**io_args):
                if user_data is not None:
                    callback_func(mouse_pos, user_data)
                else:
                    callback_func(mouse_pos)

            # print(f'is_any_item_focused = {imgui.core.is_any_item_focused()}')
            # print(f'is_item_focused = {imgui.core.is_item_focused()}')
            # print(f'is_item_hovered = {imgui.core.is_item_hovered()}')
            # print(f'is_item_visible = {imgui.core.is_item_visible()}')
                
    # register callback function
    def register_callback(self, name, func, io_args=None, user_data=None):
        if not hasattr(self, 'callbacks'):
            self.callbacks = []

        uid = uuid.uuid1()
        self.callbacks.append({
            'name': name,
            'func': func,
            'io_args': io_args if io_args is not None else {},
            'user_data': user_data,
            'uid': uid,
        })
        return uid

    # unregister callback function
    def unregister_callback(self, uid):
        if not hasattr(self, 'callbacks'):
            self.callbacks = []

        self.callbacks = [c for c in self.callbacks if c['uid'] != uid]

