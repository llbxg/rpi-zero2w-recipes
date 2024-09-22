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

### Ethernet　Adapter

By specifying the eth_addr adapter, the following network-related modules are enabled:

- `cdc_ncm`
- `cdc_ether`

Example command:

```bash
debos -t eth_addr:"12:34:56:78:9a:bc" -t recipe_dir:${PWD} zero2w.yaml
```

### Camera Module 3

Enable the use of Camera Module 3 (standard) by importing several modules and device tree overlays (dtbos) from the firmware. 
The setup also includes installing rpicam-apps to facilitate camera functionality. 
The detailed setup is documented in camera.yaml.

Example command:

```bash
debos -t camera_v3:"true" -t recipe_dir:${PWD} zero2w.yaml
```

## Initial Boot Partition Expansion

The first boot of the OS automatically expands the filesystem to fully utilize the available storage space on the SD card.
This feature is controlled by setting `enable_expand_rootfs: true` in the [`recipes/base.yaml`](recipes/base.yaml).

- **Tools Installed**: The script uses fdisk and parted for resizing.
- **Script and Service**: A dedicated script (expand-rootfs-partition.sh) and a systemd service (expand-rootfs-partition.service) handle the expansion process. After successful expansion, both the script and the service are automatically removed to clean up the system.

For more details on how this feature is implemented, refer to the [`zero2w.yaml`](zero2w.yaml) file.

## Customization

The repository includes various parts of the recipe stored separately to help you customize your own build.
You can modify these parts or create your own recipes based on the provided examples ([`zero2w.yaml`](zero2w.yaml)).

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
