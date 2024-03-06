use std::fs;
use std::path::PathBuf;

use dialoguer::{Confirm, Input};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct Config {
    pub editor_command: String,
    pub upload_enabled: bool,
}

impl Config {
    pub fn parse(path: &PathBuf) -> Self {
        let file_data = fs::read_to_string(path).expect("Failed to read config file");

        serde_json::from_str(&file_data).expect("Failed to parse config file")
    }

    pub fn write(&self, path: &PathBuf) {
        let data = serde_json::to_string_pretty(self).expect("Failed to serialize config");

        fs::write(path, data).expect("Failed to write config data to file");
    }

    pub fn new() -> Self {
        Self {
            editor_command: if cfg!(target_os = "windows") {
                "notepad"
            } else {
                "nano"
            }
            .into(),
            upload_enabled: false,
        }
    }
}
