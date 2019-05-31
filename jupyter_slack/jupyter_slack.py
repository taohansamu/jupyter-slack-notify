import os
import requests
import time
from IPython.core import magic_arguments
from IPython.core.magics import ExecutionMagics
from IPython.core.magic import cell_magic, magics_class
import slackweb

def notify_self(attachments):
    url=os.environ["SLACK_URL"]
    slack = slackweb.Slack(url)
    slack.notify(attachments=attachments)


def construct_time_mess(elapsed):
    day = elapsed // (24 * 3600)
    elapsed = elapsed % (24 * 3600)
    hour = elapsed // 3600
    elapsed %= 3600
    minutes = elapsed // 60
    elapsed %= 60
    seconds = round(elapsed, 1)
    time_mess = ""
    if day > 0:
        time_mess += " {} days".format(day)
    if hour > 0:
        time_mess += " {} hours ".format(hour)
    if minutes > 0:
        time_mess += " {} minutes".format(minutes)
    if seconds >= 0:
        time_mess += " {} seconds".format(seconds)
    return time_mess


@magics_class
class MessengerMagics(ExecutionMagics):

    def __init__(self, shell):
        super().__init__(shell)

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("message", type=str)
    @magic_arguments.argument("--time", "-t", action="store_true")
    def notify(self, line="", cell=None):
        args = magic_arguments.parse_argstring(self.notify, line)
        mess = args.message.replace("\"", "")
        detail={}
        attachment = {}
        start = time.time()
        try:
            self.shell.ex(cell)
            status=0
            {"title": "Sushi",
                "pretext": "Sushi _includes_ gunkanmaki",
                "text": "Eating *right now!*",
                "mrkdwn_in": ["text", "pretext"]}
            detail['status'] = 'Success'
        except BaseException as e:
            detail['status'] = 'Fail'
            detail['error'] = "{!r}".format(e)
            raise e
        finally:
            detail['runtime'] = construct_time_mess(time.time()-start)
            attachment['pretext'] = "'{}'".format(mess) + ' was done !' 
            attachment['title'] = "'{}'".format(mess) + ' was {} !'.format(detail['status'])
            attachment['text'] = '\n'.join(['{}:{}'.format(key, content) for key, content in detail.items()]) 
            notify_self([attachment])
