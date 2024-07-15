# rpi-zero2w-recipes

This repository contains a recipe for building a minimal 64-bit OS for the Raspberry Pi Zero 2 W using [debos](https://github.com/go-debos/debos).
The OS is based on Debian Bookworm and includes the necessary firmware and modules from the [Raspberry Pi firmware](https://github.com/raspberrypi/firmware).

## Usage

To generate the OS image, run the following command with debos:

```bash
debos -t recipe_dir:${PWD} zero2w.yaml
```

This command will produce an image file (`rpi_zero2w.img`) that can be flashed to an SD card.
The default user is `user` with the password `password`.

## Enabled Modules

By specifying the eth_addr adapter, the following network-related modules are enabled:

- `cdc_ncm`
- `cdc_ether`
- `lan743x`

Example command:

```bash
debos -t eth_addr:"12:34:56:78:9a:bc" -t recipe_dir:${PWD} zero2w.yaml
```

## Customization

The repository includes various parts of the recipe stored separately to help you customize your own build.
You can modify these parts or create your own recipes based on the provided examples ([`zero2w.yaml`](zero2w.yaml)).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
