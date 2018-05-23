# Addok-usine

Helpers to manage a remote instance of Addok using [usine](https://github.com/pyrates/usine).
Targeted on Ubuntu and Debian flavours.

**¡Experimental!**


## Usage

    python remote/{flavour} {command} --hostname xxx

Where `flavour` is one of `france`, `geozones`, `idcc` and `command` any valid
command: type `python remote/france --help` for example to see valid commands.


You can pass a configpath to override configuration (data_uri,
number of processes…):

    python remote/{flavour} {command} --hostname xxx  --configpath path/to.yml
