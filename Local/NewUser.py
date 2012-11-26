import cherrypy, json, time, re, urllib, urllib2, smtplib
from recaptcha.client import captcha
from couchdb import Database, Server
from xml.etree.ElementTree import tostring

class NewUser(object):

    # validate email by pattern and by top level domains
    @cherrypy.expose
    def valid_email(self, *args, **kwargs):
    
        if not "email" in kwargs:
            return json.dumps({"valid": False, "error": "No email value."})

        email = kwargs["email"]
        if not re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", email):
            return json.dumps({"valid": False, "error": "Malformed email address %s"%email})

        # load list if we don't have it
        if not hasattr(self, "tlds"):
            self.load_tlds()

        tld = email.rsplit(".", 1)[1]

        if not tld.upper() in self.tlds:
            return json.dumps({"valid": False, "error": "Invalid top-level domain (%s)."%tld})

        reply = {"valid": True, "tld": tld, "email": email}
        reply.update(self.geoip())
        return json.dumps(reply)

    # TODO: clean this up. it works but it's brittle and weak
    # TODO: should probably live in it's own mod since we will use it for
    # getting time zone information as well.
    def geoip(self):
        ip = cherrypy.request.headers["Remote-Addr"]
        key = "9a1b4ace13f8f789209e16b2b9862c925813a12150449331fa0d078a76a53b55"

        url = "http://api.ipinfodb.com/v3/ip-city/"
        data = urllib.urlencode({"ip": ip, "key": key, "format": "json"})

        #request = urllib2.Request(url, data)
        request = urllib2.Request("%s?%s"%(url, data))
        response = urllib2.urlopen(request).read()
        try:
            return json.loads(response)
        except:
            return {}

    # admin can refresh tlds, this should probably be some sort of timed doo-dad
    @cherrypy.expose
    @cherrypy.tools.authenticate(allowed_groups=["admin"]) 
    def refresh(self):
        then = time.time()
        self.load_tlds()
        return json.dumps({"loaded": time.time() - then})

    # load tlds
    def load_tlds(self):
        self.tlds = [i.strip() for i in open(cherrypy.request.app.config["email"]["tlds"])]
        self.tlds.pop(0)

    # TODO clean this up, use templates, use config, possibly move to 
    # Authentication module
    @cherrypy.expose
    def captcha_check(self, *args, **kwargs):

        if not "recaptcha_challenge_field" in kwargs:
            raise cherrypy.HTTPRedirect("/new_user?error=No captcha challenge field. That is totally weird. Please try reloading the page.")

        if not "recaptcha_response_field" in kwargs:
            raise cherrypy.HTTPRedirect("/new_user?error=No captcha response field. That is totally weird. Please try reloading the page.")


        recaptcha_challenge_field = kwargs["recaptcha_challenge_field"]
        recaptcha_response_field = kwargs["recaptcha_response_field"]

        captcha_results = captcha.submit(
                recaptcha_challenge_field,
                recaptcha_response_field,
                cherrypy.request.app.config["captcha"]["private"],
                cherrypy.request.headers["Remote-Addr"],)

        if captcha_results.is_valid:
            # TODO redirect to "your email should get a code" page
            return "valid"

        if captcha_results.error_code:
            # needs an error message
            if captcha_results.error_code == "invalid-site-private-key":
                # TODO log and alert operator
                pass
            raise cherrypy.HTTPRedirect("/new_user?error=%s"%
                    captcha_results.error_code)

    # TODO get ssl working!
    @cherrypy.expose
    @cherrypy.tools.mako(filename="new_user.html")
    def default(self, *args, **kwargs):
        if cherrypy.session.get("userid", None):
            raise cherrypy.HTTPRedirect("/")
        captcha_html = captcha.displayhtml(
                cherrypy.request.app.config["captcha"]["public"],
                use_ssl=False,
                error="Dadgummit")

        error = None
        if "error" in kwargs:
            error = kwargs["error"]

        if error in cherrypy.request.app.config["captcha errors"]:
            error = cherrypy.request.app.config["captcha errors"][error]

        return {"captcha": captcha_html, "error": error}

