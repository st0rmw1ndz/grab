use clap::Args;

use crate::cli::GlobalOptions;

#[derive(Debug, Args)]
pub struct EditCommand {
    /// Name of the paste
    pub name: String,

    #[command(flatten)]
    pub globals: GlobalOptions,
}
