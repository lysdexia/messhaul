import cherrypy

# provides an authentication decorator
# if user is not logged in, we redirect to login screen
# if user does not have permissions for page, return to previous screen with
# error message

# authentication decorator
def authenticate(allowed_groups=None, debug=False):
    cherrypy.session["login_return_to"] = cherrypy.url()
    userid = cherrypy.session.get("userid", None)
    user_groups = cherrypy.session.get("groups", None)
 
    if not userid:
        raise cherrypy.HTTPRedirect("/login")
    # if we have group-level access, make sure we have the midiclorians to enter
    if allowed_groups:
        foo = set(allowed_groups)
        bar = set(user_groups)
        if not foo.intersection(bar):
            raise cherrypy.HTTPRedirect("/login")

# create a nice auth tool
cherrypy.tools.authenticate = cherrypy.Tool("before_handler", authenticate)
