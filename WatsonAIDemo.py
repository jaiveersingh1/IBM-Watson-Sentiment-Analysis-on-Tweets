import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle, count_tweets):
    twitter_consumer_key = 'H5hcMDj7RimnmAKiXHIa3sTva'
    twitter_consumer_secret = 'u4uiGKKauTCjj831Kd3ZBb0mUQkWQHaUM17r5OlkrKqfnih3Ll'
    twitter_access_token = '4207694353-NhSzLcQDQfWpKcs3N0B3AllPW6dTSCEJ3atQR8b'
    twitter_access_secret = 'HVNcV2LvP11vWTgLVmI0ihgqSCndE7wYeLsCusqTiTI4J'
    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret = twitter_consumer_secret, access_token_key = twitter_access_token, access_token_secret=twitter_access_secret)
    statuses = twitter_api.GetUserTimeline(screen_name=handle, count=count_tweets, include_rts=False)
    text = ""
    pi_username = "08a4dc26-4091-4d5b-8046-d714e03a0602"
    pi_password = "O03PuGNBOQeT"
    personality_insights = PersonalityInsights(username=pi_username, password=pi_password)
    for status in statuses:
        if (status.lang == 'en'):
            text += status.text.encode('utf-8')
    pi_result = personality_insights.profile(text)
    return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data

user_handle = "@realDonaldTrump"
user_long_term = analyze(user_handle, 200)
user_short_term = analyze(user_handle, 5)
user = flatten(user_long_term)
user2 = flatten(user_short_term)
compared_results = compare(user, user2)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1), reverse=True)
print "We are comparing " + user_handle + "'s most recent 5 tweets to their overall \
    historical tweets. This simple demo can be expanded into a more complex tool \
    to identify 'Twitter rants' and potentially stop them before they occur."
for keys, value in sorted_result[:5]:
    print "Identified trait: " + keys
    print "Long term trait value: " + str(user[keys])
    print "Short term trait value: " + str(user2[keys])
