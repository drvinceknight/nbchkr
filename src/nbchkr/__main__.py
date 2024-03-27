import glob
import pathlib
import re
import time
import pandas as pd
import humanize
import typer

import nbchkr.utils

app = typer.Typer()


@app.command()
def release(
    source: pathlib.Path = typer.Option(..., help="The path to the source ipynb file"),
    output: pathlib.Path = typer.Option(
        ..., help="The path to the destination ipynb file"
    ),
):
    """
    This releases a piece of coursework by removing the solutions and checks from a source.
    """
    # TODO Add a check that all cells with no tags are markdown cells.
    nb_path = pathlib.Path(source)
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    nbchkr.utils.remove_cells(nb_node=nb_node)

    output_path = pathlib.Path(output)
    nbchkr.utils.write(output_path=output_path, nb_node=nb_node)
    typer.echo(
        f"Solutions and checks removed from {source}. New notebook written to {output}."
    )


@app.command()
def solve(
    source: pathlib.Path = typer.Option(..., help="The path to the source ipynb file"),
    output: pathlib.Path = typer.Option(
        ..., help="The path to the destination ipynb file"
    ),
):
    """
    This solves a piece of coursework by removing the checks from a source.
    """
    solution_regex = re.compile("$^")  # Matches nothing
    nb_path = pathlib.Path(source)
    nb_node = nbchkr.utils.read(nb_path=nb_path)
    nbchkr.utils.remove_cells(nb_node=nb_node, solution_regex=solution_regex)

    output_path = pathlib.Path(output)
    nbchkr.utils.write(output_path=output_path, nb_node=nb_node)
    typer.echo(f"Checks removed from {source}. New notebook written to {output}.")


@app.command()
def check(
    source: pathlib.Path = typer.Option(..., help="The path to the source ipynb file"),
    submitted: str = typer.Option(
        ..., help="The path pattern to the submitted ipynb file(s)"
    ),
    feedback_suffix: str = typer.Option(
        "-feedback.md", help="The suffix to add to the file name for the feedback"
    ),
    output: pathlib.Path = typer.Option(
        "output.csv", help="The path to output comma separated value file"
    ),
):
    """
    This checks a given submission against a source.
    """

    source_nb_node = nbchkr.utils.read(source)
    data = []

    paths_to_check = sorted(glob.iglob(submitted))
    number_of_paths_to_check = len(paths_to_check)

    for i, path in enumerate(paths_to_check):
        start_date = time.time()
        typer.echo(f"Check {i + 1}/{number_of_paths_to_check}: {path}")
        nb_node = nbchkr.utils.read(path)
        if nb_node != {}:
            tags_match = nbchkr.utils.check_tags_match(
                source_nb_node=source_nb_node, nb_node=nb_node
            )

            nb_node = nbchkr.utils.add_checks(
                nb_node=nb_node, source_nb_node=source_nb_node
            )
            try:
                score, maximum_score, feedback_md, passed_check = nbchkr.utils.check(
                    nb_node=nb_node
                )
            except TimeoutError:  # pragma: no cover
                feedback_md = "This notebook timed out."
                score, maximum_score = None, None
        else:
            score, maximum_score, feedback_md, passed_check = (
                None,
                None,
                "\tYour notebook file was not in the correct format and could not be read",
                {},
            )
            tags_match = False

        time_delta = time.time() - start_date

        measures = {
            "Submission filepath": path,
            "Score": score,
            "Maximum score": maximum_score,
            "Tags match": tags_match,
        }
        measures.update(passed_check)
        measures.update({"Run time": time_delta})

        data.append(measures)

        with open(f"{path}{feedback_suffix}", "w") as f:
            f.write(feedback_md)

        df = pd.json_normalize(data)
        df.to_csv(f"{output}")

        typer.echo(
            f"\t{path} checked against {source}. Feedback written to {path}{feedback_suffix} and output written to {output}."
        )
        if tags_match is False:
            typer.echo(f"\tWARNING: {path} has tags that do not match the source.")

        human_time_delta = humanize.precisedelta(
            time_delta, minimum_unit="seconds", format="%d"
        )
        typer.echo(f"\tFinished in {human_time_delta}")


if __name__ == "__main__":  # pragma: no cover
    app()
