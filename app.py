from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return "請提供有效的 YouTube 網址", 400

    # 💡 升級為新版 Cobalt v10 API 主網址
    cobalt_api_url = "https://api.cobalt.tools/"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # 💡 根據 v10 官方新規格調整的參數 (Payload)
    payload = {
        "url": video_url,
        "videoQuality": "720",    # 新版參數名改為 videoQuality
        "downloadMode": "video"    # 新版下載模式設定
    }

    try:
        # 向新版 API 發送請求
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
        res_data = response.json()
        
        # 💡 取得下載連結
        download_url = res_data.get("url")
        
        if download_url:
            # 順利解析成功，直接跳轉下載
            return redirect(download_url)
        else:
            # 如果還是失敗，把新版 API 回傳的錯誤原因印出來
            error_msg = res_data.get("text", "未知錯誤")
            return f"解析失敗，原因: {error_msg}", 500
            
    except Exception as e:
        return f"連線到新版解析伺服器失敗: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False)
