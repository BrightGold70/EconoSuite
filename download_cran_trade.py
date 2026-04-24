import os
import urllib.request
import re

new_packages = [
    "comtradr", "tradestatistics", "gravity", 
    "pwt10", "leontief"
]

output_dir = r"d:\Coding\EconoSuite\data\statistics"
os.makedirs(output_dir, exist_ok=True)

for pkg in new_packages:
    print(f"Processing {pkg}...")
    
    pdf_url = f"https://cran.r-project.org/web/packages/{pkg}/{pkg}.pdf"
    pdf_path = os.path.join(output_dir, f"{pkg}_manual.pdf")
    try:
        urllib.request.urlretrieve(pdf_url, pdf_path)
        print(f"  [OK] Downloaded manual: {pkg}_manual.pdf")
    except Exception as e:
        print(f"  [FAIL] Failed to download manual for {pkg}: {e}")

    pkg_url = f"https://cran.r-project.org/package={pkg}"
    try:
        req = urllib.request.urlopen(pkg_url)
        html = req.read().decode('utf-8')
        
        match = re.search(r'href="([^"]*src/contrib/[^"]+\.tar\.gz)"', html)
        if match:
            filename = match.group(1).split('/')[-1]
            src_url = f"https://cran.r-project.org/src/contrib/{filename}"
            
            src_path = os.path.join(output_dir, filename)
            urllib.request.urlretrieve(src_url, src_path)
            print(f"  [OK] Downloaded package source: {filename}")
        else:
            print(f"  [FAIL] Could not find source tarball link for {pkg}")
            
    except Exception as e:
        print(f"  [FAIL] Failed to process package page for {pkg}: {e}")
