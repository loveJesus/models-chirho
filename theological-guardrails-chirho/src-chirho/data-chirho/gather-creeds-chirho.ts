// For God so loved the world that he gave his only begotten Son,
// that whoever believes in him should not perish but have eternal life. - John 3:16

/**
 * gather-creeds-chirho.ts
 * Collects historical creed texts from public domain sources.
 * Outputs structured JSON to data-chirho/raw-chirho/creeds-chirho.json
 */

import { writeFile, mkdir } from "fs/promises";

const OUTPUT_DIR_CHIRHO = `${process.cwd()}/data-chirho/raw-chirho/`;

interface CreedChirho {
  nameChirho: string;
  yearChirho: number;
  councilChirho: string | null;
  textChirho: string;
  sourceChirho: string;
  keyDoctrinesChirho: string[];
}

// Historical creeds - public domain texts
const CREEDS_CHIRHO: CreedChirho[] = [
  {
    nameChirho: "Nicene Creed (325 AD, expanded 381 AD)",
    yearChirho: 325,
    councilChirho: "Nicaea I / Constantinople I",
    sourceChirho: "Public domain - ecumenical councils",
    keyDoctrinesChirho: [
      "Christ is God",
      "consubstantial with the Father",
      "begotten not made",
      "Holy Spirit proceeds from the Father",
      "one holy catholic and apostolic Church",
    ],
    textChirho: `We believe in one God, the Father Almighty, Maker of heaven and earth, and of all things visible and invisible.

And in one Lord Jesus Christ, the only-begotten Son of God, begotten of the Father before all worlds; God of God, Light of Light, very God of very God; begotten, not made, being of one substance with the Father, by whom all things were made.

Who, for us and for our salvation, came down from heaven, and was incarnate by the Holy Spirit of the virgin Mary, and was made man; and was crucified also for us under Pontius Pilate; He suffered and was buried; and the third day He rose again, according to the Scriptures; and ascended into heaven, and sits on the right hand of the Father; and He shall come again, with glory, to judge the living and the dead; whose kingdom shall have no end.

And we believe in the Holy Spirit, the Lord and Giver of Life; who proceeds from the Father; who with the Father and the Son together is worshipped and glorified; who spoke by the prophets.

And we believe in one holy catholic and apostolic Church. We acknowledge one baptism for the remission of sins; and we look for the resurrection of the dead, and the life of the world to come. Amen.`,
  },
  {
    nameChirho: "Apostles' Creed",
    yearChirho: 180,
    councilChirho: null,
    sourceChirho: "Public domain - early church tradition",
    keyDoctrinesChirho: [
      "God the Father Almighty",
      "Jesus Christ His only Son",
      "conceived by the Holy Spirit",
      "born of the Virgin Mary",
      "rose from the dead",
      "holy catholic Church",
      "communion of saints",
      "resurrection of the body",
    ],
    textChirho: `I believe in God, the Father almighty, creator of heaven and earth.

I believe in Jesus Christ, his only Son, our Lord, who was conceived by the Holy Spirit, born of the Virgin Mary, suffered under Pontius Pilate, was crucified, died, and was buried; he descended to the dead. On the third day he rose again; he ascended into heaven, he is seated at the right hand of the Father, and he will come to judge the living and the dead.

I believe in the Holy Spirit, the holy catholic Church, the communion of saints, the forgiveness of sins, the resurrection of the body, and the life everlasting. Amen.`,
  },
  {
    nameChirho: "Chalcedonian Definition (451 AD)",
    yearChirho: 451,
    councilChirho: "Chalcedon",
    sourceChirho: "Public domain - Council of Chalcedon",
    keyDoctrinesChirho: [
      "two natures",
      "without confusion",
      "without change",
      "without division",
      "without separation",
      "truly God and truly man",
      "consubstantial with the Father as regards divinity",
      "consubstantial with us as regards humanity",
    ],
    textChirho: `Following, then, the holy Fathers, we all unanimously teach that our Lord Jesus Christ is to us one and the same Son, the self-same perfect in Godhead, the self-same perfect in manhood; truly God and truly man; the self-same of a rational soul and body; consubstantial with the Father according to the Godhead, the self-same consubstantial with us according to the manhood; like us in all things, sin apart; before the ages begotten of the Father as to the Godhead, but in the last days, the self-same, for us and for our salvation born of Mary the Virgin Theotokos as to the manhood;

One and the same Christ, Son, Lord, Only-begotten; acknowledged in two natures without confusion, without change, without division, without separation; the difference of the natures being in no way removed because of the union, but rather the properties of each nature being preserved, and both concurring into one Person and one Subsistence — not parted or divided into two persons, but one and the same Son and Only-begotten God, Word, Lord, Jesus Christ; even as from the beginning the prophets have taught concerning him, and as the Lord Jesus Christ himself has taught us, and as the Symbol of the Fathers has handed down to us.`,
  },
  {
    nameChirho: "Athanasian Creed (Quicunque Vult)",
    yearChirho: 500,
    councilChirho: null,
    sourceChirho: "Public domain - attributed tradition",
    keyDoctrinesChirho: [
      "Trinity",
      "three persons one God",
      "coeternal",
      "coequal",
      "incarnation",
      "two natures one person",
    ],
    textChirho: `Whosoever will be saved, before all things it is necessary that he hold the catholic faith; which faith except every one do keep whole and undefiled, without doubt he shall perish everlastingly.

And the catholic faith is this: That we worship one God in Trinity, and Trinity in Unity; neither confounding the persons nor dividing the substance. For there is one person of the Father, another of the Son, and another of the Holy Spirit. But the Godhead of the Father, of the Son, and of the Holy Spirit is all one, the glory equal, the majesty coeternal.

Such as the Father is, such is the Son, and such is the Holy Spirit. The Father uncreated, the Son uncreated, and the Holy Spirit uncreated. The Father incomprehensible, the Son incomprehensible, and the Holy Spirit incomprehensible. The Father eternal, the Son eternal, and the Holy Spirit eternal. And yet they are not three eternals but one eternal. As also there are not three uncreated nor three incomprehensible, but one uncreated and one incomprehensible.

So likewise the Father is almighty, the Son almighty, and the Holy Spirit almighty. And yet they are not three almighties, but one almighty. So the Father is God, the Son is God, and the Holy Spirit is God; and yet they are not three Gods, but one God. So likewise the Father is Lord, the Son Lord, and the Holy Spirit Lord; and yet they are not three Lords but one Lord.

For like as we are compelled by the Christian verity to acknowledge every Person by himself to be God and Lord; so are we forbidden by the catholic religion to say; There are three Gods or three Lords.

The Father is made of none, neither created nor begotten. The Son is of the Father alone; not made nor created, but begotten. The Holy Spirit is of the Father and of the Son; neither made, nor created, nor begotten, but proceeding.

So there is one Father, not three Fathers; one Son, not three Sons; one Holy Spirit, not three Holy Spirits. And in this Trinity none is afore or after another; none is greater or less than another. But the whole three persons are coeternal, and coequal. So that in all things, as aforesaid, the Unity in Trinity and the Trinity in Unity is to be worshipped.

He therefore that will be saved must thus think of the Trinity.

Furthermore it is necessary to everlasting salvation that he also believe rightly the incarnation of our Lord Jesus Christ. For the right faith is that we believe and confess that our Lord Jesus Christ, the Son of God, is God and man. God of the substance of the Father, begotten before the worlds; and man of substance of his mother, born in the world. Perfect God and perfect man, of a reasonable soul and human flesh subsisting. Equal to the Father as touching his Godhead, and inferior to the Father as touching his manhood. Who, although he is God and man, yet he is not two, but one Christ. One, not by conversion of the Godhead into flesh, but by taking of that manhood into God. One altogether, not by confusion of substance, but by unity of person. For as the reasonable soul and flesh is one man, so God and man is one Christ;

Who suffered for our salvation, descended into hell, rose again the third day from the dead; he ascended into heaven, he sits on the right hand of the Father, God, Almighty; from thence he shall come to judge the living and the dead. At whose coming all men shall rise again with their bodies; and shall give account of their own works. And they that have done good shall go into life everlasting and they that have done evil into everlasting fire. This is the catholic faith, which except a man believe faithfully he cannot be saved.`,
  },
  {
    nameChirho: "Definition of Constantinople III (681 AD)",
    yearChirho: 681,
    councilChirho: "Constantinople III",
    sourceChirho: "Public domain - Sixth Ecumenical Council",
    keyDoctrinesChirho: [
      "two wills in Christ",
      "divine will and human will",
      "human will follows divine will",
      "contra Monothelitism",
    ],
    textChirho: `We also proclaim two natural wills in him, and two natural operations, without division, without change, without separation, without confusion, according to the teaching of the holy Fathers — and two natural wills not contrary to each other, God forbid, as the impious heretics assert, but his human will following, and not resisting or reluctant, but rather subject to, his divine and omnipotent will.

For it was proper for the will of the flesh to be moved, but to be subject to the divine will, according to the most wise Athanasius. For as his flesh is called and is the flesh of God the Word, so also the natural will of his flesh is called and is the proper will of God the Word, as he himself says: "I came down from heaven, not to do my own will, but the will of the Father who sent me," where he calls his own will the will of the flesh, since the flesh also became his own.

For as his most holy and immaculate animated flesh was not destroyed because it was deified but continued in its own state and sphere, so also his human will, although deified, was not suppressed, but was rather preserved.`,
  },
  {
    nameChirho: "Definition of Constantinople II (553 AD)",
    yearChirho: 553,
    councilChirho: "Constantinople II",
    sourceChirho: "Public domain - Fifth Ecumenical Council",
    keyDoctrinesChirho: [
      "condemns Three Chapters",
      "reinforces Chalcedon",
      "condemns Nestorianism",
      "condemns Origenism",
      "one Christ in two natures",
    ],
    textChirho: `If anyone does not confess that the Father and the Son and the Holy Spirit are one nature or essence, one power or authority, a consubstantial Trinity to be adored, one Godhead in three persons or hypostases, let him be anathema. For there is one God and Father, from whom are all things, and one Lord Jesus Christ, through whom are all things, and one Holy Spirit, in whom are all things.

If anyone does not confess that God the Word was twice begotten, the first before all time from the Father, non-temporal and bodiless, the other in the last days when he came down from the heavens and was incarnate by the holy, glorious Theotokos and ever-virgin Mary, and born of her, let him be anathema.

If anyone says that the wonder-working God the Word is one and Christ who suffered is another, or says that God the Word was together with the Christ who came from woman, or was in him as one in another, but not that there is one and the same our Lord Jesus Christ, the Word of God, who was incarnate and became man, and that the miracles and the sufferings which he voluntarily endured in flesh belong to the same person, let him be anathema.`,
  },
];

// Additional confessional texts for broader orthodox coverage
const CONFESSIONAL_TEXTS_CHIRHO: CreedChirho[] = [
  {
    nameChirho: "Westminster Shorter Catechism (Selected Questions)",
    yearChirho: 1647,
    councilChirho: null,
    sourceChirho: "Public domain - Westminster Assembly",
    keyDoctrinesChirho: [
      "chief end of man",
      "Trinity",
      "decrees of God",
      "creation",
      "providence",
      "covenant of works",
      "covenant of grace",
    ],
    textChirho: `Q. 1. What is the chief end of man?
A. Man's chief end is to glorify God, and to enjoy him forever.

Q. 4. What is God?
A. God is a Spirit, infinite, eternal, and unchangeable, in his being, wisdom, power, holiness, justice, goodness, and truth.

Q. 6. How many persons are there in the Godhead?
A. There are three persons in the Godhead: the Father, the Son, and the Holy Ghost; and these three are one God, the same in substance, equal in power and glory.

Q. 21. Who is the Redeemer of God's elect?
A. The only Redeemer of God's elect is the Lord Jesus Christ, who, being the eternal Son of God, became man, and so was, and continueth to be, God and man in two distinct natures, and one person, forever.

Q. 22. How did Christ, being the Son of God, become man?
A. Christ, the Son of God, became man, by taking to himself a true body, and a reasonable soul, being conceived by the power of the Holy Ghost, in the womb of the virgin Mary, and born of her, yet without sin.`,
  },
  {
    nameChirho: "Heidelberg Catechism (Selected Questions)",
    yearChirho: 1563,
    councilChirho: null,
    sourceChirho: "Public domain - Reformed tradition",
    keyDoctrinesChirho: [
      "only comfort",
      "Trinity",
      "true God and true man",
      "mediator",
    ],
    textChirho: `Q. 1. What is your only comfort in life and death?
A. That I, with body and soul, both in life and death, am not my own, but belong unto my faithful Savior Jesus Christ; who with his precious blood has fully satisfied for all my sins, and delivered me from all the power of the devil; and so preserves me that without the will of my heavenly Father not a hair can fall from my head; yea, that all things must be subservient to my salvation, wherefore by his Holy Spirit he also assures me of eternal life, and makes me heartily willing and ready, henceforth, to live unto him.

Q. 25. Since there is but one divine Being, why do you speak of three: Father, Son, and Holy Spirit?
A. Because God has so revealed himself in his Word, that these three distinct persons are the one, true, eternal God.

Q. 35. What is the meaning of "conceived by the Holy Spirit, born of the Virgin Mary"?
A. That the eternal Son of God, who is and continues true and eternal God, took upon him the very nature of man, of the flesh and blood of the Virgin Mary, by the operation of the Holy Spirit; so that he might also be the true seed of David, like unto his brethren in all things, sin excepted.`,
  },
];

async function mainChirho(): Promise<void> {
  console.log("📜 Gathering creed texts...\n");

  await mkdir(OUTPUT_DIR_CHIRHO, { recursive: true });

  const allCreedsChirho = [...CREEDS_CHIRHO, ...CONFESSIONAL_TEXTS_CHIRHO];

  const outputChirho = {
    metadataChirho: {
      generatedAtChirho: new Date().toISOString(),
      countChirho: allCreedsChirho.length,
      descriptionChirho:
        "Historical creeds and confessional texts for theological guardrails training",
    },
    creedsChirho: allCreedsChirho,
  };

  const outputPathChirho = `${OUTPUT_DIR_CHIRHO}creeds-chirho.json`;
  await writeFile(outputPathChirho, JSON.stringify(outputChirho, null, 2), "utf-8");

  console.log(`✅ Written ${allCreedsChirho.length} creed texts to ${outputPathChirho}`);

  // Also output a summary
  for (const creedChirho of allCreedsChirho) {
    console.log(
      `  - ${creedChirho.nameChirho} (${creedChirho.yearChirho} AD) - ${creedChirho.keyDoctrinesChirho.length} key doctrines`
    );
  }
}

mainChirho();
