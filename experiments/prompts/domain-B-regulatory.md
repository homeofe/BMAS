# Domain B: Regulatory / Compliance Prompts

**Pre-registered ground truth required before any model runs.**
Ground truth stored in: `experiments/prompts/domain-B-ground-truth.md`

---

## B01 - GDPR Right to Erasure Exceptions
**Prompt:**
Under GDPR Article 17(3), under which conditions can a controller refuse a data subject's request for erasure? List all valid legal bases defined in the article and provide a one-sentence explanation for each.

**Expected structure:** Complete list of Article 17(3) exceptions with explanations
**Ground truth source:** GDPR Regulation (EU) 2016/679, Article 17(3)

---

## B02 - TISAX AL3 Requirements
**Prompt:**
What distinguishes TISAX Assessment Level 3 (AL3) from AL2? What additional controls or assessment requirements apply at AL3, and for what type of information is AL3 relevant?

**Expected structure:** AL2 vs AL3 delta + applicable information types
**Ground truth source:** ENX TISAX Assessment Criteria (VDA ISA)

---

## B03 - BSI C5 Cloud Audit
**Prompt:**
The BSI Cloud Computing Compliance Criteria Catalogue (C5) defines a set of requirements for cloud service providers. Which of the 17 C5 domains is specifically concerned with encryption and key management, and what are the core requirements in that domain?

**Expected structure:** Domain identification + core requirements list
**Ground truth source:** BSI C5:2020

---

## B04 - ISO 27001:2022 Changes
**Prompt:**
ISO 27001:2022 introduced significant changes compared to ISO 27001:2013. What are the three most impactful changes to Annex A controls? For each, describe what was changed and the practical compliance implication.

**Expected structure:** 3 changes with practical implication per change
**Ground truth source:** ISO/IEC 27001:2022

---

## B05 - GDPR Data Breach Notification Timing
**Prompt:**
Under GDPR Article 33, when must a personal data breach be notified to the supervisory authority? What is the exact time limit, when does the clock start, and under what conditions is notification not required?

**Expected structure:** Time limit, start condition, exception conditions
**Ground truth source:** GDPR Article 33

---

## B06 - eIDAS 2.0 vs eIDAS 1.0
**Prompt:**
What are the three most significant legal and technical changes that eIDAS 2.0 (Regulation 2024/1183) introduces compared to the original eIDAS regulation (Regulation 910/2014)?

**Expected structure:** 3 changes with legal basis citation
**Ground truth source:** Regulation (EU) 2024/1183 and Regulation (EU) 910/2014

---

## B07 - GDPR Processor vs Controller
**Prompt:**
Under GDPR, what distinguishes a data controller from a data processor? Can a single entity be both simultaneously for the same data? Cite the relevant GDPR articles.

**Expected structure:** Definition of both roles, distinction, simultaneous role answer with article cites
**Ground truth source:** GDPR Articles 4(7), 4(8), 28, 29

---

## B08 - NIS2 Directive Scope
**Prompt:**
The NIS2 Directive (EU) 2022/2555 defines "essential entities" and "important entities." What criteria determine whether an organization falls into each category? List the sectors explicitly named in Annexes I and II.

**Expected structure:** Criteria for each category + sector lists from Annex I and II
**Ground truth source:** NIS2 Directive (EU) 2022/2555

---

## B09 - DPIA Trigger Conditions
**Prompt:**
Under GDPR Article 35, when is a Data Protection Impact Assessment (DPIA) mandatory? List all conditions that trigger the DPIA requirement and cite any relevant EDPB guidance on high-risk processing.

**Expected structure:** Mandatory trigger conditions + EDPB guidance reference
**Ground truth source:** GDPR Article 35, EDPB Guidelines 09/2022

---

## B10 - SOC 2 Type II vs ISO 27001
**Prompt:**
Compare SOC 2 Type II and ISO 27001 on the following dimensions: (1) issuing body, (2) what is certified (organization vs. system), (3) audit frequency, (4) public availability of the report, (5) geographic adoption. Which is more appropriate for a European cloud service provider targeting enterprise customers in the EU and US?

**Expected structure:** 5-dimensional comparison + recommendation with rationale
**Ground truth source:** AICPA (SOC 2), ISO/IEC 27001:2022
