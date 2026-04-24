import os
import urllib.request
import re

new_packages = [
    "OECD", "imfr", "eurostat", "fredr", "rdbnomics", "rvest", "httr2"
]

output_dir = r"d:\Coding\EconoSuite\data\statistics"
os.makedirs(output_dir, exist_ok=True)

for pkg in new_packages:
    print(f"Processing {pkg}...")
    
    pdf_url = f"https://cran.r-project.org/web/packages/{pkg}/{pkg}.pdf"
    pdf_path = os.path.join(output_dir, f"{pkg}_manual.pdf")
    try:
        req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(pdf_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"  [OK] Downloaded manual: {pkg}_manual.pdf")
    except Exception as e:
        print(f"  [FAIL] Failed to download manual for {pkg}: {e}")

    pkg_url = f"https://cran.r-project.org/package={pkg}"
    try:
        req = urllib.request.Request(pkg_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        match = re.search(r'href="([^"]*src/contrib/[^"]+\.tar\.gz)"', html)
        if match:
            filename = match.group(1).split('/')[-1]
            src_url = f"https://cran.r-project.org/src/contrib/{filename}"
            
            src_path = os.path.join(output_dir, filename)
            req_src = urllib.request.Request(src_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_src) as response, open(src_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  [OK] Downloaded package source: {filename}")
        else:
            print(f"  [FAIL] Could not find source tarball link for {pkg}")
            
    except Exception as e:
        print(f"  [FAIL] Failed to process package page for {pkg}: {e}")
