import requests
from bs4 import BeautifulSoup

URL = "https://www.city.shiga-konan.lg.jp/soshiki/kensetsu_keizai/toshi_seisaku/2_3/36890.html"

def fetch_timetable():
    response = requests.get(URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all("table")
    html_rows = ""

    for table in tables:
        headers = table.find_all("th")
        rows = table.find_all("tr")

        if not headers:
            continue

        # ヘッダー行
        header_html = "".join([f"<th>{th.get_text(strip=True)}</th>" for th in headers])
        html_rows += "<table border='1' cellspacing='0' cellpadding='5' style='margin-bottom:30px;'>\n"
        html_rows += f"<thead><tr>{header_html}</tr></thead>\n"
        html_rows += "<tbody>\n"

        # データ行
        for row in rows[1:]:  # 最初の行はヘッダー
            cols = row.find_all("td")
            if not cols:
                continue
            row_html = "".join([f"<td>{td.get_text(strip=True)}</td>" for td in cols])
            html_rows += f"<tr>{row_html}</tr>\n"

        html_rows += "</tbody></table>\n"

    return html_rows


def generate_html():
    html_body = fetch_timetable()

    html_template = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>湖南市バス時刻表</title>
    <style>
        body {{
            font-family: sans-serif;
            padding: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f0f0f0;
        }}
    </style>
</head>
<body>
    <h1>湖南市バス時刻表（下田線・甲西駅ルート）</h1>
    <p>※元データ：<a href="{URL}" target="_blank">{URL}</a></p>
    {html_body}
</body>
</html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    print("✅ 'index.html' を生成しました！")


if __name__ == "__main__":
    generate_html()
