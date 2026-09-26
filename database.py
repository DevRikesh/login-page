import mysql.connector

def get_connection():
    connection = mysql.connector.connect(

        host = "127.0.0.1",
        user = "root",
        password = "123456",
        database="login_system"
       
    )

    return connection
#jtjt


if __name__ == "__main__":
    connection = get_connection()

    if connection.is_connected():
        print("data base connected successfully")
        connection.close()
    



