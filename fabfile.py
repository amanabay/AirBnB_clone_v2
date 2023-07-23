from fabric.api import task, local
from pack_web_static import do_pack


@task
def pack():
    do_pack()
