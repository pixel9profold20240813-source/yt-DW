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

    # 💡 關鍵修正：棄用官方封鎖的網址，改用社群公開、免驗證的 Cobalt 穩定鏡像端點
    cobalt_api_url = "https://cobalt.hyperborea.cloud/"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    payload = {
        "url": video_url,
        "videoQuality": "720",
        "downloadMode": "video"
    }

    try:
        response = requests.post(cobalt_api_url, json=payload, headers=headers)
        
        # 如果這個鏡像暫時有問題，自動切換到備用鏡像
        if response.status_code != 200:
            # 💡 備用鏡像二
            cobalt_api_url = "https://co.wuk.sh/"
            response = requests.post(cobalt_api_url, json=payload, headers=headers)
            
        if response.status_code != 200:
            return f"所有解析鏡像皆暫時拒絕回應 (代碼 {response.status_code})。原始回應：{response.text}", 500
            
        res_data = response.json()
        download_url = res_data.get("url")
        
        if download_url:
            # 解析成功，直接帶領瀏覽器前往下載
            return redirect(download_url)
        else:
            return f"鏡像解析成功但未成功產生網址，回應：{str(res_data)}", 500
            
    except Exception as e:
        return f"連線到解析鏡像失敗: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False)
