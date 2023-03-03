from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_homepage(self):
        with app.test_client() as client:
            # import pdb
            # pdb.set_trace()
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 id="timer"></h3>', html)
            self.assertIn('board', session)

    def test_valid_word(self):
        with app.test_client() as client:
             with client.session_transaction() as session_change:
                session_change['board'] = [['h', 'e', 'l', 'l', '0'],
                                           ['h', 'e', 'l', 'l', '0'],
                                           ['h', 'e', 'l', 'l', '0'],
                                           ['h', 'e', 'l', 'l', '0'],
                                           ['h', 'e', 'l', 'l', '0']]
                res = client.get('/valid-word?guess=hello')
                self.assertEqual(res.json['result'], 'ok')

    def test_show_high_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_played'] = 10
                change_session['high_score'] = 10

            client.get('/score')
            # res_post = client.post('/score', data={'score': 20})
            self.assertEqual(session['game_played'], 10)
            self.assertEqual(session['high_score'], 10)
