import os
import flaskr
import unittest
import tempfile

class FlaskrTestCases(unittest.TestCase):

  #sets up database and testing environment
  def setUp(self):
    self.db_file, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    self.app = flaskr.app.test_client()
    flaskr.init_db()

  #get rid of database after each test
  def tearDown(self):
    os.close(self.db_file)
    os.unlink(flaskr.app.config['DATABASE'])

  #helper function to avoid creating a post request
  #by hand every time
  def login(self, username, password):
    return self.app.post('/login',
        data={'username' : username,
              'password' : password},
        follow_redirects=True)

  #helper function to avoid creating a request
  #by hand every time
  def logout(self):
    return self.app.get('/logout', follow_redirects=True)

  """test cases"""

  def test_empty_db(self):
    response = self.app.get('/')
    assert 'No entries here so far' in response.data
  
  def test_login_logout(self):
    response = self.login('admin', 'default')
    assert 'You are logged in' in response.data
    response = self.logout()
    assert 'You were logged out' in response.data

  def test_fail_login(self):
   response = self.login('administrator', 'default')
   assert 'Invalid username or password' in response.data
   response = self.login('admin', 'notDefault')
   assert 'Invalid username or password' in response.data

  def test_new_message(self):
   self.login('admin', 'default')
   response = self.app.post('/add', data={
     'title' : 'Hello',
     'text' : "<strong>HTML</strong> is allowed here"},
     follow_redirects = True)
   assert 'No entries here so far' not in response.data
   assert 'Hello' in response.data
   assert '<strong>HTML</strong> is allowed here' in response.data
if __name__ == '__main__':
  unittest.main()
