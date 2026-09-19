# srm-toolkit

- [cli](./scripts/srm-cli/)
- [addons](./scripts-blender/addons/)

## `srm-cli`

CLI tool to process red-green normal maps and extract the texture alpha channel
into its own file.

You can do a `--dry-run` to have the tool run without making changes.

```sh
srm-cli normals --dry-run path/to/dir
```

```sh
srm-cli alpha --dry-run path/to/dir
```
