from flask import *
from database import *

public=Blueprint("public",__name__)

@public.route('/')
def home():
    return render_template("home.html")

@public.route('/login',methods=['post','get'])
def login():
    if 'submit' in request.form:
        username=request.form['user']
        password=request.form['pass']
        print(username,password)
        sql="select * from login where username='%s'AND password='%s'"%(username,password)
        db=select(sql)
        if db:
            session['log']=db[0]['login_id']
        print(db)
        if db:
            if db[0]['usertype']=='admin':
                return redirect(url_for('admin.adminhome'))
            
            if db[0]['usertype']=='user':
                qry = " select * from user where login_id='%s'"%(session['log'])
                res =select(qry)
                if res:
                    session['user']=res[0]['user_id']

                return redirect(url_for('user.userpage'))

    return render_template("login.html")

@public.route('/register',methods=['post','get'])
def register():
    if 'submit' in request.form:
        first=request.form['fname']
        last=request.form['lname']
        emal=request.form['mail']
        phno=request.form['phone']
        plc=request.form['place']
        # regdate=request.form['date']
        username=request.form['name']
        password=request.form['pass']
        check_username_query = "SELECT * FROM login WHERE username = '%s'" % (username)
        existing_user = select(check_username_query)

        if existing_user:
                return """
                    <script>
                        alert('Username already exists! Please choose a different username.');
                        window.history.back();
                    </script>
                """

            # *2. Check if Faculty Member with Same Email or Phone Exists*
        check_faculty_query = "SELECT * FROM user WHERE email = '%s' OR phone = '%s'" % (emal,phno)
        existing_faculty = select(check_faculty_query)

        if existing_faculty:
                return """
                    <script>
                        alert('A faculty member with the same email or phone number already exists.');
                        window.history.back();
                    </script>
                """
        regdb="insert into login values(null,'%s','%s','user')"%(username,password)
        regins=insert(regdb)
        print(regins)

        reguser="insert into user values(null,'%s','%s','%s','%s','%s','%s',curdate())"%(regins,first,last,emal,phno,plc)
        ins=insert(reguser)
        print(ins)
        return "<script>alert('Registration Done!');window.location='/login'</script>"
      
    return render_template("register.html")



@public.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@public.route('/aboutus')
def about():
    return render_template('aboutus.html')






        

