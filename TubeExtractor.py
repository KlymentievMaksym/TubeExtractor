import sys
import os

import pytube.exceptions
from pytube import YouTube

# Commands
existing_commands_main = {"0": "exit", "1": "download from YT", "2": "configs", "help": "help"}
existing_commands_yt = {"0": "exit", "1": "video", "2": "music", "help": "help"}
existing_commands_cnfg = {"0": "exit", "1": "destination", "2": "resolution", "3": "show config", "help": "help"}
existing_commands_yt_download = {"": "start"}

# Param
links = set()
config = dict()
path = ""

# Flags
is_first_time_main = True
is_first_time_yt = True
is_first_time_cnfg = True

# Downloads
save = os.getenv('APPDATA').split("\\")
for glue in save[0:3]:
    path += f"{glue}\\"
path += "Downloads\\"


# Config file
def config_file():
    try:
        with open("config.txt", "r") as cnfg:

            all_text = cnfg.read(-1).split("\n")

            for line in all_text:
                opts = line.split(" : ")
                config[opts[0]] = opts[1]

            if __name__ == "__main__":
                main_page(destination=config["destination"], resolution=config["resolution"])
            else:
                return config

    except FileNotFoundError:
        with open("config.txt", "x") as write_cnfg:
            write_cnfg.writelines(f"destination : {path}\nresolution : 360p")
            print("config.txt is missing. Try restarting program\n")
        config_file()


# Help Page
def help_page(destination, resolution, count=0, find="main"):
    print(["\n----HELP----", "----HELP----"][count])

    if find == "main":

        for command, name in existing_commands_main.items():
            print(f"{command}: {name}")

        global is_first_time_main
        is_first_time_main = False

        config_file()

    elif find == "yt":

        for command, name in existing_commands_yt.items():
            print(f"{command}: {name}")

        global is_first_time_yt
        is_first_time_yt = False

        download_from_yt(destination, resolution)

    elif find == "cnfg":

        for command, name in existing_commands_cnfg.items():
            print(f"{command}: {name}")

        global is_first_time_cnfg
        is_first_time_cnfg = False

        config_page(destination, resolution)


def config_page(destination, resolution):
    if is_first_time_cnfg:
        help_page(destination, resolution, find="cnfg")

    destination = destination
    resolution = resolution
    local_config = config

    ask = input("\nWhat you want to change?\nAnswer: ")
    while ask not in existing_commands_cnfg:
        if ask == "":
            break
        ask = input("What you want to change?\nAnswer: ")

    if ask == "0" or ask == "":
        config_file()
    elif ask == "1":
        destination = input("Destination: ")
    elif ask == "2":
        resolution = input("Resolution: ")
    elif ask == "3":
        print("\n", local_config, sep='')
        config_page(destination, resolution)
    elif ask == "help":
        help_page(destination, resolution, find="cnfg")

    with open("config.txt", "w") as write_cnfg:

        if local_config.get("destination") == destination and ask == "1":
            print("It already was with these argument")
        else:
            local_config["destination"] = destination

        if local_config.get("resolution") == resolution and ask == "2":
            print("It already was with these argument")
        else:
            local_config["resolution"] = resolution

        write_cnfg.writelines(f"destination : {local_config['destination']}\nresolution : {local_config['resolution']}")
        print("Restarting program...")

    config_file()


# Main Page
def main_page(destination, resolution):
    if is_first_time_main:
        help_page(destination, resolution, 1)

    print('', end="\n")
    print("----MAIN PAGE----")

    global links
    links = set()

    request = input("Your request: ")

    while request not in existing_commands_main:
        print(f"{request} doesnt exists in command list!")
        request = input("Your request: ")

    if request == "0":
        sys.exit()
    elif request == "help":
        help_page(destination, resolution)
    elif request == "1":
        download_from_yt(destination, resolution, from_main=True)
    elif request == "2":
        config_page(destination, resolution)


# YouTube Page
def download_from_yt(destination, resolution, from_main=False):
    if from_main:
        help_page(destination, resolution, find="yt")

    ask = input("\nWhat you want to do?\nAnswer: ")

    if ask == "":
        config_file()
    elif ask == "0":
        sys.exit()
    elif ask == "help":
        help_page(destination, resolution, find="yt")
    elif ask == "1":
        download_page_video(destination, resolution)
    elif ask == "2":
        download_page_music(destination, resolution)


# YouTube Download Pages
# Video
def download_page_video(destination, resolution):
    print("\nLeave empty to start\n")
    link = input("Link: ")

    if link == '':
        download_from_yt(destination, resolution)

    if "https://www.youtube.com/" in link:
        links.add(link)
    else:
        print("Wrong link")

    while link != '':

        link = input("Link: ")

        while "https://www.youtube.com/" not in link:
            if link == "":
                break
            print("Wrong link")
            link = input("Link: ")

        if link == '':
            download_video(destination, resolution)
        else:
            links.add(link)

    config_file()


# Video Download
def download_video(destination, resolution):
    print("Started!\n")

    try:
        for single_link in links:

            video = YouTube(single_link)

            if resolution == "highest":
                stream = video.streams.get_highest_resolution()
            elif resolution == "lowest":
                stream = video.streams.get_lowest_resolution()
            else:
                stream = video.streams.get_by_resolution(resolution=resolution)

            try:
                vid = stream.download(output_path=destination)
            except AttributeError:
                try:
                    print("Attribute was not found, using lowest instead")
                    stream = video.streams.get_lowest_resolution()
                    print(f'{stream.resolution} was used')
                    vid = stream.download(output_path=destination)
                except AttributeError:
                    print("Something wrong with config.txt.\nReturning to menu...")
                    config_file()

            print(f"{video.title} was successfully downloaded to {vid}!")

        print("\nFinished!\n")
    except pytube.exceptions.RegexMatchError:
        print("Error: (Wrong format)")


# Music
def download_page_music(destination, resolution):
    print("\nLeave empty to start\n")
    link = input("Link: ")

    if link == '':
        download_from_yt(destination, resolution)

    if "https://www.youtube.com/" in link:
        links.add(link)
    else:
        print("Wrong link")

    while link != '':

        link = input("Link: ")

        while "https://www.youtube.com/" not in link:
            if link == "":
                break
            print("Wrong link")
            link = input("Link: ")

        if link == '':
            download_music(links, destination)
        else:
            links.add(link)

    config_file()


# Music Download
def download_music(list_of_links, destination):
    print("Started!\n")

    for single_link in list_of_links:
        try:
            video = YouTube(single_link)
            stream = video.streams.filter(only_audio=True).first()
            vid = stream.download(output_path=destination)
            base, ext = os.path.splitext(vid)
            mus = base + '.mp3'
            os.rename(vid, mus)
            print(f"{video.title} was successfully downloaded to {vid}!")
        except pytube.exceptions.RegexMatchError:
            print("\nError: (Wrong format)\n")
        except FileExistsError:
            print("File is already exists")

    print("\nFinished!\n")


# Start
config_file()
