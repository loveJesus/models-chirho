# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
compile-evidence-chirho.py
Compiles structured scientific, historical, and miracle evidence into JSONL format.
Each entry has: claim, evidence, citations, counter_arguments, rebuttal, scripture, confidence, category.
All claims weighted against Scripture as final authority.
"""

import json
from pathlib import Path

OUTPUT_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent / "data-chirho" / "raw-chirho" / "evidence-chirho"


def build_creation_science_chirho() -> list[dict]:
    """Build creation science evidence entries."""
    return [
        {
            "claim_chirho": "Soft tissue has been found preserved in dinosaur bones, contradicting the claim that these bones are tens of millions of years old.",
            "evidence_chirho": "In 2005, Dr. Mary Schweitzer (NC State University) published findings of soft, flexible tissue including blood vessels and red blood cell-like structures inside a T. rex femur (MOR 1125). In 2025, NC State confirmed additional soft tissue finds. Collagen proteins were sequenced and matched to chicken/ostrich. Multiple labs have since replicated findings in Hadrosaur, Triceratops, and other specimens.",
            "citations_chirho": [
                "Schweitzer, M.H. et al. (2005) 'Soft-Tissue Vessels and Cellular Preservation in Tyrannosaurus rex.' Science 307(5717):1952-1955.",
                "Schweitzer, M.H. et al. (2007) 'Analyses of Soft Tissue from Tyrannosaurus rex Suggest the Presence of Protein.' Science 316(5822):277-280.",
                "Armitage, M.H. & Anderson, K.L. (2013) 'Soft sheets of fibrillar bone from a fossil of the supraorbital horn of Triceratops horridus.' Acta Histochemica 115(6):603-608."
            ],
            "counter_arguments_chirho": "Some scientists propose iron acts as a preservative (Schweitzer 2013), or that cross-linking of proteins could preserve tissue for millions of years under the right conditions.",
            "rebuttal_chirho": "Iron preservation experiments only demonstrated short-term stabilization under laboratory conditions. No experiment has demonstrated preservation for even thousands of years, let alone 68 million. The burden of proof is on explaining how soft, flexible tissue with intact proteins survives geological time scales.",
            "scripture_chirho": ["Genesis 1:24-25", "Exodus 20:11", "Job 40:15-24"],
            "confidence_chirho": "high",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "Radiometric dating methods have produced demonstrably incorrect ages for rocks of known age, calling their reliability into question.",
            "evidence_chirho": "Lava flows from the 1980 Mt. St. Helens eruption were dated by K-Ar method at 0.35-2.8 million years old (Austin 1996), despite being known to be <20 years old. Hawaiian lava flows from 1800-1801 were dated at 160 million to 3 billion years by K-Ar. The RATE (Radioisotopes and the Age of the Earth) project documented systematic discordances between different radiometric methods applied to the same rocks.",
            "citations_chirho": [
                "Austin, S.A. (1996) 'Excess Argon within Mineral Concentrates from the New Dacite Lava Dome at Mount St Helens Volcano.' Creation Ex Nihilo Technical Journal 10(3):335-343.",
                "Funkhouser, J.G. & Naughton, J.J. (1968) 'Radiogenic Helium and Argon in Ultramafic Inclusions from Hawaii.' Journal of Geophysical Research 73(14):4601-4607.",
                "DeYoung, D. (2005) 'Thousands Not Billions.' Master Books. (RATE project summary)"
            ],
            "counter_arguments_chirho": "Mainstream geologists attribute these to excess argon inherited from the magma source, contamination, or improper sample preparation. They argue these are well-understood limitations, not fundamental flaws.",
            "rebuttal_chirho": "If the method can produce wildly incorrect results for rocks of known age, how can we trust it for rocks of unknown age? The 'excess argon' explanation is ad hoc — invoked only when the dates contradict expectations. The same circular reasoning applies: dates that confirm the expected age are accepted, while anomalous dates are explained away.",
            "scripture_chirho": ["Genesis 1:1", "Psalm 33:6", "Hebrews 11:3"],
            "confidence_chirho": "high",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "The Cambrian Explosion shows most major animal phyla appearing suddenly in the fossil record without clear evolutionary ancestors.",
            "evidence_chirho": "In the Cambrian period (~541-530 million years ago by conventional dating), representatives of nearly all major animal phyla appear in an extremely narrow window. Darwin himself called this 'inexplicable' and hoped future discoveries would fill the gaps. Over 160 years later, the pattern persists. The Burgess Shale (Canada) and Chengjiang (China) fossil beds show extraordinary diversity appearing with no transitional precursors in Precambrian strata.",
            "citations_chirho": [
                "Meyer, S.C. (2013) 'Darwin's Doubt: The Explosive Origin of Animal Life and the Case for Intelligent Design.' HarperOne.",
                "Marshall, C.R. (2006) 'Explaining the Cambrian Explosion of Animals.' Annual Review of Earth and Planetary Sciences 34:355-384.",
                "Erwin, D.H. et al. (2011) 'The Cambrian Conundrum: Early Divergence and Later Ecological Success.' Science 334(6059):1091-1097."
            ],
            "counter_arguments_chirho": "Molecular clock studies suggest divergence began earlier but lacked hard parts for fossilization. Small soft-bodied ancestors may not have been preserved. Environmental triggers (oxygen levels, predation) could explain rapid diversification.",
            "rebuttal_chirho": "Exceptional preservation sites (Ediacaran biota) do preserve soft-bodied organisms, yet Cambrian-type body plans are absent. Molecular clock estimates rely on assumptions about mutation rates and require calibration — often circular with the fossil record. The appearance of 20+ phyla with distinct body plans in a geological instant remains better explained by design than unguided processes.",
            "scripture_chirho": ["Genesis 1:20-25", "Job 12:7-10", "Psalm 104:24-25"],
            "confidence_chirho": "high",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "Carbon-14 has been found in diamonds and coal deposits that should be completely C-14 dead if they are billions or millions of years old.",
            "evidence_chirho": "The RATE project measured significant C-14 in 10 coal samples from across the geologic column (Pennsylvanian to Eocene, conventionally 40-300 million years). All showed C-14 well above instrument background. Diamonds, supposedly 1-3 billion years old, also contained measurable C-14. Since C-14 has a half-life of ~5,730 years, after ~100,000 years there should be zero detectable C-14.",
            "citations_chirho": [
                "Baumgardner, J.R. et al. (2003) 'Measurable 14C in Fossilized Organic Materials.' Proceedings of the 5th International Conference on Creationism, pp. 127-142.",
                "Taylor, R.E. & Southon, J. (2007) 'Use of Natural Diamonds to Monitor 14C AMS Instrument Backgrounds.' Nuclear Instruments and Methods B 259:282-287."
            ],
            "counter_arguments_chirho": "Contamination during sample preparation, in-situ production of C-14 from nitrogen via neutron capture from uranium decay, or instrument background noise.",
            "rebuttal_chirho": "The RATE samples were carefully prepared to avoid contamination, and the C-14 levels measured were consistently above background across multiple labs. In-situ production via neutron capture can account for only a fraction of the observed C-14. If contamination were the explanation, levels should vary randomly — but they cluster around specific values consistent with a young age.",
            "scripture_chirho": ["Genesis 7:11-12", "2 Peter 3:5-6"],
            "confidence_chirho": "medium",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "Earth's magnetic field has been measured decaying since 1835, and extrapolation backward implies a young earth.",
            "evidence_chirho": "Direct measurements of Earth's magnetic dipole moment since 1835 show a consistent decay with a half-life of approximately 1,400 years. If we extrapolate backward more than about 20,000 years, the field strength would have been impossibly high (generating enough heat to liquefy Earth's surface). Dr. Thomas Barnes first published this analysis in 1971, updated by D. Russell Humphreys.",
            "citations_chirho": [
                "Barnes, T.G. (1971) 'Decay of the Earth's Magnetic Moment and the Geochronological Implications.' Creation Research Society Quarterly 8(1):24-29.",
                "Humphreys, D.R. (1990) 'Physical Mechanism for Reversals of the Earth's Magnetic Field During the Flood.' Proceedings of the 2nd International Conference on Creationism, pp. 129-142."
            ],
            "counter_arguments_chirho": "The geomagnetic field undergoes reversals and fluctuations over geological time (recorded in seafloor basalts). The current decay may represent a fluctuation, not a permanent trend. Dynamo theory explains field regeneration.",
            "rebuttal_chirho": "Magnetic reversals recorded in lava flows are consistent with rapid reversals during a catastrophic event (the Flood). Humphreys' model predicts field strengths of other planets (measured by Voyager/Messenger) more accurately than dynamo theory. The measured energy decay is real and measurable — the question is whether unobserved mechanisms can reverse the trend indefinitely.",
            "scripture_chirho": ["Genesis 1:1", "Psalm 102:25-26", "Isaiah 40:22"],
            "confidence_chirho": "medium",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "The universe's expansion is accelerating faster than any known force can account for, matching biblical descriptions of God stretching out the heavens.",
            "evidence_chirho": "In 1998, observations of Type Ia supernovae showed the universe's expansion is accelerating (Perlmutter, Riess, Schmidt — 2011 Nobel Prize). 'Dark energy' was proposed to explain this, but it remains the most mysterious concept in physics — an unknown force comprising ~68% of the universe's energy. Meanwhile, at least 11 Bible passages describe God 'stretching out the heavens' (Job 9:8, Isaiah 40:22, Isaiah 42:5, Isaiah 44:24, Isaiah 45:12, Isaiah 48:13, Isaiah 51:13, Jeremiah 10:12, Jeremiah 51:15, Zechariah 12:1, Psalm 104:2).",
            "citations_chirho": [
                "Riess, A.G. et al. (1998) 'Observational Evidence from Supernovae for an Accelerating Universe and a Cosmological Constant.' Astronomical Journal 116(3):1009-1038.",
                "Perlmutter, S. et al. (1999) 'Measurements of Omega and Lambda from 42 High-Redshift Supernovae.' Astrophysical Journal 517(2):565-586."
            ],
            "counter_arguments_chirho": "Dark energy is a placeholder for unknown physics, not evidence for God. The Bible passages are poetic language, not scientific descriptions. Cosmological expansion is well-explained by general relativity.",
            "rebuttal_chirho": "The fact that the Bible used the language of cosmic expansion thousands of years before it was scientifically discovered is remarkable regardless of the genre. That modern physics requires an unexplained force (dark energy) to account for the observed expansion is consistent with a sustaining divine will. General relativity describes HOW the universe expands but cannot explain WHY it accelerates — science describes the mechanism, the Bible reveals the Agent.",
            "scripture_chirho": ["Job 9:8", "Isaiah 40:22", "Isaiah 42:5", "Isaiah 44:24", "Isaiah 45:12", "Psalm 104:2", "Zechariah 12:1"],
            "confidence_chirho": "high",
            "category_chirho": "cosmological"
        },
        {
            "claim_chirho": "The bacterial flagellum is an irreducibly complex molecular machine that defies gradual evolutionary explanation.",
            "evidence_chirho": "The bacterial flagellum consists of approximately 40 protein parts working together as a rotary motor (spinning at up to 100,000 RPM). It includes a rotor, stator, drive shaft, universal joint, and propeller — all required for function. Dr. Michael Behe proposed in 'Darwin's Black Box' (1996) that removing any essential component renders the system non-functional, meaning it could not have been built gradually by natural selection.",
            "citations_chirho": [
                "Behe, M.J. (1996) 'Darwin's Black Box: The Biochemical Challenge to Evolution.' Free Press.",
                "Behe, M.J. (2019) 'Darwin Devolves: The New Science About DNA That Challenges Evolution.' HarperOne."
            ],
            "counter_arguments_chirho": "The type III secretion system (T3SS) shares homologous components with the flagellum, suggesting parts could have been co-opted from other functions. Exaptation (repurposing existing parts) provides a pathway.",
            "rebuttal_chirho": "The T3SS is phylogenetically derived FROM the flagellum (not ancestral to it), based on comparative genomics. Even if some parts were co-opted, this does not explain the origin of the information specifying their assembly into a functional motor. Co-option requires foresight about future use — which natural selection cannot provide. The flagellum remains the poster child of specified complexity.",
            "scripture_chirho": ["Psalm 139:14", "Romans 1:20", "Colossians 1:16-17"],
            "confidence_chirho": "high",
            "category_chirho": "design"
        },
        {
            "claim_chirho": "The fine-tuning of universal constants points to intentional design rather than chance.",
            "evidence_chirho": "Multiple physical constants must be precisely calibrated for life to exist: the gravitational constant (1 part in 10^60), the strong nuclear force (if 2% stronger, no hydrogen; 2% weaker, no elements beyond hydrogen), the cosmological constant (1 part in 10^120), the ratio of electromagnetic to gravitational force (1 in 10^40). Roger Penrose calculated the odds of the universe's initial low entropy state at 1 in 10^(10^123). Even secular physicists acknowledge the extreme fine-tuning.",
            "citations_chirho": [
                "Penrose, R. (1989) 'The Emperor's New Mind.' Oxford University Press.",
                "Collins, R. (2009) 'The Teleological Argument: An Exploration of the Fine-Tuning of the Universe.' in Craig & Moreland (eds) 'The Blackwell Companion to Natural Theology.'",
                "Barrow, J.D. & Tipler, F.J. (1986) 'The Anthropic Cosmological Principle.' Oxford University Press."
            ],
            "counter_arguments_chirho": "The multiverse hypothesis proposes that all possible values exist across infinite universes, making our fine-tuning inevitable by selection. The anthropic principle says we can only observe a universe compatible with our existence.",
            "rebuttal_chirho": "The multiverse is unfalsifiable and generates more questions than it answers (what fine-tuned the multiverse generator?). The anthropic principle explains why we observe fine-tuning but not WHY it exists. As physicist Paul Davies wrote, 'The impression of design is overwhelming.' The simplest explanation consistent with the evidence is an intelligent Designer — exactly what the Bible teaches.",
            "scripture_chirho": ["Romans 1:19-20", "Psalm 19:1-4", "Isaiah 45:18", "Jeremiah 33:25"],
            "confidence_chirho": "high",
            "category_chirho": "design"
        },
        {
            "claim_chirho": "Religious practice is associated with 37% increased survival and significant health benefits, supported by peer-reviewed research.",
            "evidence_chirho": "A meta-analysis published in JAMA Internal Medicine (Li et al., 2016, Harvard T.H. Chan School of Public Health) found that women attending religious services more than once per week had a 33% lower mortality risk compared to those who never attended. McCullough et al. (2000) meta-analysis in Health Psychology found religious involvement was associated with 29% lower odds of mortality. 75% of the nearly 350 studies examining religious practice and health in the Handbook of Religion and Health found positive correlations.",
            "citations_chirho": [
                "Li, S. et al. (2016) 'Association of Religious Service Attendance With Mortality Among Women.' JAMA Internal Medicine 176(6):777-785.",
                "McCullough, M.E. et al. (2000) 'Religious Involvement and Mortality: A Meta-Analytic Review.' Health Psychology 19(3):211-222.",
                "Koenig, H.G. et al. (2012) 'Handbook of Religion and Health.' 2nd Edition. Oxford University Press."
            ],
            "counter_arguments_chirho": "Correlation is not causation. Healthier people may be more able to attend services. Social support networks, not religion itself, may drive the benefits.",
            "rebuttal_chirho": "The Harvard study controlled for diet, exercise, social integration, depression, and other confounders — the effect persisted. While social support is one mechanism, studies also show independent effects of prayer, forgiveness, purpose, and hope on biomarkers (cortisol, inflammatory markers, telomere length). The consistency across hundreds of studies, populations, and methodologies makes the association robust. God designed us for relationship with Him — it should not surprise us that living according to His design produces flourishing.",
            "scripture_chirho": ["Proverbs 3:7-8", "Psalm 103:2-3", "3 John 1:2", "Hebrews 10:25"],
            "confidence_chirho": "high",
            "category_chirho": "health"
        },
        {
            "claim_chirho": "Polystrate fossils — trees spanning multiple geological strata — indicate rapid deposition rather than millions of years of gradual sediment accumulation.",
            "evidence_chirho": "Fossilized trees (notably at Joggins, Nova Scotia — UNESCO World Heritage Site) stand upright through multiple sedimentary layers conventionally assigned ages spanning thousands to millions of years. The trees show no sign of decay at the top despite supposedly being buried over vast time spans. Similar polystrate fossils exist at Yellowstone Specimen Ridge, Joggins Fossil Cliffs, and coal seams worldwide. At Mt. St. Helens (1980), Spirit Lake log deposits produced similar upright 'polystrate' arrangements in a single event.",
            "citations_chirho": [
                "Austin, S.A. (1986) 'Mt. St. Helens and Catastrophism.' Impact Article #157, Institute for Creation Research.",
                "Rupke, N.A. (1966) 'Prolegomena to a Study of Cataclysmal Sedimentation.' Research Society Quarterly 3(1):16-37."
            ],
            "counter_arguments_chirho": "Geologists explain polystrate fossils as rapid local sedimentation events (channel fills, crevasse splays) within longer geological sequences. Not all strata represent equal time spans.",
            "rebuttal_chirho": "If rapid deposition is admitted for the strata containing polystrate fossils, how do we know other strata were not similarly deposited rapidly? The Mt. St. Helens demonstration showed that what geologists interpret as long-age sequences can form in hours to days. The existence of polystrate fossils across multiple geological 'periods' is exactly what a global flood model predicts.",
            "scripture_chirho": ["Genesis 7:11-12", "Genesis 7:19-20", "2 Peter 3:5-6", "Psalm 104:6-9"],
            "confidence_chirho": "high",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "Mitochondrial Eve and Y-chromosome Adam convergence points are consistent with a literal first couple.",
            "evidence_chirho": "Genetics identifies a most recent common matrilineal ancestor ('Mitochondrial Eve') and most recent common patrilineal ancestor ('Y-chromosome Adam'). While secular dating places them at different times (100-200kya for mt-Eve, 200-300kya for Y-Adam), the EXISTENCE of these convergence points is consistent with the biblical account. Recent molecular clock recalibrations using observed mutation rates (rather than assumed evolutionary divergence rates) produce much younger dates. Jeanson (2015) calculated Y-chromosome divergence consistent with ~4,500 years using measured mutation rates.",
            "citations_chirho": [
                "Jeanson, N.T. (2015) 'Replacing Darwin: The New Origin of Species.' Master Books.",
                "Cann, R.L. et al. (1987) 'Mitochondrial DNA and Human Evolution.' Nature 325:31-36.",
                "Poznik, G.D. et al. (2013) 'Sequencing Y Chromosomes Resolves Discrepancy in Time to Common Ancestor.' Science 341(6145):562-565."
            ],
            "counter_arguments_chirho": "Mitochondrial Eve and Y-chromosome Adam are not the same as biblical Adam and Eve — they represent the most recent common ancestors in their respective lineages, not the only people alive at that time. Population genetics indicates a minimum effective population size of ~10,000.",
            "rebuttal_chirho": "The effective population size estimates depend heavily on assumptions about mutation rates, generation times, and selection models. When observed (pedigree-based) mutation rates are used instead of phylogenetically calibrated rates, the timelines shrink dramatically. The convergence of both mitochondrial and Y-chromosome lineages to single individuals is at minimum consistent with a literal first couple, even if secular interpretations add caveats.",
            "scripture_chirho": ["Genesis 2:7", "Genesis 2:21-22", "Genesis 3:20", "Acts 17:26"],
            "confidence_chirho": "medium",
            "category_chirho": "creation_science"
        },
        {
            "claim_chirho": "Prophecy fulfillment in the Bible demonstrates supernatural foreknowledge with mathematical impossibility of chance.",
            "evidence_chirho": "Professor Peter Stoner (Science Speaks, 1958) calculated the probability of one person fulfilling just 8 Messianic prophecies at 1 in 10^17 (1 in 100 quadrillion). For 48 prophecies, the probability becomes 1 in 10^157. Jesus fulfilled over 300 Messianic prophecies. Key examples: born in Bethlehem (Micah 5:2, written ~700 BC), born of a virgin (Isaiah 7:14), entered Jerusalem on a donkey (Zechariah 9:9), betrayed for 30 pieces of silver (Zechariah 11:12-13), crucified with pierced hands/feet (Psalm 22:16, written ~1000 BC — before crucifixion was invented), lots cast for garments (Psalm 22:18).",
            "citations_chirho": [
                "Stoner, P.W. (1958) 'Science Speaks: Scientific Proof of the Accuracy of Prophecy and the Bible.' Moody Press.",
                "McDowell, J. (1999) 'The New Evidence That Demands a Verdict.' Thomas Nelson."
            ],
            "counter_arguments_chirho": "The prophecies may have been written or edited after the events (postdiction). Jesus may have deliberately arranged to fulfill them. The prophecies are vague enough to apply to many people.",
            "rebuttal_chirho": "The Dead Sea Scrolls (discovered 1947, dated 150 BC-70 AD) contain copies of Isaiah, Psalms, and other prophetic books — confirming they predate Jesus. Many prophecies (birthplace, manner of death, betrayal price) were beyond Jesus' control to arrange. The specificity of combined prophecies (born in Bethlehem AND of the tribe of Judah AND betrayed for exactly 30 silver pieces AND crucified despite being written before crucifixion existed) eliminates vagueness as an objection.",
            "scripture_chirho": ["Isaiah 53:1-12", "Psalm 22:1-18", "Micah 5:2", "Zechariah 11:12-13", "Daniel 9:24-26"],
            "confidence_chirho": "high",
            "category_chirho": "historical"
        },
    ]


def build_historical_evidence_chirho() -> list[dict]:
    """Build historical evidence for Christianity entries."""
    return [
        {
            "claim_chirho": "Multiple non-Christian sources from the 1st-2nd century confirm the historical existence of Jesus and early Christian beliefs.",
            "evidence_chirho": "Josephus (Antiquities 18.3.3, ~93 AD) mentions Jesus as 'a wise man' who was crucified under Pilate — the Testimonium Flavianum, even in its likely partially interpolated form, is accepted by most scholars as having an authentic core. Josephus also mentions 'James, the brother of Jesus who is called Christ' (Antiquities 20.9.1). Tacitus (Annals 15.44, ~116 AD) describes 'Christus' being executed under Pontius Pilate. Pliny the Younger (Letters 10.96, ~112 AD) describes Christians singing hymns 'to Christ as to a god.' Thallus (~52 AD, preserved in Julius Africanus) attempted to explain away the darkness at the crucifixion as an eclipse. Mara bar Serapion (~73 AD) references the execution of 'the wise King' of the Jews. Lucian of Samosata (~170 AD) mocks Christians for worshipping 'the crucified sophist.'",
            "citations_chirho": [
                "Josephus, 'Antiquities of the Jews' 18.3.3 and 20.9.1",
                "Tacitus, 'Annals' 15.44",
                "Pliny the Younger, 'Letters' 10.96",
                "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' Eerdmans."
            ],
            "counter_arguments_chirho": "Josephus' Testimonium may be partially or wholly interpolated by Christian scribes. The other sources date to decades after Jesus' death and may rely on Christian reports rather than independent investigation.",
            "rebuttal_chirho": "Even critical scholars (Meier, Vermes, Crossan) accept the core of the Testimonium as authentic. The James passage in Antiquities 20 is almost universally accepted. Tacitus was a careful historian who used Roman archives — he specifies 'Christus' was executed under Pilate, confirming the basic gospel narrative from a hostile source. The cumulative weight of multiple independent sources, both sympathetic and hostile, establishes Jesus' historicity beyond reasonable doubt. No credible ancient source denied Jesus' existence.",
            "scripture_chirho": ["Luke 1:1-4", "1 Corinthians 15:3-8", "2 Peter 1:16"],
            "confidence_chirho": "high",
            "category_chirho": "historical"
        },
        {
            "claim_chirho": "The New Testament has vastly superior manuscript evidence compared to any other ancient text.",
            "evidence_chirho": "There are approximately 5,900 Greek manuscripts of the New Testament, plus 10,000 Latin Vulgate manuscripts, 9,300+ in other languages — totaling over 25,000 manuscripts. Compare: Homer's Iliad (~1,800 manuscripts, earliest copy 500 years after original), Caesar's Gallic Wars (~10 manuscripts, earliest 1,000 years after), Plato's works (~7 manuscripts, earliest 1,200 years after). The earliest NT fragment (P52, John 18) dates to ~125 AD, within ~30-60 years of composition. The Dead Sea Scrolls showed the Hebrew Bible was transmitted with 95% word-for-word accuracy over 1,000 years.",
            "citations_chirho": [
                "Metzger, B.M. & Ehrman, B.D. (2005) 'The Text of the New Testament.' 4th Edition. Oxford University Press.",
                "Geisler, N.L. & Nix, W.E. (1986) 'A General Introduction to the Bible.' Moody Press.",
                "Wallace, D.B. (2010) 'Revisiting the Corruption of the New Testament.' Kregel Academic."
            ],
            "counter_arguments_chirho": "More manuscripts means more variants. The sheer number of textual variants (~400,000) shows the text was not perfectly transmitted. Important theological passages (Mark 16:9-20, John 7:53-8:11) are disputed.",
            "rebuttal_chirho": "The overwhelming majority of variants are spelling differences, word order changes, or obvious scribal errors that affect no doctrine. Critical scholars estimate 99.5% of the NT text is established beyond doubt. Having more manuscripts is a STRENGTH, not a weakness — it enables scholars to identify and correct scribal errors through comparison. No other ancient text comes close to this level of attestation. The disputed passages represent a tiny fraction and no essential Christian doctrine depends on any of them.",
            "scripture_chirho": ["Isaiah 40:8", "Matthew 24:35", "1 Peter 1:25", "Psalm 12:6-7"],
            "confidence_chirho": "high",
            "category_chirho": "historical"
        },
        {
            "claim_chirho": "The canon of the New Testament was NOT decided at the Council of Nicaea (325 AD), contrary to popular myth.",
            "evidence_chirho": "The Council of Nicaea (325 AD) addressed the Arian heresy and the date of Easter — the canon was not on its agenda (as confirmed by its surviving records). The books of the NT were already widely recognized by the mid-2nd century. The Muratorian Fragment (~170 AD) lists most NT books. Irenaeus (~180 AD) references the four Gospels as authoritative. Athanasius' 39th Festal Letter (367 AD) lists the 27 books. The Councils of Hippo (393 AD) and Carthage (397 AD) formally ratified what was already the church's received collection — they recognized the canon, they did not create it.",
            "citations_chirho": [
                "Metzger, B.M. (1987) 'The Canon of the New Testament.' Oxford University Press.",
                "Kruger, M.J. (2012) 'Canon Revisited: Establishing the Origins and Authority of the New Testament Books.' Crossway.",
                "Athanasius, '39th Festal Letter' (367 AD)"
            ],
            "counter_arguments_chirho": "The canonical process was messy and politically influenced. Some books (Revelation, 2 Peter, James) were disputed for centuries. Other early Christians used books not in the current canon (Shepherd of Hermas, Didache).",
            "rebuttal_chirho": "Early disputes actually strengthen confidence in the canon — they show the early church was critically examining texts rather than blindly accepting them. The criteria used (apostolic origin, widespread use, doctrinal consistency) were reasonable. The 'rejected' books were rejected precisely because they failed these tests. The myth that the canon was decided by political fiat at Nicaea is demonstrably false and stems from popular fiction (Dan Brown's 'The Da Vinci Code'), not historical scholarship.",
            "scripture_chirho": ["2 Timothy 3:16-17", "2 Peter 3:15-16", "John 16:13"],
            "confidence_chirho": "high",
            "category_chirho": "historical"
        },
        {
            "claim_chirho": "Archaeological discoveries have consistently confirmed biblical accounts rather than contradicting them.",
            "evidence_chirho": "Key confirmations: (1) Pool of Siloam discovered in 2004, confirming John 9:7. (2) Pilate inscription found at Caesarea Maritima (1961), confirming his role as prefect. (3) Caiaphas ossuary discovered in 1990. (4) House of David inscription (Tel Dan Stele, 1993). (5) Hezekiah's Tunnel confirmed (2 Kings 20:20). (6) Cyrus Cylinder confirms Cyrus' policy of returning exiles (Ezra 1:1-4). (7) Ebla tablets (1964-1975) confirm patriarchal-era customs. (8) Merneptah Stele (~1208 BC) — earliest extra-biblical reference to 'Israel.' Nelson Glueck, renowned archaeologist, stated: 'No archaeological discovery has ever controverted a biblical reference.'",
            "citations_chirho": [
                "Shanks, H. (2004) 'The Siloam Pool.' Biblical Archaeology Review 31(5):16-23.",
                "Kitchen, K.A. (2003) 'On the Reliability of the Old Testament.' Eerdmans.",
                "McRay, J. (2008) 'Archaeology and the New Testament.' Baker Academic."
            ],
            "counter_arguments_chirho": "Absence of evidence for some biblical events (Exodus, conquest of Canaan) is sometimes cited. Some scholars date the patriarchal narratives as later literary compositions.",
            "rebuttal_chirho": "Absence of evidence is not evidence of absence, especially for events in regions with limited excavation. The trend over 150+ years of biblical archaeology has been consistently toward confirmation. Critics who once denied the existence of the Hittites, King David, Pontius Pilate, and the Pool of Siloam were proven wrong by subsequent discoveries. The archaeological record is incomplete — future discoveries may confirm what is currently unattested, as has happened repeatedly.",
            "scripture_chirho": ["Joshua 24:13", "Luke 3:1-2", "Acts 26:26"],
            "confidence_chirho": "high",
            "category_chirho": "historical"
        },
        {
            "claim_chirho": "The disciples' willingness to die for their testimony of the resurrection, when they were in a position to know if it was true, provides strong evidence for its historicity.",
            "evidence_chirho": "The apostles claimed to be eyewitnesses of the risen Jesus (1 Corinthians 15:3-8 — Paul lists over 500 witnesses, most still alive when he wrote). Church tradition records that Peter was crucified upside down, James (son of Zebedee) was beheaded by Herod (Acts 12:2), James the Just was thrown from the temple (Josephus, Hegesippus), Paul was beheaded in Rome, Thomas was speared in India. People die for beliefs they hold to be true — but the apostles were in a unique position to KNOW whether the resurrection happened. They would not die for a known lie.",
            "citations_chirho": [
                "Habermas, G.R. & Licona, M.R. (2004) 'The Case for the Resurrection of Jesus.' Kregel.",
                "Wright, N.T. (2003) 'The Resurrection of the Son of God.' Fortress Press.",
                "Josephus, 'Antiquities' 20.9.1 (death of James)"
            ],
            "counter_arguments_chirho": "Many people die for false beliefs (martyrs of other religions, cults). Some apostolic martyrdoms are traditions, not independently verified. Group hallucination or cognitive dissonance could explain their conviction.",
            "rebuttal_chirho": "The key distinction: others die for beliefs they sincerely hold but cannot verify. The apostles died for claims about events they personally witnessed. Hallucinations are individual experiences — they cannot be shared by 500+ people in different locations over 40 days. Group cognitive dissonance does not explain the radical transformation of the disciples from fearful fugitives (Mark 14:50) to bold proclaimers willing to face execution. Something happened to convince them — and the most parsimonious explanation is what they claimed: they saw the risen Christ.",
            "scripture_chirho": ["1 Corinthians 15:3-8", "1 Corinthians 15:14-17", "Acts 4:18-20", "2 Peter 1:16"],
            "confidence_chirho": "high",
            "category_chirho": "historical"
        },
    ]


def build_miracle_evidence_chirho() -> list[dict]:
    """Build documented miracle testimony entries."""
    return [
        {
            "claim_chirho": "George Muller of Bristol documented approximately 50,000 specific answered prayers with dates during his lifetime, including miraculous provision for 10,024 orphans.",
            "evidence_chirho": "George Muller (1805-1898) operated 5 orphan houses in Bristol, England, caring for 10,024 orphans over his lifetime. He never asked anyone for money — relying solely on prayer. His personal journals, published as 'A Narrative of Some of the Lord's Dealings with George Muller,' document approximately 50,000 specific answered prayers with dates and details. Food arriving at the exact moment of need was documented repeatedly. Over $7.5 million (in contemporary value, equivalent to hundreds of millions today) was received without solicitation. His life was independently verified by contemporaries and auditors.",
            "citations_chirho": [
                "Muller, G. (1837-1886) 'A Narrative of Some of the Lord's Dealings with George Muller.' (6 volumes, public domain)",
                "Pierson, A.T. (1899) 'George Muller of Bristol.' Fleming H. Revell Company.",
                "Steer, R. (1997) 'George Muller: Delighted in God.' Christian Focus Publications."
            ],
            "counter_arguments_chirho": "Self-reported answers to prayer are subject to confirmation bias. Donations may have come through indirect solicitation or reputation rather than supernatural intervention.",
            "rebuttal_chirho": "Muller's records were meticulous and audited. He deliberately kept his needs private to prove that God answers prayer — often the orphanages' accounts were completely empty before provision arrived. The consistency over 60+ years, the specific timing of provision (food arriving minutes before meals with nothing in the cupboard), and the scale of operation ($7.5M+ without asking) defy naturalistic explanation. His experiment in faith was conducted precisely to demonstrate God's faithfulness.",
            "scripture_chirho": ["Matthew 6:25-33", "Philippians 4:19", "Matthew 7:7-11", "James 1:17"],
            "confidence_chirho": "high",
            "category_chirho": "miracle"
        },
        {
            "claim_chirho": "Craig Keener's two-volume academic study documents hundreds of miracle claims with medical evidence from around the world.",
            "evidence_chirho": "Dr. Craig Keener (Asbury Theological Seminary) published a rigorous 1,200-page academic study of miracle claims in 2011. The work documents hundreds of cases from Asia, Africa, Latin America, and the West, many with medical documentation. Cases include sudden healing of verified blindness, deafness, and paralysis during or after prayer. The study notes that miracle reports are especially prevalent in regions of recent Christian expansion, consistent with the pattern in Acts.",
            "citations_chirho": [
                "Keener, C.S. (2011) 'Miracles: The Credibility of the New Testament Accounts.' 2 Volumes. Baker Academic.",
                "Brown, C.G. (2012) 'Testing Prayer: Science and Healing.' Harvard University Press."
            ],
            "counter_arguments_chirho": "Anecdotal evidence, even in large quantities, does not constitute scientific proof. Confirmation bias, placebo effect, and misdiagnosis can explain many cases.",
            "rebuttal_chirho": "Keener specifically addresses methodological objections throughout his work. He includes cases with before-and-after medical documentation. The point is not that every case is proven beyond all doubt, but that the sheer volume of well-documented cases from diverse cultures and medical contexts — combined with the pattern of their occurrence in prayer contexts — constitutes evidence that demands an explanation beyond blanket dismissal.",
            "scripture_chirho": ["Mark 16:17-18", "James 5:14-15", "Acts 3:6-8", "John 14:12"],
            "confidence_chirho": "high",
            "category_chirho": "miracle"
        },
        {
            "claim_chirho": "A Dutch study published in a peer-reviewed medical journal documented 83 reports of proximal intercessory prayer healing, with 27 meeting medical criteria for documentation.",
            "evidence_chirho": "A study published in the Southern Medical Journal (Byrd, 1988) was one of the first randomized controlled trials of prayer. A more comprehensive Dutch study examined 83 reports of healing attributed to proximal intercessory prayer. Of these, 27 cases met their medical documentation criteria, showing improvement that could not be attributed to normal medical treatment. The Global Medical Research Institute (GMRI) has compiled additional peer-reviewed cases.",
            "citations_chirho": [
                "Byrd, R.C. (1988) 'Positive Therapeutic Effects of Intercessory Prayer in a Coronary Care Unit Population.' Southern Medical Journal 81(7):826-829.",
                "Brown, C.G. et al. (2010) 'Study of the Therapeutic Effects of Proximal Intercessory Prayer (STEPP) on Auditory and Visual Impairments in Rural Mozambique.' Southern Medical Journal 103(9):864-869."
            ],
            "counter_arguments_chirho": "Small sample sizes, lack of blinding in proximal prayer studies, potential for spontaneous remission, and the failure of large-scale prayer studies (STEP trial, 2006) to show effects.",
            "rebuttal_chirho": "The STEP trial tested distant intercessory prayer by strangers — a very different intervention from personal, proximal prayer by believing communities. The Mozambique study (Brown et al.) measured auditory and visual improvements with audiometers and eye charts before and after prayer, showing statistically significant improvements. God is not obligated to perform on demand for skeptical researchers — but documented cases from clinical contexts deserve honest evaluation.",
            "scripture_chirho": ["James 5:14-16", "Matthew 17:20", "Mark 11:24", "Acts 28:8"],
            "confidence_chirho": "medium",
            "category_chirho": "miracle"
        },
    ]


def main_chirho():
    """Compile all evidence categories into JSONL files."""
    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    categories_chirho = {
        "creation-science-chirho": build_creation_science_chirho(),
        "historical-evidence-chirho": build_historical_evidence_chirho(),
        "miracle-testimony-chirho": build_miracle_evidence_chirho(),
    }

    total_chirho = 0
    for name_chirho, entries_chirho in categories_chirho.items():
        output_path_chirho = OUTPUT_DIR_CHIRHO / f"{name_chirho}.jsonl"
        with open(output_path_chirho, "w", encoding="utf-8") as f_chirho:
            for entry_chirho in entries_chirho:
                f_chirho.write(json.dumps(entry_chirho, ensure_ascii=False) + "\n")
        print(f"  {name_chirho}: {len(entries_chirho)} entries → {output_path_chirho}")
        total_chirho += len(entries_chirho)

    print(f"\nTotal evidence entries compiled: {total_chirho}")
    print("These are SEED entries — comprehensive research will expand each category significantly.")


if __name__ == "__main__":
    main_chirho()
