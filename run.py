import requests

source_urls = [
    "https://fastly.jsdelivr.net/gh/fanmingming/live/tv.m3u",
    "https://fastly.jsdelivr.net/gh/ssili126/tv/iptv4.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u"
]

out_file = "my_live.m3u"
seen_url = set()
output_lines = ["#EXTM3U"]

for src in source_urls:
    try:
        resp = requests.get(src, timeout=15)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        i = 0
        while i < len(lines):
            infoline = lines[i].strip()
            if infoline.startswith("#EXTINF") and i + 1 < len(lines):
                playurl = lines[i+1].strip()
                if playurl.startswith("http") and "[" not in playurl:
                    if playurl not in seen_url:
                        seen_url.add(playurl)
                        output_lines.append(infoline)
                        output_lines.append(playurl)
                i = i + 2
            else:
                i = i + 1
    except Exception as err:
        print(f"读取出错 {src} : {err}")

with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
print("执行结束，已过滤IPv6")
