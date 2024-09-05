from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_manager, LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash



# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='harshithbhaskar'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(1000))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost:4136/farmers'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost:4136/farmer_database'

db=SQLAlchemy(app)


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))


# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))

class farmers(db.Model):
    farmer_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    farming_experience = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    town_village = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    


class land_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    soil_type = db.Column(db.String(255), nullable=False)
    irrigation_system = db.Column(db.String(255), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    farmer = db.relationship('User', backref=db.backref('land_details', lazy=True))

class crops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    planting_date = db.Column(db.Date, nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    expected_yield = db.Column(db.Integer, nullable=False)
    actual_yield = db.Column(db.Integer, nullable=False)
    fertilizers_used = db.Column(db.String(255), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    farmer = db.relationship('User', backref=db.backref('crops', lazy=True))


class addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)



class trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    farmer_id=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))




class farm_equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    farmer = db.relationship('User', backref=db.backref('farm_equipment', lazy=True))

class farm_animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    breed = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_status = db.Column(db.String(255), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    farmer = db.relationship('User', backref=db.backref('farm_animals', lazy=True))


class labour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    town_village = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    farmer = db.relationship('User', backref=db.backref('labours', lazy=True))

class labour_hiring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    labour_id = db.Column(db.Integer, db.ForeignKey('labour.id'))
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hiring_date = db.Column(db.Date, nullable=False)
    no_of_days_worked = db.Column(db.Integer, nullable=False)
    labour_cost = db.Column(db.DECIMAL(10, 2), nullable=False)
    labour = db.relationship('labour', backref=db.backref('hiring', lazy=True))
    farmer = db.relationship('User', backref=db.backref('labour_hiring', lazy=True))


    

@app.route('/')
def index(): 
    return render_template('index.html')



@app.route('/crops', methods=['POST', 'GET'])
@login_required
def addcrop():
    if request.method == "POST":
        crop_type = request.form.get('type')
        planting_date = request.form.get('planting_date')
        harvest_date = request.form.get('harvest_date')
        expected_yield = request.form.get('expected_yield')
        actual_yield = request.form.get('actual_yield')
        fertilizers_used = request.form.get('fertilizers_used')

        crop = Crops(
            type=crop_type,
            planting_date=planting_date,
            harvest_date=harvest_date,
            expected_yield=expected_yield,
            actual_yield=actual_yield,
            fertilizers_used=fertilizers_used,
            farmer_id=current_user.id
        )

        db.session.add(crop)
        db.session.commit()

        flash("Crop Added", "success")

    return render_template('crops.html')  # Adjust the template name as needed

@app.route('/farmequipments', methods=['POST', 'GET'])
@login_required
def addfarmequipment():
    if request.method == "POST":
        equipment_type = request.form.get('type')
        model = request.form.get('model')
        price = request.form.get('price')
        purchase_date = request.form.get('purchase_date')

        farm_equipment = FarmEquipment(
            type=equipment_type,
            model=model,
            price=price,
            purchase_date=purchase_date,
            farmer_id=current_user.id
        )

        db.session.add(farm_equipment)
        db.session.commit()

        flash("Farm Equipment Added", "success")

    return render_template('farm_equipments.html')
      # Adjust the template name as needed

@app.route('/labour', methods=['POST', 'GET'])
@login_required
def addlabour():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gender = request.form.get('gender')
        phone_no = request.form.get('phone_no')
        state = request.form.get('state')
        district = request.form.get('district')
        town_village = request.form.get('town_village')
        pincode = request.form.get('pincode')

        labour = labour(
            fname=fname,
            lname=lname,
            gender=gender,
            phone_no=phone_no,
            state=state,
            district=district,
            town_village=town_village,
            pincode=pincode,
            farmer_id=current_user.id
        )

        db.session.add(labour)
        db.session.commit()

        flash("Labour Added", "success")

    return render_template('labour.html')  # Adjust the template name as needed

@app.route('/labourhiring', methods=['POST', 'GET'])
@login_required
def hirelabour():
    if request.method == "POST":
        labour_id = request.form.get('labour_id')
        hiring_date = request.form.get('hiring_date')
        no_of_days_worked = request.form.get('no_of_days_worked')
        labour_cost = request.form.get('labour_cost')

        labour_hiring = labour_hiring(
            labour_id=labour_id,
            farmer_id=current_user.id,
            hiring_date=hiring_date,
            no_of_days_worked=no_of_days_worked,
            labour_cost=labour_cost
        )

        db.session.add(labour_hiring)
        db.session.commit()

        flash("Labour Hired", "success")

    return render_template('labour_hiring.html')  # Adjust the template name as needed

@app.route('/farmanimals', methods=['POST', 'GET'])
@login_required
def addfarmanimal():
    if request.method == "POST":
        name = request.form.get('name')
        breed = request.form.get('breed')
        gender = request.form.get('gender')
        age = request.form.get('age')
        health_status = request.form.get('health_status')

        farm_animal = farm_animals(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            health_status=health_status,
            farmer_id=current_user.farmer_id
        )

        db.session.add(farm_animal)
        db.session.commit()

        flash("Farm Animal Added", "success")

    return render_template('farm_animals.html')  # Adjust the template name as needed

@app.route('/agroproducts')
def agroproducts():
    # query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    query=addagroproducts.query.all()
    return render_template('agroproducts.html',query=query)

@app.route('/addagroproduct',methods=['POST','GET'])
@login_required
def addagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        products=addagroproducts(username=username,email=email,productname=productname,productdesc=productdesc,price=price)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addagroproducts.html')

@app.route('/triggers')
@login_required
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/landdetails', methods=['POST', 'GET'])
@login_required
def landdetails():
    if request.method == "POST":
        # farmingtype = request.form.get('farming')
        # query = Farming.query.filter_by(farmingtype=farmingtype).first()

        # if query:
        #     flash("Farming Type Already Exists", "warning")
        #     return redirect('/addfarming')

        # farming = Farming(farmingtype=farmingtype)
        # db.session.add(farming)
        # db.session.commit()

        size = request.form.get('size')
        location = request.form.get('location')
        soil_type = request.form.get('soil_type')
        irrigation_system = request.form.get('irrigation_system')

        land_details = land_details(
            size=size,
            location=location,
            soil_type=soil_type,
            irrigation_system=irrigation_system,
            farmer_id=current_user.id
        )

        db.session.add(land_details)
        db.session.commit()

        flash("Land Details Added", "success")

    return render_template('land_details.html')


@app.route('/farmerdetails')
@login_required
def farmerdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=farmers.query.all()
    return render_template('farmerdetails.html',query=query)

@app.route("/delete/<string:farmer_id>",methods=['POST','GET'])
@login_required
def delete(farmer_id):
    # db.engine.execute(f"DELETE FROM `register` WHERE `register`.`rid`={rid}")
    post=farmers.query.filter_by(farmer_id=farmer_id).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/farmerdetails')

@app.route("/editfarmer/<int:farmer_id>", methods=['POST', 'GET'])
@login_required
def edit_farmer(farmer_id):
    if request.method == "POST":
        farmername = request.form.get('farmername')
        lname = request.form.get('lname')
        dob = request.form.get('dob')
        farming_experience = request.form.get('farming_experience')
        phonenumber = request.form.get('phonenumber')
        state = request.form.get('state')
        district = request.form.get('district')
        town_village = request.form.get('town_village')
        pincode = request.form.get('pincode')
        

        farmer = farmers.query.get(farmer_id)
        farmer.fname = farmername
        farmer.lname = lname
        farmer.dob = dob
        farmer.farming_experience = farming_experience
        farmer.phone_no = phonenumber
        farmer.state = state
        farmer.district = district
        farmer.town_village = town_village
        farmer.pincode = pincode
        

        db.session.commit()
        flash("Farmer details updated successfully", "success")
        return redirect('/farmerdetails')

    farmer = farmers.query.get(farmer_id)
    return render_template('editfarmer.html', farmer=farmer)



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=user(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","warning")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/farmerRegister',methods=['POST','GET'])
@login_required
def farmer_Register():
    # farming = Farming.query.all()  # Assuming Farming is another model you have defined

    if request.method == "POST":
        farmername = request.form.get('fname')
        lname = request.form.get('lname')  # Add missing form fields as needed
        dob = request.form.get('dob')
        farming_experience = request.form.get('farming_experience')
        phonenumber = request.form.get('phone_no')
        state = request.form.get('state')
        district = request.form.get('district')
        town_village = request.form.get('town_village')
        pincode = request.form.get('pincode')
        

        # Create a new instance of the Farmers class
        new_farmer = farmers(
            fname=farmername,
            lname=lname,
            dob=dob,
            farming_experience=farming_experience,
            phone_no=phonenumber,
            state=state,
            district=district,
            town_village=town_village,
            pincode=pincode
            
        )

        # Add the new farmer to the database
        db.session.add(new_farmer)
        db.session.commit()

    return render_template('farmer.html')  
    

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    
