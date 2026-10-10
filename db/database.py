import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "youtube_trends.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """데이터베이스 테이블 및 인덱스 초기화"""
    os.makedirs(DB_DIR, exist_ok=True)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. 유튜브 영상 메타데이터 및 분석 결과 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE NOT NULL,      -- 유튜브 고유 ID (예: dQw4w9WgXcQ)
                title TEXT NOT NULL,                -- 영상 제목
                channel_title TEXT NOT NULL,        -- 채널명 (예: 삼프로TV, 슈카월드 등)
                channel_id TEXT,                    -- 채널 ID
                analyst_name TEXT,                  -- 주요 분석가/패널명 (예: 오건영, 염승환, 김일구 등)
                category TEXT NOT NULL,             -- 매크로/금리, 국내주식, 미국주식, 부동산, 환율/원자재 등
                published_at TEXT NOT NULL,         -- 발행 일자 (YYYY-MM-DD 또는 ISO)
                video_url TEXT NOT NULL,            -- 유튜브 재생 URL
                thumbnail_url TEXT,                 -- 썸네일 이미지 URL
                view_count INTEGER DEFAULT 0,       -- 조회수
                duration_sec INTEGER DEFAULT 0,     -- 영상 길이(초)
                summary_text TEXT,                  -- 3줄 요약 또는 핵심 주장
                transcript_text TEXT,               -- 자막/스크립트 전체 텍스트
                sentiment_label TEXT,               -- 스탠스/성향 (bullish, neutral, bearish, caution)
                sentiment_score REAL DEFAULT 0.0,   -- 성향 점수 (-1.0 ~ 1.0)
                processed INTEGER DEFAULT 0,        -- 0: 미처리, 1: 처리완료, -1: 오류
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. 영상별 추출 키워드 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS video_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                keyword TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                weight REAL DEFAULT 1.0,
                FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE
            )
        """)
        
        # 3. 분석가별/주제별 핵심 의견 및 스탠스 타임라인 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyst_opinions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                analyst_name TEXT NOT NULL,
                topic TEXT NOT NULL,                -- 금리/통화정책, AI/반도체, 환율/외환, 부동산, 증시전망 등
                stance TEXT NOT NULL,               -- Bullish(낙관), Neutral(중립), Bearish(비관), Caution(경계)
                core_argument TEXT NOT NULL,        -- 핵심 주장
                key_quote TEXT,                     -- 인상적인 발언/근거
                period_label TEXT NOT NULL,         -- 예: 2024-Q1, 2024-Q2, 2024-09 등
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE
            )
        """)
        
        # 4. 영상별 AI 상세 요약 테이블 (Ollama 캐시)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS video_ai_summaries (
                video_id TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                summary_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE
            )
        """)
        
        # 5. 대시보드 트렌드 집계 캐시 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trend_cache (
                cache_key TEXT PRIMARY KEY,
                data_json TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 인덱스 생성
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_videos_pub_date ON videos(published_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_videos_category ON videos(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_videos_analyst ON videos(analyst_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_videos_sentiment ON videos(sentiment_label)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_v_keywords_kw ON video_keywords(keyword)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_v_keywords_vid ON video_keywords(video_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_opinions_analyst ON analyst_opinions(analyst_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_opinions_topic ON analyst_opinions(topic)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_opinions_period ON analyst_opinions(period_label)")

def save_video(video: Dict[str, Any]) -> bool:
    """단일 영상 메타데이터 저장 (중복 시 무시 또는 업데이트)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO videos (
                    video_id, title, channel_title, channel_id, analyst_name,
                    category, published_at, video_url, thumbnail_url,
                    view_count, duration_sec, summary_text, transcript_text,
                    sentiment_label, sentiment_score, processed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                video.get("video_id"),
                video.get("title"),
                video.get("channel_title"),
                video.get("channel_id", ""),
                video.get("analyst_name", ""),
                video.get("category", "거시경제/금리"),
                video.get("published_at"),
                video.get("video_url"),
                video.get("thumbnail_url", ""),
                video.get("view_count", 0),
                video.get("duration_sec", 0),
                video.get("summary_text", ""),
                video.get("transcript_text", ""),
                video.get("sentiment_label", "neutral"),
                video.get("sentiment_score", 0.0),
                video.get("processed", 0)
            ))
            return True
        except Exception as e:
            print(f"[DB] Error saving video {video.get('video_id')}: {e}")
            return False

def save_videos_bulk(videos: List[Dict[str, Any]]) -> int:
    """영상 다건 일괄 저장"""
    saved_count = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        for v in videos:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO videos (
                        video_id, title, channel_title, channel_id, analyst_name,
                        category, published_at, video_url, thumbnail_url,
                        view_count, duration_sec, summary_text, transcript_text,
                        sentiment_label, sentiment_score, processed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    v.get("video_id"),
                    v.get("title"),
                    v.get("channel_title"),
                    v.get("channel_id", ""),
                    v.get("analyst_name", ""),
                    v.get("category", "거시경제/금리"),
                    v.get("published_at"),
                    v.get("video_url"),
                    v.get("thumbnail_url", ""),
                    v.get("view_count", 0),
                    v.get("duration_sec", 0),
                    v.get("summary_text", ""),
                    v.get("transcript_text", ""),
                    v.get("sentiment_label", "neutral"),
                    v.get("sentiment_score", 0.0),
                    v.get("processed", 0)
                ))
                if cursor.rowcount > 0:
                    saved_count += 1
            except Exception as e:
                print(f"[DB] Bulk save error: {e}")
    return saved_count

def get_video_by_id(video_id: str) -> Optional[Dict[str, Any]]:
    """영상 상세 조회"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos WHERE video_id = ?", (video_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_videos(
    category: Optional[str] = None,
    analyst: Optional[str] = None,
    sentiment: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """필터링 조건에 따른 영상 목록 조회"""
    query = "SELECT * FROM videos WHERE 1=1"
    params = []
    
    if category and category != "all":
        query += " AND category = ?"
        params.append(category)
        
    if analyst and analyst != "all":
        query += " AND analyst_name = ?"
        params.append(analyst)
        
    if sentiment and sentiment != "all":
        query += " AND sentiment_label = ?"
        params.append(sentiment.lower())
        
    if start_date:
        query += " AND published_at >= ?"
        params.append(start_date)
        
    if end_date:
        query += " AND published_at <= ?"
        params.append(end_date)
        
    if search:
        query += " AND (title LIKE ? OR summary_text LIKE ? OR analyst_name LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern])
        
    query += " ORDER BY published_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

def get_videos_count() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM videos")
        return cursor.fetchone()[0]

def update_video_transcript(video_id: str, transcript_text: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE videos SET transcript_text = ? WHERE video_id = ?", (transcript_text, video_id))

def update_video_nlp_status(
    video_id: str,
    processed: int,
    summary_text: Optional[str] = None,
    sentiment_label: Optional[str] = None,
    sentiment_score: Optional[float] = None,
    category: Optional[str] = None,
    analyst_name: Optional[str] = None
):
    updates = ["processed = ?"]
    params = [processed]
    
    if summary_text is not None:
        updates.append("summary_text = ?")
        params.append(summary_text)
    if sentiment_label is not None:
        updates.append("sentiment_label = ?")
        params.append(sentiment_label)
    if sentiment_score is not None:
        updates.append("sentiment_score = ?")
        params.append(sentiment_score)
    if category is not None:
        updates.append("category = ?")
        params.append(category)
    if analyst_name is not None:
        updates.append("analyst_name = ?")
        params.append(analyst_name)
        
    params.append(video_id)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE videos SET {', '.join(updates)} WHERE video_id = ?", params)

def save_video_keywords(video_id: str, keywords: Dict[str, int]):
    """영상별 키워드 빈도 저장"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM video_keywords WHERE video_id = ?", (video_id,))
        for kw, cnt in keywords.items():
            cursor.execute("""
                INSERT INTO video_keywords (video_id, keyword, count)
                VALUES (?, ?, ?)
            """, (video_id, kw, cnt))

def save_analyst_opinion(
    video_id: str,
    analyst_name: str,
    topic: str,
    stance: str,
    core_argument: str,
    key_quote: str = "",
    period_label: str = ""
):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analyst_opinions (
                video_id, analyst_name, topic, stance, core_argument, key_quote, period_label
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (video_id, analyst_name, topic, stance, core_argument, key_quote, period_label))

def get_analyst_opinions(
    analyst: Optional[str] = None,
    topic: Optional[str] = None,
    period: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    query = """
        SELECT o.*, v.title, v.published_at, v.channel_title, v.video_url
        FROM analyst_opinions o
        JOIN videos v ON o.video_id = v.video_id
        WHERE 1=1
    """
    params = []
    if analyst and analyst != "all":
        query += " AND o.analyst_name = ?"
        params.append(analyst)
    if topic and topic != "all":
        query += " AND o.topic = ?"
        params.append(topic)
    if (not start_date and not end_date) and period and period not in ("all", "custom", "recent-3m"):
        if len(period) == 7 and period[4] == "-":
            query += " AND SUBSTR(v.published_at, 1, 7) = ?"
            params.append(period)
        else:
            query += " AND (o.period_label = ? OR SUBSTR(v.published_at, 1, 7) = ?)"
            params.extend([period, period])
    if start_date:
        query += " AND v.published_at >= ?"
        params.append(start_date)
    if end_date:
        query += " AND v.published_at <= ?"
        params.append(end_date)
    query += " ORDER BY v.published_at DESC"
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def save_video_ai_summary(video_id: str, model_name: str, summary_data: Dict[str, Any]):
    summary_json = json.dumps(summary_data, ensure_ascii=False)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO video_ai_summaries (video_id, model_name, summary_json, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (video_id, model_name, summary_json))

def get_video_ai_summary(video_id: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT model_name, summary_json, created_at FROM video_ai_summaries WHERE video_id = ?", (video_id,))
        row = cursor.fetchone()
        if row:
            try:
                data = json.loads(row["summary_json"])
                data["_model_name"] = row["model_name"]
                data["_created_at"] = row["created_at"]
                return data
            except Exception:
                return None
        return None

def get_trend_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data_json, updated_at FROM trend_cache WHERE cache_key = ?", (cache_key,))
        row = cursor.fetchone()
        if row:
            try:
                return json.loads(row["data_json"])
            except Exception:
                return None
    return None

def set_trend_cache(cache_key: str, data: Dict[str, Any]):
    data_json = json.dumps(data, ensure_ascii=False)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO trend_cache (cache_key, data_json, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (cache_key, data_json))

def clear_trend_cache():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trend_cache")

def get_filter_options() -> Dict[str, List[str]]:
    """UI 필터 드롭다운용 목록"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM videos WHERE category IS NOT NULL AND category != '' ORDER BY category")
        categories = [r[0] for r in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT analyst_name FROM videos WHERE analyst_name IS NOT NULL AND analyst_name != '' ORDER BY analyst_name")
        analysts = [r[0] for r in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT channel_title FROM videos WHERE channel_title IS NOT NULL AND channel_title != '' ORDER BY channel_title")
        channels = [r[0] for r in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT period_label FROM analyst_opinions WHERE period_label IS NOT NULL AND period_label != '' ORDER BY period_label DESC")
        periods = [r[0] for r in cursor.fetchall()]
        
        return {
            "categories": categories,
            "analysts": analysts,
            "channels": channels,
            "periods": periods
        }
