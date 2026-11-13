---
title: "AI for Smallholder Agriculture: Closing the Advisory, Data and Access Gap in Emerging Economies"
subtitle: "Final Research Project Report, with the FarmWise working prototype"
author: "Khan Salman, Beijing Normal University, IEDE ID A20260058"
date: "Tsinghua University Global Program on The AI Economy: Innovation, Skills & Entrepreneurship (IEDE THU), Autumn 2026. Instructor: Prof. Kris Singh"
---

# Abstract

Smallholders make up about 80% of farmers in developing countries, yet most receive little agronomic advice because conventional extension costs roughly $30 to $35 per farmer. This project studies how artificial intelligence can close that advisory gap. It reviews current AI applications in agriculture, compares three delivery routes (China, India and the Farmer.Chat programme in Africa and beyond), identifies six specific challenges to smallholder adoption, and maps a solution to each. It then proposes a mobile-first, layered advisory framework and tests the first layer by building **FarmWise**, a working offline maize advisory prototype for South Asian smallholders. On a held-out set of questions the prototype retrieved the correct guidance for 20 of 22 maize questions (90.9%), gave no wrong answers, referred the other two to an extension officer, and correctly declined all 9 questions it should not answer, including pesticide dose and poisoning cases. These results come from a small question set written by the author and a knowledge base not yet validated by an agronomist, so they show technical feasibility, not field impact.

# 1. Introduction

Agriculture faces rising demand and climate pressure. The world population is projected to reach about 9.7 billion by 2050. Around 570 million smallholder farmers produce much of the food in developing regions, but yields lag far behind: maize yields in parts of sub-Saharan Africa are about 2 to 3 tonnes per hectare, against more than 10 in the United States.

Part of this gap is an information gap. Timely advice on planting, pests, fertiliser and storage raises yields, but human extension services are thin and costly. AI changes the cost of advice. Digital Green estimates that its language-model assistant Farmer.Chat could cut the cost of advisory from about $35 per farmer to about $0.35. At the same time, a 2026 comparative study warns that smallholders risk being left behind, because AI tools need electricity, connectivity, money and digital skills, and models trained on large industrial farms can give poor advice on small plots.

This project asks how AI can be deployed so that low-resource farmers benefit first.

# 2. Objectives and research questions

**Objectives**

1. Map where AI delivers value across the farm cycle.
2. Compare AI adoption routes in China, India and Africa.
3. Identify the specific barriers facing smallholders.
4. Propose a practical mobile-first framework and test its first layer with a working prototype.

**Research questions**

1. Which AI applications give smallholders measurable gains today?
2. What blocks adoption: infrastructure, cost, data, skills or trust?
3. How can rollout be sequenced so low-resource farmers benefit first?
4. Can a safe, offline advisory assistant be built with minimal resources, and how well does it perform?

# 3. Method

The project combined three methods.

- **Desk research.** Recent reports, news and programme publications (2024 to October 2026) on AI in agriculture, listed in the references.
- **Comparative case studies.** China, India and Farmer.Chat were compared on delivery model, technology, enablers and constraints.
- **Design and build.** A prototype was built and evaluated with unit tests and a two-part question set: a development split used for tuning and a held-out test split used only for reporting.

# 4. AI applications and market

Six application areas recur in the sources:

| Application | What it does |
|---|---|
| Smart advisory | Language-model chat in local languages by voice or text |
| Pest and disease detection | Phone or drone images analysed with computer vision |
| Precision irrigation | Sensors and weather models reduce water use |
| Sowing and yield forecasts | Satellite and climate data guide timing |
| Machinery and drones | Targeted spraying, ripeness maps, fleet platforms |
| Breeding and markets | Genomic models; price and credit signals |

Market estimates vary by publisher and scope. Roots Analysis put the AI-in-agriculture market at USD 2.14 billion in 2024; Maximize Market Research at USD 2.96 billion in 2025, growing 21.5% a year to USD 11.59 billion by 2032; a June 2026 industry release cited more than USD 4.7 billion. Precision farming holds about a quarter of the 2026 market. These figures are indicative only.

# 5. Case studies

## 5.1 China: state-led AI at scale

China's 2026 No. 1 Document calls for deeper integration of AI, drones and robots in farming. Henan's agricultural machinery cloud had connected more than 138,000 machines by June 2026. Field robots trained with the DeepSeek model reached pest-identification accuracy above 80%. A 200-hectare smart rice farm is managed by four people with net income above 30,000 yuan per hectare. Maoming built a local assistant on a lychee knowledge base with more than five million data points. Limits include high upfront costs and rural infrastructure gaps, and many results come from showcase projects.

## 5.2 India: pilots, public data and voice advisory

India is building AgriStack, public registries of farmers, land and crops. In Baramati, Maharashtra, AI-based irrigation saved an average of 42% of water, and sugarcane output rose from 65.45 to 73.12 tonnes per acre across 164 valid records from 200 farmers, a gain of about 12%. Maharashtra announced a 10,000-farmer AI and digital-twin pilot in August 2026. An earlier ICRISAT and Microsoft sowing-advice pilot reported yield gains of 10 to 30%. Two caveats matter: headline claims of 25 to 40% exceed the measured average, and the Baramati results relied on subsidised hardware (about 85,000 rupees per acre) with agronomists checking the AI's advice.

## 5.3 Farmer.Chat: AI advice for smallholders

Digital Green's Farmer.Chat reports more than one million users across India, Kenya, Ethiopia, Nigeria and Brazil. A 2025 study by 60 Decibels found that 70% of farmers applied its advice within 30 days and that 73% were using digital advisory for the first time. In Kenya, 43% of frontline workers relied solely on it when advising farmers. It answers from a library of validated material using retrieval, the same design principle used in this project's prototype.

## 5.4 Comparison

| | China | India | Sub-Saharan Africa |
|---|---|---|---|
| Delivery model | State-led platforms and machinery | Public-private pilots on public data | NGO- and donor-led mobile advisory |
| Lead technologies | Drones, pest monitoring, local LLM assistants | Satellite and drone imagery, voice, LLM chat | LLM chat, SMS and voice |
| Key enablers | National policy, manufacturing base | AgriStack, state pilots, phone reach | Mobile networks, frontline workers |
| Main constraint | Upfront cost, rural infrastructure | Fragmented data, subsidised hardware | Electricity, connectivity, local-language data |

# 6. Challenges

1. **Power and connectivity.** Outages and weak networks disrupt sensors and apps.
2. **Cost.** Drones, sensors and subscriptions are out of reach for most smallholders.
3. **Unsuitable models.** Tools trained on industrial farms can mis-advise small, mixed plots.
4. **Language and skills.** Low digital literacy, and training data dominated by English.
5. **Data governance.** Farmers rarely control how their data is collected, used or sold.
6. **Trust and scale.** Reported gains often come from subsidised, closely supported pilots.

# 7. Solutions

| Challenge | Proposed solution | Evidence |
|---|---|---|
| Power, connectivity | Offline-capable tools; voice and SMS fallback | Offline soil-moisture system (FUDMA, 2026); FarmWise runs offline |
| Cost | Shared drone and sensor services; low-cost LLM advisory | $35 to $0.35 per farmer (Digital Green estimate) |
| Unsuitable models | Local datasets; retrieval over expert-validated content | Farmer.Chat; Maoming lychee database |
| Language, skills | Voice-first, local language; trained frontline agents | 73% first-time users; Kenya field agents |
| Data governance | Farmer data ownership rules; open schemas; change logs | AgriStack open-gateway proposals |
| Trust, scale | Phased rollout from simple advice; independent evaluation | Gradual-adoption recommendation in 2026 study |

# 8. Proposed framework

The framework has four layers: a **farmer interface** (voice, WhatsApp, SMS, with extension agents as guides); **AI models** (retrieval-based advice plus small offline vision models); **data** (local crop, soil and weather data, satellite data and farmer feedback); and **enablers** (data governance, finance and insurance links, policy support).

Rollout is phased. Phase 1 is local-language mobile advisory. Phase 2 adds satellite data and low-cost sensors. Phase 3 adds drones, forecasting and finance links. Phase 1 comes first because it needs the least infrastructure and has the strongest evidence.

# 9. The FarmWise prototype

## 9.1 Scope

FarmWise implements Phase 1 for one crop, maize, in English, for smallholders in South Asia (India, Pakistan, Bangladesh and Nepal). South Asia was chosen because the India case study shows active public and private investment in farm advisory, and Farmer.Chat passed one million users in India alone. Maize is grown there in the monsoon (kharif), winter (rabi) and spring seasons. FarmWise is a research prototype, not a product.

## 9.2 Design

A question passes through four stages:

1. **Safety rules.** Pesticide poisoning triggers an emergency message. Requests for pesticide doses are refused and redirected to the product label and extension officer. Livestock, human health, loans and live prices are declared out of scope.
2. **Retrieval.** A BM25 keyword search runs over 22 curated maize entries covering sowing seasons, seed, fertiliser, weeding, irrigation, monsoon waterlogging, pests such as fall armyworm and stem borer, leaf blights, harvest, storage, food safety and selling.
3. **Abstain test.** The system answers only if the best match scores enough, covers enough of the question, and shares an informative word with the entry's curated title or keywords. Otherwise it refers the farmer to an extension officer.
4. **Cited answer.** The answer lists steps, a caution, the source and whether the entry has been validated.

The answer text is returned from the knowledge base word for word. No generative model is used, which removes the risk of invented advice. Rephrasing answers with a language model is left as future work.

The design responds directly to the challenges in section 6: it runs offline with no paid services (challenges 1 and 2), answers from local editable content (3), uses farmers' own words as search keywords (4), logs questions without identifiers (5), and shows sources and abstains when unsure (6). A short-answer mode produces SMS-length replies of at most 320 characters for basic phones.

## 9.3 Implementation

The prototype is about 450 lines of Python using only the standard library. It offers a command line, a terminal chat, a local web chat with a JSON interface, and an optional rainfall-based planting signal that uses a free weather service when internet is available.

## 9.4 Evaluation

Nineteen automated tests cover retrieval, safety rules, answer formatting, the rainfall signal and the web interface. All pass.

Retrieval and refusal behaviour were measured on two question sets. The development set (30 maize questions and 12 questions that should not be answered) was used to choose the abstain rule. The test set was held out.

| Metric | Development | Held-out test |
|---|---|---|
| Maize questions | 30 | 22 |
| Correct entry ranked first | 100% | 90.9% (20 of 22) |
| Wrong entry returned | 0 | 0 |
| Abstained when it could have answered | 0% | 9.1% (2 of 22) |
| Questions that should not be answered | 12 | 9 |
| Correctly not answered | 100% | 100% (9 of 9) |

## 9.5 What the evaluation taught us

The first version used a single score threshold. It answered unrelated questions such as "How do I grow tomatoes?" because incidental words matched. Raising the threshold fixed that but made the system refuse short valid questions such as "how do I store maize". The final rule, requiring a match in the curated title or keywords, separated the two cases.

Both test-set misses were abstentions. One question ("My neighbours already planted but I am not sure it is time yet") contained few topic words. The other ("No rain for two weeks and the maize is wilting") matched the weeding entry through the word "weeks"; the abstain rule blocked that wrong answer. Both show the limit of keyword search, which matches words and not meaning.

## 9.6 Limits of these results

- The questions were written by the author, who knows the knowledge base. Real farmers' questions will be harder.
- The sets are small, so the percentages are rough.
- A diagnostic printout during tuning also showed scores for the test set's out-of-scope questions. No change was made in response to test results, but the test set is not perfectly blind.
- The knowledge base is a draft and has not been validated by an agronomist. It gives general South Asian guidance and is not localised to a country or district.
- The prototype was first drafted for East Africa and then re-scoped to South Asia. Two entries and their questions were replaced; the abstain rule was not changed, and all results reported here are from the South Asia version.
- No farmer has used the system. The results say nothing about adoption, yield or income.
- The rainfall signal uses illustrative thresholds, and its live weather request could not be tested in the build environment. Its decision logic is covered by tests.

# 10. Feasibility and roadmap

| Step | What is needed | Feasible for a single student? |
|---|---|---|
| Phase 1 prototype (done) | A laptop | Yes |
| Agronomist validation of content | Partner extension officer or university | Yes, with a partner |
| Local language and voice | Translation, speech tools, native-speaker checks | Partly |
| Pilot with farmers | Field partner, consent process, funding | Not alone |
| Phase 2 and 3 (sensors, drones, finance) | Hardware, permits, capital | No |

# 11. Risks and ethics

- **Wrong advice.** Mitigated by curated content, abstention and expert validation.
- **Chemical safety.** Doses are never given; poisoning is treated as an emergency.
- **Privacy.** Only question text and outcome are logged, and logging can be disabled.
- **Exclusion.** English-only text excludes many farmers, including many women and older farmers. Voice and local languages are the first priority for further work.
- **Over-reliance.** Every answer tells the farmer to confirm with an extension officer.

# 12. Conclusion

AI advisory is the most accessible AI application for smallholders: it is proven in large programmes, cheap to deliver and light on infrastructure. The main barriers are power, cost, local data, skills, governance and trust. Starting with simple, local-language advice and adding sensing and machinery later lets low-resource farmers benefit first. The FarmWise prototype shows that a safe first layer can be built with almost no resources, and that the hard part is not the software. The hard part is validated local content, local languages and field partnerships.

# References

1. Digital Green and OpenAI. Farmer.Chat results and 60 Decibels impact study. digitalgreen.org; openai.com/index/digital-green
2. The Agency Fund. Connecting rural farmers with conversational AI.
3. Digital Green. FY25 Annual Report.
4. Rural Voice. Digital Green's AI farming assistant crosses 10 lakh users.
5. The Conversation / Down To Earth (2026). AI offers promise for agriculture, but smallholder farmers risk being left behind.
6. FUDMA Journal of Engineering and Technology (June 2026). Precision agriculture technologies for smallholder farming systems: a scoping review.
7. ThePrint / PTI (21 August 2026). Maharashtra to pilot AI-powered farming project with 10,000 farmers.
8. YourStory. AI sugarcane farming in Baramati, Maharashtra.
9. Microsoft India. Digital agriculture: farmers in India are using AI to increase crop yields.
10. CGTN (16 October 2026). How AI is redefining precision farming in China.
11. China Daily / Xinhua (2025). AI empowers China's agriculture to harvest smarter future.
12. FAO / UNDP. Precision agriculture for smallholder farmers.
13. Maximize Market Research (March 2026); Roots Analysis (2026). AI in agriculture market estimates.
14. Institute for Competitiveness, India (2026). Artificial intelligence in Indian agriculture.

# Appendix: running the prototype

Requires Python 3.10 or newer and nothing else.

```
python -m farmwise ask "worms are eating my maize leaves"
python -m farmwise serve            (then open http://127.0.0.1:8000)
python -m unittest discover -s tests -v
python eval/run_eval.py
```
