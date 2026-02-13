// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * gather-heresies-chirho.ts
 * Collects documented heresy descriptions from historical/academic sources.
 * These are public domain descriptions of historical theological positions
 * condemned by the first six ecumenical councils.
 */

import { writeFile, mkdir } from "fs/promises";

const OUTPUT_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;

interface HeresyChirho {
  nameChirho: string;
  labelChirho: string;
  founderChirho: string | null;
  centuryChirho: number;
  condemnedByChirho: string;
  domainChirho: string;
  coreClaimsChirho: string[];
  orthodoxResponseChirho: string;
  keyScriptureChirho: string[];
  exampleStatementsChirho: string[];
}

const HERESIES_CHIRHO: HeresyChirho[] = [
  {
    nameChirho: "Arianism",
    labelChirho: "arianism_chirho",
    founderChirho: "Arius of Alexandria",
    centuryChirho: 4,
    condemnedByChirho: "Council of Nicaea (325 AD)",
    domainChirho: "christology",
    coreClaimsChirho: [
      "The Son is a created being, the first and greatest of God's creations",
      "There was a time when the Son was not",
      "The Son is of a different substance (heteroousios) than the Father",
      "The Son is subordinate to the Father in nature and being",
      "The Son is a lesser, derived god",
    ],
    orthodoxResponseChirho:
      "The Nicene Creed declares Christ 'begotten, not made, of one Being (homoousios) with the Father.' John 1:1 states the Word was God. Colossians 1:15-17 and Hebrews 1:3 affirm Christ's full divinity.",
    keyScriptureChirho: [
      "John 1:1",
      "John 1:14",
      "John 10:30",
      "Colossians 1:15-17",
      "Hebrews 1:3",
      "Philippians 2:6",
    ],
    exampleStatementsChirho: [
      "Jesus is a created being, the first and greatest of God's creations.",
      "There was a time before the Son existed.",
      "Jesus is divine but not equal to God the Father in essence.",
      "The Son of God is a lesser deity, not truly God.",
      "Christ was made by God as the greatest angel.",
      "Jesus is godlike but not the same substance as the Father.",
    ],
  },
  {
    nameChirho: "Pelagianism",
    labelChirho: "pelagianism_chirho",
    founderChirho: "Pelagius",
    centuryChirho: 5,
    condemnedByChirho: "Council of Ephesus (431 AD)",
    domainChirho: "soteriology",
    coreClaimsChirho: [
      "Humans are born morally neutral, without original sin",
      "Adam's sin affected only Adam, not the human race",
      "Humans can achieve salvation through their own moral effort",
      "Grace is helpful but not necessary for salvation",
      "Free will alone is sufficient to obey God perfectly",
    ],
    orthodoxResponseChirho:
      "Scripture teaches that all have sinned (Romans 3:23), that humans are dead in sin (Ephesians 2:1-5), and that salvation is by grace through faith, not works (Ephesians 2:8-9). Original sin is attested in Romans 5:12-19.",
    keyScriptureChirho: [
      "Romans 3:23",
      "Romans 5:12-19",
      "Ephesians 2:1-5",
      "Ephesians 2:8-9",
      "Psalm 51:5",
      "John 15:5",
    ],
    exampleStatementsChirho: [
      "Humans are born morally perfect and only sin by choice.",
      "Adam's fall did not affect human nature at all.",
      "We can earn our salvation through our own good works.",
      "God's grace is a nice bonus but we don't actually need it to be saved.",
      "Original sin is a myth; babies are born pure.",
      "Through willpower alone, a person can live a sinless life.",
    ],
  },
  {
    nameChirho: "Gnosticism",
    labelChirho: "gnosticism_chirho",
    founderChirho: null,
    centuryChirho: 2,
    condemnedByChirho: "Early church fathers, multiple councils",
    domainChirho: "theology_proper",
    coreClaimsChirho: [
      "The material world is evil, created by a lesser god (demiurge)",
      "The true God is purely spiritual and did not create the physical world",
      "Salvation comes through secret knowledge (gnosis), not faith",
      "Christ was a purely spiritual being who did not truly have a physical body",
      "The Old Testament God is the evil demiurge, not the true God",
    ],
    orthodoxResponseChirho:
      "Genesis 1:31 declares creation 'very good.' John 1:14 states the Word became flesh. 1 John 4:2-3 condemns denial of Christ coming in the flesh. Salvation is by grace through faith (Ephesians 2:8-9), not secret knowledge.",
    keyScriptureChirho: [
      "Genesis 1:31",
      "John 1:14",
      "1 John 4:2-3",
      "Colossians 2:9",
      "1 Timothy 2:5",
      "Ephesians 2:8-9",
    ],
    exampleStatementsChirho: [
      "The physical world is inherently evil and was created by a lesser deity.",
      "The God of the Old Testament is actually an evil demiurge.",
      "True salvation comes only through secret spiritual knowledge.",
      "Jesus never had a real physical body; it was only an illusion.",
      "Matter is evil; only the spiritual realm is good.",
      "The creator God and the true God are different beings.",
    ],
  },
  {
    nameChirho: "Modalism (Sabellianism)",
    labelChirho: "modalism_chirho",
    founderChirho: "Sabellius",
    centuryChirho: 3,
    condemnedByChirho: "Council of Constantinople I (381 AD)",
    domainChirho: "trinity",
    coreClaimsChirho: [
      "God is one person who appears in three modes or manifestations",
      "Father, Son, and Spirit are not distinct persons but roles played by one person",
      "God was the Father in the OT, became the Son in the incarnation, and is now the Spirit",
      "There is no eternal distinction between the three persons of the Trinity",
    ],
    orthodoxResponseChirho:
      "The baptism of Jesus (Matthew 3:16-17) shows all three persons simultaneously. Jesus prays to the Father as a distinct person (John 17). The Nicene Creed confesses three persons (hypostases) in one essence (ousia).",
    keyScriptureChirho: [
      "Matthew 3:16-17",
      "Matthew 28:19",
      "John 17:1-5",
      "2 Corinthians 13:14",
      "John 14:16-17",
    ],
    exampleStatementsChirho: [
      "God is one person who wears different masks: sometimes Father, sometimes Son, sometimes Spirit.",
      "The Trinity just means God acts in three different ways at different times.",
      "Father, Son, and Holy Spirit are three names for the same person.",
      "God switched from being the Father to being Jesus and now is the Holy Spirit.",
      "There is only one divine person who manifests in three modes.",
      "Jesus and the Father are literally the same person, not just the same substance.",
    ],
  },
  {
    nameChirho: "Docetism",
    labelChirho: "docetism_chirho",
    founderChirho: null,
    centuryChirho: 1,
    condemnedByChirho: "Council of Chalcedon (451 AD)",
    domainChirho: "christology",
    coreClaimsChirho: [
      "Christ only appeared to have a physical body",
      "Christ's sufferings and death were an illusion",
      "The divine Christ could not truly suffer or die",
      "Christ's humanity was apparent, not real",
    ],
    orthodoxResponseChirho:
      "John 1:14 states 'the Word became flesh.' 1 John 4:2 warns against denying Christ came in the flesh. The Chalcedonian Definition affirms Christ is 'truly man, of a reasonable soul and body, consubstantial with us according to the manhood.'",
    keyScriptureChirho: [
      "John 1:14",
      "1 John 4:2-3",
      "Hebrews 2:14-17",
      "Luke 24:39",
      "Colossians 2:9",
    ],
    exampleStatementsChirho: [
      "Jesus only appeared to have a physical body but was really pure spirit.",
      "Christ's death on the cross was just an illusion; God cannot die.",
      "Jesus pretended to eat and drink but didn't actually have a real body.",
      "The incarnation was an appearance, not a reality.",
      "Christ's human nature was a phantom, not genuine flesh.",
    ],
  },
  {
    nameChirho: "Nestorianism",
    labelChirho: "nestorianism_chirho",
    founderChirho: "Nestorius",
    centuryChirho: 5,
    condemnedByChirho: "Council of Ephesus (431 AD)",
    domainChirho: "christology",
    coreClaimsChirho: [
      "Christ is two separate persons: one divine and one human",
      "Mary is the mother of the human person only (Christotokos), not of God (Theotokos)",
      "The divine and human natures in Christ are so distinct they constitute two persons",
      "The union between the two natures is merely moral or relational, not personal",
    ],
    orthodoxResponseChirho:
      "The Council of Ephesus affirmed Mary as Theotokos (God-bearer) because the person born of her is the divine Son. Chalcedon clarified: two natures concur in 'one Person and one Subsistence—not parted or divided into two persons.'",
    keyScriptureChirho: [
      "Luke 1:35",
      "Luke 1:43",
      "John 1:14",
      "Galatians 4:4",
      "Colossians 2:9",
    ],
    exampleStatementsChirho: [
      "There are really two persons in Christ: a divine person and a human person.",
      "Mary is the mother of the human Jesus, not the mother of God.",
      "The divine Word merely dwelt in the man Jesus, like God dwelling in a temple.",
      "Jesus the man and God the Son are two separate individuals joined together.",
      "The human nature of Christ is a separate person from the divine nature.",
    ],
  },
  {
    nameChirho: "Marcionism",
    labelChirho: "marcionism_chirho",
    founderChirho: "Marcion of Sinope",
    centuryChirho: 2,
    condemnedByChirho: "Early church, various synods",
    domainChirho: "theology_proper",
    coreClaimsChirho: [
      "The God of the Old Testament is a different, inferior deity from the God of Jesus",
      "The Old Testament should be rejected entirely",
      "The God of the OT is wrathful and unjust; Jesus revealed the true, loving God",
      "The Jewish scriptures have no authority for Christians",
      "The material creation is the work of the evil OT God",
    ],
    orthodoxResponseChirho:
      "Jesus affirmed the OT scriptures (Matthew 5:17, Luke 24:27, 44). Paul says all Scripture is God-breathed (2 Timothy 3:16). The God who created the world is the same God who sent Christ (Acts 17:24-28).",
    keyScriptureChirho: [
      "Matthew 5:17",
      "Luke 24:27",
      "Luke 24:44",
      "2 Timothy 3:16",
      "Acts 17:24-28",
      "Hebrews 1:1-2",
    ],
    exampleStatementsChirho: [
      "The God of the Old Testament is an evil deity, not the true God.",
      "Christians should completely reject the Old Testament.",
      "The wrathful God of the Hebrews is not the loving Father Jesus spoke of.",
      "The Old Testament has no relevance or authority for Christians today.",
      "There are two gods: the cruel creator god and the good god Jesus revealed.",
    ],
  },
  {
    nameChirho: "Apollinarianism",
    labelChirho: "apollinarianism_chirho",
    founderChirho: "Apollinaris of Laodicea",
    centuryChirho: 4,
    condemnedByChirho: "Council of Constantinople I (381 AD)",
    domainChirho: "christology",
    coreClaimsChirho: [
      "Christ had a human body but not a human mind/soul",
      "The divine Logos replaced the human rational soul in Christ",
      "Christ was not fully human because he lacked a human mind",
      "A true union of divine and human requires the divine to replace part of the human",
    ],
    orthodoxResponseChirho:
      "Gregory of Nazianzus argued: 'What has not been assumed has not been healed.' If Christ lacks a human mind, human minds are not redeemed. Chalcedon affirms Christ has 'a rational soul and body,' being 'truly man.'",
    keyScriptureChirho: [
      "Luke 2:52",
      "Mark 14:34",
      "Hebrews 2:17",
      "Hebrews 4:15",
      "Philippians 2:7-8",
    ],
    exampleStatementsChirho: [
      "Jesus had a human body but his mind was entirely divine, not human.",
      "The divine Word replaced the human soul in Jesus.",
      "Christ did not have a real human mind; his thoughts were purely divine.",
      "Jesus wasn't truly human in his inner life, only in his physical body.",
      "The Logos took the place of a human rational soul in Christ.",
    ],
  },
  {
    nameChirho: "Monothelitism",
    labelChirho: "monothelitism_chirho",
    founderChirho: "Sergius I of Constantinople",
    centuryChirho: 7,
    condemnedByChirho: "Council of Constantinople III (681 AD)",
    domainChirho: "christology",
    coreClaimsChirho: [
      "Christ has only one will (the divine will)",
      "Christ's human nature does not have its own will",
      "Having two wills would create internal conflict in Christ",
      "The human will was absorbed by or replaced by the divine will",
    ],
    orthodoxResponseChirho:
      "Constantinople III declared Christ has 'two natural wills...not contrary to each other' with the human will 'subject to his divine will.' Christ's prayer in Gethsemane (Luke 22:42) demonstrates two wills: 'not my will, but yours be done.'",
    keyScriptureChirho: [
      "Luke 22:42",
      "Matthew 26:39",
      "John 6:38",
      "Hebrews 5:7-8",
      "John 5:30",
    ],
    exampleStatementsChirho: [
      "Christ has only one will, the divine will.",
      "Jesus did not have a separate human will alongside his divine will.",
      "Having two wills would have meant internal conflict in Christ.",
      "Christ's human will was absorbed into his divine will.",
      "There is only one operation and one will in the incarnate Christ.",
    ],
  },
  {
    nameChirho: "Semi-Pelagianism",
    labelChirho: "semi_pelagianism_chirho",
    founderChirho: "John Cassian (attributed)",
    centuryChirho: 5,
    condemnedByChirho: "Council of Orange (529 AD)",
    domainChirho: "soteriology",
    coreClaimsChirho: [
      "Humans can make the first step toward God without grace",
      "The initial desire for salvation comes from human free will",
      "Grace is needed but humans initiate the process of salvation",
      "Faith begins with human effort, then God responds with grace",
    ],
    orthodoxResponseChirho:
      "Jesus said 'No one can come to me unless the Father draws him' (John 6:44). Philippians 1:29 says even faith is granted by God. Ephesians 2:8-9 declares salvation is 'the gift of God, not of works.' The Council of Orange affirmed prevenient grace.",
    keyScriptureChirho: [
      "John 6:44",
      "John 6:65",
      "Philippians 1:29",
      "Ephesians 2:8-9",
      "Romans 9:16",
      "2 Timothy 2:25",
    ],
    exampleStatementsChirho: [
      "Humans take the first step toward God, and then God responds with grace.",
      "The initial desire for salvation comes from our own free will, not from God.",
      "We choose God first, and then He gives us the grace we need.",
      "Faith begins as a human decision, which God then supports with grace.",
      "People can seek God on their own and God meets them halfway.",
    ],
  },
  {
    nameChirho: "Adoptionism",
    labelChirho: "adoptionism_chirho",
    founderChirho: "Theodotus of Byzantium",
    centuryChirho: 2,
    condemnedByChirho: "Multiple synods, reinforced by ecumenical councils",
    domainChirho: "christology",
    coreClaimsChirho: [
      "Jesus was born as an ordinary human who was later adopted as Son of God",
      "Jesus became divine at his baptism when the Spirit descended on him",
      "Jesus earned or was promoted to divine status through his righteousness",
      "Christ is not eternally the Son of God but was elevated to that status",
    ],
    orthodoxResponseChirho:
      "John 1:1-3 declares the Word was God 'in the beginning.' Philippians 2:6 says Christ existed 'in the form of God' before the incarnation. Hebrews 1:2-3 affirms the Son is the eternal 'heir of all things.'",
    keyScriptureChirho: [
      "John 1:1-3",
      "John 8:58",
      "Philippians 2:5-11",
      "Hebrews 1:2-3",
      "Colossians 1:17",
    ],
    exampleStatementsChirho: [
      "Jesus was a normal human being who was adopted as God's Son at his baptism.",
      "Christ earned his divine status through his perfect obedience.",
      "Jesus wasn't always the Son of God; he was promoted to that role.",
      "At Jesus' baptism, God elevated him from a mere man to divine sonship.",
      "Jesus became God's Son; he wasn't always God's Son from eternity.",
    ],
  },
  {
    nameChirho: "Patripassianism",
    labelChirho: "patripassianism_chirho",
    founderChirho: "Praxeas",
    centuryChirho: 3,
    condemnedByChirho: "Early church, connected to Modalism condemnations",
    domainChirho: "trinity",
    coreClaimsChirho: [
      "God the Father himself suffered on the cross",
      "Father and Son are the same person, so the Father was crucified",
      "There is no real distinction between the Father and the Son",
      "The Father directly experienced the suffering of the cross",
    ],
    orthodoxResponseChirho:
      "The distinction of persons means the Son suffered in his humanity while the Father did not. Jesus prayed to the Father as distinct from himself (John 17). Tertullian argued against Praxeas that the Father sent the Son (Galatians 4:4), showing personal distinction.",
    keyScriptureChirho: [
      "John 17:1-5",
      "Galatians 4:4",
      "Hebrews 5:7-8",
      "Romans 8:32",
      "Matthew 27:46",
    ],
    exampleStatementsChirho: [
      "God the Father himself was crucified on the cross.",
      "When Jesus suffered, it was the Father suffering because they are the same person.",
      "The Father directly experienced the pain of crucifixion.",
      "There is no difference between the Father and Jesus, so the Father died on the cross.",
      "It was the Father disguised as the Son who was nailed to the cross.",
    ],
  },
];

async function mainChirho(): Promise<void> {
  console.log("📜 Gathering heresy descriptions...\n");

  await mkdir(OUTPUT_DIR_CHIRHO, { recursive: true });

  const outputChirho = {
    metadataChirho: {
      generatedAtChirho: new Date().toISOString(),
      countChirho: HERESIES_CHIRHO.length,
      totalExampleStatementsChirho: HERESIES_CHIRHO.reduce(
        (accChirho, hChirho) => accChirho + hChirho.exampleStatementsChirho.length,
        0
      ),
      descriptionChirho:
        "Historical heresy descriptions with example statements for theological guardrails training",
    },
    heresiesChirho: HERESIES_CHIRHO,
  };

  const outputPathChirho = `${OUTPUT_DIR_CHIRHO}heresies-chirho.json`;
  await writeFile(outputPathChirho, JSON.stringify(outputChirho, null, 2), "utf-8");

  console.log(`✅ Written ${HERESIES_CHIRHO.length} heresy descriptions to ${outputPathChirho}`);
  console.log(
    `   Total example statements: ${outputChirho.metadataChirho.totalExampleStatementsChirho}`
  );

  for (const heresyChirho of HERESIES_CHIRHO) {
    console.log(
      `  - ${heresyChirho.nameChirho}: ${heresyChirho.exampleStatementsChirho.length} examples, domain: ${heresyChirho.domainChirho}`
    );
  }
}

mainChirho();
