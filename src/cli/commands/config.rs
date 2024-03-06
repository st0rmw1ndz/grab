use clap::{Args, Subcommand};

use crate::cli::GlobalOptions;

#[derive(Debug, Args)]
pub struct ConfigGenerateCommand {
    /// Skip asking for confirmation
    #[arg(short = 'y', long)]
    pub yes: bool,

    #[command(flatten)]
    pub globals: GlobalOptions,
}

#[derive(Debug, Args)]
pub struct ConfigEditCommand {
    #[command(flatten)]
    pub globals: GlobalOptions,
}

#[derive(Debug, Subcommand)]
pub enum ConfigSubcommands {
    /// Generate a new configuration file
    Generate(ConfigGenerateCommand),

    /// Open the configuration file in the default text editor
    Edit(ConfigEditCommand),
}

#[derive(Debug, Args)]
pub struct ConfigCommand {
    #[clap(subcommand)]
    pub command: ConfigSubcommands,
}
