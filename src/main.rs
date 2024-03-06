use clap::Parser;

use crate::cli::{Cli, Executable};
use crate::data::file_exists_and_has_content;
use crate::models::Config;

mod cli;
mod commands;
mod data;
mod models;

fn main() -> eyre::Result<()> {
    let args = Cli::parse();

    env_logger::Builder::new()
        .filter_level(args.globals.verbose.log_level_filter())
        .init();

    if !file_exists_and_has_content(&args.globals.config) {
        log::warn!("It seems the config file provided either doesn't exist, or has no data. A default will be created. You can edit this at using 'config edit'.");
        let config = Config::new();
        config.write(&args.globals.config);
    }

    args.command.execute()?;

    Ok(())
}
