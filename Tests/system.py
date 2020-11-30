import unittest, os
from app import app, db
from app.models import User, Post
from selenium import webdriver
import time
basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path = os.path.join(basedir,'geckodriver'))
        if not self.driver:
            self.skipTest
        else:
            db.init_app(app)
            db.create_all()
            db.session.query(User).delete()
            db.session.query(Post).delete()
            u=User(id=1,username='dk',email='dk@dk.com')
            u.set_password('dk')
            db.session.add(u)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.query(Post).delete()
            db.session.commit()
            db.session.remove()

    def testlogin(self):
        self.driver.get('http://localhost:5000')
        time.sleep(1)
        user_field =self.driver.find_element_by_id('username')
        password_field =self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        user_field.send_keys('Dk')
        password_field.send_keys('dk')
        submit.click()
        time.sleep(1)

        header=self.driver.find_element_by_id('header').get_attribute('innerHTML')
        self.assertEqual(greeting, 'Python questionnaire to check your proficiency!')

if __name__=='__main__':
    unittest.main(verbosity=2)
