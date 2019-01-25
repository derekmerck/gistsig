"""
gistsig
Derek Merck
Winter 2019

Sign and verify Python packages using public gists.
"""

import logging, os
from pprint import pformat
from datetime import datetime
import click
from gist import get_gist, update_gist
from pkg_sig import get_pkg_key, get_pkg_hash


@click.group()
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.option('--gist_id')
@click.option('--gist_oauth_tok')
@click.pass_context
def cli(ctx, verbose, gist_id, gist_oauth_tok):
    ctx.obj['gist_id'] = gist_id
    ctx.obj['gist_oauth_tok'] = gist_oauth_tok
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
    pass


@cli.command()
@click.argument('packages', nargs=-1)
@click.pass_context
def show(ctx, packages):
    for pkg_name in packages:
        value = get_pkg_hash(pkg_name=pkg_name)
        key = get_pkg_key(pkg_name=pkg_name)
        msg = click.style("Local package has signature {}:{}.".format(key, value), fg='yellow')
        click.echo(msg)


@click.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def pull(ctx, packages):
    gist_id = ctx.obj['gist_id']
    for pkg_name in packages:
        pkg_sigs = get_gist(gist_id=gist_id, name=pkg_name)
        msg = click.style("Reference package has signatures:", fg='yellow')
        click.echo(msg)
        click.echo(pformat(pkg_sigs))


@click.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def verify(ctx, packages):
    exit_code = 0
    gist_id = ctx.obj['gist_id']
    for pkg_name in packages:
        key = get_pkg_key(pkg_name=pkg_name)
        value = get_pkg_hash(pkg_name=pkg_name)

        pkg_sigs = get_gist(gist_id=gist_id, name=pkg_name)

        ref = None
        if pkg_sigs:
            entry = pkg_sigs.get(key)
            if entry:
                ref = entry.get('hash')

        if value != ref:
            msg = click.style("Package signature {}:{} is not valid.".format(key, value), fg='red')
            click.echo(msg)
            exit_code = 1
        else:
            msg = click.style("Package signature {}:{} is valid.".format(key, value), fg="green")
            click.echo(msg)

    exit(exit_code)


@click.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def push(ctx, packages):
    gist_id = ctx.obj['gist_id']
    gist_oauth_tok = ctx.obj['gist_oauth_tok']
    for pkg_name in packages:
        pkg_sigs = get_gist(gist_id=gist_id, name="{}.json".format(pkg_name))
        value = get_pkg_hash(pkg_name=pkg_name)
        key = get_pkg_key(pkg_name=pkg_name)
        click.echo("Submitting signature {}:{}".format(key, value))
        pkg_sigs[key] = { "hash": value,
                          "time": datetime.now().isoformat() }
        update_gist(oauth_tok=gist_oauth_tok, gist_id=gist_id,
                    name=pkg_name, content=pkg_sigs)


def _cli():
    cli.add_command(show)
    cli.add_command(pull)
    cli.add_command(verify)
    cli.add_command(push)
    cli(auto_envvar_prefix="GISTSIG", obj={})


if __name__ == "__main__":
    _cli()
