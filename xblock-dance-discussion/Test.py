from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
import settings as s
from datetime import date, datetime, timedelta
import mysql.connector as db_connector
import pkg_resources
import sys
        
user_id = ''
parent_comment_id = -1 #This should be set in case the user clicks 'reply to an existing comment'
thread_id = -1 #This should be fetched using the parent_comment_id to fetch it's thread_id
comment = ''
db = None #This is the DB connection. WE NEED TO ENSURE THIS IS CLOSED!

def resource_string( path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")

def get_error_msg():
    return(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))

def exec_query(query, prefix_msg = ""):
    cursor = db.cursor()
    try:
        cursor.execute(query)
    except:
        print(prefix_msg + " Error :" + get_error_msg()) # PROBABLY NEED TO REPLACE THIS WITH A LOGGING STATEMENT!
    else:
        db.commit()
    cursor.close()


def setup_db():
    global db
    config_file = open("db_settings.txt", 'r')
    config = dict()
    for line in config_file:
        (key, value) = line.strip(' \t\r\n').split(':', 1);
        config[str(key).strip()] = str(value).strip()
    print config
    config_file.close()
    db = db_connector.connect(**s.database)
    """
    settings.py contains a dictionary of key value pairs that define the mysql user name + password, the host on
    which the mysql user has been configured, the name of the database to use (the user specified here must be
    granted access to it on the host specified) and whether warnings should raise exceptions (which will show up in
    lms logs.)
    """
    create_query = (resource_string( "./discussion_setup.sql"))
    exec_query( create_query, "Initial Table Create Query")
    test_query = ("INSERT INTO discussion_table (thread_id, user_id, comment, parent_id) VALUES (1, 11, 'Akash made this comment', 1)")
    exec_query( test_query, "Table Insert Query")

setup_db()

db.close()