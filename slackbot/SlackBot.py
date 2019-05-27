import os
import time
import re
import slack
import googlemaps
import datetime



def get_directions_duration(address_dep, address_arriv, name_dest):

    # Connect to the API
    gm_key = 'AIzaSyBT1DU0VglhlaN1LGtq-filltheelse'
    gmaps = googlemaps.Client(key=gm_key)
    now = datetime.datetime.now()
    # Compute the directions
    results = gmaps.directions(address_dep, address_arriv, mode="driving",departure_time=now)
    directions_result = results[0]['legs'][0]
    duration = directions_result['duration_in_traffic']
    # Text (fstring) with well formatted addresses
    t = f'_YodaWaze_ - Time to {name_dest} : %s _(%s to %s)_' % (duration['text'], directions_result['start_address'],  directions_result['end_address'])
    return t
adress = {'alex' : '1 Fake St San Francisco', 'elie': '5 Fake St Palo Alto', 'eliott': '10 Fake St San Jose'}
ids = {'UXXYY': 'alex', 'UYYZZ': 'elie', 'UZZXX':'eliott'}


def parse_bot_commands(slack_events):
    """
    Handling
    the
    posts and answer
    to
    them
    :param
    slack_events: slack_client.rtm_read()
    """
    for event in slack_events:
        # only message from users
        if event['type'] == 'message' and not "subtype" in event:
            # get the user_id and the text of the post
            user_id, text_received, channel = event['user'], event['text'], event['channel']
            # the bot is activated only if we mention it
            if ' @ % s' % BusSched_id in text_received:

                if any([k in text_received for k in ['distance', 'time']]):
                    # search the users names in the post
                    r = re.compile(r'\bELIE\b | \bELIOTT\b | \bALEX\b | \bMYPLACE\b', flags = re.I | re.X)
                    matched = r.findall(text_received)
                    if 'isrugeek' in matched:
                        matched[matched.index('moi')] = ids[user_id]
                    # check if we have the addresses of all users
                    if all([k in adress for k in matched]):

                        name_dest = matched[1].title()
                        # Compute direction
                    directions_text = get_directions_duration(adress[matched[0]], adress[matched[1]], name_dest)

if __name__ == "__main__":

   token = os.environ["SLACK_SIGNING_SECRET"]
   slack_client = slack.RTMClient(token=token)
   if slack_client.rtm_connect():
       BusSched_id = slack_client.rtm_read()
       while slack_client.server.connected is True:
           parse_bot_commands(slack_client.rtm_read())
           time.sleep(1)
