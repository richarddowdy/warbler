"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.user1 = User.signup(email="user1@gmail.com",
                            username="username1",
                            password="password1",
                            image_url=None
                            )

        self.user2 = User.signup(email="user2@gmail.com",
                            username="username2",
                            password="password2",
                            image_url=None
                            )

        self.user3 = User.signup(email="user3@gmail.com",
                            username="username3",
                            password="password3",
                            image_url=None
                            )

        # db.session.add_all([self.user1, self.user2, self.user3])
        db.session.commit()

        self.client = app.test_client()
        # self.user1 = user1
        # self.user2 = user2
        # self.user3 = user3


    def tearDown(self):
        """Clean up fouled transactions"""

        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_is_following(self):
        """Does is_following properly check who a user is following."""

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess["curr_user"] = self.user1.id
        user1 = self.user1
        user2 = self.user2
        user3 = self.user3

        user1.following.append(user2)
        self.assertEqual(user1.is_following(user2), True)
        self.assertEqual(user1.is_following(user3), False)

    def test_is_followed_by(self):
        """
        Does is_followed_by successfully detect when user1 is followed
        by user3.
        """

        user1 = self.user1
        user2 = self.user2
        user3 = self.user3

        user1.followers.append(user3)
        self.assertEqual(user1.is_followed_by(user3), True)
        self.assertEqual(user1.is_followed_by(user2), False)
    
    def test_user_created(self):
        """
        Does User.create successfully create a new user given
        valid credentials?
        """

        user1 = self.user1
        user2 = self.user2
        user3 = User.signup(email="user3@gmail.com",
                            username="username1",
                            password="password3",
                            image_url=None
                            )

        db.session.add_all([user1, user2, user3])
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_user_authenticate(self):
        """
        Does User.authenticate successfully return a user 
        when given a valid username and password?
        """

        user1 = self.user1
        user2 = self.user2

        db.session.add_all([user1, user2])
        db.session.commit()
        
        self.assertEqual(User.authenticate(user1.username, '345345'), False)
        self.assertEqual(User.authenticate(user2.username, 'password2'), user2)


