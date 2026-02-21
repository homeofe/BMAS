# BMAS Domain B - Pre-Registered Ground Truth

**Domain:** Regulatory / Compliance
**Pre-registration date:** 2026-02-22
**Status:** LOCKED - do not modify after first model run
**Researcher:** Akido (web-verified against primary sources)
**Human review required:** See items marked UNVERIFIED

---

## B01 - GDPR Article 17(3) - Right to Erasure Exceptions

### Correct Answer Summary
Article 17(3) of GDPR (Regulation EU 2016/679) lists five categories under which a controller may refuse a data subject's erasure request. These exceptions apply only when the processing is necessary for one of the listed purposes; they are not blanket overrides and must be evaluated case-by-case.

### Key Facts (scoring checklist)
- [ ] **Legal basis:** GDPR Regulation (EU) 2016/679, Article 17(3) - exactly 5 sub-paragraphs (a) through (e)
- [ ] **(a) Freedom of expression and information:** Processing necessary to exercise the right of freedom of expression and information
- [ ] **(b) Legal obligation:** Processing necessary for compliance with a legal obligation under EU or Member State law
- [ ] **(c) Public interest / health:** Processing necessary for reasons of public interest in the area of public health (Articles 9(2)(h) and (i), and Article 9(3))
- [ ] **(d) Archiving / research / statistics:** Processing necessary for archiving purposes in the public interest, scientific or historical research purposes, or statistical purposes, where erasure would seriously impair or render impossible the achievement of the objectives
- [ ] **(e) Legal claims:** Processing necessary for the establishment, exercise, or defence of legal claims
- [ ] Assessment must be case-by-case; controllers cannot apply exceptions as blanket policies
- [ ] All exceptions require the processing to be NECESSARY (proportionality applies)

### Common Errors to Watch For
- Error 1: Listing fewer than 5 exceptions (all 5 sub-paragraphs must be named)
- Error 2: Confusing Article 17(3) with Article 17(1) (which lists when erasure IS required)
- Error 3: Adding "vital interests" or "legitimate interests" as exceptions (those are lawful bases under Article 6, not Article 17(3) exceptions)
- Error 4: Claiming controllers can refuse erasure simply because they "want to" or based on legitimate interest alone
- Error 5: Conflating UK GDPR / Data Protection Act 2018 exceptions with the EU GDPR text

### Primary Sources
- GDPR Article 17(3): https://gdpr-info.eu/art-17-gdpr/ (Article 17, paragraph 3)
- EUR-Lex full text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679

---

## B02 - TISAX Assessment Level 3 vs AL2

### Correct Answer Summary
TISAX (Trusted Information Security Assessment Exchange) defines three assessment levels. AL2 uses a remote plausibility check of the self-assessment (VDA ISA questionnaire) via web conference. AL3 adds mandatory on-site physical verification of all controls, not just a plausibility check. AL3 applies to very high protection needs, strictly confidential information, and all prototype-related objectives.

### Key Facts (scoring checklist)
- [ ] **AL2 audit method:** Remote (web conference / telephone); plausibility check of self-assessment and evidence; interview with security lead
- [ ] **AL3 audit method:** On-site, comprehensive verification of ALL controls and their operational effectiveness; in-person at company premises
- [ ] **AL2 depth:** Sampled/plausibility-based; no full control-by-control verification unless ambiguities exist
- [ ] **AL3 depth:** Every requirement checked; verifies controls are actively functioning, not just documented
- [ ] **AL3 information types (VDA ISA labels):** Info very high, Strictly confidential, Very high availability, Proto parts, Proto vehicles, Test vehicles, Proto event, Special data
- [ ] **AL2 information types:** Info high, Confidential, High availability, Data
- [ ] **Prototype rule:** ALL prototype-related assessment objectives ALWAYS require AL3, regardless of other protection levels
- [ ] **AL2.5 variant exists:** Full remote check of all controls (AL3 depth but no on-site); results labeled as AL2
- [ ] Control domains are the same at both levels; AL3 applies stricter enforcement and verification depth
- [ ] Duration: AL3 audits are longer and more resource-intensive due to on-site requirements

### Common Errors to Watch For
- Error 1: Claiming AL3 adds entirely new controls not present in AL2 (the control framework is the same; the difference is audit depth and method)
- Error 2: Missing that prototype-related objectives always require AL3 regardless of info classification
- Error 3: Confusing TISAX with ISO 27001 (TISAX is automotive-sector-specific, based on VDA ISA)
- Error 4: Not mentioning the on-site requirement as the core AL3 differentiator

### Primary Sources
- ENX TISAX: https://enx.com/en-US/TISAX/
- CIS-CERT deep dive: https://www.cis-cert.com/en/news/tisax-deep-dive-the-three-assessment-levels/

---

## B03 - BSI C5:2020 - Cryptography and Key Management Domain

### Correct Answer Summary
The BSI C5:2020 (Cloud Computing Compliance Criteria Catalogue) addresses cryptography and key management in the **CRY domain** (Section 5.8). It contains 4 controls (CRY-01 through CRY-04) covering policy, data-in-transit encryption, data-at-rest encryption, and secure key lifecycle management. ISO reference alignment: ISO/IEC 27002 control A.10 (Cryptography).

### Key Facts (scoring checklist)
- [ ] **Domain name:** CRY (Cryptography and Key Management), Section 5.8
- [ ] **Number of controls:** 4 (CRY-01 through CRY-04)
- [ ] **CRY-01:** Cryptographic policy covering key lifecycle (generation, distribution, storage, rotation, revocation, destruction) and security objectives
- [ ] **CRY-02:** Encryption for data in transit (transport encryption, e.g., TLS 1.2/1.3 with strong ciphers)
- [ ] **CRY-03:** Encryption for sensitive data at rest using strong algorithms; key separation for different protection levels
- [ ] **CRY-04:** Secure key management: cryptographically secure key generation, secure storage (e.g., HSMs), access control by least privilege, rotation and revocation procedures
- [ ] **ISO alignment:** ISO/IEC 27002 A.10 Cryptography
- [ ] Applies to cloud service providers (CSPs) operating in Germany and seeking BSI C5 attestation
- [ ] C5 requires Type 2 attestation (controls tested over an observation period by an auditor)

### Common Errors to Watch For
- Error 1: Citing the wrong domain name (e.g., "Information Security" or "Data Protection" instead of CRY)
- Error 2: Listing more than 4 controls or wrong control IDs
- Error 3: Confusing BSI C5 with BSI IT-Grundschutz (different BSI frameworks)
- Error 4: Claiming specific algorithm requirements in CRY (C5 references standards; algorithm specifics are in TR-02102)

### Primary Sources
- BSI C5:2020 (PDF): https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/CloudComputing/ComplianceControlsCatalogue/2020/C5_2020.pdf
- BSI C5 page: https://www.bsi.bund.de/EN/Topics/CloudComputing/Compliance_Criteria_Catalogue/Compliance_Criteria_Catalogue_node.html

---

## B04 - ISO 27001:2022 Annex A Changes vs ISO 27001:2013

### Correct Answer Summary
ISO 27001:2022 (published October 2022) introduced three major structural changes to Annex A: (1) number of controls reduced from 114 to 93, (2) control groupings restructured from 14 domains to 4 themes, and (3) 11 new controls added addressing modern threats including cloud security and threat intelligence.

### Key Facts (scoring checklist)
- [ ] **Control count change:** 114 controls (2013) reduced to 93 controls (2022) through mergers, splits, and renames
- [ ] **Mergers:** Multiple 2013 controls merged into fewer 2022 controls (approximately 57 controls involved in mergers)
- [ ] **Structural change:** 14 control domains (2013) replaced by 4 themes (2022):
  - Organizational controls (37 controls)
  - People controls (8 controls)
  - Physical controls (14 controls)
  - Technological controls (34 controls)
- [ ] **11 new controls** added in 2022 that did not exist in 2013, including:
  - A.5.7 Threat intelligence
  - A.5.23 Information security for use of cloud services
  - A.5.30 ICT readiness for business continuity
  - A.7.4 Physical security monitoring
  - A.8.10 Information deletion
  - A.8.12 Data leakage prevention
- [ ] **Compliance implication of domain restructure:** Organizations must update Statement of Applicability (SoA) to map to new control structure
- [ ] **Compliance implication of new controls:** Gap analysis required; new controls must be assessed and either implemented or justified as not applicable
- [ ] **Compliance implication of threat intelligence control (A.5.7):** Organizations must establish a threat intelligence process, not just reactive monitoring

### Common Errors to Watch For
- Error 1: Stating 114 controls were reduced to 93 without explaining HOW (mergers, not deletions; security is maintained)
- Error 2: Not naming the 4 new themes (Organizational, People, Physical, Technological)
- Error 3: Missing that 11 controls are entirely new (not just renamed from 2013)
- Error 4: Confusing ISO 27001 (ISMS standard, certifiable) with ISO 27002 (implementation guidance, not certifiable)

### Primary Sources
- ISO/IEC 27001:2022: https://www.iso.org/standard/27001 (purchaseable)
- Summary: https://hightable.io/iso-27001-2013-vs-2022/

---

## B05 - GDPR Article 33 - Data Breach Notification

### Correct Answer Summary
GDPR Article 33 requires controllers to notify the competent supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of a personal data breach. The clock starts when the controller becomes aware. Processors must notify controllers without undue delay after their own awareness. Notification is not required if the breach is unlikely to result in a risk to individuals' rights and freedoms.

### Key Facts (scoring checklist)
- [ ] **Time limit:** 72 hours (where feasible)
- [ ] **Standard:** "Without undue delay" - 72 hours is the feasibility target, not an absolute deadline
- [ ] **When clock starts:** When the CONTROLLER becomes aware of the breach (not when the breach occurred)
- [ ] **Processor obligation:** Processor must notify the controller "without undue delay" after becoming aware; this triggers the controller's 72-hour clock
- [ ] **Exception (no notification required):** Breach is unlikely to result in a risk to the rights and freedoms of natural persons
- [ ] **Late notification:** If >72 hours, notification must include reasons for delay (phased notification allowed)
- [ ] **Mandatory documentation:** All breaches must be documented regardless of whether notification is required (Article 33(5))
- [ ] **Notification content minimum (Article 33(3)):**
  - Nature of the breach (categories and approximate number of data subjects and records)
  - Contact details of DPO or other contact point
  - Likely consequences of the breach
  - Measures taken or proposed to address and mitigate effects

### Common Errors to Watch For
- Error 1: Claiming 72 hours is an absolute hard deadline (the law says "where feasible")
- Error 2: Starting the clock from when the breach OCCURRED rather than when the controller BECAME AWARE
- Error 3: Missing the exception (low-risk breaches do not require notification)
- Error 4: Confusing Article 33 (supervisory authority notification) with Article 34 (communication to data subjects, which has a different trigger - high risk, not just risk)
- Error 5: Claiming processors notify the supervisory authority directly (processors notify the controller, not the SA)

### Primary Sources
- GDPR Article 33: https://gdpr-info.eu/art-33-gdpr/
- GDPR Article 34: https://gdpr-info.eu/art-34-gdpr/ (data subject notification - distinct from Art. 33)

---

## B06 - eIDAS 2.0 vs eIDAS 1.0 - Three Major Changes

### Correct Answer Summary
Regulation (EU) 2024/1183 (eIDAS 2.0) amending Regulation 910/2014 (eIDAS 1.0) introduces three major changes: introduction of the EU Digital Identity Wallet (EUDI Wallet) framework, addition of four new qualified trust services, and extension of scope to private-sector services with mandatory acceptance.

### Key Facts (scoring checklist)
- [ ] **Legal basis:** Regulation (EU) 2024/1183 amending Regulation (EU) 910/2014
- [ ] **Change 1 - EUDI Wallet:** eIDAS 2.0 introduces the European Digital Identity Wallet (Article 5a); member states must provide at least one free wallet to all natural and legal persons; citizens can selectively disclose attributes; self-sovereign identity principles applied
- [ ] **Change 2 - New qualified trust services (4 new):**
  - Qualified Electronic Archiving Services
  - Management of Remote Electronic Signature and Seal Creation Devices
  - Qualified Electronic Attestation of Attributes (QEAA)
  - Qualified Electronic Ledgers (blockchain-based)
- [ ] **Change 3 - Expanded scope:** eIDAS 2.0 extends to private-sector services (banking, telecom, transport) that are legally required to accept the EUDI Wallet; eIDAS 1.0 was primarily public-sector focused
- [ ] **eIDAS 1.0 trust services:** Electronic signatures, seals, timestamps, QWAC (certificates for website authentication) - these continue in 2.0
- [ ] **Voluntary for citizens:** Citizens choose whether to use the wallet; mandatory for member states to offer it and for certain services to accept it

### Common Errors to Watch For
- Error 1: Saying eIDAS 2.0 replaces eIDAS 1.0 entirely (it amends it; existing provisions remain)
- Error 2: Listing only the EUDI Wallet without mentioning new qualified trust services
- Error 3: Claiming any of the 4 new services existed under eIDAS 1.0 (they are genuinely new)
- Error 4: Missing the private sector expansion as a major change

### Primary Sources
- Regulation (EU) 2024/1183: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1183
- Regulation (EU) 910/2014: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014R0910

---

## B07 - GDPR Controller vs Processor Distinction

### Correct Answer Summary
GDPR Article 4(7) defines a controller as the entity that "alone or jointly with others, determines the purposes and means of processing." Article 4(8) defines a processor as one that "processes personal data on behalf of the controller." A single entity CAN be a controller for some processing activities and a processor for others (different clients, different datasets). However, for the same specific processing activity, the roles are mutually exclusive: if an entity begins determining purposes and means, it becomes a controller by operation of Article 28(10), not a processor.

### Key Facts (scoring checklist)
- [ ] **Controller definition (Article 4(7)):** Determines the PURPOSES and MEANS of processing; alone or jointly with others (joint controllers possible under Article 26)
- [ ] **Processor definition (Article 4(8)):** Processes personal data ON BEHALF OF the controller; follows controller's instructions
- [ ] **Key distinguishing criterion:** Who decides WHY and HOW the data is processed (purpose + means = controller)
- [ ] **Simultaneous roles for the same activity:** NOT possible; roles are mutually exclusive for a given processing activity
- [ ] **Simultaneous roles in general:** YES possible for different activities - e.g., entity is controller for its employee data, but processor for its clients' data
- [ ] **Article 28(10):** If a processor determines purposes and means, it becomes a controller for that processing
- [ ] **Relevant articles:** 4(7) controller definition, 4(8) processor definition, 26 joint controllers, 28 processor obligations, 28(10) processor becomes controller
- [ ] **Joint controllers (Article 26):** Two or more entities that JOINTLY determine purposes and means are joint controllers; must define responsibilities by agreement

### Common Errors to Watch For
- Error 1: Saying an entity can NEVER play both roles (it can, for different processing activities)
- Error 2: Saying an entity CAN be both simultaneously for the SAME processing activity (it cannot)
- Error 3: Missing Article 28(10) which defines the transformation from processor to controller
- Error 4: Missing joint controller (Article 26) as a distinct concept

### Primary Sources
- GDPR Article 4(7) and 4(8): https://gdpr-info.eu/art-4-gdpr/
- GDPR Article 28: https://gdpr-info.eu/art-28-gdpr/
- GDPR Article 26: https://gdpr-info.eu/art-26-gdpr/
- European Commission guidance: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/controllerprocessor/

---

## B08 - NIS2 Directive - Essential vs Important Entities

### Correct Answer Summary
NIS2 Directive (EU) 2022/2555 classifies entities based on sector (Annex I or II) and size. Large entities in Annex I sectors are essential; medium entities in Annex I and medium/large entities in Annex II are important. Some entities qualify as essential regardless of size (e.g., DNS providers, top-level domain registries, qualified trust service providers). Member states must establish entity lists by April 17, 2025.

### Key Facts (scoring checklist)
- [ ] **Essential entities:** Large enterprises (250+ employees OR €50M+ turnover OR €43M+ balance sheet) in Annex I sectors
- [ ] **Essential entities regardless of size:** DNS service providers, TLD name registries, qualified trust service providers, public electronic communications networks (medium or above), central government public administration entities
- [ ] **Important entities:** Medium enterprises (50-249 employees OR €10-50M turnover) in Annex I sectors; medium or large enterprises in Annex II sectors
- [ ] **Supervision:** Essential = proactive ex-ante; Important = reactive ex-post
- [ ] **Maximum penalties:** Essential = €10M or 2% of global annual turnover; Important = €7M or 1.4%
- [ ] **Annex I sectors (11 high-criticality):** Energy, Transport, Banking, Financial market infrastructures, Health, Drinking water, Wastewater, Digital infrastructure, Public administration (central government), Space, Research organisations (applied R&D for commercial exploitation)
- [ ] **Annex II sectors (7 important):** Postal and courier services, Waste management, Chemicals, Food production/processing/distribution, Manufacturing of critical products (medical devices, computers, electronics, vehicles), Digital providers (online marketplaces, search engines, social networks), Research (other than Annex I)
- [ ] **Member state list deadline:** April 17, 2025

### Common Errors to Watch For
- Error 1: Listing incorrect sectors (e.g., putting manufacturing in Annex I when it is in Annex II)
- Error 2: Using wrong size thresholds (confusing EU SME definition: medium = 50-249 employees, large = 250+)
- Error 3: Missing "regardless of size" entities that are always essential
- Error 4: Confusing NIS2 with DORA (Digital Operational Resilience Act, which is for financial sector specifically)
- Error 5: Stating the same supervision model for both categories (different: proactive vs. reactive)

### Primary Sources
- NIS2 Directive (EU) 2022/2555: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555
- NIS2 Article 3: https://www.nis-2-directive.com/NIS_2_Directive_Article_3.html

---

## B09 - GDPR Article 35 - DPIA Mandatory Triggers

### Correct Answer Summary
GDPR Article 35 requires a Data Protection Impact Assessment (DPIA) prior to processing that is likely to result in high risk to individuals. Article 35(3) defines three absolute triggers where a DPIA is always mandatory. The EDPB (and previously the Article 29 Working Party) identified 9 criteria for high-risk processing; if two or more criteria apply, a DPIA is typically required.

### Key Facts (scoring checklist)
- [ ] **General trigger (Article 35(1)):** Processing "likely to result in a high risk to the rights and freedoms of natural persons," especially using new technologies
- [ ] **Absolute trigger 1 (Article 35(3)(a)):** Systematic and extensive profiling of natural persons, based on automated processing, that produces legal effects or similarly significant effects
- [ ] **Absolute trigger 2 (Article 35(3)(b)):** Large-scale processing of special categories of data (Article 9: health, biometric, genetic, etc.) or criminal convictions data (Article 10)
- [ ] **Absolute trigger 3 (Article 35(3)(c)):** Systematic monitoring of publicly accessible areas on a large scale
- [ ] **EDPB 9 criteria (2 or more = likely mandatory DPIA):**
  1. Evaluation or scoring (profiling)
  2. Automated decision-making with legal or significant effects
  3. Systematic monitoring
  4. Sensitive data or highly personal data
  5. Large-scale processing
  6. Matching or combining datasets
  7. Data concerning vulnerable subjects (children, employees, patients)
  8. Innovative use or application of technological/organisational solutions
  9. Processing that prevents data subjects from exercising rights or accessing services
- [ ] **DPIA not required:** Small-scale processing unlikely to result in high risk; processing mandated by law where an equivalent DPIA already exists (Article 35(10))
- [ ] **EDPB guidance:** Supersedes WP29 Guidelines on DPIA (WP248); EDPB Guidelines 09/2022 address "legitimate interests" as lawful basis (separate from DPIA triggers)

### Common Errors to Watch For
- Error 1: Listing only 3 triggers without mentioning the EDPB 9 criteria
- Error 2: Confusing GDPR Article 35 (DPIA) with Article 32 (security of processing)
- Error 3: Stating DPIA is mandatory for ALL special category data (only when processed at large scale)
- Error 4: Missing the "two or more criteria" threshold from EDPB guidance
- Error 5: Referencing EDPB Guidelines 09/2022 incorrectly (that guideline addresses legitimate interests, not DPIA specifically; WP248 is the DPIA-specific guideline)

**VERIFICATION NOTE:** EDPB Guidelines 09/2022 address legitimate interests (Article 6(1)(f)), not DPIA specifically. The DPIA-specific guidance is WP248 rev.01 (Article 29 WP, endorsed by EDPB). Manual verification of the correct guideline number recommended.

### Primary Sources
- GDPR Article 35: https://gdpr-info.eu/art-35-gdpr/
- WP248 rev.01 (DPIA guidelines): https://ec.europa.eu/newsroom/article29/items/611236
- EDPB Guidelines index: https://edpb.europa.eu/our-work-tools/our-documents/guidelines_en

---

## B10 - SOC 2 Type II vs ISO 27001

### Correct Answer Summary
SOC 2 Type II and ISO 27001 are complementary but distinct frameworks. For a European cloud service provider targeting both EU and US enterprise customers, ISO 27001 is the primary recommendation due to its global recognition; SOC 2 Type II is recommended as a supplement for US market credibility. Obtaining both is increasingly common for companies serving both markets.

### Key Facts (scoring checklist)
- [ ] **SOC 2 issuing body:** AICPA (American Institute of Certified Public Accountants); report issued by an independent CPA firm
- [ ] **ISO 27001 issuing body:** ISO (International Organization for Standardization); certification issued by an accredited certification body (e.g., TUV, BSI Group, DNV)
- [ ] **What SOC 2 certifies:** Operational effectiveness of controls based on Trust Services Criteria (Security mandatory; Availability, Processing Integrity, Confidentiality, Privacy optional) - service-specific scope
- [ ] **What ISO 27001 certifies:** The entire Information Security Management System (ISMS) of an organization - organizational scope
- [ ] **SOC 2 audit frequency:** Annual re-audit; 6-12 month observation period for Type II
- [ ] **ISO 27001 audit frequency:** Initial 2-stage certification; annual surveillance audits; full re-certification every 3 years
- [ ] **SOC 2 report availability:** NOT publicly available; shared confidentially with customers/prospects on request
- [ ] **ISO 27001 certificate availability:** Publicly searchable in accreditation body registers; shows overall compliance (no control-level details)
- [ ] **SOC 2 geographic adoption:** Primarily US; standard request from American SaaS customers
- [ ] **ISO 27001 geographic adoption:** Global; widely recognized in EU, APAC, Middle East; dominant in European enterprise procurement
- [ ] **Recommendation for EU+US provider:** ISO 27001 as primary (EU recognition, global credibility); SOC 2 Type II as supplement for US market; both are increasingly expected by enterprise customers in both markets

### Common Errors to Watch For
- Error 1: Stating SOC 2 report is publicly available (it is not; shared confidentially)
- Error 2: Claiming ISO 27001 provides control-level pass/fail details (it does not; only overall certification status is public)
- Error 3: Stating ISO 27001 requires annual recertification (surveillance annually, full recertification every 3 years)
- Error 4: Recommending only SOC 2 for an EU provider (ISO 27001 is the correct primary choice for European/global recognition)

### Primary Sources
- SOC 2 (AICPA): https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2
- ISO/IEC 27001: https://www.iso.org/standard/27001

---

## Summary

| Prompt | Verified | Manual Review Needed |
|---|---|---|
| B01 - GDPR Article 17(3) exceptions | Yes | No |
| B02 - TISAX AL3 vs AL2 | Yes | No |
| B03 - BSI C5 CRY domain | Yes | No |
| B04 - ISO 27001:2022 Annex A changes | Yes | No |
| B05 - GDPR Article 33 breach notification | Yes | No |
| B06 - eIDAS 2.0 vs eIDAS 1.0 | Yes | No |
| B07 - Controller vs Processor | Yes | No |
| B08 - NIS2 essential vs important entities | Yes | No |
| B09 - GDPR Article 35 DPIA triggers | Partial | EDPB guideline number (09/2022 vs WP248) |
| B10 - SOC 2 Type II vs ISO 27001 | Yes | No |

**9/10 fully verified. 1/10 needs minor clarification on EDPB guideline reference number.**
