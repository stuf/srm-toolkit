Most of the contents of this is hacky and using it to learn Python to some extent.

# srm-toolkit

- [cli](./scripts/srm-cli/)
- [addons](./scripts-blender/addons/)

## `srm-cli`

CLI tool to process red-green normal maps and extract the texture alpha channel
into its own file.

You can do a `--dry-run` to have the tool run without making changes.

```sh
srm-cli fix-normalmaps --help # fix normalmaps
srm-cli fix-alpha --help      # extract alpha channel
srm-cli conv-cast --help      # batch bfres to cast conversion
```
