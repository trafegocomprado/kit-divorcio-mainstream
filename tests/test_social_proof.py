from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
INDEX = PUBLIC / "index.html"

VIDEO_IDS = (
    "NjGfd9zKDf4",
    "KLxQ5Dr6W8s",
    "XrZHAOsWbcs",
    "__rkMASEkDc",
)


class InitialMarkupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.iframes = []
        self.video_triggers = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "iframe":
            self.iframes.append(attributes)
        if tag == "button" and "video-proof__trigger" in attributes.get("class", ""):
            self.video_triggers.append(attributes)


def test_youtube_social_proof_is_complete_and_lazy_loaded():
    html = INDEX.read_text(encoding="utf-8")
    parser = InitialMarkupParser()
    parser.feed(html)

    assert len(parser.video_triggers) == 4
    assert not parser.iframes, "YouTube iframes must only be created after interaction"
    assert "youtube-nocookie.com/embed/" in html
    assert "[VALIDAÇÃO PENDENTE] Depoimento real" not in html

    for position, video_id in enumerate(VIDEO_IDS, start=1):
        assert html.count(video_id) >= 2
        assert any(item.get("data-youtube-id") == video_id for item in parser.video_triggers)
        assert f"https://www.youtube.com/watch?v={video_id}" in html
        assert (PUBLIC / "assets" / "proof" / f"depoimento-{position}.webp").exists()

