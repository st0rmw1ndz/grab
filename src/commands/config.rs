use crate::cli::{ConfigCommand, ConfigGenerateCommand, ConfigResetCommand, ConfigSubcommands};

pub fn handle_config(data: ConfigCommand) {
    match data.command {
        ConfigSubcommands::Generate(data) => handle_config_generate(data),
        ConfigSubcommands::Reset(data) => handle_config_reset(data),
    }
}

pub fn handle_config_generate(data: ConfigGenerateCommand) {
    if !data.globals.quiet {
        println!("{:#?}", data);
    }
}

pub fn handle_config_reset(data: ConfigResetCommand) {
    if !data.globals.quiet {
        println!("{:#?}", data);
    }
}
