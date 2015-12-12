import facepy
import re
import csv
import datetime
import urllib
import io

from pprint import pprint

TOKEN = 'CAAFjrq34vZCEBAL5qbkPOh6OR9Kp9wINPjZBwTCMLZAkpeUttm3jnioYl7MFncTKiVnBurYgbkBtf88Bf12F91T41LwPQphKKaZAx3VAAxtL2ZBfMCFp1KEZBpAd7XR3aISxW0Cf4ZC0PHiqaHV8SzPN9PdhZACoceq4Wbnx6juniC3akWiYmMlDjZBSCRLfNzNn3qh7PYEj5RyM4isX5ehiH'

graph = facepy.GraphAPI(TOKEN, version='2.3')

users_fetched = []

REGEX_URL = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

def main():
    with open('data-jeremy.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["link", "timestamp", "Facebook user id"])

        me = graph.get('me')

        # start depth-first recursion
        get_likes(me['id'], writer, 1)


def get_likes(user_id, writer, depth):
    if depth > 2:
        return

    if user_id in users_fetched:
        return
    else:
        users_fetched.append(user_id)

    for page in graph.get(user_id + '/statuses', page=True):
        for post in page['data']:
            date = datetime.datetime.strptime(post['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')
            if date < datetime.datetime.now() - datetime.timedelta(days=2*365):
                return

            if 'message' in post and 'likes' in post:
                links = REGEX_URL.findall(post['message'])
                if links:

                    while True:
                        try:
                            for likes in graph.get(post['id'] + '/likes', page=True):
                                for like in likes['data']:
                                    for link in links:
                                        writer.writerow([link[0].encode('utf8'), post['updated_time'], like['id']])
                                        print like['name'] + ": ", [link[0].encode('utf8'), post['updated_time'], like['id']]
                                        get_likes(like['id'], writer, depth + 1)
                        except facepy.exceptions.OAuthError:
                            continue
                        break

if __name__ == "__main__":
    main()
