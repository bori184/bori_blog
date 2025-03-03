import requests
import json
import os
import time

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UCHD1jo5RhijLfx5-0Ehe_cg"  # 앤팀 공식 유튜브 채널 ID

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
            duration = item.get("contentDetails", {}).get("duration", "")

            print(f"📌 {title} (ID: {video_id}) | Duration: {duration}")  # API 응답 출력

            # 🛠️ 쇼츠 판별 방법 수정 (영상 길이 60초 이하 OR 제목에 #Shorts 포함)
            is_shorts = ("#Shorts" in title) or ("PT" in duration and "M" not in duration and int(duration.replace("PT", "").replace("S", "")) <= 60)

            if is_shorts:
                if len(latest_shorts_ids) < 4:
                    latest_shorts_ids.append(video_id)  # ✅ 쇼츠를 최대 4개까지 저장
            else:
                if latest_video_id is None:
                    latest_video_id = video_id  # ✅ 최신 일반 영상 1개 저장

            # 일반 영상 1개 & 쇼츠 4개가 모두 확보되면 종료
            if latest_video_id and len(latest_shorts_ids) == 4:
                break

        # ✅ 기존 JSON과 비교하지 않고 무조건 덮어쓰기
        new_data = {
            "latest_video_id": latest_video_id,
            "latest_shorts_ids": latest_shorts_ids
        }

        file_path = "youtube.json"

        # ✅ 파일이 정상적으로 저장되는지 확인하는 디버깅 코드 추가
        print("📂 새로운 youtube.json 내용:")
        print(json.dumps(new_data, indent=4, ensure_ascii=False))

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

        # ✅ Git이 변경 사항을 감지하도록 파일 수정 시간을 변경
        os.utime(file_path, None)

        print("✅ 최신 일반 영상 1개 & 쇼츠 4개를 youtube.json에 저장 완료!")

    else:
        print("❌ 최신 영상을 찾을 수 없습니다.")
else:
    print("❌ 채널 정보를 찾을 수 없습니다. (채널 ID 확인 필요)")
