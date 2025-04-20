import uuid
from flask import *
from database import *

user=Blueprint("user",__name__)

@user.route('/userhome')
def userpage():
        if 'log' in session:
            response = make_response(render_template("userhome.html"))
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
    # return render_template("userhome.html")



@user.route('/send_complaint',methods=['post','get'])
def send_complaint():
        if 'log' in session:
            data={}
            a="select * from complaint where sender_id='%s'" %(session['log'])
            res=select(a)
            if res:
                data['view']=res
            if 'submit' in request.form:
                cmptyp=request.form['type']
                desc=request.form['des']
    
                
                comdb="insert into complaint values(null,'%s','%s','%s','pending',curdate(),curtime())"%(session['log'],cmptyp,desc)
                comins=insert(comdb)
                print(comins)
                return "<script>alert('Send Complaint');window.location='/send_complaint'</script>"

            response = make_response(render_template("send_complaint.html",data=data))
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
    
        # return render_template("send_complaint.html",data=data)

@user.route('/view_notification')
def view_notification():
    if 'log' in session:
        data={}
        a="select * from notification"
        data['view']=select(a)
        response = make_response(render_template("view_notification.html",data=data))
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
    
    return render_template("view_notification.html",data=data)

# @user.route('/userpdf',methods=['post','get'])
# def userpdf():
#     if 'log' in session:
#         data = {}
#         query = """
#             SELECT * FROM user 
            
#             INNER JOIN upload_pdf ON user.login_id = upload_pdf.user_id where upload_pdf.user_id='%s'
#         """%(session['log'])
#         data['view'] = select(query)
#         if 'action' in request.args:
#             action=request.args.get('action')
#             print(action,"NNNNNNNNNNNNn")
#             id=request.args.get('id')

#             # action=request.args['action']
#             # id=request.args['id']

#             if action=='delete':
#                 qry1="delete from upload_pdf where pdf_id='%s'"% id
#                 delete(qry1)
#                 print("JJJJJJJJJJJJJJJJJJ")
#                 return "<script>alert('PDF Deleted Successfully');window.location='/userpdf'</script>"

#             if action == 'update':
#                 qry="select * from upload_pdf where pdf_id='%s'"%id
#                 reslt=select(qry)
#                 if reslt:
#                     data['up']=reslt

#                     if 'update_file' in request.form:
#                         upfile=request.files['new_file']

#                         path = 'static/pdf_files/'+str(uuid.uuid4())+upfile.filename
#                         upfile.save(path)

#                         a="update upload_pdf set file_path='%s' where pdf_id='%s'"%(path,id)
#                         b=update(a)
#                         if b:
#                             return "<script>alert('PDF Updated Successfully');window.location='/userpdf'</script>"

                    

#                         print(data,"&&&&&&&&&&&&&&&&&&")



        
#         pdf=''
#         if 'submit' in request.form:
#             pdf=request.files['file']

#             path = 'static/pdf_files/'+str(uuid.uuid4())+pdf.filename
#             pdf.save(path)

            

#             comdb="insert into upload_pdf values(null,'%s','pending','%s',curdate())"%(session['log'],path)
#             comins=insert(comdb)
#             print(comins)
#             return "<script>alert('Uploaded PDF');window.location='/userpdf'</script>"
        
#         response = make_response(render_template("userpdf.html",data=data))
#     else:
#         response = make_response("""
#             <script>
#                 alert('Session Expired');
#                 window.location.href = '/';
#             </script>
#         """)
    
#     # Set headers to prevent caching
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
    
#     return response
    
#     return render_template("userpdf.html")


@user.route('/user_view', methods=['GET', 'POST'])
def user_view():
    if 'log' in session:
        data = {}
        query1 = "SELECT * FROM user where user_id='%s'"%(session['user'])
        data['view'] = select(query1)

        print(data,"***********")
         
        if 'action' in request.args:
            action = request.args.get('action')
            user_login_id = request.args.get('id')

            print(action,user_login_id,"++++++++++++++++++")
            
            if action == 'update':
                qry1 = "SELECT * FROM user WHERE login_id=%s"%(user_login_id)
                result = select(qry1)
                # result = select(qry1, (user_id,))
                if result:
                    data['up'] = result 

                    if 'update' in request.form:
                        
                        new_firstname = request.form.get('firstname')
                        new_lastname = request.form.get('lastname')
                        new_phone = request.form.get('phone')
                        new_email = request.form.get('email')

                       
                        update_query ="UPDATE user SET firstname='%s', lastname='%s', phone='%s', email='%s' WHERE login_id='%s'"%(new_firstname, new_lastname, new_phone, new_email,user_login_id)

                        update(update_query)
                        return "<script>alert('User updated successfully');window.location='/user_view'</script>"

                    print(data, "&&&&&&&&&&&&&&&&&&")



        
        response = make_response(render_template("user_view.html", data=data))
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

