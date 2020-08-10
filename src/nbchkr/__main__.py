import csv
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


@main.command()
@click.option('--source', help="The path to the source ipynb file")
@click.option('--submitted', help="The path to the submitted ipynb file")
@click.option('--feedback', help="The path to feedback markdown file")
@click.option('--output', help="The path to output comma separated value file")
def check(source, submitted, feedback, output):

    source_nb_node = nbchkr.utils.read(source)
    nb_node = nbchkr.utils.read(submitted)
    nb_node = nbchkr.utils.add_checks(nb_node=nb_node, source_nb_node=source_nb_node)
    score, maximum_score, feedback_md = nbchkr.utils.check(nb_node=nb_node)

    with open(f"{feedback}", "w") as f:
        f.write(feedback_md)

    with open(f"{output}", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Submission filepath", "Maximum score", "Score"])
        csv_writer.writerow([submitted, score, maximum_score])
    click.echo(f'{submitted} checked against {source}. Feedback written to {feedback} and output written to {output}.')
