import time
import requests
from collections import Counter
from konlpy.tag import Okt

def calculate_rank_from_json(data, overall_counts):
    okt = Okt()

    if 'content' not in data:
        print("JSON 데이터에 content 필드가 없습니다.")
        return []

    text = data['content']
    morphemes = okt.pos(text)
    nouns = [word for word, pos in morphemes if pos == 'Noun']
    overall_counts.update(nouns)  # 전체 명사 카운트 업데이트

# # API 주소
# api_url = "http://49.50.175.242:9894/v1/api/post"

# # Authorization 토큰
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0dHR0IiwiaWF0IjoxNzEzNDM2NjYwLCJleHAiOjE3MTQwNDE0NjB9.8fw3Wjro09VJHFwWzBwioiLblMnXJCDvm8nyANMwHc8"  # 여기에 본인의 토큰을 넣어주세요.

# overall_counts = Counter()  # 전체 명사 카운트를 저장할 Counter 객체 생성

# try:
#     while True:
#         # API 요청에 대한 헤더 설정
#         headers = {
#             "Authorization": f"Bearer {token}"
#         }

#         # API에서 JSON 데이터 가져오기
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # 에러 체크

#         # API 응답 데이터 확인
#         json_data = response.json()
#         data_list = json_data.get('data', [])

#         if not data_list:
#             print("API 응답에서 데이터를 찾을 수 없습니다.")
#             time.sleep(3)  # 데이터가 없는 경우 잠시 대기 후 다시 요청
#             continue

#         # 전체 데이터를 순회하면서 명사 카운트 업데이트
#         for data in data_list:
#             calculate_rank_from_json(data, overall_counts)

#         # 가장 많이 나타난 명사 순으로 정렬하여 상위 명사 출력
#         top_words = overall_counts.most_common(10)
#         for i, (word, count) in enumerate(top_words, start=1):
#             print(f"Rank {i}: {word} ({count} occurrences)")

#         # 카운트 초기화
#         overall_counts.clear()

#         time.sleep(3)  # 3초 대기

# except Exception as e:
#     print("오류 발생:", e)
