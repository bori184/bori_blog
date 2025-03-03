import requests
import json
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UCHD1jo5RhijLfx5-0Ehe_cg"  # 앤팀 공식 유튜브 채널 아이디

# 1️⃣ 채널의 'Uploads' 플레이리스트 ID 가져오기
channel_url = f"https://www.googleapis.com/youtube/v3/channels?key={YOUTUBE_API_KEY}&id={CHANNEL_ID}&part=contentDetails"
channel_response = requests.get(channel_url).json()

if "items" in channel_response and len(channel_response["items"]) > 0:
    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2️⃣ 최신 15개 영상 가져오기
    playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?key={YOUTUBE_API_KEY}&playlistId={uploads_playlist_id}&part=snippet,contentDetails&maxResults=15"
    playlist_response = requests.get(playlist_url).json()

    latest_video_id = None
    latest_shorts_ids = []

    if "items" in playlist_response and len(playlist_response["items"]) > 0:
        for item in playlist_response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]

            print(f"📌 {title} (ID: {video_id})")  # API 응답 출력

            # 쇼츠 구분 방법: 제목에 '#Shorts' 포함 여부 OR 길이가 60초 이하인지 확인
            is_shorts = "#Shorts" in title or item["contentDetails"].get("duration", "").startswith("PT") and "M" not in item["contentDetails"]["duration"]

            if is_shorts:
                if len(latest_shorts_ids) < 4:
                    latest_shorts_ids.append(video_id)
            else:
                if latest_video_id is None:
                    latest_video_id = video_id

            if latest_video_id and len(latest_shorts_ids) == 4:
                break

        # ✅ 기존 JSON과 비교하지 않고 무조건 덮어쓰기
        new_data = {
            "latest_video_id": latest_video_id,
            "latest_shorts_ids": latest_shorts_ids
        }

        file_path = "youtube.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

        # ✅ Git이 변경 사항을 감지하도록 파일 수정 시간 변경
        os.utime(file_path, None)

        print("✅ 최신 일반 영상 1개 & 쇼츠 4개를 youtube.json에 저장 완료!")

    else:
        print("❌ 최신 영상을 찾을 수 없습니다.")
else:
    print("❌ 채널 정보를 찾을 수 없습니다. (채널 ID 확인 필요)")
