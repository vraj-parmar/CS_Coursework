import sqlite3
from stock_forecasting import create_usertable, add_userdata, view_all_users


def test_create_usertable():
    conn = sqlite3.connect(':memory:')  # Use an in-memory database for testing
    c = conn.cursor()
    create_usertable(c)

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='userstable';")
    assert c.fetchone() is not None


def test_add_userdata():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    create_usertable(c)

    username = "testuser"
    password = "testpassword"
    name = "Test User"
    add_userdata(username, password, name, conn, c)

    c.execute("SELECT * FROM userstable WHERE username = ?", (username,))
    assert c.fetchone() is not None


def test_view_all_users():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    create_usertable(c)

    users = view_all_users(c)
    assert isinstance(users, list)
