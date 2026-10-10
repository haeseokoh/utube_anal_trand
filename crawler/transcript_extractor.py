import re
from typing import Optional, List, Dict
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

def extract_transcript(video_id: str) -> Optional[str]:
    """
    유튜브 비디오 ID로부터 한국어 자막/스크립트 추출
    1순위: 수동 한국어 자막 ('ko')
    2순위: 자동 생성 한국어 자막 ('ko')
    3순위: 영어 자막 ('en')
    """
    if not YouTubeTranscriptApi:
        return None
        
    try:
        # 지원 언어 우선순위로 자막 가져오기
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        transcript = None
        try:
            # 1. 한국어 수동/자동 자막 찾기
            transcript = transcript_list.find_transcript(['ko', 'ko-KR', 'ko-KP'])
        except Exception:
            try:
                # 2. 번역 가능 시 한국어로 번역 시도
                for t in transcript_list:
                    if t.is_translatable:
                        transcript = t.translate('ko')
                        break
            except Exception:
                pass
                
        if not transcript:
            # 3. 아무 사용 가능한 자막 찾기
            for t in transcript_list:
                transcript = t
                break
                
        if transcript:
            data = transcript.fetch()
            # 텍스트 추출 및 정제
            lines = [item.get("text", "") for item in data]
            full_text = " ".join(lines)
            return clean_transcript_text(full_text)
            
    except Exception as e:
        # 자막이 비활성화되었거나 추출 불가인 경우
        print(f"[Transcript] Could not extract transcript for {video_id}: {e}")
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
