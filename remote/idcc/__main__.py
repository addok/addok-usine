import minicli
from usine import config, run

from ..commons import addok, main


@minicli.cli
def fetch():
    run(f'wget {config.data_uri} --output-document=/tmp/idcc.csv --quiet')


@minicli.cli
def batch():
    addok('batch /tmp/idcc.csv')


main(configpath='remote/idcc/config.yml')
