import imgui

def vec2_add(a, b):
    return imgui.Vec2(a.x + b.x, a.y + b.y)

def vec2_sub(a, b):
    return imgui.Vec2(a.x - b.x, a.y - b.y)

def vec2_scale(a, scale):
    return imgui.Vec2(a.x * scale, a.y * scale)
