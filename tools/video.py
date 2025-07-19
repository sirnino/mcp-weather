from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def youtube_transcript(video_id: str) -> str:
    """
    Fetches the transcript of a YouTube video.

    Args:
        video_id (str): The ID of the YouTube video (e.g., for
                        "https://www.youtube.com/watch?v=abc123",
                        video_id should be "abc123").

    Returns:
        str: The full transcript text

    Usage Example:
        get_yt_transcript("gK8N9myv40Q")
    """
    preferred_languages = ['it', 'en', 'es', 'de']
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id, languages=preferred_languages)
    return " ".join([snippet.text for snippet in fetched_transcript])
