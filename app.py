import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client
import datetime

app = flask.Flask(__name__)

@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  return json.dumps({'accessToken':credentials.access_token})
  #import ipdb;ipdb.set_trace()
  #if credentials.access_token_expired:
  #  return flask.redirect(flask.url_for('oauth2callback'))
  #else:
  #  http_auth = credentials.authorize(httplib2.Http())
  #  service = discovery.build('calendar', 'v3', http=http_auth)
    #now = datetime.datetime.utcnow().isoformat() + 'Z' 
    #print('Getting the upcoming 10 events')
    #eventsResult = service.events().list(
    #    calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    #    orderBy='startTime').execute()
    #events = eventsResult.get('items', [])
    #if not events:
    #    print('No upcoming events found.')
    #for event in events:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])
    #return json.dumps(events)
	#

@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secret.json',
      scope=[
          'https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.readonly'
      ],
      redirect_uri=flask.url_for('oauth2callback', _external=True))
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run(host="0.0.0.0")
