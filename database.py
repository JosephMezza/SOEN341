import mysql.connector 

db = mysql.connector.connect( 
    host ="localhost",
    user= "root",
    passwd= "Mamba248",
    port= 3306,
    database= "initialdatabase"
)

cr = db.cursor()

cr.execute("CREATE TABLE user_info (user VARCHAR(20), password VARCHAR(16), email VARCHAR(100), follower1 VARCHAR(20), follower2 VARCHAR(20), follower3 VARCHAR(20))")

sql = "INSERT INTO user_info (user, password, email, follower1, follower2, follower3) VALUES (%s, %s, %s, %s, %s, %s)"
val = [
    ('Peter', 'Hello123', 'peter@hotmail.com', 'Johnny', 'Kevin', 'Jason'),
    ('Jason', 'Password1', 'Jason.h@gmail.com', 'Johnny', 'Kevin', 'Richard'),
    ('Johnny', 'notapassword', 'johnny.yespapa@yahoo.com', 'Kevin', 'Richard', 'Kate'),
    ('Kevin', 'donthackme', 'Kevin.Durant@gmail.com', 'Richard', 'Kate', 'Peter'),
    ('Kate', 'Hardpassword11', 'Katey@hotmail.com', 'Peter', 'Johnny', 'Jason')
]
cr.executemany(sql,val)

db.commit() 
