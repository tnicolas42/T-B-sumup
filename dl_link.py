import sys

# https://drive.google.com/uc?id=OUR_FILE_ID&export=download

#link = "https://drive.google.com/file/d/1vl5BmiWZfyN8D3SInnC7sit0PNH6nDlh/view?usp=sharing"
if len(sys.argv) == 1:
    print("Usage:")
    print("\tpython dl_link.py <google_link>")
    print("\tpython dl_link.py https://drive.google.com/file/d/1ee8kd-MxYmcTy1h_vyk_rluXFE3bLVhg/view")
    exit(1)
link = sys.argv[1]

print("https://drive.google.com/uc?id=" + link.split("/")[5] + "&export=download")
