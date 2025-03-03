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

    # 2️⃣ 최신 트윗 가져오기
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5"  # 트윗 개수를 5개로 확장 가능
    tweets = make_request(tweets_url)

    if tweets:
        # ✅ 기존 JSON 비교 없이 항상 덮어쓰기
        result = {
            "latest_tweets": tweets
        }

        file_path = "tweets.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print("✅ 최신 트윗을 tweets.json에 저장 완료!")
