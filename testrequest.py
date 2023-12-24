import requests
import os

dir = os.getcwd()
print(dir)


supersecretauth = 'AIzaSyDugsExa9g7-bU51rQOViFG05skGLudDlQ'
youtubeChannelId = "UCL8_FK5K4vpMGxjiyM76B4w"

def getSubscriberCount(channelId: str, authKey: str):
    response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?id={channelId}&part=statistics&key={authKey}")
    data: dict = response.json()
    return (data.get('items', [])[0]
            .get('statistics', {})
            .get('subscriberCount', 0))

def parseSubCount(subCount: str):
    num = float('{:.3g}'.format(int(subCount)))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

subscriberCount = getSubscriberCount(youtubeChannelId, supersecretauth)
displayString = parseSubCount(subscriberCount)

print(displayString)
