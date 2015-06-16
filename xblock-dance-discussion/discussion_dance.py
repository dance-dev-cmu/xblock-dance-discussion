from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
import settings
import sys
import mysql.connector as db_connector
import pkg_resources
from xblock.fragment import Fragment


"""
TO DO:
Add exception handling for ALL database operations.
Replace console prints with logging statements
Separate out functions into their own modules (ex. All DB functions into a separate DB module)
Add more documentation when possible
#Conform to conventions (dance-discussion vs. discussion-dance for ids)
#CHECK DOUBLE QUOTES AND WILDCARD CHARACTER CASES which may be embedded in the user comment supplied via Ajax

"""

class DiscussionDance(XBlock):

    """
    This XBlock creates a discussion thread that conforms to the requirements of DiscourseDB
    (see https://groups.google.com/forum/#!topic/dancecollab/R9UQ5DysfmQ), which is an initiative of the DANCE group at
    CMU (http://www.cs.cmu.edu/~dance/)
    """
    config_file_path = "/usr0/home/akashb/proto-discussion-workspace/xblock-dance-discussion/xblock-dance-discussion/db_settings.txt"
    user_id = ''
    parent_comment_id = -1 #This should be set in case the user clicks 'reply to an existing comment'
    thread_id = -1 #This should be fetched using the parent_comment_id to fetch it's thread_id
    comment = ''
    db = None #This is the DB connection. WE NEED TO ENSURE THIS IS CLOSED!

    @staticmethod
    def resource_string(path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @staticmethod
    def get_error_msg():
        return(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))

    @staticmethod
    def exec_query(query, prefix_msg = ""):
        cursor = DiscussionDance.db.cursor()
        ret_val = 0
        try:
            cursor.execute(query)
        except:
            print(prefix_msg + " Error :" + DiscussionDance.get_error_msg()) # PROBABLY NEED TO REPLACE THIS WITH A LOGGING STATEMENT!
            ret_val = 1
        else:
            DiscussionDance.db.commit()
        cursor.close()
        return ret_val

    @XBlock.json_handler
    def post_comment(self, data, suffix=''):
        ajax_comment = data.get('comment')
        """
        The ajax supplied comment may have ' (apostrophe/single quote) embedded in it. These must be escaped before
        being put into the SQL query (which itself relies on single qutes when inserting strings).
        """
        safe_comment = ""
        for char in ajax_comment:
            if (char != "'"):
                safe_comment += char
            else:
                safe_comment +="\\'" #Escaping the embedded single quote using a single \. We use \\ to escape it in python as well
                #ALSO CHECK DOUBLE QUOTES AND WILDCARD CHARACTER CASES!!!
        insert_query = ("INSERT INTO discussion_table (thread_id, user_id, comment, parent_id) VALUES (2, 22, '" + safe_comment + "', 2)")
        "NOTE: THERE IS A PROBLEM HERE. If the comment has any single quotes in it, then then query will become invalid. Single quotes need to be safely escaped!"
        ret_val = DiscussionDance.exec_query(insert_query,"Inserting user comment")
        if(ret_val == 0):
            return {'update_status': "Success"}
        else:
            return {'update_status': "Failure"}


    @staticmethod
    def setup_db():
        config_file = open(DiscussionDance.config_file_path, 'r')
        #This path may not be know bythe person configuring the file on the edx server
        config = dict()
        for line in config_file:
            (key, value) = line.strip(' \t\r\n').split(':', 1)
            if str(value).strip() == 'True':
                config[str(key).strip()] = True
            else:
                config[str(key).strip()] = str(value).strip()

        print config
        config_file.close()

        DiscussionDance.db = db_connector.connect(**config)
        """
        settings.py (imported as s) contains a dictionary of key value pairs that define the mysql user name + password, the host on
        which the mysql user has been configured, the name of the database to use (the user specified here must be
        granted access to it on the host specified) and whether warnings should raise exceptions (which will show up in
        lms logs.)
        """
        create_query = (DiscussionDance.resource_string("./discussion_setup.sql"))
        DiscussionDance.exec_query(create_query, "Creating Table")
        test_query = ("INSERT INTO discussion_table (thread_id, user_id, comment, parent_id) VALUES (1, 11, 'Akash made this comment via XBlock', 1)")
        DiscussionDance.exec_query(test_query, "Inserting test value")

    def student_view(self, context):
        """
        Create a fragment used to display the XBlock to a student.
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """
        DiscussionDance.setup_db()
        html = DiscussionDance.resource_string('./static/html/student_view.html')
        frag = Fragment(unicode(html).format(self=self,comment=self.comment))
        css = DiscussionDance.resource_string('./static/css/discussion_dance.css')
        frag.add_css(unicode(css))
        js = DiscussionDance.resource_string('./static/js/discussion_dance.js')
        frag.add_javascript(unicode(js))
        frag.initialize_js('discussion_dance')
        return frag

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("Discussion XBlock for DANCE",
            """
            <vertical_demo>
                <discussion_dance/>
            </vertical_demo>
            """)
        ]