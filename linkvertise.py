import json
import random
import requests

_headers = {"Referer": 'https://rentry.co/'}

AUTH_KEY = "752f1ff6d7c56216425e1b9541ac8a2f356f9069b04630aa16d8670bc2529edb"

cookies = {
    'XSRF-TOKEN': 'eyJpdiI6IlRTNE1aK3EyWU9yRk13T3MrVkJ5RFE9PSIsInZhbHVlIjoiVlExTXNUSzJKV0pMU2FkN0FJTmZlQ1dnRlZid0RzNy9lZGtpYUxja3NCVTcwOWk1aVRkS2h6UXZoM2ViNlVCQWZvUXd0M0lhNHRKbXZsZEkwYnpIc0lJOG5FU1crLzJyaGJYQkhPVUhrTmRmQU5mb1FsQUxCcjRpNHB6SGtraUgiLCJtYWMiOiI2NmVhNDg3MDc0ZDljZTI0NzMzZmU2NjVkYzk1ZmNlMDJkYWU0NzlkOGI5YTM4MzBjYTE4ZWEwMmVkNDVhNWJmIiwidGFnIjoiIn0%3D',
    'laravel_session': 'TK7VmFjvN94CtzshYWulfdGMHUPwGbEB47ve7lVc',
    '_cf_bm': '598RGyLGlVPAC4U12V0YLfjgJfErmR3eKiAVsIsGdkM-1720572413-1.0.1.1-9wYLcJFASi0LjbbDaUlseBhhx.cFHPi.LkO8lv8ZEX5rQBDHdts_G5em0F4RyV_sfZzBM7qfQ1OorJT9Ywn9.A',
    'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6ImN6SWNVRHRaR2dDM29oTCtKWEw3Nnc9PSIsInZhbHVlIjoiTkQvWmxnRVdIUnFpRHhwR0hiQ2JhWU9Cd2U3SXhvL1Z2ekpoSFQxeWQxQXd0QWQ2bDZrZGVBcThGWDl3QkdoTEY3Y0dQQUgrelpzNHd4UEE1bHVVTHNiOXBOU3cyY0IzbGtzR0FmMVU1czE3MUhsWG9nNTNJYWFTeHZpRXVxU1lOcTgvZ0owZWVrT3RramxFcEJacWZxTzh6SWkxV0EvZEhxQ2w3SkZZREYrSjZVOXhsUFJicnpPN1F4OHNkWXFKQkU0ajVLeTNEMnN6cks0YU5zWExuNktUUnZMZUhkT2w4eG9iUkxBSWZCaz0iLCJtYWMiOiIyOWQ1OGJjMjU3NzUzMjg5Mzg1ZTM4ODc0MzliOWU3ZWY1NmIwZjJkZTNlNjA5ZTRkNDk2NTJlZjQ2MGQwMjc5IiwidGFnIjoiIn0%3D',
}

async def generate_linkvertise_link(main_url):
    BASE_URL = "https://publisher.linkvertise.com/graphql"
    headers = {
        "Authorization" : f"Bearer {AUTH_KEY}",
        "Content-Type" : "application/json",
        "Referer" : "https://link-mutation.linkvertise.com/"
    }
    print("---------------------------this is a header", headers)
    payload = {
        "operationName" : "createLink",
        "variables" : {
            "input" : {
                "seo_faq_ids":[],
                "available_ads": "ALL",
                "target_type" : "URL",
                "target" : f"{generate_rentry(main_url)}",
                "btn_prefix" : "zu",
                "btn_text" : str(random.randint(10000, 9999999)),
                "seo_active" : False,
                "title" : None,
                "description" : None,
                "video_url" : None,
                "images" : None,
                "require_addon" : True,
                "require_web" : True,
                "require_installer" : True,
                "require_og_ads" : True,
                "require_custom_ad_step" : True
            }
        },
        "query" : "mutation createLink($input: LinkInput!) {\n  createLink(input: $input) {\n    id\n    href\n    user_id\n    __typename\n  }\n}\n"
    }

    print("Sending request to Linkvertise")
    print("-----------------this is a data--------",json.dumps(payload))
    try:
        response = requests.post(url=BASE_URL, headers=headers, data=json.dumps(payload), allow_redirects=True, cookies=cookies)
        print("this is a response----------------", response.json())
        # if response.status_code == 200:
        response.raise_for_status()
        res = response.json()
        return res['data']['createLink']['href']
    except requests.exceptions.HTTPError as http_err :
            # print(f"Request failed with status code: {response.status_code}")
            # print("Response content:")
            # print(response.content)
            print(f"-----------------------------------HTTP error occured:{http_err}")
    except Exception as err:
            print(f"---------------------------Other error occured: {err}")
    return None


def generate_rentry(text):
    session = requests.session()
    response = session.get("https://rentry.co", headers=_headers)
    csrf_token = response.headers.get('Set-Cookie').split(';')[0].split('=')[1]

    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'url': '',
        'edit_code': '',
        'text': text
    }

    return session.post('https://rentry.co/api/new', payload, headers=_headers).json()["url"]