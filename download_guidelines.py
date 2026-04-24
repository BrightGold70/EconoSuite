import os
import urllib.request

output_dir = r"d:\Coding\EconoSuite\data\guideline"
os.makedirs(output_dir, exist_ok=True)

downloads = [
    ("Cochrane_Writing_Tips.pdf", "https://www.johnhcochrane.com/s/phd_paper_writing.pdf"),
    ("WTO_Advanced_Guide_to_Trade_Policy_Analysis.pdf", "https://www.wto.org/english/res_e/booksp_e/advancedwtounctad2016_e.pdf")
]

for filename, url in downloads:
    path = os.path.join(output_dir, filename)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
