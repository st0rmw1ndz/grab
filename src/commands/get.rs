use crate::cli::commands::get::GetCommand;
use crate::cli::Executable;

impl Executable for GetCommand {
    fn execute(&self) -> eyre::Result<()> {
        println!("{:#?}", self);

        Ok(())
    }
}
