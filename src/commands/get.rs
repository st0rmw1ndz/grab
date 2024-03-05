use crate::cli::GetCommand;

pub fn handle_get(data: GetCommand) {
    if !data.globals.quiet {
        println!("{:#?}", data);
    }
}
