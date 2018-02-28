
# Handle Default First Page
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        # Redirect to Manage Resources at login
        #return redirect('/loadboard')
        return redirect('/manageresources')

# Handle Default First Page
@app.route('/cloud')
def cloud():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Redirect to Manage Resources at login
        #return redirect('/loadboard')
        return redirect('/loadboard')

# Handle Login Page
@app.route('/login', methods=['POST'])
def do_admin_login():
    return render_template('workorders.html')   

# Handle Login Page
@app.route('/upload', methods=['POST'])
def do_upload():
    return render_template('upload.html')  

@app.route('/workorder', methods=['POST'])
def workorder():
    return render_template('workorder.html')  

@app.route('/mobilehome', methods=['POST'])
def mobilehome():
    return render_template('mobilehome.html')   

@app.route('/mobiletime', methods=['POST'])
def mobiletime():
    return render_template('mobiletime.html')  

@app.route('/mobileexp', methods=['POST'])
def mobileexp():
    return render_template('mobileexp.html') 

@app.route('/mobilesign', methods=['POST'])
def mobilesign():
    return render_template('mobilesign.html') 

# Handle Logout
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('logged_user', None)
    session.pop('logged_user_name',None)
    return render_template('login.html')

# Handle Default First Page i.e. Loadboard
@app.route('/loadboard')
def loadboard():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('loadboard.html')
    else:
        return redirect('/')

# Handle manage resources page
@app.route('/manageresources')
def manageresources():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('manageresources.html')
    else:
        return redirect('/')

# Handle manage resources page
@app.route('/analytics')
def analytics():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('analytics.html')
    else:
        return redirect('/')

# Handle manage metadata page
@app.route('/managemetadata')
def managemetadata():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('managemetadata.html')
    else:
        return redirect('/')

# Handle manage demands page
@app.route('/managedemands')
def managedemands():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('managedemands.html')
    else:
        return redirect('/')

# Handle Bookings Page
@app.route('/bookings')
def bookings():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('bookings.html')
    else:
        return redirect('/')

# Handle Add Resource Page
@app.route('/addresource')
def addresource():

    erroraddresources = 'Resources Is Not Get Added Please Fill Proper Information'
    if 'logged_user' in session:
        logged_user = session['logged_user']
        try:
            cities = []
            cities = retrievemetadatabytype('City')
            states = []
            states = retrievemetadatabytype('State')
            trucktypes = []
            trucktypes = retrievemetadatabytype('TruckType')
            
            if session['logged_user_role'] == 'Trucker':
                vehicles = getavailablevehicles(None,logged_user)
                drivers = getavailabledrivers(logged_user,None)
                return render_template('addresource.html',drivers=drivers ,vehicles=vehicles, states = states ,cities = cities, trucktypes=trucktypes)

            truckers = []
            truckers = getalltruckers()
            customers = []
            customers = getallcustomers()
            
            return render_template('addresource.html',truckers=truckers ,customers=customers ,states = states ,cities = cities, trucktypes=trucktypes,GOOGLE_MAP_API_KEY=GOOGLE_MAP_API_KEY)
        
        except Exception as e:
            print "In Add Resources",str(e)
            return render_template('addresource.html',error=erroraddresources)
    else:
        return redirect('/')

# Handle Add Resource Page
@app.route('/addmetadata')
def addmetadata():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('addmetadata.html')
    else:
        return redirect('/')



# Update SMS details for customers & admins                
@app.route('/updatesms',methods=['POST'])
def updatesms():
    failuremessage = "Failed to update SMS! Please contact Administrator"
    try:
        if not session.get('logged_in'):
            return render_template('login.html',failure="Please login and try again")
        else:
            users = []
            users = eval(str(request.form['users']))
            contact = []
            if str(request.form['contactno1'])!="":
                contact.append(str(request.form['contactno1']))
            if str(request.form['contactno2'])!="":
                contact.append(str(request.form['contactno2']))
            if str(request.form['contactno3'])!="":
                contact.append(str(request.form['contactno3']))
            if str(request.form['contactno4'])!="":
                contact.append(str(request.form['contactno4']))
            contact = json.dumps(contact)
            smsstatus = request.form['smsstatus']

            userid = str(request.form['login_id']).strip()
            output = app._engine.execute("update tluser set smsno='{0}', smsstatus='{1}' where login_id = '{2}'".format(contact, smsstatus, userid))
            if output:
                auditmsg = "SMS Contacts successfully updated for " + userid
                message = addaudit(auditmsg)
                return render_template('manageaccount.html',success="Updated SMS contacts Successfully",users=users)

    except Exception as e:
        print "Exception is ", str(e)
        return render_template('manageaccount.html',error=failuremessage,users=users)

# Update Email details for customers
@app.route('/updateemail',methods=['POST'])
def updateemail():
    failuremessage = "Failed to update EMail! Please contact Administrator"
    try:
        if not session.get('logged_in'):
            return render_template('login.html',failure="Please login and try again")
        else:
            users = []
            users = eval(str(request.form['users']))
            email = []
            if str(request.form['emailid1'])!="":
                email.append(str(request.form['emailid1']))
            if str(request.form['emailid2'])!="":
                email.append(str(request.form['emailid2']))
            if str(request.form['emailid3'])!="":
                email.append(str(request.form['emailid3']))
            if str(request.form['emailid4'])!="":
                email.append(str(request.form['emailid4']))
            emaillist = json.dumps(email)
            emailstatus = request.form['emailstatus']

            userid = str(request.form['login_id_email']).strip()
            output = app._engine.execute("update tluser set emaillist='{0}', emailstatus='{1}' where login_id = '{2}'".format(emaillist, emailstatus, userid))
            if output:
                auditmsg = "Email Contacts successfully updated for " + userid
                message = addaudit(auditmsg)
                return render_template('manageaccount.html',success="Updated Emails Successfully",users=users)

    except Exception as e:
        print "Exception is ", str(e)
        return render_template('manageaccount.html',error=failuremessage,users=users)

# Audit method to log information to tlaudit table
@app.route('/addaudit',methods=['POST'])
def addaudit(text):

    error=None
    success=None

    login_id = str(session['logged_user']) 

    i = datetime.now(timezone('Asia/Kolkata'))
    audit_ts = i.strftime('%Y-%m-%d %H:%M')
    print "**** ==== audit_ts is: ",audit_ts

    result = app._engine.execute("insert into tlaudit (`text`, `login_id`, `audit_ts`) VALUES ('{0}','{1}','{2}')".format(text,login_id,audit_ts))

    print "Audit Completed for ", text   


# Handle Add Metadata Method
@app.route('/addmetadataelement',methods=['POST'])
def addmetadataelement():
    error=None
    success=None
    count = 0
    erroraddmetadata = "Failure adding Metadata Element... Please contact administrator"
    try:
        metadatatype = str(request.form['type']).strip()
        element = str(request.form['element']).strip()
        enabled = "yes"
       
        count = checkmetadata(element,metadatatype)
        print count
        if count == 1:
            return render_template('addmetadata.html',metadatatype=metadatatype, element=element, error='metadata already exit')
        else:
            result = app._engine.execute("insert into tlmetadata (`type`, `element`, `enabled`) VALUES ('{0}','{1}','{2}')".format(metadatatype, element, enabled))
            return render_template('addmetadata.html',success='Metadata element added successfully')
        
    except Exception as e:
        print "In Add Metadata",str(e)
        return render_template('managemetadata.html',error=erroraddmetadata)

# Handle Add Metadata Method
@app.route('/updatewelcomeemailsms',methods=['POST'])
def updatewelcomeemailsms():
    error=None
    success=None
    successaddmetadata='WelcomeSMSEmail updated Successfully...'
    erroraddmetadata="Failure adding Metadata Element... Please contact administrator"
    try:
        metadatatype1 = 'WelcomeSMS'
        welcomesmsstatus = request.form['welcomesmsstatus'];
        metadatatype2 = 'WelcomeEmail'
        welcomeemailstatus = request.form['welcomeemailstatus'];
        metadatatype3 = 'WelcomeSMSList'
        enabled = 'yes'
        contact = []
        if str(request.form['welcomecontact1'])!="":
            contact.append(str(request.form['welcomecontact1']))
        if str(request.form['welcomecontact2'])!="":
            contact.append(str(request.form['welcomecontact2']))
        if str(request.form['welcomecontact3'])!="":
            contact.append(str(request.form['welcomecontact3']))
        if str(request.form['welcomecontact4'])!="":
            contact.append(str(request.form['welcomecontact4']))
        print "7"
        if str(request.form['welcomecontact5'])!="":
            contact.append(str(request.form['welcomecontact5']))
        contact = json.dumps(contact)
        print "********Contact",contact

        metadatatype4 = 'WelcomeEmailList';
        email = []
        if str(request.form['welcomeemail1'])!="":
            email.append(str(request.form['welcomeemail1']))
        if str(request.form['welcomeemail2'])!="":
            email.append(str(request.form['welcomeemail2']))
        if str(request.form['welcomeemail3'])!="":
            email.append(str(request.form['welcomeemail3']))
        if str(request.form['welcomeemail4'])!="":
            email.append(str(request.form['welcomeemail4']))
        if str(request.form['welcomeemail5'])!="":
            email.append(str(request.form['welcomeemail5']))
        email = json.dumps(email)
        print "*****email",email

        result1 = app._engine.execute("select * from tlmetadata where type='{0}'".format(metadatatype1));
        rs1 = result1.fetchone()
        if rs1 != None:
            #Update with type 1
            app._engine.execute("update tlmetadata set element='{0}' where type='{1}'".format(welcomesmsstatus, metadatatype1))
        else:
            result = app._engine.execute("insert into tlmetadata (`type`, `element`, `enabled`) VALUES ('{0}','{1}','{2}')".format(metadatatype1, welcomesmsstatus, enabled))

        result2 = app._engine.execute("select * from tlmetadata where type='{0}'".format(metadatatype2));
        rs2 = result2.fetchone()
        if rs2 != None:
            #Update with type 2
            app._engine.execute("update tlmetadata set element='{0}' where type='{1}'".format(welcomeemailstatus, metadatatype2))
        else:
            result = app._engine.execute("insert into tlmetadata (`type`, `element`, `enabled`) VALUES ('{0}','{1}','{2}')".format(metadatatype2, welcomeemailstatus, enabled))

        result3 = app._engine.execute("select * from tlmetadata where type='{0}'".format(metadatatype3));
        rs3 = result3.fetchone()
        if rs3 != None:
            #Update with type 3
            app._engine.execute("update tlmetadata set element='{0}' where type='{1}'".format(contact, metadatatype3))
        else:
            result = app._engine.execute("insert into tlmetadata (`type`, `element`, `enabled`) VALUES ('{0}','{1}','{2}')".format(metadatatype3, contact, enabled))

        result4 = app._engine.execute("select * from tlmetadata where type='{0}'".format(metadatatype4));
        rs4 = result4.fetchone()
        if rs4 != None:
            #Update with type 4
            app._engine.execute("update tlmetadata set element='{0}' where type='{1}'".format(email, metadatatype4))
        else:
            result = app._engine.execute("insert into tlmetadata (`type`, `element`, `enabled`) VALUES ('{0}','{1}','{2}')".format(metadatatype4, email, enabled))
        return render_template('managemetadata.html',success=successaddmetadata)
    except Exception as e:
        print "In Add Metadata",str(e)
        return render_template('managemetadata.html',error=erroraddmetadata)


# Handle Select From tluser Table
@app.route('/retrieveusers',methods=['GET'])
def retrieveusers():
    error=None
    success=None
    #print "1 - Deepesh /retrieveusers >> loginid is >> ", session['logged_user']
    loginid = str(session['logged_user']).strip()
    role = str(session['logged_user_role']).strip()

    # For role as admin retrieve all truckers and not specific to login id
    
    if role == 'Admin':
        result = app._engine.execute("select tu1.login_id, table1.role as role, tu1.name, tu1.email_id, tu1.address,tu1.address1, tu1.address2, tu1.address3, tu1.pin,tu1.lat, tu1.lng, tu1.gst, tu1.lraddress1, tu1.lraddress2, tu1.lraddress3, tu1.lrpin, tu1.lrcity, tu1.lrstate, tm1.id as cityid ,tm1.element as city, tm2.id as stateid,tm2.element as state,tm4.element as lrcityname, tm5.element as lrstatename, tu1.notes, tu1.contactno, tu1.drivingsince, tu1.licensetype, tu1.license,tu1.smartphone, tu1.4g, tu1.pic, tu1.pic2, tu1.pic3, tu1.pan, tu1.aadhar, tu1.owner_name, tu1.established_year, tu1.website, tu1.pointofcontact, tu1.vehicletypes, tm3.element as vehicle_v, tu1.weighttypes, tu1.routes, tu1.registered_by,tu1.vehicleno as vehicleid , DATE_FORMAT(tu1.registered_dt, '%%Y-%%m-%%d %%T') as registered_dt,tu2.vehicleno as vehicleno,tl1.parentid as vehicle_d from (select distinct userid, role from tlroles where role in ('Driver','Trucker','Customer','Consignee','Admin','Vehicle')) as table1, tluser tu1 left join tlmetadata tm1 on (tu1.city = tm1.id) left join tlmetadata tm2 on (tu1.state = tm2.id) left join tlroles tl1 on (tu1.login_id= tl1.userid and tl1.role='Drives') left join tluser tu2 on (tl1.parentid = tu2.login_id)  left join tlmetadata tm3 on (tu1.vehicletypes = tm3.id) left join tlmetadata tm4 on (tu1.lrcity = tm4.id) left join tlmetadata tm5 on (tu1.lrstate = tm5.id) where table1.userid = tu1.login_id")
    elif role == 'Consignee':
        result = app._engine.execute("select tu1.login_id, 'Customer' as role, tu1.name,tu1.email_id, tu1.address,tu1.address1, tu1.address2, tu1.address3, tu1.pin, tu1.lat, tu1.lng, tu1.gst, tu1.lraddress1, tu1.lraddress2, tu1.lraddress3, tu1.lrpin, tu1.lrcity, tu1.lrstate, tm1.id as cityid ,tm1.element as city, tm2.id as stateid, tm2.element as state, tm4.element as lrcityname, tm5.element as lrstatename, tu1.notes, tu1.contactno, tu1.drivingsince, tu1.licensetype, tu1.license,tu1.smartphone, tu1.4g, tu1.pic, tu1.pic2, tu1.pic3, tu1.pan, tu1.aadhar, tu1.owner_name, tu1.established_year, tu1.website, tu1.pointofcontact, tu1.vehicletypes, tm3.element as vehicle_v, tu1.weighttypes, tu1.routes, tu1.registered_by,tu1.vehicleno as vehicleid , DATE_FORMAT(tu1.registered_dt, '%%Y-%%m-%%d %%T') as registered_dt,tu2.vehicleno as vehicleno,tl1.parentid as vehicle_d from tlroles tl, tluser tu1 left join tlmetadata tm1 on (tu1.city = tm1.id) left join tlmetadata tm2 on (tu1.state = tm2.id) left join tlroles tl1 on (tu1.login_id= tl1.userid and tl1.role='Drives') left join tluser tu2 on (tl1.parentid = tu2.login_id) left join tlmetadata tm3 on (tu1.vehicletypes = tm3.id) left join tlmetadata tm4 on (tu1.lrcity = tm4.id) left join tlmetadata tm5 on (tu1.lrstate = tm5.id) where tu1.login_id = tl.parentid and tl.role in ('Driver','Trucker','Customer','Consignee','Admin','Vehicle') and tl.userid='{0}'".format(loginid))
    else:    
        result = app._engine.execute("select tu1.login_id, tl.role as role, tu1.name,tu1.email_id, tu1.address,tu1.address1, tu1.address2, tu1.address3, tu1.pin, tu1.lat, tu1.lng, tu1.gst,tu1.lraddress1, tu1.lraddress2, tu1.lraddress3, tu1.lrpin, tu1.lrcity, tu1.lrstate, tm1.id as cityid ,tm1.element as city, tm2.id as stateid, tm2.element as state,tm4.element as lrcityname, tm5.element as lrstatename, tu1.notes, tu1.contactno, tu1.drivingsince, tu1.licensetype, tu1.license,tu1.smartphone, tu1.4g, tu1.pic, tu1.pic2, tu1.pic3, tu1.pan, tu1.aadhar, tu1.owner_name, tu1.established_year, tu1.website, tu1.pointofcontact, tu1.vehicletypes, tm3.element as vehicle_v, tu1.weighttypes, tu1.routes, tu1.registered_by,tu1.vehicleno as vehicleid , DATE_FORMAT(tu1.registered_dt, '%%Y-%%m-%%d %%T') as registered_dt,tu2.vehicleno as vehicleno,tl1.parentid as vehicle_d from tlroles tl, tluser tu1 left join tlmetadata tm1 on (tu1.city = tm1.id) left join tlmetadata tm2 on (tu1.state = tm2.id) left join tlroles tl1 on (tu1.login_id= tl1.userid and tl1.role='Drives') left join tluser tu2 on (tl1.parentid = tu2.login_id) left join tlmetadata tm3 on (tu1.vehicletypes = tm3.id) left join tlmetadata tm4 on (tu1.lrcity = tm4.id) left join tlmetadata tm5 on (tu1.lrstate = tm5.id) where tu1.login_id = tl.userid and tl.role in ('Driver','Trucker','Customer','Consignee','Admin','Vehicle') and tl.parentid='{0}'".format(loginid))

    # Use "dict" or dictionaries in Python, Dictionaries are unordered key value pairs in Python
    # Take one row at a time and convert all items to dict (key value pairs), also keep appending the dicts to an array
    # Finally convert the array to json and return
    # To extract first item in any row - use row[0] etc
    names = []
    for row in result:
        names.append(dict(row.items()))
    
    ## If role is Admin and if names[] contains an 'registered_dt' column then update 'registered_dt' with new 'registered_dt' date
    
    for i in range(0,len(names)):
        if names[i]['registered_dt']:
            names[i]['registered_dt'] = names[i]['registered_dt'][:-3]
    
    return json.dumps(names)

# Handle Vehicle Availability Page
@app.route('/availability')
def availability():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('availability.html')
    else:
        return redirect('/')

# Handle Select From tlmetadata Table
@app.route('/retrievemetadata',methods=['GET'])
def retrievemetadata():
    error=None
    success=None

    result = app._engine.execute("select id, element, type, enabled from tlmetadata")
    
    metadata = []
    for row in result:
        metadata.append(dict(row.items()))
    return json.dumps(metadata)

# Render automationtest.html page
@app.route('/automationtest',methods=['GET'])
def automationtest():
    if 'logged_user' in session:
        logged_user = session['logged_user']
        return render_template('automationtest.html')
    else:
        return redirect('/')

# Retrieve the test scripts for execution from tlscripts table
@app.route('/retrievetestscripts',methods=['GET'])
def retrievetestscripts():
    error=None
    success=None

    result = app._engine.execute("select id, testcaseno, testscript, expresult from tlscripts")
    
    scripts = []
    for row in result:
        scripts.append(dict(row.items()))
    return json.dumps(scripts)

# Handle button click Run Test on automation test page, execute the script and send results to automationtestresult.html
@app.route('/automationtestresult')
def automationtestresult():
    if 'logged_user' in session:
        loginid = session['logged_user']
        i = 0
        count = 0
        testresult = []
        result1 = app._engine.execute("select id, testcaseno, testscript, expresult from tlscripts")
        for row in result1:
            i = i+1
            testcaseno = str(row.items()[1][1]).strip()
            testscript = str(row.items()[2][1]).strip()
            expresult = str(row.items()[3][1]).strip()

            queryresult = app._engine.execute(testscript)
            for row in queryresult:
                count = str(row.items()[0][1]).strip()
                if count == expresult:
                    summary = 'Pass'
                else:
                    summary = 'Fail'
            testresult.append({'id':i,'testcaseno':testcaseno,'testscript':testscript,'expresult':expresult,'actualresult':count,'summary':summary})    
        print "test result is:",testresult
        return render_template('automationtestresult.html',testresult = testresult )
    else:
        return redirect('/')

@app.route('/viewuser',methods=['GET'])
def viewuser():
    print " **** Processing View User Request"
    error=None
    success=None
    userdetails=None
    if 'logged_user' in session:
        logged_user = str(session['logged_user']).strip()
        userdetails  = request.args.get('userdetails')
        userdetails = json.loads(userdetails)

        userid = userdetails["login_id"]
        
        city = userdetails["city"]
        state = userdetails["state"]

        cityid = userdetails["cityid"]
        stateid = userdetails["stateid"]

        address = userdetails["address"]
        address1 = userdetails["address1"]
        address2 = userdetails["address2"]
        address3 = userdetails["address3"]
        pincode = userdetails["pin"]
        lat = userdetails["lat"]
        lng = userdetails["lng"]
        gst = userdetails["gst"]

        email = userdetails["email_id"]
        phone = userdetails["contactno"]
        notes = userdetails["notes"]
        role=str(userdetails["role"]).strip()
        name=str(userdetails["name"]).strip()

        vehicletype= str(userdetails["vehicletypes"]).strip()
        drivingsince=str(userdetails["drivingsince"]).strip()
        smartphone=str(userdetails["smartphone"]).strip()
        license=str(userdetails["license"]).strip()
        licensetype=str(userdetails["licensetype"]).strip()
        fourg=str(userdetails["4g"]).strip()
        pic=str(userdetails["pic"]).strip()

        logged_user_role = str(session['logged_user_role']).strip()

        if role == "Vehicle":
            print " **** The Role is Vehicle "

            vehicletype_v = str(userdetails["vehicle_v"]).strip()
            pic2=str(userdetails["pic2"]).strip()
            pic3=str(userdetails["pic3"]).strip()
            driverid = getdriverforvehicle(userid)

            if driverid != "None":
                drivername = getusername(driverid)
            else:
                drivername = "None"

            if logged_user_role == 'Admin':
                parentid = getparentid(userid)
                companyname = getusername(parentid)
                return render_template('viewvehicle.html',truckerid = parentid ,truckername=companyname, userid=userid ,driverid = driverid,drivername = drivername, name=name, notes=notes,vehicletype=vehicletype_v,vehicletypeid=vehicletype,pic=pic,pic2=pic2,pic3=pic3, city=city, state=state, cityid=cityid, stateid=stateid, AWS_REGION=AWS_REGION, S3_BUCKET=S3_BUCKET)
        
            elif logged_user_role == 'Trucker':
                # Logged user is trucker, so no need to pass truckerid and truckername 
                return render_template('viewvehicle.html',userid=userid ,driverid = driverid,drivername = drivername, name=name, notes=notes,vehicletype=vehicletype_v,vehicletypeid=vehicletype,pic=pic,pic2=pic2,pic3=pic3, city=city, state=state, cityid=cityid, stateid=stateid, AWS_REGION=AWS_REGION, S3_BUCKET=S3_BUCKET)
            
        if role == "Driver":
            print " **** The Role is Driver "

            vehicleno = str(userdetails["vehicleno"]).strip()
            vehicleid = str(userdetails["vehicle_d"]).strip()

            if logged_user_role == 'Admin':
                result_p =app._engine.execute("select parentid from tlroles where role='Driver' and userid = '{0}'".format(userid))
                truckerid = result_p.first()[0]
                # Get the details of Trucker for the Driver
                truckername = getusername(truckerid)
                # Render view Driver here
                return render_template('viewdriver.html', truckername=truckername,drivername=name, address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city=city, stateid=stateid, state=state,notes=notes,smartphone=smartphone,drivingsince=drivingsince,license=license,licensetype=licensetype,fourg=fourg,pic=pic,phone=phone,email=email,driverid=userid,truckerid=truckerid,vehicleno=vehicleno,vehicleid=vehicleid, AWS_REGION=AWS_REGION,S3_BUCKET=S3_BUCKET)          
            
            elif logged_user_role == 'Trucker':
                # Logged user is trucker, so no need to pass truckerid and truckername 
                return render_template('viewdriver.html', drivername=name, address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city=city, stateid=stateid, state=state,notes=notes,smartphone=smartphone,drivingsince=drivingsince,license=license,licensetype=licensetype,fourg=fourg,pic=pic,phone=phone,email=email,driverid=userid,vehicleno=vehicleno,vehicleid=vehicleid, AWS_REGION=AWS_REGION,S3_BUCKET=S3_BUCKET)
                
        elif role == "Customer":
            print " **** The Role is Customer "

            lraddress1 = userdetails["lraddress1"]
            lraddress2 = userdetails["lraddress2"]
            lraddress3 = userdetails["lraddress3"]
            lrpincode = userdetails["lrpin"]
            lrcity = userdetails["lrcityname"]
            lrstate = userdetails["lrstatename"]
            lrcityid = userdetails["lrcity"]
            lrstateid = userdetails["lrstate"]
            website=str(userdetails["website"]).strip()
            pointofcontact=str(userdetails["pointofcontact"]).strip()

            if session['logged_user_role'] == "Admin":
                print "userid",userid

                # get all truckers for view customer
                truckers = getrelateduserid(userid,'Trucker','Y')
                print "*****list of Truckers is",truckers
                
                # get all consignee for view customer
                consignees = getrelateduserid(userid,'Consignee','Y')
                print "*****list of Consignees is",consignees

                # Render view Customer here
                return render_template('viewcustomer.html',role="Customer",userid=userid,name=name, pointofcontact=pointofcontact,address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city=city, stateid=stateid, state=state,notes=notes,phone=phone,email=email,website=website,truckers=truckers,consignees=consignees,lat=lat,lng=lng,address=address,lraddress1=lraddress1,lraddress2=lraddress2,lraddress3=lraddress3,lrpincode=lrpincode,lrcityid=lrcityid,lrstateid=lrstateid,lrcity=lrcity,lrstate=lrstate) 
            else:
                 # Render view Customer here
                return render_template('viewcustomer.html',role="Customer",userid=userid,name=name, pointofcontact=pointofcontact,address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city=city, stateid=stateid, state=state,notes=notes,phone=phone,email=email,website=website,lat=lat,lng=lng,address=address,lraddress1=lraddress1,lraddress2=lraddress2,lraddress3=lraddress3,lrpincode=lrpincode,lrcityid=lrcityid,lrstateid=lrstateid,lrcity=lrcity,lrstate=lrstate)    

        elif role == "Consignee":
            print " **** The Role is Consignee "

            lraddress1 = userdetails["lraddress1"]
            lraddress2 = userdetails["lraddress2"]
            lraddress3 = userdetails["lraddress3"]
            lrpincode = userdetails["lrpin"]
            lrcity = userdetails["lrcityname"]
            lrstate = userdetails["lrstatename"]
            lrcityid = userdetails["lrcity"]
            lrstateid = userdetails["lrstate"]
            
            lng = userdetails["lng"]
            gst = userdetails["gst"]

            if session['logged_user_role'] == "Admin":
                customer = retrievecustomer(userid)
                # Render view Consignee here
                return render_template('viewconsignee.html',name=name, address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city=city, stateid=stateid, state=state,notes=notes,phone=phone,email=email,userid=userid,customerid=customer['login_id'],customername=customer['name'],lat=lat,lng=lng,address=address,lraddress1=lraddress1,lraddress2=lraddress2,lraddress3=lraddress3,lrpincode=lrpincode,lrcityid=lrcityid,lrstateid=lrstateid,lrcity=lrcity,lrstate=lrstate)
            else:
                 # Render view Consignee here
                return render_template('viewconsignee.html',name=name, address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city=city, stateid=stateid, state=state,notes=notes,phone=phone,email=email,userid=userid,lat=lat,lng=lng,address=address,lraddress1=lraddress1,lraddress2=lraddress2,lraddress3=lraddress3,lrpincode=lrpincode,lrcityid=lrcityid,lrstateid=lrstateid,lrcity=lrcity,lrstate=lrstate)   
            
        elif role == "Trucker":
            print " **** The Role is Trucker, so the User Id will be Trucker Id"
            truckerid = userid
            aadhar=str(userdetails["aadhar"]).strip()
            pan=str(userdetails["pan"]).strip()
            gst=str(userdetails["gst"]).strip()
            website=str(userdetails["website"]).strip()
            established_year=str(userdetails["established_year"]).strip()
            owner_name=str(userdetails["owner_name"]).strip()

            ## Processing Truck Types for Display in Edit Trucker Page ####
            vehicletypes=str(userdetails["vehicletypes"]).strip()
            jsonvehicles = json.loads(vehicletypes)

            trucktype = eval(getmetdatalist('TruckType',jsonvehicles.keys()))

            value = jsonvehicles.values()
            
            cnt = len(trucktype) - 1
            while (cnt < 6):
                trucktype.append({'element':'None','id':''})
                value.append(0)
                cnt=cnt+1

            ## Processing Routes for Display in Edit Trucker Page ####
            routes=str(userdetails["routes"]).strip()
            fromcity=[]
            tocity=[]

            cities = retrievemetadatabytype('City')

            num=0
            jsonroutes = json.loads(routes)
            
            for i in jsonroutes:
                for key, val in i.iteritems():
                    fromcity.append(key)
                    tocity.append(val)

            fromcity = eval(getmetdatalist('City',fromcity))
            tocity = eval(getmetdatalist('City',tocity))
                      
            num = len(fromcity)-1
            
            while (num < 6):
                fromcity.append({'element':'None','id':''})
                tocity.append({'element':'None','id':''})
                num=num+1

            logged_user_role = str(session['logged_user_role']).strip()
            if logged_user_role == "Admin":
                 # Get all associated customers for a specific Trucker
                assoc_customers = []
                assoc_customers = getrelatedparentid(truckerid,"Trucker",'Y')
                print " The Trucker Id is ",truckerid

                # Get all drivers for a specific Trucker
                assoc_drivers = []
                assoc_drivers = getrelateduserid(truckerid,'Driver','Y')
                print "*****list of Drivers is",assoc_drivers
                
                # Get all vehicles for a specific Trucker
                assoc_vehicles = []
                assoc_vehicles = getrelateduserid(truckerid,'Vehicle','Y')
                print "*****list of Vehicles is",assoc_vehicles

                return render_template('viewtrucker.html',role="Trucker",drivers=assoc_drivers,vehicles=assoc_vehicles,customers=assoc_customers,userid=truckerid,name=name, address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city =city, stateid=stateid, state=state,notes=notes,phone=phone,email=email,pan=pan,aadhar=aadhar,website=website,established_year=established_year,owner_name=owner_name,trucktype1=trucktype[0]['element'],trucktype2=trucktype[1]['element'],trucktype3=trucktype[2]['element'],trucktype4=trucktype[3]['element'],trucktype5=trucktype[4]['element'],trucktype6=trucktype[5]['element'],value1=value[0],value2=value[1],value3=value[2],value4=value[3],value5=value[4],value6=value[5],fromcity1=fromcity[0]['element'],fromcity2=fromcity[1]['element'],fromcity3=fromcity[2]['element'],fromcity4=fromcity[3]['element'],fromcity5=fromcity[4]['element'],fromcity6=fromcity[5]['element'],tocity1=tocity[0]['element'],tocity2=tocity[1]['element'],tocity3=tocity[2]['element'],tocity4=tocity[3]['element'],tocity5=tocity[4]['element'],tocity6=tocity[5]['element'],fromcity=fromcity,tocity=tocity,vehicletypes=vehicletypes)
            else:

                # Get all drivers for a specific Trucker
                assoc_drivers = []
                assoc_drivers = getrelateduserid(truckerid,'Driver','Y')
                print "*****list of Drivers is",assoc_drivers
                
                # Get all vehicles for a specific Trucker
                assoc_vehicles = []
                assoc_vehicles = getrelateduserid(truckerid,'Vehicle','Y')
                print "*****list of Vehicles is",assoc_vehicles

                return render_template('viewtrucker.html',role="Trucker",drivers=assoc_drivers,vehicles=assoc_vehicles,userid=truckerid,name=name, address1=address1, address2=address2, address3=address3, pincode=pincode, gst=gst, cityid=cityid, city =city, stateid=stateid, state=state,notes=notes,phone=phone,email=email,pan=pan,aadhar=aadhar,website=website,established_year=established_year,owner_name=owner_name,trucktype1=trucktype[0]['element'],trucktype2=trucktype[1]['element'],trucktype3=trucktype[2]['element'],trucktype4=trucktype[3]['element'],trucktype5=trucktype[4]['element'],trucktype6=trucktype[5]['element'],value1=value[0],value2=value[1],value3=value[2],value4=value[3],value5=value[4],value6=value[5],fromcity1=fromcity[0]['element'],fromcity2=fromcity[1]['element'],fromcity3=fromcity[2]['element'],fromcity4=fromcity[3]['element'],fromcity5=fromcity[4]['element'],fromcity6=fromcity[5]['element'],tocity1=tocity[0]['element'],tocity2=tocity[1]['element'],tocity3=tocity[2]['element'],tocity4=tocity[3]['element'],tocity5=tocity[4]['element'],tocity6=tocity[5]['element'],fromcity=fromcity,tocity=tocity,vehicletypes=vehicletypes)
        
        elif role == "Admin":
            return render_template('viewadmin.html', userid=userid, name=name, email=email, phone=phone, state=state, city=city, stateid=stateid, cityid=cityid, notes=notes)
        else:
            print " **** Undefined Role "
    else:
        return redirect('/')


@app.route('/updateuser',methods=['GET','POST'])
def updateuser():
    starttime = int(round(time.time() * 1000))
    print "Start Monitoring Update{0}()".format(str(request.form['role']).strip()),starttime
    error=None
    success=None
    print " **** Processing Update User Request"
    if 'logged_user' in session:
        logged_user = session['logged_user']
        city = str(request.form['city']).strip()
        state = str(request.form['state']).strip()
        email = str(request.form['email']).strip().lower()
        phone = str(request.form['phone']).strip()
        notes = str(request.form['notes']).strip()
        name = str(request.form['name']).strip()
        address1 = str(request.form['address1']).strip().title()
        address2 = str(request.form['address2']).strip().title()
        address3 = str(request.form['address3']).strip().title()
        pincode = str(request.form['pincode']).strip()
        gst = str(request.form['gst']).strip().upper()
        userid = str(request.form['userid']).strip()
        role = str(request.form['role']).strip()

        if role == "Customer":
            successupdatecustomer = "Customer info updated successfully..."
            errorupdatecustomer = "Unable to update customer info, please fill proper details..."
            try:
                lraddress1 = str(request.form['lraddress1']).strip().title()
                lraddress2 = str(request.form['lraddress2']).strip().title()
                lraddress3 = str(request.form['lraddress3']).strip().title()
                lrpincode = str(request.form['lrpincode']).strip()
                lrcity = str(request.form['lrcity']).strip()
                lrstate = str(request.form['lrstate']).strip()                
                pointofcontact = str(request.form['pointofcontact']).strip().title()
                website=str(request.form['website']).strip().lower()
                lat = float(str(request.form['lat']).strip())
                lng = float(str(request.form['lng']).strip())
                address = str(request.form['office_add']).strip() 
                
                result = app._engine.execute("update tluser set `email_id` = '{0}', `contactno` = '{1}', `address1` = '{2}', `city` = '{3}', `state` = '{4}',`notes` = '{5}', `pointofcontact` = '{6}', `website` = '{7}', `address2` = '{8}',`address3` = '{9}',`pin` = '{10}',`lat` = '{11}',`lng` = '{12}',`gst` = '{13}',`address` = '{14}',`lraddress1` = '{15}',`lraddress2` = '{16}',`lraddress3` = '{17}',`lrpin` = '{18}',`lrcity` = '{19}',`lrstate` = '{20}' where login_id = '{21}'".format(email, phone, address1, city, state, notes, pointofcontact, website, address2, address3, pincode,lat,lng, gst, address, lraddress1, lraddress2, lraddress3, lrpincode, lrcity, lrstate, userid))
                
                print "Stop Monitoring updatecustomer()",(int(round(time.time() * 1000))-starttime)
                return render_template('manageresources.html',success=successupdatecustomer)
            
            except Exception as e:
                print "In Update Customer",str(e)
                return render_template('manageresources.html',error=errorupdatecustomer)

        if role == "Consignee":
            successupdateconsignee = "Consignee info updated successfully..."
            errorupdateconsignee = "Unable to update consignee info, please fill proper details..."
            try:
                lraddress1 = str(request.form['lraddress1']).strip().title()
                lraddress2 = str(request.form['lraddress2']).strip().title()
                lraddress3 = str(request.form['lraddress3']).strip().title()
                lrpincode = str(request.form['lrpincode']).strip()
                lrcity = str(request.form['lrcity']).strip()
                lrstate = str(request.form['lrstate']).strip() 
                lat = float(str(request.form['lat']).strip())
                lng = float(str(request.form['lng']).strip())
                address = str(request.form['office_add']).strip()
                result = app._engine.execute("update tluser set `email_id` = '{0}', `contactno` = '{1}', `address1` = '{2}', `city` = '{3}', `state` = '{4}',`notes` = '{5}',`address2` = '{6}',`address3` = '{7}',`pin` = '{8}',`gst` = '{9}',`lat` = '{10}',`lng` = '{11}',`address`= '{12}',`lraddress1` = '{13}',`lraddress2` = '{14}',`lraddress3` = '{15}',`lrpin` = '{16}',`lrcity` = '{17}',`lrstate` = '{18}' where login_id = '{19}'".format(email, phone, address1, city, state, notes, address2, address3, pincode, gst, lat, lng, address, lraddress1, lraddress2, lraddress3, lrpincode, lrcity, lrstate ,userid))
                if session['logged_user_role'] == "Admin":
                    old_customerid = str(request.form['old_customerid']).strip()
                    newcustomer_id = str(request.form['customer_con']).strip()
                    if old_customerid != newcustomer_id:
                        result1 = app._engine.execute("update tlroles set `parentid` = '{0}' where `role` = 'Consignee' and `userid`='{1}'".format(newcustomer_id,userid))
                print "Stop Monitoring updateconsignee()",(int(round(time.time() * 1000))-starttime)
                return render_template('manageresources.html',success=successupdateconsignee)
            except Exception as e:
                print "In Update Consignee",str(e)
                return render_template('manageresources.html',error=errorupdateconsignee)

        if role == "Driver":
            successupdatedriver = "Driver info updated successfully..."
            errorupdatedriver = "Unable to update driver info, please fill proper details..."
            try:
                print "1)Stop Monitoring updatedriver()",(int(round(time.time() * 1000))-starttime)
                drivingsince=str(request.form['drivingsince']).strip()
                smartphone=str(request.form['smartphone']).strip().title()
                license=str(request.form['license']).strip().upper()
                licensetype=str(request.form['licensetype']).strip().upper()
                fourg=str(request.form['fourg']).strip()

                print "2)Stop Monitoring updatedriver()",(int(round(time.time() * 1000))-starttime)
                picname = str(request.form['picname']).strip()
                print " **** Driver Image File is ", picname
                extension = os.path.splitext(picname)[1]

                print "3)Stop Monitoring updatedriver()",(int(round(time.time() * 1000))-starttime)
                if extension == "":
                    result = app._engine.execute("update tluser set `drivingsince` = '{0}', `contactno` = '{1}', `license` = '{2}', `smartphone` = '{3}', `licensetype` = '{4}',`4g` = '{5}',`address1` = '{6}',`address2` = '{7}',`address3` = '{8}',`state` = '{9}',`city` = '{10}',`pin` = '{11}',`email_id` = '{12}',`notes` = '{13}' where login_id = '{14}'".format(drivingsince,phone,license,smartphone,licensetype,fourg,address1,address2,address3,state,city,pincode,email,notes,userid))
                else:
                    result = app._engine.execute("update tluser set `drivingsince` = '{0}', `contactno` = '{1}', `license` = '{2}', `smartphone` = '{3}', `licensetype` = '{4}',`4g` = '{5}',`address1` = '{6}',`address2` = '{7}',`address3` = '{8}',`state` = '{9}',`city` = '{10}',`pin` = '{11}',`email_id` = '{12}',`notes` = '{13}',`pic` = '{14}' where login_id = '{15}'".format(drivingsince,phone,license,smartphone,licensetype,fourg,address1,address2,address3,state,city,pincode,email,notes,picname,userid))    
                print "4)Stop Monitoring updatedriver()",(int(round(time.time() * 1000))-starttime)
                
                if result:

                    new_vehicleid = str(request.form['vehicle_d']).strip()
                    old_vehicleid = str(request.form['old_vehicleid']).strip()

                    if str(session['logged_user_role']).strip() == 'Admin':
                        new_truckerid = str(request.form['trucker_d']).strip()
                        old_truckerid = str(request.form['old_truckerid']).strip()
                        
                        if old_truckerid != new_truckerid:
                            # 1) If New trucker and old trucker is different
                            result1 = app._engine.execute("update tlroles set `parentid` = '{0}' where `role` = 'Driver' and `userid`='{1}'".format(new_truckerid,userid))
                        print "5)Stop Monitoring updatedriver()",(int(round(time.time() * 1000))-starttime)
                        
                    if new_vehicleid != old_vehicleid and new_vehicleid == 'None':
                        # 2) If New and Old vehicle is different and new is None
                        result2 = app._engine.execute("delete from tlroles where userid='{0}' and role='Drives'".format(userid))

                    elif new_vehicleid != old_vehicleid and old_vehicleid == 'None':
                        # 3) If New and Old vehicle is different and old is None
                        output3 = app._engine.execute("insert into tlroles (`userid`, `role`, `parentid`) VALUES ('{0}','{1}','{2}')".format(userid,'Drives',new_vehicleid))

                    elif old_vehicleid != 'None' and new_vehicleid != 'None':
                        # 4) If New vehicle is different & both is not None
                        result4 = app._engine.execute("update tlroles set `parentid` = '{0}' where `role` = 'Drives' and `userid`='{1}'".format(new_vehicleid,userid))
                    
                    print "Stop Monitoring updatedriver()",(int(round(time.time() * 1000))-starttime)
                    return render_template('manageresources.html',success=successupdatedriver)

            except Exception as e:
                print "In Update Driver",str(e)
                return render_template('manageresources.html',error=errorupdatedriver)

        elif role == "Trucker":
            print "**** Updating trucker information"
            successupdatetrucker = "Trucker info updated successfully..."
            errorupdatetrucker = "Unable to update trucker info, please fill proper details..."
            try:
                pan = str(request.form['pan']).strip().upper()
                gst=str(request.form['gst']).strip().upper()
                aadhar=str(request.form['aadhar']).strip().upper()
                website=str(request.form['website']).strip().lower()

                owner_name=str(request.form['owner_name']).strip().title()
                established_year=str(request.form['established_year']).strip() 

                trucktype1 = str(request.form['trucktype1']).strip()
                value1 = str(request.form['value1']).strip()

                trucktype2 = str(request.form['trucktype2']).strip()
                value2 = str(request.form['value2']).strip()

                trucktype3 = str(request.form['trucktype3']).strip()
                value3 = str(request.form['value3']).strip()

                trucktype4 = str(request.form['trucktype4']).strip()
                value4 = str(request.form['value4']).strip()

                trucktype5 = str(request.form['trucktype5']).strip()
                value5 = str(request.form['value5']).strip()

                trucktype6 = str(request.form['trucktype6']).strip()
                value6 = str(request.form['value6']).strip()

                print "trucktype6",trucktype6
                trucktypesdata = {}
                if ((trucktype1 != "None") & (int(value1) > 0)):
                    trucktypesdata[trucktype1] = value1
                if ((trucktype2 != "None") & (int(value2) > 0)):       
                    trucktypesdata[trucktype2] = value2    
                if ((trucktype3 != "None") & (int(value3) > 0)):
                    trucktypesdata[trucktype3] = value3
                if ((trucktype4 != "None") & (int(value4) > 0)):
                    trucktypesdata[trucktype4] = value4 
                if ((trucktype5 != "None") & (int(value5) > 0)):
                    trucktypesdata[trucktype5] = value5 
                if ((trucktype6 != "None") & (int(value6) > 0)):
                    trucktypesdata[trucktype6] = value6 
                
                print "vehicletypes",type(trucktypesdata)
                vehicletypes = json.dumps(trucktypesdata)
                
                print "*** Truck Types is ", vehicletypes

                routesdata = {}
                route = []

                fromcity1 = str(request.form['fromcity1']).strip().title()
                tocity1 = str(request.form['tocity1']).strip().title()
                if ((fromcity1 != "None") & (tocity1 != "None")):
                        routesdata[fromcity1] = tocity1
                        route.append(routesdata)
                        routesdata={}

                fromcity2 = str(request.form['fromcity2']).strip().title()
                tocity2 = str(request.form['tocity2']).strip().title()
                if ((fromcity2 != "None") & (tocity2 != "None")):
                        routesdata[fromcity2] = tocity2
                        route.append(routesdata)
                        routesdata={}

                fromcity3 = str(request.form['fromcity3']).strip().title()
                tocity3 = str(request.form['tocity3']).strip().title()
                if ((fromcity3 != "None") & (tocity3 != "None")):
                        routesdata[fromcity3] = tocity3
                        route.append(routesdata)
                        routesdata={}

                fromcity4 = str(request.form['fromcity4']).strip().title()
                tocity4 = str(request.form['tocity4']).strip().title()
                if ((fromcity4 != "None") & (tocity4 != "None")):
                        routesdata[fromcity4] = tocity4
                        route.append(routesdata)
                        routesdata ={}

                fromcity5 = str(request.form['fromcity5']).strip().title()
                tocity5 = str(request.form['tocity5']).strip().title()
                if ((fromcity5 != "None") & (tocity5 != "None")):
                        routesdata[fromcity5] = tocity5
                        route.append(routesdata)
                        routesdata = {}

                fromcity6 = str(request.form['fromcity6']).strip().title()
                tocity6 = str(request.form['tocity6']).strip().title()
                if ((fromcity6 != "None") & (tocity6 != "None")):
                        routesdata[fromcity6] = tocity6
                        route.append(routesdata)
                        routesdata ={}

                route1 = []
                for i in route:
                    if i not in route1:
                        route1.append(i)

                route = json.dumps(route1)

                print "*** Routes is ", route  

                ############################################################################################################################################################
                # 
                # Updating Customer Association for a Trucker
                # ---------------------------------------------
                #
                # Step 1 - Update tluser
                #       a. This will update all required enteries for the Trucker in tluser table
                #      
                # Step 2 - Update Trucker <> Customer Association (applicable only when Admin logs in)
                #       There are 2 possibilities
                #               a. If the admin has changed Customer from Some Customer -> None
                #                  ---   Update the tlroles set parentid = Admin_id (Truckerid > Trucker > AdminId)
                #               b. If the admin has changed Customer from None -> New Customer or old Customer -> New Customer
                #                  ---   Update the tlroles set parentid = New Customer id (Truckerid > Trucker > CustomerId)
                #
                ############################################################################################################################################################
                result = app._engine.execute("update tluser set `email_id` = '{0}', `contactno` = '{1}', `address1` = '{2}', `city` = '{3}', `state` = '{4}',`notes` = '{5}',`notes` = '{5}',`pan` = '{6}',`gst` = '{7}',`aadhar` = '{8}',`website` = '{9}',`owner_name` = '{10}',`established_year` = '{11}',`vehicletypes` = '{12}',`routes` = '{13}', `address2` = '{14}',`address3` = '{15}',`pin` = '{16}' where login_id = '{17}'".format(email, phone, address1, city, state, notes, pan, gst, aadhar,website, owner_name, established_year,vehicletypes,route,address2, address3, pincode, userid))

                logged_user_role = str(session['logged_user_role']).strip()
                logged_user = session['logged_user']
                
                if result:
                    if logged_user_role == "Admin":
                        trk_customers = []
                        trk_customers = eval(str(request.form['trk_customers']))

                        cust = []
                        for i in trk_customers:
                            cust.append({"login_id" : str(i["login_id"])})

                        while len(cust) < 5:
                            cust.append({"login_id" : "None"})
                        
                        trk_cust_list = []
                        trk_cust_list.append(cust[0]["login_id"])
                        trk_cust_list.append(cust[1]["login_id"])
                        trk_cust_list.append(cust[2]["login_id"])
                        trk_cust_list.append(cust[3]["login_id"])
                        trk_cust_list.append(cust[4]["login_id"])
                        
                        customeridsList = []
                        customeridsList.append(str(request.form['trk_customer1']).strip())
                        customeridsList.append(str(request.form['trk_customer2']).strip())
                        customeridsList.append(str(request.form['trk_customer3']).strip())
                        customeridsList.append(str(request.form['trk_customer4']).strip())
                        customeridsList.append(str(request.form['trk_customer5']).strip())

                        insert_list = set(customeridsList) - set(trk_cust_list)
                        print "************Insert Customer ID list",insert_list

                        disable_list = set(trk_cust_list) - set(customeridsList)
                        print "************Disable Customer ID list",disable_list
                        ###########################################################################################################################################################
                        # Step 1) Disable list contains those Customer id that are removed by user while selecting New Customer list
                        # Step 2) Insert list contains those Customer id that are Newly Selected by user(Means It will not contains Customer ID which is already been added)
                        ###########################################################################################################################################################
                        for custid in disable_list:
                            if custid!="None":
                                result = app._engine.execute("update tlroles set active = 'N' where userid = '{0}' and parentid = '{1}'".format(userid,custid))
                        
                        for custid in insert_list:
                            if custid!= "None":
                                result = app._engine.execute("insert into tlroles (`userid`, `role`, `parentid`) VALUES ('{0}','{1}','{2}')".format(userid,'Trucker',custid))
                    print "Stop Monitoring updatetrucker()",(int(round(time.time() * 1000))-starttime)
                    return render_template('manageresources.html',success=successupdatetrucker)
                    
            except Exception as e:
                print "In Update Trucker",str(e)
                return render_template('manageresources.html',error=errorupdatetrucker)
            
        else:
            return render_template('manageresources.html',error="Failed to update info, please contact administrator...")


# Ajax function to support upload image call from UI
@app.route('/users/api/v1/uploadimage',methods=['GET','POST'])
def uploadimage():
    print "In uploadimage()"
    starttime = int(round(time.time() * 1000))
    print "Start Monitoring uploadimage()",starttime
    try:
        file = request.files['file']
        print "File",file
        print "Name",file.filename
        extension = os.path.splitext(file.filename)[1]
        # # request.files['file'].save('/tmp/file')
        # # file_length = os.stat('/tmp/file').st_size
        # #statinfo = os.stat(file)
        # print "File Size being uploaded to Amazon is ", file_length
        if extension != "":
            upload_file_to_s3(file, file.filename ,S3_BUCKET)
            print " **** Driver Image new File Name is ", file.filename
            print "Stop Monitoring uploadimage()",(int(round(time.time() * 1000))-starttime)
            return file.filename
        else:
            return "None"    
    except Exception as e:
            print str(e)
    
    return "True";

def getlocationforuserid(userid):
    result_location=app._engine.execute("select lat ,lng, state from tluser where login_id ='{0}'".format(userid))
    location = result_location.fetchone()
    return location

#########################################
#  SMS API
#########################################
def sendsms(login_id,text,booking_id=None):
    try:
        print "**********Loginid,text",login_id,text
        cust = 'N'
        admin_op = 'N'
        total = 0
        users = app._engine.execute("select smsno, smsstatus, contactno from tluser where login_id = '{0}'".format(login_id))
        rs = users.fetchone()
        if rs != None:
            if rs[1] == "Y":
                op_status = (400,)
                contact =[]
                contact = eval(rs[0])
                contactno = rs[2]
                status = p.send_message({'src': SMS_NUMBER ,'dst' : '+91'+contactno, 'text' : text, 'method' : 'POST'})
                print "Status of Sent SMS",status
                if status[0] == 202:
                    cust = 'Y'
                    total +=1
                for i in contact:
                    #print "Text",text
                    op_status = p.send_message({'src': SMS_NUMBER ,'dst' : '+91'+i, 'text' : text, 'method' : 'POST'})
                    print "Status of Sent SMS",op_status
                if op_status[0] == 202:
                    admin_op = 'Y'
                    total +=1
        return dict({'cust':cust,'admin_op':admin_op,'total':total})
    except Exception as e:
        print str(e)

#########################################
#  EMAIL API
#########################################
def sendemail(login_id,subject,text):
    try:
        print "**********Loginid,text",login_id,text
        users = app._engine.execute("select emailstatus, emaillist, email_id from tluser where login_id = '{0}'".format(login_id))
        rs = users.fetchone()
        if rs != None:
            if rs[0] == "Y":

                from_email = Email(WELCOME_EMAIL_FROM)
                subject = subject
                content = Content("text/html", text)
                to_email = Email(rs[2])
                mail = Mail(from_email, subject, to_email, content)

                email =[]
                email = eval(rs[1])
                for cc in email:
                    mail.personalizations[0].add_cc(Email(cc))
                    # Send Email
                response = sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                    
    except Exception as e:
        print str(e)

#########################################
#  Welcome SMS API
#########################################
def sendwelcomesms(contactno,text):
    try:
        smsvalue = []
        smsvalue = retrievemetadatabytype('WelcomeSMS')
        if smsvalue != []:
            data = smsvalue[0]['element']
            print "Welcome SMS flag is:",smsvalue[0]
            data = smsvalue[0]['element']
            if data == 'Y':
                print "Status of Sent SMS",p.send_message({'src': SMS_NUMBER ,'dst' : '+91'+contactno, 'text' : text, 'method' : 'POST'})
                SMSList = retrievemetadatabytype('WelcomeSMSList')
                if SMSList != []:
                    welcomesmslist = eval(SMSList[0]['element']);
                    for contact in welcomesmslist:
                        print "Status of Sent SMS",p.send_message({'src': SMS_NUMBER ,'dst' : '+91'+contact, 'text' : text, 'method' : 'POST'})
            else:
                print "Welcome SMS disabled for New Customers... "
        else:
            print "Welcome SMS type is not available in DB"
    except Exception as e:
        print str(e)

#####################################################################################################
#  API to send Welcome Email to Customer/Trucker on successful registration in Trucklo Platform
#####################################################################################################
def sendwelcomeemail(email_id,name,type):
    
    try:

        print "Primary Email ID is ", email_id

        # If Email ID exists then send Welcome Email
        if str(email_id).strip() != "":

            # Retrieve WelcomeEMAIL flag value from tlmetadata
            emailvalue = []
            emailvalue = retrievemetadatabytype('WelcomeEMAIL')

            if emailvalue != []:
                data = emailvalue[0]['element']

                # If WelcomeEMAIL flag is 'Y' in tlmetadata, then send Welcome Email
                if data == 'Y':
                    
                    from_email = Email(WELCOME_EMAIL_FROM)
                    to_email = Email(email_id)
                    subject = WELCOME_EMAIL_SUBJECT
                    
                    if type == 'Customer':
                        content = Content("text/html", WELCOME_EMAIL_BODY_CUS.format(name))
                    elif type == 'Trucker':
                        content = Content("text/html", WELCOME_EMAIL_BODY_TRK.format(name))
                        
                    mail = Mail(from_email, subject, to_email, content)

                    # Retrieve cc list for Emails i.e. WelcomeEMAIL_LIST value in tlmetadata
                    list_of_cc = retrievemetadatabytype('WelcomeEMAILLIST')
                    if list_of_cc != []:
                        list_of_cc = [x.strip().lower() for x in eval(list_of_cc[0]['element'])]

                        for cc in list_of_cc:
                            mail.personalizations[0].add_cc(Email(cc))

                    # Send Email
                    response = sg.client.mail.send.post(request_body=mail.get())
                    print(response.status_code)
            
                else:
                    print "Welcome Emails disabled for New Customers... "  
            else:
                print "Welcome Email type is not available in DB"
        else:
            print "Welcome Email cannot be sent as there is no Email ID available..."  

    except Exception as e:
        print str(e)

#############################################################################################################
# Upload the Images on Amazon S3 with
# file = filename uploaded by User in UI
# picname = New filename ,created by developer contains random generation of numbers with image extension
# bucket_name = Name of the bucket in Amazon S3 
##############################################################################################################
def upload_file_to_s3(file, picname, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            picname,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Error while Saving Image on Amazon S3 : ", e)

# Get user name from id
@app.route('/getusername')
def getusername(id):
    result=app._engine.execute("select name from tluser where login_id = '{0}'".format(id))
    return result.first()[0]

# Get the pic name based on id
@app.route('/getpicname')
def getpicname(id):
    result=app._engine.execute("select pic from tluser where login_id = '{0}'".format(id))
    return result.first()[0]

@app.route('/getparentid')
def getparentid(id):
    result_p=app._engine.execute("select parentid from tlroles where userid = '{0}'".format(id))
    return result_p.first()[0]

# Get related userid for parentid 
def getrelateduserid(parentid,role,status):
    result_e=app._engine.execute("select login_id,name from tluser where login_id in (select userid from tlroles where role = '{0}' and  parentid = '{1}' and active = '{2}')".format(role,parentid,status))
    userids = []
    for row in result_e:
        userids.append(dict(row.items()))
    print "****List of userid with associated parent ", parentid , " is ",json.dumps(userids)
    return  userids

# Get related parentid for userid
def getrelatedparentid(userid,role,status):
   result_e=app._engine.execute("select login_id, name from tluser where login_id in (select parentid from tlroles where role = '{0}' and  userid = '{1}' and active = '{2}')".format(role,userid,status))
   parentids = []
   for row in result_e:
       parentids.append(dict(row.items()))
   print "****List of parentids with associated user ", userid , " is ", json.dumps(parentids)
   return parentids

#Get all Details of user
def getuserdetailsbyid(userid):
    result_u=app._engine.execute("select name,email_id,contactno,license,address1,address2,address3,gst,pan,pin,smsno,smsstatus,emailstatus,emaillist from tluser where login_id = '{0}'".format(userid))
    users = []
    for row in result_u:
        users.append(dict(row.items()))
    print " **** List of Users is ", json.dumps(users)
    return users

# Retrieve metadata element by id
def retrievemetadatabyid(mid):
    result_m = app._engine.execute("select element from tlmetadata where id='{0}'".format(mid))
    metadata = []
    for row  in result_m:
        metadata.append(dict(row.items()))
    print " *** List of Metadata ",json.dumps(metadata)
    return metadata

# Retrieve all metadata by type
def retrievemetadatabytype(metadatatype):
    result_m = app._engine.execute("select id,element from tlmetadata where type='{0}'".format(metadatatype))
    metadatalist = []
    for row  in result_m:
        metadatalist.append(dict(row.items()))
    print " *** List of Metadata ",json.dumps(metadatalist)
    return metadatalist

# Retrieve All truck types
def retrievealltrucktypes():
    result_types = app._engine.execute("select id,element from tlmetadata where type='TruckType'")
    trucktypes = []
    for row  in result_types:
        trucktypes.append(dict(row.items()))
    print " *** List of Trucker Types ",json.dumps(trucktypes)
    return trucktypes

# Retrieve hypertrack user id from tluser table for a given user
def gethypertrackuserid(userid):
    result_id = app._engine.execute("select hypertrackuserid from tluser where login_id='{0}'".format(userid))
    rs = result_id.fetchone()
    if rs == None:
        return "None"
    else: return rs[0]

# Retrieve all getmetdatalist
def getmetdatalist(metadatatype,arr):
    metadataarr = []
    for i in arr:
        result_metadata = app._engine.execute("select id,element from tlmetadata where type='{0}' and id='{1}'".format(metadatatype,i))        
        for row in result_metadata:
            metadataarr.append(dict(row.items()))
        print " *** List of Metadata ",json.dumps(metadataarr)
    return json.dumps(metadataarr) 

# API to retrieve vehicles for a specific trucker
@app.route('/users/api/v1/checkusername',methods=['GET'])
def checkusername():
    username = request.args.get('username').strip()
    result_id = app._engine.execute("select name from tluser where name = '{0}'".format(username))
    rs = result_id.fetchone()
    if rs == None:
        return "None"
    else: return rs[0]

#API to check if metadata element already exists in tlmetadata table
@app.route('/metadata/api/v1/checkmetadata',methods=['GET'])
def checkmetadata(element,metadatatype):
    count = 0
    element = element.strip().upper().replace(' ','')
    metadatatype = metadatatype.strip().replace(' ','')
    result_v = app._engine.execute("select * from tlmetadata where REPLACE(element,' ','') = '{0}' and REPLACE(type,' ','') = '{1}'".format(element,metadatatype))
    for row in result_v:
        count = 1
    return count


# TEST API for Android APK Interviews - Get latitude and longitude for city provided
@app.route('/latlong/api/v1/getlatlong/<cityname>',methods=['GET'])
def latandlongforcity(cityname):
    coordinates = []
    coordinatesdict = {}
    if (cityname == 'Pune'):
        coordinatesdict['latitude'] = '18.5204'
        coordinatesdict['longitude'] = '73.8567'
        coordinates.append(dict(coordinatesdict))
    elif (cityname == 'Mumbai'):
        coordinatesdict['latitude'] = '19.0760'
        coordinatesdict['longitude'] = '72.8777'
        coordinates.append(dict(coordinatesdict))
    elif (cityname == 'Varanasi'):
        coordinatesdict['latitude'] = '25.3176'
        coordinatesdict['longitude'] = '82.9739'
        coordinates.append(dict(coordinatesdict))
    else:
        coordinatesdict['latitude'] = '0'
        coordinatesdict['longitude'] = '0'
        coordinates.append(dict(coordinatesdict))

    json_coordinates = jsonify(coordinates)
    return json_coordinates

# TEST API for Android APK Interviews - Add Test Person
# - For e.g url is http://trucklo-test.herokuapp.com/addtestperson/Samuel/9807651231/Maharashtra/Pune/test@trucklo.com/test/new admin
@app.route('/addtestperson/<name>/<phone>/<state>/<city>/<email>/<password>/<notes>',methods=['POST'])
def addtestperson(name, phone, state, city, email, password, notes):

    useradd = []
    useraddstatus = {}

    print "Start Monitoring addtestperson()"

    if not session.get('logged_in'):
        try:

            print "Inside try of addtestperson"
            print name, phone, state, city, email, password, notes
            login_id = str(name[0:3]+''.join(choice(digits) for i in range(2))).strip().upper()
            result = app._engine.execute("insert into tluser (`login_id`, `name`, `country`,`customer_type`,`password`) VALUES ('{0}', '{1}', 'India','Individual', 'test')".format(login_id,name))
            print "Ended addtestperson"
            useraddstatus['errorcode'] = '000'
            useraddstatus['message'] = 'User added successfully'
            useradd.append(dict(useraddstatus)) 

        except Exception as e:

            print "Exception in addtestperson()",str(e)
            useraddstatus['errorcode'] = '801'
            useraddstatus['message'] = 'User add failed'
            useradd.append(dict(useraddstatus)) 

        return jsonify(useradd)

# TEST API for Android APK Interviews - Login User
# - For e.g url is http://trucklo-test.herokuapp.com/newlogin/hr@innoctive.com/test
@app.route('/newlogin/<email>/<password>',methods=['POST'])
def newlogin(email, password):
    loginstatus = []
    login = {}
    try:
        print "Start Monitoring newlogin()"
        # Retrieve the username and password saved in DB against the login id
        result = app._engine.execute("select name, password, login_id from tluser where email_id = '{0}'".format(email))
        rs = result.fetchone()
        if rs == None:
            print 'Invalid Email ID'
            login['errocode'] = '801'
            login['message'] = 'Invalid Email or Password'
            loginstatus.append(login)
        else: 
            dbpassword = str(rs[1])
            passwordhash = sha256_crypt.encrypt(password)
            if (sha256_crypt.verify(password, dbpassword)):
                login['login_ID'] = rs[2]
                login['name'] = rs[0]
                loginstatus.append(login)
            else:
                print 'Invalid Password'
                login['errocode'] = '802'
                login['message'] = 'Invalid Email or Password'
                loginstatus.append(login)
        return jsonify(loginstatus)
    except Exception as e:
            print str(e)
            loginstatus.append({'Error':"Invalid Email or Password"})
    return jsonify(loginstatus)

# TEST API for Android APK Interviews - Get Weather Info
# - For e.g url is http://trucklo-test.herokuapp.com/getweatherinfo/Pune
@app.route('/getweatherinfo/api/v1/<cityname>',methods=['GET'])
def getweatherinfo(cityname):
    weather = []
    weatherdict = {}
    if (cityname == 'Pune'):
        weatherdict['min'] = '18.1'
        weatherdict['max'] = '19.2'
        weather.append(dict(weatherdict))
    elif (cityname == 'Mumbai'):
        weatherdict['min'] = '26.4'
        weatherdict['max'] = '29.5'
        weather.append(dict(weatherdict))
    elif (cityname == 'Varanasi'):
        weatherdict['min'] = '16.7'
        weatherdict['max'] = '18.8'
        weather.append(dict(weatherdict))
    else:
        weatherdict['min'] = '0'
        weatherdict['max'] = '0'
        weather.append(dict(weatherdict))
    return jsonify(weather)

@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route("/uploads",methods=['POST'])
def uploads():
    return "Upload Success"

def google_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(GOOGLE_SHORT_URL_API_KEY)
    postdata = {'longUrl':url}
    headers = {'Content-Type':'application/json'}
    req = urllib2.Request(
        post_url,
        json.dumps(postdata),
        headers
    )
    ret = urllib2.urlopen(req).read()
    return json.loads(ret)['id']

