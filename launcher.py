"""포인센티아 실행기

게임시작.bat 이 이 파일을 실행합니다.
1) 비어 있는 주소(포트)를 찾습니다. 예전 게임이 아직 켜져 있어도 겹치지 않게
   → 항상 '이 폴더'의 최신 게임이 열립니다.
2) 게임 엔진(Streamlit)을 켭니다.
3) 준비되면 크롬이나 엣지를 '음악 자동 재생 허용 · 번역 끔' 게임 창으로 엽니다.
"""
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "poinsettia.py")


def port_free(port):
    """그 포트를 다른 프로그램(예전 게임 등)이 쓰고 있지 않은지"""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.3):
            return False            # 누군가 이미 응답함 → 사용 중
    except OSError:
        pass
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def find_port(start=8501, end=8599):
    for p in range(start, end + 1):
        if port_free(p):
            return p
    s = socket.socket()
    s.bind(("0.0.0.0", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def find_browser():
    cands = []
    for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"),
                 os.environ.get("LOCALAPPDATA")):
        if base:
            cands.append(os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"))
    for base in (os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles")):
        if base:
            cands.append(os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe"))
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def open_when_ready(url, browser):
    for _ in range(240):                       # 최대 약 2분 기다림
        try:
            urllib.request.urlopen(url, timeout=2)
            break
        except Exception:
            time.sleep(0.5)
    if browser:
        profile = os.path.join(os.environ.get("LOCALAPPDATA", HERE), "PoinsettiaBrowser")
        subprocess.Popen([browser,
                          "--autoplay-policy=no-user-gesture-required",
                          "--user-data-dir=" + profile,
                          "--no-first-run", "--no-default-browser-check",
                          "--lang=ko", "--disable-features=Translate,TranslateUI",
                          "--app=" + url])
    else:
        webbrowser.open(url)


def main():
    if not os.path.exists(GAME):
        print("poinsettia.py 를 찾을 수 없어요. 압축을 푼 폴더 안에서 실행해 주세요.")
        return 1
    port = find_port()
    url = f"http://localhost:{port}"
    if port != 8501:
        print(f"[알림] 예전 게임이 아직 켜져 있는 것 같아요. 겹치지 않게 {port}번 주소로 새로 엽니다.")
        print("       예전 게임의 검은 창은 닫아도 괜찮아요.")
    print("게임 폴더:", HERE)
    print("주소:", url)
    browser = find_browser()
    threading.Thread(target=open_when_ready, args=(url, browser), daemon=True).start()
    cmd = [sys.executable, "-m", "streamlit", "run", GAME,
           "--server.port", str(port), "--server.headless", "true",
           "--browser.gatherUsageStats", "false"]
    return subprocess.call(cmd, cwd=HERE)


if __name__ == "__main__":
    sys.exit(main())
