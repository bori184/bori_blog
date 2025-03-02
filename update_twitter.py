import requests
import json
import os
import time

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_USERNAME = "andTEAMofficial"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2UserLookupPython"
}

def make_request(url, max_retries=3):
    """429 오류 발생 시 재시도하는 함수"""
    retries = 0
    while retries < max_retries:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 429:
            print("⚠️ Rate Limit 초과! 60초 대기 후 재시도...")
            time.sleep(60)  # 1분 대기 후 재시도
            retries += 1
        
        else:
            print(f"❌ 오류 발생 ({response.status_code}): {response.text}")
            return None

    print("❌ 최대 재시도 횟수 초과, 요청 실패")
    return None

# 1️⃣ 유저 ID 가져오기
user_url = f"https://api.twitter.com/2/users/by/username/{TWITTER_USERNAME}"
user_data = make_request(user_url)

if user_data:
    user_id = user_data["data"]["id"]

    # 2️⃣ 유저 정보에서 고정 트윗 ID 가져오기
    user_info_url = f"https://api.twitter.com/2/users/{user_id}?tweet.fields=pinned_tweet_id"
    user_info = make_request(user_info_url)
    
    pinned_tweet_id = None
    pinned_tweet = None

    if user_info:
        pinned_tweet_id = user_info["data"].get("pinned_tweet_id")
        
        # 3️⃣ 고정된 트윗 가져오기
        if pinned_tweet_id:
            pinned_tweet_url = f"https://api.twitter.com/2/tweets/{pinned_tweet_id}"
            pinned_tweet = make_request(pinned_tweet_url)

    # 4️⃣ 최신 트윗 가져오기
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=2"
    tweets = make_request(tweets_url)

    if tweets:
        # JSON 데이터 구성
        result = {
            "pinned_tweet": pinned_tweet,
            "latest_tweets": tweets
        }

        # JSON 파일 저장
        with open("tweets.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print("✅ 최신 트윗 + 고정 트윗을 tweets.json에 저장 완료!")
