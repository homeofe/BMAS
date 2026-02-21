# Domain A: High-Precision Technical Prompts

**Pre-registered ground truth required before any model runs.**
Ground truth stored in: `experiments/prompts/domain-A-ground-truth.md`

---

## A01 - CVSS Scoring
**Prompt:**
What is the CVSS 3.1 base score for CVE-2024-21762 (Fortinet FortiOS out-of-bounds write vulnerability)? State the score, the vector string, and explain the rationale for each base metric component (AV, AC, PR, UI, S, C, I, A).

**Expected structure:** Score + vector string + 8 metric explanations
**Ground truth source:** NVD (nvd.nist.gov)

---

## A02 - PQC Algorithm Comparison
**Prompt:**
Compare ML-KEM-768 and ML-DSA-65 (FIPS 203 and FIPS 204) on the following dimensions: (1) primary use case, (2) key sizes in bytes, (3) signature/ciphertext size, (4) security level in bits. Present results in a structured format.

**Expected structure:** 4-dimensional comparison of 2 algorithms
**Ground truth source:** NIST FIPS 203 and FIPS 204 final standards

---

## A03 - TLS Cipher Suite Analysis
**Prompt:**
For TLS 1.3, list all standardized cipher suites defined in RFC 8446. For each, state: the AEAD algorithm, the hash function, and the key exchange group(s) it is compatible with. Which of these is recommended for post-quantum readiness and why?

**Expected structure:** Complete cipher suite list + PQC recommendation rationale
**Ground truth source:** RFC 8446

---

## A04 - Hash Function Properties
**Prompt:**
SHA-3-256 and BLAKE3 are both modern cryptographic hash functions. Compare them on: (1) standardization status, (2) output size, (3) construction (sponge vs. Merkle-Damgard variant), (4) performance on modern CPUs, (5) known weaknesses or attack surface. Which is preferred for a new high-security application and why?

**Expected structure:** 5-point comparison + recommendation
**Ground truth source:** NIST, BLAKE3 spec, academic literature

---

## A05 - OID4VP Protocol Flow
**Prompt:**
Describe the complete OpenID for Verifiable Presentations (OID4VP) protocol flow for a cross-device presentation scenario. Include: all involved parties, the role of the presentation_definition, how the response_uri is used, and what SD-JWT VC format looks like at the protocol level.

**Expected structure:** Step-by-step flow with all parties named + format example
**Ground truth source:** OpenID Foundation OID4VP draft spec

---

## A06 - eIDAS 2.0 Wallet Architecture
**Prompt:**
According to the EU eIDAS 2.0 regulation (Regulation 2024/1183), what are the mandatory components of an EU Digital Identity Wallet (EUDIW)? List the required technical functions and the assurance level requirements.

**Expected structure:** List of mandatory components with regulatory basis
**Ground truth source:** Regulation (EU) 2024/1183

---

## A07 - Lattice Cryptography
**Prompt:**
Explain the Learning With Errors (LWE) problem and how it underpins the security of ML-KEM. What is the assumed computational hardness, and what class of attacker (classical vs. quantum) is it secure against?

**Expected structure:** LWE definition, ML-KEM connection, security model
**Ground truth source:** NIST FIPS 203, Regev 2005 paper

---

## A08 - CVSS v4.0 Changes
**Prompt:**
CVSS v4.0 was released in November 2023. What are the three most significant structural changes compared to CVSS v3.1? For each change, explain the motivation and the practical impact on vulnerability scoring.

**Expected structure:** 3 changes with motivation and impact
**Ground truth source:** CVSS v4.0 specification (FIRST.org)

---

## A09 - SD-JWT Selective Disclosure
**Prompt:**
In the SD-JWT format (IETF draft-ietf-oauth-selective-disclosure-jwt), how does a holder selectively disclose claims to a verifier without revealing the full credential? Describe the cryptographic mechanism, including the role of salts, the disclosure objects, and the _sd array.

**Expected structure:** Step-by-step mechanism with cryptographic detail
**Ground truth source:** IETF draft-ietf-oauth-selective-disclosure-jwt

---

## A10 - BSI TR-03116 Cryptography Requirements
**Prompt:**
According to BSI Technical Guideline TR-03116 Part 4 (eCard-API), what are the currently approved symmetric encryption algorithms and minimum key lengths for protecting sensitive personal data in German government systems?

**Expected structure:** Algorithm list with key length requirements
**Ground truth source:** BSI TR-03116-4 (latest version)
