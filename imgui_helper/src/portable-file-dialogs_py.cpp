#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "portable-file-dialogs.h"

namespace py = pybind11;

enum class PyimguiOpt : uint8_t {
    none = 0,
    // For file open, allow multiselect.
    multiselect     = 0x1,
    // For file save, force overwrite and disable the confirmation dialog.
    force_overwrite = 0x2,
    // For folder select, force path to be the provided argument instead
    // of the last opened directory, which is the Microsoft-recommended,
    // user-friendly behaviour.
    force_path      = 0x4,

};
inline PyimguiOpt operator |(PyimguiOpt a, PyimguiOpt b) { return PyimguiOpt(uint8_t(a) | uint8_t(b)); }
inline bool operator &(PyimguiOpt a, PyimguiOpt b) { return bool(uint8_t(a) & uint8_t(b)); }

std::string select_folder(const std::string title, const std::string default_path = "", PyimguiOpt options = PyimguiOpt::none){
    auto folder = pfd::select_folder(title, default_path, (pfd::opt)options);
    return folder.result();
}

std::vector<std::string> open_file(std::string const title, 
    std::string const default_path = "", 
    std::vector<std::string> const filters = { "All Files", "*" }, 
    PyimguiOpt options = PyimguiOpt::none){
    auto file = pfd::open_file(title, default_path, filters, (pfd::opt)options);
    return file.result();
}

std::vector<std::string> open_file(std::string const title,
    std::string const default_path,
    std::vector<std::string> const filters,
    bool allow_multiselect){
    auto files = pfd::open_file(title, default_path, filters, allow_multiselect);
    return files.result();
}

// bind code
PYBIND11_MODULE(pfd, m) {
    // import PyimguiOpt
    py::enum_<PyimguiOpt>(m, "PyimguiOpt")
        .value("none", PyimguiOpt::none)
        .value("multiselect", PyimguiOpt::multiselect)
        .value("force_overwrite", PyimguiOpt::force_overwrite)
        .value("force_path", PyimguiOpt::force_path)
        .export_values();  
    m.def("__or__", [](PyimguiOpt a, PyimguiOpt b) { return a | b; }, py::arg("a"), py::arg("b"));
    m.def("__and__", [](PyimguiOpt a, PyimguiOpt b) { return a & b; }, py::arg("a"), py::arg("b"));

    m.def("select_folder", [](const std::string title, const std::string default_path, PyimguiOpt options) 
        { return select_folder(title, default_path, options); }, 
        py::arg("title"), 
        py::arg("default_path") = "", 
        py::arg("options") = PyimguiOpt::none);
    
    
    m.def("open_file", [](const std::string title, const std::string default_path, const std::vector<std::string> filters, PyimguiOpt options) 
        { return open_file(title, default_path, filters, options); },
        py::arg("title"),
        py::arg("default_path") = "",
        py::arg("filters") = py::cast<std::vector<std::string>>({ "All Files", "*" }),
        py::arg("options") = PyimguiOpt::none);


    m.def("open_file", [](const std::string title, const std::string default_path, const std::vector<std::string> filters, bool allow_multiselect) 
        { return open_file(title, default_path, filters, allow_multiselect); },
        py::arg("title"),
        py::arg("default_path"),
        py::arg("filters"),
        py::arg("allow_multiselect"));
}