Helper for pyimgui
> The easist way to write GUI app in python -- Neil. Z. SHAO

---

### Examples
##### Application Setup
```
import imgui_helper
app = imgui_helper.ImGuiApplication('imgui_app')
app.show()
```

##### Hello World: Standard ImGui Window
```
import imgui
import imgui_helper

app = imgui_helper.ImGuiApplication('imgui_app')

def content_func(win_pos, win_sz):
    imgui.begin("Custom window", True)
    imgui.text("Hello, world!")
    imgui.show_test_window()
    imgui.end()

app.content_func = content_func

app.show()
```

##### Hello World: Fullscreen Window
```
import imgui
import imgui_helper

app = imgui_helper.ImGuiApplication('imgui_app')

def content_func(win_pos, win_sz):
    flags = imgui.WINDOW_NO_MOVE + imgui.WINDOW_NO_COLLAPSE
    flags += imgui.WINDOW_NO_RESIZE + imgui.WINDOW_ALWAYS_AUTO_RESIZE
    flags += imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS

    imgui.set_next_window_position(win_pos.x, win_pos.y)
    imgui.set_next_window_size(win_sz.x, win_sz.y)
    imgui.begin("Custom window", True, flags=flags)
    imgui.text("Hello, world!")
    imgui.end()

    
app.content_func = content_func

app.show()
```

##### Layout
```
import imgui
import imgui_helper
import os
import cv2

app = imgui_helper.ImGuiApplication('imgui_app')

central_widget = imgui_helper.WindowWidget('MainWindow')

win1 = imgui_helper.LayoutHorizontal(parent=central_widget)
win1.set_layout_streth([1, 3])

win11 = imgui_helper.LayoutVertical(parent=win1)
win111 = imgui_helper.WindowWidget(parent=win11)
win112 = imgui_helper.WindowWidget(parent=win11)

win12 = imgui_helper.ImageWindow(parent=win1)

# main
def content_func(win_pos, win_sz):
    central_widget.show(win_pos, win_sz)
    
app.content_func = content_func

# one way of show image
wdg_img = imgui_helper.ImageWidget()
img = cv2.imread(os.path.abspath(__file__ + '/../img.jpg'))
wdg_img.create_from_ndarray(img)

wdg_img.release()
wdg_img.create_from_ndarray(img)

def show_img(win_pos, win_sz):
    wdg_img.show(win_sz)

win112.content_func = show_img

# another way of show image (w/ autofit)
win12.set_image(img)
win12.register_callback('onclick', lambda pos: print(f'{win12.name} {pos}'))
                                                     
wdg_img.register_callback('onclick', lambda pos: print(f'wdg_img {pos}'))

app.show()
```

