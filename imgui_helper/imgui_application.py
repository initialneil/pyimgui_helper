import os
import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

def impl_glfw_init(window_name="minimal ImGui/GLFW3 example", width=1280, height=720):
    if not glfw.init():
        print('[ImGuiApplication] Could not initialize OpenGL context')
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print('[ImGuiApplication] Could not initialize Window')
        return None

    return window

class ImGuiApplication(object):
    def __init__(self, app_name, window_width=1600, window_height=900):
        self.app_name = app_name
        self.window = impl_glfw_init(window_name=app_name, width=window_width, height=window_height)
        if not self.window:
            return
        
        self.clear_color = (0.45, 0.55, 0.6, 1.0)
        gl.glClearColor(*self.clear_color)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

    def __del__(self):
        self.close()

    def close(self):
        if self.window:
            self.impl.shutdown()
            glfw.terminate()
            self.window = None

    @property
    def get_config_filename(self):
        cfg_fn = os.path.join(os.getenv('LOCALAPPDATA'), f'{self.app_name}/app.yaml')
        return cfg_fn

    # default content function
    def content_func(self, win_pos, win_sz):
        imgui.begin("Custom window", True)
        imgui.text("Hello, world!")
        # if imgui.button("OK"):
        #     print(f"String: {self.string}")
        #     print(f"Float: {self.f}")
        # _, self.string = imgui.input_text("A String", self.string, 256)
        # _, self.f = imgui.slider_float("float", self.f, 0.25, 1.5)
        imgui.end()

        imgui.show_test_window()
        
    def show(self):
        if not self.window:
            return
        
        # render loop
        while not glfw.window_should_close(self.window):
            self.pre_render()

            # do stuff
            win_pos = imgui.Vec2(0, 0)
            win_sz = imgui.Vec2(self.window_width, self.window_height)
            if self.content_func is not None:
                self.content_func(win_pos, win_sz)

            self.post_render()

    def pre_render(self):
        glfw.poll_events()
        self.impl.process_inputs()
        imgui.new_frame()

        W, H = glfw.get_framebuffer_size(self.window)
        self.window_width = W
        self.window_height = H

        gl.glViewport(0, 0, W, H)
        gl.glClearColor(*self.clear_color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def post_render(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)
