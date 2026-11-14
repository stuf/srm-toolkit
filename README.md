Most of the contents of this is hacky and using it to learn Python to some extent.

# srm-toolkit

- Generic
  - [cli](./packages/srm-cli/)
- Blender
  - [addons](./scripts-blender/addons/) - Addons for install
  - [drawing](./scripts-blender/drawing/) - Freehand API style modules
  - [templates](./scripts-blender/templates/) - application templates for use in Blender

## `srm-cli`

CLI tool to process red-green normal maps and extract the texture alpha channel
into its own file, batch-convert `.bfres` files into `.cast`

You can do a `--dry-run` (or `-n`) to have the tool run without making changes.

```sh
srm-cli fix-normalmaps --help # fix normalmaps
srm-cli fix-alpha --help      # extract alpha channel
srm-cli conv-cast --help      # batch bfres to cast conversion
```
