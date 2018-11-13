import os
import json
from datetime import datetime, timedelta, timezone
import slackweb

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')
tmp_dir = '/tmp'
file_nm = 'score.txt'
score_file_path = os.path.join(tmp_dir, file_nm)
score = '0'

def app(event, context):
    button_type = event['deviceEvent']['buttonClicked']['clickType']
    if button_type == 'SINGLE':
        count_up()
        return button_type
    elif button_type == 'DOUBLE':
        count_down()
        return button_type

    elif button_type == 'LONG':
        push()
        return button_type
    else:
        return button_type

def read_score():
    if not os.path.exists(score_file_path):
        reset()

    with open(score_file_path, 'r') as f:
        tmp_score = f.read()
        return tmp_score

def write_score(tmp_score):
    with open(score_file_path, 'w') as f:
        f.write(tmp_score)

def count_up():
    score = read_score()
    tmp_cnt = int(score)
    tmp_cnt+=1
    write_score(str(tmp_cnt))

def count_down():
    score = read_score()
    tmp_cnt = int(score)
    if tmp_cnt == 0:
        return
    tmp_cnt-=1
    write_score(str(tmp_cnt))

def reset():
    write_score('0')
    
def push():
    push_score = read_score()
    now = datetime.now(JST).strftime('%Y/%m/%d %H:%M')
    payload = '```{} score: {}```'.format(now, push_score)
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=payload, mrkdwn=True)
    reset()
