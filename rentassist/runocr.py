import json
import requests


def run_ocr(filename, overlay=False, api_key='K89066063988957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    
    reading =  r.content.decode()
    y = json.loads(reading)
    _reading = y['ParsedResults'][0]['ParsedText']
    res = _reading.replace('o', '0')
    res = res.replace('T', '1')
    res = res.replace('E', '')
    res =res.replace('Z', '2')
    res = res.replace(' ', '')
    print(res)
    return res