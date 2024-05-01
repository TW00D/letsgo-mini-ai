import os
from functools import wraps
import json
from flask import Flask, Response
from flask_restx import Api, Resource
from real_time_ranking import calculate_rank_from_json
import time
import requests
from collections import Counter
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app,resources={r'*':{'origins':'http://localhost:8082'}})

load_dotenv()

api_url = os.getenv('LETSGO_API')
token = os.getenv('TOKEN')

def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function


class TrendRank(Resource):
    # @api.route('/hello')
    @as_json
    def get(self):
        overall_counts = Counter()  
        top_words_list = []  

        try:
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  

            json_data = response.json()
            data_list = json_data.get('data', [])

            if not data_list:
                print("API 응답에서 데이터를 찾을 수 없습니다.")
                time.sleep(3)  
                
            for data in data_list:
                calculate_rank_from_json(data, overall_counts)

            top_words = overall_counts.most_common(10)
            top_words_list = [{"word": word, "count": count} for word, count in top_words]
            

        except Exception as e:
            print("오류 발생:", e)
            return {"error": str(e)}, 500

        return {"top_words": top_words_list}

api.add_resource(TrendRank, '/v1/api/rank')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)
