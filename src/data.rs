use std::env;
use std::path::{Path, PathBuf};

const DEFAULT_CONFIG_NAME: &str = "config.json";

pub fn get_default_config_path() -> PathBuf {
    env::current_exe()
        .expect("Failed to read the default config path")
        .parent()
        .expect("Failed to get parent directory")
        .join(DEFAULT_CONFIG_NAME)
}

pub fn file_exists_and_has_content(path: &Path) -> bool {
    path.exists() && path.metadata().map(|meta| meta.len() > 0).unwrap_or(false)
}
