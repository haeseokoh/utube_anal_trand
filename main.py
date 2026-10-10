import argparse
import uvicorn
import os
import sys

# Windows 콘솔 인코딩 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="유튜브 경제 분석가 트렌드 인텔리전스 시스템")
    parser.add_argument("--crawl-only", action="store_true", help="수집 및 형태소 분석 파이프라인만 실행")
    parser.add_argument("--live-crawl", action="store_true", help="유튜브 RSS 실시간 신규 영상 수집 포함")
    parser.add_argument("--server-only", action="store_true", help="웹 대시보드 서버만 구동")
    parser.add_argument("--port", type=int, default=8001, help="웹 서버 포트 (기본값: 8001)")
    parser.add_argument("--no-browser", action="store_true", help="브라우저 자동 열기 비활성화")
    
    args = parser.parse_args()
    
    if args.crawl_only:
        print("🚀 유튜브 경제 데이터 수집 및 분석 파이프라인을 실행합니다...")
        run_pipeline(collect_youtube_live=args.live_crawl)
        return
        
    if not args.server_only:
        # 최초 실행 시 DB나 영상 데이터가 없으면 파이프라인 1회 초기 구동
        from db.database import DB_PATH, get_videos_count
        if not os.path.exists(DB_PATH) or get_videos_count() == 0:
            print("📦 최초 실행 감지: 시드 데이터 적재 및 형태소 분석을 실행합니다...")
            run_pipeline(collect_youtube_live=args.live_crawl)
            
    print(f"\n🌐 유튜브 경제 트렌드 대시보드 서버를 시작합니다: http://localhost:{args.port}")
    
    if not args.no_browser:
        import threading
        import webbrowser
        def _open_browser():
            import time
            time.sleep(1.2)
            try:
                webbrowser.open(f"http://localhost:{args.port}")
            except Exception:
                pass
        threading.Thread(target=_open_browser, daemon=True).start()

    uvicorn.run("app.main:app", host="0.0.0.0", port=args.port, reload=False)

if __name__ == "__main__":
    main()
