def get_user(db, key, val):
    """Search in db for row where a value corresponds to a specific key (col)"""
    VALID_KEYS = {'Username', 'Email', 'First_Name', 'Last_Name'}
    if key not in VALID_KEYS:
        print('Key {} is not a valid query key'.format(key))
        return
    cr = db.cursor(dictionary=True)
    cr.execute("SELECT * FROM users WHERE {} = '{}'".format(key, val))
    user = cr.fetchall()
    cr.close()
    return user


def get_all_users(db):
    cr = db.cursor(dictionary=True)
    cr.execute("SELECT * FROM users")
    users = cr.fetchall()
    cr.close()
    return users


def add_user(db, user, commit=True):
    "Add a user to the database"
    cursor = db.cursor()

    add_user = ("INSERT INTO users (Username, Email, First_Name, Last_Name, Password) VALUES ({})".format(
        *user.getUser()))

    # Insert new user
    cursor.execute(add_user)

    # commit to database unless specified
    if commit:
        db.commit()

    cursor.close()
    return
