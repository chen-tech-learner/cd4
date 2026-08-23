import requests

# 3个上游订阅地址
source_urls = [
    "https://fastly.jsdelivr.net/gh/a736240087/tvbox@main/tvlive/tvlive.txt",
    "https://fastly.jsdelivr.net/gh/shangzhouwan/iptv@daily-build/IPTV.m3u",
    "https://fastly.jsdelivr.net/gh/yuanzl77/IPTV@latest/live.m3u"
]

# 存放已经见过的链接，用来去重
seen_url = set()
output_lines = ["#EXTM3U"]

for url in source_urls:
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text

        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            # #EXTINF 行 + 下一行播放链接
            if line.startswith("#EXTINF") and (i+1) < len(lines):
                next_line = lines[i+1].strip()
                if next_line.startswith("http"):
                    if next_line not in seen_url:
                        seen_url.add(next_line)
                        output_lines.append(line)
                        output_lines.append(next_line)
                i += 2
            # txt格式：频道名,http链接
            elif "," in line and line.startswith(("CCTV","卫视")):
                parts = line.split(",",1)
                if len(parts)==2 and parts[1].startswith("http"):
                    name,u = parts[0], parts[1]
                    if u not in seen_url:
                        seen_url.add(u)
                        output_lines.append(f'#EXTINF:-1 tvg-name="{name}",{name}')
                        output_lines.append(u)
                i +=1
            else:
                i +=1

    except Exception as e:
        print(f"获取失败 {url} ：{e}")

# 写出文件
with open("my_live.m3u","w",encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("生成完成 my_live.m3u，一共",len(seen_url),"条链接")
