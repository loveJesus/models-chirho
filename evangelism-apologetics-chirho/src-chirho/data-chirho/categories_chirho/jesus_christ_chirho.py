# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""Jesus Christ apologetics entries."""

CAT_CHIRHO = "jesus_christ"


def e_chirho(topic_chirho, question_chirho, answer_chirho, scripture_chirho, thinkers_chirho, reading_chirho):
    return {"topic_chirho": topic_chirho, "question_chirho": question_chirho, "answer_chirho": answer_chirho,
            "scripture_chirho": scripture_chirho, "key_thinkers_chirho": thinkers_chirho,
            "further_reading_chirho": reading_chirho, "category_chirho": CAT_CHIRHO}


def build_jesus_christ_chirho() -> list[dict]:
    return [
        e_chirho(
            "Historical Evidence for Jesus",
            "What evidence exists for Jesus outside the Bible?",
            "The historical existence of Jesus is attested by multiple non-Christian sources within a century of His life. Tacitus (Annals 15.44, c. AD 116) records that 'Christus' was executed under Pontius Pilate during Tiberius's reign and that a 'most mischievous superstition' broke out again after His death. Josephus (Antiquities 18.63-64, c. AD 93) mentions Jesus in the Testimonium Flavianum, and separately references 'James, the brother of Jesus who was called Christ' (Antiquities 20.200). Pliny the Younger (Letters 10.96, c. AD 112) describes Christians worshipping Christ 'as to a god.' The Babylonian Talmud (Sanhedrin 43a) records that 'Yeshu' was hanged on Passover eve.\n\nThese sources, hostile or neutral toward Christianity, confirm key facts: Jesus existed, was crucified under Pilate, was the founder of a movement that spread rapidly, and was worshipped as divine by His followers shortly after His death. As atheist historian Bart Ehrman affirms, 'The idea that Jesus did not exist is a modern notion. It has no ancient precedent.' The non-Christian evidence alone establishes Jesus as one of the most well-attested figures of the ancient world.",
            ["1 Corinthians 15:3-8", "Luke 1:1-4", "Acts 26:26", "2 Peter 1:16"],
            ["Gary Habermas", "Bart Ehrman", "F.F. Bruce", "Robert Van Voorst"],
            ["Jesus Outside the New Testament by Robert Van Voorst", "The Historical Jesus by Gary Habermas"]
        ),
        e_chirho(
            "Deity of Christ",
            "Did Jesus claim to be God?",
            "Jesus made explicit and implicit claims to deity throughout His ministry. He claimed the divine name 'I AM' (John 8:58, echoing Exodus 3:14), prompting the Jews to pick up stones for blasphemy. He claimed authority to forgive sins (Mark 2:5-7), which the scribes correctly recognized as a divine prerogative. He accepted worship (Matthew 14:33, John 20:28) — something no faithful Jew or angel would do (Acts 10:25-26, Revelation 22:8-9). He claimed to be 'one with the Father' (John 10:30) and that to see Him was to see God (John 14:9).\n\nBeyond verbal claims, Jesus acted with divine authority: He commanded nature (Mark 4:39), claimed authority over the Sabbath (Mark 2:28), declared He would judge all humanity (Matthew 25:31-46), and said He existed before Abraham (John 8:58). The earliest Christian creed (Philippians 2:5-11, dated to within years of the crucifixion) declares Jesus equal with God. The disciples, monotheistic Jews who would never worship a creature, worshipped Jesus — the only explanation being that they recognized Him as Yahweh incarnate.",
            ["John 8:58", "John 10:30", "John 14:9", "Philippians 2:5-11", "Colossians 2:9", "John 1:1-3"],
            ["C.S. Lewis", "N.T. Wright", "Larry Hurtado", "Richard Bauckham"],
            ["Lord or Legend by Gregory Boyd", "Lord Jesus Christ by Larry Hurtado"]
        ),
        e_chirho(
            "Lewis's Trilemma",
            "What is C.S. Lewis's 'Liar, Lunatic, or Lord' argument?",
            "C.S. Lewis argued that Jesus' claims to divinity leave only three options: He was either a liar (He knew He wasn't God but said He was), a lunatic (He sincerely believed He was God but was deluded), or He was Lord (His claims were true). The popular view that Jesus was merely 'a great moral teacher' is the one option that is not available, because a mere man who claimed to be God would not be a great moral teacher — he would be either a deliberate deceiver or profoundly insane.\n\nThe liar hypothesis fails because Jesus' teaching on honesty, His willingness to die for His claims, and His character universally recognized as exemplary are incompatible with deliberate deception. The lunatic hypothesis fails because Jesus' teachings display remarkable wisdom, psychological insight, and coherence — the opposite of delusion. His responses to hostile questions, His profound parables, and His calm authority under pressure reveal a supremely rational mind. By elimination, the most reasonable conclusion is that Jesus is who He claimed to be: Lord. This trilemma forces us to take Jesus' claims seriously rather than dismissing Him as merely a good teacher.",
            ["John 14:6", "Mark 14:61-62", "John 10:33", "Matthew 16:15-16"],
            ["C.S. Lewis", "Peter Kreeft", "Josh McDowell"],
            ["Mere Christianity by C.S. Lewis", "More Than a Carpenter by Josh McDowell"]
        ),
        e_chirho(
            "Virgin Birth",
            "Why is the virgin birth of Jesus important, and is it credible?",
            "The virgin birth is prophesied in Isaiah 7:14 ('the virgin shall conceive and bear a son, and shall call his name Immanuel') and fulfilled in Matthew 1:18-25 and Luke 1:26-38. It is theologically essential because it preserves Jesus' sinless nature — born of a woman (truly human, Galatians 4:4) yet conceived by the Holy Spirit (truly divine, without inherited sin). Without the virgin birth, Jesus would be merely a man, incapable of being the sinless substitute who bears the sins of the world.\n\nSkeptics dismiss it as myth borrowed from pagan legends, but the parallels are superficial. Pagan myths involve gods physically mating with women; the biblical account is restrained — no physical union, just the overshadowing of the Holy Spirit. Matthew and Luke independently attest the virgin birth from different perspectives (Joseph's and Mary's respectively), and the early church universally affirmed it. The virgin birth also fits the pattern of God's supernatural interventions throughout Scripture — the births of Isaac, Samuel, and John the Baptist all involved divine action overcoming natural impossibility, pointing to God's sovereignty over creation.",
            ["Isaiah 7:14", "Matthew 1:18-25", "Luke 1:26-38", "Galatians 4:4"],
            ["J. Gresham Machen", "Robert Gromacki", "N.T. Wright"],
            ["The Virgin Birth of Christ by J. Gresham Machen"]
        ),
        e_chirho(
            "Resurrection Evidence: Empty Tomb",
            "What is the evidence for the empty tomb of Jesus?",
            "The empty tomb is supported by multiple lines of evidence. First, the tomb's location was known — Joseph of Arimathea, a member of the Sanhedrin, provided it (Mark 15:43-46), making it a publicly verifiable site. If the tomb were not empty, the authorities could have produced the body and ended Christianity at its inception. Second, the earliest Jewish polemic against the resurrection was that the disciples stole the body (Matthew 28:13), which implicitly concedes the tomb was empty. Third, women were the first witnesses — in a culture where women's testimony was considered unreliable, no one inventing a story would make women the primary witnesses unless it actually happened that way.\n\nFourth, the early creed in 1 Corinthians 15:3-5, dated to within 2-5 years of the crucifixion, states that Jesus 'was buried and was raised on the third day,' implying an empty tomb. Fifth, the disciples proclaimed the resurrection in Jerusalem, the very city where the tomb was located, making their claim immediately falsifiable if untrue. The convergence of these independent lines of evidence makes the empty tomb one of the best-established facts of ancient history.",
            ["Matthew 28:1-6", "Mark 16:1-6", "Luke 24:1-3", "1 Corinthians 15:3-5"],
            ["Gary Habermas", "William Lane Craig", "N.T. Wright", "Michael Licona"],
            ["The Son Rises by William Lane Craig", "The Case for the Resurrection of Jesus by Habermas and Licona"]
        ),
        e_chirho(
            "Resurrection Evidence: Post-Mortem Appearances",
            "What evidence exists for Jesus' post-resurrection appearances?",
            "The post-mortem appearances of Jesus are attested by multiple independent sources. Paul lists appearances to Peter, the Twelve, over 500 at once (most of whom were still alive when Paul wrote, c. AD 55, inviting verification), James, all the apostles, and Paul himself (1 Corinthians 15:5-8). The Gospels independently record appearances to Mary Magdalene, the women, the disciples on the Emmaus road, the gathered disciples (with and without Thomas), and seven disciples at the Sea of Galilee. These appearances occurred to individuals and groups, in various locations, over a period of 40 days.\n\nThe hallucination theory fails to account for these appearances. Hallucinations are individual psychological events — they cannot be shared by groups. They typically occur to people in expectant, hopeful states, but the disciples were in despair and disbelief. Hallucinations also do not eat fish (Luke 24:42-43) or invite physical touch (John 20:27). Furthermore, hallucinations would not produce the belief in bodily resurrection — the disciples could have concluded Jesus' spirit had appeared to them, not that He had risen bodily. Only actual encounters with the risen, bodily Christ adequately explain the diversity and character of the appearance traditions.",
            ["1 Corinthians 15:5-8", "Luke 24:36-43", "John 20:24-29", "Acts 1:3"],
            ["Gary Habermas", "Michael Licona", "Dale Allison"],
            ["The Risen Jesus and Future Hope by Gary Habermas", "Risen Indeed by Stephen Davis"]
        ),
        e_chirho(
            "Resurrection Evidence: Transformed Disciples",
            "How does the transformation of the disciples support the resurrection?",
            "The dramatic transformation of the disciples is powerful evidence for the resurrection. At the crucifixion, they fled in terror (Mark 14:50). Peter denied Jesus three times (Mark 14:66-72). They hid behind locked doors 'for fear of the Jews' (John 20:19). Yet within weeks, these same men were boldly proclaiming the resurrection in Jerusalem, willing to be arrested, beaten, imprisoned, and killed for their testimony. Peter, who cowered before a servant girl, stood before the Sanhedrin and declared, 'We must obey God rather than men' (Acts 5:29).\n\nLiars make poor martyrs. People will die for what they believe to be true (as martyrs of all religions demonstrate), but no one willingly dies for what they know to be a lie. If the disciples fabricated the resurrection, they knew it was false — and yet tradition records that Peter was crucified upside down, James was beheaded, and most apostles met violent ends without recanting. The dramatic psychological transformation from cowardice to fearless proclamation, from despair to unshakable conviction, demands an adequate cause. The best explanation is that they actually encountered the risen Christ.",
            ["Acts 2:14-36", "Acts 4:13", "Acts 5:29", "2 Corinthians 11:23-28"],
            ["N.T. Wright", "Sean McDowell", "Gary Habermas"],
            ["The Fate of the Apostles by Sean McDowell", "The Resurrection of the Son of God by N.T. Wright"]
        ),
        e_chirho(
            "Messianic Prophecy Fulfillment",
            "How many prophecies did Jesus fulfill, and what are the odds?",
            "Jesus fulfilled over 300 Old Testament prophecies, written centuries before His birth. These include His birthplace in Bethlehem (Micah 5:2), born of a virgin (Isaiah 7:14), from the tribe of Judah (Genesis 49:10) and line of David (2 Samuel 7:12-13), ministry in Galilee (Isaiah 9:1-2), entry into Jerusalem on a donkey (Zechariah 9:9), betrayal for 30 pieces of silver (Zechariah 11:12-13), crucifixion details (Psalm 22 — pierced hands and feet, garments divided, mocked), and burial in a rich man's tomb (Isaiah 53:9).\n\nPeter Stoner in 'Science Speaks' calculated the probability of one person fulfilling just 8 of these prophecies at 1 in 10^17. For 48 prophecies, the probability is 1 in 10^157. These astronomical odds make coincidental fulfillment effectively impossible. Skeptics who claim Jesus deliberately fulfilled prophecies cannot account for those beyond His control: birthplace, lineage, manner of death (crucifixion was a Roman, not Jewish, method), and betrayal price. The Dead Sea Scrolls confirm that these prophecies were written long before Jesus' birth, ruling out post-eventum invention. The fulfillment of messianic prophecy is God's fingerprint on history.",
            ["Micah 5:2", "Isaiah 7:14", "Isaiah 53:1-12", "Psalm 22:1-18", "Zechariah 9:9", "Daniel 9:24-26"],
            ["Peter Stoner", "Alfred Edersheim", "Michael Rydelnik", "Walter Kaiser"],
            ["Science Speaks by Peter Stoner", "The Life and Times of Jesus the Messiah by Alfred Edersheim"]
        ),
        e_chirho(
            "Jesus vs Other Religious Founders",
            "How is Jesus different from other religious founders like Muhammad, Buddha, or Krishna?",
            "Jesus is unique among religious founders in several decisive ways. First, He claimed to be God incarnate — not merely a prophet (Muhammad), an enlightened teacher (Buddha), or a mythological avatar (Krishna). Second, He validated His claims through historically verifiable miracles, supremely the resurrection. Third, He offered salvation by grace through faith, not by human effort — every other religion teaches some form of works-based merit. Fourth, He lived a sinless life, acknowledged even by the Quran (Surah 19:19). Fifth, He fulfilled centuries of specific prophecies.\n\nMuhammad claimed to be a prophet but performed no attested miracles comparable to Jesus' and died a natural death with no resurrection. Buddha was a spiritual philosopher who explicitly denied being divine and offered no salvation, only a path to escape suffering through self-effort. Krishna is a mythological figure with no historical attestation. Jesus alone among all religious figures claimed to be the unique Son of God, died for the sins of humanity, rose from the dead, and offers a personal relationship with the Creator. As He declared: 'I am the way, the truth, and the life. No one comes to the Father except through Me' (John 14:6).",
            ["John 14:6", "Acts 4:12", "1 Timothy 2:5", "John 10:18"],
            ["Ravi Zacharias", "Nabeel Qureshi", "John Lennox"],
            ["Jesus Among Other Gods by Ravi Zacharias", "Seeking Allah, Finding Jesus by Nabeel Qureshi"]
        ),
        e_chirho(
            "Uniqueness of Christ's Teachings",
            "What makes Jesus' teachings unique compared to all other religious and philosophical systems?",
            "Jesus' teachings are unique in both content and authority. He taught with personal authority ('I say to you') rather than appealing to prior tradition ('the rabbis say'). His Sermon on the Mount (Matthew 5-7) internalized morality — it is not enough to refrain from murder; anger itself is condemned. Not enough to avoid adultery; lust is addressed. He taught the radical love of enemies (Matthew 5:44), unprecedented in the ancient world. He elevated women, children, the poor, and outcasts in a culture that marginalized them.\n\nMost remarkably, Jesus placed Himself at the center of His teaching. While other teachers point away from themselves to principles or practices, Jesus pointed to Himself: 'I am the bread of life' (John 6:35), 'I am the light of the world' (John 8:12), 'I am the resurrection and the life' (John 11:25). He claimed that eternal destiny depends on one's relationship to Him personally (John 3:18, Matthew 7:21-23). No mere human teacher could make such claims without being either delusional or deceptive. His teachings have shaped civilization more profoundly than any other — inspiring hospitals, universities, human rights, abolition of slavery, and the dignity of every human person.",
            ["Matthew 5:44", "Matthew 7:28-29", "John 6:35", "John 8:12", "John 11:25-26"],
            ["Dallas Willard", "John Stott", "N.T. Wright"],
            ["The Divine Conspiracy by Dallas Willard", "The Cross of Christ by John Stott"]
        ),
        e_chirho(
            "Jesus as the Only Way",
            "Why do Christians believe Jesus is the only way to God?",
            "Christians believe Jesus is the only way because Jesus Himself made this exclusive claim: 'I am the way, the truth, and the life. No one comes to the Father except through Me' (John 14:6). Peter echoed this: 'There is no other name under heaven given among men by which we must be saved' (Acts 4:12). Paul affirmed: 'There is one God and one mediator between God and mankind, the man Christ Jesus' (1 Timothy 2:5). This exclusivity is not Christian arrogance — it is Jesus' own teaching.\n\nThe reason Jesus is the only way is rooted in the nature of the human problem: sin. All have sinned (Romans 3:23), and the wages of sin is death (Romans 6:23). No amount of human effort, religious ritual, or moral improvement can bridge the infinite gap between a holy God and sinful humanity. Only God Himself could pay the infinite debt — which is why God became man in Jesus Christ. The cross is not one option among many; it is the only solution to an otherwise hopeless situation. Other religions offer advice; Christianity alone offers a rescue. Other teachers say 'follow my teachings'; Jesus says 'I am the way' — not a way, but the way.",
            ["John 14:6", "Acts 4:12", "1 Timothy 2:5", "Romans 3:23", "Romans 6:23"],
            ["Ravi Zacharias", "Tim Keller", "John Piper"],
            ["The Reason for God by Tim Keller", "Jesus Among Other Gods by Ravi Zacharias"]
        ),
        e_chirho(
            "The Pre-existence of Christ",
            "Did Jesus exist before His birth in Bethlehem?",
            "Scripture teaches that Jesus, the eternal Son of God, existed before all creation. John 1:1-3 declares: 'In the beginning was the Word, and the Word was with God, and the Word was God. He was in the beginning with God. All things were made through Him.' John 8:58 records Jesus saying, 'Before Abraham was, I AM' — a claim to eternal pre-existence using God's covenant name. Colossians 1:15-17 states He is 'the firstborn over all creation' (meaning supreme over it, not created), through whom 'all things were created,' and 'in Him all things hold together.'\n\nMicah 5:2 prophesied the Messiah's origin as 'from of old, from everlasting.' Philippians 2:5-8 describes how Christ, 'being in the form of God,' emptied Himself and took the form of a servant, being born in human likeness. Hebrews 1:2 says God 'has spoken to us by His Son, through whom He made the worlds.' The pre-existence of Christ is not a later theological invention — it is embedded in the earliest Christian writings. Jesus is not a created being who was elevated to divine status; He is the eternal God who humbled Himself to enter creation for our salvation.",
            ["John 1:1-3", "John 8:58", "Colossians 1:15-17", "Micah 5:2", "Philippians 2:5-8", "Hebrews 1:2"],
            ["John of Damascus", "Athanasius", "Richard Bauckham", "Larry Hurtado"],
            ["On the Incarnation by Athanasius", "Jesus and the God of Israel by Richard Bauckham"]
        ),
        e_chirho(
            "The Sinlessness of Christ",
            "Why is the sinlessness of Jesus so important?",
            "The sinlessness of Jesus is attested by multiple New Testament authors: 'He committed no sin, neither was deceit found in His mouth' (1 Peter 2:22); 'Him who knew no sin' (2 Corinthians 5:21); 'One who in every respect has been tempted as we are, yet without sin' (Hebrews 4:15). Even His enemies found no fault in Him (John 18:38, Luke 23:4). This sinlessness is theologically essential for three reasons.\n\nFirst, only a sinless sacrifice could atone for sin. The Old Testament sacrificial system required unblemished animals (Leviticus 1:3), foreshadowing the perfect Lamb of God (John 1:29). A sinner cannot pay for others' sins — he owes for his own. Second, Jesus' sinlessness demonstrates His deity, since only God is without sin (Psalm 51:4, Romans 3:23). Third, His sinlessness qualifies Him as our righteous substitute: His perfect righteousness is imputed to believers (2 Corinthians 5:21, Romans 5:19). Without a sinless Christ, there is no gospel — no substitutionary atonement, no imputed righteousness, no salvation.",
            ["Hebrews 4:15", "2 Corinthians 5:21", "1 Peter 2:22", "John 1:29", "1 John 3:5"],
            ["John Owen", "J.I. Packer", "Wayne Grudem"],
            ["Knowing God by J.I. Packer", "The Death of Death in the Death of Christ by John Owen"]
        ),
        e_chirho(
            "The Crucifixion as Historical Fact",
            "Is the crucifixion of Jesus historically reliable?",
            "The crucifixion of Jesus is one of the best-attested events in ancient history. It is recorded in all four Gospels, referenced in the earliest Christian creed (1 Corinthians 15:3, dated to within 2-5 years of the event), and confirmed by non-Christian sources: Tacitus (Annals 15.44) states 'Christus suffered the extreme penalty during the reign of Tiberius at the hands of one of our procurators, Pontius Pilatus.' Josephus (Antiquities 18.63-64) records that 'Pilate condemned him to be crucified.' Lucian of Samosata, Mara bar Serapion, and the Talmud all reference Jesus' execution.\n\nJohn Dominic Crossan, a skeptical scholar, writes: 'That he was crucified is as sure as anything historical can ever be.' The crucifixion is embarrassing from a propaganda standpoint — a crucified Messiah was 'a stumbling block to Jews and foolishness to Gentiles' (1 Corinthians 1:23). No one would invent a crucified savior. The medical details in the Gospels (blood and water from the pierced side, John 19:34) are consistent with death by crucifixion as understood by modern medicine (pericardial and pleural effusion). The historicity of the crucifixion is the foundation upon which the entire gospel message rests.",
            ["1 Corinthians 15:3-4", "Mark 15:24-37", "John 19:34", "Galatians 3:13", "1 Corinthians 1:23"],
            ["John Dominic Crossan", "Martin Hengel", "Raymond Brown"],
            ["The Death of the Messiah by Raymond Brown", "Crucifixion by Martin Hengel"]
        ),
        e_chirho(
            "The Ascension of Christ",
            "What is the significance of Jesus' ascension?",
            "The ascension of Jesus (Acts 1:9-11, Luke 24:50-51) is a neglected but essential doctrine. After His resurrection, Jesus appeared to His disciples over 40 days, teaching about the kingdom of God (Acts 1:3), and then ascended visibly into heaven in their presence. The ascension accomplishes several things: First, it marks the completion of Jesus' earthly ministry and the beginning of His heavenly session — He is seated at the right hand of God (Mark 16:19, Hebrews 1:3), a position of supreme authority. From there He intercedes for believers (Romans 8:34, Hebrews 7:25).\n\nSecond, the ascension was necessary for the sending of the Holy Spirit (John 16:7) — 'Unless I go away, the Advocate will not come to you.' Third, it establishes Jesus' lordship over all creation (Ephesians 1:20-22, Philippians 2:9-11). Fourth, it provides the pattern for His return — 'This same Jesus, who has been taken from you into heaven, will come back in the same way you have seen him go into heaven' (Acts 1:11). The ascension assures believers that their Lord reigns now and will return personally, visibly, and bodily.",
            ["Acts 1:9-11", "Luke 24:50-51", "Hebrews 1:3", "Ephesians 1:20-22", "Philippians 2:9-11"],
            ["Thomas Torrance", "Gerrit Dawson", "N.T. Wright"],
            ["Jesus Ascended by Gerrit Dawson", "Surprised by Hope by N.T. Wright"]
        ),
        e_chirho(
            "The Titles of Jesus",
            "What do the various titles of Jesus reveal about His identity?",
            "Jesus' titles reveal His multifaceted divine identity. 'Son of God' (Matthew 16:16) denotes His unique relationship with the Father — not created, but eternally begotten, sharing God's very nature. 'Son of Man' (Daniel 7:13-14, Mark 14:62) references the divine figure in Daniel's vision who receives universal dominion — a claim to cosmic authority, not humility as often assumed. 'Lord' (Kyrios, Philippians 2:11) is the Greek translation of YHWH used in the Septuagint — calling Jesus Lord equates Him with Israel's God.\n\n'Logos/Word' (John 1:1) identifies Jesus as God's self-expression, the agent of creation, and the source of all meaning and rationality. 'Christ/Messiah' (John 4:25-26) is the long-awaited Anointed King from David's line. 'Alpha and Omega' (Revelation 1:8) claims absolute preeminence — the beginning and end of all things. 'I AM' (John 8:58) is the divine name from Exodus 3:14. 'Lamb of God' (John 1:29) identifies Him as the ultimate sacrifice for sin. Together, these titles present a portrait that is simultaneously fully human and fully divine — the God-man who bridges heaven and earth.",
            ["John 1:1", "John 1:29", "Daniel 7:13-14", "Philippians 2:11", "Revelation 1:8", "Matthew 16:16"],
            ["Oscar Cullmann", "Richard Bauckham", "Larry Hurtado"],
            ["The Christology of the New Testament by Oscar Cullmann", "Jesus and the God of Israel by Richard Bauckham"]
        ),
        e_chirho(
            "Jesus and the Old Testament",
            "How does Jesus fulfill the patterns and types of the Old Testament?",
            "Jesus is the antitype to whom all Old Testament types point. He is the true Adam (Romans 5:14, 1 Corinthians 15:45) — where Adam failed, Jesus succeeded. He is the true Israel (Matthew 2:15, Hosea 11:1) — where Israel was faithless, Jesus was faithful. He is the greater Moses (Deuteronomy 18:15, Acts 3:22) who delivers God's people from bondage to sin. He is the true Passover Lamb (1 Corinthians 5:7, Exodus 12) — slain so that death passes over God's people. He is the High Priest after the order of Melchizedek (Hebrews 7) who offers Himself as the ultimate sacrifice.\n\nHe is the Temple (John 2:19-21) — the dwelling place of God among men. He is the serpent lifted up (John 3:14, Numbers 21:8-9) — whoever looks to Him lives. He is the Bread from Heaven (John 6:32-35) — the true manna that gives life. He is David's greater Son (Matthew 22:41-45) who reigns forever. He is Jonah's sign (Matthew 12:39-40) — three days in the earth and rising again. The entire Old Testament is a preparation for Christ, and He is its fulfillment: 'These are the Scriptures that testify about Me' (John 5:39).",
            ["John 5:39", "Luke 24:27", "Luke 24:44", "Matthew 5:17", "Hebrews 1:1-3"],
            ["Edmund Clowney", "Graeme Goldsworthy", "Tremper Longman III"],
            ["The Unfolding Mystery by Edmund Clowney", "According to Plan by Graeme Goldsworthy"]
        ),
        e_chirho(
            "The Second Coming of Christ",
            "What does the Bible teach about the return of Jesus Christ?",
            "The Bible teaches that Jesus Christ will return personally, visibly, and bodily to judge the living and the dead and to establish His eternal kingdom. At His ascension, the angels declared: 'This same Jesus, who has been taken from you into heaven, will come back in the same way you have seen him go into heaven' (Acts 1:11). Jesus Himself promised: 'They will see the Son of Man coming on the clouds of heaven with power and great glory' (Matthew 24:30). Revelation 1:7 adds: 'Every eye will see him.'\n\nThe return of Christ will be unmistakable — 'as the lightning comes from the east and shines as far as the west, so will be the coming of the Son of Man' (Matthew 24:27). It will bring the final judgment (Matthew 25:31-46, 2 Corinthians 5:10), the resurrection of the dead (1 Thessalonians 4:16-17), and the renewal of all creation (Revelation 21:1-5, Romans 8:19-21). Christians are called to live in readiness and expectation (Matthew 24:42, Titus 2:13). The second coming is the 'blessed hope' that sustains the church through suffering — the assurance that history is moving toward its divinely appointed climax.",
            ["Acts 1:11", "Matthew 24:27-30", "1 Thessalonians 4:16-17", "Revelation 1:7", "Revelation 21:1-5"],
            ["N.T. Wright", "Anthony Hoekema", "George Eldon Ladd"],
            ["Surprised by Hope by N.T. Wright", "The Bible and the Future by Anthony Hoekema"]
        ),
        e_chirho(
            "Jesus' Miracles as Signs",
            "What is the apologetic significance of Jesus' miracles?",
            "Jesus' miracles function as 'signs' (semeia in John's Gospel) — not mere wonders but purposeful demonstrations of His divine identity and mission. John states: 'Jesus performed many other signs in the presence of his disciples... these are written that you may believe that Jesus is the Messiah, the Son of God' (John 20:30-31). Each miracle category reveals a specific aspect of His deity: healing the sick demonstrates power over disease, casting out demons shows authority over the spiritual realm, raising the dead proves mastery over death itself, and commanding nature reveals sovereignty over creation.\n\nThe miracles are not isolated events but fit a coherent theological pattern: they inaugurate the kingdom of God by reversing the effects of sin and the fall. Where sin brought blindness, Jesus gives sight. Where sin brought death, Jesus raises the dead. Where sin brought chaos, Jesus calms the storm. They fulfill specific messianic prophecies: 'the blind receive sight, the lame walk, those who have leprosy are cleansed, the deaf hear, the dead are raised' (Matthew 11:5, cf. Isaiah 35:5-6). Even Jesus' enemies did not deny His miracles — they attributed them to demonic power (Matthew 12:24), inadvertently confirming their reality.",
            ["John 20:30-31", "Matthew 11:4-5", "John 2:11", "Acts 2:22", "Isaiah 35:5-6"],
            ["Craig Keener", "Graham Twelftree", "C.S. Lewis"],
            ["Miracles: The Credibility of the New Testament Accounts by Craig Keener", "Jesus the Miracle Worker by Graham Twelftree"]
        ),
        e_chirho(
            "The Hypostatic Union",
            "How can Jesus be both fully God and fully man?",
            "The doctrine of the hypostatic union, defined at the Council of Chalcedon (AD 451), teaches that Jesus Christ is one person with two natures — fully divine and fully human — without confusion, change, division, or separation. He is not half God and half man, nor God wearing a human disguise, nor a man promoted to divinity. He is the eternal Son of God who assumed a complete human nature (body, soul, mind, will) while retaining His full divine nature.\n\nThis is not a logical contradiction but a mystery. A contradiction would be 'Jesus is fully God and not fully God' or 'Jesus is fully human and not fully human.' The claim is that two natures subsist in one person — which, while beyond our full comprehension, violates no law of logic. The incarnation is analogically like (though infinitely greater than) a human being who is simultaneously a father, a citizen, and an employee — different capacities in one person. Philippians 2:5-8 describes the self-emptying (kenosis) not as a loss of divine attributes but as a voluntary restraint in their independent exercise. Jesus is the unique bridge between God and humanity because He is both — the 'one mediator between God and mankind' (1 Timothy 2:5).",
            ["John 1:14", "Philippians 2:5-8", "Colossians 2:9", "1 Timothy 2:5", "Hebrews 2:14-17"],
            ["Council of Chalcedon", "Thomas Aquinas", "John of Damascus", "Donald Macleod"],
            ["The Person of Christ by Donald Macleod", "Systematic Theology by Wayne Grudem, ch. 26"]
        ),
    ]
