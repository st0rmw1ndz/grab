use crate::cli::{ConfigCommand, ConfigGenerateCommand, ConfigSubcommands};

pub fn handle_config(data: ConfigCommand) {
    match data.command {
        ConfigSubcommands::Generate(data) => handle_config_generate(data),
    }
}

pub fn handle_config_generate(data: ConfigGenerateCommand) {
    if !data.globals.quiet {
        println!("{:#?}", data);
    }
}
