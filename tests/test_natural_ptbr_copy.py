from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "public" / "index.html"


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"style", "script", "svg"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag in {"style", "script", "svg"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data):
        if not self.hidden_depth and data.strip():
            self.parts.append(data.strip())


def visible_text(html):
    parser = VisibleTextParser()
    parser.feed(html)
    return " ".join(parser.parts)


def test_copy_reads_as_native_brazilian_portuguese():
    html = INDEX.read_text(encoding="utf-8")
    text = visible_text(html)

    required = (
        "Quando a saudade bater, você vai saber o que fazer antes de procurar o ex.",
        "O celular está ali. A conversa antiga também.",
        "Na próxima vez que a vontade apertar, abra o kit primeiro.",
        "Quatro relatos em vídeo para você conhecer o trabalho de Sirlene.",
    )
    banned = (
        "reúne aplicações curtas",
        "intervalo entre o gatilho e a reação",
        "aplicação guiada de percepção e ação",
        "Menos espaço para a reação automática. Mais espaço para você.",
        "Procure a situação de partida",
        "corresponde ao que você está vivendo hoje",
        "O próximo gatilho não precisa decidir o seu próximo movimento.",
    )

    for phrase in required:
        assert phrase in text
    for phrase in banned:
        assert phrase not in text

    assert "R$ 67" in text
    assert "https://pay.hotmart.com/O106928609T" in html
