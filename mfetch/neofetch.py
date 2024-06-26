from os.path import expanduser
import os
from mfetch.get_info import get_info
from mfetch.cimage import cimage
import click
from mfetch.get_info import run_command
from mfetch.get_info import run_command
from mfetch.get_info import get_info


@click.command()
def main():
    # Your neofetch.py code here

    path = run_command("pip show mfetch | grep Location").split(": ")[1]

    sysinfo = get_info()


    pref = {}
    try:
        pref_ = (
            open(str(expanduser("~")) + "/.config/mfetch/options").read().split("\n")
        )
    except:
        pref_ = open(str(path + "/mfetch/options")).read().split("\n")

    for pref_itm in pref_:
        try:
            var, val = pref_itm.split(" ")
            pref.update({var: val})
        except:
            False

    colon_padding = int(pref["text_spacer_size"])
    logo_padding = int(pref["logo_padding"])

    if not pref["split_symbol"] == "null":
        split_symb = "\\e[2m" + pref["split_symbol"] + "\\e[0m"
    else:
        split_symb = " "

    ## SORT OS LOGO

    big = pref["logo_big"] == "True"

    if not pref["os_logo"] == "null":
        oslogo = pref["os_logo"]
    else:
        oslogo = sysinfo["os"].lower().split(" ")[0]

    ## LOAD LOGO AND COLOUR:

    if big:
        logof = "logo-big"
    else:
        logof = "logo"
    passfile = path + "/mfetch/logos/" + oslogo + "/" + logof
    try:
        open(str(passfile + ".png"))
    except:
        passfile = path + "/mfetch/logos/linux/" + logof
    cimage(passfile)

    logo = str(open(str(expanduser("~")) + "/.cache/mfetch/currentlogo").read())
    colours = str(open(path + "/mfetch/colour/colours").read().replace("\n", ""))

    ##

    dat = {}

    try:
        dat_ = open(path + "/mfetch/logos/" + oslogo + "/dat").read().split("\n")
    except:
        dat_ = open(path + "/mfetch/logos/linux/dat").read().split("\n")

    for pref_itm in dat_:
        try:
            var, val = pref_itm.split(": ")
            dat.update({var: val})
        except:
            False

    logo_col = str("\\e[3" + str(dat["col"]) + "m")
    terminator = "\\e[0m"
    bold = "\\e[1m"

    split = ":" + " " * colon_padding

    def render_info(title, item):
        title = str(title)
        item = str(item)

        out = [
            bold,
            logo_col,
            title,
            terminator,
            split_symb,
            str(" " * colon_padding),
            (" " * (maximum_title_size - len(title))),
            item,
        ]

        return str("".join(out))

    maximum_title_size = 9

    line = [
        "",
        render_info("OS", sysinfo["os"]),
        render_info("WM", sysinfo["wm"]),
        "",
        render_info("Kernel", sysinfo["kernel"]),
        render_info("Pkgs", sysinfo["packages"]),
        "",
        render_info("CPU", sysinfo["cpu"]),
        render_info("GPU", sysinfo["gpu"]),
        render_info("Memory", sysinfo["memory"]),
        "",
        colours,
    ]


    out = []
    on = 0
    out.append("")
    for i in logo.split("\n"):

        try:
            g = line[on]
        except:
            g = ""
        """
            ^ This alowes spacing between elements also alowes
            the output to be shorter in length than the logo
        """
        on += 1
        out.append(str(i) + " " * logo_padding + str(g))

    os.system("echo -e '" + "\n".join(out) + "'")

    pass


if __name__ == "__main__":
    main()
