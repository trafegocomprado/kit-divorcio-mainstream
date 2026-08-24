from pathlib import Path


VIDEO_IDS = (
    "NjGfd9zKDf4",
    "KLxQ5Dr6W8s",
    "XrZHAOsWbcs",
    "__rkMASEkDc",
)


def report_generator() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "reports" / "generate_report.mjs"
        if candidate.exists():
            return candidate
    raise AssertionError("generate_report.mjs not found in the kit-divorcio output tree")


def test_m1_m2_m3_recognizes_existing_video_proof():
    source = report_generator().read_text(encoding="utf-8")

    expected_copy = (
        "4 depoimentos em vídeo",
        "prova existente, pouco contextualizada",
        "quatro cards de vídeo",
        "a prova existe; ainda precisa de contexto textual autorizado",
    )
    for phrase in expected_copy:
        assert phrase in source

    assert "a prova ainda precisa ser real" not in source.casefold()
    for video_id in VIDEO_IDS:
        assert video_id in source

