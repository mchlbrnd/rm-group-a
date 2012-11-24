import time
import yaml
import random
from mod_python import util, Cookie, apache

PATH = '/home/michael/sites/werockit.nl/rm-group-a/respondents.yaml'
MIN_RESPONDENTS = 3
NO_AVATAR = 'no-avatar'
AVATAR = 'avatar'

def index(req):
 # check if cookie is set for respondent who already participated
 client_cookie = Cookie.get_cookie(req, 'rm-group-a')
 if client_cookie is None:
  Cookie.add_cookie(req, 'rm-group-a', 'true', expires=time.time()+31*24*3600) # expires after 1 month
 else:
  return 'You already participated.'
 
 # load current respondent conditions
 with open(PATH, 'r') as f:
  respondents = yaml.load(f)
  if respondents is None:
   respondents = []

  no_avatar_count = count_str_in_seq(NO_AVATAR, respondents)
  avatar_count = count_str_in_seq(AVATAR, respondents)

  if no_avatar_count <= MIN_RESPONDENTS and avatar_count >= MIN_RESPONDENTS:
   condition = NO_AVATAR
  elif no_avatar_count >= MIN_RESPONDENTS and avatar_count <= MIN_RESPONDENTS:
   condition = AVATAR
  else:
   condition = random.choice([NO_AVATAR, AVATAR])
 
 # write new condition entry
 with open(PATH, 'w') as f:
  respondents.append(condition)
  yaml.dump(respondents, f)
 util.redirect(req, condition + '.html')

def count_str_in_seq(s, seq):
	return len([v for v in seq if v == s])
