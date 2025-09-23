# Managing Config Files

I am using GNU `stow` to manage these configuration files.

```bash
apt install stow
```

Use the following commands to use a symbolic link file instead of the config file.

```bash
stow home
stow -t ~/.config .config
```
