import os
import sys

import click


@click.command()
def cli():
  # Logic that determines when to restart
  if click.confirm("Do you want to restart the CLI?"):
    click.echo("Restarting CLI...")
    executable = sys.executable
    args = sys.argv
    os.execv(executable, [executable] + args)
  else:
    click.echo("Exiting CLI.")


if __name__ == '__main__':
  cli()
