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

    # 使用開源的 Cobalt API，它會自動處理 YouTube 的機器人驗證與 IP 封鎖問題
    cobalt_api_url = "https://api.cobalt.tools/api/json"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # 設定下載參數（限制 720p 確保速度與穩定度）
    payload = {
        "url": video_url,
        "vQuality": "720",
        "isAudioOnly": False
    }

    try:
        # 向 API 發送請求
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
        res_data = response.json()
        
        # 取得直接下載的影片連結
        download_url = res_data.get("url")
        
        if download_url:
            # 直接讓使用者的瀏覽器重新導向到這個高速下載連結
            return redirect(download_url)
        else:
            error_msg = res_data.get("text", "未知錯誤")
            return f"解析失敗，原因: {error_msg}", 500
            
    except Exception as e:
        return f"連線到解析伺服器失敗: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False)
