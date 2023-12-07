#!/usr/bin/python3
"""
file to practice use of Fabric
"""
from fabric.api import *
from datetime import datetime


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
    timestr = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        # create folder versions if it doesn’t exist
        local("mkdir -p versions")
        # extract the contents of a tar archive
        local(f"tar -cvzf versions/web_static_{timestr}.tgz web_static/")
        return ("versions/web_static_{}.tgz".format(timestr))
    except BaseException:
        return None
