use std::path::PathBuf;
use std::process::Command;

use dialoguer::Confirm;
use eyre::eyre;
use which::which;

use crate::cli::commands::config::{ConfigEditCommand, ConfigGenerateCommand};
use crate::cli::Executable;
use crate::models::Config;

fn confirm_overwrite(config: &PathBuf) -> eyre::Result<bool> {
    let prompt = format!(
        "Do you want to overwrite the contents of '{}' with a generated config file?",
        config.display()
    );

    Confirm::new()
        .with_prompt(prompt)
        .default(false)
        .interact()
        .map_err(|e| eyre!("Failed to interact with user: {}", e))
}

impl Executable for ConfigGenerateCommand {
    fn execute(&self) -> eyre::Result<()> {
        if !self.yes && !confirm_overwrite(&self.globals.config)? {
            println!("Cancelled.");

            return Ok(());
        }

        println!("Generating!");

        Ok(())
    }
}

impl Executable for ConfigEditCommand {
    fn execute(&self) -> eyre::Result<()> {
        let config = Config::parse(&self.globals.config);

        let command_line = shlex::split(&config.editor_command).expect("Can't parse editor");
        let (command, args) = command_line.split_at(1);
        let command_path = which(&command[0]).expect("Failed to find command in PATH");

        let mut command = Command::new(command_path);
        command.args(args);
        command.arg(self.globals.config.as_os_str());

        let _ = command.output()?;

        Ok(())
    }
}
