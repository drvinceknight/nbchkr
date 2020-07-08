import pathlib
import click

import nbchkr.utils

@click.group()
def main():
    pass

@main.command()
@click.option('--source', help="The path to the source ipynb file")
@click.option('--output', help="The path to the destination ipynb file")
def release(source, output):
    nb_path = pathlib.Path(source)
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    nbchkr.utils.remove_cells(nb_node=nb_node)

    output_path = pathlib.Path(output)
    nbchkr.utils.write(output_path=output_path, nb_node=nb_node)
    click.echo(f"Solutions removed from {source}. New notebook written to {output}.")
