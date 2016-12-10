#!/usr/bin/env python
import os
import sys
import simplejson
import praw
import OAuth2Util
from re import sub
from datetime import datetime, timedelta
from praw.errors import (InvalidUser, InvalidUserPass, RateLimitExceeded,
                        HTTPException, OAuthAppRequired)
from praw.objects import Comment, Submission

USER_AGENT = "newtuber/1.0"

r = praw.Reddit( user_agent= USER_AGENT )
o = OAuth2Util.OAuth2Util(r)

config_file = './newtuber_bot.json'
with open(config_file, 'r') as f:
  ignore = simplejson.load(f);

o.refresh()

for submission in r.get_subreddit('newtubers').get_new(limit=5):
  if submission.link_flair_text == "GIVE CONTENT CRITIQUE" : 
    if submission.id in ignore:
      pass
    else:
      body = "#This is a critique thread! Here's a friendly reminder about the rules for a critique:\r\n\r\n * **2a** - In order to post your plug in a Critique thread, you **must** give meaningful feedback on at least **TWO (2)** other plugs in the thread. You should give feedback **before** posting your own plug.  \r\n\r\n * **2b** - In cases where you are the first or second plug post in a Critique thread, you may post your link before giving feedback, so long as you give feedback within ONE HOUR of your initial link. If you don't give feedback within an hour, your post will be removed. If you're a repeat offender, you will be marked as such and prohibited from posting links until your behavior improves.  \r\n\r\n See the [full rules here](https://goo.gl/qs5HAn) or in the sidebar"
      try:
        success = submission.add_comment(body)
        if success:
          ignore[submission.id] = submission.id;
      except RateLimitExceeded:
        print('Rate limit exceeded, could not post to submission id: %s' % submission.id)
      pass

with open(config_file, 'w') as wh:
  simplejson.dump(ignore, wh)
