import requests
import json
import os

# 환경 변수에서 Bearer Token 가져오기
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# 트위터 계정의 사용자명 (예: BTS_twt)
TWITTER_USERNAME = "BTS_twt"

# 트위터 API URL
API_URL = f"https://api.twitter.com/2/users/by/username/{TWITTER_USERNAME}"

# 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2UserLookupPython"
}

# 유저 정보 가져오기 (user_id 얻기 위함)
response = requests.get(API_URL, headers=headers)
if response.status_code == 200:
    user_data = response.json()
    user_id = user_data["data"]["id"]

    # 최신 트윗 가져오기
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5"
    tweet_response = requests.get(tweets_url, headers=headers)

    if tweet_response.status_code == 200:
        tweets = tweet_response.json()
        
        # JSON 파일 저장
        with open("tweets.json", "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=4)
        
        print("✅ 최신 트윗을 tweets.json에 저장 완료!")
    else:
        print("❌ 트윗 데이터를 가져오지 못했습니다:", tweet_response.text)
else:
    print("❌ 사용자 정보를 가져오지 못했습니다:", response.text)
