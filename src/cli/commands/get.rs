use clap::Args;

use crate::cli::GlobalOptions;

#[derive(Debug, Args)]
pub struct GetCommand {
    /// Name of the paste
    pub name: String,

    /// Copy the result to the clipboard
    #[arg(short = 'c', long)]
    pub copy: bool,

    #[command(flatten)]
    pub globals: GlobalOptions,
}
