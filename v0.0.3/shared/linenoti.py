import logging
from ..shared import api # azure path
# import api # local test standalone
import requests

def line_notify(msg, **kwangs: int):
    line_url = 'https://notify-api.line.me/api/notify'
    HEADERS = {'Authorization': 'Bearer ' + api.LINE_TOKEN}
    response = requests.post(line_url,headers=HEADERS,params={"message": msg,"stickerPackageId": kwangs.get('stickerPackageId'),"stickerId": kwangs.get('stickerId')})
    return logging.info("[LINE NOTIFY] %s", response)

if __name__ == '__main__':
    line_notify('Test Message Sent to LINE Notify')