import facepy
import re
import csv
import datetime
import urllib

from pprint import pprint

TOKEN = 'CAAFjrq34vZCEBANIsDLDPNEtd48RZCW5goTaf8zn3oHKjTtxlBAqx1mgJylb48HgsAYZAslLPFyhfmp3zkTIUtR7NPU70nvp2eEB7JNGAMNcXatg8AZBacEZBlwLJVM67gnM2fLxWCs3nmJ43jVxeW3Vs9Yplmj2TpxF8QO4Aesqjv4R9sEGehzJmQvZBEkYMGzfhrBxzvL5x0QcUDZArnqS45ZApqFihI0ZD'

graph = facepy.GraphAPI(TOKEN, version='2.3')

users_fetched = []

def main():
    with open('data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["link", "timestamp", "Facebook user id"])

        me = graph.get('me')

        # start depth-first recursion
        get_likes(me['id'], writer, 1)


def get_likes(user_id, writer, depth):
    if depth > 4:
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
                links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post['message'])
                if links:
                    for likes in graph.get(post['id'] + '/likes', page=True):
                        for like in likes['data']:
                            for link in links:
                                writer.writerow([link, post['updated_time'], like['id']])
                                print like['name'] + ": ", [link, post['updated_time'], like['id']]
                                get_likes(like['id'], writer, depth + 1)

if __name__ == "__main__":
    main()
