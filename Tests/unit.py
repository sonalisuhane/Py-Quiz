import unittest, os
from app import app, db
from app.models import User,Question, Result, feedback, MCQ, Post

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.session.query(User).delete()
        db.create_all()
        u=User(id =1,username='dk',email='dk@dk.com')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.session.drop_all()

    def test_set_pw(self):
        u = User.query.get(1)
        u.set_password('dk')
        self.assertFalse(u.check_password('passw0rd'))
        self.assertTrue(u.check_password('dk'))
        
    def test_set_pw2(self):
        u = User.query.get(1)
        u.set_password('dk2')
        self.assertFalse(u.check_password('dk2'))
        self.assertTrue(u.check_password('dk'))

if __name__=='__main__':
    unittest.main(verbosity=2)
