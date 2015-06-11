from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
import settings as s

import mysql.connector as db_conn
import pkg_resources


class DiscussionDance(XBlock):

    """
    This XBlock creates a discussion thread that conforms to the requirements of DiscourseDB
    (see https://groups.google.com/forum/#!topic/dancecollab/R9UQ5DysfmQ), which is an initiative of the DANCE group at
    CMU (http://www.cs.cmu.edu/~dance/)
    """

    user_id = ''
    parent_comment_id = -1 #This should be set in case the user clicks 'reply to an existing comment'
    thread_id = -1 #This should be fetched using the parent_comment_id to fetch it's thread_id
    comment = ''

    @staticmethod
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def make_db_connection(self):
        db = db_conn.connect(**s.database)
        """
        settings.py contains a dictionary of key value pairs that define the mysql user name + password, the host on
        which the mysql user has been configured, the name of the database to use (the user specified here must be
        granted access to it on the host specified) and whether warnings should raise exceptions (which will show up in
        lms logs.)
        """
        create_query = (self.resource_string(self, "./discussion_setup.sql"))
        cursor = db.cursor()
        cursor.execute(create_query)
        db.close()

