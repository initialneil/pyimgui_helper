import imgui
import numpy as np
from .imgui_preset import ImGuiColor, get_color_preset, button_preset

class FramesetBar(object):
    IS_KEYFRAME = 1
    IS_TRACKED = 2

    def __init__(self, num_frames, border=9, tag='frameset_bar', disable_io=False):
        self.num_frames = num_frames
        self.border = border
        self.tag = tag
        self.disable_io = disable_io

        self.status = np.zeros(num_frames)
        self.ui_select = -1

        # callbacks
        self.callback_ui_select = lambda x: None

    def show(self, win_pos, win_sz):
        imgui.new_line()

        N = self.num_frames
        border = self.border
        btn_w = (win_sz.x - border * 2) / N

        for i in range(N):
            start_x = i * btn_w + border
            imgui.same_line(start_x)

            if self.status[i] == self.IS_KEYFRAME:
                btn_clr = ImGuiColor.COLOR_BAR_KEYFRAME
                if self.ui_select == i:
                    btn_clr = ImGuiColor.COLOR_BAR_KEYFRAME_SELECT
            elif self.status[i] == self.IS_TRACKED:
                btn_clr = ImGuiColor.COLOR_BAR_TRACKED
                if self.ui_select == i:
                    btn_clr = ImGuiColor.COLOR_BAR_TRACKED_SELECT
            else:
                btn_clr = ImGuiColor.COLOR_BAR_FRAME
                if self.ui_select == i:
                    btn_clr = ImGuiColor.COLOR_BAR_FRAME_SELECT

            width = btn_w
            if i < self.num_frames - 1:
                if (self.status[i] == self.IS_KEYFRAME or self.status[i] == self.IS_TRACKED) and (
                    self.status[i + 1] == self.IS_KEYFRAME or self.status[i + 1] == self.IS_TRACKED) and (
                        self.status[i] == self.status[i + 1]):
                    width = btn_w = 1  

            str = f'##{self.tag}_{i:06d}'
            if button_preset(str, btn_clr, imgui.Vec2(width, 0), disable_ui=self.disable_io):
                self.ui_select = i
                self.callback_ui_select(i)

    def set_keyframe(self, idx):
        if idx >= 0 and idx < self.num_frames:
            self.status[idx] = self.IS_KEYFRAME
                
    def step_backward(self):
        if self.ui_select > 0:
            self.ui_select = self.ui_select - 1
            self.callback_ui_select(self.ui_select)

    def step_forward(self):
        if self.ui_select < self.num_frames - 1:
            self.ui_select = self.ui_select + 1
            self.callback_ui_select(self.ui_select)

