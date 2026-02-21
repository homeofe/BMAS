# Domain C: Strategic / Ambiguous Prompts

**No pre-registered ground truth** -- multiple valid answers exist.
Expert evaluation (Emre Kohler) used for synthesis quality assessment.
Ground truth = "expert consensus after synthesis review."

---

## C01 - Zero Trust Architecture Decision
**Prompt:**
For a zero-trust architecture handling cross-border EU government identity verification, should the orchestration layer be implemented as an event-driven microservice mesh or a stateless API gateway chain? The system processes ~10,000 identity verifications per day across 5 EU member states, with GDPR and eIDAS 2.0 compliance requirements. Justify your recommendation.

**Divergence hypothesis:** Models will split between "event-driven" and "API gateway" depending on their training data weighting toward different architectural communities.

---

## C02 - PQC Migration Timeline
**Prompt:**
An enterprise with a 10-year IT infrastructure lifespan is planning a post-quantum cryptography migration. Given that NIST finalized ML-KEM (FIPS 203) and ML-DSA (FIPS 204) in 2024, what should the migration priority order be across these systems: (1) TLS termination, (2) code signing, (3) data-at-rest encryption, (4) email encryption, (5) VPN tunnels? Justify each priority decision.

**Divergence hypothesis:** Different models will rank these differently based on their threat model assumptions (harvest-now-decrypt-later vs. real-time attack vectors).

---

## C03 - Open Source vs. Vendor SIEM
**Prompt:**
An organization with 200 employees, one IT administrator, and a budget of 80,000 EUR/year for security tooling is evaluating whether to deploy an open-source SIEM (e.g., Wazuh, OpenSearch) or a commercial cloud SIEM (e.g., Microsoft Sentinel, Elastic SIEM). What is your recommendation? Consider: operational overhead, detection quality, compliance reporting, and total cost of ownership.

**Divergence hypothesis:** Models may diverge on commercial vs. open-source preference based on training data bias toward vendor documentation.

---

## C04 - Microservice vs. Monolith for Regulated Systems
**Prompt:**
A team of 4 engineers is building a regulatory compliance data platform that must meet GDPR and ISO 27001 requirements. The platform needs to store, process, and report on personal data for 500 enterprise clients. Should they start with a microservice architecture or a well-structured monolith? What are the top 3 risks of each approach in this specific regulatory context?

**Divergence hypothesis:** Strong split expected between models that favor operational simplicity (monolith) vs. those trained on modern cloud-native patterns (microservices).

---

## C05 - Incident Response: Contain vs. Monitor
**Prompt:**
During a security incident, your threat intelligence indicates an attacker has established persistence in your network but has not yet exfiltrated data. You have two options: (A) immediately isolate affected systems, risking operational disruption and alerting the attacker; or (B) monitor silently to gather full attack chain intelligence, accepting the risk of ongoing access. Which approach do you recommend and under what conditions would you switch strategies?

**Divergence hypothesis:** Models may show high divergence based on different risk tolerance frameworks in their training data (aggressive isolation vs. intelligence-first).

---

## C06 - AI in Security Operations
**Prompt:**
Should a Security Operations Center (SOC) with 5 analysts use AI/LLM-based tools for alert triage and first-line investigation? List the top 3 benefits and top 3 risks. Given those, what is your overall recommendation and what governance controls are mandatory before deployment?

**Divergence hypothesis:** Moderate divergence expected; most models will recommend "yes with controls" but will differ on which controls are mandatory.

---

## C07 - Compliance vs. Security Investment
**Prompt:**
An IT leader has 200,000 EUR to invest in security for a mid-sized company. Option A: achieve ISO 27001 certification (estimated cost: 150,000 EUR including consultant + audit). Option B: invest the full amount in technical security controls (EDR, SIEM, PAM, vulnerability management). From a risk reduction perspective, which investment produces better outcomes in years 1-3? Justify with reasoning.

**Divergence hypothesis:** Models will diverge based on how they weight "framework compliance" vs. "technical security" -- a genuine expert debate.

---

## C08 - Identity Federation Design
**Prompt:**
You are designing an identity federation for 5 European government agencies that need to accept each other's credentials. The options are: (A) centralized identity broker, (B) peer-to-peer federation using SAML/OIDC trust anchors, or (C) self-sovereign identity with verifiable credentials (eIDAS 2.0 EUDIW). Each agency has 50,000 citizens. Which architecture do you recommend and why? What are the top failure modes of your chosen approach?

**Divergence hypothesis:** High divergence expected between traditional SAML/OIDC advocates and SSI/EUDIW advocates.

---

## C09 - Security Awareness Training ROI
**Prompt:**
An organization runs annual phishing simulations and security awareness training. The CISO argues this is ineffective and wants to redirect the budget (40,000 EUR/year) to technical controls (email filtering, browser isolation). The HR director argues training is a compliance requirement and builds culture. Who is right? Present both arguments and give your verdict with reasoning.

**Divergence hypothesis:** Models may side with either argument; cultural vs. technical security is a genuine expert divide.

---

## C10 - Open Source AI in Regulated Environments
**Prompt:**
Can open-source LLMs (e.g., Llama 3, Mistral) be deployed in a GDPR-compliant environment for processing personal data, assuming the model runs fully on-premises with no external API calls? What are the three key compliance requirements that must be addressed, and what is the most critical technical control needed?

**Divergence hypothesis:** Models will converge on "yes, possible" but diverge heavily on which compliance requirements are most critical.
