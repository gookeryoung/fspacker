mod utils;
mod initscript;
use std::env::{current_dir, set_current_dir};
use std::ffi::OsString;
use std::os::windows::ffi::OsStrExt;
use winapi::shared::minwindef::BOOL;
use winapi::shared::minwindef::{FARPROC, HINSTANCE};
use winapi::um::errhandlingapi::GetLastError;
use winapi::um::winbase::SetDllDirectoryW;

fn main() {
    if !utils::check_env() {
        println!("Failed checking environment variables.");
        return;
    }

    let cur_dir = current_dir().unwrap();
    let runtime_dir = cur_dir.join("runtime");
    let runtime_ws: Vec<u16> = OsString::from(runtime_dir.file_name().unwrap()).encode_wide().chain(std::iter::once(0)).collect();

    // 调用 SetDllDirectoryW 添加目录
    unsafe {
        let result: BOOL = SetDllDirectoryW(runtime_ws.as_ptr());
        if result == 0 {
            let error_code = GetLastError();
            let msg = format!("Failed to set DLL directory: {}. Error code: {}", runtime_dir.clone().display(), error_code);
            utils::msgbox("Error", msg.as_str());
            return;
        } else {
            println!("Successfully set DLL directory: {}", runtime_dir.clone().display());
        }

        let dll_file = String::from("python3.dll");
        let py_dll: HINSTANCE = utils::load_dll(dll_file.as_str());
        let py_main: FARPROC = utils::call_func(py_dll, "Py_Main");

        // restore working dir
        set_current_dir(cur_dir.clone()).unwrap();
        utils::detect_python_script();
        utils::run_py_string(py_main, initscript::INIT_SCRIPT);
    }
}
