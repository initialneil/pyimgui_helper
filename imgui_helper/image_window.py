import imgui
import OpenGL.GL as gl
from .window_widget import WindowWidget
from .io_helper import IOHandler

# image widget with gl_texture
class ImageWidget(IOHandler):
    def __init__(self):
        self.texture = None
        self.width = 0
        self.height = 0

    def __del__(self):
        self.release()

    @property
    def sz(self):
        return imgui.Vec2(self.width, self.height)

    def init(self):
        if self.texture is None:
            texture = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
            # gl.glPixelStorei(gl.GL_UNPACK_ROW_LENGTH,0)
            self.texture = texture
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def release(self):
        if self.texture is not None:
            gl.glDeleteTextures(self.texture)
            self.texture = None
            self.width = 0
            self.height = 0

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    # create from cv2 ndarray
    # HxW uint8
    # HxWx3 uint8
    # HxWx4 uint8
    def create_from_ndarray(self, img, is_bgr=True):
        self.init()
        self.height, self.width = img.shape[:2]

        self.bind()

        import numpy as np
        if img.dtype == np.uint8:
            # HxW
            if len(img.shape) == 2:
                gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 
                                0, gl.GL_RED, gl.GL_UNSIGNED_BYTE, 
                                img)
            # HxWxC
            elif len(img.shape) == 3:
                # HxWx1
                if img.shape[2] == 1:
                    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 
                                    0, gl.GL_BGR, gl.GL_UNSIGNED_BYTE, 
                                    img)
                # HxWx3
                elif img.shape[2] == 3:
                    # BGR
                    if is_bgr:
                        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 
                                        0, gl.GL_BGR, gl.GL_UNSIGNED_BYTE, 
                                        img)
                    # RGB
                    else:
                        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 
                                        0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, 
                                        img)
                # HxWx4
                elif img.shape[2] == 4:
                    # BGR
                    if is_bgr:
                        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 
                                        0, gl.GL_BGRA, gl.GL_UNSIGNED_BYTE, 
                                        img)
                    # RGB
                    else:
                        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 
                                        0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, 
                                        img)
                # HxWxC, C != 1, 3, 4
                else:
                    raise NotImplementedError
            # ???
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

        self.unbind()

    def show(self, win_sz=None):
        if win_sz is None:
            win_sz = imgui.Vec2(self.width, self.height)

        if self.texture is not None:
            imgui.image(self.texture, win_sz.x, win_sz.y)

            # handle io on image
            self.handle_io()


# window for showing one image or images in grids
class ImageWindow(WindowWidget):
    def __init__(self, name=None, parent=None, 
                 border=imgui.Vec2(8,8),
                 max_sz=imgui.Vec2(0,0),
                 fit_mode='fit'):
        super().__init__(name, parent, border, max_sz)

        self.class_name = 'ImageWindow'
        self.widget_image = ImageWidget()
        self.widget_image_list = None

        # fit window mode
        # https://support.optisigns.com/hc/en-us/articles/360026610194-Stretch-your-images-document-Stretch-vs-Fit-vs-Zoom-your-content
        # none, fit, stretch, zoom
        self.fit_mode = fit_mode

    def release(self):
        self.widget_image.release()

    ##################################################
    # set image from np.ndarray
    # usually loaded by cv2
    def set_image(self, img, is_bgr=True):
        self.widget_image.create_from_ndarray(img, is_bgr=is_bgr)

    def fit_display_size(self, win_sz):
        if self.widget_image.width == 0 or self.widget_image.height == 0:
            return win_sz
        
        if self.fit_mode == 'stretch':
            return win_sz
        
        elif self.fit_mode == 'fit':
            scale = min(win_sz.x / self.widget_image.width, win_sz.y / self.widget_image.height)
            scale = max(0.01, scale)
            width = (int)(self.widget_image.width * scale)
            height = (int)(self.widget_image.height * scale)

            cursor_x = (int)(self.border.x + (win_sz.x - width) / 2)
            cursor_y = (int)(self.border.y + (win_sz.y - height) / 2)
            imgui.set_cursor_pos(imgui.Vec2(cursor_x, cursor_y))

            return imgui.Vec2(width, height)
        
        elif self.fit_mode == 'zoom':
            scale = max(win_sz.x / self.widget_image.width, win_sz.y / self.widget_image.height)
            scale = max(0.01, scale)
            width = (int)(self.widget_image.width * scale)
            height = (int)(self.widget_image.height * scale)
            return imgui.Vec2(width, height)
        
        else:
            return self.widget_image.sz
    
    def content_func(self, win_pos, win_sz):
        if self.widget_image is not None:
            display_sz = self.fit_display_size(win_sz)
            self.widget_image.show(display_sz)
        else:
            pass

    ##################################################
    # register callback functions
    def register_callback(self, name, func, io_args=None, user_data=None):
        self.widget_image.register_callback(name, func, io_args=io_args, user_data=user_data)

