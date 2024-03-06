use clap::Subcommand;

use crate::cli::commands::config::ConfigSubcommands;
use crate::cli::Executable;

pub mod config;
pub mod edit;
pub mod get;

#[derive(Debug, Subcommand)]
pub enum Commands {
    /// Retrieve a paste by its name
    Get(get::GetCommand),

    /// Options for managing the configuration file
    Config(config::ConfigCommand),

    /// Edit a paste by its name
    Edit(edit::EditCommand),
}

impl Executable for ConfigSubcommands {
    fn execute(&self) -> eyre::Result<()> {
        match self {
            ConfigSubcommands::Generate(data) => data.execute(),
            ConfigSubcommands::Edit(data) => data.execute(),
        }
    }
}

impl Executable for Commands {
    fn execute(&self) -> eyre::Result<()> {
        match self {
            Commands::Get(sub) => sub.execute(),
            Commands::Config(sub) => sub.command.execute(),
            Commands::Edit(sub) => sub.execute(),
        }
    }
}
