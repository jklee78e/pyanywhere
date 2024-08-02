import requests
import os

# 환경 변수에서 API 토큰과 사용자 이름 가져오기
PA_API_TOKEN = os.getenv("b4b96e7b98db6e498fcbe79fb9ca406986f16ccf")
PA_USERNAME = os.getenv("kiie")
GITHUB_REPO_URL = "https://github.com/jklee78e/pyanywhere"

def deploy():
    headers = {
        'Authorization': f'Token {PA_API_TOKEN}',
    }
    data = {
        'source': 'github',
        'branch': 'master',
        'url': GITHUB_REPO_URL,
    }
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{PA_USERNAME}/webapps/<webapp_id>/code/',
        headers=headers,
        json=data,
    )
    print(response.status_code, response.json())

if __name__ == "__main__":
    deploy()
