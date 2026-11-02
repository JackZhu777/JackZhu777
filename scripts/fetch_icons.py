"""Download Devicon SVGs and their license for locally hosted profile icons."""
from pathlib import Path
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "assets" / "icons"
ROOT.mkdir(parents=True, exist_ok=True)
BASE = "https://raw.githubusercontent.com/devicons/devicon/master/"
ICONS = ["python", "java", "javascript", "html5", "css3", "spring",
         "vuejs", "react", "mysql", "pytorch", "git", "figma"]


def download(path):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(BASE + path, timeout=25) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(1)


for name in ICONS:
    data = download(f"icons/{name}/{name}-original.svg")
    assert ET.fromstring(data).tag.endswith("svg")
    (ROOT / f"{name}.svg").write_bytes(data)
    print("Saved", name)
(ROOT / "LICENSE").write_bytes(download("LICENSE"))
