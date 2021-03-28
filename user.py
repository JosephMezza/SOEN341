def get_user(db, key, val):
    """Search in db for row where a value corresponds to a specific key (col)"""
    VALID_KEYS = {'Username', 'Email', 'First_Name', 'Last_Name'}
    if key not in VALID_KEYS:
        print('Key {} is not a valid query key'.format(key))
        return
    cr = db.cursor()
    cr.execute("SELECT * FROM users WHERE {} = '{}'".format(key, val))
    user = cr.fetchall()
    cr.close()
    return user


def get_all_users(db):
    cr = db.cursor()
    cr.execute("SELECT * FROM users")
    users = cr.fetchall()
    cr.close()
    return users

def add_user(db, username, password, email, first_name, last_name):
    "Add a user to the database"
    pass
