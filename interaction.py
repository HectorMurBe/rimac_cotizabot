from rivescript import RiveScript
import os
rives=os.path.realpath("./rives")
rs = RiveScript()
rs.load_directory(rives)
rs._utf8=True
rs.sort_replies()
def get_bot_response(message,usr_id):
    return rs.reply(usr_id, message)

def get_bot_subs(message,usr_id):
    rives=os.path.realpath("./subs")
    rss = RiveScript()
    rss.load_directory(rives)
    rss._utf8=True
    rss.sort_replies()
    return rss.reply(usr_id,message)
