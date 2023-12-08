#!/usr/bin/python3
"""
script that distributes archive to webservers
"""
import os.path
from fabric.api import *
from fabric.operations import run, put, sudo
from datetime import datetime


env.hosts = ['54.172.114.96', '54.160.113.130']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """distributes an archive to your web servers.

    Args:
        archive_path (string): path to archive

    Returns:
        Boolean: whether the archive is distributed or not
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Uncompress the archive to the folder,
        # /data/web_static/releases/<archive filename without extension>
        # on the web server
        new_comp = archive_path.split("/")[-1]
        new_folder = ("/data/web_static/releases/" + new_comp.split(".")[0])
        # upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Create new directory for release
        run("mkdir -p {}".format(new_folder))
        # Untar archive
        run("tar -xzf /tmp/{} -C {}".
            format(new_comp, new_folder))
        # Delete the archive from the web server
        run("rm /tmp/{}".format(new_comp))
        # Move extraction to proper directory
        run("mv {}/web_static/* {}/".format(new_folder, new_folder))
        # Delete first copy of extraction after move
        run("rm -rf {}/web_static".format(new_folder))
        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')
        # Create new the symbolic link /data/web_static/current on web server,
        # linked to the new version of your code,
        # (/data/web_static/releases/<archive filename without extension>
        run("ln -s {} /data/web_static/current".format(new_folder))

        print('New version deployed!')
        return True
    except Exception:
        return False
