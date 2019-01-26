"""
gistsig
Derek Merck
Winter 2019

Sign and verify Python packages using public gists.
"""

import logging
from pprint import pformat
from datetime import datetime
import click
from . import get_gist, update_gist
from . import get_pkg_info, get_pkg_gist


@click.group()
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.option('--gist_id', '-g', help="Public gist id with reference signatures.")
@click.option('--gist_oauth_tok', '-o', help="Github token (only if pushing new signatures)")
@click.pass_context
def cli(ctx, verbose, gist_id, gist_oauth_tok):
    """
    Perform a simple public signature lookup to verify local Python package
    files.

    \b
    Example:
    $ gistsig -g 4b0bfbca0a415655d97f36489629e1cc show diana
    Local package has signature python-diana:2.0.13:9fec66ac3f4f87f8b933c853d8d5f49bdae0c1dc
    """
    ctx.obj['gist_id'] = gist_id
    ctx.obj['gist_oauth_tok'] = gist_oauth_tok
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)
    pass


@cli.command()
@click.argument('packages', nargs=-1)
def show(packages):
    """Compute local package signature."""
    for pkg_name in packages:
        key, value = get_pkg_info(pkg_name)
        msg = click.style("Local package has signature {}:{}.".format(key, value), fg='yellow')
        click.echo(msg)


def find_gist_id(pkg_name):
    # Check the package
    gist_id = get_pkg_gist(pkg_name)
    if gist_id and \
       click.confirm("No reference gist set, use package declared gist? ({})".format(gist_id)):
        return gist_id
    click.echo("No gist found for this package")
    return None


@click.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def pull(ctx, packages):
    """Show public package signatures."""
    gist_id = ctx.obj['gist_id']
    for pkg_name in packages:

        if not gist_id:
            gist_id = find_gist_id(pkg_name)

        pkg_sigs = get_gist(gist_id=gist_id, name=pkg_name)
        msg = click.style("Reference package has signatures:", fg='yellow')
        click.echo(msg)
        click.echo(pformat(pkg_sigs))


@click.command()
@click.argument("packages", nargs=-1)
@click.pass_context
def verify(ctx, packages):
    """Compare local to public package signatures."""
    exit_code = 0
    gist_id = ctx.obj['gist_id']

    for pkg_name in packages:
        key, value = get_pkg_info(pkg_name)

        if not gist_id:
            gist_id = find_gist_id(pkg_name)

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
    """Update public package signatures"""
    gist_id = ctx.obj['gist_id']
    gist_oauth_tok = ctx.obj['gist_oauth_tok']

    if not gist_oauth_tok:
        click.echo("Need a gist oauth token to push data.  Set with envvar or on the cli.")
        exit(1)

    for pkg_name in packages:

        if not gist_id:
            gist_id = find_gist_id(pkg_name)

        pkg_sigs = get_gist(gist_id=gist_id, name="{}.json".format(pkg_name))
        key, value = get_pkg_info(pkg_name)
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
