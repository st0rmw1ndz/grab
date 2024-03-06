use std::path::PathBuf;
use std::process::Command;
use std::str::FromStr;

use which::which;

use crate::cli::commands::edit::EditCommand;
use crate::cli::Executable;
use crate::models::Config;

pub fn create_edit_command(editor_command: &str, file_path: &PathBuf) -> eyre::Result<Command> {
    let command_line = shlex::split(editor_command).expect("Can't parse editor");
    let (command, args) = command_line.split_at(1);
    let command_path = which(&command[0]).expect("Failed to find command in PATH");

    let mut command = Command::new(command_path);
    command.args(args);
    command.arg(file_path);

    Ok(command)
}

impl Executable for EditCommand {
    fn execute(&self) -> eyre::Result<()> {
        let config = Config::parse(&self.globals.config);

        let file_path = PathBuf::from_str(&self.name).expect("Failed to find paste");
        let command = create_edit_command(&config.editor_command, &file_path);
        let _ = command?.output()?;

        Ok(())
    }
}
