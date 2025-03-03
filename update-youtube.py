import requests
import json
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UCHD1jo5RhijLfx5-0Ehe_cg"  # 앤팀 공식 유튜브 채널 ID

# 1️⃣ 채널의 'Uploads' 플레이리스트 ID 가져오기
channel_url = f"https://www.googleapis.com/youtube/v3/channels?key={YOUTUBE_API_KEY}&id={CHANNEL_ID}&part=contentDetails"
channel_response = requests.get(channel_url).json()

if "items" in channel_response and len(channel_response["items"]) > 0:
    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2️⃣ 최신 15개 영상 가져오기
    playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?key={YOUTUBE_API_KEY}&playlistId={uploads_playlist_id}&part=snippet&maxResults=15"
    playlist_response = requests.get(playlist_url).json()

    # 3️⃣ 영상 ID 리스트 생성
    video_ids = []
    if "items" in playlist_response:
        for item in playlist_response["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])

    # 4️⃣ 각 영상의 상세 정보(길이 포함) 가져오기
    details_url = f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}&id={','.join(video_ids)}&part=contentDetails"
    details_response = requests.get(details_url).json()

    latest_video_id = None
    latest_shorts_ids = []

    if "items" in details_response:
        for item in details_response["items"]:
            video_id = item["id"]
            duration = item["contentDetails"]["duration"]

            # 🎯 유튜브의 ISO 8601 Duration 형식 (예: PT5M10S, PT45S) → 초 단위로 변환
            minutes = 0
            seconds = 0
            if "M" in duration:
                minutes = int(duration.split("M")[0].replace("PT", ""))
            if "S" in duration:
                seconds = int(duration.split("S")[0].replace("PT", "").replace("M", ""))

            total_seconds = (minutes * 60) + seconds  # 총 길이(초)

            # 🎯 최신 일반 영상: 60초 이상 영상 중 가장 최신 것
            if total_seconds > 60 and latest_video_id is None:
                latest_video_id = video_id

            # 🎯 최신 쇼츠: 60초 이하 영상 중 4개 찾기
            if total_seconds <= 60 and len(latest_shorts_ids) < 4:
                latest_shorts_ids.append(video_id)

            # ✅ 최신 일반 영상 1개 + 최신 쇼츠 4개가 모두 찾아지면 중단
            if latest_video_id and len(latest_shorts_ids) == 4:
                break

        # 5️⃣ JSON 데이터 저장
        result = {
            "latest_video_id": latest_video_id,
            "latest_shorts_ids": latest_shorts_ids
        }

        with open("youtube.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print("✅ 최신 일반 영상 1개 & 쇼츠 4개를 youtube.json에 저장 완료!")
    else:
        print("❌ 최신 영상을 찾을 수 없습니다.")
else:
    print("❌ 채널 정보를 찾을 수 없습니다. (채널 ID 확인 필요)")
