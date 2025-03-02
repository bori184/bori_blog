import requests
import json
import os

# 환경 변수에서 Bearer Token 가져오기
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# 트위터 계정의 사용자명
TWITTER_USERNAME = "andTEAMofficial"

# 요청 헤더 설정
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2UserLookupPython"
}

# 1️⃣ 유저 ID 가져오기
user_url = f"https://api.twitter.com/2/users/by/username/{TWITTER_USERNAME}"
response = requests.get(user_url, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    user_id = user_data["data"]["id"]
    
    # 2️⃣ 유저 정보에서 고정 트윗 ID 가져오기
    user_info_url = f"https://api.twitter.com/2/users/{user_id}?tweet.fields=pinned_tweet_id"
    user_info_response = requests.get(user_info_url, headers=headers)
    
    pinned_tweet_id = None
    pinned_tweet = None

    if user_info_response.status_code == 200:
        user_info = user_info_response.json()
        pinned_tweet_id = user_info["data"].get("pinned_tweet_id")  # 고정 트윗 ID
        
        # 3️⃣ 고정된 트윗 가져오기
        if pinned_tweet_id:
            pinned_tweet_url = f"https://api.twitter.com/2/tweets/{pinned_tweet_id}"
            pinned_tweet_response = requests.get(pinned_tweet_url, headers=headers)

            if pinned_tweet_response.status_code == 200:
                pinned_tweet = pinned_tweet_response.json()

    # 4️⃣ 최신 트윗 가져오기
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5"
    tweets_response = requests.get(tweets_url, headers=headers)

    if tweets_response.status_code == 200:
        tweets = tweets_response.json()
        
        # JSON 데이터 구성
        result = {
            "pinned_tweet": pinned_tweet,  # 고정 트윗 데이터 추가
            "latest_tweets": tweets        # 최신 트윗 리스트 추가
        }

        # JSON 파일 저장
        with open("tweets.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print("✅ 최신 트윗 + 고정 트윗을 tweets.json에 저장 완료!")
    else:
        print("❌ 최신 트윗을 가져오지 못했습니다:", tweets_response.text)
else:
    print("❌ 사용자 정보를 가져오지 못했습니다:", response.text)
