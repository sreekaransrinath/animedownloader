import json
import requests
from bs4 import BeautifulSoup
import os
from clint.textui import progress
import time


def searchAnimepahe(query):
    r = requests.get("https://animepahe.com/api?m=search&q="+query)
    results = json.loads(r.text)
    if (results["total"] == '0'): return None, -1
    for idx, i in enumerate(results["data"]):
        print("{0} - {1} ".format(idx, results["data"][idx]["title"]), end='')
        if (results["data"][idx]["type"] != "TV"):
            print("({0})".format(results["data"][idx]["type"]), end='')
        print()
    choice = int(input("Choose your anime (or -1 to quit): "))

    return results["data"][choice]["title"], results["data"][choice]["id"]


def countEpisodesAnimepahe(anime_id):
    r = requests.get("https://animepahe.com/api?m=release&id={0}".format(anime_id))
    results = json.loads(r.text)
    return results["total"]


def getEpisodeIdAnimepahe(anime_id, ep):
    page = int((ep-1) / 30)
    idx = int((ep-1) % 30)
    r = requests.get("https://animepahe.com/api?m=release&id={0}&sort=episode_asc&page={1}".format(anime_id, page))
    results = json.loads(r.text)
    return results["data"][idx]["id"]


def getKwikVideoUrl(episode_id):
    r = requests.get("https://animepahe.com/api?m=embed&id={0}&p=kwik".format(episode_id))
    results = json.loads(r.text)
    try:
        return results["data"][str(episode_id)]["720p"]["url"][18:]
    except KeyError:
        return None  


def getKwikDownloadUrl(kwik_id):
    r = requests.session()
    test = r.get("https://kwik.cx/f/"+kwik_id, headers={'Referer': 'https://kwik.cx/e/'+kwik_id})
    html = test.text

    soup = BeautifulSoup(html, "html.parser")
    token = soup.input["value"]

    payload = {'_token': token}
    header = {'Host': 'kwik.cx','Referer': 'https://kwik.cx/f/'+kwik_id}
    post = r.post("https://kwik.cx/d/"+kwik_id, headers=header, data=payload)
    return post.url


def downloadVideo(title, episode, link):
    if (link == "Sorry, but this video link is broken. Please try another host/quality."):
        print(link)
        return

    for x in range(5):
        try:
            r = requests.get(link, stream=True)
        except ConnectionError:
            print("Connection error, retrying in 10 seconds...")
            time.sleep(10)
    
    folder_name = str(title)
    if os.path.isdir(folder_name) == False:
        os.mkdir(folder_name)
    path = folder_name+'/'+str(title)+' Episode '+str(episode)+'.mp4'
    with open(path, 'wb') as f:
        try:
            total_length = int(r.headers.get('content-length'))
        except TypeError:
            return 1
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
    return 0


print("********** ANIMEPAHE + KWIK DOWNLOADER V0.1.5 **********")
while (True):
    print("========== SEARCH ==========")
    search = input("Type search query: ")
    if (search == "-1"): break
    anime_title, anime_id = searchAnimepahe(search)
    if (anime_id == -1): continue
    ep_count = countEpisodesAnimepahe(anime_id)

    last_ep_fname = os.path.join(anime_title, 'last_ep_finished.txt')
    try:
        last_ep_finished = int(open(last_ep_fname, 'r').read())
    except (FileNotFoundError or ValueError) as error:
        last_ep_finished = 0

    while (True):
        print()
        choice = input("Download all episodes of {0} (or resume from last time)? (Y/N) ".format(anime_title))
        choice = choice.lower()
        if (choice == 'y'):
            if (last_ep_finished > 0):
                print('Last episode that finished downloading:', last_ep_finished)
            start_ep = last_ep_finished + 1
            end_ep = ep_count
            break
        elif (choice == 'n'): break
    
    print()
    print("Last episode of "+str(anime_title)+" is "+str(ep_count)+".")
    while (choice == 'n'):
        start_ep = int(input("Start downloading from what episode? "))
        if (start_ep <= ep_count and start_ep >= 1): break
    while (choice == 'n'):
        end_ep = int(input("Until what episode? "))
        if (end_ep >= start_ep and end_ep <= ep_count): break

    print("Feel free to terminate download by pressing Ctrl+C. Program remembers the last episode that finished downloading.")

    timeout_counter = 5
    for i in range(start_ep, end_ep+1):
        ep_id = getEpisodeIdAnimepahe(anime_id, i)
        ep_kwik_url = getKwikVideoUrl(ep_id)
        print("\tEpisode {0}".format(i))
        video_url = getKwikDownloadUrl(ep_kwik_url)
        while (timeout_counter > 0):
            download_return = downloadVideo(anime_title, i, video_url)
            if (download_return == 0): break
            timeout_counter -= 1
            if (timeout_counter == 0):
                print("Something went wrong. Skipping episode...")
                timeout_counter = 5
                break
        print('',end='')
        with open(last_ep_fname, 'w') as fileObj:
            fileObj.write(str(i))
    break
