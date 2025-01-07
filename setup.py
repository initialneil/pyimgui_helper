# Useful helpers for pyimgui
# https://github.com/pyimgui/pyimgui
# Developed by Neil Z. SHAO
# https://github.com/initialneil/pyimgui_helper
import os
from pathlib import Path

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_packages

__version__ = "0.1.0"

# 查找系统库的路径（例如 user32.dll 和 shell32.dll）
def find_system_library(library_name):
    possible_paths = [
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32'),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SysWow64')
    ]
    for path in possible_paths:
        library_path = os.path.join(path, library_name)
        if os.path.exists(library_path):
            return path  # 返回库所在的目录
    return None

# 查找Windows SDK的路径
def find_windows_sdk_path():
    sdk_lib_path = os.environ.get('WindowsSdkDir', None)
    if sdk_lib_path:
        return sdk_lib_path
    return None

# 自动设置库路径
def get_library_paths(libraries):
    library_dirs = []
    include_dirs = []
    
    for lib in libraries:
        # 查找系统库路径
        lib_path = find_system_library(f"{lib}.dll")
        if lib_path:
            library_dirs.append(lib_path)

        # 查找Windows SDK路径并设置include目录
        sdk_path = find_windows_sdk_path()
        if sdk_path:
            include_dirs.append(os.path.join(sdk_path, 'Include', '10.0.22000.0', 'ucrt'))

    return library_dirs, include_dirs


# 获取自动配置的路径
libraries = ['User32', 'Shell32']
library_dirs, include_dirs = get_library_paths(libraries)

ext_modules = [
    Pybind11Extension(
        "imgui_helper.pfd", 
        ["imgui_helper/src/portable-file-dialogs_py.cpp"],
        define_macros=[('VERSION_INFO', __version__)],
        libraries=libraries,
        library_dirs=library_dirs,
        include_dirs=include_dirs,
    )
]

setup(
    name="imgui_helper",
    version=__version__,
    author="Neil Z. Shao",
    author_email="initialneil@gmail.com",
    url="",
    description="Useful helpers for pyimgui",
    long_description="",
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.0",
)
