from app import app

from unittest import TestCase
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True


db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    def setUp(self):

        User.query.delete()

        user = User(first_name="Nick", last_name="F",
                    image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/3">Nick F</a></li>', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Nick F</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            new = {"first_name": "TestUser",
                   "last_name": "Number2", "image_url": ""}
            resp = client.post("/", data=new, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/2">TestUser Number2</a></li>', html)
