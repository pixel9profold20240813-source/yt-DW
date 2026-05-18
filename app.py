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

    cobalt_api_url = "https://api.cobalt.tools/"
    
    # 💡 加強偽裝：加入真實瀏覽器的 Headers，避免被 Cobalt 認定是惡意機器人
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://cobalt.tools",
        "Referer": "https://cobalt.tools/"
    }
    
    payload = {
        "url": video_url,
        "videoQuality": "720",
        "downloadMode": "video"
    }

    try:
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
        
        # 💡 除錯核心：先檢查狀態碼，200 代表成功，其餘代表伺服器拒絕
        if response.status_code != 200:
            return f"Cobalt 伺服器拒絕請求 (錯誤代碼 {response.status_code})，可能目前流量過大，請稍後再試。原始回應：{response.text}", 500
            
        res_data = response.json()
        download_url = res_data.get("url")
        
        if download_url:
            return redirect(download_url)
        else:
            # 💡 深入剖析：如果成功回傳 JSON 卻沒有 url，直接把整個 JSON 印在網頁上給你看
            return f"解析失敗，API 回傳的完整內容為: {str(res_data)}", 500
            
    except Exception as e:
        return f"連線到解析伺服器失敗: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False)
