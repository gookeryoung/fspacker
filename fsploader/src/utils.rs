use std::env::{current_dir, current_exe, set_current_dir, set_var};
use std::ffi::{CString, OsString};
use std::io::Error;
use std::os::windows::ffi::OsStrExt;
use winapi::shared::minwindef::{FARPROC, HINSTANCE};
use winapi::shared::windef::HWND;
use winapi::um::errhandlingapi::GetLastError;
use winapi::um::libloaderapi::{GetProcAddress, LoadLibraryW};
use winapi::um::winuser::{MessageBoxW, MB_OK};


type PyMain = extern "system" fn(i32, *mut *mut i8) -> i32;

pub fn msgbox(title: &str, msg: &str) {
    // convert to wide string
    let wide_title: Vec<u16> = OsString::from(title).encode_wide().chain(std::iter::once(0)).collect();
    let wide_message: Vec<u16> = OsString::from(msg).encode_wide().chain(std::iter::once(0)).collect();

    unsafe {
        MessageBoxW(
            0 as HWND,
            wide_message.as_ptr(),
            wide_title.as_ptr(),
            MB_OK,
        );
    }
}

pub fn check_env() -> bool {
    let cur_dir = current_dir().unwrap();
    let runtime_dir = cur_dir.join("runtime");
    if !runtime_dir.exists() {
        msgbox("Error", "Runtime directory not found!");
        return false;
    }

    let py_dll_file = runtime_dir.join("python3.dll");
    if !py_dll_file.exists() {
        msgbox("Error", "python3.dll not found!");
        return false;
    }

    let py_exe_file = runtime_dir.join("python.exe");
    if !py_exe_file.exists() {
        msgbox("Error", "python.exe not found!");
        return false;
    }

    set_var("FSPLOADER", current_exe().unwrap());
    set_var("FSPLOADER_HOME", current_dir().unwrap());
    set_var("FSPLOADER_RUNTIME", runtime_dir.to_str().unwrap());
    set_var("PYTHONHOME", runtime_dir.to_str().unwrap());
    set_var("PYTHONPATH", current_exe().unwrap());
    set_var("PYTHONIOENCODING", "utf-8");
    set_var("LC_ALL", "en_US.UTF-8");
    true
}

pub fn load_dll(dll_name: &str) -> HINSTANCE {
    let wide_dll_name: Vec<u16> = OsString::from(dll_name).encode_wide().chain(std::iter::once(0)).collect();
    unsafe {
        let h_module: HINSTANCE = LoadLibraryW(wide_dll_name.as_ptr());

        if h_module.is_null() {
            // 获取并打印错误信息
            let error_code = GetLastError();
            eprintln!("Failed to load library: {}. Error code: {}", dll_name, error_code);
        } else {
            println!("Successfully loaded library: {}", dll_name);
        }

        h_module
    }
}

pub fn call_func(h_module: HINSTANCE, function_name: &str) -> FARPROC {
    // convert name into CString
    let c_function_name: CString = CString::new(function_name).expect("Failed to create CString");

    let function_address: FARPROC;
    unsafe {
        function_address = GetProcAddress(h_module, c_function_name.as_ptr());

        if function_address.is_null() {
            // 获取并打印错误信息
            let error_code = GetLastError();
            eprintln!("Failed to get function address: {}. Error code: {}", function_name, error_code);
        } else {
            println!("Successfully getting function address: {:?}", function_address);
        }

        function_address
    }
}

pub fn load_python() -> Result<FARPROC, Error> {
    let cur_dir = current_dir()?;
    let runtime_dir = cur_dir.join("runtime");
    set_current_dir(runtime_dir).expect("Failed to set current dir");

    let dll_file = load_dll("python3.dll");
    let py_main = call_func(dll_file, "Py_Main");

    set_current_dir(cur_dir)?;
    Ok(py_main)
}


pub fn run_py_string(py_main_addr: FARPROC, script: &str) {
    let cur_dir = current_dir().unwrap();
    let python_exe_file = cur_dir.join("runtime").join("python.exe");
    let py_cmd = format!("{:?}", python_exe_file.display());
    let py_cmd_c = CString::new(py_cmd).expect("Failed to create CString");

    let py_main: PyMain = unsafe { std::mem::transmute(py_main_addr) };

    let command = format!("\"{}\"", script);
    let command_c = CString::new(command).expect("Failed to create CString");
    let mut argv: Vec<*mut i8> = vec![
        // CString::new("python.exe").expect("Failed to create CString").into_raw(),
        py_cmd_c.into_raw(),
        CString::new("-I").expect("Failed to create CString").into_raw(),
        CString::new("-s").expect("Failed to create CString").into_raw(),
        CString::new("-S").expect("Failed to create CString").into_raw(),
        CString::new("-c").expect("Failed to create CString").into_raw(),
        command_c.into_raw(),
    ];

    // println!("Running script: {}", script);
    // set_current_dir(cur_dir).expect("Failed to set current working directory");
    let hr = py_main(argv.len() as i32, argv.as_mut_ptr());
    println!("py_main returned : {}", hr);
    unsafe {
        for arg in &argv {
            let s = CString::from_raw(*arg);
            println!("{}", s.to_string_lossy());
        }
    }
}

pub fn detect_python_script() {
    let current_dir = current_dir().unwrap();
    let binding = current_exe().unwrap();
    let application_name = binding.file_stem().unwrap().to_str().unwrap();
    let extensions = vec!["fsc", "int", "py", "pyw"];

    for ext in &extensions {
        let full_filepath = current_dir.join(format!("{}.{}", application_name, ext));
        if full_filepath.exists() {
            println!("Find python script at {:?}", full_filepath);
            set_var("FSPLOADER_SCRIPT", full_filepath.to_str().unwrap());
            return;
        }
    }

    let names: Vec<String> = extensions.iter().map(|e| format!("fsploader.{}", e.to_string())).collect();
    let msg = format!("Cannot find python script named: {}", names.join(", "));
    msgbox("Error", &msg);
}