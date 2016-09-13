from nose.tools import *
from thespomat.bot import ThespomatBot

b = None


def setup():
    global b
    b = ThespomatBot()
    b.auth()


def teardown():
    pass


# def test_tweet():
#     b.tweet()


def test_clear():
    b.clear()
