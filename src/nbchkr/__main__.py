import csv
import glob
import pathlib

import click

import nbchkr.utils


@click.group()
def main():
    """Create and check notebook assignments."""
    pass


@main.command()
@click.option("--source", help="The path to the source ipynb file")
@click.option("--output", help="The path to the destination ipynb file")
def release(source, output):
    """
    This releases a piece of coursework by removing the solutions from a source.
    """
    nb_path = pathlib.Path(source)
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    nbchkr.utils.remove_cells(nb_node=nb_node)

    output_path = pathlib.Path(output)
    nbchkr.utils.write(output_path=output_path, nb_node=nb_node)
    click.echo(f"Solutions removed from {source}. New notebook written to {output}.")


@main.command()
@click.option("--source", help="The path to the source ipynb file")
@click.option("--submitted", help="The path pattern to the submitted ipynb file(s)")
@click.option(
    "--feedback_suffix", help="The suffix to add to the file name for the feedback"
)
@click.option("--output", help="The path to output comma separated value file")
def check(source, submitted, feedback_suffix, output):
    """
    This checks a given submission against a source.
    """

    source_nb_node = nbchkr.utils.read(source)
    with open(f"{output}", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ["Submission filepath", "Score", "Maximum score", "Tags match"]
        )

        with click.progressbar(sorted(glob.iglob(submitted))) as bar:
            for path in bar:
                nb_node = nbchkr.utils.read(path)
                tags_match = nbchkr.utils.check_tags_match(
                    source_nb_node=source_nb_node, nb_node=nb_node
                )

                nb_node = nbchkr.utils.add_checks(
                    nb_node=nb_node, source_nb_node=source_nb_node
                )
                score, maximum_score, feedback_md = nbchkr.utils.check(nb_node=nb_node)

                with open(f"{path}{feedback_suffix}", "w") as f:
                    f.write(feedback_md)

                csv_writer.writerow([path, score, maximum_score, tags_match])
                click.echo(
                    f"{path} checked against {source}. Feedback written to {path}{feedback_suffix} and output written to {output}."
                )
                if tags_match is False:
                    click.echo(
                        f"WARNING: {path} has tags that do not match the source."
                    )
