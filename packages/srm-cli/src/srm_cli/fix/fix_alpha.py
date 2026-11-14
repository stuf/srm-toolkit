from pathlib import Path
from typing import Annotated

import async_typer as typer
from PIL import Image
from PIL.ImageOps import invert
from rich.progress import track, Progress
from srm_cli.stats import Stats

app = typer.Typer()


@app.command()
def fix_alpha(
    path: Path,
    suffix: Annotated[str, typer.Option("--suffix")] = "Alb",
    verbose: Annotated[
        bool,
        typer.Option("--verbose/--quiet", "-v/-q"),
    ] = False,
    recursive: Annotated[bool, typer.Option("--recursive", "-r")] = False,
    output_suffix: Annotated[str, typer.Option("--output-suffix")] = "Opa",
    dry_run: Annotated[bool, typer.Option("--dry-run", "-n")] = False,
):
    """Handle (usually Spl2) Alb textures that use alpha channels,
    extract alpha channel into its own texture."""

    files = path.rglob("*.png") if recursive else path.glob("*.png")
    filelist = [f for f in files if f.stem.endswith(suffix)]
    filecount = len(filelist)

    stats = Stats()
    stats.filecount = filecount

    with Progress() as progress:
        task = progress.add_task(
            "Separating alpha maps",
            total=stats.filecount,
        )

        for file in filelist:
            progress.update(
                task,
                description=f'Process {file.name}',
                advance=1,
            )

            im = Image.open(file)
            filepath = Path(file)
            opa_stem = filepath.stem.replace(suffix, "") + output_suffix

            fpp = list(filepath.parts)
            fpp[-1] = f"{opa_stem}{filepath.suffix}"
            opa_filepath = Path(*fpp)

            if opa_filepath.exists():
                stats.already_handled += 1
                continue

            alpha = im.getchannel("A")

            pix_min, _ = alpha.getextrema()

            # If the minimum alpha is 255 there is probably no alpha at all
            if pix_min == 255:
                stats.not_handled += 1
                continue

            alpha_image = Image.new("RGBA", im.size, (0, 0, 0, 255))
            alpha_image.paste(alpha, mask=alpha)
            alpha_image.convert("L")

            # Finally save the image
            if not dry_run:
                alpha_image.save(str(opa_filepath))

            stats.handled += 1


if __name__ == '__main__':
    app()
