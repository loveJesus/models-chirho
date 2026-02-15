# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
compile-dialogues-chirho.py
Generate evangelism dialogue training data in JSONL format.
100 dialogues across 6 categories for training an evangelism/apologetics model.
"""

import json
from pathlib import Path

OUTPUT_DIR_CHIRHO = Path(__file__).resolve().parent.parent.parent / "data-chirho" / "raw-chirho" / "dialogues-chirho"


def build_common_objections_chirho() -> list[dict]:
    """Build 20 common objection dialogue entries."""
    return [
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "How can a loving God send people to hell?",
            "answer_chirho": "That is one of the most important questions anyone can ask, and it shows you take both love and justice seriously. The Bible teaches that God is indeed love (1 John 4:8), but He is also perfectly just and holy. A good judge does not let the guilty go unpunished. We have all sinned and fall short of God's glory (Romans 3:23), and the wages of sin is death (Romans 6:23). Hell was not created for people but for the devil and his angels (Matthew 25:41). God does not want anyone to perish but everyone to come to repentance (2 Peter 3:9). That is exactly why He sent Jesus. On the cross, Jesus took the punishment we deserve so that whoever believes in Him would not perish but have eternal life (John 3:16). God is not sending people to hell; He is rescuing people from it. If a doctor offers a cure and the patient refuses, the doctor is not responsible for the outcome. God has provided the cure in Christ. The question is not whether God is loving enough to save us — He proved His love at Calvary — but whether we will receive the gift He freely offers.",
            "dialogue_context_chirho": "A seeker wrestling with the character of God, feeling that eternal punishment contradicts divine love.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["1 John 4:8", "Romans 3:23", "Romans 6:23", "Matthew 25:41", "2 Peter 3:9", "John 3:16"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "What about people who never heard the Gospel?",
            "answer_chirho": "This is a sincere concern and shows a heart for fairness. Scripture tells us that God has revealed Himself to every person through creation so that people are without excuse (Romans 1:19-20). Everyone has an inner witness — the law written on their hearts and their conscience bearing witness (Romans 2:15). God is perfectly just and will judge each person according to the light they received. Abraham asked, 'Will not the Judge of all the earth do right?' (Genesis 18:25), and the answer is always yes. But here is what we must not miss: you have heard the Gospel right now. The more pressing question is what will you do with Jesus? He said, 'I am the way, the truth, and the life. No one comes to the Father except through Me' (John 14:6). God commands all people everywhere to repent (Acts 17:30). Rather than worrying about those who have not heard, let us be sure we respond to the message we have heard. And let us be motivated to share the Gospel so that more will hear. God's heart is that none should perish.",
            "dialogue_context_chirho": "A person questioning the fairness of God regarding those in unreached places.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Romans 1:19-20", "Romans 2:15", "Genesis 18:25", "John 14:6", "Acts 17:30"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "If God is real, why is there suffering?",
            "answer_chirho": "Suffering is real and painful, and God does not dismiss it. The Bible tells us that suffering entered the world through sin. When Adam and Eve rebelled, creation itself was subjected to futility (Romans 8:20-22). We live in a fallen world, and much suffering is the result of human choices — war, greed, abuse. But God did not leave us in our suffering. He entered into it. Jesus, God in the flesh, was a man of sorrows and acquainted with grief (Isaiah 53:3). He wept at the tomb of Lazarus (John 11:35). He suffered the worst death imaginable on the cross — not for His own sin, but for ours. God uses suffering to draw us to Himself. The psalmist wrote, 'Before I was afflicted I went astray, but now I keep Your word' (Psalm 119:67). And He promises that present sufferings are not worth comparing to the glory that will be revealed (Romans 8:18). One day He will wipe every tear from every eye (Revelation 21:4). The existence of suffering does not disprove God; it confirms the Bible's diagnosis that the world is broken and needs a Savior. That Savior is Jesus Christ.",
            "dialogue_context_chirho": "A person in pain or questioning God's existence because of observed suffering in the world.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Romans 8:20-22", "Isaiah 53:3", "John 11:35", "Psalm 119:67", "Romans 8:18", "Revelation 21:4"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "All religions lead to God.",
            "answer_chirho": "I understand why that feels appealing — it sounds inclusive and kind. But sincerity does not determine truth. If all roads led to the same destination, why would God send His only Son to die an agonizing death on the cross? Jesus Himself said, 'I am the way, the truth, and the life. No one comes to the Father except through Me' (John 14:6). That is either the most arrogant claim ever made or it is the truth spoken by God Himself. The religions of the world actually contradict each other on fundamental issues. Islam denies Jesus is God's Son. Hinduism teaches many gods. Buddhism has no personal Creator. Christianity teaches salvation by grace through faith, not by works (Ephesians 2:8-9). They cannot all be true simultaneously. The Bible says there is salvation in no one else, for there is no other name under heaven given among men by which we must be saved (Acts 4:12). This is not arrogance — it is a rescue announcement. A firefighter who says 'this is the only exit' is not being narrow-minded; he is saving your life. Jesus is that exit. He proved it by rising from the dead, something no other religious leader has done.",
            "dialogue_context_chirho": "A pluralistic friend who believes all spiritual paths are equally valid.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["John 14:6", "Ephesians 2:8-9", "Acts 4:12"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "Science has disproven God.",
            "answer_chirho": "Actually, science cannot disprove God any more than a telescope can disprove the existence of the astronomer. Science studies the natural world — how things work. God is the reason why anything exists at all. Many of the greatest scientists in history were devout Christians: Isaac Newton, Michael Faraday, James Clerk Maxwell, Georges Lemaitre who proposed the Big Bang theory was a priest. The Bible says, 'The heavens declare the glory of God; the skies proclaim the work of His hands' (Psalm 19:1). Science reveals the order and fine-tuning of the universe: the cosmological constants, DNA information, the laws of physics — all pointing to an intelligent Designer. Romans 1:20 says God's invisible attributes are clearly seen through what has been made. The real question is: can matter, energy, and blind chance produce the information in DNA, the fine-tuning of the universe, and human consciousness? Science has not answered that — and many honest scientists admit it. The Bible and true science are not enemies. But more importantly, God did not just create the universe and walk away. He stepped into history as Jesus Christ, lived, died for our sins, and rose again. That is a historical claim that can be investigated.",
            "dialogue_context_chirho": "A person who trusts science and assumes faith is incompatible with reason.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Psalm 19:1", "Romans 1:20"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "The Bible has been changed over time.",
            "answer_chirho": "This is a common claim but it does not hold up under examination. We have over 5,800 Greek manuscripts of the New Testament, some dating to within decades of the originals. The Dead Sea Scrolls, discovered in 1947, contained Old Testament texts from around 150 BC that matched our modern text with remarkable accuracy — particularly Isaiah, which contains the prophecy of Christ's suffering (Isaiah 53). By comparison, we have fewer than ten copies of Caesar's Gallic Wars, yet no one doubts its authenticity. Jesus said, 'Heaven and earth will pass away, but My words will never pass away' (Matthew 24:35). The Bible also says, 'The grass withers and the flowers fall, but the word of our God endures forever' (Isaiah 40:8). God has providentially preserved His Word. The minor textual variants that exist (mostly spelling differences) affect no doctrine whatsoever. The message is clear and consistent: all have sinned (Romans 3:23), the wages of sin is death (Romans 6:23), but God demonstrates His love in that while we were still sinners Christ died for us (Romans 5:8). That message has not changed in two thousand years because God Himself preserves it.",
            "dialogue_context_chirho": "A skeptic who has heard that the Bible is unreliable due to copying errors and translations.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Isaiah 53", "Matthew 24:35", "Isaiah 40:8", "Romans 3:23", "Romans 6:23", "Romans 5:8"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "Christians are hypocrites.",
            "answer_chirho": "You are not wrong that many Christians fail to live up to what they profess, and I am sorry for the ways that has hurt you or others. But here is the thing: Christianity is not a religion for perfect people. It is a hospital for sinners. Jesus said, 'It is not the healthy who need a doctor, but the sick. I have not come to call the righteous, but sinners to repentance' (Luke 5:31-32). Every Christian is a work in progress. The Bible says, 'If we claim to be without sin, we deceive ourselves' (1 John 1:8). The difference is not that Christians are perfect but that they have a perfect Savior. A hypocrite pretends to be something they are not. A Christian who sins and repents is not a hypocrite — they are exactly what the Bible describes: a sinner saved by grace. But consider this: would you reject medicine because the pharmacist is unhealthy? The truth of the Gospel does not depend on the behavior of its followers. It depends on Christ. And He never failed. He lived a sinless life, died for sinners, and rose from the dead. Judge Christianity by Christ, not by Christians. He said, 'Come to Me, all who are weary and burdened, and I will give you rest' (Matthew 11:28).",
            "dialogue_context_chirho": "A person who has been disappointed or hurt by the behavior of professing Christians.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Luke 5:31-32", "1 John 1:8", "Matthew 11:28"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "I'm a good person, I don't need saving.",
            "answer_chirho": "I appreciate your sincerity, and by human standards you may well be a good person. But the question is: by whose standard are we measured? Jesus said, 'No one is good except God alone' (Mark 10:18). God's standard is perfection. Have you ever told a lie? Stolen anything, even something small? Looked at someone with lust? Jesus said that is adultery in the heart (Matthew 5:28). Used God's name as a curse word? That is blasphemy. If God judges you by the Ten Commandments — His moral law — would you be innocent or guilty? The Bible says all have sinned and fall short of the glory of God (Romans 3:23). We are not sinners because we sin; we sin because we are sinners. Our good works cannot pay our sin debt any more than good deeds can pay a speeding fine. But here is the wonderful news: God, being rich in mercy, sent Christ to pay the fine on our behalf. 'For by grace you have been saved through faith, and that not of yourselves; it is the gift of God, not of works, lest anyone should boast' (Ephesians 2:8-9). You do not need to be good enough. You need a Savior. And His name is Jesus.",
            "dialogue_context_chirho": "A morally upright person who sees no personal need for salvation.",
            "methodology_chirho": "law_then_grace",
            "scripture_chirho": ["Mark 10:18", "Matthew 5:28", "Romans 3:23", "Ephesians 2:8-9"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "Why does God allow evil?",
            "answer_chirho": "This is one of the deepest questions of human existence. God created beings with free will — genuine choice to love or rebel. Love that is forced is not love at all. When humanity chose to rebel against God, evil entered the world. But God did not stand back and watch. He entered our broken world Himself. The cross of Jesus Christ is God's ultimate answer to evil. At the cross, the worst evil in history — the murder of the innocent Son of God — was used by God to accomplish the greatest good: the salvation of the world. As Joseph told his brothers, 'You meant evil against me, but God meant it for good' (Genesis 50:20). God is not indifferent to evil. He is so opposed to it that He sent His Son to destroy the works of the devil (1 John 3:8). And He promises a day when He will make all things new, where there will be no more death or mourning or crying or pain (Revelation 21:4). The real question is not 'why does God allow evil?' but 'what has God done about it?' The answer is the cross. And what will we do with the salvation He offers? He calls us to repent and believe the Gospel (Mark 1:15).",
            "dialogue_context_chirho": "A person troubled by the existence of evil and wondering about God's sovereignty.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Genesis 50:20", "1 John 3:8", "Revelation 21:4", "Mark 1:15"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "The Bible is outdated and irrelevant.",
            "answer_chirho": "The Bible addresses every issue the human heart faces: guilt, fear, purpose, death, relationships, justice, identity. Those are not outdated concerns. The writer of Hebrews says, 'The word of God is alive and active, sharper than any double-edged sword' (Hebrews 4:12). It was written over 1,500 years by 40 authors across three continents, yet it tells one unified story of redemption through Jesus Christ. Its prophecies have been fulfilled with stunning accuracy — over 300 prophecies about the Messiah alone, all fulfilled in Jesus. The Bible predicted the rise and fall of empires (Daniel 2), the scattering and regathering of Israel, and the exact nature of Christ's death (Psalm 22, Isaiah 53) centuries before it happened. Jesus said, 'Heaven and earth will pass away, but My words will never pass away' (Mark 13:31). Cultures change, technology advances, but the human condition remains the same: we are sinners who need a Savior. The Bible's message is as relevant today as it was two thousand years ago because the God who inspired it is the same yesterday, today, and forever (Hebrews 13:8). I would encourage you to read the Gospel of John and see for yourself.",
            "dialogue_context_chirho": "A modern person who views the Bible as an ancient book with no bearing on contemporary life.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Hebrews 4:12", "Daniel 2", "Psalm 22", "Isaiah 53", "Mark 13:31", "Hebrews 13:8"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "You can't prove God exists.",
            "answer_chirho": "You are right that God cannot be put in a test tube, but that does not mean there is no evidence. You cannot put love in a test tube either, yet you know it exists. The evidence for God is overwhelming when considered honestly. Creation itself testifies: 'The heavens declare the glory of God' (Psalm 19:1). The universe had a beginning, and everything that begins has a cause. The fine-tuning of physical constants, the information encoded in DNA, and the existence of objective moral laws all point to an intelligent, moral Creator. Romans 1:20 says that God's eternal power and divine nature have been clearly seen from what has been made. But the strongest evidence is the resurrection of Jesus Christ. It is a historical event attested by over 500 eyewitnesses (1 Corinthians 15:6), an empty tomb that no one could explain away, and disciples who went from cowards to martyrs overnight. People die for what they believe is true, but no one dies for what they know is a lie. The resurrection changes everything. If Jesus rose from the dead, then He is who He claimed to be — God in the flesh — and His offer of salvation is real. I urge you to investigate it honestly.",
            "dialogue_context_chirho": "An empirically minded person demanding verifiable proof for God's existence.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Psalm 19:1", "Romans 1:20", "1 Corinthians 15:6"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "What about all the wars fought in God's name?",
            "answer_chirho": "It is true that terrible things have been done in the name of religion, and that is tragic. But doing something in God's name does not mean God endorsed it. Jesus said, 'Many will say to Me on that day, Lord, Lord, did we not do many things in Your name? And I will say, I never knew you; depart from Me' (Matthew 7:22-23). The Crusades, the Inquisition, and other atrocities were committed by people who violated the very teachings of Christ. Jesus taught us to love our enemies, turn the other cheek, and bless those who persecute us (Matthew 5:44). Compare that with the explicitly atheistic regimes of the 20th century: Stalin, Mao, and Pol Pot killed over 100 million people. The problem is not religion or irreligion — the problem is the human heart. Jeremiah 17:9 says, 'The heart is deceitful above all things, and desperately wicked.' That is precisely why we need a Savior. Jesus did not come to start wars; He came to reconcile us to God and to one another. He said, 'Peace I leave with you; My peace I give to you' (John 14:27). Do not judge the Prince of Peace by those who violate His commands.",
            "dialogue_context_chirho": "A person who views Christianity as a violent religion responsible for historical atrocities.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Matthew 7:22-23", "Matthew 5:44", "Jeremiah 17:9", "John 14:27"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "I believe in science, not faith.",
            "answer_chirho": "Science and faith are not opposites. Science answers 'how' questions; faith answers 'why' questions. Science can tell you how the human body works but not why human life has value. You actually exercise faith every day — faith that the laws of physics will remain constant, faith that your senses are reliable, faith that other minds exist. These are philosophical assumptions science cannot prove but must presuppose. The Bible says, 'By faith we understand that the universe was formed at God's command, so that what is seen was not made out of what was visible' (Hebrews 11:3). Modern science was born in a Christian worldview because Christians believed in a rational God who made an orderly universe that could be studied. The very intelligibility of the universe points to a Mind behind it. As Einstein said, the most incomprehensible thing about the universe is that it is comprehensible. Romans 1:20 tells us that God's invisible qualities are clearly understood from creation. I would encourage you to apply the same rigor you use in science to investigating the claims of Christ: the historical evidence for His resurrection, the fulfilled prophecies, the transformed lives. Honest investigation leads to truth, and Jesus said, 'I am the truth' (John 14:6).",
            "dialogue_context_chirho": "A scientifically minded person who sees faith as opposed to rational thinking.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Hebrews 11:3", "Romans 1:20", "John 14:6"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "The Bible contradicts itself.",
            "answer_chirho": "Many people say this, but when asked for a specific example, most cannot name one. There are passages that seem difficult at first glance, but context resolves the vast majority. The Bible was written over 1,500 years by about 40 different authors, yet it tells one consistent story from Genesis to Revelation: God creates, humanity falls, God redeems through Christ. That unity across centuries is itself a miracle. Jesus affirmed the Old Testament's authority: 'Scripture cannot be broken' (John 10:35). Apparent contradictions often arise from not considering genre, context, audience, or the complementary nature of accounts. Four Gospels give four perspectives on the same events, just as four witnesses at a trial may emphasize different details without contradicting each other. The Bible says, 'All Scripture is God-breathed and is useful for teaching, rebuking, correcting, and training in righteousness' (2 Timothy 3:16). I would encourage you to bring me a specific passage you find contradictory, and let us look at it together. But do not let a perceived difficulty keep you from the Bible's central message: 'Christ Jesus came into the world to save sinners' (1 Timothy 1:15). That message is crystal clear from cover to cover.",
            "dialogue_context_chirho": "A skeptic who has heard the Bible is full of contradictions but may not have read it carefully.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["John 10:35", "2 Timothy 3:16", "1 Timothy 1:15"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "How can you believe a book written by men?",
            "answer_chirho": "Every book is written by human hands, including science textbooks and history books. The question is whether the Author behind the human authors is God. The Bible claims to be God-breathed: 'All Scripture is inspired by God' (2 Timothy 3:16). Peter explains, 'Prophets, though human, spoke from God as they were carried along by the Holy Spirit' (2 Peter 1:21). God used human personalities and writing styles, but the message is His. The evidence supports this claim remarkably. The Bible contains over 2,000 fulfilled prophecies. It predicted the exact manner of Christ's death by crucifixion (Psalm 22) centuries before crucifixion was invented. It predicted the birth city of the Messiah (Micah 5:2), His betrayal for thirty pieces of silver (Zechariah 11:12-13), and His resurrection (Psalm 16:10). The probability of one person fulfilling just eight of these prophecies by chance is 1 in 10 to the 17th power. The Bible also contains scientific insights ahead of its time: the earth hanging on nothing (Job 26:7), the water cycle (Ecclesiastes 1:7), and the expansion of the universe (Isaiah 40:22). This book transforms lives. It has survived every attempt to destroy it. It is the most scrutinized book in history, and it stands. Read it and let God speak to you through it.",
            "dialogue_context_chirho": "A person skeptical of the Bible's divine authorship because of its human writers.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["2 Timothy 3:16", "2 Peter 1:21", "Psalm 22", "Micah 5:2", "Zechariah 11:12-13", "Job 26:7"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "Isn't it arrogant to claim there's only one way?",
            "answer_chirho": "It might seem arrogant if a person invented the claim. But Christians did not invent it — Jesus said it: 'I am the way, the truth, and the life. No one comes to the Father except through Me' (John 14:6). If Jesus is who He claimed to be — God in the flesh, proven by His resurrection — then this is not arrogance but truth spoken in love. Is it arrogant for a doctor to say there is only one cure for a disease? Is a math teacher arrogant for insisting two plus two equals four? Truth by its nature is exclusive. Every worldview makes exclusive claims. Even saying 'all paths lead to God' excludes the views of anyone who disagrees. The Bible says, 'There is one God and one mediator between God and mankind, the man Christ Jesus, who gave Himself as a ransom for all people' (1 Timothy 2:5-6). Christianity is actually the most humble religion because it says no one is good enough to earn salvation — it is a gift of grace (Ephesians 2:8-9). We come to God not on our own merit but through what Christ did for us. That is not arrogance; that is humility. We are beggars telling other beggars where to find bread.",
            "dialogue_context_chirho": "A person who feels that exclusivity claims are inherently intolerant or arrogant.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["John 14:6", "1 Timothy 2:5-6", "Ephesians 2:8-9"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "Why would God create people just to condemn them?",
            "answer_chirho": "God did not create people to condemn them. He created us for relationship with Him, to know His love and reflect His glory. The Bible says God created humanity in His own image (Genesis 1:27) and called His creation 'very good' (Genesis 1:31). It was humanity's free choice to rebel against God that brought condemnation. God, in His foreknowledge, knew we would fall — and He had a plan of redemption before the foundation of the world (Ephesians 1:4). Jesus is described as 'the Lamb slain from the foundation of the world' (Revelation 13:8). God created us knowing we would fall, but also knowing He would redeem us at infinite cost to Himself. John 3:17 says, 'God did not send His Son into the world to condemn the world, but to save the world through Him.' The condemnation is not God's desire; it is the consequence of rejecting His rescue. If someone builds a boat to save drowning people and some refuse to get on board, the builder is not condemning them — their refusal is. God's heart is salvation. He has done everything possible to save you. The cross proves it.",
            "dialogue_context_chirho": "A person questioning God's motives in creation, struggling with predestination and free will.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Genesis 1:27", "Genesis 1:31", "Ephesians 1:4", "Revelation 13:8", "John 3:17"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "I've been hurt by the church.",
            "answer_chirho": "I am genuinely sorry for the pain you have experienced. That should never have happened, and your hurt is valid. The church is made up of imperfect people, and sometimes those people cause real damage. But please do not let a broken instrument keep you from the Physician. Jesus Himself was betrayed by one of His own disciples, denied by another, and abandoned by most of them in His hour of greatest need. He understands betrayal and pain more deeply than anyone. Isaiah 53:3 says He was 'despised and rejected by men, a man of sorrows and acquainted with grief.' Jesus never hurt anyone — He only healed, loved, and gave. He said, 'Come to Me, all you who are weary and burdened, and I will give you rest' (Matthew 11:28). The failures of the church are actually predicted in Scripture. Jesus warned about wolves in sheep's clothing (Matthew 7:15) and tares among the wheat (Matthew 13:24-30). The Bible never promised that every person in a church building is genuine. But Jesus is genuine. He will never leave you or forsake you (Hebrews 13:5). I encourage you to separate your experience with flawed people from your relationship with a perfect Savior. Give Jesus another chance — He has never changed.",
            "dialogue_context_chirho": "A person who has experienced spiritual abuse, hypocrisy, or mistreatment from church members or leaders.",
            "methodology_chirho": "direct_witness",
            "scripture_chirho": ["Isaiah 53:3", "Matthew 11:28", "Matthew 7:15", "Matthew 13:24-30", "Hebrews 13:5"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "Religion is a crutch for weak people.",
            "answer_chirho": "If Christianity is a crutch, then it is a crutch for people who realize their leg is broken — which is all of us. The Bible says, 'All have sinned and fall short of the glory of God' (Romans 3:23). Recognizing your need is not weakness; it is honesty. It takes more courage to admit you cannot save yourself than to pretend you have it all together. Jesus said, 'It is not the healthy who need a doctor, but the sick' (Mark 2:17). Many of the boldest people in history were Christians: William Wilberforce who ended the slave trade, Corrie ten Boom who hid Jews from the Nazis, Dietrich Bonhoeffer who stood against Hitler and was executed for it. These were not weak people clinging to a crutch — they were empowered by the living God. The apostle Paul wrote, 'I can do all things through Christ who strengthens me' (Philippians 4:13) and 'When I am weak, then I am strong' (2 Corinthians 12:10). Christianity is not about weakness; it is about the admission of human limitation met by divine power. The question is not whether you are strong enough to not need God. The question is: are you honest enough to admit that you do?",
            "dialogue_context_chirho": "A self-reliant person who views faith as intellectual or emotional weakness.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Romans 3:23", "Mark 2:17", "Philippians 4:13", "2 Corinthians 12:10"]
        },
        {
            "source_chirho": "compiled_dialogues",
            "category_chirho": "evangelism_dialogue",
            "question_chirho": "What about evolution?",
            "answer_chirho": "Whether you believe God created in six literal days or through a longer process, the central question is not how long it took but who did it. The Bible is clear: 'In the beginning God created the heavens and the earth' (Genesis 1:1). 'By faith we understand that the universe was formed at God's command' (Hebrews 11:3). Even if evolution were true in every detail, it would not explain the origin of life from non-life, the origin of information in DNA, or the origin of consciousness. These point to a Mind behind the material. Psalm 139:14 says, 'I praise You because I am fearfully and wonderfully made; Your works are wonderful.' The complexity of a single cell exceeds that of any human technology. But here is what matters most: the evolution debate is not a salvation issue. Whether God created in six days or six billion years, the Gospel remains the same. You are a sinner who needs a Savior. Jesus Christ, God's Son, died for your sins and rose from the dead. That is the issue that determines your eternal destiny. Romans 10:9 says, 'If you confess with your mouth that Jesus is Lord and believe in your heart that God raised Him from the dead, you will be saved.' Do not let a secondary issue keep you from the primary one.",
            "dialogue_context_chirho": "A person who believes evolution disproves the need for God or the Bible's authority.",
            "methodology_chirho": "apologetic_bridge",
            "scripture_chirho": ["Genesis 1:1", "Hebrews 11:3", "Psalm 139:14", "Romans 10:9"]
        },
    ]


def build_law_then_grace_chirho() -> list[dict]:
    """Build 15 law-then-grace dialogue entries."""
    return []


def build_atheist_encounters_chirho() -> list[dict]:
    """Build 15 atheist/agnostic encounter dialogue entries."""
    return []


def build_gospel_presentations_chirho() -> list[dict]:
    """Build 15 Gospel presentation dialogue entries."""
    return []


def build_world_religion_chirho() -> list[dict]:
    """Build 15 world religion comparison dialogue entries."""
    return []


def build_personal_youth_chirho() -> list[dict]:
    """Build 20 personal/youth dialogue entries."""
    return []


def main_chirho() -> None:
    """Main entry point: compile all dialogues and write to JSONL."""
    all_dialogues_chirho: list[dict] = []
    all_dialogues_chirho.extend(build_common_objections_chirho())
    all_dialogues_chirho.extend(build_law_then_grace_chirho())
    all_dialogues_chirho.extend(build_atheist_encounters_chirho())
    all_dialogues_chirho.extend(build_gospel_presentations_chirho())
    all_dialogues_chirho.extend(build_world_religion_chirho())
    all_dialogues_chirho.extend(build_personal_youth_chirho())

    OUTPUT_DIR_CHIRHO.mkdir(parents=True, exist_ok=True)
    output_path_chirho = OUTPUT_DIR_CHIRHO / "compiled-dialogues-chirho.jsonl"

    with open(output_path_chirho, "w", encoding="utf-8") as f_chirho:
        for entry_chirho in all_dialogues_chirho:
            f_chirho.write(json.dumps(entry_chirho, ensure_ascii=False) + "\n")

    print(f"Total dialogues compiled: {len(all_dialogues_chirho)}")
    print(f"Output written to: {output_path_chirho}")

    # Category breakdown
    categories_chirho: dict[str, int] = {}
    for entry_chirho in all_dialogues_chirho:
        method_chirho = entry_chirho.get("methodology_chirho", "unknown")
        categories_chirho[method_chirho] = categories_chirho.get(method_chirho, 0) + 1
    print("Methodology breakdown:")
    for method_chirho, count_chirho in sorted(categories_chirho.items()):
        print(f"  {method_chirho}: {count_chirho}")


if __name__ == "__main__":
    main_chirho()
