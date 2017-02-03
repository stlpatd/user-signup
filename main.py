import webapp2
import cgi
import re

def build_page(username, password, ver_pass, email, error_username, error_password, error_ver_pass, error_email):
    header = "<h1>Signup</h1>"
    user_label= "<label style='margin:2% 4%; font-#weight: bold; font-size: 14px; '>Username</label>"
    user_input= "<input type='text' name='username' value='{0}'>".format(username)
    #added to try and run user error
    error_username= "<p style='color:red' name='error_username' >{0}</p>".format(error_username)
    pw_label= "<label style='margin:2% 4%; font-#weight: bold; font-size: 14px; '>Password</label>"
    pw_input= "<input type='password' name='password' value=''>".format(password)
    error_password= "<p style='color:red' name='error_password' >{0}</p>".format(error_password)
    ver_pw_label= "<label style='margin:2% 4%; font-#weight: bold; font-size: 14px; '>Verify Password</label>"
    ver_pw_input= "<input type='password' name='ver_pass' value=''>".format(ver_pass)
    error_ver_pass= "<p style='color:red' name='error_ver_pass' >{0}</p>".format(error_ver_pass)
    email_label= "<label style='margin:2% 4%; font-#weight: bold; font-size: 14px; '>Email (optional)</label>"
    email_input= "<input type='text' name='email' value=''>".format(email)
    error_email= "<p style='color:red' name='error_email' >{0}</p>".format(error_email)
    submit= "<input type='submit'/>"
    form= "<form method='post'>" + user_label + user_input + error_username + "<br>" + pw_label + pw_input + error_password + "<br>" +ver_pw_label + ver_pw_input + error_ver_pass + "<br>" + email_label + email_input + error_email + "<br>" + submit + "</form>"

    return header + form

#added to try and validate 
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
#end of validate                                    

class Signup(webapp2.RequestHandler):
    def get(self):
       content= build_page('', '', '', '','','','','')
       self.response.write(content)
        
    def post(self):
    #added to check if error exist 
        have_error = False
    #end of error exist check
        username = self.request.get('username')
        password = self.request.get("password")
        ver_pass = self.request.get("ver_pass")
        email = self.request.get("email")
        error_username = self.request.get('error_username')
        error_password = self.request.get('error_password')
        error_ver_pass = self.request.get('error_ver_pass')
        error_email = self.request.get('error_email')
        
        #self.response.write(content)  #<-comment out to try and get validate to work
            
        if not valid_username(username):
            error_username= "That's not a valid username."
            have_error= True
        if not valid_password(password):
            error_password= "That's not a valid password."
            have_error= True
        if password != ver_pass:
            error_ver_pass = "Your passwords didn't match."
            have_error= True
        if not valid_email(email):
            error_email= "Please enter a valid email."
        if have_error:
            content= build_page(username, password, ver_pass, email, error_username, error_password, error_ver_pass, error_email)
            self.response.out.write(content)
        else:
            self.redirect('/welcome?username=' + username)
            
class Welcome(webapp2.RequestHandler):
    def get(self):
        username= self.request.get('username')
        if valid_username(username):
            self.response.write("Hello, " + username)
        else:
            self.redirect('Signup')
        

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/signup', Signup),
    ('/welcome', Welcome)
    ], debug=True)
