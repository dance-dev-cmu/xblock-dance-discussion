from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
import settings as s

import mysql.connector as db_conn
import pkg_resources


#@staticmethod
#def resource_string(self, path):
def resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")

#def make_db_connection(self):
def make_db_connection():
    db = db_conn.connect(**s.database)
    """
     settings.py contains a dictionary of key value pairs that define the mysql user name + password, the host on
     which the mysql user has been configured, the name of the database to use (the user specified here must be
    granted access to it on the host specified) and whether warnings should raise exceptions (which will show up in
    lms logs.)
    """
    #create_query = (self.resource_string(self, "./discussion_setup.sql"))
    create_query = (resource_string( "./discussion_setup.sql"))
    cursor = db.cursor()
    cursor.execute(create_query)
    test_query=("INSERT INTO discussion_table VALUES (1,-1,-1,'HELLO! FIRST COMMENT', -1,12/12/2015)")
    cursor.execute(test_query) #-----> THIS DID NOT WORK!!! ALSO, FIGURE OUT HOW TO GET AUTOINCREMENT TO WORK!
    cursor.close()
    db.close()
        
user_id = ''
parent_comment_id = -1 #This should be set in case the user clicks 'reply to an existing comment'
thread_id = -1 #This should be fetched using the parent_comment_id to fetch it's thread_id
comment = ''

make_db_connection()