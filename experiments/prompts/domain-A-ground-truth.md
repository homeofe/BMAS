# BMAS Domain A - Pre-Registered Ground Truth

**Domain:** High-Precision Technical
**Pre-registration date:** 2026-02-22
**Status:** LOCKED - do not modify after first model run
**Researcher:** Akido (web-verified against primary sources)
**Human review required:** See items marked UNVERIFIED

---

## A01 - CVE-2024-21762 (Fortinet FortiOS CVSS Scoring)

### Correct Answer Summary
CVE-2024-21762 is an out-of-bounds write (CWE-787) in the sslvpnd component of FortiOS and FortiProxy. Fortinet (as CNA) assigned a CVSS 3.1 base score of **9.6** with vector `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`. NVD had not published its own CVSS assessment as of the research date - the advisory number is FG-IR-24-015. CISA added this to the Known Exploited Vulnerabilities (KEV) catalog on 2024-02-09 with remediation deadline 2024-02-16.

### Key Facts (scoring checklist)
- [ ] CWE: CWE-787 (out-of-bounds write)
- [ ] Attack Vector: Network (AV:N) - remotely exploitable via HTTP
- [ ] Attack Complexity: Low (AC:L)
- [ ] Privileges Required: None (PR:N) - unauthenticated
- [ ] User Interaction: None (UI:N)
- [ ] Scope: Unchanged (S:U) per Fortinet CNA
- [ ] Confidentiality: High / Integrity: High / Availability: High
- [ ] CVSS 3.1 base score: 9.6 (Fortinet CNA) - NVD score pending
- [ ] Affected component: sslvpnd (SSL-VPN daemon)
- [ ] Workaround: Disable SSL VPN entirely (disabling web mode alone is NOT a valid workaround)
- [ ] CISA KEV: Yes, added 2024-02-09
- [ ] Actively exploited in the wild at time of publication

### Score Rationale (metric by metric)
- **AV:N** - exploitable via crafted HTTP requests over the network, no physical/local access needed
- **AC:L** - no special conditions required for exploitation
- **PR:N** - attacker does not need any authentication
- **UI:N** - no victim action required
- **S:U** - exploit stays within the vulnerable component (sslvpnd), does not cross to other components
- **C:H, I:H, A:H** - arbitrary code execution enables full compromise of all three pillars

### Common Errors to Watch For
- Error 1: Citing CVSS score as 9.8 (possible if scope or other metric interpreted differently; note discrepancy)
- Error 2: Claiming NVD has published its own CVSS score (it had not as of research date)
- Error 3: Stating that disabling webmode is a valid workaround (explicitly stated as insufficient in advisory)
- Error 4: Missing that only sslvpnd is the vulnerable component (not all FortiOS)

### Primary Sources
- Fortinet PSIRT: https://fortiguard.com/psirt/FG-IR-24-015
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2024-21762 (no CVSS score published)
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**VERIFICATION NOTE:** Score discrepancy exists between some sources (9.6 vs 9.8). Fortinet (CNA) is authoritative for their own CVEs. Manual verification of exact Fortinet CVSS vector string recommended.

---

## A02 - ML-KEM-768 vs ML-DSA-65 (FIPS 203 / FIPS 204)

### Correct Answer Summary
ML-KEM-768 (FIPS 203) is a key encapsulation mechanism for establishing shared secrets; ML-DSA-65 (FIPS 204) is a digital signature scheme. Both target NIST security Category 3 (roughly equivalent to 192-bit classical security / 128-bit quantum security). Key and ciphertext/signature sizes are precise constants defined in the standards.

### Key Facts (scoring checklist)
- [ ] **ML-KEM-768 primary use:** Key Encapsulation Mechanism (KEM) - establishes shared secret between two parties; NOT for signing
- [ ] **ML-DSA-65 primary use:** Digital signatures - sign and verify messages; NOT for encryption
- [ ] **ML-KEM-768 public key:** 1184 bytes
- [ ] **ML-KEM-768 ciphertext:** 1088 bytes
- [ ] **ML-KEM-768 shared secret:** 32 bytes (output)
- [ ] **ML-DSA-65 public key:** 1952 bytes
- [ ] **ML-DSA-65 private key:** 4032 bytes
- [ ] **ML-DSA-65 signature:** 3309 bytes
- [ ] Both: NIST security Category 3 (192-bit classical equivalent)
- [ ] ML-KEM standardized in FIPS 203 (August 2024 final)
- [ ] ML-DSA standardized in FIPS 204 (August 2024 final)

### Common Errors to Watch For
- Error 1: Confusing ML-KEM and ML-DSA use cases (KEM vs. signature)
- Error 2: Incorrect byte sizes (Kyber-768 had slightly different sizes pre-standardization)
- Error 3: Calling these "CRYSTALS-Kyber" and "CRYSTALS-Dilithium" without noting the official FIPS names
- Error 4: Incorrect security level (Category 3, not Category 2 or 5)
- Error 5: Claiming ML-KEM provides 256-bit quantum security (it is 128-bit quantum / 192-bit classical at level 3)

### Primary Sources
- FIPS 203 (ML-KEM): https://csrc.nist.gov/pubs/fips/203/final
- FIPS 204 (ML-DSA): https://csrc.nist.gov/pubs/fips/204/final
- OQS reference implementation: https://openquantumsafe.org/liboqs/algorithms/kem/ml-kem.html

---

## A03 - TLS 1.3 Cipher Suites (RFC 8446)

### Correct Answer Summary
RFC 8446 (TLS 1.3, August 2018) defines exactly **5 cipher suites**, all using AEAD. Only the first two are MANDATORY for all compliant implementations. TLS 1.3 completely removes all TLS 1.2 cipher suites. Post-quantum readiness requires additional extensions (e.g., key exchange groups using ML-KEM) as TLS 1.3 itself does not include PQC natively.

### Key Facts (scoring checklist)
- [ ] **Exactly 5 cipher suites** defined in RFC 8446 Appendix B.4
- [ ] TLS_AES_128_GCM_SHA256 (0x1301) - MANDATORY
- [ ] TLS_AES_256_GCM_SHA384 (0x1302) - MANDATORY
- [ ] TLS_CHACHA20_POLY1305_SHA256 (0x1303) - defined, not mandatory
- [ ] TLS_AES_128_CCM_SHA256 (0x1304) - defined, not mandatory
- [ ] TLS_AES_128_CCM_8_SHA256 (0x1305) - defined, not mandatory (truncated tag)
- [ ] All suites use AEAD only (no CBC, RC4, 3DES - those are TLS 1.2 only)
- [ ] Cipher suite in TLS 1.3 specifies: AEAD algorithm + hash for HKDF (not key exchange - that is separate)
- [ ] PQC: not natively in TLS 1.3; requires key_share extension with ML-KEM groups (IETF drafts / RFC 9180)
- [ ] TLS_AES_256_GCM_SHA384 recommended for post-quantum readiness (256-bit symmetric security is quantum-safe)

### Common Errors to Watch For
- Error 1: Listing TLS 1.2 cipher suites as TLS 1.3 options
- Error 2: Claiming only 2 cipher suites exist in TLS 1.3 (there are 5 defined, 2 mandatory)
- Error 3: Including key exchange (ECDHE, RSA) in the cipher suite name (TLS 1.3 cipher suites do NOT include KEX)
- Error 4: Claiming TLS 1.3 natively supports PQC (it does not; PQC KEX is via extension groups)
- Error 5: Wrong hex values for suite identifiers

### Primary Sources
- RFC 8446 Appendix B.4: https://datatracker.ietf.org/doc/html/rfc8446#appendix-B.4
- RFC 8446 Section 9.1 (mandatory suites): https://datatracker.ietf.org/doc/html/rfc8446#section-9.1

---

## A04 - SHA-3-256 vs BLAKE3

### Correct Answer Summary
SHA-3-256 is NIST-standardized (FIPS 202, 2015) with a Keccak sponge construction. BLAKE3 (2020) is not NIST-standardized but is production-proven, using a parallelizable Bao tree + ARX (add-rotate-XOR) construction. BLAKE3 is significantly faster on multi-core hardware. Neither has known practical attacks as of 2026. SHA-3-256 is the correct choice for any FIPS-required or government-regulated application.

### Key Facts (scoring checklist)
- [ ] **SHA-3-256 standardization:** NIST FIPS 202 (August 2015) - mandatory for FIPS-compliant systems
- [ ] **BLAKE3 standardization:** None (not NIST-standardized) - no FIPS approval
- [ ] **SHA-3-256 construction:** Keccak sponge (capacity = 512 bits, rate = 1088 bits)
- [ ] **BLAKE3 construction:** Binary tree (Bao) + BLAKE2-based ARX compression; NOT Merkle-Damgard
- [ ] **SHA-3-256 performance:** Sequential, no native parallelism; ~150 MB/s on modern CPUs
- [ ] **BLAKE3 performance:** Parallelizable via SIMD/multi-core; 2-5x faster than SHA-3-256 on large inputs
- [ ] **Both:** immune to length-extension attacks (unlike SHA-256)
- [ ] **Known weaknesses:** None practical for either; SHA-3 has more cryptanalysis history (10+ years)
- [ ] **Recommendation for new high-security application:** SHA-3-256 for FIPS/regulatory compliance; BLAKE3 for speed-critical non-FIPS contexts

### Common Errors to Watch For
- Error 1: Calling BLAKE3 NIST-standardized or FIPS-approved (it is not)
- Error 2: Calling SHA-3-256 "Merkle-Damgard based" (it is sponge-based; SHA-2 is Merkle-Damgard)
- Error 3: Claiming BLAKE3 has known security weaknesses (it does not - only reduced-round theoretical attacks)
- Error 4: Claiming SHA-3-256 is faster (BLAKE3 is faster on multi-core; SHA-3 can be faster only on tiny inputs)

### Primary Sources
- FIPS 202 (SHA-3): https://csrc.nist.gov/publications/detail/fips/202/final
- BLAKE3 specification: https://github.com/BLAKE3-team/BLAKE3-specs

---

## A05 - OID4VP Cross-Device Protocol Flow

### Correct Answer Summary
OID4VP (OpenID for Verifiable Presentations) is the protocol by which a holder wallet presents verifiable credentials to a verifier. In the cross-device flow, the verifier presents a QR code; the wallet scans it, fetches the authorization request via request_uri, gathers matching credentials using the presentation_definition, obtains holder consent, and posts the VP Token (containing the Verifiable Presentation) to the response_uri.

### Key Facts (scoring checklist)
- [ ] **Parties:** Holder (wallet, typically mobile), Verifier (relying party/service), Issuer (issued the credential; not actively involved during presentation)
- [ ] **Cross-device trigger:** Verifier displays QR code or deep link with authorization request URI
- [ ] **request_uri:** URL the wallet fetches to retrieve the signed authorization request object (indirect request pattern)
- [ ] **presentation_definition:** JSON object specifying what credentials/claims the verifier requires (input descriptors, format, constraints)
- [ ] **VP Token:** The wallet's response containing one or more Verifiable Presentations; posted to response_uri
- [ ] **response_uri:** Verifier's HTTPS endpoint that receives the VP Token
- [ ] **SD-JWT VC format at protocol level:** Compact serialization: base64url(header).base64url(payload)~base64url(disclosure1)~...~base64url(disclosureN)
- [ ] **Key binding:** KB-JWT appended to bind presentation to specific verifier session (anti-replay)
- [ ] Based on OAuth 2.0 authorization flow (response_type=vp_token)

### Common Errors to Watch For
- Error 1: Confusing request_uri and response_uri roles (request_uri = wallet fetches request FROM; response_uri = wallet POSTS TO)
- Error 2: Including the Issuer as an active party in the presentation flow (Issuer only involved during issuance, not presentation)
- Error 3: Describing only the same-device flow (QR code scanning is cross-device specific)
- Error 4: Not mentioning key binding JWT (KB-JWT) for cross-device sessions
- Error 5: Calling the response "Authorization Code" (it is vp_token, not a code)

### Primary Sources
- OID4VP specification: https://openid.net/specs/openid-4-verifiable-presentations-1_0.html
- Draft 24: https://openid.net/specs/openid-4-verifiable-presentations-1_0-24.html

---

## A06 - eIDAS 2.0 EUDIW Mandatory Components (Regulation 2024/1183)

### Correct Answer Summary
Article 5a of Regulation (EU) 2024/1183 defines the mandatory functionalities of the European Digital Identity Wallet (EUDIW). Each EU member state must provide at least one wallet within 24 months of the implementing acts entering into force. The wallet must support selective disclosure, qualified electronic signatures, and operate at LoA High.

### Key Facts (scoring checklist)
- [ ] **Legal basis:** Regulation (EU) 2024/1183, Article 5a (amending eIDAS Regulation 910/2014)
- [ ] **Member state obligation:** Must provide at least 1 EUDIW to all natural and legal persons (Article 5a(1))
- [ ] **Deadline:** 24 months after implementing acts enter into force (expected ~December 2026)
- [ ] **Mandatory function (a):** Request, obtain, store, delete, share, and present person identification data and attestations - with **selective disclosure**
- [ ] **Mandatory function (b):** Authenticate to online and offline services
- [ ] **Mandatory function (c):** Sign with **qualified electronic signatures** (QES) and seal with qualified electronic seals
- [ ] **Mandatory function (d):** Share pseudonyms where full identification not legally required
- [ ] **Mandatory function (e):** Download own data and attestations
- [ ] **Mandatory function (f):** Exercise data portability rights
- [ ] **Assurance Level:** HIGH (per Article 8) - required for identity proofing and authentication
- [ ] **Common protocols:** Must support standard interfaces for issuance, validation, and presentation (online and offline)
- [ ] **Voluntary use:** Citizens are not obligated to use the wallet; but public services requiring ID must accept it

### Common Errors to Watch For
- Error 1: Confusing eIDAS 1.0 (Regulation 910/2014) with eIDAS 2.0 (Regulation 2024/1183)
- Error 2: Omitting qualified electronic signatures as a mandatory wallet function
- Error 3: Stating LoA Substantial is sufficient (LoA High is required)
- Error 4: Missing the offline presentation capability (wallets must work offline, not only online)
- Error 5: Claiming wallets are mandatory for citizens (they are voluntary for citizens, mandatory for member states to OFFER)

### Primary Sources
- Regulation (EU) 2024/1183 Article 5a: https://www.european-digital-identity-regulation.com/Article_5a_(Regulation_EU_2024_1183).html
- EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1183

---

## A07 - LWE Problem and ML-KEM Security

### Correct Answer Summary
The Learning With Errors (LWE) problem, introduced by Oded Regev in 2005, is the computational hardness assumption underlying ML-KEM. The problem: given samples (a_i, b_i) where b_i = <a_i, s> + e_i mod q (s is a secret vector, e_i is small noise from a discrete Gaussian distribution), recover s or distinguish these samples from uniform random. ML-KEM uses the Module-LWE variant (LWE over ring modules) for efficiency. LWE is believed to be hard for both classical and quantum attackers.

### Key Facts (scoring checklist)
- [ ] **LWE definition:** Given (a, b = As + e mod q), recover secret s OR distinguish from uniform (decision-LWE)
- [ ] **Key components:** A (public matrix), s (secret vector), e (noise from discrete Gaussian), q (modulus)
- [ ] **Introduced by:** Oded Regev, 2005
- [ ] **ML-KEM variant:** Module-LWE (not plain LWE, not Ring-LWE) - uses matrices of polynomial rings for efficiency via Number Theoretic Transform (NTT)
- [ ] **Classical hardness:** Reduces to worst-case lattice problems (GapSVP, SIVP); no polynomial-time classical algorithm known
- [ ] **Quantum hardness:** Regev's reduction shows solving LWE implies quantum algorithms for worst-case lattice problems; no quantum polynomial-time algorithm known (Shor's algorithm does NOT apply to lattice problems)
- [ ] **Security model:** IND-CCA2 security under Module-LWE assumption (per FIPS 203)
- [ ] **Noise role:** Critical - too small enables recovery attacks (Arora-Ge); parameters carefully tuned in FIPS 203

### Common Errors to Watch For
- Error 1: Claiming Shor's algorithm threatens LWE security (it does not - Shor applies to discrete log/factoring, not lattices)
- Error 2: Confusing Ring-LWE with Module-LWE (ML-KEM uses Module-LWE for better security-performance tradeoff)
- Error 3: Omitting the role of noise (e_i) - the problem is trivially solvable without noise
- Error 4: Incorrectly attributing LWE to a different author or year

### Primary Sources
- Regev 2005 paper: "On Lattices, Learning with Errors, Random Linear Codes, and Cryptography" (ACM STOC 2005)
- FIPS 203 Section 3: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf

---

## A08 - CVSS v4.0 Changes vs CVSS v3.1

### Correct Answer Summary
CVSS v4.0 was released by FIRST in November 2023. The three most significant structural changes are: (1) Attack Complexity split into two parameters, (2) Scope replaced with separate Subsequent System Impact metrics, and (3) Temporal metrics restructured into Threat Metrics with fewer parameters.

### Key Facts (scoring checklist)
- [ ] **Release:** CVSS v4.0 by FIRST, November 2023
- [ ] **Change 1 - AC split:** Attack Complexity (v3.1) split into two separate metrics in v4.0: **Attack Complexity** (evasion of security-enhancing techniques) and **Attack Requirements** (specific deployment conditions enabling the attack). Motivation: v3.1 AC was overloaded with two distinct concepts.
- [ ] **Change 2 - Scope removed:** "Scope" (S: Changed/Unchanged) in v3.1 replaced with separate **Subsequent System Impact Metrics**: SC (Subsequent System Confidentiality), SI (Subsequent System Integrity), SA (Subsequent System Availability). The vulnerable system gets its own VC/VI/VA metrics. Motivation: more precise impact attribution; reduces score inflation from blanket Scope:Changed.
- [ ] **Change 3 - Temporal restructured:** v3.1 Temporal group renamed to **Threat Metrics**. Two metrics removed: Remediation Level (RL) and Report Confidence (RC). Exploit Code Maturity (E) renamed to **Exploit Maturity (E)**; values simplified (High+Functional merged into "Attacked"). Motivation: RL and RC had low discriminatory value in practice.
- [ ] **Practical impact (AC split):** Scoring now separates "is the attack technically complex?" from "does it need a specific precondition in the environment?"
- [ ] **Practical impact (Scope change):** No more binary S:C vs S:U; instead granular per-component impact assessment

### Common Errors to Watch For
- Error 1: Listing score range changes as a major structural change (CVSS v4.0 maintains 0-10 scale)
- Error 2: Not naming the specific metrics that were added/removed
- Error 3: Claiming v4.0 changed the Base Score calculation formula significantly (the changes are in metric structure, not formula type)
- Error 4: Confusing the "Subsequent System" terminology with prior "Changed Scope" without explaining the difference

### Primary Sources
- FIRST CVSS v4.0 specification: https://www.first.org/cvss/v4.0/specification-document
- FIRST CVSS v4.0 FAQ: https://www.first.org/cvss/faq

---

## A09 - SD-JWT Selective Disclosure Mechanism

### Correct Answer Summary
SD-JWT (Selective Disclosure JWT, IETF RFC 9901) enables a holder to selectively reveal individual claims from a credential without exposing the full set. The mechanism uses cryptographic salts, disclosure objects, and a hash array (_sd) in the JWT payload. The holder controls which disclosures to include when presenting the SD-JWT to a verifier.

### Key Facts (scoring checklist)
- [ ] **Salt:** Issuer generates a unique cryptographically random salt (minimum 128 bits / 16 bytes) for each disclosable claim
- [ ] **Disclosure array:** [salt, claim_name, claim_value] - a JSON array serialized and base64url-encoded
- [ ] **Hash computation:** SHA-256 (default, specified by _sd_alg claim) of the base64url-encoded disclosure string
- [ ] **_sd array:** Located in the JWT payload; contains the hashes (digests) of all potentially disclosable claims; replaces the plain claim values
- [ ] **_sd_alg:** Claim in JWT payload specifying the hash algorithm used (default: "sha-256")
- [ ] **Compact format:** SD-JWT = base64url(header).base64url(payload) + ~ + base64url(disclosure1) + ~ + ... (disclosures appended with tilde separator)
- [ ] **Holder presentation:** Holder selects which disclosure arrays to include; verifier recomputes hash and matches against _sd array
- [ ] **Undisclosed claims:** Claims with hashes in _sd but no matching disclosure remain hidden; verifier cannot determine their values
- [ ] **Decoy digests:** Issuer may add fake hashes to _sd to obscure the total number of claims
- [ ] **Anti-replay (KB-JWT):** Key Binding JWT appended as last element; binds presentation to specific verifier nonce

### Common Errors to Watch For
- Error 1: Confusing SD-JWT with JWE (encryption-based) - SD-JWT uses hashing, not encryption
- Error 2: Stating the verifier can see undisclosed claim names (they cannot; only hashes)
- Error 3: Missing the salt's role in preventing dictionary attacks (without salt, verifier could brute-force common values)
- Error 4: Describing disclosure as a single field rather than a [salt, name, value] array
- Error 5: Missing the tilde (~) separator in the compact format

### Primary Sources
- RFC 9901 (SD-JWT): https://datatracker.ietf.org/doc/rfc9901/
- IETF draft: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-selective-disclosure-jwt

---

## A10 - BSI TR-03116-4 Cryptography Requirements

### Correct Answer Summary
BSI TR-03116 Part 4 (eCard-API Framework) specifies cryptographic requirements for German government eCard applications. The approved symmetric encryption algorithm is AES; AES-GCM is the preferred mode. The minimum key length is 128 bits, with 256-bit keys recommended for long-term security. ChaCha20/Poly1305 is not approved under this guideline.

### Key Facts (scoring checklist)
- [ ] **Document:** BSI Technical Guideline TR-03116-4 (eCard-API Framework)
- [ ] **Approved symmetric algorithm:** AES (Advanced Encryption Standard, FIPS 197)
- [ ] **Preferred mode:** AES-GCM (Galois/Counter Mode) - authenticated encryption
- [ ] **Permitted mode with restrictions:** AES-CBC (requires Encrypt-then-MAC, correct IV handling, no padding oracles)
- [ ] **Minimum key length:** 128 bits for AES
- [ ] **Not approved:** ChaCha20/Poly1305 (lacks BSI/FIPS certification; AES-hardware-acceleration preferred)
- [ ] **Context:** eCard applications, German government systems, smart card interfaces

### Common Errors to Watch For
- Error 1: Citing TR-02102 instead of TR-03116-4 (TR-02102 is BSI's general crypto guide; TR-03116-4 is specifically for eCard-API)
- Error 2: Claiming 256-bit is mandatory (128-bit is the minimum; 256-bit is recommended for long-term)
- Error 3: Claiming AES-CCM is approved under TR-03116-4 (UNVERIFIED - primary source needed)
- Error 4: Stating ChaCha20 is approved (it is not in BSI's BSI-aligned standards for government systems)

**VERIFICATION NOTE:** Direct access to the full TR-03116-4 PDF was not possible during research. Key facts derived from secondary sources aligned with BSI TR-02102 series. **Manual verification against the primary BSI document recommended before locking this ground truth entry.**

### Primary Sources
- BSI TR-03116-4: https://www.bsi.bund.de/EN/Topics/ElectrIDDocuments/securID/eCardAPI/ecard_api_node.html
- BSI TR-02102-1 (related): https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-1.pdf

---

## Summary

| Prompt | Verified | Manual Review Needed |
|---|---|---|
| A01 - CVE-2024-21762 | Partial | CVSS score (9.6 vs 9.8 discrepancy) |
| A02 - ML-KEM-768 vs ML-DSA-65 | Yes | No |
| A03 - TLS 1.3 cipher suites | Yes | No |
| A04 - SHA-3-256 vs BLAKE3 | Yes | No |
| A05 - OID4VP protocol flow | Yes | No |
| A06 - eIDAS 2.0 EUDIW | Yes | No |
| A07 - LWE and ML-KEM | Yes | No |
| A08 - CVSS v4.0 changes | Yes | No |
| A09 - SD-JWT mechanism | Yes | No |
| A10 - BSI TR-03116-4 | Partial | Full primary source check needed |

**8/10 fully verified. 2/10 need manual review before experiment runs.**
