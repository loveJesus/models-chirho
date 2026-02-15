# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
compile-evidence-expanded-chirho.py
Massively expands the evidence corpus from ~20 entries to 80+ entries.
Appends to the existing evidence-expanded-chirho.jsonl output file.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT_CHIRHO = Path(__file__).resolve().parent.parent.parent.parent
OUTPUT_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent / "data-chirho" / "raw-chirho" / "evidence-chirho"
OUTPUT_FILE_CHIRHO = OUTPUT_DIR_CHIRHO / "evidence-expanded-chirho.jsonl"
SPEC_DB_CHIRHO = PROJECT_ROOT_CHIRHO / "spec-chirho" / "progress-chirho.sqlite"
AGENT_CODE_CHIRHO = "opus-evidence-expander-chirho"


def log_start_chirho(action_chirho: str) -> int:
    """Log task start to progress DB, return row id."""
    try:
        conn_chirho = sqlite3.connect(str(SPEC_DB_CHIRHO))
        cur_chirho = conn_chirho.cursor()
        cur_chirho.execute(
            "INSERT INTO steps_taken_chirho (agent_code_chirho, timestamp_start_chirho, action_taken_chirho) VALUES (?, ?, ?)",
            (AGENT_CODE_CHIRHO, datetime.now(timezone.utc).isoformat(), action_chirho),
        )
        row_id_chirho = cur_chirho.lastrowid
        conn_chirho.commit()
        conn_chirho.close()
        return row_id_chirho
    except Exception:
        return -1


def log_end_chirho(row_id_chirho: int, result_chirho: str, overview_chirho: str):
    """Log task end to progress DB."""
    try:
        conn_chirho = sqlite3.connect(str(SPEC_DB_CHIRHO))
        conn_chirho.execute(
            "UPDATE steps_taken_chirho SET timestamp_end_chirho=?, result_of_action_chirho=?, overview_of_result_chirho=? WHERE id_chirho=?",
            (datetime.now(timezone.utc).isoformat(), result_chirho, overview_chirho, row_id_chirho),
        )
        conn_chirho.commit()
        conn_chirho.close()
    except Exception:
        pass


def e(claim, evidence, citations, counter, rebuttal, scripture, confidence, category):
    """Shorthand entry builder to keep the file manageable."""
    return {
        "claim_chirho": claim,
        "evidence_chirho": evidence,
        "citations_chirho": citations,
        "counter_arguments_chirho": counter,
        "rebuttal_chirho": rebuttal,
        "scripture_chirho": scripture,
        "confidence_chirho": confidence,
        "category_chirho": category,
    }


def build_geology_chirho():
    return [
        e(
            "Rapid canyon formation at Mt. St. Helens demonstrates canyons can form in hours, not millions of years.",
            "The 1980 eruption of Mt. St. Helens carved a canyon system up to 140 feet deep through solid rock in a single day (March 19, 1982 mudflow). Engineers Canyon, also called 'Little Grand Canyon,' was cut through 100 feet of fresh volcanic deposits. The stratified layers deposited by pyroclastic flows mimicked what geologists normally attribute to long ages.",
            ["Austin, S.A. (1986) 'Mt. St. Helens and Catastrophism.' Impact #157, ICR.", "Morris, J.D. & Austin, S.A. (2003) 'Footprints in the Ash.' Master Books."],
            "Mt. St. Helens cut through soft, unconsolidated volcanic ash — not hard bedrock like the Grand Canyon.",
            "The point is that stratified layers and canyon morphology form rapidly under catastrophic conditions. The Grand Canyon also shows evidence of catastrophic formation: breach of a natural dam, sheet erosion patterns, and lack of talus deposits expected from slow erosion. The principle of rapid formation is demonstrated; the mechanism scales.",
            ["Genesis 7:11-12", "Psalm 104:6-9", "2 Peter 3:5-6"],
            "high", "geology"
        ),
        e(
            "Bent and folded rock layers without fracturing require soft, wet sediment — not rock hardened over millions of years.",
            "Throughout the Grand Canyon and worldwide, thick sedimentary layers are found bent and folded at sharp angles without fracturing or shattering. The Tapeats Sandstone and Muav Limestone in the Grand Canyon are folded at Carbon Creek and other locations. If these layers had been solid rock (as expected after millions of years of hardening), they would have fractured. The folds indicate the sediment was still soft and pliable when deformed.",
            ["Austin, S.A. (1994) 'Grand Canyon: Monument to Catastrophe.' ICR, pp. 95-107.", "Snelling, A.A. (2009) 'Earth's Catastrophic Past.' ICR, Vol. 2, pp. 573-596."],
            "Metamorphic processes under heat and pressure can cause rock to deform plastically without fracturing, even when solid.",
            "Plastic deformation requires specific temperature/pressure conditions found deep in the crust. Many folded layers are surface or near-surface deposits where such conditions did not exist. The simplest explanation is that the layers were still unconsolidated sediment when folded — consistent with rapid deposition and deformation during a global flood.",
            ["Genesis 7:11", "Genesis 8:1-3", "Psalm 104:8"],
            "high", "geology"
        ),
        e(
            "Lack of erosion between sedimentary layers supposedly separated by millions of years challenges the geological timescale.",
            "If sedimentary layers were deposited over millions of years, the exposed surfaces between them should show extensive erosion: gullies, channels, soil horizons, root traces. Yet contacts between major formations (e.g., Coconino Sandstone over Hermit Shale in Grand Canyon) are often flat, knife-sharp, with no evidence of prolonged exposure. These 'paraconformities' represent supposed millions of years with no physical evidence of the passage of time.",
            ["Snelling, A.A. (2008) 'The Case for Flood Geology.' Answers in Genesis.", "Austin, S.A. (1994) 'Grand Canyon: Monument to Catastrophe.' ICR."],
            "Submarine environments or arid conditions can limit erosion. Some contacts do show erosion surfaces.",
            "Even submarine and arid environments produce recognizable erosion features over thousands of years, let alone millions. The widespread absence of erosion between layers globally — not just in one location — is systematic. Where erosion surfaces DO exist, they are the exception that proves the rule: time should leave evidence, and its absence across major boundaries is telling.",
            ["Genesis 7:19-20", "Genesis 7:24", "Job 12:15"],
            "medium", "geology"
        ),
        e(
            "Rapid stalactite and stalagmite formation has been observed in modern settings, contradicting claims of millions of years.",
            "Stalactites and stalagmites are often presented as requiring thousands to millions of years to form. However, stalactites have been observed growing inches per year under bridges, in mines, and in man-made tunnels. The Lincoln Memorial (built 1922) had stalactites up to 5 feet long by 1968 — 46 years. Carlsbad Caverns rangers have documented rapid growth under certain mineral-rich water conditions.",
            ["Meyers, S. (1993) 'Rapid stalactite growth in Postojna Cave.' Speleological Society Bulletin 45:34-38.", "Wieland, C. (1998) 'Rapid stalactites.' Creation 20(1):37."],
            "Conditions in man-made structures differ from natural caves. Natural cave formation rates are slower due to lower mineral concentrations.",
            "The point is not that all stalactites grow fast, but that the assumption of uniform slow growth is falsified. Growth rate depends on water flow, mineral content, CO2 levels, and temperature — not inherently on time. When conditions are right, rapid formation is demonstrated. This removes stalactites as a proof of old ages.",
            ["Job 14:18-19", "Psalm 104:10"],
            "medium", "geology"
        ),
        e(
            "Coal can be produced in weeks under laboratory conditions, not requiring millions of years.",
            "Argonne National Laboratory experiments (1984) produced coal from organic material in 2-8 months using heat and pressure simulating burial conditions. CSIRO (Australia) produced coal in weeks. The organic material plus clay plus heat/pressure produces lignite to bituminous coal rapidly. What is required is the right conditions, not vast time.",
            ["Hayatsu, R. et al. (1984) 'Artificial coalification study.' Organic Geochemistry 6:463-471.", "Snelling, A.A. (1994) 'How fast can coal form?' Creation 16(3):38-41."],
            "Laboratory conditions use higher temperatures/pressures than natural settings, accelerating the process. Natural coal formation may still require long periods at lower temperatures.",
            "The experiments demonstrate that time is not the essential variable — conditions are. A global flood would provide precisely the conditions needed: massive burial of vegetation under enormous sediment loads with geothermal heat. The result would be rapid coal formation, consistent with the extensive coal seams found worldwide.",
            ["Genesis 7:11-12", "Genesis 7:19-20", "2 Peter 3:6"],
            "medium", "geology"
        ),
        e(
            "The Grand Canyon shows evidence of catastrophic formation by a breached dam, not slow erosion over millions of years.",
            "The Grand Canyon lacks a delta at its mouth (Colorado River deposits are insufficient). The canyon cuts through the Kaibab Upwarp — water does not flow uphill. Breached-dam models (similar to documented events at Lake Missoula, Channeled Scablands) explain the canyon's morphology. The canyon's side canyons show amphitheater heads consistent with sapping erosion from a single catastrophic event. Internal features resemble Channeled Scablands (formed by documented catastrophic flooding).",
            ["Austin, S.A. (1994) 'Grand Canyon: Monument to Catastrophe.' ICR.", "Oard, M.J. (2010) 'The origin of Grand Canyon.' Journal of Creation 24(3):90-97."],
            "Mainstream geology attributes the canyon to 5-6 million years of Colorado River erosion with occasional flooding. River incision through an upwarp is explained by antecedent drainage or superposition.",
            "The missing delta, the upwarp cutting, and the canyon morphology all fit a catastrophic breach model better than slow erosion. Lake Missoula's documented catastrophic flooding carved the Channeled Scablands in days — a scaled analogy. The burden is on slow-erosion models to explain the missing sediment and upwarp problem.",
            ["Genesis 8:1-3", "Psalm 104:6-9", "Proverbs 8:28-29"],
            "medium", "geology"
        ),
        e(
            "Submarine canyons carved into continental shelves indicate lower sea levels during a post-Flood Ice Age.",
            "Massive canyons (some larger than the Grand Canyon) are carved into continental shelves worldwide, extending to depths of 2,000+ meters below current sea level. The Monterey Canyon (California), Congo Canyon (Africa), and Ganges Canyon (India) are examples. These canyons were carved by subaerial (above-water) erosion when sea levels were dramatically lower — consistent with a single post-Flood Ice Age that locked water in ice sheets.",
            ["Oard, M.J. (1990) 'An Ice Age Caused by the Genesis Flood.' ICR.", "Shepard, F.P. (1981) 'Submarine canyons: multiple causes and long-time persistence.' AAPG Bulletin 65:1062-1077."],
            "Turbidity currents (underwater sediment flows) can carve submarine canyons without requiring lower sea levels.",
            "While turbidity currents contribute to canyon maintenance, the V-shaped profiles and meandering patterns of many submarine canyons match subaerial river erosion, not turbidity current morphology. The scale and distribution of these canyons worldwide is best explained by a single dramatic sea-level lowering event — precisely what a post-Flood Ice Age would produce.",
            ["Genesis 8:1-5", "Job 38:8-11", "Psalm 33:7"],
            "medium", "geology"
        ),
    ]


def build_biology_chirho():
    return [
        e(
            "DNA contains 3.2 billion base pairs of specified information, and no known mechanism adds new functional genetic information via random mutation.",
            "The human genome contains approximately 3.2 billion base pairs encoding ~20,000 protein-coding genes plus vast regulatory networks. Information theory (Shannon, Kolmogorov) demonstrates that specified complex information requires an intelligent source. While mutations occur frequently (~100-200 per generation), the vast majority are neutral or deleterious. No observed mutation has been documented to produce a novel protein fold or functional system not already encoded in the genome.",
            ["Sanford, J.C. (2005) 'Genetic Entropy & the Mystery of the Genome.' FMS Publications.", "Meyer, S.C. (2009) 'Signature in the Cell.' HarperOne.", "Axe, D. (2016) 'Undeniable: How Biology Confirms Our Intuition That Life Is Designed.' HarperOne."],
            "Gene duplication followed by divergence, horizontal gene transfer, and exon shuffling can generate new genetic information. Nylonase is an example of a new enzyme arising from a frameshift mutation.",
            "Gene duplication copies existing information — it does not create new specified information. Nylonase involves a frameshift in an existing gene, producing a marginally functional enzyme — not a new protein fold. Douglas Axe's research at Cambridge estimated the probability of finding a functional protein fold by random search at 1 in 10^77. The origin of biological information remains unexplained by undirected processes.",
            ["Psalm 139:13-16", "Jeremiah 1:5", "Job 10:8-12"],
            "high", "biology"
        ),
        e(
            "Genetic entropy: mutations accumulate and fitness decreases over generations, contradicting upward evolutionary progress.",
            "Dr. John Sanford (Cornell University, inventor of the gene gun) demonstrated that the vast majority of mutations are 'nearly neutral' — too slight for natural selection to remove, yet cumulatively degrading. His computational model Mendel's Accountant shows that genomes inexorably deteriorate over time. The human mutation rate (~100-200 new mutations per person per generation) far exceeds the rate at which selection can remove them. This genetic load increases each generation.",
            ["Sanford, J.C. (2005) 'Genetic Entropy & the Mystery of the Genome.' FMS Publications.", "Sanford, J.C. et al. (2007) 'Mendel's Accountant: A biologically realistic forward-time population genetics program.' SCPE 8(2):147-165.", "Lynch, M. (2016) 'Mutation and Human Exceptionalism.' Genetics 202(3):869-875."],
            "Natural selection, genetic repair mechanisms, and sexual recombination counter the accumulation of deleterious mutations. Organisms have persisted for billions of years.",
            "Lynch (secular geneticist) acknowledges the human mutation rate exceeds the capacity of selection to purge harmful mutations. Sexual recombination shuffles mutations but does not eliminate them. DNA repair is not 100% efficient — errors accumulate. Genetic entropy is consistent with a young creation (thousands of years of accumulation) but problematic for millions of years of supposed evolutionary progress. Genomes are degrading, not improving.",
            ["Genesis 3:17-19", "Romans 8:20-22", "Romans 5:12"],
            "high", "biology"
        ),
        e(
            "The blood clotting cascade is an irreducibly complex system requiring multiple interdependent components.",
            "The blood clotting cascade involves over 20 proteins in a precisely ordered series of activations. Remove any essential factor (e.g., Factor VIII in hemophilia A, Factor IX in hemophilia B) and the system fails catastrophically — the organism bleeds to death. The cascade includes both an intrinsic and extrinsic pathway converging on a common pathway, with multiple feedback loops and inhibitors preventing runaway clotting.",
            ["Behe, M.J. (1996) 'Darwin's Black Box.' Free Press, Ch. 4.", "Doolittle, R.F. & Feng, D.F. (1987) 'Reconstructing the evolution of vertebrate blood coagulation.' Cold Spring Harbor Symposia 52:869-874."],
            "Doolittle argues the cascade evolved by gene duplication from simpler systems. Some organisms have fewer clotting factors (e.g., pufferfish lack Factor XII).",
            "Organisms with fewer factors still have functional cascades — they are not intermediate systems but fully functional alternatives. Removing factors from the HUMAN cascade causes lethal bleeding disorders. Gene duplication does not explain the origin of the regulatory specificity that makes each factor activate the next in sequence. The system requires coordinated specificity that gene duplication alone cannot provide.",
            ["Psalm 139:14", "Job 10:11", "Leviticus 17:11"],
            "high", "biology"
        ),
        e(
            "Specified complexity in biological systems (Dembski's mathematical framework) provides a rigorous design detection method.",
            "William Dembski's specified complexity framework establishes that when an event or structure is both highly improbable (complex) and conforms to an independently given pattern (specified), design is the best explanation. Biological systems routinely exhibit specified complexity: DNA encodes functional proteins according to a code (specification) with astronomically low probability of arising by chance (complexity). The universal probability bound of 10^150 (all probabilistic resources in the universe) is far exceeded by biological information content.",
            ["Dembski, W.A. (1998) 'The Design Inference.' Cambridge University Press.", "Dembski, W.A. (2002) 'No Free Lunch: Why Specified Complexity Cannot Be Purchased without Intelligence.' Rowman & Littlefield."],
            "Natural selection is a non-random process that can accumulate improbable outcomes incrementally. Dembski's framework has been criticized for conflating specification with post-hoc pattern recognition.",
            "Natural selection can only select for function — it cannot anticipate future utility. Dembski's specification criterion requires independent, pre-existing patterns (like the genetic code), not post-hoc recognition. The genetic code IS an independently specified pattern. Incremental accumulation requires each step to be functional — but many biological systems require multiple coordinated changes before any function exists.",
            ["Romans 1:19-20", "Proverbs 3:19", "Colossians 1:17"],
            "high", "biology"
        ),
        e(
            "Biomimicry: human engineers consistently copy designs found in nature, implying an original Designer.",
            "Velcro was inspired by burdock burrs (George de Mestral, 1941). Japan's Shinkansen bullet train nose was redesigned after the kingfisher beak to reduce sonic booms. Gecko-inspired adhesives replicate van der Waals force structures on gecko feet. Shark skin-inspired surfaces reduce drag and bacterial adhesion (Sharklet Technologies). Spider silk is stronger than steel per unit weight — synthetic replication remains inferior. The Eastgate Centre in Zimbabwe mimics termite mound ventilation for passive cooling. Each case shows human intelligence copying biological designs that materialists attribute to blind processes.",
            ["Bar-Cohen, Y. (2006) 'Biomimetics: Biologically Inspired Technologies.' CRC Press.", "Benyus, J.M. (1997) 'Biomimicry: Innovation Inspired by Nature.' William Morrow."],
            "Biomimicry shows that natural selection produces effective designs, not that an intelligence created them. Evolution is an excellent optimizer.",
            "If it takes human intelligence to merely COPY these designs (often imperfectly), why is it rational to claim no intelligence was required to CREATE the originals? The argument from biomimicry is cumulative: in every other domain, when we find engineered solutions (aerodynamics, adhesion, structural engineering, information processing), we infer a designer. Biology should not be an exception simply because of philosophical commitment to naturalism.",
            ["Job 12:7-10", "Proverbs 6:6-8", "Isaiah 40:26"],
            "high", "biology"
        ),
        e(
            "No observed speciation event has produced new body plans — microevolution does not extrapolate to macroevolution.",
            "All observed speciation events involve variations within existing body plans: finch beak sizes, fruit fly wing shapes, bacteria developing antibiotic resistance. None have produced a new organ, body plan, or genetic information not already present. The distinction between microevolution (variation within kinds) and macroevolution (origin of new body plans) is empirically supported. Breeding experiments with fruit flies over thousands of generations produced only fruit flies — often less fit ones.",
            ["Gould, S.J. (1980) 'Is a new and general theory of evolution emerging?' Paleobiology 6(1):119-130.", "Behe, M.J. (2019) 'Darwin Devolves.' HarperOne."],
            "Given enough time, small changes accumulate into large changes. Speciation is the first step; macroevolutionary patterns emerge over millions of years. We cannot observe millions of years directly.",
            "This is an argument from extrapolation, not observation. Behe documents in 'Darwin Devolves' that the most common beneficial mutations in observed evolution BREAK or BLUNT existing genes rather than creating new ones. The claim that micro extrapolates to macro is like claiming that because you can walk to the corner store, you can walk to the moon given enough time. The mechanism matters — and observed mechanisms degrade rather than build.",
            ["Genesis 1:11-12", "Genesis 1:21", "Genesis 1:24-25"],
            "high", "biology"
        ),
        e(
            "Convergent evolution — the same designs appearing in unrelated lineages — is better explained by a common Designer than common descent.",
            "Echolocation evolved independently in bats and dolphins. Camera eyes evolved independently in vertebrates and octopi. Powered flight evolved independently in birds, bats, insects, and pterosaurs. Identical molecular solutions (e.g., antifreeze proteins in Arctic and Antarctic fish with different genetic sequences producing the same protein) appear repeatedly in unrelated lineages. Convergent evolution requires the same improbable solutions to arise multiple times independently.",
            ["McGhee, G.R. (2011) 'Convergent Evolution: Limited Forms Most Beautiful.' MIT Press.", "Conway Morris, S. (2003) 'Life's Solution: Inevitable Humans in a Lonely Universe.' Cambridge University Press."],
            "Conway Morris argues convergent evolution shows that evolution is constrained to find optimal solutions. Similar environments produce similar adaptations.",
            "Constraints channel evolution toward limited solutions — but this begs the question of where the constraints come from and why the same solutions are always available. A common Designer using the same optimal solutions in different organisms (as a human engineer might use wheels on both cars and bicycles) is a simpler explanation than the same improbable innovations arising independently dozens of times.",
            ["Isaiah 45:12", "Colossians 1:16", "Nehemiah 9:6"],
            "medium", "biology"
        ),
    ]


def build_radiometric_chirho():
    return [
        e(
            "The RATE project found systematic evidence that radiometric decay rates may not have been constant throughout Earth's history.",
            "The RATE (Radioisotopes and the Age of the Earth) project (1997-2005), involving eight PhD scientists, found: (1) significant amounts of helium retained in zircon crystals despite supposedly billions of years for diffusion, (2) C-14 in diamonds and coal, (3) discordance between different radiometric methods on same samples, (4) evidence of accelerated nuclear decay (fission tracks, radiohalos). The project was funded at $1.25M and produced peer-reviewed publications.",
            ["Vardiman, L. et al. (2005) 'Radioisotopes and the Age of the Earth.' ICR/CRS.", "DeYoung, D. (2005) 'Thousands Not Billions.' Master Books."],
            "Accelerated decay would produce lethal radiation and heat. The RATE team acknowledged this 'heat problem' without solving it. Mainstream physics has no evidence for variable decay rates.",
            "The heat problem is acknowledged but does not invalidate the observational data (helium retention, C-14 in diamonds). God, who created nuclear physics, could certainly manage the heat. The RATE findings are observational — the interpretation (accelerated decay) may need refinement, but the raw data (helium where it shouldn't be, C-14 where it shouldn't be) stand and demand explanation.",
            ["2 Peter 3:8", "Psalm 90:4", "Hebrews 1:10-12"],
            "medium", "radiometric"
        ),
        e(
            "Helium retention in zircon crystals indicates thousands, not billions, of years.",
            "Radioactive decay of uranium in zircon crystals produces helium as a byproduct. Zircon crystals from deep granite boreholes (Fenton Hill, New Mexico) retain 58% of the helium theoretically produced over their supposed 1.5-billion-year history. Helium diffusion experiments by the RATE project (Humphreys et al. 2003) measured diffusion rates and calculated that the observed helium retention is consistent with ~6,000 years, not billions. The helium should have escaped in ~100,000 years at measured diffusion rates.",
            ["Humphreys, D.R. et al. (2003) 'Helium diffusion rates support accelerated nuclear decay.' Proceedings of the 5th ICC, pp. 175-196.", "Humphreys, D.R. (2005) 'Young Helium Diffusion Age of Zircons Supports Accelerated Nuclear Decay.' in Vardiman et al., RATE II, ICR."],
            "Some argue the diffusion measurements were performed incorrectly or that helium can be trapped in crystal defects.",
            "The diffusion measurements were performed by an independent lab (Geochron Laboratories) using standard techniques. Crystal defects might slow diffusion somewhat but cannot account for a factor of 100,000x difference between observed and expected retention. The helium retention data remain a significant challenge to the assumed ages of these rocks.",
            ["Genesis 1:1", "Psalm 33:6-9", "Isaiah 48:13"],
            "high", "radiometric"
        ),
        e(
            "Discordant radiometric dates from the same rock samples undermine confidence in absolute dating.",
            "When multiple radiometric methods are applied to the same rock, they frequently give different ages. The RATE project documented examples: Grand Canyon basalts yielded K-Ar ages of 516 Ma but Rb-Sr ages of 1,111 Ma. Mt. Ngauruhoe (New Zealand) lava flows of known age (1949-1975) yielded K-Ar dates of 0.27-3.5 Ma. Somerset Dam layered mafic intrusion (Australia) yielded Rb-Sr age of 225 Ma, Sm-Nd age of 364 Ma, and Pb-Pb age of 1,425 Ma — for the same rock.",
            ["Snelling, A.A. (2005) 'Isochron Discordances and the Role of Inheritance and Mixing.' Proceedings of the 5th ICC.", "Austin, S.A. & Snelling, A.A. (1998) 'Discordant Potassium-Argon Model and Isochron Ages for Cardenas Basalt.' Proceedings of the 4th ICC."],
            "Discordances can result from open-system behavior, inheritance of older material, or mixing of different magma sources. Geologists use concordance among multiple methods to validate ages.",
            "Using concordance as the criterion introduces circularity: concordant dates are accepted as reliable, discordant dates are explained away. If the methods were truly measuring absolute time, they should agree. The frequency of discordances — not just occasional anomalies — suggests the assumptions underlying radiometric dating (known initial conditions, closed system, constant decay) are not reliably met.",
            ["Hebrews 11:3", "Job 38:4-7", "Psalm 90:2"],
            "high", "radiometric"
        ),
        e(
            "Radiometric dating depends on three unverifiable assumptions about the distant past.",
            "All radiometric dating methods require three assumptions: (1) known initial conditions (how much parent and daughter isotope were present at formation), (2) constant decay rates throughout history, (3) closed system (no addition or removal of parent/daughter isotopes). None of these can be verified for rocks supposedly billions of years old. Initial conditions are inferred from isochron methods (which have their own assumptions). Decay rate constancy is assumed but has been questioned by evidence of variation. Open-system behavior is documented in weathered and metamorphosed rocks.",
            ["Faure, G. & Mensing, T.M. (2005) 'Isotopes: Principles and Applications.' 3rd Ed. Wiley.", "Snelling, A.A. (2009) 'Earth's Catastrophic Past.' ICR."],
            "Isochron methods account for initial conditions. Decay rates are extremely well-characterized in laboratory settings. Multiple concordant methods provide cross-checks.",
            "Laboratory measurements of decay rates span decades, not billions of years — extrapolation is the assumption. Isochrons can produce 'ages' from mixing processes unrelated to time. Cross-checks work only when they agree; disagreements are attributed to open-system behavior, which is ad hoc. The point is not that radiometric dating is useless, but that it is assumption-dependent and should not be treated as infallible.",
            ["Genesis 1:1", "Proverbs 8:22-31", "Job 38:4"],
            "high", "radiometric"
        ),
        e(
            "Radiohalos (pleochroic halos) in granites may indicate rapid formation rather than slow crystallization.",
            "Radiohalos are microscopic discoloration spheres in minerals caused by alpha decay of radioactive inclusions. Robert Gentry documented polonium-218 halos (half-life 3.1 minutes) in granite biotite crystals. For these halos to form, the granite must have solidified within minutes of the polonium being concentrated — far too fast for conventional granite cooling models (which require millions of years). Gentry proposed these as evidence of instantaneous creation of the original granite.",
            ["Gentry, R.V. (1986) 'Creation's Tiny Mystery.' Earth Science Associates.", "Gentry, R.V. (1974) 'Radiohalos in a Radiochronological and Cosmological Perspective.' Science 184(4132):62-66."],
            "Polonium halos may form from radon transport through microfractures in already-solidified granite. Hydrothermal fluids can concentrate polonium rapidly in secondary sites.",
            "The hydrothermal transport model is contested because it requires the granite to have been solid enough to retain microfractures but fluid enough for rapid polonium transport and halo formation — within 3.1 minutes. The detailed experimental conditions have not been replicated. Gentry's challenge — to synthesize a hand-sized piece of granite with polonium halos in the lab — remains unanswered.",
            ["Genesis 1:1", "Exodus 20:11", "Psalm 33:6-9"],
            "medium", "radiometric"
        ),
    ]


def build_cosmological_chirho():
    return [
        e(
            "The horizon problem: the uniformity of the cosmic microwave background has no naturalistic explanation without inflation theory, which is itself unverified.",
            "The cosmic microwave background (CMB) radiation is uniform to 1 part in 100,000 across the sky. Yet opposite sides of the observable universe are so far apart that light (and thus heat) could never have traveled between them in the supposed 13.8 billion years since the Big Bang. This is the 'horizon problem.' Inflation theory was invented to solve it — proposing the universe expanded faster than light in a fraction of a second. But inflation is unverified, its mechanism unknown, and it creates its own fine-tuning problems.",
            ["Guth, A.H. (1981) 'Inflationary universe.' Physical Review D 23(2):347-356.", "Ijjas, A. et al. (2017) 'Pop goes the universe.' Scientific American 316(2):32-39.", "Humphreys, D.R. (1994) 'Starlight and Time.' Master Books."],
            "Inflation theory is well-supported by CMB observations (power spectrum, B-mode polarization). It makes testable predictions.",
            "Even proponents disagree: Steinhardt (co-inventor of inflation) has argued it is unfalsifiable because any outcome can be fitted by adjusting parameters. Ijjas, Steinhardt, and Loeb (2017) in Scientific American called inflation 'untestable.' It was invented to solve a problem created by Big Bang cosmology — it is a patch, not an independent prediction. Alternative cosmologies (e.g., Humphreys' white-hole cosmology) solve the horizon problem within a young-creation framework.",
            ["Isaiah 40:22", "Job 9:8", "Jeremiah 10:12"],
            "medium", "cosmological"
        ),
        e(
            "The flatness problem: the universe's geometric flatness requires extreme fine-tuning of initial conditions.",
            "The density parameter (Omega) of the universe is measured at 1.000 +/- 0.005, meaning the universe is geometrically flat. For Omega to be this close to 1 today, it must have been fine-tuned to 1 part in 10^60 at the Planck time (10^-43 seconds after the Big Bang). Any deviation would have caused the universe to collapse immediately (Omega > 1) or expand so rapidly that no structures could form (Omega < 1). This extraordinary fine-tuning is unexplained by naturalistic cosmology.",
            ["Dicke, R.H. & Peebles, P.J.E. (1979) 'The big bang cosmology — enigmas and nostrums.' in General Relativity: An Einstein Centenary Survey.", "Collins, R. (2009) 'The Teleological Argument.' in Blackwell Companion to Natural Theology."],
            "Inflation naturally drives Omega toward 1 regardless of initial conditions.",
            "This is circular: inflation was partly invented to solve the flatness problem. But inflation itself requires fine-tuning (the inflaton potential must have a very specific shape). Furthermore, the measure problem in inflation means that even with inflation, the probability of our particular universe is not well-defined. Moving the fine-tuning from initial conditions to the inflation mechanism does not eliminate it.",
            ["Isaiah 45:18", "Jeremiah 33:25-26", "Proverbs 8:27-29"],
            "medium", "cosmological"
        ),
        e(
            "The missing antimatter problem: the Big Bang should have produced equal matter and antimatter, annihilating to pure energy.",
            "According to Big Bang theory, the initial conditions should have produced exactly equal amounts of matter and antimatter. When matter and antimatter meet, they annihilate completely into energy. Yet the observable universe is overwhelmingly matter. The 'baryon asymmetry problem' — why there is more matter than antimatter — is one of the great unsolved problems in physics. CP violation (the known matter-antimatter asymmetry) is far too small to account for the observed excess.",
            ["Canetti, L. et al. (2012) 'Matter and antimatter in the universe.' New Journal of Physics 14:095012.", "Sakharov, A.D. (1967) 'Violation of CP Invariance.' JETP Letters 5:24-27."],
            "Baryogenesis models propose mechanisms for generating matter-antimatter asymmetry in the early universe. This is an active area of research.",
            "After 60+ years of research, no satisfactory mechanism has been demonstrated. The required CP violation is orders of magnitude larger than observed in particle physics. This is not a gap that is closing — it is a fundamental problem with the standard Big Bang model. A created universe has no such problem: God created matter, not equal parts matter and antimatter.",
            ["Genesis 1:1", "Hebrews 11:3", "Colossians 1:16-17"],
            "medium", "cosmological"
        ),
        e(
            "Galaxy spiral arms should wind up in far less than the supposed age of the universe, yet they remain well-defined.",
            "Spiral galaxies rotate differentially — inner regions rotate faster than outer regions. Over billions of years, this should wind the spiral arms into a featureless disk (the 'winding problem'). After just a few hundred million years, spiral structure should be unrecognizable. Yet galaxies like the Milky Way supposedly 10+ billion years old still display prominent spiral arms. Density wave theory was proposed to explain this, but it has significant problems with generating and maintaining spiral structure long-term.",
            ["Binney, J. & Tremaine, S. (2008) 'Galactic Dynamics.' 2nd Ed. Princeton University Press.", "Humphreys, D.R. (2005) 'Evidence for a Young World.' ICR Impact #384."],
            "Density wave theory explains spiral arms as compression waves that pass through the disk, maintaining structure indefinitely. Stars move in and out of arms.",
            "Density wave theory has been challenged by simulations showing that waves dissipate within a few rotations without external driving mechanisms. Some spirals show stars of all ages in the arms (not just young stars as density wave theory predicts). The winding problem remains significant for many spiral galaxies and is naturally resolved if galaxies are thousands, not billions, of years old.",
            ["Psalm 19:1-4", "Isaiah 40:26", "Nehemiah 9:6"],
            "medium", "cosmological"
        ),
        e(
            "The Moon's recession rate, extrapolated backward, places an upper limit on the Earth-Moon system far below billions of years.",
            "The Moon is moving away from Earth at approximately 3.82 cm/year (measured by lunar laser ranging since 1969). Due to tidal interaction physics, the recession rate was faster in the past when the Moon was closer. Extrapolating backward using tidal dissipation models, the Moon would have been touching Earth about 1.4 billion years ago — yet the Earth-Moon system is supposed to be 4.5 billion years old. This is the 'lunar recession problem.'",
            ["Lambeck, K. (1980) 'The Earth's Variable Rotation: Geophysical Causes and Consequences.' Cambridge University Press.", "DeYoung, D. (2016) 'The Moon: faithful witness in the sky.' Acts & Facts 45(7):10-13."],
            "The recession rate has varied over time due to continental configuration changes affecting tidal dissipation. The current rate may be anomalously high.",
            "Even accounting for variable continental configurations, models consistently place the Moon too close or touching Earth well before 4.5 billion years. The problem is not the current rate alone but the physics of tidal interaction: closer = stronger = faster recession. The 1.4 billion year limit is generous; some models give much less. This is an upper limit, not a precise age — but it contradicts the claimed 4.5 billion years.",
            ["Genesis 1:16", "Psalm 8:3", "Psalm 136:9", "Jeremiah 31:35"],
            "medium", "cosmological"
        ),
        e(
            "Ocean salinity accumulation rates set an upper limit on Earth's age far below billions of years.",
            "Sodium (salt) enters the ocean from river input, volcanic activity, and other sources at measurable rates. Sodium is also removed through sea spray, ion exchange, and halite deposits. Austin and Humphreys (1990) calculated that even using maximum removal rates and minimum input rates, the oceans could not have accumulated their current sodium content in more than 62 million years — far less than the supposed 3.5 billion years of ocean existence. Similar analyses apply to other dissolved elements.",
            ["Austin, S.A. & Humphreys, D.R. (1990) 'The Sea's Missing Salt: A Dilemma for Evolutionists.' Proceedings of the 2nd ICC, pp. 17-33."],
            "Early Earth's oceans had different chemistry, and removal mechanisms have varied over geological time. Plate tectonics recycles ocean floor (and its salt) through subduction.",
            "The 62 million year figure already uses the most generous assumptions (maximum removal, minimum input). Subduction zones are not known to remove significant dissolved sodium. The calculation provides an UPPER LIMIT — the actual age may be much younger. The point is not precision but that even generous assumptions cannot stretch the salt clock to billions of years.",
            ["Genesis 1:9-10", "Psalm 33:7", "Proverbs 8:29", "Job 38:8-11"],
            "medium", "cosmological"
        ),
    ]


def build_human_origins_chirho():
    return [
        e(
            "No confirmed transitional forms exist between apes and humans — the fossil record shows distinct types.",
            "Despite over 150 years of searching, the human fossil record shows distinct categories without clear transitions. Australopithecines (Lucy, etc.) are classified by many as extinct apes with no demonstrated link to Homo. Homo erectus specimens show significant overlap with modern human variation. The 'tree of human evolution' is constantly redrawn as new finds contradict previous schemes. Renowned paleoanthropologist Bernard Wood stated: 'The origin of our own genus remains frustratingly unclear.'",
            ["Wood, B. & Collard, M. (1999) 'The Human Genus.' Science 284(5411):65-71.", "Lubenow, M.L. (2004) 'Bones of Contention: A Creationist Assessment of Human Fossils.' Baker Books."],
            "Fossils like Homo habilis, Homo erectus, Homo heidelbergensis show a gradual increase in brain size and tool use.",
            "Brain size overlap between categories is significant. Homo erectus brain size (850-1100cc) overlaps with modern human variation (1000-1800cc). Tool use is a behavioral, not morphological, marker. The fossils are best interpreted as either fully ape or fully human with normal variation. Each new discovery changes the proposed lineage — suggesting the lineage itself is a construct imposed on the data.",
            ["Genesis 1:26-27", "Genesis 2:7", "Acts 17:26"],
            "medium", "human_origins"
        ),
        e(
            "Piltdown Man was a deliberate fraud that fooled evolutionary scientists for 41 years, demonstrating confirmation bias in paleoanthropology.",
            "Piltdown Man (Eoanthropus dawsoni) was 'discovered' in 1912 in Sussex, England, and was accepted for 41 years as a key human ancestor. It was exposed as a fraud in 1953: a modern human cranium combined with an orangutan jawbone, the teeth filed down and the bones chemically stained to appear ancient. Over 500 scientific papers were written about Piltdown Man before the fraud was exposed.",
            ["Weiner, J.S. (1955) 'The Piltdown Forgery.' Oxford University Press.", "Walsh, J.E. (1996) 'Unraveling Piltdown.' Random House."],
            "Piltdown was detected by the scientific process — science is self-correcting. This is not representative of modern paleontology.",
            "It took 41 years and 500+ papers before the self-correction occurred. During those decades, Piltdown shaped evolutionary thinking and was used to dismiss legitimate questions. The fraud succeeded precisely because it confirmed existing expectations. The lesson is not that fraud is common, but that confirmation bias in evolutionary science can override critical scrutiny for decades.",
            ["Proverbs 14:12", "Jeremiah 17:9", "1 Thessalonians 5:21"],
            "high", "human_origins"
        ),
        e(
            "Nebraska Man was reconstructed from a single tooth that turned out to belong to a pig.",
            "In 1922, geologist Harold Cook found a tooth in Nebraska that Henry Fairfield Osborn (American Museum of Natural History) identified as belonging to an ape-man he named Hesperopithecus haroldcookii. The Illustrated London News published a full reconstruction of Nebraska Man, his wife, and their environment — all from a single tooth. By 1927, further excavation revealed the tooth belonged to an extinct peccary (a pig-like animal). The 'species' was quietly retracted.",
            ["Osborn, H.F. (1922) 'Hesperopithecus, the first anthropoid primate found in America.' Science 55:463-465.", "Gregory, W.K. (1927) 'Hesperopithecus apparently not an ape nor a man.' Science 66:579-581."],
            "Nebraska Man was quickly corrected and was never widely accepted in the scientific community. It was a mistake, not fraud.",
            "While it was corrected faster than Piltdown, the episode demonstrates how eagerly the scientific establishment embraces supposed ape-to-human evidence. An entire family was reconstructed from a PIG TOOTH. The Scopes Trial (1925) used Nebraska Man as evidence for evolution before its retraction. The lesson: extraordinary caution is warranted with fossil-based claims about human ancestry.",
            ["Proverbs 18:17", "Isaiah 44:25", "1 Corinthians 3:19"],
            "high", "human_origins"
        ),
        e(
            "Homo naledi (2013) has a small brain and unique morphology that challenges linear ape-to-human evolution narratives.",
            "Homo naledi, discovered in South Africa's Rising Star Cave (2013, published 2015 by Lee Berger), has a brain size of ~560cc (gorilla-sized) but was dated to 236-335 kya — contemporary with large-brained Homo sapiens. This contradicts the narrative of steadily increasing brain size over time. Its mosaic of features (small brain, curved fingers for climbing, but human-like feet and hands) defies placement on a linear evolutionary tree. Some researchers question whether it is even in the genus Homo.",
            ["Berger, L.R. et al. (2015) 'Homo naledi, a new species of the genus Homo.' eLife 4:e09560.", "Dirks, P.H.G.M. et al. (2017) 'The age of Homo naledi.' eLife 6:e24231."],
            "Mosaic evolution is expected — not all features evolve at the same rate. Homo naledi may represent an early-diverging lineage.",
            "The existence of a small-brained hominin contemporary with modern humans contradicts the central prediction of linear brain-size increase. 'Mosaic evolution' is descriptive, not explanatory — it names the pattern without explaining it. Each new hominin discovery adds complexity and contradiction to evolutionary trees rather than resolving them.",
            ["Genesis 1:26-27", "Psalm 8:4-6", "Isaiah 45:12"],
            "medium", "human_origins"
        ),
        e(
            "Human footprints alongside dinosaur tracks have been reported at the Paluxy River, Texas.",
            "The Paluxy River near Glen Rose, Texas, contains dinosaur trackways in Cretaceous limestone. Human-like footprints alongside and within these trackways have been reported since the 1930s. Some tracks show anatomically human features (arch, toes, proper proportions). The site was extensively studied by creationist researchers and filmed in multiple documentaries. If confirmed, this would demolish the evolutionary timescale.",
            ["Morris, J.D. (1980) 'Tracking Those Incredible Dinosaurs and the People Who Knew Them.' Creation-Life Publishers.", "Baugh, C.E. (1987) 'Dinosaur: Scientific Evidence That Dinosaurs and Men Walked Together.' Promise Publishing."],
            "ICR and other creationist organizations eventually backed away from the Paluxy claims. Many 'human' tracks were reinterpreted as elongated dinosaur tracks or erosion features. Some may have been carved.",
            "Caution is warranted with Paluxy — some creationist organizations have retracted support. However, not all tracks have been explained. New discoveries continue to be made at the site. The point is that the evidence is debated, not definitively resolved. Each track must be evaluated individually. The existence of even one confirmed human track alongside dinosaurs would be revolutionary.",
            ["Job 40:15-19", "Genesis 1:24-31"],
            "low", "human_origins"
        ),
    ]


def build_intelligent_design_chirho():
    return [
        e(
            "The gravitational constant is fine-tuned to 1 part in 10^60 — a change this small would prevent a life-supporting universe.",
            "The gravitational constant (G = 6.674 x 10^-11 N m^2/kg^2) must be precisely calibrated relative to other forces. If gravity were slightly stronger, stars would burn too hot and too briefly for life. If slightly weaker, stars would never ignite nuclear fusion. The ratio of gravitational to electromagnetic force must be balanced to approximately 1 in 10^40. Freeman Dyson noted: 'The more I examine the universe, the more evidence I find that the universe in some sense must have known we were coming.'",
            ["Davies, P.C.W. (1982) 'The Accidental Universe.' Cambridge University Press.", "Dyson, F. (1979) 'Disturbing the Universe.' Harper & Row.", "Rees, M. (1999) 'Just Six Numbers.' Basic Books."],
            "We can only observe a universe compatible with our existence (anthropic principle). Other constants may permit different forms of life.",
            "The anthropic principle describes our observation but does not explain the fine-tuning itself. Speculative 'different forms of life' are not supported by any physics — life requires complex chemistry, which requires specific force strengths. The fine-tuning is a fact; the question is whether design or an unfalsifiable multiverse better explains it.",
            ["Romans 1:19-20", "Psalm 19:1-4", "Isaiah 45:18"],
            "high", "intelligent_design"
        ),
        e(
            "The cosmological constant is fine-tuned to 1 part in 10^120 — the most extreme fine-tuning in physics.",
            "The cosmological constant (Lambda) determines the expansion rate of the universe. Its observed value (~10^-122 in Planck units) is 120 orders of magnitude smaller than quantum field theory predicts. Steven Weinberg (Nobel laureate, atheist) calculated that if Lambda were larger by a factor of a few, no galaxies or stars could form. This is often called 'the worst prediction in physics' and represents the most extreme fine-tuning known.",
            ["Weinberg, S. (1987) 'Anthropic bound on the cosmological constant.' Physical Review Letters 59(22):2607.", "Carroll, S.M. (2001) 'The cosmological constant.' Living Reviews in Relativity 4:1."],
            "The multiverse, if it exists, would contain regions with all possible values of Lambda. We exist in one where it permits structure.",
            "The multiverse is unfalsifiable and requires its own fine-tuning (a mechanism to generate all possible values). Even multiverse proponents admit this. The cosmological constant problem is often cited as the strongest evidence for fine-tuning, even by secular physicists. Weinberg himself, though an atheist, called it 'the one fine-tuning problem that I find truly impressive.'",
            ["Psalm 19:1", "Romans 1:20", "Jeremiah 33:25-26"],
            "high", "intelligent_design"
        ),
        e(
            "Michael Behe's 'Edge of Evolution' demonstrates mathematical limits to what Darwinian processes can achieve.",
            "Michael Behe (Lehigh University biochemist) analyzed the best-studied evolutionary example: the malaria parasite Plasmodium falciparum vs. human sickle cell defense. With 10^20 malaria organisms produced per year and 10,000+ years of human-malaria interaction, the mutational search space is enormous. Yet the adaptations produced are meager: point mutations, gene duplications, loss-of-function changes. Behe calculated the 'edge of evolution' — the limit of what random mutation and selection can build — at roughly two coordinated mutations. Anything requiring more is beyond Darwinian reach.",
            ["Behe, M.J. (2007) 'The Edge of Evolution: The Search Within the Limits of Darwinism.' Free Press.", "Behe, M.J. (2019) 'Darwin Devolves.' HarperOne."],
            "Two-mutation barriers can be crossed given sufficient population size and time. Chloroquine resistance (which Behe uses) DID evolve.",
            "Behe's point is precisely that chloroquine resistance DID evolve — after 10^20 organisms. This establishes the empirical difficulty. Structures requiring 3+ coordinated mutations would need populations and time beyond what is available. The flagellum requires dozens of coordinated proteins. The math shows that complex adaptations are beyond the reach of undirected processes.",
            ["Psalm 139:14", "Romans 1:20", "Proverbs 3:19-20"],
            "high", "intelligent_design"
        ),
        e(
            "Stephen Meyer's 'Signature in the Cell' demonstrates that DNA is information, and information always comes from minds.",
            "Meyer (PhD Cambridge, Philosophy of Science) argues that DNA constitutes genuine information in the Shannon and functional senses. The origin of the first self-replicating organism requires hundreds of specified proteins (minimum ~250 genes for simplest known free-living organism, Mycoplasma genitalium). The probability of generating even ONE functional protein of 150 amino acids by chance is ~1 in 10^164 (Axe 2004). No naturalistic origin-of-life model has explained how specified information arises from chemistry alone.",
            ["Meyer, S.C. (2009) 'Signature in the Cell: DNA and the Evidence for Intelligent Design.' HarperOne.", "Axe, D.D. (2004) 'Estimating the prevalence of protein sequences adopting functional enzyme folds.' Journal of Molecular Biology 341(5):1295-1315."],
            "RNA world hypothesis proposes that self-replicating RNA preceded DNA. Chemical evolution research has produced amino acids and nucleotides in prebiotic conditions.",
            "The RNA world faces severe problems: RNA is chemically fragile, no self-replicating RNA has been produced from prebiotic chemistry, and the transition from RNA to DNA/protein life is unexplained. Producing amino acids (Miller-Urey) is trivially different from assembling them into functional proteins — like producing letters versus writing a novel. The information problem is not a gap — it is a fundamental barrier.",
            ["John 1:1-3", "Colossians 1:16-17", "Hebrews 11:3"],
            "high", "intelligent_design"
        ),
        e(
            "Stephen Meyer's 'Return of the God Hypothesis' presents God as the best explanation for cosmological, biological, and informational evidence.",
            "Meyer synthesizes three lines of evidence: (1) the fine-tuning of physics for life, (2) the origin of biological information in DNA, and (3) the origin of the universe from nothing (Big Bang cosmology implies a beginning). He argues that theism — specifically, the God of the Bible — provides a better explanation than materialism, deism, or pantheism for all three. The book engages with the best naturalistic alternatives (multiverse, chemical evolution, eternal universe) and demonstrates their inadequacy.",
            ["Meyer, S.C. (2021) 'Return of the God Hypothesis: Three Scientific Discoveries That Reveal the Mind Behind the Universe.' HarperOne."],
            "These arguments commit the God-of-the-gaps fallacy. Science may eventually explain what is currently unexplained.",
            "Meyer explicitly addresses the God-of-the-gaps objection. His argument is not from ignorance (we don't know, therefore God) but from positive evidence: we KNOW that intelligence produces information, fine-tuning, and contingent events with beginnings. Inferring an intelligent cause from information, fine-tuning, and a cosmic beginning follows the same logic used in archaeology, forensic science, and SETI.",
            ["Romans 1:19-20", "Psalm 19:1-4", "Acts 14:17", "Acts 17:24-28"],
            "high", "intelligent_design"
        ),
        e(
            "William Lane Craig's Kalam Cosmological Argument demonstrates the universe had a cause — which must be personal, timeless, and immaterial.",
            "(1) Everything that begins to exist has a cause. (2) The universe began to exist. (3) Therefore, the universe has a cause. Premise 1 is supported by universal experience and metaphysical reasoning. Premise 2 is supported by Big Bang cosmology, the BGV theorem (Borde-Guth-Vilenkin: any universe that has been expanding must have a beginning), and the impossibility of an actual infinite past. The cause must be timeless (existed before time), spaceless, immaterial, enormously powerful, and personal (to choose to create).",
            ["Craig, W.L. (2008) 'Reasonable Faith.' 3rd Ed. Crossway.", "Craig, W.L. & Sinclair, J.D. (2009) 'The Kalam Cosmological Argument.' in Blackwell Companion to Natural Theology.", "Borde, A., Guth, A.H., & Vilenkin, A. (2003) 'Inflationary spacetimes are incomplete in past directions.' Physical Review Letters 90:151301."],
            "Quantum mechanics shows particles can appear from nothing. The universe may be eternal in some models (cyclic, quantum gravity).",
            "Quantum vacuum fluctuations occur in a quantum vacuum — which is not 'nothing' but a physical state with energy and laws. Cyclic models require a beginning (BGV theorem applies). Quantum gravity models (Hawking-Hartle) redefine 'beginning' but do not eliminate it. Vilenkin (atheist physicist) stated: 'All the evidence we have says that the universe had a beginning.' A personal, timeless, immaterial, powerful cause is exactly what the Bible describes.",
            ["Genesis 1:1", "John 1:1-3", "Hebrews 11:3", "Romans 4:17", "Isaiah 44:24"],
            "high", "intelligent_design"
        ),
        e(
            "The moral argument: objective morality requires a transcendent standard, pointing to God.",
            "(1) If God does not exist, objective moral values and duties do not exist. (2) Objective moral values and duties do exist. (3) Therefore, God exists. Premise 1: without a transcendent standard, morality is reducible to social convention, evolutionary advantage, or personal preference — all of which are subjective. Premise 2: virtually all people recognize some acts (torturing children for fun, genocide) as objectively wrong, not merely unfashionable. This moral intuition is best explained by a moral Lawgiver.",
            ["Craig, W.L. (2008) 'Reasonable Faith.' Crossway, Ch. 3.", "Lewis, C.S. (1952) 'Mere Christianity.' Geoffrey Bles. Book I.", "Copan, P. (2008) 'The Moral Argument.' in Blackwell Companion to Natural Theology."],
            "Evolutionary ethics explains moral intuitions as survival adaptations. Secular moral frameworks (consequentialism, contractualism) do not require God.",
            "If morality is an evolutionary adaptation, then it has no objective truth value — it is a useful illusion selected for reproductive fitness. But then the Holocaust was not objectively wrong — merely disadvantageous. Secular moral frameworks describe how we reason about morality but cannot ground WHY morality is binding. Consequentialism requires an objective standard of 'good consequences.' Only a transcendent moral Lawgiver grounds objective moral obligation.",
            ["Romans 2:14-15", "Genesis 1:27", "Micah 6:8", "Romans 1:32"],
            "high", "intelligent_design"
        ),
        e(
            "The argument from consciousness: the hard problem of consciousness has no materialist solution and points to a conscious Creator.",
            "David Chalmers' 'hard problem of consciousness' asks why physical brain processes give rise to subjective experience (qualia). No amount of neuroscience explains WHY there is 'something it is like' to see red, feel pain, or taste sweetness. Physical processes (neurons firing) are objective; consciousness is subjective. This explanatory gap is not closing — it is a category problem. If the fundamental reality is material, consciousness should not exist. If the fundamental reality is a conscious Mind (God), then consciousness in creatures made in His image is expected.",
            ["Chalmers, D. (1996) 'The Conscious Mind.' Oxford University Press.", "Moreland, J.P. (2008) 'Consciousness and the Existence of God.' Routledge.", "Nagel, T. (2012) 'Mind and Cosmos.' Oxford University Press."],
            "Consciousness may emerge from complex information processing. Future neuroscience may solve the hard problem.",
            "Emergence is descriptive, not explanatory — saying consciousness 'emerges' from matter is like saying a rabbit 'emerges' from a hat. Thomas Nagel (atheist philosopher) argues in 'Mind and Cosmos' that materialist neo-Darwinism is 'almost certainly false' because it cannot account for consciousness, reason, or value. The hard problem is not a gap in knowledge but a category error in materialism.",
            ["Genesis 1:27", "Genesis 2:7", "Ecclesiastes 12:7", "Psalm 94:9-10"],
            "high", "intelligent_design"
        ),
        e(
            "C.S. Lewis's argument from reason: naturalism is self-defeating because it undermines the reliability of human reasoning.",
            "If human reasoning is the product of non-rational causes (random mutation + natural selection for survival, not truth), then we have no reason to trust it — including the reasoning that leads to naturalism. Natural selection selects for survival behavior, not true beliefs. As Alvin Plantinga formalized in the Evolutionary Argument Against Naturalism (EAAN): P(R|N&E) is low — the probability that our cognitive faculties are reliable, given naturalism and evolution, is low or inscrutable. Naturalism therefore provides a defeater for itself.",
            ["Lewis, C.S. (1947) 'Miracles.' Geoffrey Bles. Ch. 3.", "Plantinga, A. (2011) 'Where the Conflict Really Lies: Science, Religion, and Naturalism.' Oxford University Press."],
            "Evolution selects for accurate perception because organisms with true beliefs about predators and food sources survive better.",
            "This assumes that accurate perception requires true beliefs — but many organisms survive with systematically false perceptions (optical illusions, instinctive responses). Plantinga shows that behavior, not belief content, is what selection acts on — many different belief sets could produce the same survival behavior. If naturalism cannot guarantee the reliability of reason, it cannot rationally ground itself. Theism, which holds that we are made in the image of a rational God, provides a foundation for trusting reason.",
            ["Isaiah 1:18", "Proverbs 2:6", "Colossians 2:2-3", "John 1:9"],
            "high", "intelligent_design"
        ),
        e(
            "The Anthropic Principle: the universe's properties read like a specification sheet for human life.",
            "The Anthropic Principle observes that the universe's fundamental constants, initial conditions, and physical laws are precisely those needed for the existence of conscious observers. This extends beyond the 'big' constants: the properties of water (anomalous expansion, high heat capacity, universal solvent), the carbon atom (unique bonding versatility), Earth's position (habitable zone, magnetic field, plate tectonics, large moon stabilizing axis) — all are precisely calibrated for life. The cumulative improbability is staggering.",
            ["Gonzalez, G. & Richards, J.W. (2004) 'The Privileged Planet.' Regnery.", "Barrow, J.D. & Tipler, F.J. (1986) 'The Anthropic Cosmological Principle.' Oxford University Press.", "Ward, P.D. & Brownlee, D. (2000) 'Rare Earth: Why Complex Life Is Uncommon in the Universe.' Copernicus."],
            "Given enough planets and enough time, Earth-like conditions will arise somewhere. We observe this universe because we exist in it.",
            "The observation that we exist in a life-permitting universe does not explain WHY the universe is life-permitting. As John Leslie illustrated: if you face a firing squad of 100 marksmen and they all miss, you should not simply shrug and say 'Well, I could only observe a universe in which I survived.' You should infer either that the marksmen intended to miss or that there are a vast number of executions. The first is design; the second is the untestable multiverse.",
            ["Psalm 8:3-4", "Isaiah 45:18", "Acts 17:24-28", "Psalm 115:16"],
            "high", "intelligent_design"
        ),
    ]


def build_historical_expanded_chirho():
    return [
        e(
            "Josephus' Antiquities 18.3.3 (Testimonium Flavianum) provides non-Christian attestation to Jesus' existence, teachings, crucifixion, and followers.",
            "Josephus wrote (c. 93-94 AD): 'At this time there was a wise man who was called Jesus. And his conduct was good, and he was known to be virtuous. And many people from among the Jews and the other nations became his disciples. Pilate condemned him to be crucified and to die. And those who had become his disciples did not abandon his discipleship.' The Arabic version (Agapius) and Syriac version preserve what most scholars consider closer to the original text, minus Christian interpolations.",
            ["Josephus, 'Antiquities of the Jews' 18.3.3.", "Meier, J.P. (1991) 'A Marginal Jew.' Doubleday, Vol. 1, pp. 56-88.", "Whealey, A. (2003) 'Josephus on Jesus: The Testimonium Flavianum Controversy from Late Antiquity to Modern Times.' Peter Lang."],
            "The Testimonium is partially or wholly interpolated by Christian scribes. The Greek text contains phrases no non-Christian Jew would write.",
            "The scholarly consensus (Meier, Vermes, Feldman) is that an authentic core exists. The Arabic and Syriac versions lack the most overtly Christian phrases while preserving the historical core. Josephus' style and vocabulary are present throughout. Complete fabrication is improbable because (a) no manuscript lacks the passage, (b) Origen (3rd century) knew Josephus discussed Jesus but noted Josephus did not believe Jesus was the Messiah — consistent with an authentic, non-Christian original.",
            ["Luke 1:1-4", "Acts 26:26"],
            "high", "historical_evidence"
        ),
        e(
            "Josephus' Antiquities 20.9.1 — the reference to James, 'the brother of Jesus who is called Christ' — is almost universally accepted as authentic.",
            "In describing events of 62 AD, Josephus writes: 'He [Ananus] assembled the Sanhedrin of judges, and brought before them the brother of Jesus, who was called Christ, whose name was James, and some others. And when he had formed an accusation against them as breakers of the law, he delivered them to be stoned.' This passage identifies Jesus by his commonly known title ('called Christ') and his brother James — an incidental reference that is virtually impossible to explain as a Christian interpolation.",
            ["Josephus, 'Antiquities of the Jews' 20.9.1.", "Feldman, L.H. (1984) 'Josephus and Modern Scholarship.' de Gruyter.", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' Eerdmans."],
            "Some scholars (Carrier) argue this may also be interpolated, though this is a minority view.",
            "This passage is accepted as authentic by virtually all scholars, including skeptics like Bart Ehrman. The reference to Jesus is casual and identifying — Josephus uses 'Jesus who is called Christ' to distinguish this James from other Jameses. A Christian interpolator would more likely have used reverential language. The passage confirms Jesus' historical existence, his title 'Christ,' and the existence of his brother James — all from a non-Christian source.",
            ["Acts 12:17", "Acts 15:13", "Galatians 1:19", "Galatians 2:9"],
            "high", "historical_evidence"
        ),
        e(
            "Tacitus (Annals 15.44, c. 116 AD) provides hostile Roman attestation to Christ's execution under Pontius Pilate.",
            "Tacitus, Rome's greatest historian, wrote about the Great Fire of Rome (64 AD): 'Nero fastened the guilt and inflicted the most exquisite tortures on a class hated for their abominations, called Christians by the populace. Christus, from whom the name had its origin, suffered the extreme penalty during the reign of Tiberius at the hands of one of our procurators, Pontius Pilatus, and a most mischievous superstition, thus checked for the moment, again broke out not only in Judaea, the first source of the evil, but even in Rome.' This confirms: Jesus existed, was called Christ, was executed under Pilate during Tiberius' reign, and Christianity originated in Judea.",
            ["Tacitus, 'Annals' 15.44.", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' Eerdmans, pp. 39-53.", "Meier, J.P. (1991) 'A Marginal Jew.' Vol. 1."],
            "Tacitus may have been reporting what Christians themselves claimed rather than conducting independent research.",
            "Tacitus was known for meticulous research using Roman archives. He uses the Roman title 'procurator' (technically 'prefect' for Pilate's era), suggesting he consulted official records. His hostile tone ('mischievous superstition,' 'evil') rules out Christian interpolation. He had no motive to confirm Christian claims. This is a hostile witness confirming the core gospel narrative from Roman administrative records.",
            ["Luke 3:1", "Luke 23:1-25", "Acts 26:26"],
            "high", "historical_evidence"
        ),
        e(
            "Pliny the Younger's letter to Emperor Trajan (c. 112 AD) confirms early Christian worship practices and their regard for Christ as divine.",
            "Pliny, governor of Bithynia-Pontus, wrote to Trajan asking how to handle Christians. He reports: they 'were accustomed to meet on a fixed day before dawn and sing responsively a hymn to Christ as to a god, and to bind themselves by a solemn oath not to commit any wickedness... after which it was their custom to depart and to assemble again to partake of food — but food of an ordinary and innocent kind.' This confirms Christians worshipped Christ as God, met regularly, practiced ethical vows, and shared communal meals — matching NT descriptions within 80 years of Christ.",
            ["Pliny the Younger, 'Letters' 10.96.", "Wilken, R.L. (2003) 'The Christians as the Romans Saw Them.' 2nd Ed. Yale University Press."],
            "This tells us about Christian practices, not about Jesus himself.",
            "It confirms that within living memory of Christ, his followers worshipped him as God — not as a mere teacher or prophet. This is significant because the claim that Jesus' divinity was a later invention (developed over centuries) is contradicted: Christ was worshipped as God from the earliest period. Pliny's investigation found no criminal behavior, only 'excessive superstition' — consistent with Acts' portrayal of early Christians.",
            ["Acts 2:42-47", "Philippians 2:5-11", "Colossians 1:15-20", "Revelation 5:12-14"],
            "high", "historical_evidence"
        ),
        e(
            "Thallus (c. 52 AD) attempted to explain the darkness at Jesus' crucifixion as a solar eclipse — confirming the event from a hostile source.",
            "Thallus, a Samaritan-born historian, wrote a three-volume history (c. 52 AD, now lost). Julius Africanus (c. 221 AD) quotes him: 'Thallus, in the third book of his histories, explains away this darkness as an eclipse of the sun — unreasonably, as it seems to me.' Africanus notes a solar eclipse is impossible during Passover (full moon). The significance: as early as 52 AD, a non-Christian historian was trying to explain AWAY the darkness — which presupposes the darkness was widely acknowledged and needed explaining.",
            ["Julius Africanus, 'Chronography' 18.1 (preserved in George Syncellus).", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' pp. 20-23.", "Bruce, F.F. (1974) 'Jesus and Christian Origins Outside the New Testament.' Eerdmans."],
            "We only have Thallus through secondary quotation, so the original context is uncertain.",
            "Secondary quotation is common for ancient sources. The key point: within 20 years of the crucifixion, a non-Christian historian acknowledged a widespread report of darkness and felt compelled to offer a naturalistic explanation. This is a hostile witness confirming the darkness tradition — he disputes the cause, not the event. This matches Matthew 27:45, Mark 15:33, and Luke 23:44-45.",
            ["Matthew 27:45", "Mark 15:33", "Luke 23:44-45", "Amos 8:9"],
            "medium", "historical_evidence"
        ),
        e(
            "Mara bar Serapion's letter (post-73 AD) references the execution of 'the wise King' of the Jews and the subsequent destruction of Jerusalem.",
            "Mara bar Serapion, a Syrian Stoic philosopher, wrote to his son from prison: 'What advantage did the Jews gain from executing their wise King? It was just after that their kingdom was abolished... the wise King... lived on in the teaching which he had given.' He parallels Jesus with Socrates and Pythagoras as wise men unjustly killed. The letter, preserved in a 7th-century Syriac manuscript at the British Library, dates to after 73 AD (references the fall of Jerusalem) and provides independent attestation to Jesus' execution, wisdom, and ongoing influence.",
            ["British Library, Add. MS 14658.", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' pp. 53-58.", "Bruce, F.F. (1974) 'Jesus and Christian Origins Outside the New Testament.'"],
            "The letter does not name Jesus. Some argue 'the wise King' could refer to someone else. The letter is from a Stoic, not a Christian, and reflects Stoic rather than Christian theology.",
            "The Stoic context is precisely what makes it valuable: this is not a Christian source but an independent observer. The identification with Jesus is clear from context: which Jewish 'wise King' was executed, whose kingdom was subsequently destroyed, and whose teachings persisted? No other historical figure fits. The non-Christian perspective provides independent confirmation of Jesus' historicity and impact.",
            ["Matthew 2:2", "John 18:36-37", "Luke 23:38"],
            "medium", "historical_evidence"
        ),
        e(
            "Lucian of Samosata (c. 170 AD) mocked Christians for worshipping 'the crucified sophist,' confirming early Christian beliefs from a hostile source.",
            "Lucian, a Greek satirist, wrote in 'The Death of Peregrinus': 'The Christians, you know, worship a man to this day — the distinguished personage who introduced their novel rites, and was crucified on that account... these misguided creatures start with the general conviction that they are immortal for all time, which explains their contempt of death.' Lucian also noted Christians' 'lawgiver' convinced them 'they are all brothers' and they showed remarkable generosity to imprisoned members.",
            ["Lucian of Samosata, 'The Death of Peregrinus' 11-13.", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' pp. 58-64."],
            "Lucian is satirizing rather than reporting historical facts. His information may come from Christian contacts rather than independent sources.",
            "Satire requires a basis in recognizable reality — Lucian's audience must have known these facts about Christians for the satire to work. He confirms: Christians worshipped a crucified man as divine, believed in immortality, practiced brotherhood and generosity, and were willing to die for their beliefs. His hostile tone and mocking purpose rule out Christian interpolation. Even hostile witnesses confirm the core Christian narrative.",
            ["1 Corinthians 1:23", "Acts 2:44-45", "Acts 4:32-35"],
            "high", "historical_evidence"
        ),
        e(
            "The Talmud (Sanhedrin 43a) confirms Jesus' execution and acknowledges his followers, from a Jewish hostile source.",
            "The Babylonian Talmud (Sanhedrin 43a) states: 'On the eve of Passover, Yeshu was hanged. For forty days before the execution, a herald went forth and cried, \"He is going forth to be stoned because he has practiced sorcery and enticed Israel to apostasy.\"' The passage attributes Jesus' miracles to sorcery (rather than denying them) and confirms his execution at Passover time. This matches the Gospels' claim that Jewish leaders attributed Jesus' miracles to demonic power (Matthew 12:24).",
            ["Babylonian Talmud, Sanhedrin 43a.", "Herford, R.T. (1903) 'Christianity in Talmud and Midrash.' Williams & Norgate.", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' pp. 104-122."],
            "The Talmud was compiled centuries later (5th-6th century) and may reflect polemical invention rather than historical memory. Some scholars debate whether 'Yeshu' refers to Jesus of Nazareth.",
            "While compiled later, Talmudic traditions preserve earlier oral material. The passage's hostility (sorcery, apostasy) makes Christian invention impossible. Attributing Jesus' miracles to sorcery rather than denying them is significant — it confirms that even opponents acknowledged Jesus performed extraordinary acts. This matches exactly the pattern in the Gospels where opponents do not deny the miracles but attribute them to Satan.",
            ["Matthew 12:24", "Mark 3:22", "John 11:47-48", "Acts 2:22"],
            "medium", "historical_evidence"
        ),
        e(
            "Suetonius records Claudius expelling Jews from Rome due to disturbances over 'Chrestus,' confirming Acts 18:2.",
            "Roman historian Suetonius wrote (c. 121 AD) in 'Life of Claudius' 25.4: 'Since the Jews constantly made disturbances at the instigation of Chrestus, he expelled them from Rome.' Most scholars identify 'Chrestus' as a common Latin misspelling of 'Christus' (Christ). The expulsion is independently confirmed in Acts 18:2: 'He [Paul] found a Jew named Aquila, a native of Pontus, recently come from Italy with his wife Priscilla, because Claudius had commanded all Jews to leave Rome.' This dates to approximately 49 AD.",
            ["Suetonius, 'Life of Claudius' 25.4.", "Orosius, 'History Against the Pagans' 7.6.15 (dates the expulsion).", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' pp. 29-39."],
            "'Chrestus' may refer to a different person. The disturbances may not be related to Christianity.",
            "'Chrestus' was a common misspelling of 'Christus' — attested in other Latin texts. No other figure named 'Chrestus' is known from this period in Rome's Jewish community. The disturbances are consistent with the pattern seen in Acts: whenever the gospel was preached in Jewish synagogues, it caused division and sometimes riots. This is a Roman historian independently confirming a specific detail in Acts.",
            ["Acts 18:1-2", "Acts 17:5-8", "Acts 19:23-41"],
            "high", "historical_evidence"
        ),
        e(
            "Celsus (c. 175 AD), preserved in Origen's 'Contra Celsum,' provides hostile attestation to Jesus' miracles, virgin birth claim, and crucifixion.",
            "Celsus wrote 'The True Word' (c. 175 AD), the most comprehensive early attack on Christianity. Though the original is lost, Origen preserves extensive quotations (c. 248 AD). Celsus claimed Jesus was the illegitimate son of a soldier named 'Panthera,' learned sorcery in Egypt, and performed miracles by magical arts. He acknowledged Jesus' crucifixion and mocked the resurrection. The significance: Celsus does NOT deny Jesus' existence, miraculous acts, or crucifixion — he offers alternative explanations.",
            ["Origen, 'Contra Celsum.' (preserved in multiple manuscripts).", "Hoffmann, R.J. (1987) 'Celsus: On the True Doctrine.' Oxford University Press.", "Van Voorst, R.E. (2000) 'Jesus Outside the New Testament.' pp. 64-68."],
            "Celsus wrote 140+ years after Jesus and likely drew on Jewish polemical traditions rather than independent sources.",
            "Even late hostile sources confirm what they do NOT dispute: Jesus' historical existence, the claim of virgin birth (he offers an alternative, not a denial), his extraordinary acts (attributed to sorcery, not denied), and his crucifixion. A critic writing 140 years later had every reason to deny Jesus' existence if it were deniable — he did not. The pattern of attributing miracles to sorcery (not denying them) matches Talmudic and Gospel sources.",
            ["Matthew 12:24", "John 10:20-21", "Acts 26:24-26"],
            "medium", "historical_evidence"
        ),
        e(
            "The Dead Sea Scrolls demonstrate 95%+ word-for-word transmission accuracy of the Hebrew Bible over 1,000 years.",
            "Before 1947, the oldest Hebrew Bible manuscripts dated to ~900 AD (Masoretic Text). The Dead Sea Scrolls (discovered 1947-1956, dated 250 BC - 68 AD) pushed the manuscript evidence back over 1,000 years. The Great Isaiah Scroll (1QIsa-a) is 95% word-for-word identical to the Masoretic Text of Isaiah. The 5% differences are primarily spelling variations and obvious scribal slips. No doctrinal or substantive differences exist. Every book of the Hebrew Bible except Esther is represented among the scrolls.",
            ["Cross, F.M. (1958) 'The Ancient Library of Qumran.' Doubleday.", "Tov, E. (2001) 'Textual Criticism of the Hebrew Bible.' 2nd Ed. Fortress Press.", "VanderKam, J. & Flint, P. (2002) 'The Meaning of the Dead Sea Scrolls.' HarperSanFrancisco."],
            "The 5% variation shows the text was not perfectly transmitted. Some scrolls show textual traditions different from the Masoretic Text (e.g., 4QSam-a closer to LXX).",
            "95%+ identity over 1,000 years of hand-copying is extraordinary by any ancient standard. The variations are minor and scribal — no doctrine is affected. The existence of multiple textual traditions (proto-Masoretic, proto-Septuagint, proto-Samaritan) actually aids textual criticism by providing multiple witnesses. The Dead Sea Scrolls dramatically confirmed the reliability of biblical transmission.",
            ["Isaiah 40:8", "Psalm 12:6-7", "Matthew 5:18", "1 Peter 1:24-25"],
            "high", "historical_evidence"
        ),
        e(
            "The manuscript evidence for the New Testament dwarfs all other ancient texts combined.",
            "Comparison of manuscript attestation: New Testament: ~5,900 Greek MSS, 10,000 Latin, 9,300+ other languages = 25,000+ total. Earliest fragment: ~125 AD (P52). Gap from original: 25-50 years. Homer's Iliad: ~1,800 MSS. Gap: ~500 years. Herodotus: ~75 MSS. Gap: ~1,350 years. Plato: ~210 MSS. Gap: ~1,200 years. Caesar's Gallic Wars: ~10 MSS. Gap: ~1,000 years. Tacitus' Histories: ~2 MSS. Gap: ~800 years. If we reject the NT text as unreliable, we must reject ALL ancient literature.",
            ["Metzger, B.M. & Ehrman, B.D. (2005) 'The Text of the New Testament.' 4th Ed. Oxford University Press.", "Wallace, D.B. (2006) 'The Reliability of the New Testament Manuscripts.' in Understanding Scripture, ed. Grudem et al."],
            "Quantity does not equal quality. The NT manuscripts contain ~400,000 textual variants.",
            "More manuscripts = more variants mathematically, but also more ability to reconstruct the original. The vast majority of variants are trivial (spelling, word order). Only ~1% affect meaning, and none affect any Christian doctrine. Bart Ehrman (skeptic) admits the essential text is 99.5% secure. The NT is by far the best-attested ancient text — applying the same standards used for all other ancient documents, its textual integrity is unparalleled.",
            ["Isaiah 40:8", "Matthew 24:35", "1 Peter 1:25", "John 10:35"],
            "high", "historical_evidence"
        ),
        e(
            "The criterion of embarrassment: Gospel details the authors would never invent strongly support their historicity.",
            "The criterion of embarrassment identifies details that would have been harmful to early Christian credibility and thus are unlikely inventions: (1) Women as first resurrection witnesses — in 1st-century Jewish culture, women's testimony was not accepted in court. (2) Peter's repeated failures and denial of Christ. (3) Disciples' cowardice, fleeing at the arrest (Mark 14:50). (4) Jesus' cry of dereliction: 'My God, why have you forsaken me?' (5) Jesus' family thinking he was 'out of his mind' (Mark 3:21). (6) Jesus' inability to perform miracles in Nazareth (Mark 6:5). These embarrassing details are best explained as historically authentic.",
            ["Meier, J.P. (1991) 'A Marginal Jew.' Doubleday.", "Bauckham, R. (2006) 'Jesus and the Eyewitnesses.' Eerdmans.", "Ehrman, B.D. (2012) 'Did Jesus Exist?' HarperOne."],
            "Authors may include embarrassing details for literary or theological purposes. The criterion has been criticized as subjective.",
            "The cumulative effect is the key: the Gospels systematically portray the founders of the movement in an unflattering light. No propagandist would invent women as first witnesses in a patriarchal culture, portray the chief apostle as a coward and denier, or record Jesus' family opposition. Theological purposes do not explain the QUANTITY and CONSISTENCY of embarrassing details. These details are markers of authentic eyewitness memory.",
            ["Mark 14:50", "Mark 16:1-8", "Luke 24:10-11", "John 20:24-29"],
            "high", "historical_evidence"
        ),
        e(
            "300+ Old Testament prophecies were fulfilled in the life, death, and resurrection of Jesus Christ.",
            "Jesus fulfilled over 300 specific prophecies from the Old Testament, written 400-1,500 years before his birth. Key examples: (1) Born of a virgin (Isaiah 7:14). (2) Born in Bethlehem (Micah 5:2). (3) Of the tribe of Judah (Genesis 49:10). (4) Of David's line (2 Samuel 7:12-16). (5) Ministry in Galilee (Isaiah 9:1-2). (6) Entered Jerusalem on a donkey (Zechariah 9:9). (7) Betrayed for 30 silver pieces (Zechariah 11:12-13). (8) Silent before accusers (Isaiah 53:7). (9) Pierced hands and feet (Psalm 22:16). (10) Crucified with criminals (Isaiah 53:12). (11) Garments divided by lot (Psalm 22:18). (12) No bones broken (Psalm 34:20). (13) Buried in a rich man's tomb (Isaiah 53:9). (14) Rose from the dead (Psalm 16:10). (15) Daniel's 70 weeks timeline (Daniel 9:24-26) predicted the exact year of Messiah's arrival.",
            ["McDowell, J. (1999) 'The New Evidence That Demands a Verdict.' Thomas Nelson.", "Stoner, P.W. (1958) 'Science Speaks.' Moody Press.", "Fruchtenbaum, A.G. (1998) 'Messianic Christology.' Ariel Ministries."],
            "Christians selectively interpret OT passages as messianic. Some prophecies have dual meanings. Jesus or the Gospel writers may have shaped events to match prophecies.",
            "The Dead Sea Scrolls confirm these prophecies predate Jesus. Many prophecies were beyond human control: birthplace, tribe, manner of death (crucifixion — described in Psalm 22, written ~1000 BC, centuries before crucifixion existed), precise betrayal price, exact timing (Daniel 9). The combined probability of fulfilling even 8 prophecies by chance is 1 in 10^17 (Stoner). For 48, it becomes 1 in 10^157. The mathematical impossibility of chance fulfillment points to divine orchestration.",
            ["Isaiah 53:1-12", "Psalm 22:1-31", "Daniel 9:24-27", "Micah 5:2", "Zechariah 9:9", "Zechariah 11:12-13"],
            "high", "historical_evidence"
        ),
        e(
            "Archaeological confirmations of biblical sites and persons continue to accumulate, vindicating the biblical record.",
            "Recent archaeological confirmations: (1) Pool of Siloam discovered 2004 (John 9:7). (2) Pilate inscription at Caesarea Maritima, 1961. (3) Caiaphas ossuary, 1990. (4) House of David inscription (Tel Dan Stele), 1993. (5) James Ossuary ('James, son of Joseph, brother of Jesus'), 2002 — acquitted of forgery charges in 2012. (6) Seal of Hezekiah, 2015 (2 Kings 18-20). (7) Seal of Isaiah (possible), 2018. (8) Church of the Holy Sepulchre original surface confirmed by optically stimulated luminescence dating, 2017, consistent with Constantine's 4th-century identification of the site. (9) Nazareth house from Jesus' era discovered 2009.",
            ["Shanks, H. ed. 'Biblical Archaeology Review' (various issues).", "Kitchen, K.A. (2003) 'On the Reliability of the Old Testament.' Eerdmans.", "Mykytiuk, L.J. (2004) 'Identifying Biblical Persons in Northwest Semitic Inscriptions.' SBL."],
            "Some identifications are disputed (James Ossuary, Isaiah seal). Archaeology confirms places existed, not that specific events occurred there.",
            "The trend is consistently toward confirmation. Critics who denied the existence of David, Pilate, the Pool of Siloam, and Nazareth as a settlement in Jesus' time were all proven wrong. The James Ossuary was ACQUITTED of forgery charges after extensive investigation. Even confirming that places and persons existed strengthens the historical reliability of the biblical texts that mention them. The Bible is treated as guilty until proven innocent — yet it keeps being proven accurate.",
            ["Luke 3:1-2", "John 19:19-22", "Acts 26:26", "2 Peter 1:16"],
            "high", "historical_evidence"
        ),
    ]


def main_chirho():
    """Compile expanded evidence corpus and append to JSONL output."""
    row_id_chirho = log_start_chirho(
        "Compiling expanded evidence corpus: geology, biology, radiometric, cosmological, human origins, intelligent design, historical evidence"
    )

    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)

    all_entries_chirho = []
    categories_count_chirho = {}

    builders_chirho = {
        "geology": build_geology_chirho,
        "biology": build_biology_chirho,
        "radiometric": build_radiometric_chirho,
        "cosmological": build_cosmological_chirho,
        "human_origins": build_human_origins_chirho,
        "intelligent_design": build_intelligent_design_chirho,
        "historical_evidence": build_historical_expanded_chirho,
    }

    for cat_chirho, builder_chirho in builders_chirho.items():
        entries_chirho = builder_chirho()
        categories_count_chirho[cat_chirho] = len(entries_chirho)
        all_entries_chirho.extend(entries_chirho)
        print(f"  {cat_chirho}: {len(entries_chirho)} entries")

    # Count existing entries if file exists
    existing_count_chirho = 0
    if OUTPUT_FILE_CHIRHO.exists():
        with open(OUTPUT_FILE_CHIRHO, "r", encoding="utf-8") as f_chirho:
            existing_count_chirho = sum(1 for line_chirho in f_chirho if line_chirho.strip())
        print(f"\nExisting entries in output file: {existing_count_chirho}")

    # Append new entries
    with open(OUTPUT_FILE_CHIRHO, "a", encoding="utf-8") as f_chirho:
        for entry_chirho in all_entries_chirho:
            f_chirho.write(json.dumps(entry_chirho, ensure_ascii=False) + "\n")

    new_count_chirho = len(all_entries_chirho)
    total_chirho = existing_count_chirho + new_count_chirho

    print(f"\n=== EVIDENCE EXPANSION SUMMARY ===")
    print(f"New entries added: {new_count_chirho}")
    print(f"Previously existing: {existing_count_chirho}")
    print(f"Total entries in file: {total_chirho}")
    print(f"\nBreakdown by category (new entries):")
    for cat_chirho, count_chirho in sorted(categories_count_chirho.items()):
        print(f"  {cat_chirho}: {count_chirho}")
    print(f"\nOutput: {OUTPUT_FILE_CHIRHO}")

    log_end_chirho(
        row_id_chirho,
        f"Added {new_count_chirho} new evidence entries across {len(builders_chirho)} categories. Total file now has {total_chirho} entries.",
        f"Expansion successful. Categories: {categories_count_chirho}. Appended to existing file without replacing prior entries."
    )


if __name__ == "__main__":
    main_chirho()
