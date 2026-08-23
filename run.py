import requests
import time

source_urls = [
    "https://fastly.jsdelivr.net/gh/a736240087/tvbox@main/tvLive/tvLive.txt",
    "https://fastly.jsdelivr.net/gh/shangzhouwan/iptv@daily-build/IPTV.m3u",
    "https://fastly.jsdelivr.net/gh/yuanzL77/IPTV@latest/Live.m3u"
]

out_file = "my_live.m3u"
timeout_sec = 6
seen_url = set()
output_lines = ["#EXTM3U"]

def is_alive(url):
    try:
        headers = {"User‑Agent":"Mozilla/5.0"}
        r = requests.head(url, headers=headers, timeout=timeout_sec)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    return False

for src in source_urls:
    try:
        resp = requests.get(src, timeout=15)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        i = 0
        while i < len(lines):
            infoline = lines[i].strip()
            if infoline.startswith("#EXTINF") and i+1 < len(lines):
                playurl = lines[i+1].strip()
                if playurl.startswith("http"):
                    if playurl not in seen_url:
                        if is_alive(playurl):
                            seen_url.add(playurl)
                            output_lines.append(infoline)
                            output_lines.append(playurl)
                i += 2
            else:
                i += 1
    except Exception as e:
        print(f"读取源失败：{src} ，错误：{e}")

with open(out_file,"w",encoding="utf-8") as f:
    f.write("\n".join(output_lines))
print("处理完成")
