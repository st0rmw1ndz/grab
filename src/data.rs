use std::env;
use std::path::PathBuf;

pub fn get_default_config_path() -> PathBuf {
    let mut path = env::current_exe().unwrap();
    path.pop();
    path.push("config.json");

    path
}
