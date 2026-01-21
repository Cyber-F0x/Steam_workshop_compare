import requests
import argparse
import os
import re
import json
import pprint
import csv
import time


def is_valid_file_path(parser,arg):
    if not os.path.exists(arg):
        parser.error(f"Mod list not found {arg}")
    else:
        return arg

def check_for_error(dom_body):
    title_pattern = r"\<title\>(.*)Error\<\/title\>"
    title = re.match(title_pattern,dom_body)
    if title:
        print("An error occured searching for the collection, please double check your collection id and try again.")    
    return


def parse_mod_title(dom_body):
    title_pattern = r"\<title\>Steam Workshop::(.*)<\/title\>"
    title = re.search(title_pattern,dom_body)
    return title.group(1)   


def find_all_sub_mods(dom_body):
    json_pattern  = r"{\"id\":.*appid\":[0-9]*}"
    sub_mods = re.findall(json_pattern,dom_body)
    if not sub_mods:
        print("No mods found in the collection, exiting")
        exit()
    cleaned_list = [json.loads(mod) for mod in sub_mods]
    return cleaned_list


def parse_csv(file_path):
    currently_installed = []
    with open(file_path) as mod_list:
        csv_read = csv.reader(mod_list)
        for mods in csv_read:
            currently_installed.extend(mods)
    currently_installed = list(set(currently_installed))
    return currently_installed


def main(args):
    file_path = args.modlist
    steam_collection_id = args.collection
    installed_mods = parse_csv(file_path)
    url = f"https://steamcommunity.com/sharedfiles/filedetails?id={steam_collection_id}"
    print(f"Collection url: {url}")
    s = requests.Session()
    response = s.get(url).text
    check_for_error(response)
    collection_mods = find_all_sub_mods(response)
    for each_item in collection_mods:
        if each_item["id"] in installed_mods:
            #print(f"{each_item['title']} is installed")
            installed_mods.remove(each_item["id"])
    if len(installed_mods) == 0:
        print("Mod pack is up-to-date")
        exit()
    print(f"{len(installed_mods)} missing from collection")
    for each_missing_mod in installed_mods:
        time.sleep(5)
        url = f"https://steamcommunity.com/sharedfiles/filedetails?id={each_missing_mod}"
        s = requests.Session()
        reponse = s.get(url).text
        print(f"Missing {parse_mod_title(reponse)}, ID: {each_missing_mod} from collection")
        

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("--modlist",nargs='?',const=1, default="./modlist.csv", help="Modlist to compare",metavar="FILE",type=lambda x: is_valid_file_path(parse,x))
    parse.add_argument("--collection",help="The work shop collection you want to compare against",type=int)
    args = parse.parse_args()
    if args.collection is None:
        print("No collection Id supplied, exiting")
        exit()
    main(args)


