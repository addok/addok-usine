import minicli
from usine import config, connect, exists, put, run, sudo, template


@minicli.cli
def addok(command):
    """Run a addok command on the remote server.

    :command: the addok command to run.
    """
    with sudo(user='addok'):
        run(f'/srv/addok/venv/bin/addok {command}')


@minicli.cli
def pip(command):
    """Run a pip command on the remote server.

    :command: the pip command to run.
    """
    with sudo(user='addok'):
        run(f'/srv/addok/venv/bin/pip {command}')


@minicli.cli
def system():
    run('apt update')
    run('apt install sudo redis-server build-essential git nginx python3-dev '
        'wget tar software-properties-common gcc xz-utils python3-venv '
        'bzip2 --yes')
    # run('add-apt-repository --yes --update ppa:jonathonf/python-3.6')
    # run('apt-get install --yes python3.6 python3.6-dev python3.6-venv')
    run('mkdir -p /etc/addok')
    run('mkdir -p /var/log/addok')
    run('useradd -N addok -m -d /srv/addok/ || exit 0')
    run('chown addok:users /var/log/addok')
    run('chsh -s /bin/bash addok')


@minicli.cli
def venv():
    """Setup the python virtualenv."""
    path = '/srv/addok/venv/'
    if not exists(path):
        with sudo(user='addok'):
            run(f'python3 -m venv {path}')
    pip('install pip -U')


@minicli.cli
def http():
    conf = template('remote/gunicorn.conf', workers=config.workers)
    with sudo():
        put(conf, '/srv/addok/gunicorn.conf')
    nginx_conf = template('remote/nginx.conf', domain=config.domain)
    with sudo():
        put(nginx_conf, '/etc/nginx/sites-enabled/addok')
    # On LXC containers, somaxconn cannot be changed. This must be done on the
    # host machine.
    run(f'sudo sysctl -w net.core.somaxconn={config.connections} || exit 0')
    restart()


@minicli.cli
def bootstrap():
    system()
    service()
    venv()
    deploy()
    http()


@minicli.cli
def service():
    """Deploy/update the addok systemd service."""
    conf = template('remote/addok.service', **config)
    put(conf, '/etc/systemd/system/addok.service')
    systemctl('enable addok.service')


# @minicli.cli
# def reload():
#     fetch()
#     run('sudo systemctl stop addok')
#     addok('reset')
#     batch()
#     restart()


@minicli.cli
def deploy():
    pip(f'install {" ".join(config.packages)} gunicorn --upgrade')
    put(str(config.settings), '/etc/addok/addok.conf')
    restart()


@minicli.cli
def restart():
    run('sudo systemctl restart addok nginx')


@minicli.cli
def systemctl(*args):
    """Run a systemctl command on the remote server.

    :command: the systemctl command to run.
    """
    run(f'systemctl {" ".join(args)}')


@minicli.cli
def logs(lines=50):
    """Display the addok logs.

    :lines: number of lines to retrieve
    """
    run(f'journalctl --lines {lines} --unit addok --follow')


@minicli.wrap
def wrapper(hostname, configpath):
    configpath = ['remote/commons/config.yml', configpath]
    with connect(hostname=hostname, configpath=configpath):
        yield


def main(configpath):
    minicli.run(hostname='root@163.172.180.45', configpath=configpath)
