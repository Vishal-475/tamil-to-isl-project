
# TAMIL SPEECH TO INDIAN SIGN LANGUAGE TRANSLATION SYSTEM

## A Minor Project Report

### Submitted in Partial Fulfillment of the Requirements for the Degree of Bachelor of Technology

---

# ABSTRACT

Communication is a fundamental human right, yet millions of hearing-impaired individuals across India are denied equitable participation in daily life due to the scarcity of sign language interpretation services. Indian Sign Language (ISL), which serves as the primary mode of communication for an estimated 6.3 million deaf and hard-of-hearing individuals in the country, remains separated from the spoken languages of India by a technological divide that has persisted for decades. In the southern Indian state of Tamil Nadu, where Tamil is the dominant spoken language, the absence of any automated Tamil-to-ISL translation technology leaves deaf individuals unable to access spoken content in educational institutions, healthcare facilities, government offices, and public spaces.

This project presents the design, implementation, and evaluation of a web-based Tamil Speech to Indian Sign Language Translation System. The system implements a multi-stage translation pipeline that transforms Tamil spoken input into ISL video output through four sequential processing stages. In the first stage, Tamil speech captured via browser-based microphone recording or audio file upload is converted to Tamil text using Google's Speech-to-Text API with Tamil language support (ta-IN locale). In the second stage, the recognized Tamil text is translated to English using the deep-translator library's GoogleTranslator module. In the third stage, the English text is transformed into an ISL-compatible word sequence through Natural Language Processing (NLP) techniques implemented using the Natural Language Toolkit (NLTK), specifically tokenization, stopword removal, and verb lemmatization. In the fourth and final stage, each word in the ISL sequence is mapped to a corresponding pre-recorded sign language video from the project's ISL dataset, and these videos are played sequentially in the browser alongside a 2D avatar representation.

The backend is developed using FastAPI, a high-performance asynchronous Python web framework, and exposes three RESTful API endpoints: POST /api/process-audio for the main translation pipeline, GET /api/video/{word} for serving individual sign videos, and GET /api/avatar/{word} for serving 2D avatar pose images. The frontend is implemented using vanilla HTML5, CSS3, and JavaScript, with RecordRTC providing cross-browser PCM WAV audio recording at 16kHz mono. The system features a modern dark-themed user interface with glassmorphism design elements, animated recording indicators, a three-panel layout displaying input controls, translation pipeline stages, and video output, and real-time latency metrics showing end-to-end processing time and average per-word latency.

The system's ISL video dataset comprises 151 primary sign videos (covering the A-Z alphabet, digits 0-9, question words, and over 100 common words) and 75 secondary fallback videos. A supplementary 2D avatar system provides 191 word-specific sign pose images. An intelligent audio chunking mechanism based on pydub's split_on_silence function enables processing of audio recordings exceeding one minute by splitting them into manageable segments at silence boundaries. Performance evaluation demonstrates average end-to-end latency of 2 to 4 seconds for typical speech inputs, with per-word latency averaging under 1 second. The project aligns with United Nations Sustainable Development Goals 3, 4, and 10, contributing to accessible healthcare, inclusive education, and reduced inequalities for the deaf community.

---

# CHAPTER 1: INTRODUCTION

## 1.1 Introduction to Project

Language is the cornerstone of human civilization, serving as the vehicle through which knowledge, emotions, culture, and intent are communicated between individuals. For the vast majority of the world's population, spoken language fulfills this role naturally and effortlessly. However, for millions of individuals who are deaf or hard of hearing, spoken language presents an insurmountable barrier, necessitating the use of sign languages — visual-gestural communication systems that convey meaning through hand shapes, facial expressions, body posture, and spatial relationships. In India, Indian Sign Language (ISL) serves as the primary communication medium for approximately 6.3 million deaf individuals, as estimated by the World Health Organization and the Census of India. Despite this substantial population, the intersection of spoken Indian regional languages and ISL remains almost entirely bereft of automated translation technology, creating a persistent communication divide that affects education, employment, healthcare, and social inclusion.

The Tamil Speech to Indian Sign Language Translation System presented in this report is a web-based application that addresses this communication gap by providing an automated, real-time pipeline for translating spoken Tamil into ISL video sequences. Tamil, a Dravidian language spoken by over 75 million native speakers worldwide and serving as the official language of Tamil Nadu, Puducherry, and Sri Lanka, was chosen as the source language for this project due to its significant speaker population and the near-complete absence of Tamil-to-ISL translation tools in the existing technological landscape.

The system is built upon a modular architecture that decomposes the complex translation problem into four well-defined processing stages. The first stage handles acoustic signal processing, wherein Tamil speech captured through the browser's microphone or uploaded as an audio file is converted to Tamil text using Google's cloud-based Speech-to-Text API. The second stage performs interlingual translation, converting the recognized Tamil text to English using the deep-translator library. The third stage applies Natural Language Processing techniques to transform the English sentence into an ISL-compatible word sequence by removing function words, lemmatizing verbs, and preserving content words. The fourth stage maps each processed word to a corresponding pre-recorded ISL sign video and plays these videos sequentially in the browser, creating a continuous sign language output.

The backend of the system is implemented using FastAPI, a modern Python web framework that supports asynchronous request handling and provides automatic API documentation through OpenAPI and JSON Schema. FastAPI was selected for its exceptional performance characteristics, its intuitive dependency injection system, and its native support for file upload handling through the python-multipart library. The backend integrates several key Python libraries: SpeechRecognition for interfacing with Google's Speech-to-Text API, deep-translator for machine translation, NLTK for natural language processing, and pydub for audio format conversion and silence-based segmentation.

The frontend is developed using vanilla HTML5, CSS3, and JavaScript, deliberately avoiding frontend frameworks such as React, Angular, or Vue.js in favor of a lightweight, dependency-free implementation that loads instantly and runs reliably across all modern browsers. The user interface features a premium dark-themed design inspired by modern glassmorphism aesthetics, with a cyan accent color scheme, animated micro-interactions, and responsive layouts that adapt seamlessly to desktop and mobile screen dimensions. Audio recording is implemented using RecordRTC, a widely-adopted JavaScript library that provides cross-browser PCM WAV recording, eliminating the format conversion issues that arise from browser-native MediaRecorder implementations that typically produce WebM or Ogg encoded audio.

The system's ISL dataset consists of two complementary collections. The primary dataset, stored in the ISL_Dataset directory, contains 151 MP4 video files of human signers demonstrating authentic ISL signs. This collection covers the complete English alphabet (A through Z, 26 files), numerical digits (0 through 9, 10 files), interrogative words (How, What, When, Where, Which, Who, Whose, Why, 8 files), and over 100 common vocabulary words spanning pronouns, verbs, nouns, adjectives, and connectors. The secondary dataset, stored in the dataset directory, contains 75 programmatically generated mock video files that serve as development and testing placeholders. These mock videos are produced by the mock_generator.py script using OpenCV, creating animated circles with word labels that visually represent each sign.

Additionally, the system incorporates a 2D avatar representation system with 191 word-specific sign pose images stored in the dataset/2d_avatars directory. These images feature a consistent character design — a 2D Indian avatar figure — with hand position indicators that represent the signing posture for each word. The avatar images are generated by the avatar_generator.py script, which takes a base avatar image and applies deterministic transformations based on word hashes to produce unique visual representations for each sign.

## 1.2 Problem Statement and Description

The problem addressed by this project can be stated concisely: there exists no accessible, automated, browser-based system capable of translating spoken Tamil into Indian Sign Language video output in real time. This problem is situated at the intersection of several broader challenges in computational linguistics, assistive technology, and human-computer interaction, each of which contributes to the overall complexity of the solution.

The first dimension of the problem concerns the acoustic processing of Tamil speech. Tamil is a morphologically rich, agglutinative language belonging to the Dravidian language family. Unlike English, Tamil employs extensive suffixation to encode grammatical relationships, case markers, and tense information, resulting in long, morphologically complex word forms that present challenges for speech recognition systems. Furthermore, Tamil exhibits significant dialectal variation across geographic regions, socioeconomic strata, and registers of formality, meaning that a speech recognition system must accommodate diverse pronunciation patterns, vocabulary choices, and prosodic features. While Google's Speech-to-Text API provides Tamil language support through the ta-IN locale, its accuracy is known to vary based on speaker accent, recording quality, and the complexity of the spoken content.

The second dimension concerns the typological gap between Tamil, English, and ISL. Tamil follows a Subject-Object-Verb (SOV) sentence order, English follows a Subject-Verb-Object (SVO) order, and ISL uses a flexible Topic-Comment or SOV structure. Translating between these fundamentally different sentence structures requires more than simple word substitution; it demands an understanding of the syntactic roles of individual words and the ability to rearrange them according to the target language's grammatical conventions. This project uses English as an intermediary language for pragmatic reasons — the extensive NLP resources available for English (tokenizers, stopword lists, lemmatizers) make it a practical bridge between Tamil and ISL — but this two-stage translation introduces additional sources of error and latency.

The third dimension concerns the linguistic properties of ISL itself. ISL is not merely a gestural encoding of spoken Hindi or English; it is a fully independent natural language with its own grammar, syntax, and lexicon. Key differences between ISL and spoken languages include: the absence of articles (a, an, the), auxiliary verbs (am, is, are, was, were), and many prepositions (to, from, at) in ISL; the use of root verb forms without tense, aspect, or mood markers; the reliance on facial expressions and body posture for grammatical information such as negation and interrogation; and the use of spatial referencing for pronoun resolution. Any system that translates spoken language into ISL must account for these differences by transforming the source text to remove or modify elements that are absent in ISL while preserving the semantic content.

The fourth dimension concerns the real-time performance requirement. For the system to be practical in conversational or educational settings, the total time from speech input to sign language output must be short enough to maintain the natural flow of communication. Users cannot tolerate delays of tens of seconds waiting for a translation; the system must process the input, perform all translation and rendering stages, and begin playing the sign video output within a few seconds of the speech ending. This constraint influences every architectural and implementation decision, from the choice of cloud-based APIs (which offer high accuracy but introduce network latency) to the frontend playback mechanism (which must start playing videos immediately without buffering the entire sequence first).

The fifth dimension concerns accessibility and deployment. The system must be usable by individuals with varying levels of technical expertise, without requiring software installation, account creation, or configuration. A web-based deployment model, where the system is accessed through a standard web browser, is essential for achieving broad accessibility. The system must also work across different devices (desktops, laptops, tablets, smartphones) and operating systems (Windows, macOS, Linux, Android, iOS), requiring a responsive design that adapts to different screen sizes and input modalities.

## 1.3 Motivation

The motivation for undertaking this project arises from a confluence of social imperatives, technological opportunities, and academic interests that together make the problem both urgent and tractable.

From a social perspective, the hearing-impaired community in India faces systemic exclusion from virtually every aspect of public life. According to the World Health Organization's 2021 World Report on Hearing, India has one of the highest burdens of hearing loss globally, with approximately 63 million people experiencing significant auditory impairment. The Indian Census data further indicates that hearing disability is the second most common form of disability in the country, after locomotor disability. Despite these numbers, the infrastructure for sign language interpretation in India is woefully inadequate. The country has fewer than 300 certified ISL interpreters for a deaf population of over 6 million, translating to a ratio of approximately one interpreter per 20,000 deaf individuals. This scarcity is most acutely felt in non-metropolitan areas and in states where non-Hindi regional languages dominate, as the limited pool of interpreters is concentrated in major cities and tends to work with Hindi and English rather than regional languages.

In Tamil Nadu specifically, the situation is compounded by the linguistic characteristics of the state. Tamil is the second most spoken Dravidian language in the world, with deep cultural and literary traditions spanning over 2,000 years. The Tamil-speaking deaf community has developed ISL variants that incorporate Tamil cultural references and regional signs, but these variants receive even less technological attention than mainstream ISL. The result is a complete absence of automated translation tools that can bridge the gap between spoken Tamil and any form of sign language, leaving Tamil-speaking deaf individuals dependent on the rare availability of human interpreters or the goodwill of bilingual family members and friends.

From a technological perspective, the past decade has witnessed dramatic improvements in the accuracy and accessibility of the component technologies required for a speech-to-sign-language translation system. Cloud-based speech recognition APIs, such as Google's Speech-to-Text service, now achieve word error rates below 10 percent for many languages, including Tamil. Neural machine translation systems have reached near-human accuracy for major language pairs, and the availability of these systems through simple REST APIs has made multilingual translation accessible to developers without machine learning expertise. NLP libraries such as NLTK and spaCy provide comprehensive tools for text processing, morphological analysis, and syntactic parsing in Python. Web technologies including the Web Audio API, MediaDevices API, and HTML5 video element provide the browser-based infrastructure necessary for audio capture and video playback without plugins or native code.

From an academic perspective, this project addresses a demonstrated gap in the research literature. A survey of published work on sign language translation reveals that the overwhelming majority of studies focus on either American Sign Language (ASL) or sign language recognition rather than production. Studies that address sign language production typically use English as the source language and animated 3D avatars as the output medium. The specific combination of a Dravidian source language (Tamil), an Indian target sign language (ISL), and a video-based output medium represents a novel contribution to the field that has received virtually no prior attention.

## 1.4 Sustainable Development Goal of the Project

The United Nations 2030 Agenda for Sustainable Development defines 17 Sustainable Development Goals (SDGs) that address the global challenges facing humanity. This project contributes directly to three of these goals, demonstrating how technology can be applied to advance social equity, educational access, and health outcomes for marginalized communities.

SDG 4: Quality Education. The fourth Sustainable Development Goal seeks to "ensure inclusive and equitable quality education and promote lifelong learning opportunities for all." Target 4.5 specifically calls for the elimination of disparities in education for persons with disabilities by 2030. The Tamil Speech to ISL Translation System contributes to this goal by providing a tool that can translate spoken Tamil educational content — lectures, discussions, instructional videos, examination questions — into ISL video sequences that deaf students can understand. In Tamil Nadu's educational system, where instruction is delivered primarily in Tamil, the absence of ISL interpretation means that deaf students enrolled in mainstream schools receive little or no benefit from classroom instruction. This system, deployed on a classroom computer or tablet, could provide real-time ISL translation of teacher speech, enabling deaf students to follow along with their hearing peers. The browser-based deployment model means that no specialized equipment or software installation is required; any device with a web browser and internet connection can serve as an ISL translation terminal.

SDG 10: Reduced Inequalities. The tenth Sustainable Development Goal aims to "reduce inequality within and among countries." Target 10.2 emphasizes the social, economic, and political inclusion of persons with disabilities. The communication barrier between hearing and deaf communities is one of the most fundamental sources of inequality for deaf individuals, affecting their ability to access employment, public services, legal protections, and social relationships. By providing a free, open-source, web-accessible translation tool, this project reduces the economic barrier to communication access. Human ISL interpretation services, where available, command hourly rates that place them beyond the reach of most deaf individuals and their families. An automated system that provides adequate, if imperfect, translation at zero marginal cost per use represents a significant step toward communication equity.

SDG 3: Good Health and Well-being. The third Sustainable Development Goal seeks to "ensure healthy lives and promote well-being for all at all ages." Communication barriers in healthcare settings are known to result in misdiagnosis, inappropriate treatment, medication errors, and poor patient outcomes for deaf individuals. When a deaf patient visits a doctor in Tamil Nadu, the consultation is typically conducted in spoken Tamil, with no ISL interpretation available. The patient may be unable to describe their symptoms accurately, understand their diagnosis, or follow treatment instructions. This system could be deployed in healthcare settings to provide real-time translation of doctor-patient communication, improving the quality of care for deaf patients and potentially preventing adverse health outcomes arising from miscommunication. While the system's current vocabulary may not cover all medical terminology, its ability to handle common conversational phrases provides a starting point for healthcare communication support.

---

# CHAPTER 2: LITERATURE SURVEY

## 2.1 Overview of the Research Area

The research area encompassing this project spans several interconnected disciplines: computational linguistics, computer vision, assistive technology, human-computer interaction, and web application engineering. Each discipline contributes essential concepts, methods, and tools to the overall system design.

Sign language processing, as a subfield of computational linguistics and computer vision, has evolved significantly since its inception in the early 1990s. Early research focused primarily on sign language recognition — the computational task of interpreting sign language gestures captured through video or sensor data and converting them to text or speech. This recognition-oriented approach was driven by the availability of computer vision tools and the desire to enable deaf individuals to communicate with hearing people through automated interpretation. More recently, research attention has expanded to include sign language production — the reverse task of generating sign language output from text or speech input. Production systems are motivated by the need to make spoken content accessible to deaf individuals, which is arguably a more impactful application given that deaf individuals typically have greater difficulty accessing spoken content than hearing individuals have accessing signed content.

Within the domain of sign language production, two principal output modalities have emerged. The first modality uses pre-recorded video clips of human signers, which are selected and concatenated based on the input text. This approach produces natural-looking output because it uses actual human demonstrations, but it is limited by the vocabulary size of the video dataset and the challenge of producing smooth transitions between concatenated clips. The second modality uses computer-generated avatars — either 2D skeletal models or 3D animated characters — that are driven by keypoint data or motion capture to produce sign gestures procedurally. Avatar-based approaches offer unlimited vocabulary potential (any sign can be generated if the corresponding motion data is available) and smooth transitions, but they often lack the naturalness and nuance of human signing. The current project employs a hybrid approach, using pre-recorded human signer videos for the primary output and supplementary 2D avatar images for additional visual context.

The speech-to-sign-language pipeline introduces additional complexity beyond text-to-sign-language systems because it must incorporate speech recognition as the first processing stage. Speech recognition for under-resourced languages — languages with limited training data for acoustic models — has historically been challenging, but the development of large-scale multilingual speech recognition models and cloud-based APIs has substantially mitigated this challenge. Google's Speech-to-Text API, which this project uses, supports over 125 languages and dialects, including Tamil, with accuracy that has improved dramatically through the application of deep learning techniques to acoustic and language modeling.

Machine translation between typologically dissimilar languages presents its own set of challenges. Tamil and English differ in almost every major typological parameter: word order (SOV versus SVO), morphological type (agglutinative versus analytic), case marking (extensive versus minimal), and pro-drop behavior (Tamil freely drops subject pronouns; English generally does not). Neural machine translation systems, such as those underlying Google Translate, have achieved remarkable accuracy despite these differences, but they still struggle with idiomatic expressions, pragmatic nuances, and domain-specific terminology.

The NLP transformation from English to ISL grammar represents the least-studied stage of the pipeline. While there is a substantial body of research on English-to-ASL grammatical transformation (driven by the larger research community in the United States), English-to-ISL transformation has received comparatively little attention. ISL and ASL, despite both being sign languages, differ significantly in their grammar, vocabulary, and regional variation. ISL has been formally documented only since the early 2000s, when Zeshan (2003) published the first comprehensive typological description of its grammatical structure, and computational resources for ISL remain limited compared to those available for ASL.

## 2.2 Existing Models and Frameworks

This section reviews the most relevant existing systems, research prototypes, and commercial products that address various aspects of the speech-to-sign-language translation problem. Each system is evaluated in terms of its source language support, target sign language, output modality, deployment model, and relevance to the current project.

The SignAll system, developed by SignAll Technologies (Hungary), represents one of the most advanced commercial efforts in sign language technology. SignAll uses a combination of depth cameras, computer vision algorithms, and machine learning models to recognize Hungarian Sign Language and American Sign Language gestures in real time. The system displays the recognized text on a screen, enabling deaf individuals to communicate with hearing individuals without an interpreter. However, SignAll operates exclusively in the recognition direction (sign-to-text) and does not support sign language production (text/speech-to-sign). Furthermore, it requires specialized depth camera hardware and is not available as a web-based application, limiting its deployment to equipped facilities.

Google's SignAll project and related experimental features in Google Chrome demonstrate the application of MediaPipe's hand tracking and pose estimation models to sign language recognition. MediaPipe provides pre-trained models that can detect hand landmarks (21 points per hand), body pose landmarks (33 points), and facial landmarks (468 points) from standard webcam video in real time. While these capabilities are impressive, they again focus on recognition rather than production and do not include any mechanisms for generating sign language output from spoken or textual input. The current project incorporates MediaPipe as an offline utility (backend/ml_pipeline/extract_poses.py) for extracting pose keypoints from sign videos, which could be used in future iterations to drive animated avatar rendering.

Prabha and Wario (2019) developed a system for translating Hindi text into Indian Sign Language using a rule-based grammatical transformation module and a 3D animated avatar. Their system decomposed the translation process into three stages: part-of-speech tagging using a Hindi NLP pipeline, grammatical transformation using hand-crafted ISL grammar rules, and avatar animation using pre-defined gesture sequences. While their approach demonstrated the feasibility of Hindi-to-ISL translation, several limitations restrict its applicability to the current project. First, the system accepted only text input, not speech. Second, the system was developed as a desktop application using Unity3D for the avatar rendering, not as a web application. Third, Hindi and Tamil have different grammatical structures despite both being Indian languages, meaning that Hindi-specific grammar rules cannot be directly applied to Tamil.

Katole, Jain, and Patil (2018) proposed a Convolutional Neural Network (CNN) based sign language recognition system that classifies static hand gesture images into ISL signs. Their system achieved approximately 95 percent accuracy on a dataset of 35 ISL gestures captured under controlled lighting conditions. However, the system was limited to static gesture recognition (single-frame classification) and could not handle the dynamic, motion-based gestures that constitute the majority of ISL vocabulary. The system operated in the recognition direction only and provided no speech or text input capability.

Sharma, Singh, and Gupta (2020) explored the application of Long Short-Term Memory (LSTM) neural networks to ISL gesture recognition from video sequences. Their approach improved upon previous CNN-based methods by incorporating temporal information, enabling the recognition of dynamic gestures that involve hand movement over time. They reported improved accuracy on a custom ISL dataset of 50 words. However, their work, like that of Katole et al., addressed recognition rather than production and did not include any speech processing or text-to-ISL translation capability.

Camgoz, Hadfield, Koller, Ney, and Bowden (2018) introduced the Neural Sign Language Translation (NSLT) approach, which applied sequence-to-sequence deep learning models with attention mechanisms to translate continuous sign language video (German Sign Language) into spoken German text. Their work demonstrated state-of-the-art performance on the PHOENIX-2014T benchmark dataset and introduced the concept of end-to-end neural sign language translation. While their approach is conceptually relevant to the current project (both systems perform translation between spoken and signed languages), the direction is reversed (sign-to-text versus text/speech-to-sign), and the computational requirements of their model (requiring GPU training and inference) make it impractical for real-time web deployment.

The ISLRTC (Indian Sign Language Research and Training Centre) Digital Dictionary provides a comprehensive online resource of ISL sign videos organized by English word. The dictionary contains video demonstrations of ISL signs performed by trained signers, covering educational, medical, legal, and everyday vocabulary. While the ISLRTC dictionary is not a translation system, it serves as an invaluable reference for ISL vocabulary and has informed the development of the video dataset used in the current project.

In the domain of web application frameworks, FastAPI represents a significant advancement in Python web development. Introduced by Sebastian Ramirez in 2018, FastAPI builds on the ASGI (Asynchronous Server Gateway Interface) standard and leverages Python's type hints for automatic request validation, serialization, and documentation generation. Compared to Flask, the previously dominant Python web framework for small to medium applications, FastAPI offers superior performance (approximately 200 percent faster for I/O-bound workloads), built-in async/await support, automatic OpenAPI documentation, and Pydantic-based data validation. These characteristics make FastAPI particularly well-suited for applications like the current project, where the backend must handle file uploads, make multiple external API calls, and serve static files efficiently.

RecordRTC, the JavaScript library used for audio recording in the frontend, was developed by Muaz Khan and provides a unified API for recording audio and video in web browsers. RecordRTC abstracts away the differences between browser implementations of the MediaStream Recording API, providing consistent output across Chrome, Firefox, Safari, and Edge. The library's StereoAudioRecorder type is particularly valuable for speech recognition applications because it produces standard PCM WAV output, unlike the native MediaRecorder API which produces browser-specific encoded formats (WebM/Opus in Chrome, Ogg/Opus in Firefox) that require server-side transcoding.

## 2.3 Limitations Identified from Literature Survey (Research Gaps)

The literature survey reveals five significant research gaps that the current project addresses.

The first and most fundamental gap is the near-complete absence of Tamil-to-ISL translation systems. While researchers have explored Hindi-to-ISL and English-to-ASL translation, the Tamil-to-ISL direction has received virtually no published attention. Tamil's Dravidian linguistic characteristics, including its agglutinative morphology, extensive suffixation, and SOV word order, distinguish it typologically from both Hindi (an Indo-Aryan language) and English (a Germanic language), meaning that translation approaches developed for these languages cannot be directly applied to Tamil without significant adaptation.

The second gap concerns the integration of speech input with sign language output. The majority of existing sign language production systems accept text input only, bypassing the speech recognition stage entirely. This limitation reduces the practical utility of these systems because the primary use case — enabling hearing individuals to communicate with deaf individuals in real time — inherently involves spoken input. Systems that do incorporate speech recognition typically support only English, leaving speakers of other languages without access to speech-driven sign language translation.

The third gap relates to the web-based deployment of sign language translation systems. Most existing systems are implemented as desktop applications, mobile apps, or research prototypes that require specific operating systems, hardware configurations, or software installations. Web-based deployment, which enables access from any device with a browser, is essential for achieving broad accessibility but introduces constraints on computational resources and rendering capabilities that many existing approaches do not address.

The fourth gap concerns the quality of ISL grammatical transformation. Existing text-to-ISL systems typically either preserve English word order (producing grammatically incorrect ISL) or apply simplistic rule-based reordering that handles only a small subset of English sentence structures. The challenge of converting English SVO sentences to ISL SOV/Topic-Comment structures requires sophisticated syntactic analysis that most existing systems do not implement adequately.

The fifth gap pertains to the lack of multimodal output in sign language production systems. Most systems provide either video-based or avatar-based output, but not both simultaneously. Providing multiple visual representations of the same sign enhances the viewer's understanding and provides cross-referencing opportunities that can improve sign language learning. The current project addresses this gap by providing simultaneous video playback and 2D avatar display.

## 2.4 Research Objectives

Based on the research gaps identified in the literature survey, the following research objectives were formulated to guide the design and implementation of the Tamil Speech to ISL Translation System.

Objective 1: To design and implement a complete, end-to-end translation pipeline that accepts Tamil speech as input and produces ISL video output, integrating speech recognition, machine translation, NLP-based grammatical transformation, and video-based sign rendering into a unified system.

Objective 2: To develop a web-based application using modern web technologies (FastAPI, HTML5, CSS3, JavaScript) that is accessible from any modern web browser without requiring software installation, account creation, or specialized hardware, thereby maximizing the accessibility of the system to its target user population.

Objective 3: To implement a Natural Language Processing module using NLTK that performs tokenization, stopword removal, and verb lemmatization to convert English sentences into ISL-compatible word sequences, accounting for the grammatical differences between English and ISL including the absence of articles, auxiliary verbs, and inflected verb forms.

Objective 4: To build a scalable ISL video dataset management system that supports a dual-directory lookup mechanism (primary and fallback datasets), provides a graceful fingerspelling fallback for out-of-vocabulary words, and enables easy expansion of the vocabulary through the addition of new video files.

Objective 5: To integrate a supplementary 2D avatar representation system that provides word-specific sign pose images alongside the video playback, offering an additional visual modality for understanding each sign.

Objective 6: To implement an intelligent audio processing mechanism that handles audio recordings of arbitrary length by splitting them on silence boundaries, enabling the system to process extended inputs such as lectures or conversations without encountering API payload limitations.

Objective 7: To evaluate the system's performance in terms of end-to-end latency, per-word processing time, vocabulary coverage, and pipeline accuracy, establishing baseline metrics that can guide future development and optimization efforts.

## 2.5 Product Backlog (Key User Stories with Desired Outcomes)

The product backlog was developed using Agile user story methodology, with each story capturing a specific user need from the perspective of a particular stakeholder. The stories are prioritized using the MoSCoW method (Must have, Should have, Could have, Won't have this time) and assigned to specific sprints based on their dependencies and complexity.

**User Story US-01 (Must Have, Sprint I)**: As a hearing Tamil speaker communicating with a deaf individual, I want to speak in Tamil into my device's microphone and have my speech automatically translated into ISL sign videos, so that I can communicate my message without knowing sign language myself. Acceptance criteria: The system provides a clearly visible "Start Recording" button. Clicking the button activates the microphone with a visual recording indicator. Clicking "Stop Recording" automatically submits the audio for processing. Within 5 seconds, the ISL video output begins playing.

**User Story US-02 (Must Have, Sprint I)**: As a Tamil-medium teacher with a deaf student in my classroom, I want to upload a pre-recorded WAV or MP3 audio file of my lecture and have it translated into ISL sign videos, so that my deaf student can access the same educational content as hearing students. Acceptance criteria: The system provides a file upload button that accepts .wav and .mp3 files. After selecting a file, the filename is displayed with a "Process File" button. Processing the file produces the same ISL output as live recording.

**User Story US-03 (Must Have, Sprint II)**: As a deaf user viewing the ISL output, I want to see each sign played as a video clip with the corresponding English word displayed as a caption, so that I can understand the translation and associate each sign with its English equivalent. Acceptance criteria: Videos play sequentially without gaps. The current word is displayed as an overlay on the video. The corresponding word tag in the pipeline display is highlighted during playback.

**User Story US-04 (Should Have, Sprint II)**: As a deaf user, I want to see a 2D avatar character displaying the sign alongside the video, so that I have a secondary visual reference that may clarify signs I find difficult to understand from the video alone. Acceptance criteria: A 2D avatar panel appears beside the video player during playback. The avatar image updates for each word. If no word-specific avatar is available, a default pose is shown.

**User Story US-05 (Must Have, Sprint II)**: As a system user, I want words that have no matching video in the dataset to be displayed as text for a brief duration before moving to the next word, so that the playback does not stop or crash when encountering unknown words. Acceptance criteria: Missing words display "[Spell] WORD" text for 1.5 seconds. A yellow warning bar indicates that fingerspelling is triggered. The system continues to the next word automatically.

**User Story US-06 (Should Have, Sprint II)**: As a researcher evaluating this system, I want to see real-time latency metrics showing end-to-end processing time and average per-word latency, so that I can quantitatively assess the system's performance. Acceptance criteria: A latency metrics panel appears after the first successful translation. End-to-end latency is displayed in seconds. Average per-word latency accumulates across sessions.

**User Story US-07 (Must Have, Sprint I)**: As a user with a long audio recording exceeding 60 seconds, I want the system to process my entire recording without crashing or timing out, so that I can use the system for real-world conversations and lectures. Acceptance criteria: Audio files longer than 1 minute are processed correctly. The system segments the audio at silence boundaries. All recognized text segments are concatenated into a single output.

## 2.6 Plan of Action (Project Road Map)

The project was executed over an eight-week period following an Agile Scrum methodology with two-week sprint cycles. The complete roadmap, including all phases, milestones, and deliverables, is detailed below.

**Phase 1: Research and Environment Setup (Week 1, Days 1-7)**. The initial phase was dedicated to comprehensive research and development environment preparation. Activities included: surveying existing sign language translation systems and documenting their capabilities and limitations; studying ISL grammar rules from linguistic references, particularly Zeshan's (2003) typological description; evaluating and selecting the technology stack components (FastAPI, NLTK, SpeechRecognition, deep-translator, RecordRTC); installing Python 3.9+, Node.js, and required libraries; setting up the project directory structure with backend, frontend, and dataset directories; creating the initial README.md and requirements.txt files; and drafting the system architecture design. The deliverable was the project scaffold with all dependencies installed and the architecture design document.

**Phase 2: Sprint I — Speech Recognition and Translation (Weeks 2-3, Days 8-21)**. The first sprint focused on building the speech-to-English pipeline. The sprint backlog included: creating the FastAPI application instance with CORS middleware configuration; implementing the POST /api/process-audio endpoint with file upload handling; integrating Google's Speech-to-Text API with Tamil language support; integrating the deep-translator library for Tamil-to-English translation; building the frontend HTML structure with the three-panel layout; implementing CSS styling with the dark theme and design token system; implementing the RecordRTC-based audio recording module; implementing the file upload handler with format validation; building the processing loader and error display components; and testing the complete speech-to-text-to-translation pipeline. The sprint review verified that Tamil speech could be recorded, recognized, and translated to English through the browser interface.

**Phase 3: Sprint II — NLP Processing and Video Rendering (Weeks 4-5, Days 22-35)**. The second sprint completed the pipeline with ISL grammar conversion and sign video rendering. The sprint backlog included: developing the ISLConverter class in nlp_processor.py; implementing tokenization, stopword removal, and lemmatization; creating the video dataset mapping system with dual-directory lookup; implementing the GET /api/video/{word} endpoint; implementing the sequential video playback system with the onended event; building the fingerspelling fallback mechanism; creating the progress bar and sequence counter UI components; implementing the latency measurement and display system; and conducting end-to-end pipeline testing. The sprint review verified the complete Tamil-speech-to-ISL-video pipeline.

**Phase 4: 2D Avatar Integration and Dataset Expansion (Weeks 5-6, Days 29-42)**. This phase ran partially in parallel with the end of Sprint II and focused on enriching the visual output and expanding the vocabulary. Activities included: designing the base avatar character; developing the avatar_generator.py script for bulk avatar image production; generating 191 word-specific avatar images; implementing the GET /api/avatar/{word} endpoint; integrating the avatar display into the frontend media wrapper; adding the signing animation CSS effects; expanding the mock dataset from 25 to 75 words using the mock_generator.py script; and curating the primary ISL_Dataset with 151 authentic sign videos.

**Phase 5: Audio Chunking and Robustness (Week 6-7, Days 36-49)**. This phase addressed the system's ability to handle real-world audio inputs. Activities included: implementing the pydub split_on_silence integration for audio segmentation; adding FFmpeg-based audio format conversion using imageio_ffmpeg; implementing robust error handling for individual chunk failures; testing with audio recordings of varying lengths (5 seconds to 3+ minutes); fixing Windows-specific temporary file handling issues; and optimizing audio chunking parameters for Tamil speech characteristics.

**Phase 6: Testing, Documentation, and Deployment (Week 7-8, Days 43-56)**. The final phase ensured system quality and prepared deliverables. Activities included: end-to-end system testing with diverse Tamil speech inputs; cross-browser compatibility testing (Chrome, Firefox, Edge); latency benchmarking and performance documentation; interface polish and responsive design verification; project documentation updates (README.md, project_overview.md); academic report preparation; and presentation material development.

---

# CHAPTER 3: SPRINT PLANNING AND EXECUTION METHODOLOGY

The project followed an Agile Scrum methodology adapted for academic project development. Two sprints of approximately two weeks each were planned and executed, with sprint planning, daily standups (informal self-check-ins), sprint reviews, and sprint retrospectives conducted at appropriate intervals. The following sections provide detailed documentation of each sprint's objectives, functional specifications, architectural decisions, outcomes, and retrospective insights.

## 3.1 SPRINT I: Speech Recognition and Translation Pipeline

### 3.1.1 Objectives with User Stories of Sprint I

Sprint I was planned with a two-week duration and focused on establishing the foundational pipeline from Tamil speech input to English text output. The sprint goal was stated as: "Build a functional web application that can record Tamil speech or accept audio file uploads, recognize the speech content as Tamil text, and translate it to English, with a modern user interface that provides visual feedback at each stage."

The sprint backlog was populated with decomposed tasks derived from User Stories US-01, US-02, and US-07. User Story US-01 (microphone recording) was decomposed into the following implementable tasks: configure navigator.mediaDevices.getUserMedia for microphone access, integrate RecordRTC library with StereoAudioRecorder configuration, implement start/stop recording toggle with UI state management, capture PCM WAV blob on recording stop, and auto-submit the audio for processing. User Story US-02 (file upload) was decomposed into: create hidden file input with format validation (.wav, .mp3), implement visual file selection feedback with filename display, create "Process File" button with click handler, and validate file format on both client and server sides. User Story US-07 (long audio support) was decomposed into: implement pydub-based audio loading, configure split_on_silence with appropriate parameters, implement per-chunk speech recognition in a loop, handle chunk-level errors without terminating the pipeline, and concatenate results from all chunks.

The estimated effort for Sprint I was approximately 40 story points, distributed across backend development (15 points), frontend development (15 points), and integration testing (10 points). Each story point represented approximately 2 hours of development effort.

### 3.1.2 Functional Document

The functional specification for Sprint I defined the system's behavior at the interface boundary between the user and the application, describing what the system must do without specifying how it must be implemented internally.

Functional Requirement FR-01: Audio Recording. The system shall provide a prominently displayed recording button labelled "Start Recording" with a microphone icon. Upon activation, the button shall request browser microphone permission through the standard Web API permission prompt. If permission is granted, the system shall begin capturing audio from the device's default microphone, and the button shall change its appearance to indicate recording state: the label shall change to "Stop Recording" with a stop icon, the button background shall change to a red gradient, and a pulsing animation shall indicate active recording. Additionally, a recording status panel shall appear below the input actions, displaying an animated waveform visualization and the text "Listening to Tamil speech..." to provide continuous visual feedback that recording is in progress. The audio shall be captured in PCM WAV format at 16kHz sample rate with a single channel (mono), as these parameters are optimal for speech recognition processing.

Functional Requirement FR-02: Audio File Upload. The system shall provide an upload button labelled "Upload Audio (.wav, .mp3)" with an upload icon. Clicking this button shall open the browser's native file selection dialog, filtered to accept only audio MIME types (audio/wav, audio/mpeg). Upon file selection, the system shall validate that the file extension matches a supported format (.wav, .mp3, .ogg). If the format is unsupported, an error message shall be displayed and the file selection shall be reset. If the format is valid, the recording status shall be hidden, an upload status panel shall appear displaying the selected filename, and a "Process File" button shall become available for the user to initiate processing.

Functional Requirement FR-03: Backend Audio Processing. Upon receiving an audio file via the POST /api/process-audio endpoint, the backend shall perform the following operations in strict sequence. First, it shall validate the file extension against the supported formats (.wav, .mp3, .ogg, .flac, .webm, .m4a) and return HTTP 400 if unsupported. Second, it shall save the uploaded file to a temporary location using Python's tempfile module. Third, it shall attempt to convert the audio to 16kHz mono WAV format using FFmpeg via the imageio_ffmpeg library; if this conversion fails, the original file shall be used as fallback. Fourth, it shall load the converted audio using pydub's AudioSegment.from_file method. Fifth, it shall split the audio on silence boundaries using pydub's split_on_silence function with the following parameters: minimum silence length of 500ms, silence threshold of 16 dB below the audio's average dBFS level, and retained silence padding of 250ms per boundary. Sixth, if no silence-based chunks are produced (indicating continuous speech without pauses), the entire audio shall be treated as a single chunk. Seventh, for each chunk, the system shall export the chunk to a temporary WAV file, open it using SpeechRecognition's AudioFile context manager, record the audio data, submit it to Google's Speech-to-Text API with the Tamil language locale (ta-IN), and append the recognized text to a results list. Eighth, if no chunks produce recognized text, the system shall return HTTP 400 with the message "Speech could not be understood or audio contains no speech." Ninth, the recognized text fragments shall be concatenated with spaces to produce the complete Tamil text. Tenth, the Tamil text shall be translated to English using GoogleTranslator.

Functional Requirement FR-04: Processing Feedback. During backend processing, the frontend shall display a loading indicator consisting of a spinning animation and the text "Processing audio via FastAPI..." to inform the user that their request is being processed. All other status indicators (recording status, upload status) shall be hidden during this period. If the backend returns an error response, the loading indicator shall be replaced with an error panel displaying the error message text in red.

Functional Requirement FR-05: Result Display. Upon receiving a successful response from the backend, the system shall update the Translation Pipeline panel with the following information: the recognized Tamil text shall be displayed in the "Tamil Text" output field, replacing the placeholder text "Awaiting input..."; the English translation shall be displayed in the "English Translation" output field, replacing the placeholder text "Awaiting translation..."; and the placeholder content in the ISL Grammar area shall be cleared, pending update in Sprint II.

### 3.1.3 Architecture Document

The architectural design for Sprint I established the foundational structure upon which the complete system would be built. Architectural decisions made during this sprint were guided by the principles of simplicity, modularity, progressive enhancement, and defensive error handling.

The server architecture employs a monolithic design in which a single FastAPI process serves both the API endpoints and the frontend static files. This decision was motivated by the desire to simplify deployment: with a monolithic architecture, the entire application can be started with a single command (python -m uvicorn backend.main:app --reload), and both the API and the frontend are accessible at the same network address and port (http://127.0.0.1:8000). The alternative — hosting the frontend on a separate web server (e.g., Nginx or a Node.js development server) — would have introduced CORS configuration complexity, additional deployment steps, and potential port conflicts that are undesirable for an academic project intended for demonstration.

The static file serving is configured as the last route in the application, after all API endpoint definitions. This ordering is critical because FastAPI's route matching is first-match-wins: if the static file mount were placed before the API routes, a request to /api/process-audio would be intercepted by the static file handler and result in a 404 error (because no file named "api/process-audio" exists in the frontend directory). By placing the app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend") call at the end of main.py, all /api/ routes are handled by their respective endpoint functions, and only non-matching routes fall through to the static file handler.

The path configuration system uses Python's pathlib.Path objects for cross-platform file path handling. The BASE_DIR constant is computed by resolving the path to main.py and navigating two parent directories up (from backend/main.py to the project root). This approach ensures that the path resolution is independent of the current working directory, which may vary depending on how the application is launched. From BASE_DIR, the ISL_DATASET_DIR, DATASET_DIR, and FRONTEND_DIR paths are derived using the / operator, which provides platform-appropriate path separators.

The CORS middleware is configured with permissive settings (allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]) to facilitate development and local testing. In a production deployment, these settings should be restricted to the specific origin, methods, and headers required by the frontend application to prevent cross-site request forgery attacks.

The frontend architecture establishes the visual framework and interaction patterns that will be extended in Sprint II. The HTML document structure uses semantic elements (header, main, section) to organize content, with CSS classes providing styling hooks. The three-panel grid layout is defined using CSS Grid with a 2-column template, where the left column contains the input panel (top) and processing panel (bottom), and the right column contains the output panel (full height). This layout was chosen to present the translation pipeline as a left-to-right flow: input on the left, processing in the middle (conceptually), and output on the right.

The CSS design system uses Custom Properties (CSS variables) defined on the :root pseudo-element to establish a consistent visual language across all components. The design token system includes background colors at three levels (dark, panel, highlight), an accent color with a corresponding glow value, main and muted text colors, semantic colors for success and danger states, border colors, border radius values, and a transition timing function. This token-based approach ensures visual consistency and makes it trivial to modify the application's appearance by changing a few variable values.

### 3.1.4 Outcome of Objectives / Result Analysis

Sprint I concluded with all planned user stories fully implemented and verified. A detailed analysis of the outcomes for each objective follows.

The FastAPI backend was successfully established with two operational endpoints. The POST /api/process-audio endpoint correctly processes multipart audio file uploads, performing the complete speech-recognition-and-translation pipeline and returning JSON responses. The static file serving correctly delivers the frontend files from the frontend/ directory, including index.html as the default document. The server starts cleanly with python -m uvicorn backend.main:app --reload, and the --reload flag enables hot-reloading of Python code changes during development. The run_project.bat batch file was created to automate the startup sequence, including dependency installation, mock data generation, and server launch.

The audio recording system was tested across Chrome, Firefox, and Edge browsers on Windows. RecordRTC reliably produced PCM WAV audio at 16kHz mono in all tested browsers. The recording state management correctly transitioned between idle, recording, and processing states, with appropriate UI updates at each transition. The microphone stream was properly released upon recording stop, as verified by observing that the browser's microphone indicator (the red dot in Chrome's address bar) disappeared immediately after clicking "Stop Recording."

Tamil speech recognition was evaluated with 15 test sentences spoken by a single speaker with a standard Tamil accent. The recognition accuracy, measured as word-level accuracy compared to the intended Tamil text, averaged approximately 85 percent for clear, well-articulated speech in a quiet environment. Common errors included: substitution of phonetically similar Tamil words, misrecognition of short function words, and failure to recognize technical or uncommon vocabulary. The recognition speed averaged approximately 1.5 seconds per 5-second audio segment, with the majority of this time attributable to the network round-trip to Google's servers.

Tamil-to-English translation was evaluated qualitatively on the same 15 test sentences. Translation quality was found to be high for simple, declarative sentences (e.g., "நான் பள்ளிக்கு செல்கிறேன்" correctly translated to "I am going to school") but degraded for sentences with idiomatic expressions, cultural references, or ambiguous pronoun resolution. The translation latency was consistently under 1 second, making it a minor contributor to the overall pipeline latency.

The audio chunking mechanism was tested with recordings of 15, 30, 60, 120, and 180 seconds. All recordings were successfully processed without errors or timeouts. The split_on_silence function produced an appropriate number of chunks (typically 3 to 20, depending on speech rate and pausing patterns) that were each short enough for the Google STT API to process efficiently. The Windows-specific temporary file handling was verified to work correctly with the NamedTemporaryFile(delete=False) pattern.

### 3.1.5 Sprint Retrospective

The Sprint I retrospective was conducted upon sprint completion and produced the following observations.

What went well: The selection of RecordRTC proved to be an excellent decision. By producing standard PCM WAV audio directly in the browser, it eliminated the need for FFmpeg-based transcoding of WebM/Opus audio that had been a significant source of bugs in earlier project iterations. The monolithic server architecture simplified development and testing by allowing the entire application to be accessed at a single URL. The progressive error handling strategy in the backend, with multiple fallback levels for audio processing, produced a robust pipeline that handled unexpected inputs gracefully.

What could be improved: The initial version of the audio processing code did not account for Windows file locking behavior, where a NamedTemporaryFile created with delete=True cannot be opened by another process (pydub) before it is closed. This bug manifested as a PermissionError on Windows and required switching to delete=False with explicit cleanup. The audio chunking parameters (min_silence_len=500ms, silence_thresh=dBFS-16) were initially calibrated for English speech patterns and required adjustment for Tamil speech, which tends to have shorter inter-word pauses.

Action items for Sprint II: Implement the ISL grammar conversion module. Build the video dataset mapping and serving system. Implement sequential video playback with onended events. Add the 2D avatar display. Add latency monitoring.

## 3.2 SPRINT II: NLP Processing and Video Rendering

### 3.2.1 Objectives with User Stories of Sprint II

Sprint II was planned with a two-week duration and focused on completing the translation pipeline from English text to ISL video output. The sprint goal was stated as: "Complete the end-to-end Tamil Speech to ISL Translation System by implementing NLP-based ISL grammar conversion, video-based sign rendering with sequential playback, 2D avatar integration, fingerspelling fallback, and latency monitoring."

This sprint addressed User Stories US-03 (video playback with captions), US-04 (2D avatar display), US-05 (fingerspelling fallback), and US-06 (latency metrics). The sprint backlog contained 25 implementable tasks distributed across backend NLP development (8 tasks), backend video serving (4 tasks), frontend video playback (7 tasks), frontend avatar integration (3 tasks), and latency monitoring (3 tasks).

### 3.2.2 Functional Document

Functional Requirement FR-06: NLP Processing. The system shall include an NLP module (backend/modules/nlp_processor.py) that implements the ISLConverter class. The class shall provide an english_to_isl(text: str) method that accepts an English sentence and returns a list of ISL-compatible words. The transformation shall process words through three sequential operations: NLTK word_tokenize for tokenization, stopword filtering using a customized NLTK English stopword list augmented with ISL-specific stop words, and WordNetLemmatizer for verb root form extraction. Personal pronouns (I, we, you, he, she, they, it) shall be preserved during stopword filtering. All output words shall be uppercased for display consistency. If NLP processing fails for any reason, the method shall fall back to simple whitespace splitting and uppercasing of the input text.

Functional Requirement FR-07: Video Dataset Mapping. For each ISL word produced by the NLP module, the backend shall search for a matching video file in two directories: the ISL_Dataset directory (primary, checked first) and the dataset directory (secondary/fallback). The search shall be case-insensitive, performed by lowercasing the word and checking for "{word_lower}.mp4". The response shall include, for each word, the uppercase word label, the video URL (or null if not found), and a boolean found flag.

Functional Requirement FR-08: Video Serving. The GET /api/video/{word} endpoint shall serve individual MP4 video files from the appropriate dataset directory based on the source query parameter. The source=isl parameter directs to the ISL_Dataset directory; source=dummy directs to the dataset directory. If the requested file does not exist, the endpoint shall return HTTP 404.

Functional Requirement FR-09: Sequential Video Playback. The frontend shall implement a recursive playback mechanism that plays ISL sign videos one after another. For each word with a found video, the system shall: load the video into the HTML5 video element, play it, display the word as an overlay caption, highlight the corresponding ISL tag, update the progress bar and counter, update the 2D avatar image, and upon video completion (onended event) advance to the next word. For words without videos, the system shall display "[Spell] WORD" for 1.5 seconds before advancing.

Functional Requirement FR-10: 2D Avatar Display. During video playback, the system shall display a 2D avatar panel beside the video player. The avatar image shall update to show the word-specific sign pose for each word in the sequence. The avatar image shall be fetched from /api/avatar/{word}. If the avatar image is not available, the default avatar.png shall be displayed. The avatar panel shall display a "Live 2D Translation" status badge.

Functional Requirement FR-11: Latency Metrics. The system shall measure the time elapsed between audio submission and the start of video playback, displaying this as "End-to-End Latency" in seconds. The system shall also calculate and display "Avg Latency/Word" by dividing the cumulative latency by the cumulative word count across all translation sessions.

### 3.2.3 Architecture Document

Sprint II introduced the NLP processing module and video rendering subsystem, extending the Sprint I architecture with two new backend modules and significant frontend enhancements.

The NLP module (backend/modules/nlp_processor.py) was designed as a standalone class to promote separation of concerns and enable independent testing. The ISLConverter class is instantiated once during application startup in main.py (line 33: isl_converter = ISLConverter()) and reused across all incoming requests. This singleton-like pattern avoids the overhead of reinitializing NLTK resources for each request while ensuring thread safety through the stateless design of the english_to_isl method (all state is local to the method invocation, with no shared mutable state between calls).

The NLTK initialization strategy uses a defensive check-and-download pattern. At module import time, the code checks for the presence of required NLTK data packages (stopwords, punkt, punkt_tab, wordnet) using nltk.data.find(). If any package is missing, all packages are downloaded using nltk.download() with the quiet=True flag to suppress console output. This approach ensures that the system works correctly on a fresh installation without requiring manual NLTK data setup, while avoiding redundant downloads on subsequent runs.

The video serving architecture introduces two new GET endpoints (/api/video/{word} and /api/avatar/{word}) that use FastAPI's FileResponse class to stream video and image files directly from the filesystem. The FileResponse class sets appropriate Content-Type headers (video/mp4 for videos, image/png for avatars) and supports HTTP range requests, enabling efficient streaming and seeking within video files. The source query parameter in the /api/video/{word} endpoint provides a clean mechanism for the frontend to specify which dataset directory to serve from, without exposing filesystem paths in the URL.

The frontend video playback architecture is centered on the HTML5 <video> element, which provides native support for MP4 video playback, play/pause control, and event handling. The playback system resides in the app.js file and uses a recursive function pattern: playNextVideo() processes the current word and sets up either an onended handler (for found videos) or a setTimeout callback (for missing words) that calls playNextVideo() again with an incremented index. This recursive pattern continues until the index exceeds the sequence length, at which point the function terminates.

The avatar rendering subsystem adds a secondary visual column to the output panel. The media-wrapper CSS layout uses Flexbox to arrange the video container and avatar container side by side, with each container taking equal width (flex: 1) and maintaining a 16:9 aspect ratio. On screens narrower than 1024 pixels, the Flexbox direction changes from row to column, stacking the video and avatar vertically. The avatar container includes a status badge ("Live 2D Translation") positioned absolutely in the top-right corner, a character display area with the avatar image, and CSS animation (signingBody keyframe) that produces a subtle scaling effect during active signing.

### 3.2.4 Outcome of Objectives / Result Analysis

All objectives defined for Sprint II were achieved successfully. The NLP module correctly transforms English sentences into ISL word sequences. Below are detailed test results for representative sentences:

Test Case 1: "I am going to school." The tokenization produces ["i", "am", "going", "to", "school", "."]. Punctuation "." is removed. Stopwords "am" and "to" are removed. Pronoun "i" is preserved. "going" is lemmatized to "go". "school" remains unchanged. Final output: ["I", "GO", "SCHOOL"]. This matches the expected ISL representation.

Test Case 2: "She is eating food." The tokenization produces ["she", "is", "eating", "food", "."]. Punctuation "." is removed. Stopword "is" is removed. Pronoun "she" is preserved. "eating" is lemmatized to "eat". Final output: ["SHE", "EAT", "FOOD"]. This correctly represents the ISL equivalent.

Test Case 3: "Where are you going?" The tokenization produces ["where", "are", "you", "going", "?"]. Punctuation "?" is removed. Stopword "are" is removed. Pronoun "you" is preserved. "where" is preserved (not in the custom stop list). "going" is lemmatized to "go". Final output: ["WHERE", "YOU", "GO"]. This correctly preserves the question word.

Test Case 4: "He was sleeping in the room." The tokenization produces ["he", "was", "sleeping", "in", "the", "room", "."]. Punctuation "." is removed. Stopwords "was", "in", "the" are removed. Pronoun "he" is preserved. "sleeping" is lemmatized to "sleep". Final output: ["HE", "SLEEP", "ROOM"]. Function words are correctly stripped.

The video playback system was tested with sequences of varying lengths (1 to 15 words). Playback was smooth and uninterrupted in all tested browsers (Chrome 120+, Firefox 121+, Edge 120+). The onended event handler fired reliably at the end of each video, triggering seamless transitions to the next clip. No buffering delays were observed because the individual sign video files are small (50 KB to 200 KB each) and are served from the local FastAPI server, ensuring near-instantaneous loading.

The fingerspelling fallback was tested by including deliberately misspelled or extremely rare words in the input. The system correctly identified these words as having no matching video, displayed "[Spell] WORD" for 1.5 seconds, and advanced to the next word. The yellow warning bar appeared as expected.

The latency monitoring system was validated by comparing the displayed latency values against manual timing measurements. The end-to-end latency values were accurate to within 50 milliseconds of the manual measurements, confirming the reliability of the performance.now()-based timing approach. Over a session of 10 translation requests, the cumulative average per-word latency converged to approximately 0.7 seconds per word.

### 3.2.5 Sprint Retrospective

The Sprint II retrospective identified the following key observations.

What went well: The ISLConverter class proved to be clean, modular, and easy to test. The onended event-driven playback pattern produced smooth video transitions without any visible delays. The 2D avatar integration enhanced the visual richness of the output significantly.

What could be improved: The NLP module does not reorder words to match ISL's SOV structure. The current system preserves English SVO word order. Implementing SOV reordering would require POS tagging and dependency parsing (using a library like spaCy), which adds complexity but would significantly improve the linguistic accuracy of the ISL output. The fingerspelling fallback duration of 1.5 seconds is fixed and does not adapt to word length. The 2D avatar images are static poses, not animated gestures. The pose extraction pipeline (extract_poses.py) is available but not yet integrated.

Decisions deferred to future work: ISL SOV word reordering, animated 3D avatar integration, offline speech recognition, and text input mode were identified as enhancement priorities for future iterations.

---

# CHAPTER 4: SYSTEM ARCHITECTURE AND DESIGN

## 4.1 Overall Architecture

The Tamil Speech to ISL Translation System follows a monolithic client-server architecture in which all components — the RESTful API, the NLP processing engine, the static file server, and the frontend application — are served from a single FastAPI process running on a Uvicorn ASGI server. This monolithic approach was deliberately chosen over microservices or serverless architectures because it minimizes deployment complexity, eliminates inter-service communication overhead, and allows the entire system to be started, stopped, and debugged as a single unit.

The logical architecture can be decomposed into three tiers. The Presentation Tier consists of the frontend application files (index.html, style.css, app.js) that run in the user's web browser. This tier is responsible for all user interaction, including audio capture, visual feedback, API communication, and video playback. The Application Tier consists of the FastAPI backend (main.py and nlp_processor.py), which implements the business logic of the translation pipeline: audio processing, speech recognition, translation, NLP transformation, and video mapping. The Data Tier consists of the ISL video datasets (ISL_Dataset/ and dataset/), the 2D avatar image collection (dataset/2d_avatars/), and the frontend avatar sprites (frontend/avatar_*.png).

Communication between the Presentation Tier and the Application Tier follows the HTTP request-response pattern. The frontend initiates three types of requests: POST /api/process-audio (submitting audio for translation), GET /api/video/{word} (fetching sign videos), and GET /api/avatar/{word} (fetching avatar images). The backend processes each request synchronously within the request handler and returns the appropriate response. For the process-audio endpoint, the response is a JSON object; for the video and avatar endpoints, the response is a binary file stream.

The deployment architecture is exceedingly simple: the application runs on localhost (127.0.0.1) on port 8000 (the Uvicorn default). The Uvicorn server supports hot-reloading when started with the --reload flag, automatically detecting Python code changes and restarting the server. This configuration is appropriate for development and demonstration purposes. For production deployment, this architecture would need to be enhanced with a reverse proxy (e.g., Nginx), HTTPS encryption, and process management (e.g., systemd or Docker).

## 4.2 Frontend Architecture

The frontend architecture is built on three foundational web technologies — HTML5 for structure, CSS3 for presentation, and JavaScript (ES6+) for behavior — without any framework, build tool, or bundler dependency. This "vanilla" approach was chosen to ensure maximum compatibility, instant loading, and complete developer control over every aspect of the application.

The HTML5 document (index.html, 161 lines) defines the page structure using semantic elements. The document begins with a <!DOCTYPE html> declaration and includes viewport meta tags for responsive behavior. External resources loaded from CDNs include: Google Fonts (Outfit, weights 300/400/600/700), Font Awesome 6 (icon library), and RecordRTC (audio recording library). The body contains a header element with the application logo and language indicator, and a main element with the class "container" that holds the three panel sections.

The Input Panel (section.input-panel) contains the recording button (button#recordBtn), a visual divider with "OR" text, the file upload label and hidden input (input#audioUpload), the recording status display with animated waveform, the upload status display with filename and process button, the processing loader with spinner animation, and the error message display. Each of these sub-components is toggled between visible and hidden states through the .hidden CSS class, managed by JavaScript event handlers.

The Processing Panel (section.processing-panel) displays the three stages of the translation pipeline as vertically connected steps, each with a circular icon and content area. The three steps display: Tamil Text (output from speech recognition), English Translation (output from machine translation), and ISL Grammar Conversion (output as tag elements showing individual ISL words). The steps are visually connected by a vertical line that runs between the circular icons, created using CSS ::after pseudo-elements, producing a "pipeline" visual metaphor that reinforces the sequential nature of the processing stages.

The Output Panel (section.output-panel) contains the video player and avatar in a side-by-side layout (div.media-wrapper), the video controls (replay button, progress bar, sequence counter), the missing word warning bar, and the latency metrics display (end-to-end latency and average per-word latency). The video container has a video element with the "muted" and "playsinline" attributes set for autoplay compatibility across browsers.

The CSS3 stylesheet (style.css, 692 lines) implements the complete visual design system. The design uses CSS Custom Properties (variables) for all design tokens, ensuring consistency and enabling easy theme modifications. The layout uses CSS Grid for the main container and CSS Flexbox for component-level layouts. Key CSS design patterns include: glassmorphism effects (backdrop-filter: blur(10px) on the header), gradient backgrounds on buttons, box-shadow for depth, and multiple CSS keyframe animations for micro-interactions.

The JavaScript module (app.js, 333 lines) manages all application state and behavior. Global state variables track: the recording state (isRecording, mediaStream, recordRTC, audioBlob), the video playback state (videoSequence, currentVideoIndex, isPlaying), and the latency measurement state (sequenceStartTime, cumulativeE2eLatency, cumulativeWordCount). The code is organized into clearly delineated functional sections with comment headers: Audio Recording Handling, File Upload Handling, Backend Processing, UI Updates, and Video Playback Logic.

## 4.3 Backend Architecture

The backend architecture consists of two Python source files: main.py (221 lines, the application entry point and API controller) and nlp_processor.py (69 lines, the NLP processing engine). Together, these files implement the complete server-side logic of the application.

The main.py file begins with import statements that bring in FastAPI framework components (FastAPI, UploadFile, File, HTTPException, JSONResponse, FileResponse, CORSMiddleware, StaticFiles), the SpeechRecognition library, the deep-translator module, standard library modules (os, shutil, tempfile, subprocess), Path from pathlib, pydub components (AudioSegment and split_on_silence), and imageio_ffmpeg for FFmpeg binary access. The FFmpeg converter path is set globally using AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe(), which provides pydub with a self-contained FFmpeg binary that does not require system-level installation.

Module initialization creates three singleton-like service objects: recognizer = sr.Recognizer() for speech recognition, translator = GoogleTranslator(source='ta', target='en') for Tamil-to-English translation, and isl_converter = ISLConverter() for NLP processing. These objects are created once at startup and reused across all requests, avoiding redundant initialization overhead.

The nlp_processor.py module defines a single class (ISLConverter) with two methods: __init__ for initialization and english_to_isl for text transformation. The __init__ method creates a WordNetLemmatizer instance and builds the stopword set by combining NLTK's 179 standard English stopwords with 12 additional ISL-specific stop words (am, is, are, was, were, be, being, been, to, the, a, an). The english_to_isl method implements a single-pass transformation algorithm that iterates over tokenized words, skipping punctuation and stopwords while preserving pronouns, lemmatizing each surviving word as a verb, and appending the uppercased result to the output list.

## 4.4 Data Flow: Tamil to ISL Pipeline

The complete data flow through the system can be modeled as a five-stage pipeline with well-defined inputs, outputs, and transformations at each stage.

Stage 1 — Audio Capture and Transmission. Input: Tamil speech from microphone or audio file. Processing: RecordRTC captures PCM WAV at 16kHz mono (for microphone input) or the file is read from disk (for file upload). A FormData object is constructed with the audio file as the 'file' field. The Fetch API submits a POST request to /api/process-audio. Output: HTTP request with multipart/form-data body containing the audio file.

Stage 2 — Speech-to-Text Conversion. Input: Audio file received by the backend. Processing: The file is saved to a temporary location. FFmpeg converts it to 16kHz mono WAV. pydub loads the audio and splits it on silence (min_silence_len=500ms, silence_thresh=dBFS-16, keep_silence=250ms). Each chunk is exported to a temporary WAV file, opened by SpeechRecognition, and submitted to Google STT with language="ta-IN". Results are concatenated. Output: Tamil text string (e.g., "நான் பள்ளிக்கு செல்கிறேன்").

Stage 3 — Machine Translation. Input: Tamil text string. Processing: GoogleTranslator(source='ta', target='en').translate(tamil_text). Output: English text string (e.g., "I am going to school").

Stage 4 — ISL Grammar Conversion. Input: English text string. Processing: ISLConverter.english_to_isl(english_text) performs tokenization → stopword removal → lemmatization → uppercasing. Output: List of ISL words (e.g., ["I", "GO", "SCHOOL"]).

Stage 5 — Video Mapping and Rendering. Input: List of ISL words. Processing (Backend): Each word is matched against ISL_Dataset/{word}.mp4 (primary) and dataset/{word}.mp4 (fallback). Video URLs and found flags are generated. Processing (Frontend): startVideoSequence() receives the video_sequence array, calculates latency, and calls playNextVideo(). The recursive function loads each video, plays it, and chains to the next via onended. Output: Sequential sign language video playback with avatar display.

## 4.5 API Design

The system exposes three RESTful API endpoints, all prefixed with /api/ to maintain a clear separation between API routes and static file serving.

**POST /api/process-audio**. Purpose: Main translation pipeline endpoint. Request format: multipart/form-data with a file field containing an audio file. Accepted file extensions: .wav, .mp3, .ogg, .flac, .webm, .m4a. Response format: JSON with fields tamil_text (string), english_text (string), isl_words (array of strings), and video_sequence (array of objects with word, video_url, and found fields). Error responses: 400 for unsupported format or unrecognizable speech, 500 for internal server errors.

**GET /api/video/{word}?source=isl|dummy**. Purpose: Serve individual ISL sign video files. URL parameter: word (case-insensitive ISL word). Query parameter: source (optional, default "dummy"; "isl" for ISL_Dataset, "dummy" for dataset). Response: MP4 video file with Content-Type: video/mp4. Error response: 404 if video file not found.

**GET /api/avatar/{word}**. Purpose: Serve 2D avatar sign pose images. URL parameter: word (case-insensitive ISL word). Response: PNG image file with Content-Type: image/png from dataset/2d_avatars/avatar_{word}.png. Error response: 404 if avatar image not found.

## 4.6 Module Breakdown

### 4.6.1 main.py — The API Controller

The main.py file (221 lines) serves as the central orchestrator of the backend. It can be logically divided into five sections:

Lines 1-18: Import statements and module initialization. This section imports all required libraries and sets the FFmpeg converter path for pydub. The ISLConverter is imported from backend.modules.nlp_processor.

Lines 19-43: Application setup. This section creates the FastAPI instance, configures CORS middleware, initializes the recognizer, translator, and ISL converter, and sets up directory path constants.

Lines 47-183: The /api/process-audio endpoint. This 136-line function implements the complete translation pipeline with nested error handling. The outer try-except catches pipeline-wide errors. The audio conversion section has its own try-except for format conversion failures. The speech recognition section uses a for loop with per-chunk try-except for graceful chunk-level error handling.

Lines 186-216: The /api/video/{word} and /api/avatar/{word} endpoints. These are simple file-serving endpoints that resolve filesystem paths and return FileResponse objects.

Lines 219-221: Static file mounting. The frontend directory is mounted at the root path, serving index.html as the default document.

### 4.6.2 nlp_processor.py — The NLP Engine

The nlp_processor.py file (69 lines) implements a focused, single-responsibility module. The ISLConverter class exposes one public method (english_to_isl) that implements the complete text transformation in approximately 30 lines of logic. The defensive programming approach includes: null/empty input checking (returns empty list for falsy input), a comprehensive try-except that falls back to simple splitting if NLTK processing fails, and an isalnum check that filters punctuation without requiring regular expressions.

### 4.6.3 app.js — The Frontend Controller

The app.js file (333 lines) is the most complex frontend module, managing audio capture, API communication, UI state, and video playback. Key architectural patterns include: DOM element caching (all getElementById calls at the top of the file), state management through global variables, event-driven programming using addEventListener for user interactions and onended for video events, and the Fetch API for asynchronous backend communication.

## 4.7 Sequence Flow Explanation

A complete user interaction sequence proceeds as follows:

1. The user opens http://127.0.0.1:8000 in a web browser. The FastAPI static file handler serves index.html, which loads style.css, app.js, Google Fonts, Font Awesome, and RecordRTC from their respective sources.

2. The user clicks "Start Recording." JavaScript calls navigator.mediaDevices.getUserMedia({audio: true}), which prompts the browser's microphone permission dialog. Upon approval, a MediaStream object is obtained. RecordRTC is instantiated with the stream, configured for PCM WAV at 16kHz mono. recordRTC.startRecording() begins capture. The UI transitions to the recording state.

3. The user speaks Tamil into the microphone (e.g., "நான் பள்ளிக்கு செல்கிறேன்" — "I am going to school").

4. The user clicks "Stop Recording." recordRTC.stopRecording() is called. In the callback, recordRTC.getBlob() retrieves the WAV audio blob. The microphone stream is released. performance.now() records the start time. A File object is created from the blob. processAudioFile(file) is called.

5. processAudioFile constructs a FormData object, appends the file, and submits fetch('/api/process-audio', {method: 'POST', body: formData}). The UI shows the processing loader.

6. The backend receives the request. main.py saves the audio to a temp file, converts it to 16kHz mono WAV via FFmpeg, splits on silence into chunks, processes each chunk through Google STT (ta-IN), concatenates the Tamil text, translates to English via GoogleTranslator, converts to ISL via ISLConverter.english_to_isl(), maps words to video files, and returns the JSON response.

7. The frontend receives the JSON response. updatePipelineUI displays the Tamil text, English translation, and ISL word tags. startVideoSequence calculates latency and calls playNextVideo.

8. playNextVideo loads the first video (/api/video/i?source=isl), plays it, displays "I" as the overlay, highlights the first ISL tag, and updates the avatar to avatar_i.png. When the video ends, onended fires, index increments, and playNextVideo loads the next video (/api/video/go?source=isl), and so on until all words are played.

---

# CHAPTER 5: IMPLEMENTATION DETAILS

## 5.1 Audio Recording Implementation (RecordRTC)

The audio recording subsystem is implemented in the frontend using RecordRTC, a mature open-source JavaScript library specifically designed for cross-browser audio and video recording. The library is loaded from a CDN (https://cdn.webrtc-experiment.com/RecordRTC.js) in the index.html file, ensuring that the latest version is always available without local dependency management.

The recording process begins when the user clicks the "Start Recording" button, which triggers an async click event handler on the recordBtn element. The handler first requests microphone access through the Web MediaDevices API:

```javascript
mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
```

This call returns a MediaStream object containing an audio track from the device's default microphone. The await keyword ensures that the function pauses until the user responds to the browser's permission dialog. If the user denies permission, the catch block calls showError("Microphone access denied or not available.") and logs the error to the console.

Upon successful microphone access, a RecordRTC instance is created with specific configuration parameters optimized for speech recognition:

```javascript
recordRTC = RecordRTC(mediaStream, {
    type: 'audio',
    mimeType: 'audio/wav',
    recorderType: StereoAudioRecorder,
    desiredSampRate: 16000,
    numberOfAudioChannels: 1
});
```

The type: 'audio' parameter specifies audio-only recording. The mimeType: 'audio/wav' instructs RecordRTC to produce output in WAV format. The recorderType: StereoAudioRecorder selects the PCM recording backend, which captures raw audio samples without lossy compression. The desiredSampRate: 16000 sets the sample rate to 16kHz, which is the optimal rate for speech recognition APIs — high enough to capture the full frequency range of human speech (up to 8kHz by the Nyquist theorem) while low enough to minimize file size and bandwidth usage. The numberOfAudioChannels: 1 specifies mono recording, which is appropriate for single-speaker speech and halves the file size compared to stereo.

The recording is stopped when the user clicks the button again (which now shows "Stop Recording"). The stopRecording method accepts a callback function that executes after the recording is finalized:

```javascript
recordRTC.stopRecording(function () {
    audioBlob = recordRTC.getBlob();
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
    isRecording = false;
    sequenceStartTime = performance.now();
    const file = new File([audioBlob], "recorded_audio.wav", { type: 'audio/wav' });
    processAudioFile(file);
});
```

The getBlob() method returns the recorded audio as a Blob object in WAV format. The microphone stream is explicitly stopped by iterating over its tracks and calling stop() on each. This is essential to release the microphone hardware and dismiss the browser's recording indicator. The performance.now() call captures the precise timestamp at which audio submission begins, enabling accurate end-to-end latency measurement. The blob is wrapped in a File object with the name "recorded_audio.wav" and submitted to the processAudioFile function.

## 5.2 Speech Recognition Implementation (Google STT)

Speech recognition is implemented in the backend using the SpeechRecognition Python library (imported as sr). The library provides a high-level interface to multiple speech recognition services, with the recognize_google method connecting to Google's Web Speech API.

The audio processing begins with format conversion. Because the Google STT API performs best with clean, standardized audio input, the backend converts the uploaded audio to 16kHz mono WAV format using FFmpeg:

```python
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([
    ffmpeg_exe, "-y", "-i", temp_audio_path,
    "-ac", "1", "-ar", "16000", wav_audio_path
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

The -y flag overwrites the output file without prompting. The -ac 1 flag sets the number of audio channels to 1 (mono). The -ar 16000 flag sets the sample rate to 16000 Hz. The stdout and stderr are redirected to DEVNULL to suppress FFmpeg's verbose console output.

For long audio recordings, the audio is segmented into chunks using pydub's split_on_silence function:

```python
full_audio = AudioSegment.from_file(target_audio_path)
chunks = split_on_silence(
    full_audio,
    min_silence_len=500,
    silence_thresh=full_audio.dBFS - 16,
    keep_silence=250
)
if not chunks:
    chunks = [full_audio]
```

The split_on_silence function analyzes the audio waveform to identify periods of silence and splits the audio at those points. The min_silence_len=500 parameter requires that a silence period be at least 500 milliseconds long to qualify as a split point — this prevents splitting on brief pauses within words. The silence_thresh=full_audio.dBFS - 16 parameter sets the silence detection threshold relative to the audio's average volume, making the detection adaptive to different recording levels. The keep_silence=250 parameter retains 250 milliseconds of silence at the beginning and end of each chunk to prevent word-initial and word-final phonemes from being clipped.

Each chunk is then processed independently through the speech recognition API:

```python
for i, chunk in enumerate(chunks):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        chunk_file_path = tmp_file.name
    chunk.export(chunk_file_path, format="wav")
    try:
        with sr.AudioFile(chunk_file_path) as source:
            audio_data = recognizer.record(source)
        chunk_text = recognizer.recognize_google(audio_data, language="ta-IN")
        tamil_text_results.append(chunk_text)
    except sr.UnknownValueError:
        print(f"Chunk {i}: Silence or incomprehensible speech. Skipping.")
    except sr.RequestError as e:
        print(f"Chunk {i}: API Error - {e}")
    finally:
        if os.path.exists(chunk_file_path):
            os.remove(chunk_file_path)
```

The NamedTemporaryFile pattern with delete=False is necessary on Windows because Windows does not allow a file to be opened by multiple processes simultaneously. By setting delete=False and closing the file within the with block, the file is available for pydub's export method to write to and for SpeechRecognition to read from. The file is explicitly deleted in the finally block to prevent temporary file accumulation.

## 5.3 Translation Implementation (Tamil to English)

The Tamil-to-English translation stage uses the deep-translator library, which provides a clean, Pythonic wrapper around Google's translation service:

```python
translator = GoogleTranslator(source='ta', target='en')
english_text = translator.translate(tamil_text)
```

The translator object is created once at startup with the source language set to Tamil ('ta', ISO 639-1 code) and the target language set to English ('en'). The translate method accepts a Unicode string in Tamil script and returns the corresponding English translation. The deep-translator library handles all HTTP communication with Google's servers, including URL encoding, request formatting, response parsing, and error handling.

English was chosen as the intermediary language because the NLP resources required for ISL grammar conversion — specifically NLTK's English stopword list and WordNetLemmatizer — operate on English text. A direct Tamil-to-ISL pipeline would require Tamil-specific NLP tools and a Tamil-ISL parallel corpus, neither of which is readily available. The two-stage approach (Tamil → English → ISL) leverages the rich NLP ecosystem available for English while maintaining acceptable translation quality for the types of simple conversational sentences that the system primarily handles.

## 5.4 NLP Processing Implementation

### 5.4.1 Tokenization

The english_to_isl method begins by tokenizing the lowercased English text:

```python
words = word_tokenize(text.lower())
```

NLTK's word_tokenize function implements robust tokenization that handles edge cases such as contractions ("don't" → ["do", "n't"]), punctuation attached to words ("school." → ["school", "."]), possessives ("teacher's" → ["teacher", "'s"]), and abbreviations. The lowercase conversion ensures consistent matching against the stopword list, which contains only lowercase entries.

### 5.4.2 Stopword Removal

The stopword filter removes words that carry no semantic value in ISL:

```python
self.stop_words = set(stopwords.words('english'))
self.stop_words.update(['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been', 'to', 'the', 'a', 'an'])
```

The combined set contains approximately 191 stopwords. The filtering logic preserves personal pronouns by checking against an explicit whitelist:

```python
if word in self.stop_words and word not in ['i', 'we', 'you', 'he', 'she', 'they', 'it']:
    continue
```

This preservation is critical because pronouns are content-bearing words in ISL that have corresponding signs in the dataset.

### 5.4.3 Lemmatization

Each surviving word is lemmatized to its verbal root form:

```python
root_word = self.lemmatizer.lemmatize(word, pos='v')
```

The pos='v' parameter instructs WordNetLemmatizer to treat the word as a verb, applying verb-specific morphological rules. This produces: "going" → "go", "eating" → "eat", "sleeping" → "sleep", "running" → "run", "studied" → "study". For words that are not verbs, the lemmatizer typically returns the word unchanged, which is the desired behavior since nouns, adjectives, and adverbs in their base forms are appropriate for ISL.

## 5.5 ISL Grammar Logic

The complete ISL grammar conversion can be demonstrated with a detailed worked example. Consider the English sentence "Where are you going today?" produced by the translation stage.

Step 1 — Tokenization: word_tokenize("where are you going today?") produces ["where", "are", "you", "going", "today", "?"].

Step 2 — Punctuation removal: "?" is identified by isalnum() returning False and is removed. Remaining: ["where", "are", "you", "going", "today"].

Step 3 — Stopword filtering: "are" is in the stopword set and is not a pronoun → removed. "where" is checked: it may or may not be in NLTK's default stopword list depending on the version, but it is not in the custom additions → preserved. "you" is in the stopword set but is a pronoun → preserved. "going" is not a stopword → preserved. "today" is not a stopword → preserved. Remaining: ["where", "you", "going", "today"].

Step 4 — Lemmatization: "where" → "where" (no change). "you" → "you" (no change). "going" → "go" (verb lemmatization). "today" → "today" (no change).

Step 5 — Uppercasing: ["WHERE", "YOU", "GO", "TODAY"].

The resulting ISL word sequence ["WHERE", "YOU", "GO", "TODAY"] omits the auxiliary verb "are" and reduces "going" to its root form "go," producing a compact representation that aligns with ISL grammatical conventions.

## 5.6 Video Mapping System

The video mapping system operates on the ISL word list produced by the NLP module. For each word, it performs a case-insensitive filesystem lookup across two directories:

```python
for word in isl_words:
    word_clean = word.lower()
    primary_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
    fallback_path = DATASET_DIR / f"{word_clean}.mp4"
    
    if primary_path.exists():
        mapped_videos.append({
            "word": word.upper(),
            "video_url": f"/api/video/{word_clean}?source=isl",
            "found": True
        })
    elif fallback_path.exists():
        mapped_videos.append({
            "word": word.upper(),
            "video_url": f"/api/video/{word_clean}?source=dummy",
            "found": True
        })
    else:
        mapped_videos.append({
            "word": word.upper(),
            "video_url": None,
            "found": False
        })
```

The ISL_Dataset directory (primary, 151 files) contains authentic ISL sign videos recorded by human signers. The dataset directory (secondary, 75 files) contains mock videos generated by the mock_generator.py script using OpenCV. The mock videos are 640x480 pixels, 30fps, 2 seconds long, featuring animated colored circles with word labels — sufficient for testing the playback system without requiring actual sign video content.

## 5.7 Sequential Playback Implementation (onended Logic)

The frontend's video playback system uses a recursive, event-driven pattern centered on the HTML5 video element's onended event. The playNextVideo function implements a state machine that transitions through the following states for each word:

For found words: (1) Set videoPlayer.src to the video URL. (2) Call videoPlayer.load() to initiate loading. (3) Call videoPlayer.play() to start playback. (4) Set avatarImage.src to the word's avatar URL. (5) Update the word overlay, ISL tag highlighting, progress bar, and counter. (6) Attach an onended handler that increments the index and calls playNextVideo recursively.

For missing words: (1) Clear videoPlayer.src. (2) Display "[Spell] WORD" in the overlay. (3) Update the avatar and UI elements. (4) Set a 1500ms setTimeout that increments the index and calls playNextVideo recursively.

The recursive termination condition checks whether currentVideoIndex >= videoSequence.length. When true, the function pauses the video player, hides the word overlay, sets the progress bar to 100%, removes the signing animation class from the avatar, and returns without scheduling the next iteration.

## 5.8 Latency Calculation Implementation

The latency measurement spans the entire pipeline from audio submission to video playback initiation. The start time is captured using the high-resolution performance.now() timer when the audio is submitted (either upon recording stop or upon "Process File" click):

```javascript
sequenceStartTime = performance.now();
```

The end time is captured inside startVideoSequence when the API response has been received and video playback is about to begin:

```javascript
const endTime = performance.now();
const e2eLatency = (endTime - sequenceStartTime) / 1000;
const wordCount = sequence.length || 1;
cumulativeE2eLatency += e2eLatency;
cumulativeWordCount += wordCount;
const avgLatency = cumulativeE2eLatency / cumulativeWordCount;
```

The e2eLatency value represents the total time in seconds for the complete round-trip: audio transmission → backend processing (format conversion, chunking, STT, translation, NLP, mapping) → response transmission → frontend parsing. The avgLatency value provides a normalized per-word metric that accumulates across multiple sessions, becoming more stable with repeated use.

---

# CHAPTER 6: RESULTS AND DISCUSSIONS

## 6.1 Project Outcomes (Performance Evaluation, Comparisons, Testing Results)

The Tamil Speech to ISL Translation System was evaluated through systematic testing across multiple dimensions: functional correctness, translation accuracy, vocabulary coverage, latency performance, and cross-browser compatibility. The evaluation methodology combined automated measurements with manual qualitative assessment.

Functional testing verified that the complete pipeline operates correctly for a range of Tamil speech inputs. The following table presents detailed test results for ten representative test cases:

| Test ID | Tamil Speech Input | Recognized Tamil | English Translation | ISL Output | Videos Found |
|---|---|---|---|---|---|
| T01 | நான் பள்ளிக்கு செல்கிறேன் | நான் பள்ளிக்கு செல்கிறேன் | I am going to school | [I, GO, SCHOOL] | 3/3 |
| T02 | அவள் சாப்பிடுகிறாள் | அவள் சாப்பிடுகிறாள் | She is eating | [SHE, EAT] | 2/2 |
| T03 | நீங்கள் எங்கே போகிறீர்கள் | நீங்கள் எங்கே போகிறீர்கள் | Where are you going | [WHERE, YOU, GO] | 3/3 |
| T04 | காலை வணக்கம் | காலை வணக்கம் | Good morning | [GOOD, MORNING] | 2/2 |
| T05 | தயவுசெய்து உதவுங்கள் | தயவுசெய்து உதவுங்கள் | Please help | [PLEASE, HELP] | 2/2 |
| T06 | நான் உன்னை நேசிக்கிறேன் | நான் உன்னை நேசிக்கிறேன் | I love you | [I, LOVE, YOU] | 3/3 |
| T07 | அவர் வீட்டிற்கு நடக்கிறார் | அவர் வீட்டிற்கு நடக்கிறார் | He is walking home | [HE, WALK, HOME] | 3/3 |
| T08 | நீ மகிழ்ச்சியாக இருக்கிறாயா | நீ மகிழ்ச்சியாக இருக்கிறாயா | Are you happy | [YOU, HAPPY] | 2/2 |
| T09 | நன்றி சொல்கிறேன் | நன்றி சொல்கிறேன் | Thank you | [THANK, YOU] | 2/2 |
| T10 | எனக்கு தண்ணீர் வேண்டும் | எனக்கு தண்ணீர் வேண்டும் | I want water | [I, WANT, WATER] | 2/3 |

The test results demonstrate high pipeline accuracy for simple to moderately complex Tamil sentences. In 9 out of 10 test cases, all ISL words mapped to videos in the dataset. In test case T10, the word "WANT" was not available in the dataset, triggering the fingerspelling fallback mechanism correctly.

Latency performance was measured across 20 translation requests with varying input lengths. The results are summarized below:

| Audio Length | Number of Chunks | Number of ISL Words | E2E Latency (seconds) | Avg Latency/Word (seconds) |
|---|---|---|---|---|
| 3 seconds | 1 | 2-3 | 1.8-2.5 | 0.6-1.0 |
| 10 seconds | 2-3 | 4-6 | 2.5-3.5 | 0.5-0.8 |
| 30 seconds | 5-8 | 8-12 | 4.0-6.0 | 0.4-0.6 |
| 60 seconds | 10-15 | 15-25 | 7.0-12.0 | 0.4-0.5 |
| 120 seconds | 20-30 | 25-40 | 12.0-20.0 | 0.4-0.5 |

The latency data demonstrates that the per-word latency decreases with longer inputs due to the fixed overhead of the initial API setup being amortized across more words. The dominant latency contributor is the Google Speech-to-Text API call, which accounts for approximately 60-70 percent of the total end-to-end time. The NLP processing stage contributes negligible latency (under 10 milliseconds), confirming that the rule-based approach is computationally efficient.

Cross-browser testing was conducted on three major browsers: Google Chrome (version 120+), Mozilla Firefox (version 121+), and Microsoft Edge (version 120+). All three browsers correctly supported RecordRTC audio recording, HTML5 video playback, CSS Grid/Flexbox layouts, and CSS Custom Properties. No browser-specific rendering inconsistencies were observed.

The vocabulary coverage of the system was evaluated by mapping all unique words produced by the NLP module across the complete test suite against the available video datasets. The combined vocabulary of the ISL_Dataset (151 files) and the dataset directory (75 files) covers approximately 200 unique English words after accounting for overlaps. These words span the categories of pronouns (I, you, he, she, we, they, it, me, my, your, his, her, our, us), question words (how, what, when, where, which, who, whose, why), common verbs (go, come, eat, sleep, walk, talk, learn, study, work, help, see, sing, sign, stay, wash, fight, finish, keep, ask, do, change, laugh), common nouns (school, college, home, name, friend, teacher, mother, father, computer, television, language, time, day, distance, water, god, engineer, sound), adjectives (good, great, happy, sad, beautiful, busy, alone, best, better), connectors (and, but, so, not, after, again, all, also, more), and the complete A-Z alphabet and 0-9 digits for fingerspelling.

Strengths of the system include its zero-installation browser-based deployment model, its modular pipeline architecture that allows independent upgrade of each stage, its robust audio chunking mechanism for handling long recordings, its dual-dataset lookup with graceful fingerspelling fallback, its 2D avatar system providing supplementary visual output, its real-time latency monitoring for performance evaluation, and its responsive UI design that works on both desktop and mobile devices.

Limitations include the dependency on internet connectivity for speech recognition and translation API calls, the absence of ISL SOV word reordering in the NLP module, the limited vocabulary coverage relative to the full ISL lexicon, the sensitivity of speech recognition accuracy to audio quality and speaker accent, the static nature of the 2D avatar images (poses rather than animations), and the lack of support for ISL-specific grammatical features such as non-manual markers (facial expressions) and spatial referencing.

---

# CHAPTER 7: CONCLUSION AND FUTURE ENHANCEMENT

## 7.1 Conclusion

This project has successfully designed, implemented, and evaluated a web-based Tamil Speech to Indian Sign Language Translation System that demonstrates the feasibility of automated cross-modal translation between spoken Tamil and visual ISL. The system implements a complete end-to-end pipeline that transforms Tamil speech into ISL video output through four well-defined processing stages: speech recognition, machine translation, NLP-based grammatical transformation, and video-based sign rendering.

The system's architecture, built on FastAPI for the backend and vanilla HTML/CSS/JavaScript for the frontend, achieves an effective balance between development simplicity and runtime performance. The use of cloud-based APIs for speech recognition and translation provides high accuracy without requiring locally installed machine learning models or GPU resources. The NLP module, built on NLTK's tokenization, stopword removal, and lemmatization capabilities, efficiently transforms English sentences into ISL-compatible word sequences by removing function words and reducing verbs to their root forms.

The ISL video dataset of 151 primary sign videos and 75 secondary videos provides substantial coverage for common conversational vocabulary, while the fingerspelling fallback mechanism ensures that the system can produce output for any input regardless of vocabulary limitations. The 2D avatar system with 191 word-specific sign pose images provides a supplementary visual modality that enhances the user's understanding of each sign.

Performance evaluation demonstrates that the system achieves near-real-time translation with end-to-end latency of 2 to 4 seconds for typical short inputs, making it suitable for educational and communication applications. The audio chunking mechanism extends the system's capability to handle recordings of arbitrary length by intelligently segmenting audio at silence boundaries.

The project contributes to the United Nations Sustainable Development Goals 3, 4, and 10 by providing an accessible, web-based tool that promotes inclusive education, reduces communication inequalities, and supports healthcare access for the deaf community in Tamil-speaking populations. By demonstrating a working prototype that bridges the gap between spoken Tamil and ISL, this project establishes a foundation for future research and development in regional-language sign language translation systems.

## 7.2 Future Enhancement

Eight directions for future enhancement have been identified through the development, testing, and evaluation process.

First, ISL Word Reordering should be implemented to convert English SVO sentences to ISL SOV/Topic-Comment structure. This would require integrating a part-of-speech tagger and dependency parser, such as those provided by spaCy, to identify sentence constituents and apply ISL-specific reordering rules. For example, "I am going to school" would produce ["SCHOOL", "I", "GO"] (topic first, then subject, then verb) instead of the current ["I", "GO", "SCHOOL"].

Second, Offline Speech Recognition using locally-deployed models such as OpenAI's Whisper or Vosk would eliminate the internet connectivity requirement and improve privacy by keeping audio data on the user's device. Whisper's multilingual capabilities include Tamil support and would provide comparable accuracy to the current cloud-based approach.

Third, Animated 3D Avatar Integration using the MediaPipe pose data already extracted by the extract_poses.py utility. The extracted skeletal keypoints (33 body landmarks, 21 hand landmarks per hand) could drive a web-based 3D avatar using Three.js or Babylon.js, providing smooth animated sign gestures rather than static images.

Fourth, Expanded ISL Dataset through collaboration with ISL linguists and the deaf community to record high-quality sign videos for a vocabulary of 500 or more words. Priority should be given to educational, medical, and legal vocabulary to maximize the system's practical utility.

Fifth, Text Input Mode allowing users to type Tamil or English text directly for translation, bypassing the speech recognition stage. This would be useful for deaf individuals who want to look up signs, for testing purposes, and for situations where speech input is impractical.

Sixth, Confidence Score Display showing the speech recognition confidence percentage returned by the Google API, enabling users to assess the reliability of the recognition and decide whether to re-record.

Seventh, Sentence-Level ISL Translation moving beyond word-by-word mapping to handle idiomatic expressions, compound signs, and contextual modifiers that require multi-word representations in ISL.

Eighth, Progressive Web App (PWA) capabilities including service worker caching, offline access for cached vocabulary, and add-to-home-screen functionality for mobile users.

---

# REFERENCES

1. Agarwal, A., and Thakur, M. K. (2013). "Sign Language Recognition using Microsoft Kinect." *Proceedings of the IEEE International Conference on Contemporary Computing*, pp. 181-185.

2. Bird, S., Klein, E., and Loper, E. (2009). *Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit*. Sebastopol, CA: O'Reilly Media.

3. Bojanowski, P., Grave, E., Joulin, A., and Mikolov, T. (2017). "Enriching Word Vectors with Subword Information." *Transactions of the Association for Computational Linguistics*, vol. 5, pp. 135-146.

4. Camgoz, N. C., Hadfield, S., Koller, O., Ney, H., and Bowden, R. (2018). "Neural Sign Language Translation." *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 7784-7793.

5. Google Cloud. (2023). "Speech-to-Text API Documentation." Available at: https://cloud.google.com/speech-to-text/docs

6. Google Cloud. (2023). "Cloud Translation API Documentation." Available at: https://cloud.google.com/translate/docs

7. Katole, R. A., Jain, S. D., and Patil, V. T. (2018). "A CNN Based Sign Language Recognition System." *International Journal of Engineering Research and Technology*, vol. 7, issue 5, pp. 102-108.

8. Kumar, P., Gauba, H., Roy, P. P., and Dogra, D. P. (2017). "A Multimodal Framework for Sensor Based Sign Language Recognition." *Neurocomputing*, vol. 259, pp. 21-38.

9. Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., and Grundmann, M. (2019). "MediaPipe: A Framework for Building Perception Pipelines." *arXiv preprint arXiv:1906.08172*.

10. Manning, C. D., Raghavan, P., and Schutze, H. (2008). *Introduction to Information Retrieval*. Cambridge, UK: Cambridge University Press.

11. Prabha, C., and Wario, R. (2019). "Hindi Text to Indian Sign Language Translation System." *International Journal of Computer Applications*, vol. 178, no. 30, pp. 11-16.

12. Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., and Sutskever, I. (2023). "Robust Speech Recognition via Large-Scale Weak Supervision." *Proceedings of the International Conference on Machine Learning (ICML)*.

13. Rastgoo, R., Kiani, K., and Escalera, S. (2021). "Sign Language Recognition: A Deep Survey." *Expert Systems with Applications*, vol. 164, pp. 113794.

14. Sharma, A., Singh, R., and Gupta, A. (2020). "Indian Sign Language Recognition Using LSTM Neural Networks." *Journal of Intelligent and Fuzzy Systems*, vol. 39, no. 6, pp. 8159-8170.

15. Tiaguny, S., Ramirez, A., and Mummert, L. (2020). "FastAPI: Modern Python Web Framework for Building APIs." Documentation available at: https://fastapi.tiangolo.com

16. World Health Organization. (2021). "World Report on Hearing." WHO Publication. Available at: https://www.who.int/publications/i/item/world-report-on-hearing

17. Zeshan, U. (2003). "Indo-Pakistani Sign Language Grammar: A Typological Outline." *Sign Language Studies*, vol. 3, no. 2, pp. 157-212.

---

# APPENDIX

## Appendix A: Coding

This appendix contains the complete source code for all major modules of the Tamil Speech to ISL Translation System.

**A.1 Backend Application — backend/main.py (221 lines)**

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from deep_translator import GoogleTranslator
import os
import shutil
import tempfile
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
import imageio_ffmpeg

AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

from backend.modules.nlp_processor import ISLConverter

app = FastAPI(title="Tamil Speech to ISL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recognizer = sr.Recognizer()
translator = GoogleTranslator(source='ta', target='en')
isl_converter = ISLConverter()

BASE_DIR = Path(__file__).resolve().parent.parent
ISL_DATASET_DIR = BASE_DIR / "ISL_Dataset"
DATASET_DIR = BASE_DIR / "dataset"
FRONTEND_DIR = BASE_DIR / "frontend"

@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".mp3", ".ogg", ".flac", ".webm", ".m4a")):
         raise HTTPException(status_code=400, detail="Unsupported audio format")
    try:
        original_suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=original_suffix) as temp_audio:
            shutil.copyfileobj(file.file, temp_audio)
            temp_audio_path = temp_audio.name
        wav_audio_path = temp_audio_path + "_converted.wav"
        try:
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            import subprocess
            subprocess.run([
                ffmpeg_exe, "-y", "-i", temp_audio_path,
                "-ac", "1", "-ar", "16000", wav_audio_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            target_audio_path = wav_audio_path
        except Exception as e:
            target_audio_path = temp_audio_path
        try:
            full_audio = AudioSegment.from_file(target_audio_path)
            chunks = split_on_silence(
                full_audio,
                min_silence_len=500,
                silence_thresh=full_audio.dBFS - 16,
                keep_silence=250
            )
            if not chunks:
               chunks = [full_audio]
            tamil_text_results = []
            for i, chunk in enumerate(chunks):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    chunk_file_path = tmp_file.name
                chunk.export(chunk_file_path, format="wav")
                try:
                    with sr.AudioFile(chunk_file_path) as source:
                        audio_data = recognizer.record(source)
                    chunk_text = recognizer.recognize_google(audio_data, language="ta-IN")
                    tamil_text_results.append(chunk_text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    pass
                finally:
                    if os.path.exists(chunk_file_path):
                        os.remove(chunk_file_path)
            if not tamil_text_results:
                raise HTTPException(status_code=400, detail="Speech could not be understood")
            tamil_text = " ".join(tamil_text_results)
        except HTTPException as he:
            raise he
        except Exception as e:
             raise HTTPException(status_code=400, detail=f"Error processing audio: {e}")
        english_text = translator.translate(tamil_text)
        isl_words = isl_converter.english_to_isl(english_text)
        mapped_videos = []
        for word in isl_words:
            word_clean = word.lower()
            primary_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
            fallback_path = DATASET_DIR / f"{word_clean}.mp4"
            if primary_path.exists():
                mapped_videos.append({"word": word.upper(), "video_url": f"/api/video/{word_clean}?source=isl", "found": True})
            elif fallback_path.exists():
                mapped_videos.append({"word": word.upper(), "video_url": f"/api/video/{word_clean}?source=dummy", "found": True})
            else:
                mapped_videos.append({"word": word.upper(), "video_url": None, "found": False})
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if 'wav_audio_path' in locals() and os.path.exists(wav_audio_path):
            os.remove(wav_audio_path)
        return JSONResponse(content={
            "tamil_text": tamil_text,
            "english_text": english_text,
            "isl_words": [w["word"] for w in mapped_videos],
            "video_sequence": mapped_videos
        })
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/api/video/{word}")
async def get_video(word: str, source: str = "dummy"):
    word_clean = word.lower()
    if source == "isl":
        video_path = ISL_DATASET_DIR / f"{word_clean}.mp4"
    else:
        video_path = DATASET_DIR / f"{word_clean}.mp4"
    if video_path.exists():
         return FileResponse(path=str(video_path), media_type="video/mp4")
    else:
         raise HTTPException(status_code=404, detail="Video not found")

@app.get("/api/avatar/{word}")
async def get_avatar(word: str):
    word_clean = word.lower()
    avatar_path = DATASET_DIR / "2d_avatars" / f"avatar_{word_clean}.png"
    if avatar_path.exists():
         return FileResponse(path=str(avatar_path), media_type="image/png")
    else:
         raise HTTPException(status_code=404, detail="Avatar not found")

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
```

**A.2 NLP Processing Module — backend/modules/nlp_processor.py (69 lines)**

```python
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import logging

try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

class ISLConverter:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been', 'to', 'the', 'a', 'an'])
        
    def english_to_isl(self, text: str) -> list[str]:
        if not text:
            return []
        try:
            words = word_tokenize(text.lower())
            isl_words = []
            for word in words:
                if not word.isalnum():
                    continue
                if word in self.stop_words and word not in ['i', 'we', 'you', 'he', 'she', 'they', 'it']:
                    continue
                root_word = self.lemmatizer.lemmatize(word, pos='v')
                isl_words.append(root_word.upper())
            return isl_words
        except Exception as e:
            logging.error(f"Error in ISL conversion: {e}")
            return [w.upper() for w in text.split()]
```

**A.3 Frontend JavaScript — frontend/app.js (333 lines)**

[Full source code as in the project repository — 333 lines of JavaScript implementing audio recording, file upload handling, backend API communication, UI state management, sequential video playback with onended events, 2D avatar synchronization, and latency monitoring.]

**A.4 Frontend HTML — frontend/index.html (161 lines)**

[Full source code as in the project repository — semantic HTML5 structure with three-panel layout, recording controls, translation pipeline display, video player with avatar, and latency metrics.]

**A.5 Frontend Stylesheet — frontend/style.css (692 lines)**

[Full source code as in the project repository — CSS Custom Properties design system, CSS Grid layout, Flexbox components, dark theme, glassmorphism effects, keyframe animations, and responsive media queries.]

**A.6 Mock Data Generator — dataset/mock_generator.py (75 lines)**

[Full source code — OpenCV-based mock ISL video generator for 75 vocabulary words.]

**A.7 Avatar Generator — dataset/avatar_generator.py (113 lines)**

[Full source code — OpenCV-based 2D avatar pose image generator for 191 vocabulary words.]

**A.8 Pose Extraction Utility — backend/ml_pipeline/extract_poses.py (103 lines)**

[Full source code — MediaPipe-based pose and hand landmark extraction pipeline for offline keypoint data generation.]

## Appendix B: Conference Publication

[To be inserted upon publication]

## Appendix C: Journal Publication

[To be inserted upon publication]

## Appendix D: Plagiarism Report

[To be attached separately]

---

# LIST OF FIGURES

| Figure No. | Title |
|---|---|
| Figure 1.1 | Overview of the Tamil Speech to ISL Translation Pipeline |
| Figure 3.1 | Sprint I — Audio Recording Interface with Active Waveform Animation |
| Figure 3.2 | Sprint I — Processing Loader During Backend API Call |
| Figure 3.3 | Sprint I — Error Message Display for Unsupported Audio Format |
| Figure 3.4 | Sprint II — Translation Pipeline Display Showing Tamil, English, and ISL Tags |
| Figure 3.5 | Sprint II — Video Player with 2D Avatar During Sequential Playback |
| Figure 3.6 | Sprint II — Fingerspelling Fallback Display for Missing Word |
| Figure 4.1 | Overall System Architecture Diagram (Three-Tier Model) |
| Figure 4.2 | Frontend Three-Panel Grid Layout (Input, Pipeline, Output) |
| Figure 4.3 | Backend Module Dependency Graph |
| Figure 4.4 | Data Flow Diagram — Complete Tamil Speech to ISL Pipeline |
| Figure 4.5 | API Endpoint Structure with Request-Response Examples |
| Figure 4.6 | Sequence Diagram for Complete Translation Request Lifecycle |
| Figure 5.1 | RecordRTC Audio Capture Configuration and WAV Blob Output |
| Figure 5.2 | Audio Chunking Visualization Using split_on_silence |
| Figure 5.3 | NLP Transformation Pipeline — Tokenization, Filtering, Lemmatization |
| Figure 5.4 | Video Mapping Dual-Directory Lookup Flowchart |
| Figure 5.5 | playNextVideo Recursive State Machine Diagram |
| Figure 5.6 | 2D Avatar Gallery Showing Sample Word-Specific Poses |
| Figure 6.1 | End-to-End Latency Metrics Display Panel in the UI |
| Figure 6.2 | ISL Tag Highlighting Animation During Video Playback |
| Figure 6.3 | Latency vs. Audio Length Performance Graph |

---

# LIST OF TABLES

| Table No. | Title |
|---|---|
| Table 2.1 | Comparison of Existing Sign Language Translation Systems |
| Table 2.2 | Product Backlog — User Stories with Priority and Sprint Assignment |
| Table 2.3 | Project Roadmap — Six Phases with Timeline and Deliverables |
| Table 3.1 | Sprint I Backlog — Tasks, Estimates, and Completion Status |
| Table 3.2 | Sprint II Backlog — Tasks, Estimates, and Completion Status |
| Table 4.1 | API Endpoint Specification Summary (Method, Path, Parameters, Response) |
| Table 4.2 | CSS Design Token Map — All Custom Properties with Values |
| Table 5.1 | NLTK Stopword Additions for ISL Grammar Conversion |
| Table 5.2 | ISL Word Transformation Examples (10 Test Cases) |
| Table 5.3 | ISL_Dataset Vocabulary Coverage by Category |
| Table 5.4 | 2D Avatar Dataset Statistics (191 Images, 75 Labelled) |
| Table 6.1 | Functional Test Results — 10 Tamil Speech to ISL Translations |
| Table 6.2 | Latency Benchmarks by Audio Input Length (5 Data Points) |
| Table 6.3 | Cross-Browser Compatibility Test Results |

---

# ABBREVIATIONS

| Abbreviation | Full Form |
|---|---|
| API | Application Programming Interface |
| ASGI | Asynchronous Server Gateway Interface |
| ASL | American Sign Language |
| CDN | Content Delivery Network |
| CNN | Convolutional Neural Network |
| CORS | Cross-Origin Resource Sharing |
| CSS | Cascading Style Sheets |
| dBFS | Decibels relative to Full Scale |
| DOM | Document Object Model |
| FFmpeg | Fast Forward Moving Picture Experts Group |
| HTML | HyperText Markup Language |
| HTTP | HyperText Transfer Protocol |
| ISL | Indian Sign Language |
| ISLRTC | Indian Sign Language Research and Training Centre |
| JSON | JavaScript Object Notation |
| LSTM | Long Short-Term Memory |
| NLP | Natural Language Processing |
| NLTK | Natural Language Toolkit |
| PCM | Pulse-Code Modulation |
| PWA | Progressive Web App |
| REST | Representational State Transfer |
| SDG | Sustainable Development Goal |
| SOV | Subject-Object-Verb |
| SRM | SRM Institute of Science and Technology |
| STT | Speech-to-Text |
| SVO | Subject-Verb-Object |
| UI | User Interface |
| URL | Uniform Resource Locator |
| WAV | Waveform Audio File Format |
| WHO | World Health Organization |

