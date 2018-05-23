import minicli
from usine import run, config


from ..commons import addok, restart, main


@minicli.cli
def fetch():
    run(f'wget {config.data_uri} --output-document=/tmp/data.bz2 --quiet')
    run('bunzip2 /tmp/data.bz2 --stdout > /tmp/data.json')


@minicli.cli
def batch():
    run('redis-cli config set save ""')
    addok('batch /tmp/data.json')
    addok('ngrams')
    run('redis-cli save')


@minicli.cli
def reload():
    fetch()
    run('sudo systemctl stop addok')
    addok('reset')
    batch()
    restart()


main()
