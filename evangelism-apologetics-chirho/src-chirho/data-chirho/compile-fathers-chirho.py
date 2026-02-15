# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
compile-fathers-chirho.py
Compiles early church fathers' apologetic texts into structured JSONL format.

IMPORTANT PRINCIPLE: These writings are SECONDARY to Scripture. The Bible is the
final authority (2 Timothy 3:16-17). Church fathers are useful for showing what
the earliest Christians believed and how they defended the faith, but Scripture
alone is the ultimate standard of truth (sola Scriptura).

NOTE: Origen is deliberately excluded due to heterodox teachings including
the pre-existence of souls and universal salvation (apokatastasis).

Fathers included:
  1. Justin Martyr (100-165 AD)
  2. Irenaeus (130-202 AD)
  3. Tertullian (155-220 AD)
  4. Athanasius (296-373 AD)
  5. Augustine (354-430 AD)
  6. Chrysostom (347-407 AD)
  7. Polycarp (69-155 AD)
  8. Clement of Rome (35-99 AD)
"""

import json
from pathlib import Path

OUTPUT_DIR_CHIRHO = (
    Path(__file__).resolve().parent.parent.parent
    / "data-chirho"
    / "raw-chirho"
    / "fathers-chirho"
)

OUTPUT_FILE_CHIRHO = OUTPUT_DIR_CHIRHO / "early-fathers-apologetics-chirho.jsonl"

# Every entry carries this weight designation — church fathers are secondary to Scripture
WEIGHT_CHIRHO = "secondary_to_scripture"
CATEGORY_CHIRHO = "early_church_apologetics"


def build_justin_martyr_chirho() -> list[dict]:
    """Justin Martyr (100-165 AD): First Apology, Second Apology, Dialogue with Trypho."""
    return [
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "First Apology",
            "argument_chirho": (
                "Christians should not be punished merely for bearing the name 'Christian.' "
                "Justin appeals to Emperor Antoninus Pius that justice demands examining the "
                "actual conduct and beliefs of Christians rather than condemning them on the "
                "basis of name alone. He argues that if Christians are found to be wrongdoers, "
                "punish them as wrongdoers — but if they live virtuously, the name itself is "
                "no crime. This is one of the earliest legal-philosophical defenses of religious liberty."
            ),
            "context_chirho": (
                "Written circa 155 AD, addressed to Emperor Antoninus Pius and his sons. "
                "Christians were being executed simply for confessing the name of Christ, "
                "without any investigation of actual crimes. Justin, a trained philosopher, "
                "used the language of Roman law and Greek philosophy to make his case."
            ),
            "relevance_chirho": (
                "Demonstrates that the earliest Christians engaged intellectually with secular "
                "authorities rather than retreating from public discourse. Establishes the "
                "principle that faith should be evaluated on its merits and fruits, not "
                "dismissed by label — a principle still vital when Christianity is caricatured "
                "in modern culture."
            ),
            "scripture_chirho": ["1 Peter 3:15-16", "Matthew 5:11-12", "Acts 26:1-29"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "First Apology",
            "argument_chirho": (
                "Christ is the divine Logos (Reason/Word) through whom all truth comes. "
                "Justin taught that the 'seeds of the Logos' (logos spermatikos) were scattered "
                "throughout creation, so that whatever truth pagan philosophers discovered — "
                "Socrates, Plato, the Stoics — they discovered through the same Logos who "
                "became incarnate in Jesus Christ. Christ is not one teacher among many; He is "
                "the source of all truth that any teacher has ever found."
            ),
            "context_chirho": (
                "Justin was a trained philosopher who had studied Stoicism, Aristotelianism, "
                "Pythagoreanism, and Platonism before converting to Christianity. His Logos "
                "theology built a bridge between Greek philosophical concepts and the Gospel "
                "of John's declaration that 'the Word became flesh.' He wrote for an educated "
                "Roman audience fluent in philosophical categories."
            ),
            "relevance_chirho": (
                "Provides a framework for engaging with truth found in secular philosophy, "
                "science, and culture without compromising the uniqueness of Christ. All truth "
                "is God's truth — a principle that empowers Christians to engage confidently "
                "in academic and intellectual settings, claiming every true insight as belonging "
                "to Christ (Colossians 2:3)."
            ),
            "scripture_chirho": ["John 1:1-14", "John 14:6", "Colossians 1:15-17", "Colossians 2:3"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "Dialogue with Trypho",
            "argument_chirho": (
                "Jesus Christ is the fulfillment of Hebrew Messianic prophecy. In his lengthy "
                "dialogue with the Jewish rabbi Trypho, Justin systematically demonstrates how "
                "Jesus fulfilled prophecies from Isaiah, the Psalms, Daniel, Micah, and Zechariah. "
                "He argues that the two comings of the Messiah — first in humility and suffering "
                "(Isaiah 53), then in glory and judgment (Daniel 7:13-14) — resolve the apparent "
                "contradiction that troubled Jewish readers expecting only a conquering king."
            ),
            "context_chirho": (
                "Written circa 160 AD, this records a dialogue (likely somewhat literary in form) "
                "between Justin and Trypho, a learned Jew, possibly after the Bar Kokhba revolt "
                "(132-135 AD). It is the earliest surviving extended Christian-Jewish dialogue and "
                "shows how the first Christians argued for Jesus' Messiahship from the Hebrew Scriptures."
            ),
            "relevance_chirho": (
                "Provides a model for respectful interfaith dialogue grounded in Scripture. The "
                "two-comings framework remains the strongest answer to Jewish objections about "
                "why Jesus did not fulfill the political expectations of the Messiah. Justin's "
                "method of arguing from shared Scripture is still the most effective approach "
                "in Jewish-Christian apologetics."
            ),
            "scripture_chirho": ["Isaiah 53:1-12", "Daniel 7:13-14", "Psalm 22:1-18", "Micah 5:2", "Zechariah 9:9"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "First Apology",
            "argument_chirho": (
                "The moral transformation of Christian converts proves the truth of the faith. "
                "Justin catalogs the dramatic changes in converts: former fornicators now live in "
                "chastity, former practitioners of magic have dedicated themselves to God, those "
                "who once valued wealth above all now share freely with the needy, and those who "
                "once hated people of other tribes now pray for their enemies. He challenges the "
                "emperor: examine our lives and see if this is the work of demons or of God."
            ),
            "context_chirho": (
                "Romans accused Christians of secret immorality (incest, cannibalism in the "
                "Eucharist, atheism for rejecting pagan gods). Justin turns the accusation on "
                "its head by pointing to the visible, verifiable moral transformation of converts "
                "from paganism — transformation that pagan philosophy had failed to achieve "
                "despite centuries of teaching."
            ),
            "relevance_chirho": (
                "The argument from changed lives remains one of the most powerful apologetic "
                "tools. When Christianity is accused of being harmful or regressive, pointing "
                "to verifiable transformation — addiction recovery, broken families restored, "
                "criminal rehabilitation — provides empirical evidence of the Gospel's power. "
                "This is the same argument Paul makes in 1 Corinthians 6:9-11: 'such were some "
                "of you, but you were washed.'"
            ),
            "scripture_chirho": ["1 Corinthians 6:9-11", "2 Corinthians 5:17", "Galatians 5:19-23", "Titus 3:3-7"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "Second Apology",
            "argument_chirho": (
                "The courage of Christians facing death proves their sincerity and the power of "
                "their faith. Justin writes that it was precisely watching Christians die fearlessly "
                "in the arena that first convinced him Christianity was true — because no one "
                "devoted to pleasure and sin would willingly embrace suffering and death. The "
                "cheerfulness of martyrs in the face of torture was inexplicable apart from "
                "genuine supernatural conviction."
            ),
            "context_chirho": (
                "Written shortly after Justin witnessed the unjust execution of Christians under "
                "the urban prefect Urbicus in Rome. Justin himself would later be martyred "
                "(hence his title 'Martyr'), fulfilling his own argument. His Second Apology "
                "is shorter and more urgent than the First, written in response to immediate "
                "persecution."
            ),
            "relevance_chirho": (
                "The witness of suffering Christians has been a powerful testimony throughout "
                "history — from the Roman arena to modern persecuted churches in North Korea, "
                "China, Iran, and Nigeria. When believers maintain faith, joy, and forgiveness "
                "under extreme pressure, it demonstrates something beyond human capacity and "
                "provokes the question: what do they have that I do not?"
            ),
            "scripture_chirho": ["Acts 7:55-60", "Philippians 1:21", "Romans 8:35-39", "Hebrews 11:35-38"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "First Apology, Chapters 61-67",
            "argument_chirho": (
                "Justin provides the earliest detailed description of Christian worship — baptism "
                "and the Eucharist — showing that Christian practice was orderly, moral, and "
                "centered on Christ, not the secret orgies and cannibalism that Romans accused. "
                "He describes the Sunday gathering: readings from the prophets and apostles, "
                "a sermon by the president, communal prayer, sharing of bread and wine, and "
                "collection for orphans and widows. This transparency was itself an apologetic act."
            ),
            "context_chirho": (
                "Romans spread wild rumors about Christian gatherings (which were closed to "
                "outsiders). By describing worship practices openly to the emperor, Justin "
                "dismantled conspiracy theories with transparency. His account matches the "
                "pattern of worship described in Acts 2:42 and 1 Corinthians 11-14."
            ),
            "relevance_chirho": (
                "Transparency about Christian practice has always been an effective apologetic "
                "against conspiracy theories and misrepresentation. Justin's descriptions show "
                "remarkable continuity with both the New Testament and many church traditions "
                "today, demonstrating that core Christian worship has ancient roots — it was not "
                "invented in the Middle Ages or by Constantine."
            ),
            "scripture_chirho": ["Acts 2:42", "1 Corinthians 11:23-26", "1 Timothy 2:1-2", "Hebrews 10:24-25"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Justin Martyr (100-165 AD)",
            "work_chirho": "Dialogue with Trypho",
            "argument_chirho": (
                "The worldwide spread of Christianity among all nations fulfills biblical prophecy "
                "and demonstrates divine power. Justin argues to Trypho that Isaiah's prophecy — "
                "that the servant of the Lord would be 'a light to the Gentiles' (Isaiah 49:6) — "
                "is being fulfilled before their eyes as people from every nation turn to the God "
                "of Israel through Christ. No mere human movement could achieve this."
            ),
            "context_chirho": (
                "By Justin's time (mid-2nd century), Christianity had spread from Palestine across "
                "the Roman Empire and beyond — to North Africa, Gaul, Mesopotamia, and India. "
                "This rapid expansion among diverse peoples and cultures, despite severe persecution, "
                "was itself an argument for supernatural origin."
            ),
            "relevance_chirho": (
                "The global spread of Christianity — now the world's largest religion with over "
                "2 billion adherents from every ethnic group, language, and nation — continues to "
                "fulfill this prophecy. The faith born in a tiny corner of the Roman Empire, "
                "without military force or political power, has reached every continent. This "
                "fulfilled prophecy is ongoing and observable."
            ),
            "scripture_chirho": ["Isaiah 49:6", "Matthew 28:19-20", "Acts 1:8", "Revelation 7:9"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_irenaeus_chirho() -> list[dict]:
    """Irenaeus (130-202 AD): Against Heresies."""
    return [
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book III",
            "argument_chirho": (
                "Apostolic succession and the public teaching tradition of the churches prove "
                "which teachings are authentic. Irenaeus argues that the true faith can be "
                "verified by tracing the line of bishops in every church back to the apostles "
                "who founded them. The public, open teaching of the churches — in contrast to "
                "the secret 'traditions' claimed by Gnostics — provides a verifiable chain of "
                "custody for Christian doctrine. He specifically traces the bishops of Rome "
                "back to Peter and Paul."
            ),
            "context_chirho": (
                "Written circa 180 AD against Gnostic teachers (especially Valentinus and Marcion) "
                "who claimed secret traditions from the apostles that contradicted the public "
                "teaching of the churches. Irenaeus, who as a youth had heard Polycarp (who knew "
                "the apostle John), represents a living link to the apostolic generation."
            ),
            "relevance_chirho": (
                "Establishes the principle that authentic Christian teaching is publicly verifiable, "
                "not hidden in esoteric 'secret knowledge.' This argument applies today against "
                "any group claiming special revelation that contradicts the apostolic witness "
                "preserved in Scripture. The chain of testimony from apostles to early church "
                "provides historical evidence for the reliability of the New Testament message."
            ),
            "scripture_chirho": ["2 Timothy 2:2", "1 Timothy 6:20", "Jude 1:3", "2 Thessalonians 2:15"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book I-II",
            "argument_chirho": (
                "Gnostic cosmologies are self-refuting absurdities when examined carefully. "
                "Irenaeus meticulously describes the Valentinian system of emanating aeons "
                "(Bythos, Nous, Aletheia, Logos, Zoe, etc.) and then demolishes it with logical "
                "analysis, showing internal contradictions: if the supreme God is perfect, why "
                "did the emanation process produce error? If matter is evil, how can a good God "
                "be its ultimate source? He famously ridicules the arbitrary complexity: why 30 "
                "aeons and not 31?"
            ),
            "context_chirho": (
                "Gnosticism was the greatest theological threat to 2nd-century Christianity, "
                "offering an alternative 'Christian' worldview that denied creation, the "
                "incarnation, and bodily resurrection. Irenaeus' method — first accurately "
                "describing opponents' views, then systematically refuting them — became the "
                "model for all subsequent Christian apologetics."
            ),
            "relevance_chirho": (
                "Irenaeus' method of careful description followed by logical refutation remains "
                "the gold standard for engaging false teachings. Modern parallels to Gnosticism "
                "abound — New Age spirituality, some forms of prosperity gospel, and any system "
                "that claims special 'hidden knowledge' accessible only to the initiated. His "
                "approach teaches us to understand what opponents actually believe before critiquing."
            ),
            "scripture_chirho": ["1 Timothy 6:20-21", "Colossians 2:8", "2 Corinthians 10:5", "1 John 4:1"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book III, Chapter 3",
            "argument_chirho": (
                "The unity of the Old and New Testaments: the God of creation is the God of "
                "redemption. Against Marcion and the Gnostics who separated the wrathful "
                "'Demiurge' of the Old Testament from the loving 'Father' of the New, Irenaeus "
                "insists that one and the same God created the world, gave the Law through Moses, "
                "spoke through the prophets, and sent His Son for salvation. The entire biblical "
                "narrative is one coherent story of one God's love for His creation."
            ),
            "context_chirho": (
                "Marcion (circa 144 AD) had created a truncated Bible, rejecting the entire Old "
                "Testament and editing Luke and Paul's letters to remove Jewish references. This "
                "was perhaps the most dangerous heresy of the era because it severed Christianity "
                "from its scriptural roots. Irenaeus demonstrates the essential unity of the "
                "biblical witness."
            ),
            "relevance_chirho": (
                "The Marcionite temptation — rejecting or minimizing the Old Testament — recurs "
                "in every generation. Modern forms include claiming that 'the God of the Old "
                "Testament is different from Jesus,' dismissing Old Testament ethics, or treating "
                "the Hebrew Scriptures as irrelevant. Irenaeus shows that without the Old "
                "Testament, the New Testament makes no sense — and vice versa."
            ),
            "scripture_chirho": ["Luke 24:27", "Matthew 5:17-18", "2 Timothy 3:16-17", "Hebrews 1:1-2"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book V",
            "argument_chirho": (
                "The recapitulation theory: Christ 'recapitulated' (summed up and reversed) the "
                "entire human story in Himself. Where Adam was disobedient, Christ was obedient. "
                "Where Eve was deceived, Mary believed. Where the tree in Eden brought death, the "
                "tree of the cross brings life. Christ passed through every stage of human life "
                "(infancy, childhood, youth, maturity) to sanctify and redeem each stage. This is "
                "not merely legal substitution but a cosmic reversal of the Fall."
            ),
            "context_chirho": (
                "Irenaeus developed this theology against Gnostics who denied the goodness of "
                "material creation and the reality of Christ's incarnation. If Christ did not "
                "truly take on human flesh, he could not truly redeem human flesh. Recapitulation "
                "affirms that salvation involves the whole person — body and soul — not escape "
                "from the material world."
            ),
            "relevance_chirho": (
                "This robust theology of incarnation answers both ancient Gnosticism and modern "
                "materialism. Against those who denigrate the body (some forms of spirituality), "
                "it affirms the body's value. Against pure materialism, it affirms the body's "
                "eternal destiny through resurrection. The recapitulation framework also provides "
                "a rich understanding of why the incarnation was necessary — not merely as a "
                "legal transaction but as a restoration of humanity from within."
            ),
            "scripture_chirho": ["Romans 5:12-21", "1 Corinthians 15:21-22", "1 Corinthians 15:45-49", "Ephesians 1:10"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book I, Chapter 10",
            "argument_chirho": (
                "The Rule of Faith: a concise summary of core Christian belief held consistently "
                "across all churches in all regions. Irenaeus presents this rule — belief in one "
                "God the Father Almighty, maker of heaven and earth; one Christ Jesus, the Son of "
                "God, incarnate for our salvation; and the Holy Spirit who spoke through the "
                "prophets — as the standard by which all teaching is to be measured. The universal "
                "agreement of geographically separated churches on these core truths testifies "
                "to their apostolic origin."
            ),
            "context_chirho": (
                "The Rule of Faith predates formal creeds (Nicaea 325 AD) and represents the "
                "earliest form of what would become the Apostles' Creed. Irenaeus notes that "
                "churches in Germany, Spain, Gaul, Egypt, Libya, and the East all confess the "
                "same core faith despite language and cultural barriers — evidence that this "
                "faith was received from the apostles, not invented locally."
            ),
            "relevance_chirho": (
                "Demonstrates that core Christian orthodoxy was established long before any "
                "church council 'decided' what Christians should believe. The consistency of "
                "belief across the early church is evidence against the claim that Christianity "
                "was significantly altered or 'invented' at Nicaea. The Rule of Faith also provides "
                "a basis for Christian unity on essentials while allowing diversity on secondary matters."
            ),
            "scripture_chirho": ["1 Corinthians 15:3-5", "Ephesians 4:4-6", "Jude 1:3", "2 Timothy 1:13-14"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book IV",
            "argument_chirho": (
                "The prophets and the Law were given by the same God who sent Christ; the "
                "progressive revelation of God unfolds in stages but with perfect consistency. "
                "Irenaeus shows that God adapted His communication to humanity's capacity to "
                "receive it — the Law was a tutor leading to Christ (anticipating Paul's language "
                "in Galatians 3:24). The covenants are not contradictory but pedagogical, leading "
                "humanity step by step toward the fullness revealed in Christ."
            ),
            "context_chirho": (
                "This argument addressed both Gnostics (who rejected the Old Testament God) and "
                "Jewish objectors (who saw no need for a New Covenant). Irenaeus holds both "
                "together: the Old Testament is genuinely from God AND it genuinely points forward "
                "to something greater. Neither the Marcionite rejection nor the Ebionite reduction "
                "of Christianity to Judaism captures the truth."
            ),
            "relevance_chirho": (
                "Provides a framework for understanding biblical progressive revelation that "
                "respects both testaments. Answers modern objections about apparent moral "
                "development between Old and New Testaments without resorting to either dismissing "
                "the Old Testament or denying the advancement brought by Christ. God's pedagogy "
                "with humanity is patient and purposeful."
            ),
            "scripture_chirho": ["Galatians 3:24-25", "Hebrews 1:1-2", "Matthew 5:17", "Romans 10:4"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Irenaeus (130-202 AD)",
            "work_chirho": "Against Heresies, Book II, Chapters 25-28",
            "argument_chirho": (
                "Human reason has limits, and accepting mystery is not anti-intellectual but "
                "intellectually honest. Irenaeus argues that the Gnostics' error is attempting "
                "to explain everything through speculative systems, when genuine wisdom recognizes "
                "that a finite mind cannot fully comprehend an infinite God. He counsels humility: "
                "'It is better to know nothing and to believe in God than to fall into impiety "
                "through subtle questions and hairsplitting.'"
            ),
            "context_chirho": (
                "The Gnostic systems claimed to explain the origin of evil, the nature of the "
                "divine realm, and the purpose of suffering through elaborate mythological "
                "frameworks. Irenaeus does not reject the use of reason but insists that reason "
                "must be grounded in revealed truth, not in speculative systems that go beyond "
                "what God has disclosed."
            ),
            "relevance_chirho": (
                "Provides a balanced approach to the faith-reason relationship. Against both "
                "anti-intellectual fideism and rationalistic overreach, Irenaeus models an "
                "apologetics that uses reason robustly while acknowledging its limits. This "
                "intellectual humility is needed in modern debates where both Christians and "
                "skeptics can overreach the bounds of what evidence and logic can demonstrate."
            ),
            "scripture_chirho": ["Deuteronomy 29:29", "Isaiah 55:8-9", "Romans 11:33-34", "1 Corinthians 13:12"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_tertullian_chirho() -> list[dict]:
    """Tertullian (155-220 AD): Apologeticum, Prescription Against Heretics, other works."""
    return [
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "Apologeticum",
            "argument_chirho": (
                "The legal persecution of Christians violates Rome's own principles of justice. "
                "Tertullian, a trained lawyer, argues that Roman law requires that a defendant "
                "be tried for specific criminal acts, not for bearing a name. Christians are "
                "convicted for the 'crime' of being Christian without evidence of any actual "
                "wrongdoing. He points out the absurd double standard: if a Christian renounces "
                "the faith, he is freed — even though his past 'crimes' should still warrant "
                "punishment if they were real crimes."
            ),
            "context_chirho": (
                "Written circa 197 AD in Carthage, addressed to Roman provincial governors. "
                "Tertullian was a North African lawyer-turned-theologian who brought legal "
                "precision to Christian apologetics. His Apologeticum is considered the finest "
                "legal defense of Christianity in the ancient world."
            ),
            "relevance_chirho": (
                "Demonstrates the importance of engaging legal and political systems on their "
                "own terms. Christians facing legal discrimination today (in both secular Western "
                "and authoritarian contexts) can follow Tertullian's model: demanding that the "
                "law be applied consistently and showing that persecution of Christians violates "
                "the persecutors' own stated principles."
            ),
            "scripture_chirho": ["Acts 25:10-11", "Romans 13:1-4", "1 Peter 2:13-17", "Acts 22:25-29"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "Apologeticum, Chapter 50",
            "argument_chirho": (
                "'The blood of the martyrs is the seed of the church' (Semen est sanguis "
                "Christianorum). Tertullian observes that persecution does not destroy Christianity "
                "but multiplies it. Every execution of a Christian produces more converts, because "
                "onlookers are compelled to investigate what inspires such courage. He challenges "
                "the Romans: 'Crucify us, torture us, condemn us, grind us to dust — your "
                "injustice is the proof that we are innocent... The more often we are mown down "
                "by you, the more in number we grow.'"
            ),
            "context_chirho": (
                "By Tertullian's time, over a century of intermittent persecution had failed to "
                "destroy Christianity. Instead, the faith had grown from a small Jewish sect to "
                "a significant movement across the Empire. Tertullian's observation was empirically "
                "verified: the great persecutions of Decius (250 AD), Valerian (257 AD), and "
                "Diocletian (303 AD) all preceded periods of explosive Christian growth."
            ),
            "relevance_chirho": (
                "This pattern has repeated throughout history: persecution in China under Mao "
                "produced the fastest-growing church in history; persecution in the Roman Empire "
                "led to Christianization of the Empire; persecution in early modern Japan "
                "produced hidden Christians who survived 250 years underground. The resilience "
                "of the church under persecution is itself evidence of supernatural sustaining power."
            ),
            "scripture_chirho": ["Matthew 16:18", "Acts 8:1-4", "Philippians 1:12-14", "2 Corinthians 4:8-10"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "De Testimonio Animae (On the Testimony of the Soul)",
            "argument_chirho": (
                "The soul is 'naturally Christian' (anima naturaliter christiana). Tertullian "
                "argues that even pagans, in unguarded moments, cry out to 'God' (not 'gods'), "
                "invoke divine judgment, sense an afterlife, and fear demons. These spontaneous "
                "expressions of the untutored soul testify to truths that Christianity explicitly "
                "teaches. The soul's innate religious sense points toward the God of Scripture "
                "even before hearing the Gospel."
            ),
            "context_chirho": (
                "This short work (circa 197-200 AD) makes an anthropological argument for "
                "Christianity: human nature itself testifies to Christian truth. Tertullian "
                "appeals not to philosophy or Scripture but to common human experience — the "
                "universal sense of God, moral accountability, and eternity that surfaces in "
                "every culture."
            ),
            "relevance_chirho": (
                "Anticipates the modern argument from universal religious experience and C.S. "
                "Lewis's 'argument from desire.' The fact that every culture in human history "
                "has had some concept of God, moral law, and afterlife points to a common source. "
                "Romans 1:19-20 teaches that God has made His existence plain to all people — "
                "Tertullian observes this playing out in everyday human experience."
            ),
            "scripture_chirho": ["Romans 1:19-20", "Romans 2:14-15", "Ecclesiastes 3:11", "Acts 17:26-28"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "Apologeticum, Chapters 7-9",
            "argument_chirho": (
                "Refutation of the charges of atheism, cannibalism, and incest leveled against "
                "Christians. Tertullian systematically dismantles each accusation: Christians "
                "are not atheists — they worship the one true God; the Eucharist involves bread "
                "and wine, not human flesh; Christian sexual ethics are stricter than Roman norms, "
                "not looser. He then turns the tables: it is pagan religion that practices human "
                "sacrifice (in gladiatorial games), and Roman mythology that celebrates divine "
                "incest (Jupiter and Juno)."
            ),
            "context_chirho": (
                "These accusations were widespread in the Roman world and were used to justify "
                "persecution. The charge of 'atheism' arose because Christians refused to "
                "sacrifice to Roman gods or the emperor. 'Cannibalism' was a misunderstanding "
                "of Eucharistic language ('eat my body, drink my blood'). 'Incest' arose from "
                "Christians calling each other 'brother' and 'sister' while practicing the 'kiss "
                "of peace.'"
            ),
            "relevance_chirho": (
                "The pattern of false accusations based on misunderstanding repeats throughout "
                "history. Christians today are accused of hatred, bigotry, and anti-science "
                "attitudes — often based on caricatures rather than actual Christian teaching "
                "and practice. Tertullian's method (address the accusation directly, correct the "
                "misunderstanding, then show that the accuser's own position has the real problem) "
                "remains effective."
            ),
            "scripture_chirho": ["1 Peter 3:16-17", "Matthew 5:11-12", "Acts 24:5-6", "Acts 28:22"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "De Praescriptione Haereticorum (Prescription Against Heretics)",
            "argument_chirho": (
                "Heretics have no right to appeal to Scripture because Scripture belongs to the "
                "church that received it from the apostles. Tertullian uses the legal concept of "
                "'prescription' (praescriptio) — a procedural objection that can end a case before "
                "it reaches the merits. Before debating individual proof-texts with heretics, he "
                "argues, we must establish WHO has the right to interpret Scripture: those churches "
                "founded by the apostles and maintaining their teaching, not newcomers with novel "
                "doctrines."
            ),
            "context_chirho": (
                "Written circa 200 AD against various heretical groups who used Scripture to "
                "support their teachings. Tertullian argues that the heretics' interpretations "
                "are innovative (novel), private (not publicly verified), and disconnected from "
                "the apostolic communities that received, preserved, and transmitted the texts."
            ),
            "relevance_chirho": (
                "Addresses the perennial problem of competing scriptural interpretations. While "
                "we affirm Scripture as the final authority, Tertullian rightly notes that context "
                "matters — Scripture was given to a community and must be read within the faith "
                "community's received understanding. This guards against individualistic "
                "interpretations that ignore 2,000 years of consistent Christian reading."
            ),
            "scripture_chirho": ["2 Peter 1:20-21", "2 Peter 3:16", "2 Timothy 2:15", "Acts 17:11"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "Apologeticum, Chapters 17-21",
            "argument_chirho": (
                "Christianity's claims can be verified by examining the Jewish Scriptures, which "
                "predate Christ and are held by a hostile witness (the Jewish nation). Tertullian "
                "argues that the antiquity of the Hebrew Scriptures — far older than Greek "
                "philosophy — gives them priority, and their preservation by Jews who reject "
                "Christ guarantees they were not fabricated by Christians. The prophecies of "
                "Christ's birth, ministry, death, and resurrection were written centuries before "
                "the events by people who had no motive to confirm Christianity."
            ),
            "context_chirho": (
                "Tertullian addresses the Roman intellectual's dismissal of Christianity as a "
                "recent novelty. By anchoring the faith in the ancient Hebrew Scriptures, he "
                "claims the antiquity that Roman culture respected. The 'hostile witness' "
                "argument — that Jews preserved prophecies about Christ without any motive to "
                "do so — remains one of the strongest evidential arguments for prophecy fulfillment."
            ),
            "relevance_chirho": (
                "The 'hostile witness' argument remains powerful: the Septuagint (Greek Old "
                "Testament, translated 250 BC), the Dead Sea Scrolls (150 BC-70 AD), and the "
                "continuous Jewish preservation of the Hebrew Bible all confirm that Messianic "
                "prophecies predate Jesus. Since Jewish communities had no reason to forge "
                "prophecies that would support Christianity, their preservation of these texts "
                "is unimpeachable testimony."
            ),
            "scripture_chirho": ["Isaiah 53:1-12", "Psalm 22:16-18", "Daniel 9:24-26", "Micah 5:2"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Tertullian (155-220 AD)",
            "work_chirho": "Apologeticum, Chapter 39",
            "argument_chirho": (
                "The Christian community's love, generosity, and mutual care demonstrate the "
                "truth of the faith. Tertullian describes the common fund to which Christians "
                "voluntarily contribute, used to feed the poor, bury the dead, support orphans, "
                "care for the elderly, and aid those imprisoned for their faith. He quotes the "
                "pagan reaction: 'See how they love one another!' — intended as mockery but "
                "actually the highest compliment and evidence of transformed lives."
            ),
            "context_chirho": (
                "Roman society was stratified and often cruel to the poor and vulnerable. "
                "Christian charity was genuinely revolutionary — caring for the sick during "
                "plagues (when pagans fled), rescuing abandoned infants, and feeding the poor "
                "regardless of status. Emperor Julian ('the Apostate', 4th century) later "
                "admitted that Christian charity put paganism to shame."
            ),
            "relevance_chirho": (
                "The argument from Christian social impact remains powerful: hospitals, "
                "universities, orphanages, abolition of slavery, civil rights movements, and "
                "global humanitarian organizations all have Christian roots. When the church "
                "lives out its calling to love, it provides the strongest apologetic for the "
                "Gospel. Jesus said the world would know His disciples by their love (John 13:35)."
            ),
            "scripture_chirho": ["John 13:34-35", "Acts 2:44-47", "Acts 4:32-35", "James 2:15-17"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_athanasius_chirho() -> list[dict]:
    """Athanasius (296-373 AD): On the Incarnation, Against the Arians."""
    return [
        {
            "father_chirho": "Athanasius (296-373 AD)",
            "work_chirho": "On the Incarnation, Chapters 1-10",
            "argument_chirho": (
                "Why God became man: humanity had fallen into corruption and death through sin, "
                "and only the Creator could recreate. Athanasius argues that since death had "
                "gained a legal hold on humanity through Adam's transgression, and since only "
                "the one who gave life could restore it, the Word of God took on a human body "
                "so that in it He could offer the sacrifice that would satisfy death's claim "
                "and restore humanity to incorruption. No angel or prophet could accomplish this "
                "— only God Himself."
            ),
            "context_chirho": (
                "Written circa 318 AD, possibly before the Council of Nicaea. This work, paired "
                "with 'Against the Gentiles,' is considered one of the greatest theological "
                "treatises of antiquity. C.S. Lewis wrote the introduction to a modern translation "
                "and called it 'a masterpiece.' Athanasius wrote it as a young man, likely in "
                "his early twenties."
            ),
            "relevance_chirho": (
                "Answers the fundamental question 'Why did God have to become human?' in a way "
                "that goes beyond mere legal substitution. The incarnation was not Plan B — it "
                "was the only way to restore what sin had destroyed, because only the Creator "
                "can re-create. This rich theology addresses the modern objection 'Why couldn't "
                "God just forgive?' — because the problem was not merely legal guilt but "
                "ontological corruption."
            ),
            "scripture_chirho": ["John 1:14", "Hebrews 2:14-15", "Romans 5:12-19", "2 Corinthians 5:21"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Athanasius (296-373 AD)",
            "work_chirho": "On the Incarnation, Chapters 20-32",
            "argument_chirho": (
                "The death and resurrection of Christ is proven by its effects: death has been "
                "robbed of its power. Athanasius argues empirically: before Christ, all people "
                "feared death. After Christ, even children and simple believers face death with "
                "courage and joy. Martyrs laugh at death. This universal change in humanity's "
                "relationship to death is inexplicable unless death was truly conquered. 'A dead "
                "man cannot perform such works — only the living.'"
            ),
            "context_chirho": (
                "Written when martyrdom was still a present reality — Christians were regularly "
                "dying for their faith. Athanasius witnessed the Great Persecution under Diocletian "
                "(303-313 AD) as a child in Alexandria. His argument draws on observable evidence: "
                "the changed behavior of Christians in the face of death."
            ),
            "relevance_chirho": (
                "The argument from the defeat of death's fear remains observable. Hospice chaplains, "
                "pastors, and medical professionals regularly witness the difference between "
                "Christian and non-Christian deaths. The peace and hope that believers display "
                "at death is not universal human experience — it is distinctively Christian and "
                "points to something real beyond this life."
            ),
            "scripture_chirho": ["1 Corinthians 15:54-57", "Hebrews 2:14-15", "Philippians 1:21-23", "Revelation 14:13"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Athanasius (296-373 AD)",
            "work_chirho": "On the Incarnation, Chapters 46-55",
            "argument_chirho": (
                "The transformation of the pagan world through Christianity proves its divine "
                "origin. Athanasius catalogs the changes wrought by the Gospel: oracles have "
                "fallen silent, demon worship has declined, human sacrifice has ceased, "
                "philosophers' schools have been superseded, warring tribes have been reconciled, "
                "and moral revolution has swept the Empire. A crucified carpenter from Galilee "
                "has accomplished what all the wisdom of Greece and power of Rome could not."
            ),
            "context_chirho": (
                "By Athanasius' time, Christianity had gone from a persecuted minority to a "
                "transformative cultural force. The old pagan temples were emptying, the "
                "gladiatorial games were being opposed, and a new moral vision was reshaping "
                "the Roman world. Athanasius presents this civilizational transformation as "
                "evidence for the resurrection."
            ),
            "relevance_chirho": (
                "The civilization-transforming power of Christianity is historically undeniable: "
                "the abolition of gladiatorial games, the elevation of women's status, the "
                "establishment of hospitals and universities, the abolition of slavery, the "
                "development of human rights. While Christians have also failed grievously at "
                "times, the net impact of the Gospel on civilization is overwhelmingly positive "
                "and historically demonstrable."
            ),
            "scripture_chirho": ["Matthew 13:31-33", "Isaiah 2:2-4", "Daniel 2:44", "Acts 17:6"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Athanasius (296-373 AD)",
            "work_chirho": "On the Incarnation, Chapters 33-40",
            "argument_chirho": (
                "The divinity of Christ is proven by His works: healing the sick, raising the "
                "dead, calming storms, and — supremely — His own resurrection. Athanasius "
                "argues that if someone performs the works of God, we should acknowledge him "
                "as God. Christ's miracles during his ministry, the manner of his death "
                "(darkness, earthquake, torn veil), and his resurrection are not merely "
                "displays of power but revelations of identity."
            ),
            "context_chirho": (
                "This section addresses pagan objectors who accepted that Jesus performed "
                "wonders but attributed them to magic (a common charge). Athanasius distinguishes "
                "Christ's miracles from magic: magicians work by incantations and charms; Christ "
                "healed by a word or touch. Magicians serve demons; Christ cast out demons. "
                "Magic cannot raise the dead permanently or transform civilizations."
            ),
            "relevance_chirho": (
                "The argument from Christ's works is still central to apologetics. Modern "
                "skeptics who acknowledge Jesus' historical existence must account for the "
                "explosive growth of a movement centered on miraculous claims. The 'legend "
                "theory' fails because the timeline is too short (Paul's letters date to 20 "
                "years after the crucifixion), and the 'conspiracy theory' fails because the "
                "apostles gained nothing worldly from their claims."
            ),
            "scripture_chirho": ["John 10:37-38", "John 14:11", "Acts 2:22", "Matthew 11:4-6"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Athanasius (296-373 AD)",
            "work_chirho": "On the Incarnation, Chapters 11-19",
            "argument_chirho": (
                "The cross was not a defeat but the definitive victory over death. Athanasius "
                "explains that Christ chose crucifixion specifically — a public death with "
                "arms outstretched — so that His victory would be visible and undeniable. He "
                "did not die in private or of old age; He accepted the worst death His enemies "
                "could inflict and then rose again, proving that no form of death could hold Him. "
                "The cross is God's trophy, not His shame."
            ),
            "context_chirho": (
                "Both Jews and pagans objected to a crucified Messiah/God. For Jews, 'cursed is "
                "anyone who hangs on a tree' (Deuteronomy 21:23). For pagans, crucifixion was "
                "the most shameful death, reserved for slaves and rebels. Athanasius transforms "
                "this objection into an argument: Christ deliberately chose the most shameful "
                "death to demonstrate that He has power over every kind of death."
            ),
            "relevance_chirho": (
                "The 'scandal of the cross' remains the most counterintuitive claim of "
                "Christianity and paradoxically its strongest argument. No human inventor would "
                "create a religion centered on a crucified founder — the idea is culturally "
                "absurd (as Paul acknowledges in 1 Corinthians 1:23). The fact that this message "
                "conquered the world despite its initial absurdity points to a power beyond human "
                "strategy."
            ),
            "scripture_chirho": ["1 Corinthians 1:18-25", "Galatians 3:13", "Colossians 2:14-15", "Hebrews 12:2"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Athanasius (296-373 AD)",
            "work_chirho": "Orationes Contra Arianos (Against the Arians)",
            "argument_chirho": (
                "If Christ is not truly God, then we are not truly saved. Athanasius argues "
                "against Arius that only God can save — if the Son is a creature (however "
                "exalted), He cannot bridge the infinite gap between Creator and creation. "
                "Salvation requires that the one who saves us IS God, for only God can grant "
                "participation in the divine life. The Arian Christ is too small for the task "
                "of redemption. The doctrine of Christ's full divinity is not speculative "
                "theology — it is the foundation of the Gospel."
            ),
            "context_chirho": (
                "Athanasius spent most of his career (and was exiled five times) fighting "
                "Arianism, which taught that the Son was the first and greatest creature but "
                "not truly God. The Council of Nicaea (325 AD) affirmed Christ's full divinity "
                "(homoousios — 'of one substance' with the Father), but Arian theology remained "
                "powerful for decades. Athanasius 'contra mundum' (against the world) stood "
                "firm when much of the church wavered."
            ),
            "relevance_chirho": (
                "The deity of Christ remains under attack from Jehovah's Witnesses, Unitarians, "
                "liberal theology, Islam, and others. Athanasius' soteriological argument is the "
                "most powerful response: the question is not abstract (what is Christ's nature?) "
                "but practical (can Christ save you?). Only if Christ is truly God can His death "
                "have infinite value and His resurrection be the firstfruits of our own."
            ),
            "scripture_chirho": ["John 1:1-3", "John 10:30", "Colossians 1:15-20", "Hebrews 1:3", "Titus 2:13"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_augustine_chirho() -> list[dict]:
    """Augustine (354-430 AD): City of God, Confessions, other works."""
    return [
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "City of God, Books I-V",
            "argument_chirho": (
                "The two cities: humanity is divided between the City of God (those who love God "
                "to the point of self-denial) and the City of Man (those who love self to the "
                "point of denying God). Augustine argues that all of human history is the story "
                "of these two cities intermingled, and that the ultimate outcome is certain: the "
                "City of God will endure while all earthly empires — Rome included — are temporary. "
                "Christians should not place their hope in any political order but in the eternal "
                "kingdom of God."
            ),
            "context_chirho": (
                "Written 413-426 AD in response to the sack of Rome by the Visigoths (410 AD). "
                "Pagans blamed Christianity for Rome's fall, claiming that abandoning the old "
                "gods had brought divine punishment. Augustine's massive work (22 books) responds "
                "by reframing all of history through a theological lens. It is arguably the most "
                "influential work of Christian philosophy ever written."
            ),
            "relevance_chirho": (
                "The 'two cities' framework is essential for Christians navigating political "
                "engagement. It prevents both the error of theocracy (confusing the City of God "
                "with any earthly state) and the error of withdrawal (abandoning responsibility "
                "for the earthly city). When empires fall and cultures shift, the church endures — "
                "a truth demonstrated by 2,000 years of history."
            ),
            "scripture_chirho": ["Hebrews 11:10", "Hebrews 13:14", "Philippians 3:20", "John 18:36"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "Confessions, Book I, Chapter 1",
            "argument_chirho": (
                "'You have made us for yourself, O Lord, and our hearts are restless until they "
                "rest in you.' Augustine's famous prayer encapsulates the argument from desire: "
                "the universal human experience of longing, dissatisfaction, and searching points "
                "to a transcendent object of desire that no earthly thing can satisfy. Augustine's "
                "own journey through sensuality, ambition, Manichaeism, and Neoplatonism — finding "
                "each ultimately hollow — illustrates that the human heart has a God-shaped void "
                "that only God can fill."
            ),
            "context_chirho": (
                "Written circa 397-400 AD. The Confessions is the first major autobiography in "
                "Western literature and traces Augustine's spiritual journey from his youth in "
                "North Africa through his conversion in Milan (386 AD). It is addressed directly "
                "to God as an extended prayer, making it simultaneously personal testimony and "
                "philosophical argument."
            ),
            "relevance_chirho": (
                "The 'restless heart' argument resonates deeply in a culture of unprecedented "
                "material abundance and unprecedented rates of depression, anxiety, and suicide. "
                "Despite having more comfort, entertainment, and choices than any generation in "
                "history, modern people report high levels of emptiness and meaninglessness. "
                "Augustine's diagnosis — that nothing less than God can satisfy the human heart — "
                "explains what material prosperity cannot."
            ),
            "scripture_chirho": ["Ecclesiastes 3:11", "Psalm 42:1-2", "Psalm 63:1", "Isaiah 55:1-2", "John 4:13-14"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "City of God, Books XI-XII; Confessions, Book VII",
            "argument_chirho": (
                "The problem of evil: evil is not a substance but a privation (absence) of good. "
                "Augustine argues that God created all things good, and evil has no independent "
                "existence — it is a corruption, a parasite on the good, like a wound in healthy "
                "flesh or darkness as absence of light. Evil entered through the free will of "
                "rational creatures (angels and humans) who chose lesser goods over the supreme "
                "Good. This means God is not the author of evil, yet evil is real and requires "
                "the good to exist."
            ),
            "context_chirho": (
                "Augustine had been a Manichaean for nine years, drawn by their answer to the "
                "problem of evil (two co-eternal principles: good and evil). His privation theory "
                "was a breakthrough that freed him from Manichaeism: evil does not require a "
                "separate evil deity because it has no positive existence of its own. This became "
                "the dominant Christian understanding of evil."
            ),
            "relevance_chirho": (
                "The problem of evil remains the most common objection to Christianity. Augustine's "
                "privation theory, combined with the free will defense, provides a coherent "
                "framework: God created a good world with free creatures; free creatures chose "
                "against God; the resulting corruption is real but parasitic on God's good "
                "creation. This is not a complete 'answer' to suffering but a demonstration "
                "that evil and a good God are not logically incompatible."
            ),
            "scripture_chirho": ["Genesis 1:31", "James 1:13-15", "Romans 5:12", "Isaiah 45:7", "1 John 1:5"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "On Free Choice of the Will; On Grace and Free Will",
            "argument_chirho": (
                "Free will and divine grace are not contradictory but complementary. Augustine "
                "argues that human beings have genuine free will — we truly choose — but that "
                "after the Fall, our will is enslaved to sin and cannot choose God without "
                "divine grace. Grace does not destroy freedom but restores it: the truly free "
                "will is the will that is free to choose the good, which only grace makes "
                "possible. 'Give what you command, and command what you will.'"
            ),
            "context_chirho": (
                "Augustine developed this theology in debate with Pelagius (circa 410-430 AD), "
                "who taught that humans can obey God perfectly by their own natural willpower "
                "without special grace. Augustine insisted that the Fall left humanity unable "
                "to save itself — grace is not merely helpful but necessary. This became the "
                "foundation of Western theology on grace and was affirmed at the Council of "
                "Carthage (418 AD)."
            ),
            "relevance_chirho": (
                "The grace-versus-works question is still central to evangelism and apologetics. "
                "Many people intuitively assume they must earn God's favor (moralism) or that "
                "they are basically good enough (Pelagianism). Augustine's insistence on grace "
                "aligns with Paul's teaching in Ephesians 2:8-9 and confronts both self-righteous "
                "moralism and despairing self-condemnation: salvation is God's gift, not our "
                "achievement."
            ),
            "scripture_chirho": ["Ephesians 2:8-9", "Romans 9:16", "John 15:5", "Philippians 2:12-13"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "City of God, Books VI-X",
            "argument_chirho": (
                "Historical apologetics: Rome fell not because of Christianity but because of "
                "its own moral corruption. Augustine demonstrates that Rome had suffered "
                "catastrophic defeats long before Christianity — the Gallic sack of 390 BC, "
                "civil wars, Nero's tyranny — when the pagan gods were still being worshipped. "
                "The old gods never protected Rome; they did not even exist. Furthermore, the "
                "Roman virtues that built the Republic (courage, self-sacrifice, justice) were "
                "distorted reflections of Christian virtues that find their true source in God."
            ),
            "context_chirho": (
                "The sack of Rome in 410 AD was a civilizational earthquake. Pagans immediately "
                "blamed Christians for angering the gods. Augustine spent years demolishing this "
                "charge, showing from Roman history itself that pagan worship had never guaranteed "
                "Roman security. He then argues that the true source of civilizational strength "
                "is virtue, and true virtue requires the true God."
            ),
            "relevance_chirho": (
                "When modern societies decline, Christianity is often blamed. Augustine's method — "
                "examining the actual historical record rather than accepting scapegoating — "
                "remains essential. The data consistently shows that societies where Christian "
                "values (rule of law, human dignity, charity) flourish tend to prosper, while "
                "their abandonment correlates with decline. This is historical observation, not "
                "theocratic assertion."
            ),
            "scripture_chirho": ["Proverbs 14:34", "Psalm 33:12", "Daniel 2:21", "Jeremiah 18:7-10"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "Confessions, Book VIII",
            "argument_chirho": (
                "The power of conversion testimony: Augustine's own dramatic conversion "
                "demonstrates that the Gospel can reach and transform anyone, no matter how "
                "deep in sin. A man enslaved to lust, intellectual pride, and false philosophy "
                "was radically transformed by hearing a child's voice say 'Take up and read' — "
                "opening Romans 13:13-14 and being instantly freed. His honest account of "
                "struggling to let go of sin ('Give me chastity, Lord — but not yet') makes "
                "the conversion all the more credible."
            ),
            "context_chirho": (
                "Augustine's conversion in a Milan garden (386 AD) is one of the most famous "
                "conversion stories in history. He had been a Manichaean, a skeptic, and a "
                "rhetorician living in sexual immorality despite years of his mother Monica's "
                "prayers. His conversion influenced countless others, including most famously "
                "the conversion of C.S. Lewis, who called the Confessions the first book that "
                "'gave him a window into another man's soul.'"
            ),
            "relevance_chirho": (
                "Personal testimony remains one of the most effective apologetic tools. Augustine "
                "models honesty about sin, intellectual struggle, and the gradual work of grace. "
                "His story resonates with anyone who has struggled with addiction, doubt, or the "
                "tension between knowing what is right and being unable to do it (Romans 7:15-25). "
                "The Gospel is not merely a theory — it is a power that transforms real people."
            ),
            "scripture_chirho": ["Romans 13:13-14", "Romans 7:15-25", "2 Corinthians 5:17", "1 Timothy 1:15-16"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Augustine (354-430 AD)",
            "work_chirho": "Confessions, Book XI",
            "argument_chirho": (
                "God exists outside of time as the eternal present. Augustine's meditation on "
                "the nature of time — 'What then is time? If no one asks me, I know; if I wish "
                "to explain it, I do not know' — leads him to conclude that God created time "
                "itself along with the universe. The question 'What was God doing before creation?' "
                "is therefore incoherent — there was no 'before' creation. God experiences all "
                "moments simultaneously in an eternal present."
            ),
            "context_chirho": (
                "This philosophical meditation in Book XI of the Confessions is one of the most "
                "profound discussions of time in all of Western philosophy, anticipating modern "
                "physics (particularly relativity theory's treatment of time as a dimension). "
                "It addresses the Manichaean objection about what God was doing 'before' creating — "
                "an objection still raised by modern skeptics."
            ),
            "relevance_chirho": (
                "Addresses the common skeptical question 'Who created God?' and 'What was God "
                "doing before the universe?' If God is the creator of time, these questions are "
                "category errors. Modern cosmology (Big Bang theory) confirms that time had a "
                "beginning — and Augustine articulated this theological truth 1,500 years before "
                "modern physics caught up. God is not a being within time needing a cause; He is "
                "the eternal cause of time itself."
            ),
            "scripture_chirho": ["Genesis 1:1", "Psalm 90:2", "2 Peter 3:8", "Revelation 1:8"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_chrysostom_chirho() -> list[dict]:
    """Chrysostom (347-407 AD): Homilies and other works."""
    return [
        {
            "father_chirho": "John Chrysostom (347-407 AD)",
            "work_chirho": "Homilies on the Gospel of Matthew",
            "argument_chirho": (
                "The power of Scripture to transform lives is itself evidence of its divine "
                "origin. Chrysostom argues that the Bible, written by fishermen and tentmakers, "
                "has achieved what the works of Plato, Aristotle, and all the philosophers could "
                "not: it has changed the moral character of entire nations, reached every social "
                "class, and remained relevant across centuries. The uneducated apostles conquered "
                "the world's greatest intellects — this is explicable only by divine power "
                "working through the text."
            ),
            "context_chirho": (
                "Chrysostom ('Golden Mouth') was the greatest preacher of the early church, "
                "serving as Archbishop of Constantinople (398-404 AD). His homilies were delivered "
                "to ordinary congregations and are remarkable for their accessibility, practical "
                "application, and rhetorical brilliance. He preached through almost the entire "
                "New Testament verse by verse."
            ),
            "relevance_chirho": (
                "The Bible remains the world's best-selling and most translated book — over 5 "
                "billion copies, translated into over 700 languages. No other ancient text has "
                "this reach or enduring impact. Chrysostom's argument is stronger today than in "
                "his time: after 2,000 years, the Scriptures continue to transform lives across "
                "every culture, language, and social class."
            ),
            "scripture_chirho": ["Isaiah 55:10-11", "Hebrews 4:12", "2 Timothy 3:16-17", "Romans 1:16"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "John Chrysostom (347-407 AD)",
            "work_chirho": "Homilies on First Corinthians",
            "argument_chirho": (
                "The moral transformation wrought by Christ proves the Gospel more effectively "
                "than any philosophical argument. Chrysostom points to the concrete changes in "
                "converts: prostitutes becoming virgins of prayer, thieves becoming philanthropists, "
                "the violent becoming peacemakers, the greedy becoming generous. Philosophy could "
                "convince the mind but could not change the heart. Christ does both."
            ),
            "context_chirho": (
                "Chrysostom preached in Antioch and Constantinople — cosmopolitan cities where "
                "Greek philosophy was still respected. He did not dismiss philosophy but argued "
                "that Christianity accomplished what philosophy only theorized about. His sermons "
                "consistently moved from doctrine to practice, insisting that transformed living "
                "is the true test of true faith."
            ),
            "relevance_chirho": (
                "In an age of therapeutic self-help culture that promises transformation through "
                "techniques and programs, the Gospel's power to genuinely change people at the "
                "deepest level remains distinctive. Addiction recovery programs, prison ministry, "
                "and transformed lives in the most hostile environments testify to a power beyond "
                "human motivation and willpower."
            ),
            "scripture_chirho": ["1 Corinthians 6:9-11", "2 Corinthians 5:17", "Ezekiel 36:26-27", "Romans 12:1-2"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "John Chrysostom (347-407 AD)",
            "work_chirho": "Homilies on Lazarus and the Rich Man; On Wealth and Poverty",
            "argument_chirho": (
                "Christian social justice flows from theological conviction, not mere humanitarianism. "
                "Chrysostom thundered against the wealthy who neglected the poor, arguing that "
                "every human being bears the image of God and that hoarding wealth while others "
                "starve is robbery. He declared: 'Not to share our wealth with the poor is theft "
                "from the poor and deprivation of their means of life. The goods we possess are "
                "not ours, but theirs.' This is not socialism but stewardship — all belongs to God."
            ),
            "context_chirho": (
                "Chrysostom's social preaching was so bold that it ultimately led to his exile. "
                "He confronted the Empress Eudoxia and the wealthy elite of Constantinople, "
                "earning the hatred of the powerful. His advocacy for the poor was rooted entirely "
                "in Scripture and theology, not in political ideology. He is considered the "
                "greatest social voice of the ancient church."
            ),
            "relevance_chirho": (
                "Christianity's record on social justice — hospitals, orphanages, abolition, "
                "civil rights, global humanitarian aid — is rooted in the theological conviction "
                "that every person bears God's image. This provides a foundation for human dignity "
                "that secular philosophies struggle to establish. When Christians care for the "
                "poor, they demonstrate the love of Christ and provide a compelling apologetic."
            ),
            "scripture_chirho": ["Matthew 25:31-46", "James 2:15-17", "Proverbs 19:17", "1 John 3:17-18"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "John Chrysostom (347-407 AD)",
            "work_chirho": "Discourses Against Judaizing Christians",
            "argument_chirho": (
                "The destruction of the Jerusalem Temple (70 AD) and the failure of Julian the "
                "Apostate's attempt to rebuild it (363 AD) are powerful confirmations of Christ's "
                "prophecy. Chrysostom argues that Jesus predicted the Temple's destruction "
                "(Matthew 24:1-2), and it was fulfilled exactly. When Emperor Julian attempted "
                "to rebuild it (specifically to disprove Christ's prophecy), fire repeatedly "
                "erupted from the foundations, forcing the project's abandonment — an event "
                "attested by both Christian and pagan historians (Ammianus Marcellinus)."
            ),
            "context_chirho": (
                "Chrysostom preached these homilies in Antioch (386-387 AD) to Christians who "
                "were attending synagogue services and Jewish festivals alongside Christian "
                "worship. While some of his rhetoric toward Jewish practice is harsh by modern "
                "standards, the core argument about fulfilled prophecy stands on its own merits. "
                "The Julian incident was recent history for his audience."
            ),
            "relevance_chirho": (
                "The destruction of the Temple in 70 AD remains one of the most dramatic "
                "fulfillments of biblical prophecy. Jesus specifically predicted it (Matthew "
                "24:1-2, Luke 19:43-44), and it was fulfilled within a generation, exactly as "
                "He said. The historical fact that no Temple has been rebuilt in nearly 2,000 "
                "years — despite multiple attempts — is a continuing testimony to Christ's "
                "prophetic authority."
            ),
            "scripture_chirho": ["Matthew 24:1-2", "Luke 19:43-44", "Luke 21:5-6", "Daniel 9:26"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "John Chrysostom (347-407 AD)",
            "work_chirho": "Homilies on the Acts of the Apostles",
            "argument_chirho": (
                "The practical fruit of Christianity — transformed communities, radical generosity, "
                "and enduring hope in suffering — is the strongest evidence for its truth. "
                "Chrysostom argues that the early church described in Acts (sharing possessions, "
                "caring for widows, rejoicing in persecution) was not a utopian ideal but a "
                "historical reality that proved the Gospel's power. He challenges his own "
                "congregation to recover this original Christian practice."
            ),
            "context_chirho": (
                "By Chrysostom's time (late 4th century), Christianity had become the Empire's "
                "official religion, and many 'converts' were nominal. Chrysostom's homilies on "
                "Acts served as both apologetics (showing what true Christianity produces) and "
                "prophetic challenge (calling nominal Christians back to authentic faith). His "
                "insistence that practice validates profession echoes James 2:17."
            ),
            "relevance_chirho": (
                "The gap between Christian profession and practice remains the single greatest "
                "obstacle to evangelism. Chrysostom's insistence that 'practical Christianity' "
                "is the best evidence resonates with Gandhi's famous observation: 'I like your "
                "Christ. I do not like your Christians.' When the church lives authentically — "
                "radical generosity, genuine community, costly love — it becomes the most "
                "powerful apologetic argument available."
            ),
            "scripture_chirho": ["Acts 2:42-47", "James 2:17", "Matthew 5:16", "John 13:34-35"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "John Chrysostom (347-407 AD)",
            "work_chirho": "Homilies on the Gospel of John",
            "argument_chirho": (
                "The Gospel of John demonstrates that the apostolic testimony is eyewitness "
                "testimony, not legend or myth. Chrysostom emphasizes John's opening claim: 'That "
                "which we have heard, which we have seen with our eyes, which we looked upon and "
                "have touched with our hands, concerning the word of life' (1 John 1:1). The "
                "specificity of detail, the inclusion of embarrassing material, and the naming "
                "of living witnesses all mark the Gospels as historical testimony, not mythology."
            ),
            "context_chirho": (
                "Chrysostom's verse-by-verse exposition of John's Gospel highlighted the "
                "eyewitness nature of the testimony against both pagan dismissal (Christianity "
                "as superstition) and heretical reinterpretation (Gnostic allegorizing that "
                "denied the historical events). He consistently argued that the historical "
                "facts of the Gospel are the foundation, not optional additions to spiritual truths."
            ),
            "relevance_chirho": (
                "Modern scholarship has increasingly recognized the Gospels as ancient biographies "
                "(bioi), not myth or legend. Richard Bauckham's 'Jesus and the Eyewitnesses' "
                "(2006) has reinforced what Chrysostom argued: the Gospels bear the marks of "
                "eyewitness testimony — specific names, precise details, irrelevant specifics, "
                "and inclusion of embarrassing material that no inventor would create."
            ),
            "scripture_chirho": ["1 John 1:1-3", "2 Peter 1:16", "Luke 1:1-4", "John 21:24"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_polycarp_chirho() -> list[dict]:
    """Polycarp (69-155 AD): Epistle to the Philippians, Martyrdom of Polycarp."""
    return [
        {
            "father_chirho": "Polycarp (69-155 AD)",
            "work_chirho": "Martyrdom of Polycarp (by the church of Smyrna)",
            "argument_chirho": (
                "Polycarp's direct connection to the apostle John provides a living chain of "
                "testimony from Christ to the post-apostolic church. Irenaeus records that as a "
                "young man he heard Polycarp recount his conversations with the apostle John and "
                "others who had seen the Lord. This is not distant hearsay but a one-link chain: "
                "Jesus spoke to John, John taught Polycarp, Polycarp taught Irenaeus. The "
                "historical proximity demolishes the claim that Christianity was significantly "
                "altered between the apostolic era and the later church."
            ),
            "context_chirho": (
                "Polycarp was Bishop of Smyrna in Asia Minor and was recognized throughout the "
                "early church as a direct disciple of the apostle John. He serves as a critical "
                "link between the apostolic generation and the 2nd-century church. His epistle "
                "and martyrdom account are among the most important early Christian documents "
                "outside the New Testament."
            ),
            "relevance_chirho": (
                "Against the claim that early Christianity was significantly different from what "
                "the New Testament presents, Polycarp provides concrete evidence of continuity. "
                "His letter to the Philippians extensively quotes or alludes to New Testament "
                "books (Matthew, Acts, Romans, 1-2 Corinthians, Galatians, Ephesians, Philippians, "
                "1-2 Timothy, 1 Peter, 1 John), showing these were already authoritative by the "
                "early 2nd century."
            ),
            "scripture_chirho": ["2 Timothy 2:2", "1 John 1:1-3", "John 21:24", "Acts 20:17-35"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Polycarp (69-155 AD)",
            "work_chirho": "Martyrdom of Polycarp",
            "argument_chirho": (
                "Polycarp's martyrdom at age 86 demonstrates steadfast faith unto death. When "
                "ordered to swear by the genius of Caesar and say 'Away with the atheists,' "
                "Polycarp pointed to the pagan crowd and said 'Away with the atheists!' When "
                "told to revile Christ, he replied: 'Eighty-six years have I served Him, and "
                "He has done me no wrong. How can I blaspheme my King and Savior?' He was then "
                "burned alive. The fire reportedly formed an arch around him, and he had to be "
                "stabbed when the flames did not consume him."
            ),
            "context_chirho": (
                "The Martyrdom of Polycarp (circa 155-156 AD) is the earliest surviving account "
                "of a Christian martyrdom outside the New Testament. It was written by the church "
                "at Smyrna as a circular letter to other churches. The account is measured and "
                "sober in tone, distinguishing it from later hagiographical embellishments. It "
                "established the genre of Christian martyrdom accounts."
            ),
            "relevance_chirho": (
                "The willingness to die for a testimony one has received directly from eyewitnesses "
                "is uniquely powerful evidence. Polycarp could have known whether the apostolic "
                "claims were true — he knew John personally. He chose death over denial at age 86 "
                "when he had nothing worldly to gain. This is not the behavior of someone "
                "following a known fiction."
            ),
            "scripture_chirho": ["Revelation 2:10", "2 Timothy 4:6-8", "Acts 7:55-60", "Philippians 1:21"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Polycarp (69-155 AD)",
            "work_chirho": "Martyrdom of Polycarp",
            "argument_chirho": (
                "The witness of martyrdom as evidence for the truth of Christianity: the early "
                "church did not merely teach doctrines but sealed them with blood. The account "
                "of Polycarp's death emphasizes that he went willingly, refused rescue, and "
                "prayed for his persecutors — paralleling Christ's own passion. The witnesses "
                "reported that his burning body smelled not of burning flesh but of baking bread "
                "and incense. Whether or not one accepts every detail, the historical fact of "
                "his willing death is undisputed."
            ),
            "context_chirho": (
                "The early church distinguished between seeking martyrdom (which was discouraged) "
                "and accepting it when it came (which was honored). Polycarp initially withdrew "
                "from the city but was eventually captured. His behavior at trial — dignified, "
                "courageous, and forgiving — set the template for how Christians should face "
                "persecution: not with hatred or fear, but with the peace that surpasses "
                "understanding."
            ),
            "relevance_chirho": (
                "Martyrdom continues in the modern world — more Christians were killed for their "
                "faith in the 20th century than in all previous centuries combined. The testimony "
                "of modern martyrs (Dietrich Bonhoeffer, Jim Elliot, the 21 Coptic martyrs in "
                "Libya) follows Polycarp's pattern: willing, forgiving, hopeful. This ongoing "
                "pattern of costly witness is among the most compelling evidence that Christianity "
                "is not merely a set of beliefs but an encounter with a living Person."
            ),
            "scripture_chirho": ["Revelation 12:11", "Acts 20:24", "Hebrews 11:35-38", "Matthew 10:28"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Polycarp (69-155 AD)",
            "work_chirho": "Epistle to the Philippians",
            "argument_chirho": (
                "Continuity with apostolic teaching: Polycarp's letter demonstrates that the "
                "theology of the early 2nd-century church was the same theology found in the "
                "New Testament. He affirms justification by faith (echoing Paul), the bodily "
                "resurrection of Christ, the reality of future judgment, and the call to holy "
                "living. He quotes or alludes to at least 16 New Testament books, showing their "
                "early widespread authority. The faith Polycarp received from John is the faith "
                "we find in the New Testament."
            ),
            "context_chirho": (
                "Written circa 110-140 AD (date debated), this letter was sent in response to "
                "the Philippian church's request for copies of Ignatius of Antioch's letters. "
                "Polycarp includes pastoral instruction that mirrors Pauline theology, showing "
                "that the apostolic deposit was faithfully transmitted. The letter's many NT "
                "allusions demonstrate which books were already authoritative."
            ),
            "relevance_chirho": (
                "Destroys the myth that early Christianity was radically diverse and that "
                "'orthodoxy' was a later invention. Polycarp, who learned from John, teaches "
                "the same Gospel that Paul taught — resurrection, judgment, grace, and holiness. "
                "This convergence of a Johannine disciple with Pauline theology proves that "
                "the apostolic message was unified, not the product of competing factions "
                "that were later harmonized."
            ),
            "scripture_chirho": ["Jude 1:3", "2 Timothy 1:13-14", "Galatians 1:8-9", "1 Corinthians 15:1-4"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Polycarp (69-155 AD)",
            "work_chirho": "Epistle to the Philippians, Chapter 7",
            "argument_chirho": (
                "Polycarp warns against those who deny the incarnation and bodily resurrection: "
                "'For whoever does not confess that Jesus Christ has come in the flesh is "
                "antichrist; and whoever does not confess the testimony of the cross is of "
                "the devil; and whoever perverts the sayings of the Lord to his own desires "
                "and says there is neither resurrection nor judgment — that man is the firstborn "
                "of Satan.' This direct echo of 1 John 4:2-3 shows the earliest church firmly "
                "held to physical incarnation and bodily resurrection as non-negotiable."
            ),
            "context_chirho": (
                "Polycarp confronted early Docetism — the heresy that Christ only appeared to "
                "have a physical body. According to Irenaeus, when Polycarp met the heretic "
                "Marcion in Rome and Marcion asked 'Do you recognize me?', Polycarp replied: "
                "'I recognize you as the firstborn of Satan.' This was not rudeness but the "
                "urgency of a man who had learned from an apostle that false teaching about "
                "Christ destroys souls."
            ),
            "relevance_chirho": (
                "The physical incarnation and bodily resurrection remain under attack from "
                "liberal theology, New Age spirituality, and Gnostic-influenced movements. "
                "Polycarp — who received his theology directly from the apostle John — treated "
                "denial of the incarnation and resurrection as the most serious possible heresy. "
                "This earliest post-apostolic testimony confirms that Christianity has always "
                "been a historical, physical, bodily faith — not merely a 'spiritual' philosophy."
            ),
            "scripture_chirho": ["1 John 4:2-3", "2 John 1:7", "1 Corinthians 15:12-19", "Romans 10:9"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def build_clement_rome_chirho() -> list[dict]:
    """Clement of Rome (35-99 AD): First Epistle to the Corinthians."""
    return [
        {
            "father_chirho": "Clement of Rome (35-99 AD)",
            "work_chirho": "First Epistle to the Corinthians",
            "argument_chirho": (
                "Church order and apostolic succession: Clement writes that the apostles, "
                "knowing there would be disputes over leadership, appointed bishops and deacons "
                "and established a rule of succession. He argues that those who were appointed "
                "by the apostles (or by other approved men with the consent of the whole church) "
                "cannot justly be removed from their office. This letter is the earliest evidence "
                "of one church (Rome) exercising authority to address disorder in another (Corinth)."
            ),
            "context_chirho": (
                "Written circa 96 AD — making it likely the earliest surviving Christian document "
                "outside the New Testament. The Corinthian church had deposed some of its presbyters, "
                "and Clement writes on behalf of the Roman church to address this disorder. "
                "Clement is traditionally identified as the third or fourth bishop of Rome, and "
                "some early sources say he was appointed by the apostle Peter himself."
            ),
            "relevance_chirho": (
                "This letter demonstrates that church structure, authority, and orderly succession "
                "were established from the very beginning — not invented later. It shows the "
                "apostolic church was organized, not chaotic, and that there was a recognized "
                "standard of order. Against claims that early Christianity had no structure or "
                "hierarchy, Clement provides contemporary evidence of a church with recognized "
                "leaders, established procedures, and inter-church accountability."
            ),
            "scripture_chirho": ["Titus 1:5-9", "1 Timothy 3:1-13", "Acts 14:23", "Acts 20:28"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Clement of Rome (35-99 AD)",
            "work_chirho": "First Epistle to the Corinthians",
            "argument_chirho": (
                "As the earliest extra-biblical Christian writing, 1 Clement demonstrates what "
                "the church believed within living memory of the apostles. Clement writes as "
                "a contemporary of the apostles (he references Peter and Paul as recent examples "
                "of martyrdom), and his theology aligns perfectly with the New Testament: he "
                "affirms the resurrection, the atonement, justification, the authority of "
                "Scripture, and the return of Christ. There is no 'gap' between apostolic and "
                "post-apostolic teaching."
            ),
            "context_chirho": (
                "Clement wrote during the reign of Domitian (81-96 AD), a period of persecution "
                "(referenced in the letter's opening). He may have known Peter and Paul personally "
                "(Irenaeus and Tertullian claim he was appointed by Peter). His letter is a "
                "firsthand witness to what the church believed just decades after the apostles "
                "and just one generation after Christ."
            ),
            "relevance_chirho": (
                "1 Clement is a critical piece of evidence against the claim that Christianity "
                "was significantly modified over time. A document from 96 AD — within 30 years "
                "of the latest New Testament writings — confirms the same core faith. This "
                "demolishes theories that Christianity was 'invented' by later generations or "
                "significantly altered at Nicaea (325 AD). The faith was fixed from the beginning."
            ),
            "scripture_chirho": ["Jude 1:3", "2 Timothy 1:13", "Hebrews 13:8", "1 Corinthians 15:3-5"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Clement of Rome (35-99 AD)",
            "work_chirho": "First Epistle to the Corinthians, Chapter 25",
            "argument_chirho": (
                "Clement argues for the resurrection from analogies in nature: the cycle of day "
                "and night, the dying and sprouting of seeds, and — remarkably — the legend of "
                "the phoenix bird that dies and rises from its own ashes. While the phoenix myth "
                "is not historical, Clement's use of it reveals the early Christian apologetic "
                "method: finding 'pointers' to the resurrection in both nature and culture. The "
                "natural world's cycles of death and renewal testify to the possibility of "
                "resurrection."
            ),
            "context_chirho": (
                "The phoenix myth was widely known in the Roman world and was used by Clement as "
                "a cultural point of contact — similar to Paul quoting pagan poets in Acts 17:28. "
                "The argument from nature (seasons, seeds) echoes Paul's own resurrection "
                "argument in 1 Corinthians 15:35-44. Clement draws on every available resource "
                "to make the resurrection plausible to his audience."
            ),
            "relevance_chirho": (
                "Models a missional apologetic that finds points of contact in the surrounding "
                "culture. Just as Paul cited Greek poets, Clement cited a Roman legend. This "
                "principle — finding 'bridges' in culture that point to Gospel truth — is "
                "essential for modern apologetics. Nature itself testifies to the pattern of "
                "death and new life: seeds, seasons, caterpillars becoming butterflies. These "
                "are not 'proofs' of resurrection but they make it culturally conceivable."
            ),
            "scripture_chirho": ["1 Corinthians 15:35-44", "John 12:24", "Romans 1:20", "Acts 17:28"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Clement of Rome (35-99 AD)",
            "work_chirho": "First Epistle to the Corinthians, Chapters 13-19",
            "argument_chirho": (
                "Humility and obedience to God's order are the marks of true faith. Clement "
                "extensively cites Old Testament examples of humility (Abraham, Job, Moses, "
                "David) and argues that the disorder in Corinth stems from pride and jealousy — "
                "the same sins that caused the first fall. He presents Christ Himself as the "
                "supreme example of humility (quoting what appears to be early liturgical material "
                "about Christ's self-emptying) and calls the church to follow His pattern."
            ),
            "context_chirho": (
                "The Corinthian church — which Paul had already addressed for divisions and pride "
                "(1 Corinthians 1-4) — was again in turmoil. Clement's response mirrors Paul's: "
                "the solution to church conflict is not political maneuvering but humility before "
                "God. His extensive use of Old Testament examples shows that the earliest church "
                "read the Hebrew Scriptures as authoritative and instructive."
            ),
            "relevance_chirho": (
                "Clement's emphasis on humility as the antidote to division speaks directly to "
                "modern church splits and Christian infighting. His use of Christ's example "
                "as the model for humility anticipates Philippians 2:5-8 as the church's "
                "governing principle. The world is not impressed by Christian arguments when "
                "Christians are visibly divided by pride; it is impressed when believers "
                "demonstrate the humility of Christ."
            ),
            "scripture_chirho": ["Philippians 2:3-8", "James 4:6", "1 Peter 5:5-6", "Matthew 23:12"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
        {
            "father_chirho": "Clement of Rome (35-99 AD)",
            "work_chirho": "First Epistle to the Corinthians, Chapters 5-6",
            "argument_chirho": (
                "Peter and Paul as 'pillars' who endured persecution to the point of death, "
                "providing the ultimate testimony to the truth of their message. Clement writes "
                "as an eyewitness to the apostolic generation: 'Let us set before our eyes the "
                "illustrious apostles. Peter, through unjust jealousy, endured not one or two "
                "but many labors, and having borne his testimony went to the place of glory due "
                "to him. Paul also... bore testimony before the rulers... and so departed from "
                "the world.' These are among the earliest references to the martyrdoms of Peter "
                "and Paul."
            ),
            "context_chirho": (
                "Clement writes about Peter and Paul's martyrdoms as recent events known to his "
                "audience. He connects their suffering to the broader pattern of 'jealousy' "
                "causing persecution — the same jealousy now dividing the Corinthian church. "
                "The apostles' willingness to die is held up as the standard of faithfulness "
                "that should shame those who divide the church over petty disputes."
            ),
            "relevance_chirho": (
                "Provides near-contemporary testimony to the martyrdoms of Peter and Paul — "
                "crucial evidence for the historical reliability of apostolic suffering. Clement's "
                "account, written circa 96 AD (within 30 years of their deaths), confirms that "
                "the apostles did not recant their testimony even under torture and execution. "
                "This is first-generation evidence that the founders of Christianity died for "
                "their claims."
            ),
            "scripture_chirho": ["2 Timothy 4:6-8", "John 21:18-19", "Acts 12:1-4", "2 Corinthians 11:23-28"],
            "weight_chirho": WEIGHT_CHIRHO,
            "category_chirho": CATEGORY_CHIRHO,
        },
    ]


def main_chirho():
    """Compile all early church fathers' apologetic texts into JSONL."""
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    builders_chirho = {
        "justin_martyr_chirho": build_justin_martyr_chirho,
        "irenaeus_chirho": build_irenaeus_chirho,
        "tertullian_chirho": build_tertullian_chirho,
        "athanasius_chirho": build_athanasius_chirho,
        "augustine_chirho": build_augustine_chirho,
        "chrysostom_chirho": build_chrysostom_chirho,
        "polycarp_chirho": build_polycarp_chirho,
        "clement_rome_chirho": build_clement_rome_chirho,
    }

    all_entries_chirho = []
    print("Compiling Early Church Fathers' Apologetic Texts")
    print("=" * 60)
    print("NOTE: All entries are SECONDARY to Scripture (2 Timothy 3:16-17).")
    print("The Bible is the final authority. Church fathers show what the")
    print("earliest Christians believed and how they defended the faith.")
    print("NOTE: Origen is deliberately excluded (heterodox teachings).")
    print("=" * 60)

    for name_chirho, builder_chirho in builders_chirho.items():
        entries_chirho = builder_chirho()
        father_label_chirho = entries_chirho[0]["father_chirho"] if entries_chirho else name_chirho
        print(f"  {father_label_chirho}: {len(entries_chirho)} entries")
        all_entries_chirho.extend(entries_chirho)

    # Write all entries to a single JSONL file
    with open(OUTPUT_FILE_CHIRHO, "w", encoding="utf-8") as f_chirho:
        for entry_chirho in all_entries_chirho:
            f_chirho.write(json.dumps(entry_chirho, ensure_ascii=False) + "\n")

    print(f"\n{'=' * 60}")
    print(f"Total entries compiled: {len(all_entries_chirho)}")
    print(f"Output file: {OUTPUT_FILE_CHIRHO}")
    print(f"{'=' * 60}")

    # Summary statistics
    fathers_count_chirho = {}
    for entry_chirho in all_entries_chirho:
        father_chirho = entry_chirho["father_chirho"]
        fathers_count_chirho[father_chirho] = fathers_count_chirho.get(father_chirho, 0) + 1

    print("\nBreakdown by father:")
    for father_chirho, count_chirho in fathers_count_chirho.items():
        print(f"  {father_chirho}: {count_chirho} entries")

    return len(all_entries_chirho)


if __name__ == "__main__":
    main_chirho()
