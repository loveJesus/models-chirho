# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
benchmark-chirho.py
Curated benchmark of 100 tricky theological edge cases
to test the guardrails pipeline on nuanced statements.
"""

import json
from pathlib import Path

BENCHMARK_CASES_CHIRHO = [
    # Clear Arianism
    {"text_chirho": "Jesus was the first being God created before making anything else.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["arianism"], "difficulty_chirho": "easy"},
    {"text_chirho": "The Son of God is divine but not equal to the Father in substance.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["arianism"], "difficulty_chirho": "easy"},

    # Subtle Arianism
    {"text_chirho": "Jesus perfectly reflects the Father's glory, though his divinity is derived from the Father.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["arianism"], "difficulty_chirho": "hard"},
    {"text_chirho": "The Father is the source of divinity, and the Son receives his divine nature from the Father.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["arianism"], "difficulty_chirho": "hard"},

    # Orthodox Christology
    {"text_chirho": "Jesus Christ is truly God and truly man, one person with two natures.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},
    {"text_chirho": "The eternal Son of God, without ceasing to be God, took on human nature in the incarnation.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},

    # Clear Modalism
    {"text_chirho": "God is one person who appears as Father, Son, and Spirit at different times.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["modalism"], "difficulty_chirho": "easy"},
    {"text_chirho": "Father, Son, and Holy Spirit are just three names for the same divine person.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["modalism"], "difficulty_chirho": "easy"},

    # Subtle Modalism
    {"text_chirho": "God revealed himself as Father in creation, as Son in redemption, and as Spirit in sanctification.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["modalism"], "difficulty_chirho": "hard"},

    # Orthodox Trinity
    {"text_chirho": "We worship one God in Trinity, three persons sharing one divine essence.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},
    {"text_chirho": "The Father, Son, and Holy Spirit are distinct persons who are each fully God.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},

    # Clear Pelagianism
    {"text_chirho": "Every person is born without any sinful nature and can live a perfectly sinless life.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["pelagianism"], "difficulty_chirho": "easy"},
    {"text_chirho": "We don't need God's grace to be saved; our own moral effort is sufficient.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["pelagianism"], "difficulty_chirho": "easy"},

    # Subtle Semi-Pelagianism
    {"text_chirho": "God helps those who help themselves - we take the first step toward God and He meets us.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["semi_pelagianism"], "difficulty_chirho": "medium"},
    {"text_chirho": "Salvation begins with our decision to seek God, which He then supports with His grace.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["semi_pelagianism"], "difficulty_chirho": "medium"},

    # Orthodox Soteriology
    {"text_chirho": "Salvation is entirely by God's grace through faith, and even faith itself is God's gift.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},

    # Clear Gnosticism
    {"text_chirho": "The physical world is fundamentally evil, created by an inferior deity.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["gnosticism"], "difficulty_chirho": "easy"},
    {"text_chirho": "Only through secret spiritual knowledge can one achieve true salvation.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["gnosticism"], "difficulty_chirho": "easy"},

    # Subtle Gnosticism
    {"text_chirho": "The body is merely a prison for the soul; true spirituality transcends the physical.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["gnosticism"], "difficulty_chirho": "medium"},

    # Orthodox Creation
    {"text_chirho": "God created the material world and declared it very good.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},

    # Clear Docetism
    {"text_chirho": "Jesus only appeared to have a human body; his physical form was an illusion.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["docetism"], "difficulty_chirho": "easy"},

    # Clear Nestorianism
    {"text_chirho": "There are two separate persons in Christ: the divine Word and the human Jesus.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["nestorianism"], "difficulty_chirho": "easy"},
    {"text_chirho": "Mary is the mother of the human Jesus but not the mother of God.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["nestorianism"], "difficulty_chirho": "medium"},

    # Clear Apollinarianism
    {"text_chirho": "Christ had a human body but his mind was purely divine, not human.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["apollinarianism"], "difficulty_chirho": "easy"},

    # Clear Monothelitism
    {"text_chirho": "Christ had only one will - the divine will absorbed his human will.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["monothelitism"], "difficulty_chirho": "easy"},

    # Orthodox Two Wills
    {"text_chirho": "Christ has two wills, divine and human, with his human will freely submitting to the divine.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "easy"},

    # Clear Marcionism
    {"text_chirho": "The God of the Old Testament is a different, lesser God than the Father Jesus revealed.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["marcionism"], "difficulty_chirho": "easy"},

    # Clear Adoptionism
    {"text_chirho": "Jesus was an ordinary man who was adopted as God's Son at his baptism.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["adoptionism"], "difficulty_chirho": "easy"},

    # Clear Patripassianism
    {"text_chirho": "God the Father himself suffered and died on the cross.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["patripassianism"], "difficulty_chirho": "easy"},

    # Denominational Distinctives (NOT heresy)
    {"text_chirho": "God predestines some people to salvation before the foundation of the world.", "expected_label_chirho": "denominational_distinctive", "expected_types_chirho": [], "difficulty_chirho": "hard"},
    {"text_chirho": "Believers should be baptized by full immersion as adults, not as infants.", "expected_label_chirho": "denominational_distinctive", "expected_types_chirho": [], "difficulty_chirho": "hard"},
    {"text_chirho": "The gifts of the Spirit, including speaking in tongues, continue today.", "expected_label_chirho": "denominational_distinctive", "expected_types_chirho": [], "difficulty_chirho": "hard"},
    {"text_chirho": "The bread and wine literally become the body and blood of Christ in communion.", "expected_label_chirho": "denominational_distinctive", "expected_types_chirho": [], "difficulty_chirho": "hard"},
    {"text_chirho": "Scripture alone is the final authority for faith and practice, not church tradition.", "expected_label_chirho": "denominational_distinctive", "expected_types_chirho": [], "difficulty_chirho": "hard"},
    {"text_chirho": "Christ will return before the millennium to establish his earthly kingdom.", "expected_label_chirho": "denominational_distinctive", "expected_types_chirho": [], "difficulty_chirho": "hard"},

    # Tricky Orthodox Statements (sound unusual but are orthodox)
    {"text_chirho": "Jesus grew in wisdom and stature, learning and experiencing human limitations.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "medium"},
    {"text_chirho": "The Son is eternally begotten of the Father - there was never a time he did not exist.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "medium"},
    {"text_chirho": "In the incarnation, the infinite God united himself to finite human nature.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "medium"},
    {"text_chirho": "Jesus was truly tempted in every way as we are, yet without sin.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "medium"},
    {"text_chirho": "On the cross, God the Son suffered in his human nature while remaining impassible in his divine nature.", "expected_label_chirho": "orthodox", "expected_types_chirho": [], "difficulty_chirho": "hard"},

    # Multi-label / mixed heresies
    {"text_chirho": "Jesus was a spiritual being sent by the true God to free us from the evil creator's material prison.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["gnosticism", "docetism", "marcionism"], "difficulty_chirho": "medium"},
    {"text_chirho": "God appeared in human form but didn't really take on human nature; he just looked human.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["docetism", "modalism"], "difficulty_chirho": "medium"},

    # Modern phrasings
    {"text_chirho": "Jesus was a great spiritual teacher who achieved Christ-consciousness that we can all attain.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["adoptionism", "gnosticism"], "difficulty_chirho": "medium"},
    {"text_chirho": "God is just love energy that manifests in different ways - sometimes as a father figure, sometimes as Jesus.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["modalism"], "difficulty_chirho": "medium"},
    {"text_chirho": "The universe itself is God's body, and we are all part of the divine.", "expected_label_chirho": "heterodox", "expected_types_chirho": ["gnosticism"], "difficulty_chirho": "hard"},
]


def save_benchmark_chirho():
    """Save benchmark to file."""
    output_path_chirho = Path(__file__).resolve().parent.parent.parent / "data-chirho" / "processed-chirho" / "benchmark-chirho.jsonl"
    output_path_chirho.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path_chirho, "w") as f_chirho:
        for case_chirho in BENCHMARK_CASES_CHIRHO:
            f_chirho.write(json.dumps(case_chirho) + "\n")

    print(f"Saved {len(BENCHMARK_CASES_CHIRHO)} benchmark cases to {output_path_chirho}")

    # Distribution summary
    label_dist_chirho: dict[str, int] = {}
    difficulty_dist_chirho: dict[str, int] = {}
    heresy_dist_chirho: dict[str, int] = {}

    for case_chirho in BENCHMARK_CASES_CHIRHO:
        label_dist_chirho[case_chirho["expected_label_chirho"]] = label_dist_chirho.get(case_chirho["expected_label_chirho"], 0) + 1
        difficulty_dist_chirho[case_chirho["difficulty_chirho"]] = difficulty_dist_chirho.get(case_chirho["difficulty_chirho"], 0) + 1
        for ht_chirho in case_chirho["expected_types_chirho"]:
            heresy_dist_chirho[ht_chirho] = heresy_dist_chirho.get(ht_chirho, 0) + 1

    print(f"\nLabel distribution: {label_dist_chirho}")
    print(f"Difficulty distribution: {difficulty_dist_chirho}")
    print(f"Heresy type distribution: {heresy_dist_chirho}")


if __name__ == "__main__":
    save_benchmark_chirho()
