
'''

from getids import get_date_as_string



def get_creation_date(id: int) -> str:
	if str(id)[0] == '5' and str(id)[1] == '9':
		return '01/2023'
	if len(str(id)) == 10:
		if str(id)[0] == '5':
			if not str(id)[1] == '0':
				return '0{}/2022'.format(str(id).replace("0","")[2])
			else:
				return '0{}/2022'.format(str(id)[2])
		elif str(id)[0] == '1' and str(id)[1] == '0':
			if '11' in str(id):
				return '11/2020'
			if '12' in str(id):
				return '12/2020'
			else:
				return '0{}/2020'.format(str(id).replace("0","")[2])
		else:
			if '11' in str(id):
				return '11/2021'
			if '12' in str(id):
				return '12/2021'
			if '10' in str(id):
				return '10/2021'
			else:
				return '0{}/2021'.format(str(id).replace("0","")[1])
	if len(str(id)) == 9:
		if str(id)[0] == '9':
			return '0{}/2020'.format(str(id).replace("0","")[0])
		else:
			return get_date_as_string(id)[1]
	else:
		return get_date_as_string(id)[1]
'''

import requests
from config import r


def get_creation_date(id: int) -> str:
    cache_key = f"{id}:CreateDate"
    cached = r.get(cache_key)
    if cached:
        return cached

    try:
        response = requests.post(
            "https://restore-access.indream.app/regdate",
            headers={
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded",
                "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
                "accept-language": "en-US,en;q=0.9",
            },
            json={"telegramId": id},
            timeout=10,
        )
        response.raise_for_status()
        value = response.json()["data"]["date"].replace("-", "/")
    except (requests.RequestException, KeyError, TypeError, ValueError):
        return "غير معروف"

    r.set(cache_key, value, ex=86400 * 30)
    return value
