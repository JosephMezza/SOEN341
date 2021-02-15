import mysql.connector 

db = mysql.connector.connect( 
    host ="localhost",
    user= "root",
    passwd= "Mamba248",
    port= 3306,
    database= "initialdatabase"
)

cr = db.cursor()

#cr.execute("CREATE TABLE User_info (user VARCHAR(20), password VARCHAR(16), followers INT(255))")


 
