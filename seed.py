"""Seed file to make sample data for user_db."""

from models import db, User, Feedback

# Drop all tables
db.drop_all()

# Create all tables
db.create_all()

# clean reset the database
# db.engine.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')

# If table isn't empty, empty it
User.query.delete()
Feedback.query.delete()

# Add users
dof = User.register(username="dof", password="112233", email="dof@springboard.com", first_name="Rodolph", last_name="Van Romondt")
david = User.register(username="david", password="aassdd", email="david@springboard.com", first_name="David", last_name="Adawole")
colt = User.register(username="colt", password="zzxxcc", email="colt@springboard.com", first_name="Colt", last_name="Steele")

# Add new objects to session
db.session.add_all([dof, david, colt])

# Commit
db.session.commit()

# Add feedback
feed1 = Feedback(title="Springboard", content="SoftWare Engineering", username="dof")
feed2 = Feedback(title="Springboard", content="Cybersecurty", username="dof")
feed3 = Feedback(title="Springboard", content="SoftWare Engineering", username="david")

# Add new feedback objects to session
db.session.add_all([feed1, feed2, feed3])

# Commit
db.session.commit()
