#!/usr/bin/env python

import os
import sys
import logging
import argparse
import simplejson
import yaml
import praw
import random
import json
import smtplib
from email.mime.text import MIMEText
import sendgrid
from sendgrid.helpers.mail import * 

from re import sub
from datetime import datetime, timedelta
from praw.errors import (InvalidUser, InvalidUserPass, RateLimitExceeded,
                        HTTPException, OAuthAppRequired)
from praw.objects import Comment, Submission


r = praw.Reddit(user_agent="newtuber/1.0")

config_file = './newtuber.json'
with open(config_file, 'r') as f:
  ignore = simplejson.load(f);

for submission in r.get_subreddit('newtubers').get_new(limit=25):
  if submission.link_flair_text == "GIVE CONTENT CRITIQUE" : 
    if submission.id in ignore:
      pass
    else:
      ignore[submission.id] = submission.id;
      sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
      from_email = Email('michaelsenpatrick@gmail.com')
      to_email = Email('michaelsenpatrick@gmail.com')
      body = "New GIVE CONTENT CRITIQUE: <a href="+submission.url+">"+submission.title+"</a>"
      content = Content('text/html',body)
      subject = "New GIVE CONTENT CRITIQUE submission"
      mail = Mail(from_email, subject, to_email, content)
      resp = sg.client.mail.send.post(request_body=mail.get())
      print(resp.status_code)
      print(resp.body)
      print(resp.headers)
      pass

with open(config_file, 'w') as wh:
  simplejson.dump(ignore, wh)
