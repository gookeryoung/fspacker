mod utils;
mod initscript;

fn main() {
    if !utils::check_env() {
        println!("Failed checking environment variables.");
        return;
    }

    let py_main = utils::load_python().unwrap();
    utils::detect_python_script();
    utils::run_py_string(py_main, "\"print('hello')\"");
    utils::run_py_string(py_main, initscript::INIT_SCRIPT);
}
