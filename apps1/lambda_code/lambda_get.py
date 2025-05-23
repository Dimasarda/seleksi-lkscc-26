import pymysql
import os
import json

# Environment variables
db_host = os.environ['rds-mariadb.chkc0ig2468z.us-west-2.rds.amazonaws.com']
db_user = os.environ['dimas']
db_pass = os.environ['dimas123arda']
db_name = os.environ['datadata']

def lambda_handler(event, context):
    try:
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            db=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        users = fetch_all_users(conn)

        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps(users)
        }

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        if 'conn' in locals() and conn:
            conn.close()

    return response

def fetch_all_users(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT nama, kelas, sekolah, gender FROM users")
        return cursor.fetchall()
