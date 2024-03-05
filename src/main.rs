use clap::Parser;

use crate::cli::{Cli, Commands};
use crate::commands::config::handle_config;
use crate::commands::get::handle_get;

mod cli;
mod commands;
mod data;

fn main() {
    let args = Cli::parse();
    match args.command {
        Commands::Get(data) => handle_get(data),
        Commands::Config(data) => handle_config(data),
    }
}
