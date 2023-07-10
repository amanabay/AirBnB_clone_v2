#!/usr/bin/python3
""" Fabric script that generated .tgz archive of web_static folder"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
         Generates a .tgz archive from the contents of the web_static folder
         of AirBnB Clone.
    """
    local("mkdir -p versions")

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(now)

    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    if result.failed:
        return None

    return "versions/{}".format(archive_name)
