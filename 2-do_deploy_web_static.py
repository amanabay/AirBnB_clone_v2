#!/usr/bin//python3
"""
    Fabric script deploys web static to web servers
"""

from fabric.api import env, put, run
import os

env.hosts = ["34.207.211.129", "54.237.9.242"]


def do_deploy(archive_path):
    """
        Deploys the static files to the servers
        Args:
            archive_path(str): Path to static files
    """
    if not os.path.isfile(archive_path):
        return False

    file = os.path.basename(archive_path)
    folder = file.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder}/"

    try:
        put(archive_path, f"/tmp/{file}")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{file} -C {folder_path}")
        run(f"rm -rf /tmp/{file}")
        run(f"mv {folder_path}web_static/* {folder_path}")
        run(f"rm -rf {folder_path}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_path} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
