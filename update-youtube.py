import requests
import json
import os

# 환경 변수에서 YouTube API 키 가져오기
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UCKgGOhz6xr0_FjDo2_i4oPA"  # 앤팀(＆TEAM) 공식 유튜브 채널 ID

# YouTube Data API 요청 URL
url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"

response = requests.get(url)
data = response.json()

print("Youtube API 응답:")
print(json.dumps(data, indent=4, ensure_ascii=False))

if response.status_code == 200:
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        video_id = data["items"][0]["id"]["videoId"]
        
        # JSON 파일 저장
        result = {"latest_video_id": video_id}
        with open("youtube.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        print("✅ 최신 유튜브 영상 ID를 youtube.json에 저장 완료!")
    else:
        print("❌ 최신 영상을 찾을 수 없습니다.")
else:
    print("❌ YouTube API 요청 실패:", response.text)
