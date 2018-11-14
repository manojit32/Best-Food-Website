from flask import Flask,render_template,request,session,redirect, url_for ,abort ,Response,flash,jsonify,Markup
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy,models_committed
from flask_login import LoginManager
import os,base64,random
from werkzeug.utils import secure_filename
import googlemaps,re
import sys
import operator


# gm=googlemaps.Client(key='AIzaSyBSh3CSZvzLS_YzZk5mb96CrNOSer0Tusg')

# geocode_result=gm.reverse_geocode((17.385044,78.486671))



app = Flask(__name__)
gpath = os.path.join(app.root_path,"static","data","bestFood.db")
print("gpath"+gpath)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/data/bestFood.db'
app.config["DATABASE"] = gpath
app.config["MAX_ITEMS_PER_PAGE"] = 21
IMAGES_FOLDER = os.path.join(app.root_path,"static","data","restaurant_images")

ITEMS_FOLDER = os.path.join(app.root_path,"static","data","item_images")

PROFILE_PICTURES = os.path.join(app.root_path,"static","data","user_profile_pics")

print(IMAGES_FOLDER)

# YOUTUBE_SPAMS = os.path.join(app.root_path,"static","data","datasets","YoutubeSpamMergedData.csv")

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png','JPG'])

app.config['IMAGES_FOLDER'] = IMAGES_FOLDER

app.config['PROFILE_PICTURES'] = PROFILE_PICTURES

app.config['ITEM_PICTURES'] = ITEMS_FOLDER

# app.config['YouTubeSpam.csv'] = YOUTUBE_SPAMS


db = SQLAlchemy(app)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = "secretkey"
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
    u_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    u_email = db.Column(db.String(80))
    u_password = db.Column(db.String(100),nullable=False)
    u_fname = db.Column(db.String(80))
    u_lname = db.Column(db.String(80))
    u_mobile = db.Column(db.String(80))
    u_address= db.Column(db.String(80))
    u_image = db.Column(db.String(80))
    u_orders = db.relationship('Order', cascade="all,delete",backref='user',lazy=True)
    def __repr__(self):
        return self.u_email+"--"+self.u_password
    def check_password(self, password):
        return check_password_hash(self.u_password, password)
    def get_id(self):
        return self.u_email

class Vendor(db.Model):
    v_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    v_email = db.Column(db.String(80))
    v_password = db.Column(db.String(100),nullable=False)
    v_vendorrestaurant = db.relationship('VendorRestaurant', cascade="all,delete",backref='vendor',lazy=True)
    v_fname = db.Column(db.String(80))
    v_lname = db.Column(db.String(80))
    v_mobile = db.Column(db.String(80))
    v_address= db.Column(db.String(80))
    def __repr__(self):
        return self.v_email+"--"+self.v_password
    def check_password(self, password):
        return check_password_hash(self.v_password, password)
    def get_id(self):
        return self.v_email

class Restaurant(db.Model):
    r_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    r_name = db.Column(db.String(80))
    r_phone = db.Column(db.String(12))
    r_rating = db.Column(db.Float)
    r_lat = db.Column(db.Float)
    r_lon = db.Column(db.Float)
    r_address = db.Column(db.String(80))
    r_email = db.Column(db.String(80))
    r_website = db.Column(db.String(80))
    r_location = db.Column(db.String(80))
    r_city = db.Column(db.String(80))
    r_zip = db.Column(db.String(80))
    r_images = db.Column(db.String(80))
    r_vendorrestaurant = db.relationship('VendorRestaurant', cascade="all,delete",backref='restaurant',lazy=True)
    r_menu = db.relationship('Menu', cascade="all,delete",backref='restaurant',lazy=True)
    r_orders = db.relationship('Order', cascade="all,delete",backref='restaurant',lazy=True)
    r_votesCount = db.Column(db.Integer)
    # def __commit_insert__(self):
    #     if "email" in session:
    #         print(session["email"])
    #         print(getVID(session["email"]))
    #         db.session.add(VendorRestaurant(v_id = getVID(session["email"]),r_id=self.r_id))
    #         # db.session.commit()

class VendorRestaurant(db.Model):
    v_id = db.Column(db.Integer,db.ForeignKey('vendor.v_id'),primary_key=True)
    r_id = db.Column(db.Integer,db.ForeignKey('restaurant.r_id'),primary_key=True)

class Menu(db.Model):
    i_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    i_name = db.Column(db.String(80))
    i_cost = db.Column(db.Float)
    i_type = db.Column(db.String)
    i_maincategory = db.Column(db.String(80))
    i_subcategory1 = db.Column(db.String(80))
    i_subcategory2 = db.Column(db.String(80))
    i_image = db.Column(db.String(80))
    r_id = db.Column(db.Integer,db.ForeignKey('restaurant.r_id'))
    i_orders = db.relationship('Order', cascade="all,delete",backref='menu',lazy=True)
    def __repr__(self):
        return self.u_email+"--"+self.u_password
    def __iter__(self):
        return iter((self.i_id,self.i_name,self.i_cost,self.i_type,self.i_maincategory,self.i_subcategory1,self.i_subcategory2,self.i_image))
        #return ("i_id","i_name","i_cost","i_type","i_maincategory1","i_subcategory1","i_subcategory2")
    def keys(self):
        return ("i_id","i_name","i_cost","i_type","i_maincategory1","i_subcategory1","i_subcategory2","i_image")

class Order(db.Model):
    # o_row_no = db.Column(db.Integer,autoincrement=True,primary_key=True)
    # o_id = db.Column(db.String,default=(str(datetime.now().timestamp()).replace('.','')+str(random.choice(range(10000)))),primary_key=True)
    o_u_id = db.Column(db.Integer,db.ForeignKey('user.u_id'),primary_key=True)
    o_r_id = db.Column(db.Integer,db.ForeignKey('restaurant.r_id'),primary_key=True)
    o_i_id = db.Column(db.Integer,db.ForeignKey('menu.i_id'),primary_key=True)
    o_i_quantity = db.Column(db.Integer)
    o_price = db.Column(db.Float)
    o_name = db.Column(db.String(30))
    o_phone = db.Column(db.String(15))
    o_address = db.Column(db.String(80))
    o_order_date = db.Column(db.DateTime,default=datetime.now(),primary_key=True)

class Cuisines(db.Model):
    c_id = db.Column(db.Integer,primary_key=True)
    c_cuisine = db.Column(db.String(20),unique=True)

class RestaurantCuisines(db.Model):
    rc_id = db.Column(db.Integer,primary_key=True)
    rc_cuisines1 = db.Column(db.String(40))
    rc_cuisines2 = db.Column(db.String(40))
    rc_cuisines3 = db.Column(db.String(40))
    rc_cuisines4 = db.Column(db.String(40))
    rc_cuisines5 = db.Column(db.String(40))
    rc_cuisines6 = db.Column(db.String(40))
    rc_r_id = db.Column(db.Integer,db.ForeignKey('restaurant.r_id'))

db.create_all()

@models_committed.connect_via(app)
def on_models_committed(sender, changes):
    for obj, change in changes:
        if change == 'insert' and hasattr(obj, '__commit_insert__'):
            obj.__commit_insert__()
        elif change == 'update' and hasattr(obj, '__commit_update__'):
            obj.__commit_update__()
        elif change == 'delete' and hasattr(obj, '__commit_delete__'):
            obj.__commit_delete__()


uLinksDict ={0:{"href":"/viewprofile","atext":"Profile"} \
                        ,1:{"href":"/showrestaurants","atext":"View Restaurants"}\
                        ,2:{"href":"/vieworders","atext":"View Orders"}\
                        }
vLinksDict ={0:{"href":"/viewprofile","atext":"Profile"} \
                        ,1:{"href":"/addrestaurant","atext":"Add Restaurant"} \
                        ,2:{"href":"/viewrestaurant","atext":"View Restaurant"}\
                        ,3:{"href":"/addmenu","atext":"Add Menu"} \
                        ,4:{"href":"/viewmenu","atext":"View Menu"}\
                        ,5:{"href":"/vieworders","atext":"View Order"}
                        }

"""
def AddEntriesIntoDB():
    c=0
    for line in sys.stdin:
        print(line)
        line=line.strip('\'\'')
        cuisine = Cuisines(c_id=c,c_cuisine=line.split('\'')[0])
        db.session.add(cuisine)
        db.session.commit()
        c+=1
    return
    for line in sys.stdin:
        # print(line.split(","))
        print(line)
        if c>0:
            restaurant,cuisine1,cuisine2,cuisine3,cuisine4,cuisine5,cuisine6 = line.split(",")
            if cuisine1 == '':
                cuisine1 = None
            if cuisine2 == '':
                cuisine2 = None
            if cuisine3 == '':
                cuisine3 = None
            if cuisine4 == '':
                cuisine4 = None
            if cuisine5 == '':

            rc_id = Restaurant.query.filter_by(r_name=restaurant).first().r_id
            print(rc_id)
            hotel = RestaurantCuisines(rc_id=c,rc_cuisines1=cuisine1,rc_cuisines2=cuisine2,rc_cuisines3=cuisine3,rc_cuisines4=cuisine4,rc_cuisines5=cuisine5,rc_cuisines6=cuisine6,rc_r_id=rc_id)
            db.session.add(hotel)
            db.session.commit()
        c+=1
    return
"""
def getRecommendations(Recommenders):
    recommend={}
    for i in range(len(Recommenders)-1):
        # print(match)
        # i = match[0]
        res=Restaurant.query.filter_by(r_id=Recommenders[i][0]).first()
        # print(res)
        recommend[Recommenders[i][0]]=[res.r_name,res.r_images]
    return recommend

def ContentBasedRecommendation(dataset,i_n_p_u_t,restaurant):
    neighbours={}
    # print(dataset)
    for data in dataset:
        x = dataset[data][data]
        j=0
        MatchScore=0
        # print()
        for i in x:
            if i==i_n_p_u_t[restaurant][j] and i==1:
                MatchScore+=1
            j+=1
        neighbours[data] = MatchScore
    return neighbours

def Make_Dataset(restaurant,cuisine):
    def buildRestaurant(Cuisines,Cuisines_In_Restaurant):
        res=[]
        check={}
        for cuisine in Cuisines:
            for feature in Cuisines_In_Restaurant:
                if cuisine == feature:
                    if cuisine not in check:
                        check[cuisine] = 1
                        res.append(1)
            if cuisine not in check:
                check[cuisine] = 0
                res.append(0)
        return res
    d={}
    c_u_i_s_i_n_e_s=[restaurant.rc_cuisines1,restaurant.rc_cuisines2,restaurant.rc_cuisines3,restaurant.rc_cuisines4,restaurant.rc_cuisines5,restaurant.rc_cuisines6]
    cuisines=[]
    for row in cuisine:
        cuisines.append(row.c_cuisine)
    d[restaurant.rc_r_id]=buildRestaurant(cuisines,c_u_i_s_i_n_e_s)
    return d

def getTopRated():
   res = Restaurant.query.order_by(Restaurant.r_votesCount.desc()).all()
   Tp = {}
   for row in res:
       Tp[row.r_id] = [row.r_name,row.r_images]
       # print(len(Tp.keys()))
       if len(Tp.keys())>10:
           break
   # print("TopRated",Tp)
   return Tp

def getPopularRestaurants():
   res = Restaurant.query.order_by(Restaurant.r_rating.desc()).all()
   Pr={}
   for row in res:
       Pr[row.r_id] = [row.r_name,row.r_images]
       if len(Pr.keys())>10:
           break
   return Pr

def getNewRestaurants():
    res = Restaurant.query.order_by(Restaurant.r_votesCount).all()
    Nr = {}
    for row in res:
        Nr[row.r_id] = [row.r_name,row.r_images]
        if len(Nr.keys())>11:
            break
    print(Nr)
    return Nr

@app.route('/')
def homepage():
    if isVendor():
        return render_template("vhomepage.html",removeCartSettings=True,nosidebar=True,header=True,username=session["email"], itemsDict=vLinksDict)
    elif isUser():
        uid = session['id']
        res = Order.query.filter_by(o_u_id=uid).order_by(Order.o_order_date.desc()).first()
        if res is None:
            return render_template("homepage.html",header=True,username=session["email"],itemsDict=uLinksDict,scripts=["foodcart.js","flickity.pkgd.min.js"],stylesheets=["flickity.min.css"],recommenders=None,TopRated=getTopRated(),PopularRestaurants=getPopularRestaurants(),NewRestaurants=getNewRestaurants())
        else:
            cuisines = Cuisines.query.all()
            restaurant = RestaurantCuisines.query.filter_by(rc_r_id=res.o_r_id).first()
            if restaurant is None:
                return render_template("homepage.html",header=True,username=session["email"],itemsDict=uLinksDict,scripts=["foodcart.js","flickity.pkgd.min.js"],stylesheets=["flickity.min.css"],recommenders=None,TopRated=getTopRated(),PopularRestaurants=getPopularRestaurants(),NewRestaurants=getNewRestaurants())
            predict_for=Make_Dataset(restaurant,cuisines)
            # print(predict_for)
            content={}
            for rest in RestaurantCuisines.query.all():
                content[rest.rc_r_id] = Make_Dataset(rest,cuisines)
            a = ContentBasedRecommendation(content,predict_for,res.o_r_id)
            sorted_x = sorted(a.items(),key=operator.itemgetter(1))
            # print(sorted_x)
            temp=(res.o_r_id,a.get(res.o_r_id))
            sorted_x=sorted_x[len(sorted_x)-9:len(sorted_x)]
            sorted_x.append(temp)
            return render_template("homepage.html",header=True,username=session["email"],itemsDict=uLinksDict,scripts=["foodcart.js","flickity.pkgd.min.js"],stylesheets=["flickity.min.css"],recommenders=getRecommendations(sorted_x),TopRated=getTopRated(),PopularRestaurants=getPopularRestaurants(),NewRestaurants=getNewRestaurants())
        return render_template("homepage.html",header=True,username=session["email"],itemsDict=uLinksDict,scripts=["foodcart.js","flickity.pkgd.min.js"],stylesheets=["flickity.min.css"],TopRated=getTopRated(),PopularRestaurants=getPopularRestaurants(),NewRestaurants=getNewRestaurants())
    return render_template("homepage.html",header=True,TopRated=getTopRated(),PopularRestaurants=getPopularRestaurants(),scripts=["foodcart.js","flickity.pkgd.min.js"],stylesheets=["flickity.min.css"],NewRestaurants=getNewRestaurants())

@app.route("/search",methods=["GET","POST"])
def search():
    if (request.method=="GET"):
        query_parameters = request.args
        # print ("mynameis",query_parameters)
        item_name = query_parameters.get('q')
        # print(item_name,"------------------------------------")

        location_name= query_parameters.get('location')
        # print(location_name,"------------------")
        location_main=""
        if(location_name):
            list1=["Gachibowli","Kukatpally","HITECCity","Ameerpet"]
            list2=location_name.split(",")
            # print(list2)
            list3=[]
            for i in list2:
                i=i.replace(" ","")
                list3.append(i)
            # print(list3)
            location_main=location_name
            for location in list3:
                temp=location.lower()
                for mainlocation in list1:
                    if(temp==mainlocation.lower()):
                        location_main=location


        sort = query_parameters.get('sort')
        minprice = query_parameters.get('minprice')
        maxprice = query_parameters.get('maxprice')
        query = "{}".format("db.session.query(Menu,Restaurant).join(Restaurant).filter(Menu.r_id==Restaurant.r_id)")
        # print("sort",sort)

        # print("Gurunath",bool(sort) != bool(sort))
        if (minprice and maxprice):
            query += ".filter(Menu.i_cost>='{}',Menu.i_cost<='{}')".format( Markup.escape(minprice),Markup.escape(maxprice))
        elif (minprice):
            query += ".filter(Menu.i_cost>='{}')".format(Markup.escape(minprice))
        elif (maxprice):
            query += ".filter(Menu.i_cost<='{}')".format(Markup.escape(maxprice))
        if (item_name):
            item_name=re.sub(re.compile("[^A-Z a-z0-9]"),'',item_name)
            query += ".filter(Menu.i_name.like('%{}%'))".format(Markup.escape(item_name))
        if (location_main):
            query += ".filter(Restaurant.r_location.like('{}'))".format(Markup.escape(location_main))
        # if (session.get("location",None)):
        #     query += ".filter(Restaurant.r_location.like('{}'))".format(session["location"])
        if (sort):
            if (sort=="1"):
                query += ".order_by((Menu.i_cost))"
            elif (sort=="2"):
                query += ".order_by(Menu.i_cost.desc())"

        # print(query)
        page = request.args.get('page', 1, type=int)
        q_paginated=eval(query).paginate(
        page, app.config['MAX_ITEMS_PER_PAGE']*2, False)
        q=q_paginated.items
        d={}
        r={}
        for i in q:
            i_dict={}
            i_dict["i_id"]=i[0].i_id
            i_dict["i_name"]=i[0].i_name
            i_dict["i_cost"]=i[0].i_cost
            i_dict["i_image"]=i[0].i_image
            if i[1].r_id not in d:
                d[i[1].r_id]=[]
                d[i[1].r_id].append(i_dict)
                r[i[1].r_id]=i[1].r_name
            else:
                d[i[1].r_id].append(i_dict)
        next_url = url_for('search', q=item_name,location_name=location_name,sort=sort,minprice=minprice,maxprice=maxprice,page=q_paginated.next_num) \
                        if q_paginated.has_next else None
        prev_url = url_for('search', q=item_name,location_name=location_name,sort=sort,minprice=minprice,maxprice=maxprice,page=q_paginated.prev_num) \
                        if q_paginated.has_prev else None
        if ("email" in session and check(session["email"])):
            return render_template("search.html",header=True,s=sort,d=d,r=r,username=session['email'],scripts=["foodcart.js","validatesidefilter.js"],itemsDict=uLinksDict,stylesheets=["style.css"],q=item_name,location=location_main,next_url=next_url,prev_url=prev_url)
        return render_template("search.html",header=True,s=sort,d=d,r=r,scripts=["foodcart.js","validatesidefilter.js"],itemsDict=uLinksDict,stylesheets=["style.css"],q=item_name,location=location_main,next_url=next_url,prev_url=prev_url)

    return "Not Allowed"

@app.route("/autosuggest/<keyword>")
def autosuggest(keyword):
    itemsList=Menu.query.filter(Menu.i_name.like('%'+keyword+'%')).all()
    autosuggestions=[]
    count  = 0
    for i in itemsList:
        autosuggestions.append(i.i_name)
        count = count+1
        if(count==5):
            break

    return jsonify(autosuggestions)

@app.route('/<latitude>/<longitude>')
def location(latitude,longitude):
   gm=googlemaps.Client(key='AIzaSyBSh3CSZvzLS_YzZk5mb96CrNOSer0Tusg')

   geocode_result=gm.reverse_geocode((latitude,longitude))

   a=geocode_result[0]["formatted_address"]
   print(a)
   return jsonify(a)

# @app.route("/search",methods=["GET","POST"])
# def search():
#     if (request.method=="GET"):
#        item_name = request.args.get('q')
#        q=db.session.query(Menu,Restaurant).join(Restaurant).filter(Menu.r_id==Restaurant.r_id).filter(Menu.i_name.like('%'+item_name+'%')).all()
#        d={}

#        for i in q:
#            i_dict={}
#            i_dict["i_id"]=i[0].i_id
#            i_dict["i_name"]=i[0].i_name
#            i_dict["i_cost"]=i[0].i_cost
#            i_dict["i_image"]=i[0].i_image
#            if i[1].r_id not in d:
#                d[i[1].r_id]=[]
#                d[i[1].r_id].append(i_dict)
#            else:
#                d[i[1].r_id].append(i_dict)

#     return render_template("search.html",header=True,d=d,username=session['email'],scripts=["foodcart.js"])

@app.route("/vieworders",methods=['GET','POST'])
def vieworders():
    u_invoices=[]
    if ("email" in session and isUser()):
        uid= session["id"]
        z=db.session.query(Order.o_u_id,Order.o_r_id,Order.o_order_date).group_by(Order.o_u_id,Order.o_r_id,Order.o_order_date).order_by(Order.o_order_date.desc()).filter_by(o_u_id=uid).all()
        #print("no of tup",len(z))

        for i,j,k in z:
            u_each_order_lines=db.session.query(Order.o_u_id,Order.o_r_id,Order.o_order_date,Order.o_i_id,Order.o_i_quantity).filter_by(o_u_id=i,o_r_id=j,o_order_date=k).all()
            # print(u_each_order_lines)
            d={}
            u_order_keys={}
            temp=None
            for i,j,k,l,m in u_each_order_lines:

                u_order_keys[l]=m
                temp=j
            d[j]=u_order_keys
            u_invoices.append(vgenInvoice(d))
        return render_template("vieworders.html",invoicelist=u_invoices,userform=True,scripts=["foodcart.js"],nosidebar=True,username=session["email"],itemsDict=uLinksDict)
    elif ("email" in session and isVendor()):
        uid= session["id"]
        z1=db.session.query(VendorRestaurant.v_id,VendorRestaurant.r_id).filter_by(v_id=uid).all()
        for x,y in z1:
            z=db.session.query(Order.o_u_id,Order.o_r_id,Order.o_order_date).group_by(Order.o_u_id,Order.o_r_id,Order.o_order_date).order_by(Order.o_order_date.desc()).filter_by(o_r_id=y).all()
        #print("no of tup",len(z))

        for i,j,k in z:
            u_each_order_lines=db.session.query(Order.o_u_id,Order.o_r_id,Order.o_order_date,Order.o_i_id,Order.o_i_quantity).filter_by(o_u_id=i,o_r_id=j,o_order_date=k).all()
            # print(u_each_order_lines)
            d={}
            u_order_keys={}
            temp=None
            for i,j,k,l,m in u_each_order_lines:

                u_order_keys[l]=m
                temp=j
            d[j]=u_order_keys
            u_invoices.append(vgenInvoice(d))
        return render_template("vieworders.html",invoicelist=u_invoices,userform=True,scripts=["foodcart.js"],nosidebar=True,username=session["email"],itemsDict=vLinksDict)
    return render_template("vieworders.html",userform=True,error="Please Login to view your orders",scripts=["foodcart.js"],nosidebar=True)

@app.route("/signup",methods=["GET","POST"])
def signup():
    if (request.method=="POST"):
        email=request.form["u_name"]
        password=request.form["u_password"]
        c_password=request.form["u_c_password"]
        if (not check(email)):
            if (password!=c_password):
                return render_template("signup.html",p_error=True,header=True,scripts=["validatesignupform.js"])
            else:
                db.session.add(User(u_email=email,u_password=password))
                db.session.commit()
            flash("Account Created Successfully.You can now login with {} creds".format(email),'success')
            return render_template("login.html",header=True)
        else:
            flash("Wrong Credentials",'error')
            return render_template("signup.html",l_error=True,header=True,scripts=["validatesignupform.js"])
    if ("email" in session):
        return render_template("success.html",email="You are already logged in.You need to sign out to create a new account")
    else:
        return render_template("signup.html",header=True,scripts=["validatesignupform.js"])

@app.route("/login/",methods=["GET","POST"])
def login():
        if (request.method=="POST"):
            email=request.form["u_name"]
            password=request.form["u_password"]
            if (check(email)):
                if (password!=getPassword(email)):
                    flash("Invalid Password",'danger')
                    return render_template("login.html",p_error=True,header=True)
                else:
                    session["email"]= email
                    session["type"] = "user"
                    flash("Successfully logged in as {}".format(email),'success')
                    session["id"] = getUID(email)
                    return redirect(url_for('homepage'))

            else:
                return render_template("login.html",l_error=True,header=True)

        if ("email" in session):
            return redirect(url_for('homepage'))
        else:
            return render_template("login.html",header=True)

@app.route("/viewprofile",methods=["GET","POST"])
def viewprofile():

    u_details={}
    if ("email" in session and check(session["email"])):

        if (request.method=="POST"):
            u_email=session["email"]
            # print(u_email)
            u_fname=request.form["first name"]
            u_lname=request.form["last name"]
            u_mobile=request.form["mobile"]
            u_address=request.form["Address"]
            # print(u_fname)
            # print(u_mobile)
            user_this=User.query.filter_by(u_email=u_email).first()
            user_this.u_fname=u_fname
            user_this.u_lname=u_lname
            user_this.u_mobile=u_mobile
            user_this.u_address=u_address
            image=""
            r_image=""
            if user_this.u_image:
                image = user_this.u_image
            else:
                image = ""
            if 'file' in request.files:
                r_image = request.files['file']
            # print(r_image)
            # print(r_image.filename)
            if r_image and allowed_file(r_image.filename):
                filename = secure_filename(r_image.filename)
                MYDIR = os.path.dirname(__file__)
                # print ("Is saving.....", MYDIR)
                r_image.save(os.path.join(MYDIR,app.config['PROFILE_PICTURES'],filename))
                user_this.u_image = filename
                # print("Printing user_this.u_image*******************",user_this.u_image)
                # print("------------------------------------------")
                db.session.commit()
                flash("Profile Updated Successfully",'success')
                u_details={'u_fname':u_fname,'u_lname':u_lname,'u_mobile':u_mobile,'u_address':u_address}
                if(isVendor()):
                    return render_template("viewprofile.html",header=True,mail_id=u_email,u_details=u_details,username=session["email"],scripts=["foodcart.js"],itemsDict=vLinksDict,profile_pic=os.path.join("static","data","user_profile_pics",filename),removeCartSettings=True)
                return render_template("viewprofile.html",header=True,mail_id=u_email,u_details=u_details,username=session["email"],scripts=["foodcart.js"],itemsDict=uLinksDict,profile_pic=os.path.join("static","data","user_profile_pics",filename))

            db.session.commit()
            # flash("Profile Updated Successfully",'success')
            u_details={'u_fname':u_fname,'u_lname':u_lname,'u_mobile':u_mobile,'u_address':u_address}
            if(isVendor()):
                return render_template("viewprofile.html",header=True,mail_id=u_email,u_details=u_details,username=session["email"],scripts=["foodcart.js"],itemsDict=vLinksDict,profile_pic=os.path.join("static","data","user_profile_pics",image),removeCartSettings=True)
            return render_template("viewprofile.html",header=True,mail_id=u_email,u_details=u_details,username=session["email"],scripts=["foodcart.js"],itemsDict=uLinksDict,profile_pic=os.path.join("static","data","user_profile_pics",image))

            # db.session.commit()
            # flash("Profile Updated Successfully",'success')

            # u_details={'u_fname':u_fname,'u_lname':u_lname,'u_mobile':u_mobile,'u_address':u_address}

            # return render_template("viewprofile.html",header=True,username=session["email"],mail_id=u_email,u_details=u_details)
        elif(request.method=="GET"):
            # print("asdfghjkl;lkjhgfds")
            u_email=session["email"]
            user=User.query.filter_by(u_email=u_email).first()
            u_details={'u_fname':user.u_fname,'u_lname':user.u_lname,'u_mobile':user.u_mobile,'u_address':user.u_address}
            # print("Printing user image string",user.u_image)
            if user.u_image:
                image = user.u_image
            else:
                image = "profile.png"
            if(isVendor()):
                return render_template("viewprofile.html",header=True,mail_id=u_email,u_details=u_details,username=session["email"],itemsDict=vLinksDict,profile_pic=os.path.join("static","data","user_profile_pics",image),removeCartSettings=True)
            return render_template("viewprofile.html",header=True,mail_id=u_email,u_details=u_details,username=session["email"],itemsDict=uLinksDict,profile_pic=os.path.join("static","data","user_profile_pics",image))

    elif("email" in session and vcheck(session["email"])):
        if (request.method=="POST"):
            v_email=session["email"]
            # print(v_email)
            v_fname=request.form["first name"]
            v_lname=request.form["last name"]
            v_mobile=request.form["mobile"]
            v_address=request.form["Address"]
            # print(v_fname)
            # print(v_mobile)
            user_this=Vendor.query.filter_by(v_email=v_email).first()
            user_this.v_fname=v_fname
            user_this.v_lname=v_lname
            user_this.v_mobile=v_mobile
            user_this.v_address=v_address

            db.session.commit()
            flash("Profile updated successfully",'success')

            u_details={'u_fname':v_fname,'u_lname':v_lname,'u_mobile':v_mobile,'u_address':v_address}
            return render_template("viewprofile.html",header=True,username=session["email"],mail_id=v_email,u_details=u_details,removeCartSettings=True,itemsDict=vLinksDict)
        elif(request.method=="GET"):
            # print("asdfghjkl;lkjhgfds")
            v_email=session["email"]
            vendor=Vendor.query.filter_by(v_email=v_email).first()
            u_details={'u_fname':vendor.v_fname,'u_lname':vendor.v_lname,'u_mobile':vendor.v_mobile,'u_address':vendor.v_address}
            return render_template("viewprofile.html",header=True,username=session["email"],mail_id=v_email,u_details=u_details,removeCartSettings=True,itemsDict=vLinksDict)
        else:
            abort(401)
    else:
        abort(401)

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.clear()
    return redirect(url_for('homepage'))

#helper Functions
def check(email):
    temp=User.query.filter_by(u_email=email).first()
    if(temp is None):
        return False
    return True

def getPassword(email):
    temp=User.query.filter_by(u_email=email).first()
    if (temp is None):
        return None
    else:
        return temp.u_password

def getUID(email):
    temp=User.query.filter_by(u_email=email).first()
    if (temp is None):
        return None
    else:
        return temp.u_id


@app.route("/showrestaurants",methods=["GET"])
def showrestaurants():
    query_parameters = request.args
    page = query_parameters.get('page', 1, type=int)
    if ("email" in session and isUser()):
        uid= session["id"]
        uemail = session["email"]
        if (request.method=="GET"):
            sort = query_parameters.get('sort',"1")
            # print('sort',sort)
            query = "{}".format("Restaurant.query")
            if(sort):
                if (sort=="1"):
                    query += ".order_by((Restaurant.r_rating.desc()))"
                elif (sort=="2"):
                    query += ".order_by(Restaurant.r_rating)"

            # print(query)
            rList=[]
            rRows_paginated=eval(query).paginate(
        page, app.config['MAX_ITEMS_PER_PAGE'], False)
            rRows=rRows_paginated.items
            #rRows=Restaurant.query.all()
            for y in rRows:
                rList.append({'r_id': y.r_id,'r_name': y.r_name,'r_phone': y.r_phone, 'r_address': y.r_address,'r_email': y.r_email,'r_website': y.r_website,'r_location': y.r_location,'r_city':y.r_city,'r_zip':y.r_zip,'r_rating':y.r_rating,'r_images':y.r_images})

            next_url = url_for('showrestaurants',sort=sort, page=rRows_paginated.next_num) \
                        if rRows_paginated.has_next else None
            prev_url = url_for('showrestaurants',sort=sort, page=rRows_paginated.prev_num) \
                        if rRows_paginated.has_prev else None
            return render_template("showrestaurants.html",s=sort,header=True,cartdisabled=True,username=session["email"],itemsDict=uLinksDict,rList=rList,scripts=["foodcart.js"],stylesheets=["style.css"],next_url=next_url,prev_url=prev_url)
    abort(401,"Pls Login as User")


@app.route("/<r_id>/showitems",methods=["GET","POST"])
def showitems(r_id):
    if ("email" in session and isUser()):
        uid= session["id"]
        uemail = session["email"]
        if (request.method=="GET"):
            current_r_id = r_id
            itemsList=Menu.query.filter_by(r_id=current_r_id).all()
            current_r_name=Restaurant.query.filter_by(r_id=current_r_id).first().r_name
            menuitemsList = []
            for item in itemsList:
                menuitemsList.append(dict(zip(item.keys(), item)))
            # print(menuitemsList)
            return render_template("showitems.html",header=True,username=session["email"],itemsDict=uLinksDict,r_id=current_r_id,r_name=current_r_name,iList = menuitemsList,scripts=["foodcart.js"],showButton=True)
    abort(401,"Pls Login as User")


@app.route("/checkout",methods=['GET','POST'])
def checkout():
    if (request.method =='POST'):
        session["u_cart"]=request.get_json() #request.json
        # print(session["u_cart"])
        if (len(session["u_cart"]) ==0):
            return render_template("_userform.html",userform=True,error="Your Cart is  Empty",scripts=["validatePlaceorder.js"])
        return render_template("_userform.html",userform=True,error="Your Cart is Empty",scripts=["validatePlaceorder.js"])
    else:
        return redirect(url_for("genForm"))

@app.route("/getcheckoutform")
def genForm():

    if "u_cart" in session:
        if(request.method=="GET"):
            u_email=session["email"]
            user=User.query.filter_by(u_email=u_email).first()
            u_details={'u_fname':user.u_fname,'u_mobile':user.u_mobile,'u_address':user.u_address}
        return render_template("_userform.html",u_details=u_details,invoice=genInvoice(session["u_cart"]),userform=True,scripts=["foodcart.js","validatePlaceorder.js"],nosidebar=True)
    return render_template("_userform.html",userform=True,error="Add Some Items to Cart",scripts=["foodcart.js","validatePlaceorder.js"],nosidebar=True)



def genInvoice(cart_dict):
    #invoice={}
    invoice = {}
    # print(cart_dict)
    # print(type(cart_dict))
    r_id = list(cart_dict.keys())[0]
    if len(cart_dict)>0:
        x=Restaurant.query.filter_by(r_id =r_id).first()
        r_name = x.r_name
        invoice["items"]=[]
        total = 0
        for key,value in cart_dict[r_id].items():
            # print(key,value)
            # print("##########################")
            each_item_id =key
            each_item_quantity = int(value)
            q=Menu.query.filter_by(i_id = each_item_id).first()
            each_item_price = q.i_cost
            each_item_name = q.i_name
            each_item_price = round(each_item_price*each_item_quantity,2)
            item_details=[key,each_item_name,each_item_quantity, each_item_price]
            item={}
            for i in range(len(item_details)):
                item[i]=item_details[i]
            invoice["items"].append(item)
            total += each_item_price
            invoice["tax"]= round(0.1 * total,2)
            invoice["total"]= round(total + invoice["tax"],2)
        invoice["restaurant"] = r_name

        # x=Restaurant.query.filter_by(r_id = cart_dict["r_id"]).first()
        # r_name = x.r_name
        # invoice["items"]=[]
        # total = 0
        # for key,value in cart_dict["items"].items():
        #     print(key,value)
        #     print("##########################")
        #     each_item_id =value ["i_id"]
        #     each_item_quantity = value["i_quantity"]
        #     q=Menu.query.filter_by(i_id = each_item_id).first()
        #     each_item_price = q.i_cost
        #     each_item_name = q.i_name
        #     each_item_price = round(each_item_price*each_item_quantity,2)
        #     item_details=[key,each_item_name,each_item_quantity, each_item_price]
        #     item={}
        #     for i in range(len(item_details)):
        #         item[i]=item_details[i]
        #     invoice["items"].append(item)
        #     total += each_item_price
        #     invoice["tax"]= round(0.1 * total,2)
        #     invoice["total"]= round(total + invoice["tax"],2)
        # invoice["restaurant"] = r_name

    return invoice



@app.route("/placeorder",methods=["GET","POST"])
def placeorder():
    if (request.method =='POST'):
        phone=""
        notproperlocation=0
        if ("email" in session and isUser() and session.get("u_cart",None)):
            mail=session["email"]
            # print(session["u_cart"])
            if "u_cart" in session:
                count=0

                for i in session["u_cart"]:
                    # print(i)
                    query=Restaurant.query.filter_by(r_id=i).first()
                    for j in session["u_cart"][i]:
                        userid=User.query.filter_by(u_email=mail).first()
                        menuprice=Menu.query.filter_by(i_id=j).first()
                        name=request.form["u_name"]
                        phone=request.form["u_phone"]
                        address=request.form["u_address"]
                        if(query.r_location.lower() in address.lower()):

                            if(count==0):

                                o=Order(o_order_date=datetime.now(),o_u_id=userid.u_id,o_r_id=i,o_i_id=j,o_i_quantity=session["u_cart"][i][j],o_price=menuprice.i_cost,o_name=name,o_phone=phone,o_address=address)
                                db.session.add(o)
                                db.session.flush()
                                temp=o.o_order_date
                                db.session.commit()
                            else:


                                o=Order(o_order_date=temp,o_u_id=userid.u_id,o_r_id=i,o_i_id=j,o_i_quantity=session["u_cart"][i][j],o_price=menuprice.i_cost,o_name=name,o_phone=phone,o_address=address)
                                db.session.add(o)


                                db.session.commit()
                            count+=1

                        else:

                            notproperlocation=1
                            flash("please select a proper location for delivery","success")
                            return render_template("_postordersuccess.html",itemsDict=uLinksDict,username=session["email"],error=notproperlocation)




                flash("your order has been successfully placed.","success")

                del session['u_cart']
                return render_template("_postordersuccess.html",itemsDict=uLinksDict,username=session["email"],error=0)
            flash("please add some items to cart","danger")
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html",header=True)
    else:

        if ("email" in session and isUser()):
            flash("please do checkout before placing an order","danger")
            return redirect(url_for("homepage"))
        elif ("email" in session and isVendor()):
            flash("hello"+session["email"]+"please login as user","danger")
            return render_template("login.html",header=True,username=session["email"])

def vgenInvoice(cart_dict):
    #invoice={}
    invoice = {}
    # print(cart_dict)
    # print(type(cart_dict))
    r_id = list(cart_dict.keys())[0]
    if len(cart_dict)>0:
        x=Restaurant.query.filter_by(r_id =r_id).first()
        r_name = x.r_name
        invoice["items"]=[]
        total = 0
        for key,value in cart_dict[r_id].items():
            # print(key,value)
            # print("##########################")
            each_item_id =key
            each_item_quantity = int(value)
            q=Menu.query.filter_by(i_id = each_item_id).first()
            z=Order.query.filter_by(o_i_id= each_item_id).first()
            each_item_price = z.o_price
            each_item_name = q.i_name

            each_item_price = round(each_item_price*each_item_quantity,2)
            item_details=[key,each_item_name,each_item_quantity, each_item_price]
            item={}
            for i in range(len(item_details)):
                item[i]=item_details[i]
            invoice["items"].append(item)
            invoice["date"] = z.o_order_date
            total += each_item_price
            invoice["tax"]= round(0.1 * total,2)
            invoice["total"]= round(total + invoice["tax"],2)
        invoice["restaurant"] = r_name
    return invoice

@app.route("/vsignup",methods=["GET","POST"])
def vsignup():
    if (request.method=="POST"):
        email=request.form["u_name"]
        password=request.form["u_password"]
        c_password=request.form["u_c_password"]
        if (not vcheck(email)):
            if (password!=c_password):
                flash("Invalid Password",'danger')
                return render_template("vsignup.html",p_error=True,header=True,scripts=["validatesignupform.js"])
            else:
                db.session.add(Vendor(v_email=email,v_password=password))
                db.session.commit()
                flash("Account Created Successfully.You can now login with {} creds".format(email),'success')
            return render_template("vlogin.html",header=True)
        else:
            return render_template("vsignup.html",l_error=True,header=True,scripts=["validatesignupform.js"])
    if ("email" in session):
        return render_template("success.html",email="You are already logged in.You need to sign out to create a new account")
    else:
        return render_template("vsignup.html",header=True,scripts=["validatesignupform.js"])

@app.route("/vlogin/",methods=["GET","POST"])
def vlogin():
        if (request.method=="POST"):
            email=request.form["u_name"]
            password=request.form["u_password"]
            if (vcheck(email)):
                if (password!=vgetPassword(email)):
                    flash("Invalid Password",'danger')
                    return render_template("vlogin.html",p_error=True,header=True)
                else:
                    session["email"]=email
                    session["type"] ="vendor"
                    session["id"] = getVID(email)
                    flash("Successfully logged in as {}".format(email),'success')
                    return redirect(url_for('homepage'))
            else:
                return render_template("vlogin.html",l_error=True,header=True)

        if ("email" in session):
            return redirect(url_for('homepage'))
        else:
            return render_template("vlogin.html",header=True)



@app.route("/vlogout",methods=["GET","POST"])
def vlogout():
    session.clear()
    return redirect(url_for('homepage'))

#Adding Restaurant by Vendor

@app.route("/addrestaurant",methods=["GET","POST"])
def addrestaurant():
    if ("email" in session and vcheck(session["email"])):
        vid=session["id"]
        if (request.method=="POST"):
            # print(request.form)
            r_name = request.form["r_name"]
            r_phone = request.form["r_phone"]
            r_email = request.form["r_email"]
            r_website = request.form["r_website"]
            r_address = request.form["r_address"]
            r_location = request.form["r_location"]
            r_city = request.form["r_city"]
            r_zip = request.form["r_zip"]
            if "file" not in request.files:
                # print("return ")
                return render_template("addrestaurant.html",header=True,removeCartSettings=True,itemsDict=vLinksDict)
            r_image = request.files['file']
            # print(r_image)
            # print(r_image.filename)
            if r_image and allowed_file(r_image.filename):
                filename = secure_filename(r_image.filename)
                MYDIR = os.path.dirname(__file__)
                # print ("Is saving.....", MYDIR)
                r_image.save(os.path.join(MYDIR,app.config['IMAGES_FOLDER'],filename))
                x=Restaurant(r_name=r_name,r_phone=r_phone,r_email=r_email \
                    ,r_website=r_website,r_address=r_address,r_location=r_location,r_city=r_city,r_zip=r_zip,r_images=filename,r_rating=1,r_votesCount=0)
                db.session.add(x)
                db.session.flush()
                db.session.add(VendorRestaurant(v_id = vid,r_id=x.r_id))
                # print("Iam rajesh",x.r_id)
                db.session.commit()
                flash("Successfully Added Restaurant Details",'success')
                return render_template("homepage1.html",header=True,username=session["email"],removeCartSettings=True,itemsDict=vLinksDict)
        elif (request.method=="GET" and getRestaurantCount(vid)>0):
            abort(401,"Currently, you can add only one restaurant.")
        return render_template("addrestaurant.html",header=True,username=session["email"],removeCartSettings=True,itemsDict=vLinksDict)
    abort(401,"Please Login as Vendor")

@app.route("/viewrestaurant",methods=["GET","POST"])
def viewrestaurant():
    if ("email" in session and vcheck(session["email"])):
        vid= session["id"]
        vemail = session["email"]
        if (request.method=="GET" and getRID(vid) is None):
            flash("You must add an Restaurant to add/view a menu","warning")
            return render_template("addrestaurant.html",header=True,username=session["email"],removeCartSettings=True,itemsDict=vLinksDict)
        if (request.method=="GET"):
            # print(session["email"])
            current_v_id=session["id"]
            current_vendor_restaurant=VendorRestaurant.query.filter_by(v_id=current_v_id).first()
            if (current_vendor_restaurant is not None):
                current_r_id = current_vendor_restaurant.r_id
                y=Restaurant.query.filter_by(r_id=current_r_id).first()
                image = os.path.join("static","data","restaurant_images",y.r_images)
                rdict={'r_name': y.r_name,'r_phone': y.r_phone, 'r_address': y.r_address,'r_email': y.r_email,'r_website': y.r_website,'r_location': y.r_location,'r_city':y.r_city,'r_zip':y.r_zip,'r_images':y.r_images}
                # print("printing************",rdict)
                # print(os.path.join(y.r_images))
                return render_template("viewrestaurant.html",header=True,username=session["email"],d=rdict,removeCartSettings=True,itemsDict=vLinksDict)
            return abort(401,"No Restaurants Found")
        elif (request.method=="POST"):
            r_name = request.form["r_name"]
            r_phone = request.form["r_phone"]
            r_email = request.form["r_email"]
            r_website = request.form["r_website"]
            r_address = request.form["r_address"]
            r_location = request.form["r_location"]
            r_city = request.form["r_city"]
            r_zip = request.form["r_zip"]
            filename=""
            # print("file" in request.files)
            # print(request.files)
            if 'file' in request.files:
                r_image = request.files['file']
                # print(r_image)
                if r_image !='':
                    # print(r_image.filename)
                    if r_image and allowed_file(r_image.filename):
                        filename = secure_filename(r_image.filename)
                        MYDIR = os.path.dirname(__file__)
                        # print ("Is saving.....", MYDIR)
                        r_image.save(os.path.join(MYDIR,app.config['IMAGES_FOLDER'],filename))
                        x=dict(r_name=r_name,r_phone=r_phone,r_email=r_email \
                    ,r_website=r_website,r_address=r_address,r_location=r_location,r_city=r_city,r_zip=r_zip,r_images=filename)
            elif 'file' not in request.files:
                current_v_id=session["id"]
                current_vendor_restaurant=VendorRestaurant.query.filter_by(v_id=current_v_id).first()
                current_r_id = current_vendor_restaurant.r_id
                admin = Restaurant.query.filter_by(r_id=current_r_id).first()
                x=dict(r_name=r_name,r_phone=r_phone,r_email=r_email \
                    ,r_website=r_website,r_address=r_address,r_location=r_location,r_city=r_city,r_zip=r_zip,r_images=admin.r_images)
            current_v_id=session["id"]
            current_vendor_restaurant=VendorRestaurant.query.filter_by(v_id=current_v_id).first()
            current_r_id = current_vendor_restaurant.r_id
            admin = Restaurant.query.filter_by(r_id=current_r_id).update(x)
            admin1 = Restaurant.query.filter_by(r_id=current_r_id).first()
            db.session.commit()
            flash("Restaurant Details Updated Successfully",category='success')
            return render_template("viewrestaurant.html",header=True,username=session["email"],d=x,image=os.path.join("static","data","restaurant_images",admin1.r_images),removeCartSettings=True,itemsDict=vLinksDict)
    abort(401,"Please Login As Vendor")

def allowed_file(filename):
    return '.'in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/addmenu",methods=["GET","POST"])
def addmenu():
    if ("email" in session and isVendor()):
        vid= session["id"]
        vemail = session["email"]
        if (request.method=="POST" and getRID(vid) is not None):
            try:
                session["v_menu_cart"]=request.get_json() #request.json
                #session["u_cart"] = request.form["u_cart"]
                # print(session["v_menu_cart"].keys())
                # print(type(session["v_menu_cart"]))
                if (len(session["v_menu_cart"]) ==0):
                    return "Add Some Menu Items"
                i=0
                while(i>-1):
                    # print(i,session["v_menu_cart"])
                    # i_name = request.form["i_name"+str(i)]
                    # i_cost = request.form["i_cost"+str(i)]
                    # i_type = request.form["i_type"+str(i)]
                    # i_maincategory = request.form["i_maincategory"+str(i)]
                    # i_subcategory1 = request.form["i_subcategory1"+str(i)]
                    # i_subcategory2 = request.form["i_subcategory2"+str(i)]
                    # print("i_name"+str(i))
                    i_name = session["v_menu_cart"]["i_name"+str(i)]
                    # print("1")
                    i_cost = session["v_menu_cart"]["i_cost"+str(i)]
                    # print("2")
                    if(session["v_menu_cart"]["i_type"+str(i)]=='Non-veg'):
                        i_type = 'nveg'
                    elif(session["v_menu_cart"]["i_type"+str(i)]=='Veg'):
                        i_type='veg'
                    elif(session["v_menu_cart"]["i_type"+str(i)]=='Egg'):
                        i_type='egg'
                    else:
                        i_type='others'
                    # print("3")
                    i_maincategory = session["v_menu_cart"]["i_maincategory"+str(i)]
                    # print("4")
                    i_subcategory1 = session["v_menu_cart"]["i_subcategory1"+str(i)]
                    # print("5","i_subcategory2"+str(i))
                    i_subcategory2 = session["v_menu_cart"]["i_subcategory2"+str(i)]
                    # print("###")

                    rid= getRID(vid)
                    i_imagebase64 = session["v_menu_cart"]["i_image"+str(i)]
                    i_image_mimecontent= i_imagebase64.split(',')[1]
                    i_imageURL=decodeBase64(i_imagebase64,i_image_mimecontent[0:12].replace('/',str(random.choice(range(100)))))
                    # print("ImageURI",i_imageURL)
                    x=Menu(r_id=rid,i_name=i_name,i_cost=i_cost,i_type=i_type,i_maincategory=i_maincategory,i_subcategory1=i_subcategory1,i_subcategory2=i_subcategory2,i_image=i_imageURL)

                    db.session.add(x)
                    db.session.commit()
                    i=i+1
                    # print("Committed")
            except KeyError:
                # print("keyerror")
                db.session.commit()
                flash("Menu added","success")
                return render_template("addmenu.html",header=True,username=session["email"],removeCartSettings=True,itemsDict=vLinksDict)
        elif (request.method=="GET" and getRID(vid) is None):
            flash("You must add an Restaurant to add/view a menu","warning")
            return render_template("addrestaurant.html",header=True,username=session["email"],removeCartSettings=True,itemsDict=vLinksDict)
        return render_template("addmenu.html",header=True,username=session["email"],scripts=["foodcart.js"],removeCartSettings=True,itemsDict=vLinksDict)
    abort(401,"Pls login as  Vendor")

@app.route("/viewmenu",methods=["GET","POST"])
def viewmenu():
    if ("email" in session  and vcheck(session["email"])):
        vid= session["id"]
        vemail = session["email"]
        if (request.method=="GET" and getRID(vid) is None):
            flash("You must add an Restaurant to add/view a menu","warning")
            return render_template("addrestaurant.html",header=True,username=session["email"],removeCartSettings=True,itemsDict=vLinksDict)
        elif (request.method=="GET"):
            current_v_id=vid
            current_vendor_restaurant=VendorRestaurant.query.filter_by(v_id=current_v_id).first()
            if (current_vendor_restaurant is not None):
                current_r_id = current_vendor_restaurant.r_id
                itemsList=Menu.query.filter_by(r_id=current_r_id).all()
                current_r_name=Restaurant.query.filter_by(r_id=current_r_id).first().r_name
                menuitemsDict = {}
                # count=0
                # for item in itemsList:
                #     menuitemsDict[count] =dict(zip(item.keys(), item))
                #     count+=1

                menuitemsList = []
                for item in itemsList:
                    menuitemsList.append(dict(zip(item.keys(), item)))
                # rdict={'r_name': y.r_name,'r_phone': y.r_phone, 'r_address': y.r_address,'r_email': y.r_email,'r_website': y.r_website,'r_location': y.r_location,'r_city':y.r_city,'r_zip':y.r_zip}
                # return str(menuitemsDict)
                return render_template("showitems.html",header=True,username=session["email"],itemsDict=vLinksDict,r_id=current_r_id,r_name=current_r_name,iList = menuitemsList,scripts=["foodcart.js"],removeCartSettings=True,showButton=False)
                #render_template("viewrestaurant.html",header=True,username=session["email"],d=rdict)
            return abort(401,"No Restaurants Found")
        elif (request.method=="POST"):
            r_name = request.form["r_name"]
            r_phone = request.form["r_phone"]
            r_email = request.form["r_email"]
            r_website = request.form["r_website"]
            r_address = request.form["r_address"]
            r_location = request.form["r_location"]
            r_city = request.form["r_city"]
            r_zip = request.form["r_zip"]
            x=dict(r_name=r_name,r_phone=r_phone,r_email=r_email \
            ,r_website=r_website,r_address=r_address,r_location=r_location,r_city=r_city,r_zip=r_zip)
            current_v_id=session["id"]
            current_vendor_restaurant=VendorRestaurant.query.filter_by(v_id=current_v_id).first()
            current_r_id = current_vendor_restaurant.r_id
            admin = Restaurant.query.filter_by(r_id=current_r_id).update(x)
            db.session.commit()
            flash("Restaurant Details Updated Successfully",category='success')
            return render_template("viewrestaurant.html",header=True,username=session["email"],d=x,removeCartSettings=True,itemsDict=vLinksDict)
    abort(401,"Please Login As Vendor")




#Vendor helper Functions
def vcheck(email):
    temp=Vendor.query.filter_by(v_email=email).first()
    if(temp is None):
        return False
    return True

def vgetPassword(email):
    temp=Vendor.query.filter_by(v_email=email).first()
    if (temp is None):
        return None
    else:
        return temp.v_password

##
def getVID(email):
    temp=Vendor.query.filter_by(v_email=email).first()
    if (temp is None):
        return None
    else:
        return temp.v_id

def getRID(vID):
    temp=VendorRestaurant.query.filter_by(v_id=vID).first()
    if (temp is None):
        return None
    else:
        return temp.r_id

def getRestaurantCount(vID):
    restaurantCount = VendorRestaurant.query.filter_by(v_id=vID).count()
    return restaurantCount


##Code

def isUser():
    if "type" in session:
        return  session["type"]=="user"
    return False

def isVendor():
    if "type" in session:
        return  session["type"]=="vendor"
    return False

def decodeBase64(base64string,outputfile):
    ext = base64string.split(',')[0].split(':')[1].split(';')[0].split('/')[1]
    base64mime = base64string.split(',')[1]
    print("Extension",ext)
    fh = open(os.path.join(app.config['ITEM_PICTURES'],outputfile+"."+ext), "wb")
    fh.write(base64.b64decode(base64mime))
    fh.close()
    return outputfile+"."+ext




@app.errorhandler(401)
def custom_401(error):
    #response = jsonify({'message': error.description})
    return Response(error.description)
    #return Response('Unauthorized Page', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})

@app.errorhandler(404)
def custom_404(error):
    return render_template("error404.html")

if __name__ == '__main__':
    # AddEntriesIntoDB()
    app.run(debug = True,use_reloader=False)
    # app.run()
