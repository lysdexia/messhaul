#!/usr/bin/env python
import cherrypy, datetime, smtplib, uuid, imaplib, socket, email
from email import message, utils
from email.MIMEText import MIMEText

from Local.TimeZones import *

# TODO create cherrypy hooks for logging and error handling

# use to look up sent email info for resend
class GmailIMAP(object):

    def connect(self, retries=0):

        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_host)

        except socket.gaierror as error:
            print error
            self.mail.shutdown()
            return

        except Exception as error:
            print "connect error %s"%error
            self.mail.shutdown()
            return

        try:
            self.mail.login(self.username, self.password)

        except Exception as error:
            print error
            self.mail.shutdown()
            return

        return True


# TODO add error handling and logging
class AuthorizationEmail(object):

    def auth_text(self, _uuid):
        return """
    This email was generated. To begin the configuration process, either click on, or paste the link below. 
    
    http://kphretiq.com/new/%s

    Thanks!
    """%_uuid
   
    def auth_email(self, msg):
        smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # send message
        smtpserver.ehlo()
        smtpserver.login(msg["From"], self.password)
        smtpserver.sendmail(msg["From"], msg["To"], msg.as_string())
        smtpserver.quit()

    def auth_new_user(self, new_user_email, _uuid): 

        msg = MIMEText(self.auth_text(_uuid), _charset="utf-8")

        msg['Subject'] = """I'm an auth email."""

        msg['From'] = self.username

        msg['Reply-to'] = self.username

        msg['To'] = new_user_email

        msg["Timestamp"] = datetime.datetime.isoformat(
                datetime.datetime.now(
                    EST()
                    )
                )

        self.auth_email(msg)

if __name__ == "__main__":
    username = "scooter.phage@gmail.com"
    password = "C@f00doo"

    g = GmailIMAP()
    g.imap_host = "imap.gmail.com"
    g.username = username
    g.password = password
    #print g.connect().select("inbox")

    ae = AuthorizationEmail()
    ae.username = username
    ae.password = password
    ae.auth_new_user("doug.shawhan@gmail.com", uuid.uuid1()) 
