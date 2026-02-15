# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
compile-apologetics-articles-chirho.py
Compiles comprehensive apologetics Q&A articles into JSONL format,
covering topics complementary to our GotQuestions dataset.
Each entry: source_chirho, category_chirho, question_chirho, answer_chirho,
topic_chirho, scripture_chirho, difficulty_chirho.
"""

import json
from pathlib import Path
from collections import Counter

OUTPUT_DIR_CHIRHO = (
    Path(__file__).resolve().parent.parent.parent
    / "data-chirho" / "raw-chirho" / "apologetics-chirho"
)
OUTPUT_FILE_CHIRHO = OUTPUT_DIR_CHIRHO / "apologetics-articles-chirho.jsonl"


def build_existence_of_god_chirho() -> list[dict]:
    """Build entries for arguments for God's existence (~20 entries)."""
    return [
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the Kalam Cosmological Argument for God's existence?",
            "answer_chirho": (
                "The Kalam Cosmological Argument, popularized by philosopher William Lane Craig, "
                "is one of the most powerful arguments for God's existence. It proceeds in two simple premises: "
                "(1) Everything that begins to exist has a cause. (2) The universe began to exist. "
                "(3) Therefore, the universe has a cause. The first premise is rooted in the metaphysical "
                "intuition that something cannot come from nothing — ex nihilo nihil fit. We never observe "
                "things popping into existence uncaused. Even quantum vacuum fluctuations occur within a "
                "pre-existing quantum field governed by physical laws, so they are not truly 'from nothing.' "
                "The second premise is supported by both philosophical arguments (the impossibility of an "
                "actually infinite series of past events) and scientific evidence. The Big Bang theory, "
                "the second law of thermodynamics (the universe is running down, so it cannot have been "
                "running forever), and the Borde-Guth-Vilenkin theorem (2003) — which shows that any "
                "universe in a state of cosmic expansion cannot be past-eternal — all point to a beginning. "
                "If the universe had a cause, that cause must be outside space, time, and matter (since it "
                "created them). It must be enormously powerful, timeless, spaceless, and personal (since "
                "only a personal agent can make a free decision to create a temporal effect from an eternal "
                "state). This matches the biblical description of God: 'In the beginning God created the "
                "heavens and the earth' (Genesis 1:1). As the Psalmist declares, 'By the word of the LORD "
                "the heavens were made, and all the host of them by the breath of His mouth' (Psalm 33:6). "
                "The Kalam argument does not prove the Christian God specifically, but it establishes a "
                "personal Creator — narrowing the field dramatically and providing a foundation for further "
                "arguments about which God created the universe. Critics sometimes object that 'Who created "
                "God?' but this misunderstands the argument: only things that BEGIN to exist need a cause. "
                "God, by definition, is the uncaused, eternal first cause — the necessary ground of all "
                "contingent reality."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Genesis 1:1", "Psalm 33:6", "Romans 1:20", "Hebrews 11:3"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does the Teleological Argument (design argument) point to God?",
            "answer_chirho": (
                "The Teleological Argument reasons from the observable order, complexity, and purpose "
                "in nature to an intelligent Designer. William Paley's classic formulation (1802) noted "
                "that if you found a watch on a heath, you would infer a watchmaker because of its "
                "organized complexity — and biological organisms display far greater complexity than any "
                "watch. Modern science has only strengthened this argument. The fine-tuning of universal "
                "constants is staggering: the gravitational constant must be precise to 1 part in 10^60, "
                "the cosmological constant to 1 part in 10^120, and the ratio of electromagnetic to "
                "gravitational force to 1 in 10^40. Roger Penrose calculated the odds of the universe's "
                "low-entropy initial state at 1 in 10^(10^123). Even slight variations in these constants "
                "would render a life-permitting universe impossible — no stars, no chemistry, no life. "
                "At the biological level, a single cell contains more organized information than the "
                "Encyclopedia Britannica. DNA operates as a digital information storage system with an "
                "error-correcting code, transcription machinery, and translation apparatus. Michael Behe's "
                "concept of 'irreducible complexity' highlights molecular machines like the bacterial "
                "flagellum (a rotary motor with 40+ protein parts) that require all components to function. "
                "The multiverse hypothesis is sometimes invoked to avoid the design inference, but it is "
                "unfalsifiable and merely pushes the question back: what designed the multiverse generator? "
                "As Paul wrote, 'For since the creation of the world God's invisible qualities — his "
                "eternal power and divine nature — have been clearly seen, being understood from what has "
                "been made, so that people are without excuse' (Romans 1:20). The heavens declare the "
                "glory of God (Psalm 19:1), and modern science increasingly reveals the depth of that "
                "declaration. Design demands a designer, and the scale of cosmic and biological design "
                "demands a Designer of supreme intelligence and power."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Romans 1:20", "Psalm 19:1-4", "Isaiah 45:18", "Jeremiah 33:25"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the Moral Argument for God's existence?",
            "answer_chirho": (
                "The Moral Argument reasons that objective moral values and duties exist, and that "
                "their existence requires a transcendent moral lawgiver — God. The argument can be "
                "formulated: (1) If God does not exist, objective moral values and duties do not exist. "
                "(2) Objective moral values and duties do exist. (3) Therefore, God exists. The key "
                "question is whether morality is objective (true regardless of human opinion) or merely "
                "subjective (a matter of personal or cultural preference). Most people live as though "
                "some things are objectively wrong — torturing an innocent child for fun, the Holocaust, "
                "slavery. These are not merely culturally unpopular; they are genuinely evil. But on "
                "atheism, what grounds this conviction? If humans are merely rearranged matter produced "
                "by blind evolutionary processes, then moral feelings are just survival instincts — not "
                "objective truths. As Dostoevsky's Ivan Karamazov observed, 'If there is no God, "
                "everything is permitted.' Evolutionary explanations for moral behavior (reciprocal "
                "altruism, kin selection) explain why we FEEL certain things are right or wrong, but "
                "they cannot establish that anything IS right or wrong. The feeling that murder is wrong "
                "would be, on naturalism, no more objectively true than the feeling of vertigo — just "
                "a useful neurological response. Christianity provides a robust foundation: moral values "
                "are grounded in God's nature (He IS good — Mark 10:18), and moral duties flow from "
                "His commands. 'He has shown you, O mortal, what is good. And what does the LORD "
                "require of you? To act justly and to love mercy and to walk humbly with your God' "
                "(Micah 6:8). The moral law written on our hearts (Romans 2:14-15) points to a moral "
                "Lawgiver. C.S. Lewis developed this argument powerfully in 'Mere Christianity,' noting "
                "that our universal sense of 'oughtness' — the feeling that we SHOULD behave in certain "
                "ways — is evidence of a moral reality behind the universe, not merely a biological instinct."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Romans 2:14-15", "Micah 6:8", "Mark 10:18", "Genesis 1:27"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the Ontological Argument for God's existence?",
            "answer_chirho": (
                "The Ontological Argument, first formulated by St. Anselm of Canterbury (1078), reasons "
                "from the very concept of God to His necessary existence. Anselm defined God as 'that "
                "than which nothing greater can be conceived.' He then argued: if such a being existed "
                "only in the mind but not in reality, we could conceive of something greater — namely, "
                "the same being existing in reality. But that would contradict our definition. Therefore, "
                "the greatest conceivable being must exist in reality. The argument has been refined by "
                "Alvin Plantinga using modal logic: (1) It is possible that a maximally great being "
                "exists (a being with maximal excellence in every possible world). (2) If it is possible "
                "that such a being exists, then it exists in some possible world. (3) If it exists in "
                "some possible world, it exists in every possible world (by definition of maximal "
                "greatness). (4) If it exists in every possible world, it exists in the actual world. "
                "(5) Therefore, a maximally great being exists. The crucial premise is (1): is it even "
                "possible for such a being to exist? If the concept of a maximally great being is "
                "coherent (not self-contradictory like a 'square circle'), then the argument succeeds. "
                "Critics like Gaunilo countered with 'the greatest conceivable island,' but islands "
                "are contingent beings — they cannot have intrinsic maximal greatness the way a "
                "necessary being can. Kant objected that existence is not a 'predicate' (property), "
                "but Plantinga's modal version avoids this by speaking of possible worlds rather than "
                "existence as a property. The argument is admittedly abstract, but it demonstrates "
                "that the concept of God is not irrational — it is coherent and, if coherent, logically "
                "entails God's actual existence. As God declared to Moses, 'I AM WHO I AM' (Exodus 3:14) "
                "— the self-existent, necessary being who is the ground of all reality."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Exodus 3:14", "Psalm 14:1", "Isaiah 45:5", "Revelation 1:8"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the Argument from Consciousness for God's existence?",
            "answer_chirho": (
                "The Argument from Consciousness observes that conscious experience — the subjective, "
                "first-person awareness of what it is like to see red, taste chocolate, or feel pain — "
                "cannot be explained by purely physical processes. This is known as the 'hard problem "
                "of consciousness' (David Chalmers, 1995). Physical science describes objective, "
                "third-person properties: wavelengths, neural firings, chemical reactions. But none of "
                "these explains WHY there is subjective experience associated with brain activity. You "
                "could know everything about the physics of color perception and still not know what it "
                "is LIKE to see red unless you have experienced it. On materialistic atheism, the "
                "universe consists entirely of matter and energy governed by impersonal physical laws. "
                "But consciousness is not physical — it has no mass, no charge, no spatial location. "
                "How does subjective experience arise from objective matter? Materialists have proposed "
                "various theories: identity theory (consciousness IS brain activity), functionalism "
                "(consciousness is computational), emergentism (consciousness 'emerges' from complexity). "
                "But none actually explains the transition from the objective to the subjective. Saying "
                "consciousness 'emerges' from matter is a label, not an explanation — it is equivalent "
                "to saying 'it just happens.' J.P. Moreland argues that consciousness fits naturally "
                "within a theistic worldview: if the fundamental reality is a conscious Mind (God), then "
                "the existence of finite conscious minds is expected. If the fundamental reality is "
                "unconscious matter, the existence of consciousness is a brute, inexplicable mystery. "
                "Genesis 2:7 describes God breathing life into Adam — consciousness is a gift from a "
                "conscious Creator, not an accident of unconscious matter. 'The spirit of man is the "
                "lamp of the LORD, searching all his innermost parts' (Proverbs 20:27). Consciousness "
                "reflects the image of God in humanity (Genesis 1:27)."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Genesis 1:27", "Genesis 2:7", "Proverbs 20:27", "Psalm 139:13-14"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is C.S. Lewis's Argument from Reason?",
            "answer_chirho": (
                "C.S. Lewis's Argument from Reason, developed in 'Miracles' (1947, revised 1960), "
                "contends that naturalism (the view that nature is all that exists) is self-defeating "
                "because it undermines the reliability of human reasoning. The argument proceeds: if "
                "naturalism is true, then all our thoughts are ultimately the product of non-rational "
                "causes — blind physical processes, chemical reactions, evolutionary pressures. But if "
                "our thoughts are entirely determined by non-rational causes, we have no reason to trust "
                "them as reliable guides to truth. A thought caused entirely by irrational physical "
                "processes is no more likely to be true than the sound of wind through trees is likely "
                "to produce a meaningful sentence. As Lewis wrote: 'If the solar system was brought "
                "about by an accidental collocation of atoms, why should we trust our brains, which are "
                "also accidental collocations of atoms?' Darwin himself expressed this worry: 'Would "
                "anyone trust the convictions of a monkey's mind, if there are any convictions in such "
                "a mind?' Natural selection selects for survival, not truth. A belief might aid survival "
                "while being completely false (Plantinga's evolutionary argument against naturalism "
                "formalizes this). If naturalism is true, we cannot trust our cognitive faculties — "
                "including the reasoning that led us to accept naturalism. Therefore, naturalism "
                "is self-defeating. Theism, by contrast, provides a sound basis for trusting reason: "
                "we are made in the image of a rational God (Genesis 1:27) and our minds are designed "
                "to apprehend truth. 'Come now, let us reason together, says the LORD' (Isaiah 1:18). "
                "God is the Logos — the divine Reason (John 1:1) — and our capacity for rational "
                "thought reflects His nature. The very act of rational argument presupposes a rational "
                "Creator."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Isaiah 1:18", "John 1:1", "Genesis 1:27", "1 Corinthians 1:25"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is C.S. Lewis's Argument from Desire?",
            "answer_chirho": (
                "C.S. Lewis observed that every natural desire corresponds to a real object that can "
                "satisfy it. Hunger corresponds to food. Thirst corresponds to water. Sexual desire "
                "corresponds to sexual fulfillment. Tiredness corresponds to sleep. In every case, "
                "the existence of the desire points to the existence of its satisfaction. Lewis then "
                "noted that human beings have an innate, deep longing that nothing in this world "
                "satisfies — a longing for something beyond, something transcendent. We experience "
                "it as nostalgia, wanderlust, the bittersweet ache at a beautiful sunset, the "
                "restlessness that persists even when all earthly needs are met. Augustine captured "
                "it: 'You have made us for yourself, O Lord, and our hearts are restless until they "
                "rest in you.' Lewis argued: if every natural desire has a corresponding real "
                "fulfillment, and we have a desire that nothing in this world fulfills, then there "
                "must exist something beyond this world that can fulfill it. That 'something' is God "
                "and the eternal life He offers. As Lewis wrote in 'Mere Christianity': 'If I find "
                "in myself a desire which no experience in this world can satisfy, the most probable "
                "explanation is that I was made for another world.' Ecclesiastes 3:11 says God 'has "
                "set eternity in the human heart.' This innate yearning for the transcendent is not "
                "evidence of delusion but of design — God has wired us to seek Him. The objection "
                "that this desire is merely evolutionary does not hold: evolution explains desires "
                "for survival (food, reproduction), not desires for transcendence that have no "
                "survival value. The universal human longing for 'something more' is a signpost "
                "pointing to the God who made us for Himself (Acts 17:26-27)."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Ecclesiastes 3:11", "Acts 17:26-27", "Psalm 42:1-2", "Philippians 3:20"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the Argument from Contingency for God's existence?",
            "answer_chirho": (
                "The Argument from Contingency, associated with Gottfried Wilhelm Leibniz, asks "
                "the most fundamental question in philosophy: 'Why is there something rather than "
                "nothing?' Everything we observe in the universe is contingent — it exists but might "
                "not have existed. You did not have to exist. The earth did not have to exist. The "
                "universe itself did not have to exist. Contingent things require an explanation for "
                "their existence outside themselves. A contingent being is explained by another being, "
                "but you cannot have an infinite chain of contingent beings each explained by another "
                "— this leads to an infinite regress that explains nothing (like an infinite chain of "
                "train cars with no engine). Therefore, there must be a Necessary Being — a being "
                "that exists by the necessity of its own nature, that cannot fail to exist, and that "
                "grounds the existence of everything else. This Necessary Being must be self-existent, "
                "eternal, uncaused, and the ultimate explanation for all contingent reality. This is "
                "precisely the God of the Bible. When Moses asked God His name, God replied 'I AM "
                "WHO I AM' (Exodus 3:14) — the self-existent One whose essence is existence itself. "
                "Paul declares, 'For from him and through him and for him are all things' (Romans "
                "11:36). God is not one more contingent thing in the universe needing explanation; He "
                "is the necessary ground of all existence. The atheist must either accept an infinite "
                "regress of contingent causes (which explains nothing), claim the universe itself is "
                "necessary (but physics shows the universe is contingent — it could have had different "
                "laws, different constants, or not existed at all), or accept a Necessary Being. "
                "Leibniz's argument reveals that the very existence of anything at all points to a "
                "self-existent Creator — 'In him we live and move and have our being' (Acts 17:28)."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Exodus 3:14", "Romans 11:36", "Acts 17:28", "Colossians 1:17"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How do transformed lives serve as evidence for God's existence?",
            "answer_chirho": (
                "While personal experience alone cannot prove God's existence to skeptics, the "
                "consistent pattern of radical life transformation through encounter with Christ "
                "constitutes significant cumulative evidence. Throughout history and across every "
                "culture, people have testified that encountering Jesus Christ has delivered them "
                "from addictions, healed broken relationships, replaced despair with hope, and "
                "fundamentally changed their character. The apostle Paul was a violent persecutor "
                "of Christians who became Christianity's greatest missionary after encountering "
                "the risen Christ (Acts 9). Augustine was a man enslaved to lust and pride who "
                "became one of history's greatest theologians. John Newton was a slave trader who, "
                "after conversion, wrote 'Amazing Grace' and fought against slavery. In modern "
                "times, Nicky Cruz was a violent gang leader in New York whose life was completely "
                "transformed through faith in Christ. The consistency of this pattern across cultures, "
                "centuries, and circumstances is remarkable. Paul described it: 'Therefore, if anyone "
                "is in Christ, the new creation has come: The old has gone, the new is here!' (2 "
                "Corinthians 5:17). Jesus said, 'You will know them by their fruits' (Matthew 7:16). "
                "The 'fruit of the Spirit' — love, joy, peace, patience, kindness, goodness, "
                "faithfulness, gentleness, self-control (Galatians 5:22-23) — manifests consistently "
                "in genuine Christian conversion. Critics claim this is merely psychological change "
                "achievable through any belief system, but no other belief system produces the same "
                "pattern of transformation with the same consistency across diverse populations. "
                "Moreover, these transformations often occur instantaneously and against the person's "
                "own efforts and expectations, suggesting an external agent — the Holy Spirit — "
                "rather than mere willpower or self-improvement."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["2 Corinthians 5:17", "Galatians 5:22-23", "Acts 9:1-22", "Matthew 7:16"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is presuppositional apologetics and the 'impossibility of the contrary'?",
            "answer_chirho": (
                "Presuppositional apologetics, developed by Cornelius Van Til and popularized by "
                "Greg Bahnsen, argues that the existence of the Christian God is the necessary "
                "precondition for all intelligible experience, logic, morality, and science. Rather "
                "than treating God's existence as a conclusion to be proven, presuppositionalism "
                "shows that God's existence must be assumed (presupposed) for anything to make sense "
                "at all. The argument proceeds by 'the impossibility of the contrary': without the "
                "Christian God, you cannot account for the laws of logic (they are universal, "
                "immaterial, and invariant — how do they exist in a purely material universe?), "
                "the uniformity of nature (why should the future resemble the past, enabling science, "
                "unless a faithful God sustains the created order? — Jeremiah 33:25-26), objective "
                "morality (without a transcendent standard, moral claims are mere preferences), or "
                "the reliability of human reasoning (as C.S. Lewis argued, if our thoughts are "
                "determined by irrational physical causes, we have no basis for trusting them). "
                "In the famous 1985 debate between Bahnsen and atheist Gordon Stein, Bahnsen "
                "challenged Stein to account for the laws of logic on atheism. Stein could not. "
                "The point is not merely that atheism fails to prove these things, but that atheism "
                "CANNOT IN PRINCIPLE account for them — they are features of a universe created and "
                "sustained by the rational, moral, faithful God of the Bible. 'The fear of the LORD "
                "is the beginning of knowledge' (Proverbs 1:7) is not just a pious platitude — it "
                "is an epistemological claim. All knowledge presupposes God because God is the "
                "precondition for the intelligibility of everything. When the atheist uses logic, "
                "science, and morality to argue against God, he is standing on Christian ground — "
                "borrowing capital from the theistic worldview while denying its source. 'In him "
                "are hidden all the treasures of wisdom and knowledge' (Colossians 2:3)."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Proverbs 1:7", "Colossians 2:3", "Jeremiah 33:25-26", "Romans 1:18-21"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Does the existence of mathematics point to God?",
            "answer_chirho": (
                "The existence and applicability of mathematics presents a profound puzzle for "
                "atheism. Mathematician Eugene Wigner famously described 'the unreasonable "
                "effectiveness of mathematics' — why should abstract mathematical truths, discovered "
                "by the human mind, perfectly describe the physical universe? Mathematical truths "
                "are necessary, universal, immaterial, and eternal. 2+2=4 was true before any human "
                "existed and would remain true if all humans perished. These are not physical objects — "
                "the number 7 has no mass, no location, no color. Yet the physical universe is "
                "structured according to elegant mathematical laws. On materialistic atheism, only "
                "physical things exist. If that is true, where do mathematical objects exist? They "
                "are not located in space. They did not evolve. They are not made of matter. Yet "
                "they are real and we can know them. The theistic answer is elegant: mathematical "
                "truths exist as thoughts in the mind of God. They describe the universe because "
                "God structured the universe according to mathematical principles. 'But you have "
                "arranged all things by measure and number and weight' (Wisdom 11:20). The remarkable "
                "correspondence between mathematical structures and physical reality — what physicist "
                "Paul Dirac called 'the most beautiful thing' — is expected if a rational Mind "
                "designed both our mathematical intuitions and the physical world they describe. "
                "As Galileo observed, the book of nature is written in the language of mathematics. "
                "The God who 'counts the number of the stars' (Psalm 147:4) and 'measured the waters "
                "in the hollow of his hand, and marked off the heavens by the span' (Isaiah 40:12) "
                "is the ultimate Mathematician whose mind grounds all mathematical reality."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Psalm 147:4", "Isaiah 40:12", "Job 38:4-7", "Proverbs 3:19-20"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does the existence of information in DNA point to an intelligent Creator?",
            "answer_chirho": (
                "DNA contains digital information encoded in a four-letter chemical alphabet "
                "(A, T, G, C). The human genome contains approximately 3.2 billion base pairs — "
                "equivalent to about 800 megabytes of data. This information specifies the "
                "construction of over 20,000 proteins, each precisely folded into three-dimensional "
                "shapes that perform specific functions. This is not merely a matter of chemistry — "
                "it is genuine information: a sequence of symbols whose arrangement, not chemical "
                "properties, determines meaning. As information theorist Hubert Yockey noted, "
                "'The sequence hypothesis applies to the protein and the genetic text as well as "
                "to written language and therefore the treatment is mathematically identical.' "
                "In our uniform experience, specified complex information always originates from "
                "an intelligent mind. Books come from authors. Computer programs come from "
                "programmers. Blueprints come from architects. We never observe random processes "
                "producing functional information. Stephen Meyer's 'Signature in the Cell' (2009) "
                "argues that the origin of biological information is best explained by intelligent "
                "design. The DNA 'code' is not a metaphor — it literally is a code, with codons "
                "(three-letter words), start signals, stop signals, error-correction mechanisms, "
                "and a translation apparatus (the ribosome) that reads the code and builds "
                "proteins accordingly. The information in DNA is irreducible to chemistry, just "
                "as the information in a book is irreducible to the properties of ink and paper. "
                "'For you formed my inward parts; you knitted me together in my mother's womb. "
                "I praise you, for I am fearfully and wonderfully made' (Psalm 139:13-14). The "
                "God who spoke the universe into existence (Genesis 1:3) encoded the language "
                "of life into every cell."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Psalm 139:13-14", "Genesis 1:3", "Romans 1:20", "Jeremiah 1:5"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the Cumulative Case argument for God's existence?",
            "answer_chirho": (
                "The Cumulative Case argument holds that while no single argument for God's existence "
                "may be individually decisive, the combined weight of multiple independent lines of "
                "evidence creates an overwhelming case. Consider the convergence: the universe had a "
                "beginning (cosmological argument), it is finely tuned for life (teleological argument), "
                "objective moral values exist (moral argument), consciousness exists in a physical "
                "world (argument from consciousness), reason itself presupposes a rational ground "
                "(argument from reason), human beings have an unfulfillable longing for transcendence "
                "(argument from desire), contingent reality requires a necessary being (argument from "
                "contingency), and the applicability of mathematics to the physical world suggests a "
                "rational mind behind both (argument from mathematics). Each of these points to the "
                "same conclusion: a personal, powerful, rational, moral, necessary, transcendent "
                "Creator. This is precisely the God described in Scripture. The probability that all "
                "these independent lines of evidence would converge on the same conclusion by chance "
                "is vanishingly small. Richard Swinburne, in 'The Existence of God,' uses Bayesian "
                "probability theory to show that the cumulative evidence makes God's existence more "
                "probable than not. Basil Mitchell compared it to a courtroom case: no single piece "
                "of evidence convicts, but the total weight of circumstantial evidence is conclusive. "
                "Paul appeals to this cumulative approach in Romans 1:19-20, suggesting that multiple "
                "features of creation collectively reveal God's nature. 'For since the creation of "
                "the world God's invisible qualities — his eternal power and divine nature — have "
                "been clearly seen, being understood from what has been made.' The case for God "
                "is not a single thread but a cable of many strands, each reinforcing the others."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Romans 1:19-20", "Psalm 19:1-6", "Acts 14:17", "Acts 17:24-28"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How do we know God is personal rather than an impersonal force?",
            "answer_chirho": (
                "Several lines of reasoning indicate that God is personal — a being with mind, will, "
                "and relational capacity — rather than an impersonal force or energy. First, the "
                "cosmological argument concludes that the cause of the universe must be personal. "
                "An impersonal cause, given sufficient conditions, produces its effect necessarily "
                "and eternally. If the cause of the universe were impersonal, the universe would be "
                "eternal (coexistent with its cause). Since the universe began a finite time ago, "
                "the cause must have freely CHOSEN to create — and choice requires personhood. "
                "Second, the moral argument points to a personal moral lawgiver. Impersonal forces "
                "cannot issue moral commands or care about right and wrong. Objective moral duties "
                "imply a personal God who commands and to whom we are accountable. Third, the "
                "existence of persons is better explained by a personal source. Personhood — "
                "consciousness, rationality, will, emotions, relational capacity — is the highest "
                "form of reality we know. It is more reasonable that persons come from a personal "
                "source than that personal beings somehow emerged from impersonal matter and energy. "
                "The greater does not come from the lesser without a greater cause. Fourth, "
                "religious experience across cultures consistently involves encounter with a personal "
                "being, not absorption into an impersonal force. Scripture reveals God as supremely "
                "personal: He speaks (Genesis 1:3), loves (John 3:16), grieves (Genesis 6:6), shows "
                "anger at injustice (Psalm 7:11), makes promises (Genesis 12:1-3), and enters into "
                "covenant relationship with His people. The incarnation of Christ is the ultimate "
                "demonstration: 'The Word became flesh and dwelt among us' (John 1:14). God is not "
                "a force to be manipulated but a Person to be known."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["John 1:14", "John 3:16", "Genesis 1:3", "Jeremiah 29:13"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Is atheism a belief or a lack of belief?",
            "answer_chirho": (
                "Modern atheists often claim that atheism is merely 'a lack of belief in God' rather "
                "than a positive claim, thereby shifting the burden of proof entirely to the theist. "
                "However, this redefinition is philosophically problematic. Historically, atheism has "
                "been understood as the positive assertion that God does not exist — a claim that "
                "carries its own burden of proof. The Stanford Encyclopedia of Philosophy defines "
                "atheism as 'the negation of theism, the denial that there is a God.' When an atheist "
                "says 'There is no God,' they are making a knowledge claim about ultimate reality "
                "that requires justification. A baby or a rock also 'lacks belief in God,' but no "
                "one calls them atheists in any meaningful sense. The 'lack of belief' definition "
                "confuses psychological states (not thinking about God) with philosophical positions "
                "(claiming God does not exist). In practice, most prominent atheists go far beyond "
                "mere 'lack of belief': Dawkins argues religion is a 'virus of the mind,' Hitchens "
                "claimed 'religion poisons everything,' and Harris advocates the 'end of faith.' "
                "These are robust positive claims, not mere absence of belief. The Christian response "
                "is twofold. First, there are powerful positive arguments for God's existence "
                "(cosmological, teleological, moral, etc.). Second, Romans 1:19-20 teaches that God's "
                "existence is evident to all through creation — atheism is not a neutral starting "
                "point but an active suppression of available evidence. 'The fool says in his heart, "
                "There is no God' (Psalm 14:1). Notice: the fool says this 'in his heart,' not 'in "
                "his mind' — atheism is ultimately a moral and volitional posture, not merely an "
                "intellectual conclusion. Everyone knows God exists; the question is whether they "
                "will acknowledge what they know (Romans 1:21)."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Psalm 14:1", "Romans 1:19-21", "Psalm 19:1", "James 2:19"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Can you prove God exists with absolute certainty?",
            "answer_chirho": (
                "The demand for 'absolute certainty' or 'scientific proof' for God's existence "
                "reflects a misunderstanding of both proof and knowledge. Very few things in life "
                "meet the standard of absolute mathematical certainty — not even the findings of "
                "science. Science works by inference to the best explanation, not by deductive proof. "
                "We accept historical events (Caesar crossing the Rubicon), scientific theories "
                "(general relativity), and other minds (that other people are conscious) on the "
                "basis of evidence that falls short of absolute certainty. The appropriate question "
                "is not 'Can you prove God with mathematical certainty?' but 'Is belief in God "
                "supported by the best available evidence?' And the answer is overwhelmingly yes. "
                "The cosmological, teleological, moral, and other arguments collectively provide "
                "strong evidence. The historical evidence for the resurrection of Jesus is powerful. "
                "The reliability of Scripture is well-attested. Personal experience of God, while "
                "not independently verifiable, is meaningful evidence for the individual. Moreover, "
                "God has chosen to make Himself known through means that require faith — not blind "
                "faith, but trusting faith based on evidence. 'Now faith is the substance of things "
                "hoped for, the evidence of things not seen' (Hebrews 11:1). Note: faith IS evidence "
                "— it is not the absence of evidence. Jesus said, 'Blessed are those who have not "
                "seen and yet have believed' (John 20:29). God desires a relationship of trust, not "
                "mere intellectual acknowledgment. Even demons believe that God exists (James 2:19). "
                "The goal is not merely to know THAT God exists but to KNOW God personally. 'You "
                "will seek me and find me when you seek me with all your heart' (Jeremiah 29:13). "
                "God promises that honest seekers will find Him."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Hebrews 11:1", "John 20:29", "Jeremiah 29:13", "James 2:19"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "If God exists, why doesn't He make His existence more obvious?",
            "answer_chirho": (
                "This question assumes God is hidden, but Scripture asserts the opposite: God has "
                "made His existence abundantly clear. 'The heavens declare the glory of God; the "
                "skies proclaim the work of his hands' (Psalm 19:1). 'For since the creation of "
                "the world God's invisible qualities — his eternal power and divine nature — have "
                "been clearly seen, being understood from what has been made, so that people are "
                "without excuse' (Romans 1:20). The problem is not insufficient evidence but "
                "suppressed evidence (Romans 1:18). That said, God does not overwhelm us with His "
                "presence for several reasons. First, God values free love, and coerced love is not "
                "love. If God appeared with undeniable, overwhelming force, compliance would be "
                "compulsory. God seeks hearts that freely choose Him, not prisoners who have no "
                "option. Second, God has provided sufficient evidence for those who genuinely seek. "
                "'You will seek me and find me when you seek me with all your heart' (Jeremiah 29:13). "
                "Third, God's partial hiddenness serves a soul-making purpose. The journey of faith "
                "— seeking, wrestling, trusting — develops character that passive certainty never "
                "could. Fourth, even when God HAS revealed Himself dramatically, people often still "
                "resist. Israel saw the plagues of Egypt, the parting of the Red Sea, manna from "
                "heaven — and still built a golden calf (Exodus 32). The rich man in Jesus' parable "
                "was told: 'If they do not listen to Moses and the Prophets, they will not be "
                "convinced even if someone rises from the dead' (Luke 16:31). The evidence is "
                "sufficient; what is often lacking is the willingness to follow where it leads. "
                "Blaise Pascal put it well: 'There is enough light for those who desire to see, "
                "and enough darkness for those of a contrary disposition.'"
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Psalm 19:1", "Romans 1:18-20", "Jeremiah 29:13", "Luke 16:31"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Who created God? Doesn't everything need a cause?",
            "answer_chirho": (
                "The question 'Who created God?' is perhaps the most common objection raised against "
                "theistic arguments, but it rests on a misunderstanding. The cosmological argument "
                "does NOT claim 'everything has a cause.' It claims 'everything that BEGINS TO EXIST "
                "has a cause.' God, by definition, did not begin to exist — He is eternal, the "
                "uncaused first cause. This is not special pleading; it is a logical necessity. "
                "Any causal chain must terminate in something uncaused, or nothing would exist at "
                "all. An infinite regress of causes is impossible because you would never arrive at "
                "the present moment — it would be like trying to count down from negative infinity. "
                "The question is not WHETHER there is an uncaused first cause, but WHAT it is. The "
                "atheist who asks 'Who created God?' must face the same question about whatever they "
                "propose as ultimate reality. If they say the universe is self-existent, they are "
                "attributing to the universe what theists attribute to God. But the universe shows "
                "every sign of contingency (it began, it could have been different, it is running "
                "down). God, as a necessary being, exists by the necessity of His own nature. His "
                "non-existence is impossible, just as the non-existence of the number 7 is impossible. "
                "'Before the mountains were brought forth, or ever you had formed the earth and the "
                "world, from everlasting to everlasting you are God' (Psalm 90:2). God IS existence "
                "itself — 'I AM WHO I AM' (Exodus 3:14). Asking 'Who created the uncreated Creator?' "
                "is like asking 'Who is the bachelor's wife?' — it is a category error. The very "
                "concept of God is the concept of an eternal, self-existent being who depends on "
                "nothing else for His existence."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Psalm 90:2", "Exodus 3:14", "Revelation 1:8", "Isaiah 44:6"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Can science disprove God?",
            "answer_chirho": (
                "Science cannot disprove God because science and God operate in different categories. "
                "Science studies the natural world through observation, experimentation, and "
                "measurement of physical phenomena. God, by definition, is supernatural — beyond "
                "the natural order. Asking science to disprove God is like asking a metal detector "
                "to disprove the existence of plastic. The tool is not designed to detect the thing "
                "in question. This is not a weakness of science but a recognition of its proper "
                "scope. Science answers 'how' questions (how do stars form? how does DNA replicate?). "
                "Theology and philosophy answer 'why' questions (why does anything exist? why is "
                "there order? what is the meaning of life?). These are complementary, not competing. "
                "In fact, science arose in a Christian context precisely because the biblical worldview "
                "provides the necessary presuppositions for science: a rational Creator made an orderly "
                "universe that human minds (made in God's image) can comprehend. Many of science's "
                "greatest pioneers were devout Christians: Newton, Kepler, Faraday, Maxwell, Pasteur, "
                "and many modern scientists. A 2009 Pew survey found that 51% of American scientists "
                "believe in God or a higher power. The 'conflict thesis' — that science and religion "
                "are inherently opposed — has been rejected by historians of science (see David "
                "Lindberg and Ronald Numbers, 'God and Nature'). 'The heavens declare the glory of "
                "God' (Psalm 19:1) — science, rightly understood, is the study of God's creation. "
                "As Johannes Kepler said, science is 'thinking God's thoughts after Him.' Every "
                "scientific discovery reveals more of the Creator's wisdom and power."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Psalm 19:1", "Proverbs 25:2", "Romans 1:20", "Job 38:1-7"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does the existence of beauty point to God?",
            "answer_chirho": (
                "The existence of beauty — aesthetic experience that moves us deeply — presents "
                "another puzzle for atheistic materialism. On a purely naturalistic account, beauty "
                "should not exist. Evolution selects for survival, not for the ability to be moved "
                "by a sunset, a symphony, or a mountain vista. The response of awe we feel before "
                "natural beauty has no obvious survival value. Why should chemical machines made of "
                "carbon be capable of aesthetic experience at all? Why should the universe be "
                "beautiful rather than merely functional? The equations of physics are not merely "
                "accurate — they are elegant. The spiral of a nautilus shell follows the Fibonacci "
                "sequence. Snowflakes form exquisite hexagonal symmetry. Galaxies spiral in "
                "breathtaking formations. None of this beauty is 'necessary' for the universe to "
                "function. But it is exactly what we would expect if the universe was created by "
                "a God who delights in beauty. 'He has made everything beautiful in its time' "
                "(Ecclesiastes 3:11). The Psalms are saturated with aesthetic appreciation of "
                "creation: 'How many are your works, LORD! In wisdom you made them all; the earth "
                "is full of your creatures' (Psalm 104:24). God is described as beautiful: 'One "
                "thing I ask from the LORD, this only do I seek: that I may dwell in the house of "
                "the LORD all the days of my life, to gaze on the beauty of the LORD' (Psalm 27:4). "
                "Beauty is a reflection of God's nature. Our capacity to perceive and be moved by "
                "beauty is part of the image of God in us. The artist's creative impulse mirrors "
                "the Creator's. When we encounter beauty, we are encountering a trace of the One "
                "who is Beauty itself — the ultimate aesthetic experience awaiting us in His presence."
            ),
            "topic_chirho": "existence_of_god",
            "scripture_chirho": ["Ecclesiastes 3:11", "Psalm 27:4", "Psalm 104:24", "Psalm 50:2"],
            "difficulty_chirho": "basic",
        },
    ]


def build_problem_of_evil_chirho() -> list[dict]:
    """Build entries for problem of evil and suffering (~15 entries)."""
    return [
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why does God allow suffering?",
            "answer_chirho": (
                "The question of suffering is perhaps the most emotionally powerful objection to "
                "Christian faith, and it deserves a thoughtful, compassionate answer. First, "
                "Christianity acknowledges that suffering is real and grievous — the Bible never "
                "minimizes pain. Jesus himself wept at the tomb of Lazarus (John 11:35) even though "
                "He was about to raise him from the dead. God is not indifferent to our pain. "
                "Second, much suffering results from human free will. God created humans with "
                "genuine moral freedom — the ability to choose good or evil. Without this freedom, "
                "love would be impossible (love must be freely given). But freedom necessarily "
                "entails the possibility of its misuse, and much of the world's suffering — war, "
                "murder, theft, abuse — results from human choices, not divine indifference. Third, "
                "natural suffering (earthquakes, disease, death) entered the world through the Fall. "
                "When Adam sinned, creation itself was subjected to futility (Romans 8:20-22). "
                "The world as it is now is not the world as God originally made it or intends it "
                "to be. Fourth, God uses suffering redemptively. 'We know that in all things God "
                "works for the good of those who love him' (Romans 8:28). Suffering produces "
                "character, endurance, and hope (Romans 5:3-5). It can draw us closer to God and "
                "make us more compassionate toward others. Fifth, the ultimate answer to suffering "
                "is the Cross. God did not remain distant from our pain — He entered it. Jesus "
                "suffered the worst evil imaginable: the innocent Son of God tortured and killed. "
                "Through the Cross, God defeated evil, sin, and death, and promises a future where "
                "'He will wipe every tear from their eyes. There will be no more death or mourning "
                "or crying or pain' (Revelation 21:4). Present suffering is temporary; God's "
                "restoration is eternal."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Romans 8:28", "Romans 5:3-5", "Romans 8:20-22", "Revelation 21:4", "John 11:35"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is Alvin Plantinga's Free Will Defense?",
            "answer_chirho": (
                "Alvin Plantinga's Free Will Defense (1974) is widely recognized — even by atheist "
                "philosophers — as having decisively resolved the logical problem of evil. The logical "
                "problem claims there is a logical contradiction between these two propositions: "
                "(1) An omnipotent, omniscient, wholly good God exists. (2) Evil exists. Plantinga "
                "showed there is no contradiction, because it is logically possible that: God could "
                "not create a world containing free creatures who always freely choose good. If God "
                "creates beings with genuine libertarian free will, it is possible that in ANY world "
                "God creates, some of those beings will freely choose evil. This is called "
                "'transworld depravity.' Plantinga's argument does not claim to know WHY God allows "
                "evil — it only needs to show that it is LOGICALLY POSSIBLE for God to have morally "
                "sufficient reasons. And it succeeds. Even J.L. Mackie, the atheist philosopher "
                "who formulated the logical problem of evil, conceded: 'Since this defense is "
                "formally possible, and its principle involves no real abandonment of our ordinary "
                "view of the opposition between good and evil, we can concede that the problem of "
                "evil does not, after all, show that the central doctrines of theism are logically "
                "inconsistent with one another.' A world with free beings who can love, create, "
                "and relate — even with the risk of evil — may be more valuable than a world of "
                "preprogrammed robots who can do none of these things. 'I have set before you life "
                "and death, blessings and curses. Now choose life' (Deuteronomy 30:19). God's "
                "gift of freedom, though costly, makes genuine love possible — and love is the "
                "highest good (1 Corinthians 13:13)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Deuteronomy 30:19", "1 Corinthians 13:13", "Joshua 24:15", "Genesis 2:16-17"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does suffering produce character and draw us closer to God (soul-making theodicy)?",
            "answer_chirho": (
                "The soul-making theodicy, associated with Irenaeus (2nd century) and developed by "
                "John Hick (1966), argues that God permits suffering because it is essential for "
                "the development of mature, virtuous character. A world without challenges would "
                "produce no courage, no compassion, no perseverance, no faith. Just as muscles "
                "grow through resistance and diamonds form under pressure, moral and spiritual "
                "character develops through trials. Paul articulates this explicitly: 'We also "
                "glory in our sufferings, because we know that suffering produces perseverance; "
                "perseverance, character; and character, hope. And hope does not put us to shame, "
                "because God's love has been poured out into our hearts through the Holy Spirit' "
                "(Romans 5:3-5). James echoes: 'Consider it pure joy, my brothers and sisters, "
                "whenever you face trials of many kinds, because you know that the testing of your "
                "faith produces perseverance. Let perseverance finish its work so that you may be "
                "mature and complete, not lacking anything' (James 1:2-4). Peter adds: 'These "
                "trials have come so that the proven genuineness of your faith — of greater worth "
                "than gold, which perishes even though refined by fire — may result in praise, "
                "glory and honor when Jesus Christ is revealed' (1 Peter 1:6-7). This does not "
                "mean God causes all suffering or that every instance of suffering has a clear "
                "purpose we can identify. But it means that God, in His sovereignty, can work "
                "through suffering to achieve goods that could not be achieved otherwise. The "
                "greatest example is Christ Himself: 'Although he was a son, he learned obedience "
                "from what he suffered' (Hebrews 5:8). If even the Son of God was perfected through "
                "suffering, how much more can God use our suffering for our ultimate good?"
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Romans 5:3-5", "James 1:2-4", "1 Peter 1:6-7", "Hebrews 5:8"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Has the logical problem of evil been solved?",
            "answer_chirho": (
                "Yes. The logical problem of evil — the claim that the existence of God and the "
                "existence of evil are LOGICALLY INCOMPATIBLE — is widely acknowledged by philosophers, "
                "including atheist philosophers, to have been solved. Alvin Plantinga's Free Will "
                "Defense (1974) demonstrated that there is no logical contradiction between an "
                "omnipotent, omniscient, wholly good God and the existence of evil. The key insight "
                "is that omnipotence does not include the ability to do logically impossible things. "
                "God cannot create a married bachelor or a square circle. Similarly, it may be "
                "logically impossible for God to create a world with free creatures who never choose "
                "evil. If every possible creature would freely choose evil in at least one "
                "circumstance (transworld depravity), then any world God creates with free beings "
                "will contain some evil. Even J.L. Mackie and William Rowe — leading atheist "
                "philosophers who pressed the problem of evil — acknowledged that the logical "
                "version fails. Philosopher William Alston wrote that 'it is now acknowledged on "
                "(almost) all sides that the logical argument from evil is bankrupt.' The "
                "discussion has shifted to the evidential problem of evil: the claim that the "
                "AMOUNT or DISTRIBUTION of evil makes God's existence improbable (not impossible). "
                "But this is a much weaker claim and faces significant challenges. We are not in "
                "a position to judge whether God could have morally sufficient reasons for permitting "
                "specific evils — our knowledge of the consequences of events is extremely limited. "
                "As God said to Isaiah: 'For my thoughts are not your thoughts, neither are your "
                "ways my ways... As the heavens are higher than the earth, so are my ways higher "
                "than your ways and my thoughts than your thoughts' (Isaiah 55:8-9)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Isaiah 55:8-9", "Romans 11:33-34", "Job 38:1-4", "Deuteronomy 29:29"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How should Christians respond to the evidential problem of evil (William Rowe's argument)?",
            "answer_chirho": (
                "William Rowe's evidential argument (1979) claims that while the existence of evil "
                "is not logically incompatible with God, the sheer amount and gratuitous nature of "
                "evil makes God's existence improbable. Rowe points to instances of apparently "
                "pointless suffering — a fawn dying slowly in a forest fire — and argues that a "
                "good God would prevent such suffering if it served no greater purpose. Christians "
                "can respond on multiple levels. First, our inability to see the purpose of specific "
                "suffering does not mean there is no purpose. This is the 'noseeum' fallacy: just "
                "because we cannot see a reason does not mean no reason exists. Our cognitive "
                "limitations are severe. We cannot foresee the ripple effects of events across "
                "history. Stephen Wykstra calls this the 'CORNEA' principle — we would not expect "
                "to perceive God's reasons even if they existed, given the vast gulf between divine "
                "and human understanding. Second, there are many well-documented cases where "
                "apparently senseless suffering led to enormous good that could not have been "
                "foreseen at the time. Joseph told his brothers: 'You intended to harm me, but "
                "God intended it for good, to accomplish what is now being done, the saving of "
                "many lives' (Genesis 50:20). Third, the Christian has a 'defeater' for the "
                "evidential argument: the positive evidence for God's existence (cosmological, "
                "teleological, moral arguments; the resurrection) may outweigh the negative "
                "evidence from evil. As Plantinga notes, the probability of God given ALL the "
                "evidence may still be high. Fourth, the existence of evil is actually a problem "
                "FOR atheism: if there is no God, there is no objective evil — only things we "
                "dislike. The very ability to call something 'evil' presupposes a moral standard "
                "that atheism cannot ground."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Genesis 50:20", "Romans 8:28", "Job 42:1-6", "Isaiah 55:8-9"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does the Fall explain natural evil like earthquakes, disease, and death?",
            "answer_chirho": (
                "The Bible teaches that the natural world was originally created 'very good' "
                "(Genesis 1:31) but was corrupted by the entrance of sin through Adam's Fall. "
                "When Adam rebelled against God, the consequences affected not only humanity but "
                "all of creation. God cursed the ground: 'Cursed is the ground because of you; "
                "through painful toil you will eat food from it all the days of your life. It will "
                "produce thorns and thistles for you' (Genesis 3:17-18). Death entered the world "
                "through sin: 'For the wages of sin is death' (Romans 6:23). Paul elaborates on "
                "the cosmic scope of the Fall in Romans 8:20-22: 'For the creation was subjected "
                "to frustration, not by its own choice, but by the will of the one who subjected "
                "it, in hope that the creation itself will be liberated from its bondage to decay "
                "and brought into the freedom and glory of the children of God. We know that the "
                "whole creation has been groaning as in the pains of childbirth right up to the "
                "present time.' Natural disasters, disease, predation, and death are symptoms of "
                "a fallen creation groaning under the weight of sin's consequences. This is not "
                "the world God intended, and it is not the world that will endure. God promises a "
                "new heavens and new earth (Isaiah 65:17, Revelation 21:1-4) where the curse will "
                "be reversed. The wolf will lie down with the lamb (Isaiah 11:6-9). There will be "
                "no more death, mourning, crying, or pain (Revelation 21:4). Natural evil is "
                "temporary — the consequence of a fallen world that God is in the process of "
                "redeeming through Christ, who will ultimately 'make all things new' (Revelation 21:5)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Romans 8:20-22", "Genesis 3:17-18", "Romans 6:23", "Revelation 21:4-5"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Was there animal suffering and death before the Fall?",
            "answer_chirho": (
                "This is a debated topic among Bible-believing Christians, with sincere believers "
                "on both sides. Young Earth Creationists generally hold that there was no animal "
                "death before the Fall, based on: Genesis 1:29-30 (which describes plants as food "
                "for all creatures, implying no predation), Romans 5:12 ('sin entered the world "
                "through one man, and death through sin'), and the description of creation as "
                "'very good' (Genesis 1:31 — is a world with animal suffering and death 'very "
                "good'?). On this view, all predation, disease, and animal death are consequences "
                "of the Fall, and the original creation was peaceful (consistent with the eschatological "
                "vision of Isaiah 11:6-9 where 'the wolf shall dwell with the lamb'). Old Earth "
                "Creationists and some others argue that Romans 5:12 refers specifically to HUMAN "
                "death, that the fossil record shows animal death long before humans existed, and "
                "that some animal death may have been part of God's 'very good' creation (animals "
                "lack the moral dimension that makes human death a consequence of sin). They note "
                "that Jesus fed people fish and God clothed Adam and Eve with animal skins (Genesis "
                "3:21), suggesting animal death is not inherently evil. Both sides agree on the "
                "essential truths: creation was originally good, the Fall had cosmic consequences, "
                "and God will ultimately restore creation. The disagreement concerns the scope of "
                "the Fall's effects on the animal kingdom. What unites all Christians is the hope "
                "that 'the creation itself will be liberated from its bondage to decay' (Romans 8:21) "
                "in the new creation."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Genesis 1:29-31", "Romans 5:12", "Isaiah 11:6-9", "Romans 8:21"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How can the existence of hell be just?",
            "answer_chirho": (
                "The doctrine of hell is one of the most difficult Christian teachings, but it "
                "is also one of the most clearly taught by Jesus Himself. Jesus spoke more about "
                "hell than any other biblical figure. The justice of hell can be understood from "
                "several angles. First, hell reflects the gravity of sin. Sin is not merely "
                "breaking a rule — it is rebellion against an infinitely holy, infinitely worthy "
                "God. The severity of an offense correlates with the dignity of the one offended. "
                "Slapping a stranger is assault; slapping a president is a federal crime. Sin "
                "against an infinite God is infinitely serious. Second, hell is fundamentally "
                "about respecting human freedom. C.S. Lewis wrote: 'The doors of hell are locked "
                "from the inside.' Those in hell have chosen self over God, autonomy over "
                "submission, their own way over God's way — and God respects that choice eternally. "
                "Hell is not God dragging unwilling victims to torture; it is God allowing people "
                "to have what they chose — existence apart from Him. Since all good comes from "
                "God, separation from God means separation from all good. Third, God has done "
                "everything possible to prevent people from going to hell — short of overriding "
                "their freedom. He sent His own Son to bear the punishment we deserve: 'For God "
                "so loved the world that he gave his one and only Son, that whoever believes in "
                "him shall not perish but have eternal life' (John 3:16). The Cross demonstrates "
                "that God takes hell seriously — seriously enough to suffer Himself rather than "
                "let us go there. Fourth, our sense of justice confirms the need for ultimate "
                "accountability. If Hitler dies and faces no judgment, justice is a fiction. "
                "Hell ensures that every wrong will be addressed: 'It is mine to avenge; I will "
                "repay, says the Lord' (Romans 12:19)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["John 3:16", "Romans 12:19", "Matthew 25:46", "2 Peter 3:9"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What happens to children and those who never hear the Gospel?",
            "answer_chirho": (
                "Scripture does not give a fully explicit answer to this question, but several "
                "biblical principles provide guidance and hope. Regarding children: David, upon "
                "the death of his infant son, said 'I will go to him, but he will not return to "
                "me' (2 Samuel 12:23), expressing confidence he would see his child again. Jesus "
                "said, 'Let the little children come to me, and do not hinder them, for the "
                "kingdom of heaven belongs to such as these' (Matthew 19:14). Many theologians "
                "hold that children below the age of moral accountability are covered by God's "
                "grace. Regarding those who never hear: Paul teaches in Romans 1:19-20 that God "
                "has revealed Himself to all people through creation, so that all are 'without "
                "excuse.' Romans 2:14-15 states that Gentiles who do not have the Law have its "
                "requirements 'written on their hearts, their consciences also bearing witness.' "
                "This suggests that God judges people according to the light they have received. "
                "Abraham's rhetorical question stands: 'Will not the Judge of all the earth do "
                "right?' (Genesis 18:25). We can trust God's justice and mercy perfectly. Several "
                "views exist among Christians: (1) Those who respond to the light they have (general "
                "revelation) may be saved through Christ's atonement even without explicit knowledge "
                "of Him. (2) God, in His sovereignty, ensures the Gospel reaches all who would "
                "respond (Acts 10 — Cornelius). (3) There may be opportunity for response at or "
                "after death (a minority view based on 1 Peter 3:18-20). What we know for certain: "
                "salvation is through Christ alone (Acts 4:12), God desires all to be saved "
                "(1 Timothy 2:4, 2 Peter 3:9), God is perfectly just and perfectly merciful, and "
                "the urgency of missions remains (Romans 10:14-15)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["2 Samuel 12:23", "Genesis 18:25", "Romans 1:19-20", "Romans 2:14-15", "Acts 4:12"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What does the Book of Job teach us about suffering?",
            "answer_chirho": (
                "The Book of Job is the Bible's most extended meditation on suffering. Job was a "
                "righteous man (Job 1:1) who lost everything — his children, his wealth, his "
                "health — not because of any sin but because God permitted Satan to test him. "
                "Job's friends insisted his suffering must be punishment for hidden sin (the "
                "'retribution principle'), but God explicitly rejected their theology (Job 42:7). "
                "Several profound lessons emerge. First, suffering is not always punishment for "
                "personal sin. The disciples asked about a blind man: 'Rabbi, who sinned, this man "
                "or his parents?' Jesus answered: 'Neither' (John 9:2-3). Second, we may not "
                "understand God's reasons for allowing suffering. God never tells Job WHY he "
                "suffered. Instead, God reveals His infinite wisdom and power through a tour of "
                "creation (Job 38-41): 'Where were you when I laid the earth's foundation?' (Job "
                "38:4). The message is not that suffering is meaningless but that God's purposes "
                "are beyond our comprehension. Third, encountering God personally is the answer. "
                "Job's response after God speaks is not 'Now I understand why I suffered' but "
                "'My ears had heard of you but now my eyes have seen you' (Job 42:5). The "
                "experience of God's presence transforms suffering even without explanation. "
                "Fourth, God restores. Job's latter end was blessed more than his beginning (Job "
                "42:12). While God does not always restore in this life, the pattern of suffering "
                "followed by restoration points to the ultimate restoration in the new creation. "
                "Fifth, God is sovereign over suffering. Satan could not touch Job without God's "
                "permission (Job 1:12, 2:6). Nothing happens outside God's control. This is not "
                "cruelty but sovereignty — the assurance that even our darkest moments are within "
                "the hands of a loving God who will bring good from them (Romans 8:28)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Job 1:1", "Job 38:4", "Job 42:5", "Job 42:12", "John 9:2-3"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Doesn't the existence of evil actually presuppose God?",
            "answer_chirho": (
                "This is a powerful counter-argument that turns the problem of evil on its head. "
                "When someone says 'Evil disproves God,' they are assuming evil is objectively real "
                "— that things like the Holocaust, child abuse, and slavery are genuinely WRONG, "
                "not merely personally distasteful. But objective evil can only exist if there is "
                "an objective moral standard — and an objective moral standard requires a transcendent "
                "moral lawgiver: God. If atheism is true, 'evil' is just a word we assign to things "
                "we dislike. On a materialistic worldview, suffering is just atoms rearranging — no "
                "different in moral status from rocks eroding. As Dostoevsky recognized, 'If there "
                "is no God, everything is permitted.' C.S. Lewis described his own journey: 'My "
                "argument against God was that the universe seemed so cruel and unjust. But how "
                "had I got this idea of just and unjust? A man does not call a line crooked unless "
                "he has some idea of a straight line.' The very concept of evil presupposes a "
                "standard of good — and that standard is God's nature. So the argument from evil, "
                "paradoxically, is actually an argument FOR God. Without God, there is no objective "
                "evil — only blind, pitiless indifference, as Dawkins himself described the universe. "
                "But we KNOW evil is real. We know the Holocaust was genuinely evil, not just "
                "unfashionable. Therefore, the moral standard that grounds our judgment of evil "
                "must exist. And that standard is grounded in the character of a holy God. As "
                "Paul writes, the moral law is 'written on their hearts' (Romans 2:15) — a gift "
                "from the Lawgiver that enables us to recognize evil for what it is."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Romans 2:14-15", "Genesis 1:31", "Isaiah 5:20", "Habakkuk 1:13"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why does God allow natural disasters?",
            "answer_chirho": (
                "Natural disasters — earthquakes, hurricanes, tsunamis, volcanic eruptions — cause "
                "immense suffering and raise difficult questions about God's goodness. Several "
                "considerations help frame a Christian response. First, the geological processes "
                "that cause natural disasters also sustain life. Plate tectonics cause earthquakes "
                "but also recycle carbon, regulate climate, and create the conditions for life. "
                "Volcanic activity creates fertile soil and maintains the atmosphere. A world "
                "without these processes would be a dead world. Second, the Fall has distorted the "
                "created order. Romans 8:20-22 teaches that creation has been 'subjected to "
                "frustration' and is in 'bondage to decay.' The original creation was harmonious; "
                "the present creation groans. Third, human choices amplify natural disasters. "
                "Building in flood plains, inadequate infrastructure, poverty caused by corruption, "
                "and environmental degradation increase death tolls dramatically. The 2010 Haiti "
                "earthquake killed 230,000 while a comparable earthquake in Chile the same year "
                "killed 525 — the difference was infrastructure and governance. Fourth, natural "
                "disasters reveal human interdependence and draw out compassion. The global "
                "response to disasters — aid, prayer, sacrifice — demonstrates the image of God "
                "in humanity. Fifth, Jesus addressed this directly. When told about Galileans killed "
                "by Pilate and those killed by the falling tower of Siloam, He said: 'Do you think "
                "they were more guilty than all the others? ... No! But unless you repent, you too "
                "will all perish' (Luke 13:1-5). Disasters remind us of life's fragility and the "
                "urgency of being right with God. They are not punishments for individual sins but "
                "reminders that we live in a fallen world in need of redemption."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Romans 8:20-22", "Luke 13:1-5", "Genesis 3:17-18", "Psalm 46:1-3"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does the Cross address the problem of evil?",
            "answer_chirho": (
                "The Cross is Christianity's ultimate answer to the problem of evil. While "
                "philosophical arguments address the intellectual problem, the Cross addresses the "
                "existential and emotional dimensions. First, the Cross demonstrates that God is "
                "not indifferent to suffering — He entered it. The incarnation means God became "
                "human and experienced hunger, fatigue, rejection, betrayal, torture, and death. "
                "Jesus is not a distant deity observing our pain from afar; He is 'a man of "
                "sorrows, and acquainted with grief' (Isaiah 53:3). When we suffer, we serve a "
                "God who knows suffering from the inside. Second, the Cross reveals that God "
                "takes evil so seriously that He bore its full consequences Himself rather than "
                "simply forgiving by decree. The punishment that brought us peace was upon Him "
                "(Isaiah 53:5). God does not sweep evil under the rug — He deals with it at "
                "infinite personal cost. Third, the Cross proves that God can bring the greatest "
                "good from the greatest evil. The most evil event in history — the murder of the "
                "innocent Son of God — became the means of salvation for the entire world. If "
                "God can redeem THAT evil, He can redeem any evil. Fourth, the Cross is a promise. "
                "Because Christ conquered death through resurrection, we know that evil, suffering, "
                "and death will not have the last word. 'Where, O death, is your victory? Where, "
                "O death, is your sting?' (1 Corinthians 15:55). The resurrection guarantees "
                "that every tear will be wiped away (Revelation 21:4). Jurgen Moltmann writes "
                "that in the crucified Christ, God has made Himself known as the God who suffers "
                "WITH us — and the resurrection reveals that God will ultimately overcome all "
                "suffering. The Cross does not remove the mystery of evil, but it assures us that "
                "God is in it with us and will triumph over it."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Isaiah 53:3-5", "1 Corinthians 15:55", "Revelation 21:4", "Romans 8:32"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "If God is sovereign, is He responsible for evil?",
            "answer_chirho": (
                "The relationship between God's sovereignty and human responsibility is one of the "
                "deepest mysteries in theology, but Scripture maintains both truths simultaneously "
                "without contradiction. God is absolutely sovereign: 'The LORD has established his "
                "throne in heaven, and his kingdom rules over all' (Psalm 103:19). Nothing happens "
                "outside His decree: 'I form the light and create darkness, I bring prosperity and "
                "create disaster; I, the LORD, do all these things' (Isaiah 45:7). Yet God is not "
                "the author of evil: 'God cannot be tempted by evil, nor does he tempt anyone' "
                "(James 1:13). 'God is light; in him there is no darkness at all' (1 John 1:5). "
                "How do we reconcile these? Several important distinctions help. First, there is "
                "a difference between God CAUSING evil and God PERMITTING evil. God allowed Satan "
                "to afflict Job but did not Himself afflict Job. God permits human free choices — "
                "including evil ones — while remaining morally pure. Second, God's purposes in "
                "permitting evil are always good, even when we cannot see them. Joseph's brothers "
                "intended evil; God intended good (Genesis 50:20). The crucifixion was the most "
                "evil human act yet accomplished God's greatest purpose (Acts 2:23). Third, "
                "sovereignty does not eliminate secondary causes. When a human commits murder, "
                "the murderer — not God — is the moral agent. God's sovereignty operates THROUGH "
                "human free choices, not by overriding them. Fourth, ultimate justice is coming. "
                "God's patience with evil is not indifference but mercy — giving time for "
                "repentance (2 Peter 3:9). The day of judgment will vindicate God's justice "
                "completely (Revelation 20:11-15). We live in the tension between 'already' and "
                "'not yet' — God has already defeated evil at the Cross, but the full manifestation "
                "of that victory awaits His return."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["Genesis 50:20", "Acts 2:23", "James 1:13", "1 John 1:5", "Psalm 103:19"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why doesn't God just eliminate all evil right now?",
            "answer_chirho": (
                "If God eliminated all evil right now, none of us would survive. 'For all have "
                "sinned and fall short of the glory of God' (Romans 3:23). Every human being has "
                "evil in their heart — selfishness, pride, dishonesty, malice. If God purged the "
                "universe of evil instantly, the purge would include us. The real question is not "
                "'Why doesn't God stop evil?' but 'Why doesn't God stop ME?' — because we are all "
                "part of the problem. God's delay in final judgment is not indifference but mercy: "
                "'The Lord is not slow in keeping his promise, as some understand slowness. Instead "
                "he is patient with you, not wanting anyone to perish, but everyone to come to "
                "repentance' (2 Peter 3:9). God IS dealing with evil — through the Cross, through "
                "the work of the Holy Spirit in transforming hearts, through the Church as salt and "
                "light, through governments ordained to restrain evil (Romans 13:1-4), and through "
                "His providential governance of history. And He WILL deal with evil finally and "
                "completely at the return of Christ. Revelation describes the ultimate defeat of "
                "evil: Satan thrown into the lake of fire (Revelation 20:10), death and Hades "
                "destroyed (Revelation 20:14), and a new creation where 'there will be no more "
                "death or mourning or crying or pain' (Revelation 21:4). The current age is the "
                "age of grace — the window of opportunity for repentance and faith before final "
                "judgment. God has defeated evil decisively at the Cross; He will manifest that "
                "victory completely at His return. In the meantime, He calls us to be agents of "
                "good in a broken world: 'Do not be overcome by evil, but overcome evil with "
                "good' (Romans 12:21)."
            ),
            "topic_chirho": "problem_of_evil",
            "scripture_chirho": ["2 Peter 3:9", "Romans 3:23", "Revelation 21:4", "Romans 12:21"],
            "difficulty_chirho": "basic",
        },
    ]


# Placeholder functions to be filled in subsequent edits
def build_reliability_of_scripture_chirho() -> list[dict]:
    """Build entries for reliability of Scripture (~20 entries)."""
    return [
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How do we know the Bible is internally consistent across 40 authors over 1,500 years?",
            "answer_chirho": (
                "The Bible was written by approximately 40 different authors over a span of roughly "
                "1,500 years (from Moses circa 1400 BC to John circa 95 AD). These authors came "
                "from vastly different backgrounds — kings (David, Solomon), shepherds (Amos), "
                "fishermen (Peter, John), a doctor (Luke), a tax collector (Matthew), a Pharisee "
                "(Paul), a cupbearer (Nehemiah), and a farmer (Elisha). They wrote in three "
                "languages (Hebrew, Aramaic, Greek), on three continents (Asia, Africa, Europe), "
                "in diverse genres (history, poetry, prophecy, law, epistle, apocalyptic). Yet "
                "the Bible tells one unified story: creation, fall, redemption, restoration. The "
                "central theme — God's plan to redeem humanity through the Messiah — runs from "
                "Genesis 3:15 (the first promise of a deliverer) through Revelation 22 (the "
                "consummation of redemption). This is without parallel in world literature. No "
                "other collection of documents produced over such a timespan by so many diverse "
                "authors exhibits this kind of thematic unity. Imagine 40 authors from different "
                "centuries writing independently about medicine — you would get contradictions, "
                "not coherence. The Bible's unity is best explained by a single divine Author "
                "working through human instruments: 'All Scripture is God-breathed' (2 Timothy "
                "3:16). 'For prophecy never had its origin in the human will, but prophets, "
                "though human, spoke from God as they were carried along by the Holy Spirit' "
                "(2 Peter 1:21). The internal consistency is not absolute uniformity — each author "
                "has his own style and emphasis — but it is a unified testimony to God's redemptive "
                "plan, woven across millennia with a coherence that defies naturalistic explanation."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["2 Timothy 3:16", "2 Peter 1:21", "Genesis 3:15", "Revelation 22:13"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the bibliographic test for the New Testament, and how does it compare to other ancient texts?",
            "answer_chirho": (
                "The bibliographic test examines the quantity and quality of manuscript copies and "
                "the time gap between the original writing and the earliest surviving copy. By this "
                "measure, the New Testament is the best-attested document in all of ancient history. "
                "There are approximately 5,900 Greek manuscripts, 10,000+ Latin Vulgate manuscripts, "
                "and 9,300+ manuscripts in other early languages (Syriac, Coptic, Armenian, etc.) — "
                "totaling over 25,000 manuscript copies. Compare this to other ancient texts: Homer's "
                "Iliad has about 1,800 manuscripts (earliest copy 500 years after the original); "
                "Caesar's Gallic Wars has about 10 manuscripts (1,000-year gap); Thucydides has 8 "
                "manuscripts (1,300-year gap); Plato's works have 7 manuscripts (1,200-year gap). "
                "The earliest New Testament fragment, Papyrus 52 (P52), contains portions of John 18 "
                "and dates to approximately 125 AD — within 30-60 years of the original. Entire "
                "books are preserved in papyri from the 2nd-3rd centuries. The Chester Beatty papyri "
                "(P45, P46, P47) date to approximately 200 AD and contain large portions of the "
                "Gospels, Acts, Paul's letters, and Revelation. No other ancient text comes remotely "
                "close. If we reject the textual reliability of the New Testament, we must reject "
                "the textual reliability of ALL ancient literature — because no other text has "
                "anything approaching this level of manuscript attestation. 'Heaven and earth will "
                "pass away, but my words will never pass away' (Matthew 24:35). God has preserved "
                "His Word through the centuries with remarkable fidelity."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Matthew 24:35", "Isaiah 40:8", "1 Peter 1:25", "Psalm 12:6-7"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the internal evidence test for the New Testament?",
            "answer_chirho": (
                "The internal evidence test asks: do the documents claim to be eyewitness accounts, "
                "and do they bear the marks of genuine eyewitness testimony? The New Testament "
                "repeatedly and explicitly claims eyewitness authority. Luke writes: 'Many have "
                "undertaken to draw up an account of the things that have been fulfilled among us, "
                "just as they were handed down to us by those who from the first were eyewitnesses' "
                "(Luke 1:1-2). John writes: 'The man who saw it has given testimony, and his "
                "testimony is true. He knows that he tells the truth' (John 19:35). Peter states: "
                "'For we did not follow cleverly devised stories when we told you about the coming "
                "of our Lord Jesus Christ in power, but we were eyewitnesses of his majesty' "
                "(2 Peter 1:16). Paul lists over 500 eyewitnesses of the resurrected Christ, "
                "noting 'most of whom are still living' — an invitation to verify (1 Corinthians "
                "15:6). The Gospels contain numerous marks of eyewitness testimony: irrelevant "
                "details that serve no theological purpose but indicate genuine memory (the number "
                "of fish caught in John 21:11 — 153; the boy with the linen cloth in Mark 14:51-52); "
                "embarrassing details the authors would not have invented (Peter's denials, the "
                "disciples' failures to understand, women as first resurrection witnesses in a "
                "culture that did not accept female testimony); geographic and cultural details "
                "confirmed by archaeology. Richard Bauckham's 'Jesus and the Eyewitnesses' (2006) "
                "demonstrates that the Gospels bear the formal characteristics of ancient "
                "eyewitness testimony, including the use of named eyewitness sources as literary "
                "inclusios (brackets) framing the narratives."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Luke 1:1-4", "John 19:35", "2 Peter 1:16", "1 Corinthians 15:6"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Does archaeology confirm the Bible?",
            "answer_chirho": (
                "Archaeological discoveries have consistently confirmed biblical accounts, never "
                "definitively contradicting them. Nelson Glueck, one of the 20th century's greatest "
                "archaeologists, stated: 'It may be stated categorically that no archaeological "
                "discovery has ever controverted a biblical reference.' Key confirmations include: "
                "The Pool of Siloam (John 9:7) was discovered in 2004 during sewer repair in "
                "Jerusalem. The Pontius Pilate inscription was found at Caesarea Maritima in 1961, "
                "confirming his title as prefect of Judea. The Caiaphas ossuary (bone box of the "
                "high priest who condemned Jesus) was found in 1990. The Tel Dan Stele (1993) "
                "contains the phrase 'House of David,' confirming David's dynasty as historical. "
                "Hezekiah's Tunnel (2 Kings 20:20) has been confirmed and explored. The Cyrus "
                "Cylinder confirms Cyrus's policy of returning exiled peoples, consistent with "
                "Ezra 1:1-4. The Merneptah Stele (c. 1208 BC) provides the earliest extra-biblical "
                "reference to 'Israel.' The Ebla tablets (1964-1975) confirm customs and place "
                "names from the patriarchal era. Luke's accuracy as a historian in Acts has been "
                "confirmed in dozens of details — Sir William Ramsay, who began as a skeptic, "
                "concluded Luke was a 'historian of the first rank.' Critics once denied the "
                "existence of the Hittites, the practice of Roman census (Luke 2:1-3), and the "
                "existence of Nazareth in Jesus' time — all have since been confirmed. The trend "
                "of archaeology consistently moves toward confirming the biblical record, not away "
                "from it. 'Every word of God proves true' (Proverbs 30:5)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Proverbs 30:5", "Joshua 24:13", "Luke 3:1-2", "Acts 26:26"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does fulfilled prophecy demonstrate the divine origin of Scripture?",
            "answer_chirho": (
                "The Bible contains hundreds of specific, verifiable prophecies that were fulfilled, "
                "often centuries after they were written. This is unique among world scriptures and "
                "constitutes powerful evidence of divine inspiration. Professor Peter Stoner calculated "
                "the probability of one person fulfilling just 8 Messianic prophecies at 1 in 10^17. "
                "For 48 prophecies, the probability is 1 in 10^157. Jesus fulfilled over 300 Messianic "
                "prophecies. Key examples: Born in Bethlehem (Micah 5:2, written c. 700 BC; fulfilled "
                "Matthew 2:1). Born of a virgin (Isaiah 7:14; fulfilled Matthew 1:18-25). From the "
                "tribe of Judah (Genesis 49:10; fulfilled Matthew 1:2-3). Entered Jerusalem on a "
                "donkey (Zechariah 9:9; fulfilled Matthew 21:1-11). Betrayed for 30 pieces of silver "
                "(Zechariah 11:12-13; fulfilled Matthew 26:15). Hands and feet pierced (Psalm 22:16, "
                "written c. 1000 BC — before crucifixion existed; fulfilled John 20:25). Lots cast "
                "for garments (Psalm 22:18; fulfilled John 19:24). Buried in a rich man's tomb "
                "(Isaiah 53:9; fulfilled Matthew 27:57-60). Daniel 9:24-26 even predicted the "
                "approximate TIME of Messiah's coming and death. Beyond Messianic prophecy, the "
                "Bible predicted the destruction and restoration of Israel (Deuteronomy 28-30; "
                "Ezekiel 37), the fall of specific empires (Daniel 2, 7), and the destruction of "
                "Tyre (Ezekiel 26). The Dead Sea Scrolls (dated 150 BC - 70 AD) confirm that these "
                "prophecies predate their fulfillment, eliminating the objection of postdiction. "
                "'I make known the end from the beginning, from ancient times, what is still to "
                "come' (Isaiah 46:10)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Isaiah 46:10", "Micah 5:2", "Psalm 22:16-18", "Daniel 9:24-26"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Does the Bible contain scientific foreknowledge?",
            "answer_chirho": (
                "While the Bible is not a science textbook, it contains numerous statements that "
                "align with scientific discoveries made centuries or millennia later. These suggest "
                "a supernatural source of knowledge. Examples include: The earth is suspended in "
                "space — 'He suspends the earth over nothing' (Job 26:7, written c. 2000 BC, when "
                "ancient cultures believed the earth rested on a giant turtle, Atlas's shoulders, "
                "or an infinite stack of elephants). The water cycle — 'He draws up the drops of "
                "water, which distill as rain to the streams; the clouds pour down their moisture "
                "and abundant showers fall on mankind' (Job 36:27-28; also Ecclesiastes 1:7). "
                "Ocean currents and paths in the seas — Matthew Maury, the father of oceanography, "
                "was inspired by Psalm 8:8 ('the fish of the sea, all that swim the paths of the "
                "seas') to search for and discover ocean currents. The expansion of the universe — "
                "at least 11 passages describe God 'stretching out the heavens' (Isaiah 40:22, "
                "Job 9:8, Zechariah 12:1), consistent with the 1929 discovery of cosmic expansion. "
                "The number of stars is uncountable — 'I will make your descendants as numerous as "
                "the stars in the sky' (Genesis 22:17). Ancient astronomers counted only about 3,000 "
                "visible stars; we now know there are over 10^22. Quarantine and hygiene laws "
                "(Leviticus 13-15) predated germ theory by 3,000 years. These are not claims that "
                "the Bible teaches modern science, but observations that biblical statements, "
                "written in pre-scientific eras, align remarkably with later discoveries — "
                "consistent with divine authorship."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Job 26:7", "Isaiah 40:22", "Ecclesiastes 1:7", "Psalm 8:8"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How accurately was the Bible transmitted over the centuries?",
            "answer_chirho": (
                "The textual transmission of the Bible is remarkably accurate, as demonstrated by "
                "manuscript comparisons spanning centuries. For the Old Testament, the most dramatic "
                "evidence comes from the Dead Sea Scrolls, discovered in 1947. Before this discovery, "
                "the oldest complete Hebrew Old Testament manuscript was the Leningrad Codex (1008 AD). "
                "The Dead Sea Scrolls contained copies of every Old Testament book except Esther, "
                "dating from the 3rd century BC to the 1st century AD — over 1,000 years earlier. "
                "When scholars compared the Dead Sea Isaiah scroll (1QIsa-a) with the Leningrad "
                "Codex, they found 95% word-for-word identity. The 5% variation consisted almost "
                "entirely of spelling differences and minor scribal slips that affected no doctrine. "
                "For the New Testament, textual scholars have identified approximately 400,000 "
                "textual variants across the 25,000+ manuscripts. This sounds alarming until you "
                "understand the nature of the variants: the vast majority (roughly 75%) are spelling "
                "differences (like 'colour' vs 'color'). Another 15% are variations in word order "
                "that do not affect meaning in Greek. About 9% are synonyms or stylistic changes. "
                "Less than 1% of variants are both meaningful and viable — and none of these affect "
                "any core Christian doctrine. Scholar Daniel Wallace estimates that we can reconstruct "
                "the original text of the New Testament with 99%+ accuracy. Bruce Metzger concluded "
                "that the New Testament text 'is more certain than that of any other ancient book.' "
                "'The grass withers, the flower fades, but the word of our God will stand forever' "
                "(Isaiah 40:8)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Isaiah 40:8", "Matthew 5:18", "Psalm 119:89", "1 Peter 1:25"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How was the biblical canon formed? Was it decided at the Council of Nicaea?",
            "answer_chirho": (
                "The popular myth — propagated by Dan Brown's 'The Da Vinci Code' and other sources — "
                "that the biblical canon was decided at the Council of Nicaea (325 AD) is demonstrably "
                "false. The Council of Nicaea addressed the Arian heresy (whether Christ was divine) "
                "and the date of Easter. The canon was not on its agenda, as confirmed by surviving "
                "council records. The New Testament canon was recognized, not created, through an "
                "organic process spanning the first four centuries. From the earliest period, the "
                "apostolic writings were treated as authoritative. Peter refers to Paul's letters as "
                "'Scriptures' (2 Peter 3:15-16). By the mid-2nd century, the core of the NT was "
                "widely recognized. The Muratorian Fragment (c. 170 AD) lists most NT books. Irenaeus "
                "(c. 180 AD) treats the four Gospels as established and authoritative. Athanasius's "
                "39th Festal Letter (367 AD) lists the 27 books of the NT exactly as we have them. "
                "The Councils of Hippo (393 AD) and Carthage (397 AD) formally ratified what was "
                "already the church's received collection. The criteria used to recognize canonical "
                "books were: (1) Apostolic origin — written by an apostle or close associate. "
                "(2) Universal acceptance — recognized by churches across the Roman Empire. "
                "(3) Doctrinal consistency — in harmony with the received apostolic teaching. "
                "(4) Divine quality — bearing evidence of spiritual power and authority. The early "
                "church fathers did not choose randomly; they critically examined each book. The "
                "disputed books (Revelation, 2 Peter, James, 2-3 John, Jude, Hebrews) were "
                "disputed precisely because the church was being careful, not careless."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["2 Peter 3:15-16", "2 Timothy 3:16-17", "John 16:13", "1 Timothy 5:18"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why don't Protestants include the Apocrypha?",
            "answer_chirho": (
                "The Apocrypha (or deuterocanonical books) — Tobit, Judith, Wisdom of Solomon, "
                "Sirach, Baruch, 1-2 Maccabees, and additions to Esther and Daniel — are included "
                "in Roman Catholic and Eastern Orthodox Bibles but not in most Protestant Bibles. "
                "Protestants exclude them for several reasons. First, the Jewish canon did not "
                "include them. Jesus and the apostles quoted from the Old Testament extensively "
                "(over 300 times in the NT) but never quoted from the Apocrypha. The Jewish "
                "historian Josephus (c. 95 AD) listed the Jewish Scriptures and did not include "
                "these books. The Talmud does not recognize them as canonical. Second, the "
                "Apocryphal books themselves do not claim divine inspiration. In fact, 1 Maccabees "
                "4:46 and 9:27 acknowledge that prophetic revelation had ceased. Third, several "
                "Church Fathers distinguished the Apocrypha from canonical Scripture. Jerome "
                "(who translated the Latin Vulgate) explicitly stated they were useful for "
                "edification but not for establishing doctrine. Athanasius listed them separately "
                "from canonical books. Fourth, the Apocrypha contains some teachings that conflict "
                "with canonical Scripture, such as prayers for the dead (2 Maccabees 12:45-46) "
                "and salvation by works (Tobit 12:9). Fifth, the Apocrypha was added to the "
                "Catholic canon at the Council of Trent (1546) largely in response to the "
                "Reformation — over a millennium after the books were written. This does not "
                "mean the Apocrypha is worthless — it contains valuable historical information "
                "about the intertestamental period. But Protestants, following the Reformers, "
                "hold that it is not inspired Scripture. 'Every word of God is flawless' "
                "(Proverbs 30:5) — the question is which words are God's."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Proverbs 30:5-6", "Revelation 22:18-19", "Deuteronomy 4:2", "Romans 3:2"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why are the Gnostic Gospels rejected as unreliable?",
            "answer_chirho": (
                "The so-called 'Gnostic Gospels' — including the Gospel of Thomas, Gospel of Philip, "
                "Gospel of Judas, and others found at Nag Hammadi (1945) — are sometimes presented as "
                "'lost' or 'suppressed' alternatives to the canonical Gospels. In reality, they are "
                "rejected for strong historical and theological reasons. First, they are late. The "
                "canonical Gospels were written within 30-65 years of Jesus' death (Mark c. 55-65 AD, "
                "Matthew and Luke c. 60-80 AD, John c. 85-95 AD). The Gnostic texts date from the "
                "mid-2nd to 4th centuries — 100-300 years after Jesus, far too late to be eyewitness "
                "accounts. Second, they are pseudepigraphal — falsely attributed to famous figures. "
                "Thomas did not write the Gospel of Thomas; Judas did not write the Gospel of Judas. "
                "Third, they reflect Gnostic theology (secret knowledge, the material world as evil, "
                "a demiurge creator) that is foreign to Judaism and early Christianity. The Gospel "
                "of Thomas (saying 114) has Jesus say Mary must become male to enter heaven — hardly "
                "consistent with Jesus' actual treatment of women. Fourth, the early Church Fathers "
                "knew about these texts and explicitly rejected them. Irenaeus (c. 180 AD) systematically "
                "refuted Gnostic teachings in 'Against Heresies.' Fifth, they lack narrative coherence. "
                "Most are collections of sayings without historical context, geography, or witnesses. "
                "The canonical Gospels, by contrast, are grounded in specific times, places, and "
                "people — verifiable claims. These texts were not 'suppressed' by a power grab; "
                "they were recognized as inauthentic by communities that had preserved genuine "
                "apostolic teaching. 'Beloved, do not believe every spirit, but test the spirits "
                "to see whether they are from God' (1 John 4:1)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["1 John 4:1", "Galatians 1:8", "2 Corinthians 11:4", "Jude 1:3"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How do we address apparent contradictions in the Bible?",
            "answer_chirho": (
                "Skeptics often point to alleged contradictions in the Bible as evidence against its "
                "reliability. While these deserve honest examination, virtually all of them dissolve "
                "upon careful study. Common types of 'contradictions' include: Different perspectives "
                "on the same event — like four witnesses to a car accident giving complementary but "
                "not identical accounts. The Gospels describe Jesus' ministry from different angles "
                "(Matthew for Jewish readers, Luke for Gentiles, etc.). Differences in detail confirm "
                "independence; if all four Gospels were identical, critics would claim collusion. "
                "Paraphrase vs. quotation — ancient writers routinely paraphrased speeches rather "
                "than quoting verbatim. When Matthew and Luke record the same teaching slightly "
                "differently, they are both accurately conveying the gist, as was the convention. "
                "Telescoping — compressing events for narrative purposes. Mark describes two "
                "incidents at the fig tree as separate events; Matthew combines them into one "
                "narrative unit. Both are accurate; the difference is in arrangement, not substance. "
                "Numbers and measures — ancient cultures used different counting systems and rounding "
                "conventions. An army of 'about 5,000' and '5,300' are not contradictions but "
                "approximations at different levels of precision. Progressive revelation — God "
                "revealed His truth over time. Old Testament practices (polygamy, dietary laws) "
                "that seem to conflict with New Testament teaching represent God accommodating to "
                "cultural situations while progressively revealing His full will. The principle to "
                "apply: if a plausible harmonization exists, the 'contradiction' is merely apparent. "
                "And in virtually every case, plausible harmonizations exist — often multiple ones. "
                "'The sum of your word is truth' (Psalm 119:160)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Psalm 119:160", "John 10:35", "2 Timothy 2:15", "Proverbs 25:2"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is the significance of the Dead Sea Scrolls?",
            "answer_chirho": (
                "The Dead Sea Scrolls, discovered between 1947 and 1956 in caves near Qumran by "
                "the Dead Sea, are arguably the most important archaeological discovery of the 20th "
                "century for biblical studies. The collection includes over 900 manuscripts dating "
                "from approximately 250 BC to 68 AD. They include copies or fragments of every Old "
                "Testament book except Esther. Before the discovery, the oldest complete Hebrew Old "
                "Testament manuscript was the Leningrad Codex (1008 AD). The Dead Sea Scrolls pushed "
                "our manuscript evidence back over 1,000 years. The Great Isaiah Scroll (1QIsa-a), "
                "dating to approximately 125 BC, is the most famous. When compared with the "
                "Masoretic text (which underlies modern translations), the scroll showed 95% "
                "word-for-word accuracy across a millennium of copying. The 5% differences were "
                "almost entirely minor spelling variations and copyist slips. Not a single "
                "theological teaching was altered. This demonstrates the extraordinary fidelity of "
                "the Jewish scribal tradition. The scrolls also confirmed that books like Isaiah "
                "and Daniel — which contain detailed prophecies about the Messiah and future "
                "kingdoms — were indeed written centuries before their fulfillment, eliminating "
                "the liberal critical claim that they were written after the events they describe. "
                "Additionally, the scrolls reveal that the Jewish community at Qumran had Messianic "
                "expectations remarkably similar to what Jesus fulfilled. The Dead Sea Scrolls "
                "provide powerful evidence that the Old Testament text we have today is substantially "
                "the same as what was written by the original authors — 'The word of our God "
                "endures forever' (Isaiah 40:8)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Isaiah 40:8", "Psalm 119:89", "Matthew 5:18", "Luke 21:33"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Were the Gospels written too late to be reliable?",
            "answer_chirho": (
                "Critical scholars sometimes claim the Gospels were written too late to be reliable "
                "eyewitness accounts. However, the evidence supports early dates well within "
                "eyewitness lifetimes. Most scholars — including liberal scholars — date the Gospels "
                "as follows: Mark 55-70 AD, Matthew 60-80 AD, Luke 60-80 AD, John 85-95 AD. Jesus "
                "was crucified c. 30-33 AD. This puts the Gospels within 25-65 years of the events — "
                "well within living memory. Many eyewitnesses would still have been alive. Compare "
                "this to Alexander the Great: our earliest surviving biographies (Plutarch, Arrian) "
                "were written 400+ years after his death, yet historians trust them. Several lines "
                "of evidence support early Gospel dates. Acts ends abruptly with Paul under house "
                "arrest in Rome (c. 62 AD), not mentioning his death (c. 64-67 AD), the destruction "
                "of Jerusalem (70 AD), or other major events — strongly suggesting Acts was written "
                "before 62 AD. Since Luke precedes Acts (Acts 1:1), and Mark likely preceded Luke, "
                "this pushes Mark into the 50s AD — only 20-25 years after Jesus. Paul's letters "
                "(written 48-65 AD) contain early creedal formulas that predate even his letters. "
                "1 Corinthians 15:3-5 is a creed that scholars date to within 3-5 years of the "
                "crucifixion. The claim that decades of oral tradition corrupted the record ignores "
                "the nature of oral cultures: in societies where memory was trained and valued, oral "
                "traditions were preserved with remarkable accuracy, as Kenneth Bailey demonstrated."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Luke 1:1-4", "1 Corinthians 15:3-5", "2 Peter 1:16", "1 John 1:1-3"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Is the Old Testament historically reliable?",
            "answer_chirho": (
                "The historical reliability of the Old Testament has been increasingly confirmed "
                "by archaeological and extra-biblical evidence, though some events (particularly "
                "from the early periods) await archaeological corroboration. For the patriarchal "
                "period (Abraham, Isaac, Jacob), the customs described in Genesis (adoption practices, "
                "birthright sales, deathbed blessings) match precisely with practices documented in "
                "the Nuzi tablets (15th century BC) and Mari letters (18th century BC). The Ebla "
                "tablets (24th century BC) contain personal names and place names matching Genesis. "
                "For the Exodus period, while direct archaeological evidence is debated, the "
                "Merneptah Stele (c. 1208 BC) confirms Israel's existence in Canaan by that date. "
                "The Brooklyn Papyrus (c. 1740 BC) contains Semitic names matching those in Genesis "
                "and Exodus. The Ipuwer Papyrus describes plague-like conditions in Egypt. For the "
                "monarchy, evidence is abundant: the Tel Dan Stele mentions the 'House of David.' "
                "The Mesha Stele mentions Israel, Omri, and Chemosh. Hezekiah's tunnel has been "
                "explored and dated. Sennacherib's prism describes his siege of Jerusalem, "
                "confirming 2 Kings 18-19. The Babylonian Chronicles confirm the capture of "
                "Jerusalem in 597 BC. The Cyrus Cylinder confirms the decree to return exiles. "
                "For the post-exilic period, the Elephantine Papyri confirm Jewish communities "
                "in Egypt with practices matching biblical descriptions. The consistent pattern: "
                "where the Old Testament can be tested against external evidence, it is confirmed. "
                "'Your word is truth' (John 17:17)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["John 17:17", "Psalm 119:160", "Joshua 21:45", "Numbers 23:19"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Can we trust the Bible when it records miracles?",
            "answer_chirho": (
                "The objection to biblical miracles often rests on David Hume's argument (1748) "
                "that miracles are by definition the least probable explanation for any event. But "
                "Hume's argument is circular: it assumes miracles cannot happen in order to conclude "
                "that they never have. If God exists — and the cosmological, teleological, and moral "
                "arguments give strong reasons to think He does — then miracles are not only possible "
                "but expected. A God who created the universe from nothing can certainly intervene "
                "within it. The question is not 'Are miracles possible?' but 'Has God actually "
                "performed them?' And the evidence says yes. The resurrection of Jesus is the "
                "central miracle of Christianity, supported by the empty tomb, post-mortem "
                "appearances to over 500 witnesses, and the transformation of the disciples from "
                "fearful fugitives to bold proclaimers willing to die. The miracles recorded in "
                "Scripture are not arbitrary magic tricks; they are signs pointing to God's identity "
                "and purposes. Jesus' miracles authenticated His divine claims: 'The works that the "
                "Father has given me to finish — the very works that I am doing — testify that the "
                "Father has sent me' (John 5:36). The Bible does not ask us to believe in miracles "
                "blindly but provides them as evidence: 'Jesus performed many other signs in the "
                "presence of his disciples... But these are written that you may believe that Jesus "
                "is the Messiah, the Son of God' (John 20:30-31). Furthermore, well-documented "
                "miracles continue today — Craig Keener's academic study documents hundreds of "
                "cases with medical documentation. The naturalistic assumption that miracles cannot "
                "occur is a philosophical presupposition, not a scientific conclusion."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["John 5:36", "John 20:30-31", "Acts 2:22", "Hebrews 2:4"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How do we know the Bible's authors were honest and not making things up?",
            "answer_chirho": (
                "Multiple features of the biblical texts indicate the authors were honest reporters "
                "rather than fabricators. First, the criterion of embarrassment: the Gospel writers "
                "included material that was embarrassing to themselves and to the early church. Peter "
                "is shown denying Christ three times (Mark 14:66-72). The disciples repeatedly fail "
                "to understand Jesus' teaching (Mark 9:32). James and John selfishly request seats "
                "of honor (Mark 10:35-37). The women — whose testimony was not accepted in Jewish "
                "courts — are the first witnesses to the resurrection. If the authors were inventing "
                "a story to promote their movement, they would never have included these details. "
                "Second, unnecessary details: genuine eyewitness accounts include incidental details "
                "that serve no theological purpose but indicate real memory — the 153 fish in John "
                "21:11, the young man who fled naked in Mark 14:51-52, the detail that Jesus was "
                "sleeping on a cushion in the stern (Mark 4:38). Third, the authors suffered and "
                "died for their testimony. People may die for beliefs they mistakenly think are true, "
                "but the apostles were in a position to KNOW whether they had seen the risen Jesus. "
                "They would not endure persecution and martyrdom for a known lie. Fourth, the "
                "writings circulated during the lifetimes of eyewitnesses who could have corrected "
                "errors. Paul explicitly invites verification: 'most of whom are still living' "
                "(1 Corinthians 15:6). Fifth, the portrait of Jesus is too consistent and compelling "
                "to be fictional. No 1st-century Jewish author could have invented a character who "
                "transcends every cultural category and continues to captivate billions. 'That which "
                "was from the beginning, which we have heard, which we have seen with our eyes, "
                "which we have looked at and our hands have touched — this we proclaim' (1 John 1:1)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["1 John 1:1", "1 Corinthians 15:6", "John 21:24", "Acts 4:20"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Has the Bible been changed or corrupted over time by the Church?",
            "answer_chirho": (
                "The claim that the Bible has been corrupted through centuries of copying and "
                "translation is widespread but demonstrably false. The manuscript evidence shows "
                "remarkable preservation. For the Old Testament: the Dead Sea Scrolls (250 BC - "
                "68 AD) proved that the Hebrew text was transmitted with 95%+ accuracy over 1,000+ "
                "years. For the New Testament: we have over 25,000 manuscripts in multiple "
                "languages, enabling textual critics to identify and correct copying errors through "
                "comparison. Modern Bible translations are not translations of translations — they "
                "go back to the earliest Greek and Hebrew manuscripts. The King James Version "
                "(1611) was translated from Greek and Hebrew, not from Latin. Modern translations "
                "like the ESV, NASB, and NIV use even earlier and better manuscripts discovered "
                "since 1611. The idea of deliberate corruption faces a practical impossibility: "
                "manuscripts were spread across the entire Roman Empire and beyond. There was no "
                "central authority that could have collected and altered all copies simultaneously. "
                "Changes in one region would be detectable by comparison with manuscripts from "
                "other regions — which is exactly how textual criticism works. The church fathers "
                "also quoted the New Testament so extensively (over 36,000 quotations) that the "
                "entire NT could be reconstructed from their writings alone, providing an "
                "independent check. Bart Ehrman, a prominent skeptic, acknowledges: 'The "
                "essential Christian beliefs are not affected by textual variants in the manuscript "
                "tradition.' God's Word has endured: 'The grass withers and the flowers fall, "
                "but the word of our God endures forever' (Isaiah 40:8)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Isaiah 40:8", "Matthew 24:35", "John 10:35", "Psalm 119:89"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What about the different Gospel accounts of the resurrection — don't they contradict?",
            "answer_chirho": (
                "The four Gospel accounts of the resurrection differ in certain details — the number "
                "of women at the tomb, the number of angels, the precise sequence of events. Skeptics "
                "claim these are contradictions; in fact, they are exactly what we would expect from "
                "independent eyewitness testimony and actually strengthen the case for historicity. "
                "Police investigators know that when multiple witnesses give identical accounts, it "
                "suggests collusion. When they give accounts that differ in peripheral details while "
                "agreeing on core facts, it suggests genuine independent testimony. The core facts "
                "all four Gospels agree on: (1) Jesus died by crucifixion on Friday. (2) He was "
                "buried in a tomb. (3) The tomb was found empty on Sunday morning. (4) Women were "
                "the first to discover the empty tomb. (5) Jesus appeared alive to His followers. "
                "The differences are in secondary details: Matthew mentions 'Mary Magdalene and the "
                "other Mary' (28:1); Mark adds Salome (16:1); Luke mentions Joanna and others "
                "(24:10). These are complementary, not contradictory — different witnesses noticed "
                "different people. One account mentions one angel; another mentions two. Mentioning "
                "one does not deny the existence of two — it is simply selective reporting. Simon "
                "Greenleaf, co-founder of Harvard Law School and author of the authoritative "
                "treatise on legal evidence, examined the Gospel resurrection accounts by the "
                "standards of courtroom evidence and concluded they would be accepted as reliable "
                "testimony in any court of law. The variations prove independence; the agreement "
                "on core facts proves reliability. As Paul summarized the common tradition: 'Christ "
                "died for our sins according to the Scriptures, he was buried, he was raised on "
                "the third day' (1 Corinthians 15:3-4)."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["1 Corinthians 15:3-5", "Matthew 28:1-10", "Mark 16:1-8", "Luke 24:1-12"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why should we trust the Bible over other holy books?",
            "answer_chirho": (
                "While respect for sincere seekers of all faiths is important, the Bible possesses "
                "unique features that distinguish it from all other religious texts. First, "
                "manuscript evidence: no other ancient text — religious or secular — approaches the "
                "New Testament's 25,000+ manuscripts. The Quran's manuscript tradition is much later "
                "and less diverse; the Hindu Vedas have far fewer manuscripts; Buddhist scriptures "
                "were transmitted orally for centuries before being written. Second, prophecy "
                "fulfillment: the Bible contains over 300 Messianic prophecies fulfilled by Jesus, "
                "plus hundreds of historical prophecies confirmed by archaeology. No other holy book "
                "approaches this level of predictive accuracy. The Quran contains no predictive "
                "prophecy comparable to biblical prophecy. Third, archaeological confirmation: "
                "biblical people, places, and events are consistently confirmed by archaeology. "
                "Fourth, historical testability: the Bible invites verification — it names specific "
                "people, places, and dates that can be checked. Paul publicly appealed to verifiable "
                "facts: 'What I am saying is true and reasonable. The king is familiar with these "
                "things... I am convinced that none of this has escaped his notice, because it was "
                "not done in a corner' (Acts 26:25-26). Fifth, internal consistency: 40 authors, "
                "1,500 years, three languages, one unified message of redemption through Christ. "
                "Sixth, transformative power: the Bible has transformed more lives, inspired more "
                "art, literature, and social reform, and shaped more civilizations than any other "
                "book in history. Seventh, Jesus Christ: the Bible centers on the most extraordinary "
                "person who ever lived — one who claimed to be God, backed it with miracles, and "
                "proved it by rising from the dead. No other holy book makes comparable claims "
                "supported by comparable evidence."
            ),
            "topic_chirho": "reliability_of_scripture",
            "scripture_chirho": ["Acts 26:25-26", "John 14:6", "2 Timothy 3:16-17", "Hebrews 4:12"],
            "difficulty_chirho": "basic",
        },
    ]


def build_jesus_christ_chirho() -> list[dict]:
    """Build entries about Jesus Christ (~20 entries)."""
    return [
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What evidence for Jesus exists outside the Bible?",
            "answer_chirho": (
                "Multiple non-Christian sources from the 1st-2nd centuries confirm the historical "
                "existence of Jesus and core claims about Him. Josephus (Jewish historian, c. 93 AD) "
                "mentions Jesus twice in 'Antiquities of the Jews': the Testimonium Flavianum "
                "(18.3.3) describes Jesus as 'a wise man' who was crucified under Pilate, and "
                "Antiquities 20.9.1 refers to 'James, the brother of Jesus who is called Christ.' "
                "Even critical scholars accept the core of these references as authentic. Tacitus "
                "(Roman historian, c. 116 AD) in 'Annals' 15.44 describes 'Christus' being executed "
                "under Pontius Pilate during Tiberius's reign. Pliny the Younger (Roman governor, "
                "c. 112 AD) in 'Letters' 10.96 describes Christians worshipping Christ 'as to a "
                "god.' Thallus (c. 52 AD, preserved by Julius Africanus) attempted to explain the "
                "darkness at Jesus' crucifixion as a solar eclipse — confirming the event while "
                "disputing its cause. Mara bar Serapion (Syrian philosopher, c. 73 AD) references "
                "the execution of 'the wise King' of the Jews. Lucian of Samosata (satirist, c. 170 "
                "AD) mocks Christians for worshipping 'the crucified sophist.' The Talmud "
                "(Sanhedrin 43a) mentions 'Yeshu' being hanged (crucified) on Passover eve. The "
                "cumulative evidence from friendly, neutral, and hostile sources establishes that: "
                "Jesus existed, was a Jewish teacher, performed remarkable deeds, was crucified under "
                "Pilate, and was worshipped by His followers as divine. No credible ancient source "
                "denied Jesus' existence. 'We did not follow cleverly devised stories' (2 Peter 1:16)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["2 Peter 1:16", "1 Corinthians 15:3-8", "Luke 1:1-4", "Acts 26:26"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What is the Lord, Liar, or Lunatic trilemma about Jesus?",
            "answer_chirho": (
                "C.S. Lewis's famous trilemma (from 'Mere Christianity') addresses the common "
                "claim that Jesus was 'a great moral teacher but not God.' Lewis argued this is "
                "not a logically available option. Jesus clearly claimed to be God: 'I and the "
                "Father are one' (John 10:30). 'Before Abraham was, I AM' (John 8:58 — using "
                "God's divine name from Exodus 3:14). He accepted worship (John 20:28-29), claimed "
                "authority to forgive sins (Mark 2:5-7), and said 'Anyone who has seen me has seen "
                "the Father' (John 14:9). Given these claims, there are only three possibilities: "
                "(1) LIAR: Jesus knew His claims were false and deliberately deceived people. But "
                "liars do not produce the most profound moral teaching in history or inspire billions "
                "to transformed lives. His ethical teaching and personal character are universally "
                "admired, even by non-Christians. A deliberate fraud does not usually get crucified "
                "for his lies when he could easily retract them. (2) LUNATIC: Jesus sincerely "
                "believed He was God but was mentally ill. But His teachings show extraordinary "
                "wisdom, coherence, and psychological insight. He engaged in sophisticated debates "
                "with trained scholars. His calm composure under trial and torture is not consistent "
                "with delusion. People suffering from grandiose delusions do not produce the "
                "Sermon on the Mount. (3) LORD: Jesus was who He claimed to be — God incarnate. "
                "This is the only option consistent with the evidence of His teaching, character, "
                "miracles, and resurrection. 'You are not yet fifty years old, and you have seen "
                "Abraham!' 'Very truly I tell you, before Abraham was born, I am!' (John 8:57-58). "
                "The title 'great moral teacher' is inadequate. He is either much more or much less."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["John 10:30", "John 8:58", "John 14:9", "John 20:28-29"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What is the evidence for the resurrection of Jesus?",
            "answer_chirho": (
                "The resurrection of Jesus is the foundation of Christian faith (1 Corinthians "
                "15:14-17) and the most well-evidenced miracle in history. The evidence rests on "
                "multiple converging lines. First, the empty tomb: Jesus was publicly executed and "
                "buried in a known tomb belonging to Joseph of Arimathea, a member of the Sanhedrin "
                "(easily verifiable). On Sunday morning, the tomb was empty. The Jewish authorities "
                "never disputed the empty tomb — instead, they claimed the disciples stole the body "
                "(Matthew 28:13), which concedes the tomb was empty. Second, post-mortem appearances: "
                "Jesus appeared to multiple individuals and groups over 40 days — to Mary Magdalene, "
                "to Peter, to the Twelve, to James (Jesus' skeptical brother, who became a church "
                "leader), and to over 500 people at once (1 Corinthians 15:3-8). Paul wrote this "
                "within 25 years, noting most witnesses were still alive — an invitation to verify. "
                "Third, the transformation of the disciples: the men who fled at Jesus' arrest "
                "(Mark 14:50) became bold proclaimers willing to die for their testimony. Something "
                "happened to change them. Fourth, the conversion of skeptics: Paul was a violent "
                "persecutor who became Christianity's greatest missionary. James was a skeptic "
                "during Jesus' ministry (John 7:5) who became the leader of the Jerusalem church. "
                "Fifth, the origin of the church: Christianity exploded in the very city where Jesus "
                "was crucified, within weeks of His death. If the resurrection were false, producing "
                "the body would have ended Christianity immediately. Sixth, the testimony of women: "
                "in a culture that did not accept female testimony, all four Gospels name women as "
                "the first resurrection witnesses — this detail would never have been invented."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["1 Corinthians 15:3-8", "1 Corinthians 15:14-17", "Acts 2:32", "Romans 1:4"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What is the minimal facts approach to the resurrection (Gary Habermas)?",
            "answer_chirho": (
                "Philosopher Gary Habermas developed the 'minimal facts' approach, which argues for "
                "the resurrection using only facts that are accepted by the vast majority of critical "
                "scholars — including skeptical ones. The minimal facts are: (1) Jesus died by "
                "crucifixion. This is accepted by virtually 100% of scholars. Crucifixion was "
                "attested by multiple Christian and non-Christian sources (Josephus, Tacitus). "
                "(2) The disciples sincerely believed Jesus rose and appeared to them. This is "
                "attested by multiple early sources, including Paul's early creed in 1 Corinthians "
                "15:3-5, which scholars date to within 1-5 years of the crucifixion. (3) The church "
                "persecutor Paul was suddenly converted. Paul's transformation from violent persecutor "
                "to the church's greatest missionary requires explanation. (4) The skeptic James "
                "(Jesus' brother) was suddenly converted. James did not believe during Jesus' "
                "ministry (John 7:5) but became leader of the Jerusalem church and died a martyr. "
                "(5) The tomb was empty. While slightly more contested, approximately 75% of scholars "
                "who have published on the subject accept the empty tomb. The question is: what "
                "hypothesis best explains ALL of these facts simultaneously? Habermas has catalogued "
                "over 3,400 scholarly publications on the resurrection and found that naturalistic "
                "alternatives (hallucination, stolen body, swoon theory) each fail to account for "
                "all the facts. Only the resurrection explains the totality of the evidence. This "
                "approach is powerful because it does not require accepting biblical inerrancy — it "
                "uses only facts that critical scholarship already grants. 'If Christ has not been "
                "raised, our preaching is useless and so is your faith' (1 Corinthians 15:14). "
                "But He HAS been raised — and the evidence confirms it."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["1 Corinthians 15:3-5", "1 Corinthians 15:14", "Acts 9:1-22", "Galatians 1:19"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Why are alternative theories about the resurrection (swoon, stolen body, hallucination) inadequate?",
            "answer_chirho": (
                "Every naturalistic alternative to the resurrection has been proposed and thoroughly "
                "refuted. The Swoon Theory claims Jesus did not actually die but merely fainted on "
                "the cross and later revived. Problems: Roman soldiers were execution professionals "
                "— failure to confirm death meant their own execution. Jesus was scourged (often "
                "fatal alone), crucified for hours, pierced with a spear producing 'blood and water' "
                "(John 19:34 — consistent with pericardial effusion, confirming death), and wrapped "
                "in 75 pounds of burial spices. A half-dead man unwrapping himself, rolling a "
                "multi-ton stone, overpowering guards, and then convincing disciples he had "
                "conquered death is medically and psychologically impossible. The Stolen Body Theory "
                "claims the disciples stole the body. Problems: the tomb was guarded (Matthew 27:65-66). "
                "The disciples were scared and hiding (John 20:19). They gained nothing from the "
                "theft — only persecution and death. People do not die for lies they invented. "
                "The Hallucination Theory claims the appearances were hallucinations. Problems: "
                "hallucinations are individual psychiatric events — they are not shared by groups. "
                "Over 500 people do not hallucinate the same thing simultaneously (1 Corinthians "
                "15:6). Hallucinations do not eat fish (Luke 24:42-43) or invite physical touch "
                "(John 20:27). And hallucinations do not explain the empty tomb. The Wrong Tomb "
                "Theory claims everyone went to the wrong tomb. Problems: Joseph of Arimathea knew "
                "his own tomb. The Jewish authorities could have simply gone to the right tomb and "
                "produced the body. The Legend Theory claims the resurrection was a myth that "
                "developed over decades. Problems: the creed in 1 Corinthians 15:3-5 dates to "
                "within 3-5 years — far too early for legend development."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["John 19:34", "1 Corinthians 15:6", "Luke 24:39-43", "John 20:27"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "How is Jesus different from other religious founders?",
            "answer_chirho": (
                "Jesus Christ stands apart from every other religious figure in history in multiple "
                "decisive ways. First, His claims: no other major religious founder claimed to be "
                "God incarnate. Muhammad claimed to be a prophet. Buddha claimed to be an enlightened "
                "teacher. Confucius was a moral philosopher. Moses was a lawgiver and prophet. Only "
                "Jesus said 'I and the Father are one' (John 10:30) and 'Anyone who has seen me has "
                "seen the Father' (John 14:9). Second, His miracles: while other religions report "
                "some wonders, the Gospel miracles are qualitatively different — they are performed "
                "publicly, witnessed by crowds, attested by hostile sources, and culminate in the "
                "resurrection. Third, His death and resurrection: every other religious founder died "
                "and stayed dead. Only Jesus claimed He would rise from the dead (Mark 8:31) and "
                "then did so — evidenced by the empty tomb, post-mortem appearances, and transformed "
                "disciples. Fourth, His sinlessness: even His enemies could not find legitimate "
                "charges against Him (John 18:38). He challenged anyone to convict Him of sin "
                "(John 8:46). No other religious founder made or could sustain such a claim. Fifth, "
                "His teaching: the Sermon on the Mount, the parables, and His ethical teachings "
                "are recognized as the most profound moral instruction ever given. Sixth, His "
                "fulfillment of prophecy: over 300 specific Messianic prophecies, written centuries "
                "before His birth, find precise fulfillment in Jesus. No other figure in any religion "
                "has anything comparable. Seventh, His impact: Jesus has influenced more art, music, "
                "literature, education, medicine, law, and social reform than any other person who "
                "ever lived — and He accomplished this without writing a book, commanding an army, "
                "or holding political office. 'God has highly exalted him and bestowed on him the "
                "name that is above every name' (Philippians 2:9)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["John 10:30", "John 14:9", "Philippians 2:9-11", "John 8:46"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What is the uniqueness of Christ's offer of salvation?",
            "answer_chirho": (
                "Christianity is unique among world religions in that salvation is received as a "
                "free gift of grace, not earned through human effort. Every other religion teaches "
                "some version of 'do this and you will be saved' — follow the Five Pillars, "
                "accumulate good karma, achieve enlightenment through meditation, follow the "
                "Eightfold Path. Christianity alone teaches: 'For it is by grace you have been "
                "saved, through faith — and this is not from yourselves, it is the gift of God — "
                "not by works, so that no one can boast' (Ephesians 2:8-9). This is not merely "
                "a different flavor of religion; it is a fundamentally different category. In "
                "every other system, the burden is on the human to reach up to God through moral "
                "effort, ritual, or spiritual practice. In Christianity, God reaches down to "
                "humanity through incarnation and sacrifice. The Cross demonstrates that humanity's "
                "problem (sin) is too severe for human solutions — it required divine intervention. "
                "We are not slightly flawed beings who need moral improvement; we are spiritually "
                "dead (Ephesians 2:1) who need resurrection. Only God can raise the dead. Christ "
                "accomplished what we could never accomplish for ourselves: perfect obedience to "
                "God's law (active righteousness) and payment for our sins through His death "
                "(passive righteousness). This righteousness is credited to all who believe: "
                "'God made him who had no sin to be sin for us, so that in him we might become "
                "the righteousness of God' (2 Corinthians 5:21). The gospel is not good advice "
                "but good news — not what we must do for God, but what God has done for us. "
                "'For God so loved the world that he gave his one and only Son, that whoever "
                "believes in him shall not perish but have eternal life' (John 3:16)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Ephesians 2:8-9", "2 Corinthians 5:21", "John 3:16", "Romans 6:23"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Why is Jesus the only way to God (John 14:6)?",
            "answer_chirho": (
                "Jesus' claim 'I am the way and the truth and the life. No one comes to the Father "
                "except through me' (John 14:6) is one of the most controversial statements ever "
                "made, but it follows logically from several realities. First, if God exists and has "
                "revealed Himself, His revelation defines truth — we don't get to negotiate with "
                "reality. If Jesus is who He claimed to be (God incarnate, demonstrated by the "
                "resurrection), then His words carry absolute authority. Second, the problem of sin "
                "demands a specific solution. A doctor does not prescribe random treatments; the "
                "disease determines the cure. Human sin against an infinite God requires an infinite "
                "sacrifice — only the God-man Jesus could provide this. Third, exclusivity is not "
                "unique to Christianity — it is inherent in all truth claims. Mathematics is "
                "'exclusive': 2+2=4, not 5, not 3.9. The law of non-contradiction is 'exclusive': "
                "contradictory claims cannot both be true. If Christianity is true, religions that "
                "contradict it cannot also be true — this is not arrogance but logic. Fourth, "
                "Christianity is exclusive in the offer but inclusive in the invitation. ANYONE "
                "can come — 'whoever believes' (John 3:16). There are no ethnic, social, economic, "
                "or educational requirements. The invitation is the most inclusive in the world; "
                "only the path is exclusive. Fifth, the exclusivity of Christ is an expression of "
                "God's love, not His restriction. A lifeguard who says 'I am the only one who can "
                "save you' is not arrogant — he is telling the truth and offering rescue. 'Salvation "
                "is found in no one else, for there is no other name under heaven given to mankind "
                "by which we must be saved' (Acts 4:12)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["John 14:6", "Acts 4:12", "John 3:16", "1 Timothy 2:5"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Is the virgin birth of Jesus fact or myth?",
            "answer_chirho": (
                "The virgin birth of Jesus is attested by two independent Gospel sources (Matthew "
                "1:18-25 and Luke 1:26-38) and has been a core Christian doctrine since the earliest "
                "creeds. Several points support its historical credibility. First, the sources are "
                "independent. Matthew and Luke clearly drew on different sources for their birth "
                "narratives (Matthew focuses on Joseph's perspective; Luke on Mary's), yet both "
                "attest to the virgin conception. Independent attestation is a strong historical "
                "criterion. Second, the doctrine was an embarrassment, not an advantage. In the "
                "ancient world, a virgin birth claim was more likely to generate suspicion of "
                "illegitimacy than reverence. The Talmud's hostile reference to Jesus' birth "
                "(suggesting illegitimacy) confirms the early church was making this claim publicly. "
                "No one invents an embarrassing detail. Third, the virgin birth is theologically "
                "necessary. If Jesus is both truly God and truly human, the virgin conception "
                "provides the means: fully human through Mary, yet uniquely conceived by the Holy "
                "Spirit. Fourth, the Old Testament prophesied it: 'The virgin will conceive and "
                "give birth to a son, and will call him Immanuel' (Isaiah 7:14). The LXX translates "
                "the Hebrew 'almah' as 'parthenos' (virgin), indicating pre-Christian Jewish "
                "understanding of this prophecy. Fifth, the objection that virgin births appear "
                "in pagan myths misunderstands the parallels. Pagan myths describe gods having "
                "physical relations with women — not a virgin conceiving by the Holy Spirit. The "
                "biblical account is qualitatively different and rooted in monotheistic theology. "
                "'The Holy Spirit will come on you, and the power of the Most High will overshadow "
                "you. So the holy one to be born will be called the Son of God' (Luke 1:35)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Isaiah 7:14", "Luke 1:35", "Matthew 1:22-23", "Galatians 4:4"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "How did Jesus fulfill Old Testament Messianic prophecies?",
            "answer_chirho": (
                "Jesus fulfilled over 300 specific Messianic prophecies written centuries before "
                "His birth. This is without parallel in any other religion or historical figure. "
                "Key fulfillments include: Born of a virgin (Isaiah 7:14 / Matthew 1:22-23). Born "
                "in Bethlehem (Micah 5:2 / Matthew 2:1). From the tribe of Judah (Genesis 49:10 / "
                "Matthew 1:2-3). From the line of David (2 Samuel 7:12-13 / Luke 3:31). Called out "
                "of Egypt (Hosea 11:1 / Matthew 2:15). Preceded by a messenger (Malachi 3:1 / "
                "Mark 1:2-4). Entered Jerusalem on a donkey (Zechariah 9:9 / Matthew 21:1-11). "
                "Betrayed by a friend (Psalm 41:9 / John 13:18-26). Sold for 30 pieces of silver "
                "(Zechariah 11:12-13 / Matthew 26:15). Money used to buy a potter's field "
                "(Zechariah 11:13 / Matthew 27:7). Silent before His accusers (Isaiah 53:7 / "
                "Matthew 27:12-14). Hands and feet pierced (Psalm 22:16 / John 20:25-27). "
                "Crucified with criminals (Isaiah 53:12 / Mark 15:27). Garments divided by lot "
                "(Psalm 22:18 / John 19:23-24). Given gall and vinegar (Psalm 69:21 / John 19:29). "
                "No bones broken (Psalm 34:20 / John 19:33-36). Side pierced (Zechariah 12:10 / "
                "John 19:34). Buried in a rich man's tomb (Isaiah 53:9 / Matthew 27:57-60). "
                "Rose from the dead (Psalm 16:10 / Acts 2:31). Many of these were beyond Jesus' "
                "control to arrange (birthplace, manner of death, soldiers' actions, burial "
                "arrangements). The Dead Sea Scrolls confirm that these prophecies existed before "
                "Jesus. 'Beginning with Moses and all the Prophets, he explained to them what was "
                "said in all the Scriptures concerning himself' (Luke 24:27)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Luke 24:27", "Isaiah 53:1-12", "Psalm 22:1-18", "Micah 5:2"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Did Jesus actually claim to be God?",
            "answer_chirho": (
                "Some skeptics claim Jesus never claimed divinity and that this was a later church "
                "invention. But the Gospels record numerous clear divine claims, and the earliest "
                "Christian sources confirm belief in Jesus' deity. Jesus' direct claims include: "
                "'I and the Father are one' (John 10:30) — His Jewish audience understood this as "
                "a claim to deity and tried to stone Him for blasphemy (10:33). 'Before Abraham was "
                "born, I am' (John 8:58) — using the divine name 'I AM' (Exodus 3:14). 'Anyone who "
                "has seen me has seen the Father' (John 14:9). He accepted Thomas's worship: 'My "
                "Lord and my God!' (John 20:28-29). Jesus' implicit claims are equally striking: "
                "He claimed authority to forgive sins — something only God can do (Mark 2:5-7). "
                "He claimed authority over the Sabbath, which God instituted (Mark 2:28). He claimed "
                "He would judge all humanity at the end of time (Matthew 25:31-46). He accepted "
                "worship on multiple occasions (Matthew 14:33, 28:9, 28:17). He placed His own "
                "words on par with God's: 'You have heard that it was said... But I tell you' "
                "(Matthew 5:21-22). The earliest Christian writings outside the Gospels confirm "
                "this: Paul's letter to the Philippians (c. 60-62 AD) contains a pre-Pauline hymn "
                "(2:5-11) declaring Jesus equal with God. The creed in 1 Corinthians 15:3-5 calls "
                "Jesus 'Christ' (Messiah/Anointed One) within 3-5 years of the crucifixion. Pliny "
                "the Younger (112 AD) reports Christians singing hymns to Christ 'as to a god.' "
                "The claim that Jesus' deity was a late invention contradicts the earliest evidence."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["John 10:30", "John 8:58", "John 20:28-29", "Philippians 2:5-11"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What is the significance of the empty tomb?",
            "answer_chirho": (
                "The empty tomb is one of the strongest evidences for the resurrection, accepted "
                "by approximately 75% of scholars who have published on the subject — including "
                "many who are not Christians. Several factors make the empty tomb historically "
                "certain. First, the tomb's location was known. Joseph of Arimathea, a member of "
                "the Sanhedrin (the Jewish ruling council that condemned Jesus), donated his tomb "
                "for Jesus' burial (Mark 15:43-46). As a public figure, his involvement could not "
                "have been fabricated — the Sanhedrin members were known. Second, the Jewish "
                "authorities' response confirms the empty tomb. When the disciples proclaimed the "
                "resurrection, the authorities did not say 'The tomb is not empty — go look.' "
                "Instead, they claimed the disciples stole the body (Matthew 28:13). This is an "
                "admission that the tomb was indeed empty. Third, the tomb was secured. Matthew "
                "records a guard was posted and the tomb was sealed (Matthew 27:62-66). The "
                "authorities took precautions specifically because Jesus had predicted His "
                "resurrection. Fourth, women were the first witnesses. In 1st-century Jewish "
                "culture, women's testimony was not accepted in court. If the empty tomb story "
                "were invented, male disciples would have been named as the first witnesses. The "
                "embarrassing detail of female witnesses is a powerful indicator of historical "
                "authenticity. Fifth, the earliest Christian preaching centered in Jerusalem — the "
                "very city where Jesus was buried. The resurrection could not have been proclaimed "
                "in Jerusalem if the body were still in the tomb. Anyone could have walked to the "
                "tomb and disproved the claim. 'He is not here; he has risen, just as he said' "
                "(Matthew 28:6)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Matthew 28:6", "Mark 15:43-46", "Matthew 28:13", "Luke 24:2-3"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "How does Jesus' resurrection differ from other resurrection claims?",
            "answer_chirho": (
                "Jesus' resurrection is categorically different from any other claim of resurrection "
                "in religious history. First, it was predicted in advance. Jesus repeatedly told His "
                "disciples He would be killed and rise on the third day (Mark 8:31, 9:31, 10:33-34). "
                "No other religious figure made and fulfilled such a prediction. Second, it was "
                "physical and bodily. Jesus ate food (Luke 24:42-43), invited physical touch "
                "(John 20:27), and was recognized by those who knew Him. This is not a ghostly "
                "apparition or a 'spiritual' resurrection — it was physical transformation. Third, "
                "it was publicly proclaimed from the beginning, in the very city where the "
                "crucifixion occurred. The disciples did not go to some distant land with an "
                "unverifiable story; they proclaimed the resurrection in Jerusalem weeks after the "
                "event, where anyone could investigate. Fourth, it was attested by multiple "
                "independent witnesses: Mary Magdalene, Peter, the Twelve, James, 500+ at once, "
                "and Paul (1 Corinthians 15:5-8). Fifth, it was confirmed by hostile witnesses "
                "through their response: the Jewish authorities bribed the guards to say the body "
                "was stolen (Matthew 28:11-15), implicitly confirming the empty tomb. Sixth, it "
                "transformed cowards into martyrs. The disciples fled at Jesus' arrest; after "
                "the resurrection, they boldly proclaimed His risen life at the cost of their own. "
                "Other 'resurrection' stories in religion are either mythological (Osiris — a "
                "cyclical nature myth), late (post-Christian), or unattested by eyewitness testimony. "
                "None match the historical evidence for Jesus' resurrection. 'He has given proof "
                "of this to everyone by raising him from the dead' (Acts 17:31)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Acts 17:31", "1 Corinthians 15:5-8", "Luke 24:39-43", "Mark 8:31"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What did the earliest Christians believe about Jesus?",
            "answer_chirho": (
                "The earliest Christian beliefs about Jesus can be traced to within months or years "
                "of the crucifixion — not decades or centuries as some critics claim. The most "
                "important early creed is 1 Corinthians 15:3-5: 'For what I received I passed on "
                "to you as of first importance: that Christ died for our sins according to the "
                "Scriptures, that he was buried, that he was raised on the third day according to "
                "the Scriptures, and that he appeared to Cephas, and then to the Twelve.' Paul "
                "says he 'received' this — it was already formulated when he learned it. Scholars "
                "date this creed to within 1-5 years of the crucifixion (c. 30-35 AD). It affirms: "
                "Jesus' atoning death, His burial, His physical resurrection, and His appearances "
                "to named witnesses. The Philippians hymn (2:6-11) is another pre-Pauline creed "
                "that declares Jesus existed 'in the form of God' and was 'equal with God.' "
                "Early church fathers confirm these beliefs: Clement of Rome (c. 96 AD) wrote of "
                "Jesus' resurrection. Ignatius of Antioch (c. 107 AD) affirmed Jesus was 'truly "
                "God' who 'truly suffered' and 'truly rose from the dead.' Polycarp (c. 110 AD), "
                "a direct disciple of the apostle John, affirmed the bodily resurrection. The "
                "Didache (c. 50-120 AD) calls Jesus 'Lord.' These beliefs were not late inventions "
                "developed over centuries — they were present from Christianity's earliest moments. "
                "As Larry Hurtado demonstrates in 'Lord Jesus Christ' (2003), the worship of Jesus "
                "as divine was a 'Big Bang' — it appeared suddenly and fully formed, not gradually. "
                "'Jesus Christ is the same yesterday and today and forever' (Hebrews 13:8)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["1 Corinthians 15:3-5", "Philippians 2:6-11", "Hebrews 13:8", "1 John 1:1-3"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Did Jesus' disciples really die for their belief in the resurrection?",
            "answer_chirho": (
                "The willingness of the apostles to suffer and die for their testimony of the "
                "resurrection is one of the strongest arguments for its truth. The key distinction: "
                "many people die for beliefs they think are true (martyrs of all religions). But the "
                "apostles were in a unique position — they claimed to be EYEWITNESSES of the risen "
                "Jesus. They either saw Him or they didn't. If they didn't, they knew they were "
                "lying and would have gained nothing by dying for a lie. The evidence for apostolic "
                "suffering is strong. Paul describes his sufferings extensively (2 Corinthians "
                "11:23-28) and was eventually executed in Rome (c. 64-67 AD). James son of Zebedee "
                "was killed by Herod (Acts 12:2 — the only apostolic martyrdom recorded in Scripture). "
                "Peter was crucified in Rome (tradition recorded by Clement of Rome c. 96 AD and "
                "Tertullian c. 200 AD). James the brother of Jesus was thrown from the Temple "
                "pinnacle (recorded by both Josephus and Hegesippus). Thomas was killed in India "
                "(recorded in multiple early sources). While some individual martyrdom accounts "
                "rest on later tradition, what is historically certain is that the apostles suffered "
                "greatly for their proclamation and none recanted. The transformation of the "
                "disciples — from terrified fugitives hiding behind locked doors (John 20:19) to "
                "bold proclaimers who 'filled Jerusalem' with their teaching (Acts 5:28) — demands "
                "an explanation. Something extraordinary happened to change them. Their own "
                "explanation: 'We are witnesses of everything he did... God raised him from the "
                "dead. We are witnesses of this' (Acts 10:39-41)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Acts 12:2", "2 Corinthians 11:23-28", "Acts 5:28-29", "Acts 10:39-41"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Was Jesus merely a copy of pagan dying-and-rising gods?",
            "answer_chirho": (
                "The claim that Jesus was borrowed from pagan dying-and-rising god myths (Osiris, "
                "Mithras, Dionysus, Attis, etc.) was popularized in the early 20th century by the "
                "'History of Religions' school but has been thoroughly debunked by modern scholarship. "
                "Leading scholar Jonathan Z. Smith concluded that 'the category of dying and rising "
                "gods, once a major topic of scholarly investigation, must be understood to have been "
                "largely a misnomer based on imaginative reconstructions and generic parallels.' "
                "The alleged parallels dissolve under scrutiny. Osiris: not a resurrection but a "
                "reanimation to rule the underworld — not a return to bodily life on earth. Mithras: "
                "born from a rock, not a virgin; no death-and-resurrection narrative exists in "
                "any Mithraic source. Attis: in the earliest version, dies from castration and "
                "remains dead; later versions mentioning transformation post-date Christianity. "
                "Dionysus: torn apart and reassembled — this is not resurrection but reconstitution, "
                "and the parallels are superficial. Furthermore, the earliest Christians were "
                "monotheistic Jews for whom pagan myths were abominations, not templates. Paul "
                "explicitly warned against 'myths' (1 Timothy 1:4, Titus 1:14). The New Testament "
                "is grounded in Jewish theology and Hebrew Scriptures, not Greco-Roman mythology. "
                "The Jesus story is rooted in specific history — datable to Pontius Pilate's "
                "governorship, attested by eyewitnesses, verifiable by contemporaries. This is "
                "categorically different from timeless myths set in a mythological past. 'We did "
                "not follow cleverly devised stories when we told you about the coming of our "
                "Lord Jesus Christ in power, but we were eyewitnesses of his majesty' (2 Peter 1:16)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["2 Peter 1:16", "1 Timothy 1:4", "1 Corinthians 15:14", "Acts 26:26"],
            "difficulty_chirho": "advanced",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "What is the historical significance of the conversion of Paul?",
            "answer_chirho": (
                "The conversion of Saul of Tarsus (Paul) is one of the most well-documented and "
                "significant events in early Christianity. Paul was not a neutral observer — he was "
                "an active, violent persecutor of the church. He describes himself as 'extremely "
                "zealous for the traditions of my fathers' (Galatians 1:14), a Pharisee who "
                "'persecuted the church of God and tried to destroy it' (Galatians 1:13). He "
                "approved Stephen's execution (Acts 8:1) and received authorization to arrest "
                "Christians (Acts 9:1-2). Then, suddenly and dramatically, he became Christianity's "
                "most powerful advocate, enduring imprisonment, beatings, shipwreck, and eventual "
                "execution for the faith he once tried to destroy. What accounts for this radical "
                "transformation? Paul's own explanation is simple: 'Last of all he appeared to me "
                "also' (1 Corinthians 15:8). He claims to have encountered the risen Christ on "
                "the road to Damascus. No naturalistic explanation adequately accounts for Paul's "
                "conversion. Hallucination? Paul was not grieving or expecting a vision — he was "
                "actively hostile. Psychological breakdown? Paul's post-conversion writings show "
                "extraordinary intellectual clarity and coherence. Gradual disillusionment? Paul "
                "describes the change as sudden and dramatic. Financial gain? Paul went from "
                "comfortable Pharisaic status to poverty and suffering. The sheer implausibility "
                "of a violent persecutor becoming the church's greatest missionary — and then "
                "suffering and dying for the same faith he tried to destroy — constitutes powerful "
                "evidence that something extraordinary happened to him. Paul staked his life on it: "
                "'For to me, to live is Christ and to die is gain' (Philippians 1:21)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["1 Corinthians 15:8", "Galatians 1:13-14", "Philippians 1:21", "Acts 9:1-22"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "historical_evidence",
            "question_chirho": "Why did Christianity explode in growth despite severe persecution?",
            "answer_chirho": (
                "The rapid spread of Christianity in its first three centuries is a historical "
                "phenomenon that demands explanation. Within 300 years of Jesus' death, Christianity "
                "grew from a handful of Jewish followers to the dominant religion of the Roman "
                "Empire — despite lacking political power, military force, social status, or wealth, "
                "and despite facing intense persecution. The Roman Empire periodically executed "
                "Christians (Nero's persecutions, Domitian, Decius, Diocletian), yet the church "
                "grew fastest during persecutions. Sociologist Rodney Stark estimates Christianity "
                "grew at approximately 40% per decade — from about 1,000 in 40 AD to over 6 "
                "million by 300 AD. What explains this? First, the resurrection. The early "
                "Christians were convinced they had witnessed something extraordinary, and their "
                "conviction was contagious. Second, the quality of Christian community. Christians "
                "cared for the sick during plagues (when pagans abandoned their own families), "
                "rescued exposed infants, treated women with unprecedented dignity, and formed "
                "inclusive communities that crossed ethnic and social boundaries. Third, the "
                "courage of martyrs. Tertullian observed that 'the blood of the martyrs is the "
                "seed of the church.' Witnesses to Christian courage under persecution were often "
                "converted. Fourth, the transforming power of the Gospel. Changed lives are the "
                "most compelling evidence. Paul's message was 'not with wise and persuasive words, "
                "but with a demonstration of the Spirit's power' (1 Corinthians 2:4). The church's "
                "growth was against every sociological prediction — it had no army, no wealth, and "
                "opposed the world's greatest empire. Yet Jesus predicted: 'I will build my church, "
                "and the gates of Hades will not overcome it' (Matthew 16:18)."
            ),
            "topic_chirho": "jesus_christ",
            "scripture_chirho": ["Matthew 16:18", "1 Corinthians 2:4", "Acts 5:38-39", "Acts 17:6"],
            "difficulty_chirho": "basic",
        },
    ]


def build_worldview_comparisons_chirho() -> list[dict]:
    """Build entries for worldview comparisons (~15 entries)."""
    return [
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity compare to atheism/materialism?",
            "answer_chirho": (
                "Atheistic materialism holds that matter and energy are all that exist — there is no "
                "God, no soul, no afterlife, and no objective meaning or morality. While this "
                "worldview presents itself as 'scientific,' it faces severe philosophical problems "
                "that Christianity resolves. First, materialism cannot account for the origin of "
                "the universe. If matter is all that exists, where did matter come from? The Big "
                "Bang shows the universe began — something cannot come from nothing without a cause. "
                "Second, materialism cannot ground objective morality. If we are merely rearranged "
                "atoms, moral claims are just chemical reactions — the Holocaust is not objectively "
                "evil, merely evolutionarily disadvantageous. Yet we KNOW it was evil. Third, "
                "materialism cannot explain consciousness. How does subjective experience arise "
                "from objective matter? The 'hard problem of consciousness' remains unsolved on "
                "materialism. Fourth, materialism is self-defeating: if our thoughts are entirely "
                "determined by physics and chemistry, we have no reason to trust them as reliable — "
                "including the thought that materialism is true (Lewis's argument from reason). "
                "Fifth, materialism provides no ultimate purpose or hope. If the universe will end "
                "in heat death, all human achievement is ultimately meaningless. Bertrand Russell "
                "honestly faced this: 'The whole temple of Man's achievement must inevitably be "
                "buried beneath the debris of a universe in ruins.' Christianity, by contrast, "
                "provides: a rational origin (a Creator), objective morality (grounded in God's "
                "nature), an explanation for consciousness (made in God's image), reliable reasoning "
                "(designed by a rational God), and ultimate purpose and hope (eternal life with "
                "our Creator). 'For in him we live and move and have our being' (Acts 17:28)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["Acts 17:28", "Romans 1:20-22", "Psalm 14:1", "Colossians 1:16-17"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What are the key differences between Christianity and Islam?",
            "answer_chirho": (
                "Christianity and Islam share some surface similarities (monotheism, Abraham, Jesus "
                "as a prophet) but differ on foundational issues. First, the nature of God: "
                "Christianity teaches that God is triune (Father, Son, Holy Spirit) — one God in "
                "three persons, a community of love. Islam teaches strict unitarian monotheism "
                "(tawhid) and considers the Trinity blasphemous (Surah 5:73). Second, the deity "
                "of Christ: Christianity teaches Jesus is God incarnate (John 1:1,14). Islam teaches "
                "Jesus was a prophet — a great one, but merely human (Surah 4:171). Third, the "
                "crucifixion: Christianity holds the crucifixion as the central event in history, "
                "where God atoned for human sin. Islam denies Jesus was crucified, claiming it was "
                "made to appear so (Surah 4:157-158) — contradicting the best-attested fact about "
                "Jesus in both Christian and secular sources. Fourth, salvation: Christianity teaches "
                "salvation by grace through faith (Ephesians 2:8-9). Islam teaches salvation through "
                "submission and works, with no assurance of outcome (even Muhammad said he did not "
                "know his own fate — Surah 46:9). Fifth, textual reliability: the New Testament is "
                "attested by over 25,000 manuscripts dating within decades of the originals. The "
                "Quran's manuscript tradition is less diverse; Uthman standardized one text and "
                "burned the variants (c. 650 AD). Sixth, Muhammad and Jesus: Jesus performed "
                "miracles, lived a sinless life, and rose from the dead. Muhammad performed no "
                "miracles according to the Quran (Surah 29:50-51), was a military commander, and "
                "died and remained dead. 'Who is the liar? It is whoever denies that Jesus is the "
                "Christ' (1 John 2:22). The differences are not trivial — they concern the nature "
                "of God, the means of salvation, and the identity of Jesus."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["John 1:1", "John 1:14", "Ephesians 2:8-9", "1 John 2:22"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity differ from Buddhism on suffering and salvation?",
            "answer_chirho": (
                "Buddhism and Christianity both address human suffering, but their diagnoses and "
                "remedies are fundamentally different. Buddhism's First Noble Truth is that life is "
                "dukkha (suffering/unsatisfactoriness). The cause of suffering is tanha (craving, "
                "attachment). The solution is the cessation of desire through the Eightfold Path, "
                "leading to Nirvana — the extinction of self and desire. Christianity agrees that "
                "life involves suffering, but the cause is sin (rebellion against God), not desire "
                "itself. Desire is not evil; God created us with desires for love, beauty, meaning, "
                "and Himself (Ecclesiastes 3:11). The problem is disordered desire — wanting good "
                "things more than God or wanting wrong things. The solution is not the extinction "
                "of self but the transformation of self through Christ. Key differences: (1) God: "
                "Buddhism is non-theistic (original Buddhism has no creator God). Christianity is "
                "grounded in a personal, loving Creator who is intimately involved with His creation. "
                "(2) Self: Buddhism teaches anatta (no-self) — the self is an illusion to be "
                "dissolved. Christianity teaches that the self is real, made in God's image, "
                "infinitely valuable, and destined for eternal relationship with God. (3) Salvation: "
                "Buddhism offers self-salvation through human effort (meditation, moral discipline). "
                "Christianity offers divine rescue through grace. (4) The problem: Buddhism sees "
                "suffering as the fundamental problem. Christianity sees sin (broken relationship "
                "with God) as the fundamental problem — suffering is a symptom. (5) Hope: Buddhism "
                "offers Nirvana (cessation). Christianity offers resurrection, restored creation, "
                "and eternal communion with God. 'I have come that they may have life, and have it "
                "to the full' (John 10:10). Christ does not extinguish life — He fulfills it."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["John 10:10", "Ecclesiastes 3:11", "Romans 8:28", "Revelation 21:4-5"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity differ from Hinduism?",
            "answer_chirho": (
                "Christianity and Hinduism differ on virtually every fundamental theological point. "
                "On God: Christianity teaches strict monotheism — one personal God who is distinct "
                "from creation. Hinduism encompasses pantheism (Brahman is all), polytheism (millions "
                "of gods), and henotheism (worship of one god while acknowledging others). The "
                "Christian God is personal; Brahman in its highest form (nirguna Brahman) is "
                "impersonal and beyond attributes. On creation: Christianity teaches God created "
                "the world 'ex nihilo' (from nothing) — the world is real, good, and distinct "
                "from God (Genesis 1:1,31). Hindu Advaita Vedanta teaches the material world is "
                "maya (illusion) and that only Brahman is real. On the human problem: Christianity "
                "teaches sin — moral rebellion against God requiring atonement. Hinduism teaches "
                "avidya (ignorance of one's true divine nature) and karma (the moral law of cause "
                "and effect across reincarnation cycles). On salvation: Christianity teaches grace — "
                "God rescues us at the Cross; we receive salvation by faith. Hinduism teaches "
                "moksha (liberation from the cycle of reincarnation) through jnana (knowledge), "
                "bhakti (devotion), karma (works), or raja (meditation) yoga — self-effort across "
                "potentially millions of lifetimes. On history: Christianity is linear — history "
                "has a beginning, a climax (the Cross), and an end (Christ's return). Hinduism is "
                "cyclical — endless repetition of cosmic ages. On human worth: Christianity teaches "
                "every person is made in God's image with equal dignity (Genesis 1:27). The caste "
                "system, while not endorsed by all Hindus, emerged from Hindu theology. "
                "'For there is one God and one mediator between God and mankind, the man Christ "
                "Jesus' (1 Timothy 2:5)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["1 Timothy 2:5", "Genesis 1:1", "Genesis 1:27", "Isaiah 45:5-6"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity respond to New Age spirituality?",
            "answer_chirho": (
                "New Age spirituality is a diverse movement that typically includes: pantheism "
                "(God is everything), monism (all is one), reincarnation, karma, spiritual "
                "evolution, channeling, crystals, astrology, and the idea that we are all divine. "
                "It appeals to modern seekers because it offers spirituality without moral "
                "accountability, transcendence without a personal God, and self-improvement without "
                "repentance. However, Christianity differs fundamentally. First, God and creation "
                "are distinct. The Bible teaches that God is the Creator, separate from His creation "
                "(Genesis 1:1, Isaiah 45:12). Pantheism ('all is God') confuses the Creator with "
                "the creation — which Paul calls exchanging 'the truth about God for a lie' and "
                "worshipping 'created things rather than the Creator' (Romans 1:25). Second, we "
                "are not divine. The New Age teaches 'you are God' or 'the divine spark is within "
                "you.' The Bible teaches we are created beings, made in God's image but not God "
                "ourselves. The original temptation was precisely this: 'You will be like God' "
                "(Genesis 3:5). Third, reincarnation contradicts Scripture: 'People are destined to "
                "die once, and after that to face judgment' (Hebrews 9:27). We do not get infinite "
                "chances; this life matters eternally. Fourth, karma contradicts grace. Karma teaches "
                "you get what you deserve — an impersonal law of moral cause and effect. The Gospel "
                "teaches you get what you do NOT deserve — mercy, forgiveness, and eternal life as "
                "a free gift (Ephesians 2:8-9). Fifth, New Age practices (channeling, divination, "
                "mediumship) are explicitly forbidden in Scripture (Deuteronomy 18:10-12). These "
                "are not neutral spiritual practices; they open doors to deception. 'Test the "
                "spirits to see whether they are from God' (1 John 4:1)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["Romans 1:25", "Genesis 3:5", "Hebrews 9:27", "Deuteronomy 18:10-12"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity differ from secular humanism?",
            "answer_chirho": (
                "Secular humanism holds that human beings can live meaningful, ethical lives without "
                "belief in God or the supernatural. It values reason, science, democracy, human "
                "rights, and compassion. Christians can affirm much of what humanism values (reason, "
                "human dignity, compassion) while recognizing that humanism cannot adequately ground "
                "these values without God. First, human dignity: secular humanism affirms human "
                "rights and dignity but cannot explain WHY humans have special worth. If we are "
                "merely evolved animals — slightly more complex arrangements of atoms — on what "
                "basis do we have 'inherent dignity'? Christianity grounds human dignity in the "
                "imago Dei: we are made in the image of God (Genesis 1:27). Second, morality: "
                "secular humanism promotes moral behavior but cannot ground objective morality. If "
                "morality is merely a human convention, it carries no binding authority. The strongest "
                "humanist values (human rights, equality, justice) historically arose from Christian "
                "foundations — as secular historian Tom Holland demonstrates in 'Dominion' (2019). "
                "Third, meaning: secular humanism encourages creating personal meaning, but in a "
                "universe destined for heat death, any meaning we create is ultimately illusory. "
                "Christianity provides cosmic meaning: we are created for relationship with God "
                "and for eternal purposes. Fourth, hope: secular humanism offers no hope beyond "
                "death. Christianity offers resurrection and eternal life. Fifth, the problem of "
                "evil: humanism can describe evil but cannot explain why the universe SHOULD be "
                "better than it is. Christianity explains both the reality of evil (the Fall) and "
                "the hope of redemption (the Cross and coming restoration). 'For what will it "
                "profit a man if he gains the whole world and forfeits his soul?' (Matthew 16:26)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["Genesis 1:27", "Matthew 16:26", "Ecclesiastes 12:13-14", "Romans 2:14-15"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity differ from Mormonism?",
            "answer_chirho": (
                "The Church of Jesus Christ of Latter-day Saints (Mormonism) uses Christian "
                "terminology but teaches fundamentally different doctrines. Understanding these "
                "differences is essential. On God: Christianity teaches there is one God, eternally "
                "existing in three persons (Deuteronomy 6:4, Isaiah 44:6). Mormonism teaches that "
                "God the Father was once a man who progressed to godhood (Lorenzo Snow couplet: "
                "'As man now is, God once was; as God now is, man may be'). Mormonism teaches the "
                "existence of multiple gods (henotheism). On Jesus: Christianity teaches Jesus is "
                "eternally God, the Second Person of the Trinity (John 1:1). Mormonism teaches "
                "Jesus is a spirit child of Heavenly Father and Heavenly Mother, the spirit brother "
                "of Lucifer, who achieved godhood. On salvation: Christianity teaches salvation by "
                "grace through faith alone (Ephesians 2:8-9). Mormonism teaches that grace is "
                "necessary but not sufficient — 'it is by grace that we are saved, after all we "
                "can do' (2 Nephi 25:23). Works (temple ordinances, tithing, obedience) are "
                "required for 'exaltation' (the highest level of Mormon salvation). On Scripture: "
                "Christianity holds the Bible as the final, complete revelation (Revelation 22:18-19). "
                "Mormonism adds the Book of Mormon, Doctrine and Covenants, and Pearl of Great Price, "
                "claiming the Bible has been corrupted. However, the Book of Mormon lacks any "
                "archaeological support — no cities, coins, peoples, or artifacts from the civilizations "
                "it describes have been found, despite over a century of searching. DNA evidence "
                "contradicts the claim that Native Americans descended from Israelites. 'But even "
                "if we or an angel from heaven should preach a gospel other than the one we preached "
                "to you, let them be under God's curse!' (Galatians 1:8)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["Galatians 1:8", "Isaiah 44:6", "Deuteronomy 6:4", "John 1:1"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "How does Christianity differ from Jehovah's Witnesses?",
            "answer_chirho": (
                "Jehovah's Witnesses (the Watchtower Society) claim to be Christian but deviate "
                "from historic Christianity on essential doctrines. On the Trinity: Christianity "
                "teaches one God in three co-equal, co-eternal persons. JWs deny the Trinity, "
                "teaching that Jehovah alone is God, Jesus is Michael the archangel (a created "
                "being), and the Holy Spirit is an impersonal force. However, Scripture attributes "
                "divine titles, worship, and attributes to Jesus (John 1:1, Hebrews 1:8, "
                "Revelation 5:13-14) and to the Holy Spirit (Acts 5:3-4, 2 Corinthians 3:17). "
                "On the deity of Christ: JWs claim Jesus is 'a god' (their New World Translation "
                "renders John 1:1 as 'the Word was a god'). But this is grammatically unjustified — "
                "Greek scholars across the theological spectrum reject this rendering. Thomas called "
                "Jesus 'My Lord and my God!' (John 20:28) and Jesus accepted this worship. On "
                "salvation: JWs teach that only 144,000 people go to heaven (the 'anointed class') "
                "while the rest hope for paradise on earth. But Revelation 7:9 describes 'a great "
                "multitude that no one could count' from every nation in heaven. On the resurrection: "
                "JWs deny the bodily resurrection of Jesus, teaching He was raised as a spirit "
                "creature. But Jesus said, 'Look at my hands and my feet. It is I myself! Touch "
                "me and see; a ghost does not have flesh and bones, as you see I have' (Luke 24:39). "
                "On blood transfusions: JWs refuse blood transfusions based on Acts 15:29, but "
                "this passage refers to the Jewish dietary practice of consuming blood, not to "
                "medical procedures. On failed prophecies: the Watchtower predicted Armageddon in "
                "1914, 1925, and 1975 — all failed. 'If what a prophet proclaims in the name of "
                "the LORD does not take place, that is a message the LORD has not spoken' "
                "(Deuteronomy 18:22)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["John 1:1", "John 20:28", "Luke 24:39", "Deuteronomy 18:22"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Is Christianity exclusive? How can there be only one way in a pluralistic world?",
            "answer_chirho": (
                "The claim that Christianity is arrogant for asserting exclusive truth is itself an "
                "exclusive truth claim — it claims to know that no religion can be exclusively true. "
                "This is the 'pluralism paradox': the statement 'all religions are equally valid' is "
                "itself a religious/philosophical claim that excludes all religions that claim "
                "exclusivity. It is not a neutral position; it is a positive assertion that must be "
                "defended. Every worldview is exclusive. Atheism excludes theism. Islam excludes "
                "polytheism. Buddhism excludes the existence of a creator God. The question is not "
                "WHETHER truth is exclusive but WHICH exclusive claim is true. Christianity's "
                "exclusivity is not arbitrary arrogance but logical necessity. The world's religions "
                "make contradictory claims: Christianity says God is triune; Islam says God is "
                "strictly unitarian; Buddhism says there is no creator God; Hinduism offers millions "
                "of gods. These cannot all be true simultaneously (law of non-contradiction). Either "
                "God is personal or impersonal — not both. Either Jesus rose from the dead or He "
                "didn't. Either salvation is by grace or by works. The fact that sincere people "
                "hold different views does not make all views true — sincere people can be sincerely "
                "wrong. What makes Christianity's exclusive claim credible is the evidence supporting "
                "it: the cosmological and moral arguments for God, the reliability of Scripture, "
                "the historical evidence for the resurrection, and the transformative power of the "
                "Gospel. Moreover, Christianity's exclusivity coexists with radical inclusivity: "
                "'Whoever believes' (John 3:16) — anyone, from any background, is welcome. 'There "
                "is neither Jew nor Gentile, neither slave nor free, nor is there male and female, "
                "for you are all one in Christ Jesus' (Galatians 3:28)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["John 14:6", "Acts 4:12", "Galatians 3:28", "John 3:16"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Can multiple religions be true at the same time?",
            "answer_chirho": (
                "The popular notion that 'all religions are basically the same' or 'all paths lead "
                "to God' sounds tolerant and open-minded, but it is actually logically impossible "
                "and deeply disrespectful to the religions themselves. The law of non-contradiction "
                "states that contradictory propositions cannot both be true at the same time and in "
                "the same sense. The world's religions make mutually exclusive claims: Christianity "
                "teaches there is one God in three persons. Islam teaches there is one God, one "
                "person, and the Trinity is blasphemy. Buddhism teaches there is no creator God. "
                "Hinduism offers pantheism, polytheism, or monism. At most one of these can be "
                "correct about the nature of ultimate reality. Christianity teaches Jesus died on "
                "the cross. Islam teaches He did not (Surah 4:157). One of them is wrong — they "
                "cannot both be right. Christianity teaches we live once and face judgment (Hebrews "
                "9:27). Hinduism and Buddhism teach reincarnation. These are contradictory. To say "
                "'all religions are true' is actually to disrespect every religion by reducing them "
                "to something they do not claim to be. No serious Muslim, Christian, Buddhist, or "
                "Hindu would say their religion is 'basically the same' as the others. The 'blind "
                "men and the elephant' parable is often invoked, but it assumes the storyteller "
                "can see the whole elephant — claiming a privileged epistemic position above all "
                "religions. The right approach is not to claim all are equal but to examine the "
                "evidence for each claim and follow the truth wherever it leads. Christianity "
                "invites examination: 'Come now, let us reason together' (Isaiah 1:18). 'Test "
                "everything; hold fast what is good' (1 Thessalonians 5:21)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["Isaiah 1:18", "1 Thessalonians 5:21", "Hebrews 9:27", "John 17:17"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "What is wrong with the view that all religions are just different paths up the same mountain?",
            "answer_chirho": (
                "The 'many paths up one mountain' metaphor is attractive but fatally flawed. It "
                "assumes all religions share the same destination, which they emphatically do not. "
                "Christianity's destination is eternal personal communion with the triune God who "
                "created us. Buddhism's destination is Nirvana — the extinction of individual "
                "selfhood and the cessation of desire. Hinduism's Advaita Vedanta goal is "
                "absorption into impersonal Brahman — the dissolution of individual identity. "
                "Islam's destination is Paradise where Allah rewards the obedient. These are not "
                "different paths to the same peak — they are paths to entirely different peaks. "
                "The metaphor also assumes all religious claims about the mountain are equally "
                "partial and equally wrong. But this is itself a strong religious claim — it assumes "
                "the speaker has a God's-eye view of reality that transcends all particular "
                "religions. On what basis? Furthermore, the religions themselves reject the metaphor. "
                "Jesus did not say 'I am one of many paths.' He said 'I am THE way' (John 14:6). "
                "Muhammad did not say 'Islam is one option among many.' He claimed the Quran is the "
                "final revelation from the one true God. The Buddha did not say 'Any path works.' "
                "He taught a specific Eightfold Path and warned against wrong views. Taking "
                "religions seriously means taking their differences seriously — not papering over "
                "them with a flattering but false metaphor. The loving thing to do is not to tell "
                "people 'all paths are fine' when they may be walking off a cliff, but to point "
                "them to the true path — even if it means being called narrow. 'Small is the gate "
                "and narrow the road that leads to life, and only a few find it' (Matthew 7:14)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["John 14:6", "Matthew 7:13-14", "Proverbs 14:12", "Acts 4:12"],
            "difficulty_chirho": "basic",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Why is Christianity true while other religions are not?",
            "answer_chirho": (
                "Claiming Christianity is true is not arrogance — it is a testable claim based on "
                "evidence. Christianity invites investigation in a way that sets it apart from "
                "other faiths. Paul wrote: 'If Christ has not been raised, our preaching is "
                "useless and so is your faith' (1 Corinthians 15:14). Christianity staked its "
                "entire credibility on a single historical event — the resurrection — that can be "
                "examined. What makes Christianity uniquely credible? First, historical verifiability: "
                "Christianity is grounded in specific historical events (the life, death, and "
                "resurrection of Jesus) attested by multiple independent sources, both Christian and "
                "non-Christian. No other religion's founding claims have comparable historical "
                "attestation. Second, prophecy fulfillment: over 300 Messianic prophecies, written "
                "centuries before Jesus, find precise fulfillment in Him. No other religion has "
                "anything comparable. Third, manuscript evidence: the New Testament is the best-"
                "attested document in all of antiquity (25,000+ manuscripts). Fourth, philosophical "
                "coherence: Christianity provides answers to the deepest philosophical questions — "
                "Why is there something rather than nothing? Why is there order? Why are there "
                "moral values? What happens at death? — that are logically consistent and "
                "existentially satisfying. Fifth, transformative power: Christianity has consistently "
                "transformed lives, communities, and civilizations in ways that other worldviews "
                "have not matched in scope or consistency. Sixth, the person of Jesus: no other "
                "religious figure claimed to be God, backed it with miracles, predicted His own "
                "death and resurrection, and then fulfilled that prediction. The question is not "
                "whether it is narrow to believe in truth — of course truth is narrow. The question "
                "is where the evidence points. 'You will know the truth, and the truth will set "
                "you free' (John 8:32)."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["1 Corinthians 15:14", "John 8:32", "1 Peter 3:15", "Acts 17:11"],
            "difficulty_chirho": "intermediate",
        },
        {
            "source_chirho": "compiled_apologetics",
            "category_chirho": "apologetics_qa",
            "question_chirho": "Is it intolerant to claim that Christianity is the only true religion?",
            "answer_chirho": (
                "The modern confusion between tolerance and truth is one of the greatest obstacles "
                "to honest thinking about religion. Tolerance in its classical sense means treating "
                "people with respect and dignity even when you disagree with their beliefs. It does "
                "NOT mean agreeing that all beliefs are equally true. In fact, you can only be "
                "tolerant of views you disagree with — if you agree, no tolerance is needed. A "
                "doctor who tells a patient 'you have cancer and need treatment' is not being "
                "intolerant — she is being truthful and compassionate. The truly intolerant response "
                "would be to withhold the truth to avoid discomfort. Similarly, if Christianity is "
                "true — if Jesus really is the only way to salvation — then sharing that message "
                "is the most loving thing a person can do. The real intolerance would be knowing "
                "the truth and staying silent. Christians are explicitly commanded to be respectful "
                "in their truth-telling: 'Always be prepared to give an answer to everyone who "
                "asks you to give the reason for the hope that you have. But do this with "
                "gentleness and respect' (1 Peter 3:15). Jesus loved people who disagreed with "
                "Him — He ate with sinners, healed foreigners, and prayed for His executioners: "
                "'Father, forgive them, for they do not know what they are doing' (Luke 23:34). "
                "Christianity teaches that every human being is made in the image of God and "
                "deserves dignity and love, regardless of their beliefs. But loving people does "
                "not mean affirming everything they believe. 'Faithful are the wounds of a friend' "
                "(Proverbs 27:6). True love speaks truth — gently, humbly, but clearly."
            ),
            "topic_chirho": "worldview_comparisons",
            "scripture_chirho": ["1 Peter 3:15", "Luke 23:34", "Proverbs 27:6", "Ephesians 4:15"],
            "difficulty_chirho": "basic",
        },
    ]


def build_science_and_faith_chirho() -> list[dict]:
    """Build entries for science and faith (~20 entries)."""
    return []


def build_ethics_christian_living_chirho() -> list[dict]:
    """Build entries for ethics and Christian living (~15 entries)."""
    return []


def build_church_history_theology_chirho() -> list[dict]:
    """Build entries for church history and theology (~15 entries)."""
    return []


def build_modern_challenges_chirho() -> list[dict]:
    """Build entries for modern challenges (~10 entries)."""
    return []


def main_chirho():
    """Compile all apologetics Q&A entries into a single JSONL file."""
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    all_entries_chirho: list[dict] = []
    category_counts_chirho: Counter = Counter()
    topic_counts_chirho: Counter = Counter()

    builders_chirho = [
        ("Existence of God", build_existence_of_god_chirho),
        ("Problem of Evil/Suffering", build_problem_of_evil_chirho),
        ("Reliability of Scripture", build_reliability_of_scripture_chirho),
        ("Jesus Christ", build_jesus_christ_chirho),
        ("Worldview Comparisons", build_worldview_comparisons_chirho),
        ("Science and Faith", build_science_and_faith_chirho),
        ("Ethics and Christian Living", build_ethics_christian_living_chirho),
        ("Church History and Theology", build_church_history_theology_chirho),
        ("Modern Challenges", build_modern_challenges_chirho),
    ]

    for section_name_chirho, builder_func_chirho in builders_chirho:
        entries_chirho = builder_func_chirho()
        print(f"  {section_name_chirho}: {len(entries_chirho)} entries")
        for entry_chirho in entries_chirho:
            category_counts_chirho[entry_chirho["category_chirho"]] += 1
            topic_counts_chirho[entry_chirho["topic_chirho"]] += 1
        all_entries_chirho.extend(entries_chirho)

    # Write JSONL
    with open(OUTPUT_FILE_CHIRHO, "w", encoding="utf-8") as f_chirho:
        for entry_chirho in all_entries_chirho:
            f_chirho.write(json.dumps(entry_chirho, ensure_ascii=False) + "\n")

    print(f"\n{'='*60}")
    print(f"Total entries: {len(all_entries_chirho)}")
    print(f"Output: {OUTPUT_FILE_CHIRHO}")
    print(f"\nBy category:")
    for cat_chirho, count_chirho in sorted(category_counts_chirho.items()):
        print(f"  {cat_chirho}: {count_chirho}")
    print(f"\nBy topic:")
    for topic_chirho, count_chirho in sorted(topic_counts_chirho.items()):
        print(f"  {topic_chirho}: {count_chirho}")


if __name__ == "__main__":
    main_chirho()
