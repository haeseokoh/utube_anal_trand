import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from crawler.transcript_extractor import extract_transcript
from processor.nlp_engine import extract_keywords_and_sentiment
from db.database import clear_trend_cache

DB_PATH = "data/youtube_trends.db"

def check_and_fetch_transcript(item):
    vid, title, tr = item
    real_transcript = extract_transcript(vid)
    if real_transcript and len(real_transcript.strip()) > 30 and "글로벌 금융시장에서는" not in real_transcript:
        return vid, real_transcript, True
    return vid, "", False

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Check current fake boilerplate count
    cursor.execute("SELECT COUNT(*) FROM videos WHERE transcript_text LIKE '%글로벌 금융시장에서는%' OR transcript_text LIKE '%거시경제 환경을 살펴보면%'")
    fake_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM videos")
    total_count = cursor.fetchone()[0]
    print(f"Total videos: {total_count}, Fake boilerplate transcript count: {fake_count}", flush=True)
    
    # 2. Select all videos that have fake boilerplate
    cursor.execute("""
        SELECT video_id, title, transcript_text FROM videos 
        WHERE transcript_text LIKE '%글로벌 금융시장에서는%' 
           OR transcript_text LIKE '%거시경제 환경을 살펴보면%'
           OR transcript_text LIKE '%안녕하십니까,%시청자 여러분%'
    """)
    fake_rows = cursor.fetchall()
    print(f"Processing {len(fake_rows)} videos in parallel with ThreadPoolExecutor...", flush=True)
    
    results = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(check_and_fetch_transcript, row): row for row in fake_rows}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            
    updated_real = 0
    cleared_fake = 0
    for vid, text, is_real in results:
        if is_real:
            cursor.execute("UPDATE videos SET transcript_text = ? WHERE video_id = ?", (text, vid))
            updated_real += 1
        else:
            cursor.execute("UPDATE videos SET transcript_text = '' WHERE video_id = ?", (vid,))
            cleared_fake += 1
            
    # Also clear any stray rows that might still contain the phrase
    cursor.execute("UPDATE videos SET transcript_text = '' WHERE transcript_text LIKE '%글로벌 금융시장에서는%' OR transcript_text LIKE '%거시경제 환경을 살펴보면%'")
    conn.commit()
    print(f"Transcript update complete: REAL transcripts found={updated_real}, Cleared fake to empty={cleared_fake}", flush=True)
    
    # Verify fake count is 0
    cursor.execute("SELECT COUNT(*) FROM videos WHERE transcript_text LIKE '%글로벌 금융시장에서는%' OR transcript_text LIKE '%거시경제 환경을 살펴보면%'")
    remaining_fake = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM videos WHERE transcript_text != ''")
    real_count = cursor.fetchone()[0]
    print(f"Verification: Remaining fake count = {remaining_fake}, Videos with verified real transcripts = {real_count}", flush=True)
    
    # 3. Re-run Kiwi keyword extraction & sentiment on verified original text only
    print("Re-indexing Kiwi keywords and sentiments on verified original text only...", flush=True)
    cursor.execute("SELECT video_id, title, transcript_text FROM videos")
    all_videos = cursor.fetchall()
    
    for vid, title, tr in all_videos:
        # 검증된 원문(제목 + 실제 자막 원문이 있을 때만 자막)만 분석에 투입
        if tr and len(tr.strip()) > 30:
            analysis_text = f"{title} {tr}"
        else:
            analysis_text = title
            
        nlp_res = extract_keywords_and_sentiment(analysis_text, top_n=25)
        
        cursor.execute("DELETE FROM video_keywords WHERE video_id = ?", (vid,))
        for kw, cnt in nlp_res["keywords"].items():
            cursor.execute(
                "INSERT INTO video_keywords (video_id, keyword, count) VALUES (?, ?, ?)",
                (vid, kw, cnt)
            )
            
        cursor.execute(
            "UPDATE videos SET processed = 1, sentiment_label = ?, sentiment_score = ? WHERE video_id = ?",
            (nlp_res["sentiment_label"], nlp_res["sentiment_score"], vid)
        )
        
    conn.commit()
    conn.close()
    clear_trend_cache()
    print("Successfully completed Kiwi re-indexing and cleared trend cache!", flush=True)

if __name__ == "__main__":
    main()
