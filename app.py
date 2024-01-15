from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User, Feedback
from forms import AddUser, LoginUser, FeedbackForm
from sqlalchemy.exc import DataError, IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "springboard"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register_user():

    form = AddUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password,
                    email=email, first_name=first_name,
                    last_name=last_name)
        
        if isinstance(user, str):
            flash(f"{user} is already taken.", "info")
            return redirect("/register")

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        flash("User successfully created", "success")
        return redirect(f"/users/{username}")

    return render_template("user_register.html", form=form)

@app.route("/users/<username>/delete")
def delete_user(username):

    if session.get("username", False) and session["username"] == username:
        Feedback.query.filter(Feedback.username == username).delete()
        User.query.filter(User.username == username).delete()

        db.session.commit()

        session.pop("username")

        flash("User deleted.", "info")
        return redirect("/")
    
    flash("You don't have permission to delete someone else.", "danger")
    return redirect("/login")

@app.route("/users/<username>")
def secret_page(username):

    if username != session.get("username") or not session.get("username", False):
        flash("Log In First", "dander")
        return redirect("/login")

    user = User.query.get(username)

    return render_template("user_page.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login_user():

    if session.get("username", False):

        flash("You're already logged in.", "info")
        return redirect(f"/users/{session['username']}")

    form = LoginUser()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        userIn = User.query.filter(User.username == username).first()
        if not userIn:
            flash("Invalid username/password.", "danger")
            return redirect("/login")

        user = User.authenticate(username=username, password=password)

        if user:
            flash("Log In Successfully", "success")
            session["username"] = username
            return redirect(f"/users/{username}")

    return render_template("user_login.html", form=form)

@app.route("/logout")
def logout_user():

    session.clear()

    flash("You've been logged out", "success")
    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    if not session.get("username", False) or username != session["username"]:
        flash("First, log in to your account", "danger")
        return redirect("/login")

    form = FeedbackForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback created", "success")
        return redirect(f"/users/{username}")

    return render_template("feedback_add.html", form=form, user=username)

@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def edit_feedback(id):

    feedback = Feedback.query.get(id)

    if not session.get("username", False) or feedback.username != session["username"]:
        flash("First, log in to your account", "danger")
        return redirect("/login")
    
    form = FeedbackForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.commit()

        flash("Feedback edited.", "success")
        return redirect(f"/users/{feedback.username}")
    
    return render_template("feedback_edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:id>/delete")
def delete_feedback(id):

    feedback = Feedback.query.get(id)

    if not feedback:
        flash("Feedback does not exist.", "info")
        return redirect("/login")

    if not session.get("username", False) or feedback.username != session["username"]:
        flash("You can't delete someone else feedback.", "danger")
        return redirect("/login")
    
    db.session.delete(feedback)
    db.session.commit()

    flash("Feedback deleted.", "success")
    return redirect(f"/users/{feedback.username}")