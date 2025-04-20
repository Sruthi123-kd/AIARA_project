from flask import *
from database import *

admin=Blueprint("admin",__name__)

@admin.route('/adminhome')
def adminhome():
    if 'log' in session:
        response = make_response(render_template("adminhome.html"))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response
    return render_template("adminhome.html")

@admin.route('/admin_view_user')
def admin_view_user():

    if 'log' in session:
        data={}
        a="select * from user"
        data['view']=select(a)
        response = make_response(render_template("admin_view_user.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response



    data={}
    a="select * from user"
    data['view']=select(a)


    return render_template("admin_view_user.html",data=data)


@admin.route('/admin_complaint',methods=['get','post'])
def admin_complaint():
    if 'log' in session:
        data={}
        b="select * from complaint"
        data['view']=select(b)

        if'action'in request.args:
            action=request.args['action']
            id=request.args['id']

            if action=='reply':
                q="select * from complaint where complaint_id='%s'"%(id)
                r=select(q)
                if r:
                    data['reply']=r

                if'submit'in request.form:
                    reply=request.form['reply']
                    a=" update complaint set reply='%s'where complaint_id='%s'"%(reply,id)
                    update(a)
                    return "<script>alert('Replied Complaint');window.location='/admin_complaint'</script>" 


        response = make_response(render_template("admin_complaint.html",data=data))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

    data={}
    b="select * from complaint"
    data['view']=select(b)

    if'action'in request.args:
        action=request.args['action']
        id=request.args['id']

        if action=='reply':
            q="select * from complaint where complaint_id='%s'"%(id)
            r=select(q)
            if r:
                data['reply']=r

                if'submit'in request.form:
                    reply=request.form['reply']
                    a=" update complaint set reply='%s'where complaint_id='%s'"%(reply,id)
                    update(a)
                    return "<script>alert('Replied Complaint');window.location='/admin_complaint'</script>"
    return render_template("admin_complaint.html",data=data)

@admin.route('/adminsendnotification',methods=['post','get'])
def adminnotification():
    if 'log' in session:
        if 'submit' in request.form:
            notitype=request.form['type']
            urg=request.form['urgency']
            des=request.form['description']
            noti="insert into notification values(null,'%s','%s','%s',curdate(),curtime())"%(notitype,urg,des)
            notify=insert(noti)
            print(notify)
            return "<script>alert('Notification sended');window.location='/adminsendnotification'</script>" 

        response = make_response(render_template("notifi.html"))
    else:
        response = make_response("""
            <script>
                alert('Session Expired');
                window.location.href = '/';
            </script>
        """)
    
    # Set headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response
    if 'submit' in request.form:
        notitype=request.form['type']
        urg=request.form['urgency']
        des=request.form['description']
        noti="insert into notification values(null,'%s','%s','%s',curdate(),curtime())"%(notitype,urg,des)
        notify=insert(noti)
        print(notify)

    
    return render_template("notifi.html")



