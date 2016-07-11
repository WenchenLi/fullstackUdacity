#!/usr/bin/env python
"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""

import logging
import webapp2
from google.appengine.api import mail, app_identity
from api import ConcentrationApi
from models import User

app_url ="https://game-backend-wc.appspot.com"

class SendReminderEmail(webapp2.RequestHandler):
    """
    send reminder to user who has active games
    """
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        user_game_dict = ConcentrationApi.gameReminderhelper()
        for email in user_game_dict:
            subject = 'You have active games!'
            body = 'Hello, you have the following games still active.'
            for game_key_url_safe  in user_game_dict[email]:
                body += "{}/game/{}".format(app_url,game_key_url_safe) + "\n"
            # This will send test emails, the arguments to send_mail are:
            # from, to, subject, body
            if user_game_dict[email]:#send email only have games active
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               email,
                               subject,
                               body)

class UpdateAverageMovesRemaining(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        ConcentrationApi._cache_average_attempts()
        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
    ('/tasks/cache_average_attempts', UpdateAverageMovesRemaining),
], debug=True)
