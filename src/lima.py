from .const import S
import docker
import psutil
import humanize
import json
from functools import partial
import os

# 

dir = os.path.expanduser("~/.lima/")
sock = dir + "gk-docker.sock"


def prepare_docker():
    m = f'docker context create lima-docker-default --docker "host=unix://{sock}"'
    os.system(m)
    os.system("docker context use lima-docker-default")


def docker_sock(vm):
    _ = [d.get("hostSocket") for d in vm["config"].get("portForwards", ())]
    return _[0] if _ else None


def _act(item, a, ctx):
    a(ctx, item)
    S.app.build_menu()


def act(action, ctx):
    return partial(_act, a=action, ctx=ctx)


def stop(ctx, item):
    os.system(f"limactl stop {ctx['name']}")


def start(ctx, item):
    h = S.menutitle
    n = ctx["name"]
    os.system(f"notify-send -t 3 '⏰' '{n} booting...'")
    os.system(f"limactl start {n}")
    activate(ctx, item)
    os.system(f"notify-send -t 1 '✅' '{n} active'")


def activate(ctx, item):
    if not "dockersock" in ctx:
        pass
    os.unlink(sock) if os.path.islink(sock) else 0
    os.symlink(ctx["dockersock"], sock)


def dkr_run(img, _):
    os.system(f"docker run -d --rm {img.tags[0]}")


def dkr_shell(img, _):
    os.system(f"wezterm start -- docker run -it '{img.tags[0]}' /bin/sh &")


def dkr_stop(cont, _):
    cont.stop()


def dkr_att(cont, _):
    os.system(f"wezterm start -- docker exec -ti {cont.id} /bin/sh &")


def add_docker_menu(subs):
    client = docker.DockerClient(base_url=f"unix://{sock}")
    subs.append(["─── docker images ───", None])
    images = client.images.list()
    if not images:
        subs.append(["No images found", None])
        return
    running_conts = client.containers.list()
    for image in images:
        tag_info = image.tags[0] if image.tags else "<none>:<none>"
        name, tag = tag_info.split(":", 1) if ":" in tag_info else (tag_info, "latest")
        size = humanize.naturalsize(image.attrs["Size"])
        created = image.attrs["Created"].split("T")[0]
        image_conts = [c for c in running_conts if c.image.id == image.id]
        has_running_conts = len(image_conts) > 0
        status_icon = "🟢" if has_running_conts else "⚫"
        image_menu = []
        image_menu.append(["Image Shell", act(dkr_shell, image)])
        if not has_running_conts:
            image_menu.append(["Image Run", act(dkr_run, image)])
        else:
            image_menu.append(["─── Running conts ───", None])
            for cont in image_conts:
                cont_name = cont.name.lstrip("/")
                cont_menu = [
                    ["Stop", act(dkr_stop, cont)],
                    ["Attach", act(dkr_att, cont)],
                ]
                image_menu.append([f"{cont_name} ({cont.short_id})", cont_menu])
        subs.append([f"{status_icon} {name}:{tag} - {size} ({created})", image_menu])


def add_vm(name, vm):
    vm["dockersock"] = _ = docker_sock(vm)
    typ, linked = "L", False
    if _:
        typ = "D"
        if os.path.islink(sock) and os.readlink(sock) == _:
            linked = True
    c = vm["config"]
    running = 0
    if vm["status"] == "Running":
        running = 1
        subs = [["Stop VM", act(stop, vm)]]
        if linked:
            status = "🟢"
            add_docker_menu(subs)
        else:
            status = "⚪"
            if vm["dockersock"]:
                subs.append(["Activate for docker cmd", act(activate, vm)])
    else:
        status = "🟣" if linked else "⚫"
        subs = [["Start VM", act(start, vm)]]
    t = f"{status} {name}"
    add = subs.append
    if running:
        pid = vm["hostAgentPID"]
        mem = humanize.naturalsize(psutil.Process(pid).memory_info().rss)
        add([f"Mem: {mem}", None])

    s = "hostname vmType cpus"
    [add([f"{i}: {vm.get(i)}", None]) for i in s.split()]
    vm = vm["config"]
    s = "arch disk memory"
    [add([f"{i}: {vm.get(i)}", None]) for i in s.split()]
    S.app.add(t, subs, parent=S.app.menu)
    return running


def build_menu():
    if not os.path.exists(dir):
        return
    S.app.add("─── lima vms ───", None)
    all = os.popen("limactl list --json").read().strip()
    all = [json.loads(s) for s in all.splitlines() if s.strip()]
    all = {i["name"]: i for i in all}
    S.menutitle.pop("lima", 0)
    if any([add_vm(name, vm) for name, vm in all.items()]):
        S.menutitle["lima"] = "•"
    S.app.set_title()


class Lima:
    build_menu = build_menu
    prepare_docker_socket = prepare_docker
