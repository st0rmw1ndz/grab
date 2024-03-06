use std::env;
use std::path::PathBuf;

use clap::{Args, ColorChoice, Parser};
use clap_verbosity_flag::Verbosity;

use crate::data::get_default_config_path;

pub mod commands;

pub trait Executable {
    fn execute(&self) -> eyre::Result<()>;
}

#[derive(Debug, Args)]
pub struct GlobalOptions {
    #[command(flatten)]
    pub verbose: Verbosity,

    /// Path to configuration file
    #[arg(short = 'C', long, global = true)]
    #[arg(default_value = get_default_config_path().into_os_string())]
    pub config: PathBuf,
}

#[derive(Debug, Parser)]
#[command(author, about, long_about = None, after_help = env!("CARGO_PKG_REPOSITORY"), version)]
#[command(color = ColorChoice::Never, propagate_version = true)]
pub struct Cli {
    #[command(subcommand)]
    pub command: commands::Commands,

    #[command(flatten)]
    pub globals: GlobalOptions,
}
