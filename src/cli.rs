use std::env;
use std::path::PathBuf;

use clap::{Args, ColorChoice, Parser, Subcommand};

use crate::data::get_default_config_path;

#[derive(Debug, Args)]
pub struct Globals {
    /// Suppress all output
    #[arg(short = 'q', long, global = true)]
    pub quiet: bool,

    /// Path to configuration file
    #[arg(short = 'C', long, global = true)]
    #[arg(default_value = get_default_config_path().into_os_string())]
    pub config: PathBuf,
}

#[derive(Debug, Args)]
pub struct GetCommand {
    /// Name of the paste
    pub name: String,

    /// Copy the result to the clipboard
    #[arg(short = 'c', long)]
    pub copy: bool,

    #[command(flatten)]
    pub globals: Globals,
}

#[derive(Debug, Args)]
pub struct ConfigGenerateCommand {
    /// Skip asking for confirmation
    #[arg(short = 'y', long)]
    pub yes: bool,

    #[command(flatten)]
    pub globals: Globals,
}

#[derive(Debug, Subcommand)]
pub enum ConfigSubcommands {
    /// Generate a new config
    Generate(ConfigGenerateCommand),
}

#[derive(Debug, Args)]
pub struct ConfigCommand {
    #[clap(subcommand)]
    pub command: ConfigSubcommands,
}

#[derive(Debug, Subcommand)]
pub enum Commands {
    /// Get a paste
    Get(GetCommand),

    /// Config options
    Config(ConfigCommand),
}

#[derive(Debug, Parser)]
#[command(author, about, long_about = None, after_help = env!("CARGO_PKG_REPOSITORY"), version)]
#[command(color = ColorChoice::Never, propagate_version = true)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}
