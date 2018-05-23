import minicli
from usine import config, run

from ..commons import addok, main


@minicli.cli
def fetch():
    run(f'wget {config.data_uri} --output-document=/tmp/data.tar.xz --quiet')
    run('tar xf /tmp/data.tar.xz --directory /tmp')


@minicli.cli
def batch():
    run('redis-cli config set save ""')
    addok('batch /tmp/zones.msgpack')
    run('redis-cli save')


main(configpath='remote/geozones/config.yml')
