import re
from typing import Optional, List, Dict
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

def extract_transcript(video_id: str) -> Optional[str]:
    """
    유튜브 비디오 ID로부터 실제 한국어 자막/스크립트 추출
    1순위: 수동 한국어 자막 ('ko')
    2순위: 자동 생성 한국어 자막 ('ko')
    3순위: 번역 자막 ('ko')
    4순위: 기타 자막
    """
    if not YouTubeTranscriptApi:
        return None
        
    try:
        # youtube_transcript_api v1.x (인스턴스 기반 .list) 및 레거시(.list_transcripts) 모두 호환
        transcript_list = None
        if hasattr(YouTubeTranscriptApi, 'list_transcripts'):
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            except Exception:
                pass
                
        if not transcript_list:
            try:
                ytt = YouTubeTranscriptApi()
                transcript_list = ytt.list(video_id)
            except Exception as e:
                pass
                
        if not transcript_list:
            return None
            
        transcript = None
        try:
            # 1. 한국어 수동/자동 자막 찾기
            transcript = transcript_list.find_transcript(['ko', 'ko-KR', 'ko-KP'])
        except Exception:
            try:
                # 2. 번역 가능 시 한국어로 번역 시도
                for t in transcript_list:
                    if getattr(t, 'is_translatable', False):
                        transcript = t.translate('ko')
                        break
            except Exception:
                pass
                
        if not transcript:
            # 3. 다른 언어 자막
            for t in transcript_list:
                transcript = t
                break
                
        if transcript:
            data = transcript.fetch()
            lines = []
            for item in data:
                # FetchedTranscriptSnippet 객체 또는 dict 지원
                txt = getattr(item, 'text', None)
                if txt is None and isinstance(item, dict):
                    txt = item.get("text", "")
                if txt:
                    lines.append(txt)
            full_text = " ".join(lines)
            cleaned = clean_transcript_text(full_text)
            if cleaned and len(cleaned) > 20:
                return cleaned
                
    except Exception as e:
        # 자막이 제공되지 않는 영상
        pass
        
    return None

def clean_transcript_text(text: str) -> str:
    """자막 텍스트 특수문자 및 불필요한 공백 정제"""
    if not text:
        return ""
    # [음악], [웃음], [박수] 등 괄호 태그 제거
    text = re.sub(r"\[.*?\]", " ", text)
    text = re.sub(r"\(.*?\)", " ", text)
    # 반복되는 불필요한 기호 제거
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
