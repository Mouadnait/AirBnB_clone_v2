#!/usr/bin/python3
"""
script that distributes archive to webservers
"""
from fabric.api import put, run, env, local
from datetime import datetime
from os.path import exists


env.hosts = ['100.27.12.205', '54.160.113.130']
env.user = 'ubuntu'


def do_pack():
    """ generates a .tgz archive from the contents of the web_static

    All files in the folder web_static must be added to the final archive.
    All archives must be stored in the folder versions.
    The name of the archive created must be:
        web_static_<year><month><day><hour><minute><second>.tgz
    The function do_pack must return the archive path if the archive has
    been correctly generated. Otherwise, it should return None.

    Returns:
        fabric.operations._AttributeString: archive path.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # create folder versions if it doesn’t exist
    local("mkdir -p versions")

    # extract the contents of a tar archive
    result = local(f"tar -czvf versions/web_static_{now}.tgz web_static")
    if result.failed:
        return None
    else:
        return result


def do_deploy(archive_path):
    """distributes an archive to your web servers.

    Args:
        archive_path (string): path to archive

    Returns:
        Boolean: whether the archive is distributed or not
    """
    if exists(archive_path) is False:
        return False
    try:
        # upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Uncompress the archive to the folder,
        # /data/web_static/releases/<archive filename without extension>
        # on the web server
        file_name = archive_path.split("/")[-1]
        no_ext = ("/data/web_static/releases/" + file_name.split(".")[0])
        # Create new directory for release
        run("mkdir -p {}/".format(no_ext))
        # Uncompress archive
        run("tar -xzf /tmp/{} -C {}".format(file_name, no_ext))
        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        # Move extraction to proper directory
        run("mv {0}/web_static/* {0}/".format(no_ext))
        # Delete first copy of extraction after move
        run("rm -rf {}/web_static".format(no_ext))
        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")
        # Create new the symbolic link /data/web_static/current on web server,
        # linked to the new version of your code,
        # (/data/web_static/releases/<archive filename without extension>
        run("ln -s {}/ /data/web_static/current".format(no_ext))
        print("New version deployed!")
        return True
    except FileNotFoundError:
        return False
