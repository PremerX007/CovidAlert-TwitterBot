import logging
import requests

def line_notify(msg, stickerPackageId : int = None, stickerId : int = None):
    line_token = '**** private ****'
    line_url = 'https://notify-api.line.me/api/notify'
    HEADERS = {'Authorization': 'Bearer ' + line_token}
    response = requests.post(line_url,headers=HEADERS,params={"message": msg,"stickerPackageId": stickerPackageId, "stickerId": stickerId})
    return logging.info("[LINE NOTIFY] %s", response)

if __name__ == '__main__':
    line_notify('Test Message Sent to LINE Notify [Service Available]')