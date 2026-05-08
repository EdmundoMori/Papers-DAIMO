# Requirements & Competency Questions across 8 SWJ Ontology Papers

Extracted for a PhD student drafting CQs for DAIMO (AI-model governance in data spaces).

---

## Per-paper extractions

### 1. FATO (food allergen traceability)
- **Requirements artefact**: No ORSD. Three narrative "use cases" + a CQ list in an appendix.
- **CQ count**: Not enumerated in main text; main text quotes one CQ per user group (3 examples), says "full list of competency questions is available in Appendix"; appendix is outside the extracted body (N=~24, matching the 24 operational errors used as elicitation seed).
- **CQ format**: Natural-language questions, grouped by target user group (internal auditors / food production operators / food product developers). No CQ numbering codes in the main text.
- **Source of CQs**: Literature review identifying "24 common operational errors in food allergen management"; cross-referenced with the standardised FPIF form and with existing ontologies (EPCIS, FoodOn).
- **Presentation location**: Main-text prose for exemplars; full list in Appendix. Sample SPARQL queries also in Appendix.
- **Example CQs**:
  - "What are the common operational errors that need to be addressed in food allergen management?"
  - "Which operations are needed to improve food allergen management?"
  - "Can a food product, that is not labelled as suitable for a particular consumer group, be identified as such?"
- **Non-functional reqs**: Compatibility with EPCIS/FoodOn/GS1; OOPS! pitfall-free; validated with Themis requirement tests.

### 2. RePlanIT (Digital Product Passports for ICT)
- **Requirements artefact**: Table 6 (appendix) called "Evaluation of RePlanIT with Competency Questions" — effectively a requirement-and-mapping table.
- **CQ count**: 55 CQs.
- **CQ format**: Numbered 1..55, grouped into 6 categories: (1) ICT Device, (2) Hardware Component, (3) Material Composition, (4) CE Strategy, (5) Agent, (6) Indicators. Each row: Number | CQ | RePlanIT Class | Object Property | Data Property.
- **Source of CQs**: Interviews with 11 domain experts across 5 organisations + extensive literature survey (Table 2 in prior work [10]); refined iteratively.
- **Presentation location**: Appendix Table 6 / Table 2 spanning ~10 pages; built knowledge graph used as validation.
- **Example CQs**:
  - "What is the type of the device?"
  - "Where was the device assembled?"
  - "What is the role of the agent associated with the specific device or component?"
- **Non-functional reqs**: FAIR compliance, OOPS! check, Pellet/HermiT consistency, WIDOCO docs, reuse of PROV-O/SOSA/DCAT/MatOnto.

### 3. GloSIS (global soil info)
- **Requirements artefact**: ORSD-like bulleted "Requirements" section (Sec. 3.2). NO competency questions.
- **CQ count**: 0.
- **CQ format**: n/a — replaced by narrative requirements ("The model shall support…").
- **Source**: Standards synthesis (ISO 28258, ANZSoilML, UN FAO guidelines, SOTER/ISRIC, OGC Soil IE); stakeholder discussions.
- **Presentation location**: Section 3.2 main text; wiki for details.
- **Example requirements**:
  - "Re-use ISO 28258 as the base model."
  - "The model shall specify the main 'groups' of soil body properties according to the UN FAO guidelines."
  - "Provide mappings between the newly developed model and all existing data-exchange models."
- **Non-functional reqs**: Linked Data publication, codelists/vocabs as detachable modules, AGROVOC reuse, licensing.

### 4. NutriLink (nutrition/shopping)
- **Requirements artefact**: Motivating scenario + 5 explicitly numbered CQs in main text (Sec. 3.1).
- **CQ count**: 5 CQs.
- **CQ format**: CQ1..CQ5, each a natural-language question followed by a paragraph explaining motivation and data challenges. Each CQ paired with a SPARQL query (.rq files in GitHub) and one UI view in the application.
- **Source of CQs**: Derived from motivating scenario (automated dietary counselling for 76 users in FoodCoach system).
- **Presentation location**: Section 3.1 main text; SPARQL queries in repo; each CQ mapped to a UI view in Sec. 4.
- **Example CQs**:
  - "CQ1. What is the quantity of a specific product in a basket?"
  - "CQ3. What are the historic product- and basket-level Nutri-Scores in an individual's shopping history?"
  - "CQ5. What information about the most recent baskets is needed to generate structured dietary recommendations?"
- **Non-functional reqs**: Multilingual support (via AGROVOC), FAIR alignment, Fair Trade extensibility.

### 5. ANNO (anthropological notation)
- **Requirements artefact**: "Domain specification" step: 3 use cases each with sub-items (a)(b)(c)… acting as "competence questions" (footnote defines them as "queries that the ontology must be able to answer").
- **CQ count**: 12 competence questions = UC1 (5) + UC2 (4) + UC3 (3).
- **CQ format**: Grouped by use case (anatomical annotation / spatial relations / phenotyping). Mixed form: some are imperative ("Query all bone types") and some natural-language questions.
- **Source**: Expert review of literature/ontologies by anthropologists and ontologists together.
- **Presentation location**: Section 3.1 main text, inline enumerated list.
- **Example CQs**:
  - "Query all parts (types) of a specific bone (type)"
  - "What is the relative anatomical location of an anatomical entity in relation to another anatomical entity?"
  - "Which parameters/variables are required to determine a particular phenotype?"
- **Non-functional reqs**: Reuse of GFO top-level; "remain relatively simple and compact" for software integration (three-ontology method).

### 6. SAE (autonomous-driving levels)
- **Requirements artefact**: Section 3 "Problem statement and objectives" — narrative goals only. No ORSD, no CQs.
- **CQ count**: 0.
- **CQ format**: n/a. Ontology validated instead by DL consistency check + worked example (analysis of the SAE-J3016 standard).
- **Source**: The SAE-J3016 standard itself; literature critique of its ambiguities.
- **Presentation location**: Section 3 main text.
- **Non-functional reqs**: Grounded in BFO (ISO/IEC 21838-2); DL/OWL consistency; machine-readable rendering of the standard.

### 7. MAINT (maintenance activity ontology)
- **Requirements artefact**: Numbered CQs introducing an application-level ontology (Sec. 5.1).
- **CQ count**: 4 CQs (Q1–Q4).
- **CQ format**: Q1..Q4, each a two-sentence natural-language question (general question + "specifically" clarification). Paired with SWRL rules (instead of SPARQL) for a data-quality reasoning task over Maintenance Work Orders.
- **Source of CQs**: Real industrial use case (Sec. 3) on MWO data-quality assessment, based on 7 activity words collected from industry data.
- **Presentation location**: Section 5.1 main text.
- **Example CQs**:
  - "Q1. Is the information in a MWO record indicating a replace activity (through various terms) consistent with the expectations of such an activity?"
  - "Q4. What is the likely activity type for a record in which no discernible activity term was recorded?"
- **Non-functional reqs**: Reference-level vs application-level ontology split; SWRL reasoning profile; reproducibility of data-quality assessment.

### 8. EXPL (Explanation Ontology)
- **Requirements artefact**: Two CQ tables (Table 9 task-based, Table 10 application-based) — a rich catalogue with metadata columns.
- **CQ count**: 13 CQs = 6 task-based (Q1–Q6) + 7 application-based (Q1–Q7, one per use case).
- **CQ format**: Q1..Q7 per table, grouped by "Setting" (System Design / System Analysis) in Tab. 9 and by "Use Case" (Food Recommendation / Proactive Retention / Health Survey / Medical Expenditure / Credit Approval) in Tab. 10. Every CQ paired with: Answer, SPARQL Query Length, Property Restrictions Accessed?, Inference Required?, Filter Statements — borrowed from Kendall & McGuinness.
- **Source**: Crafted by authors (XAI expertise) + expert panel of system designers in their lab (task-based utility check); covers 5 use cases from finance, food, healthcare.
- **Presentation location**: Main-text Tab. 9 and Tab. 10; full SPARQL set on companion website.
- **Example CQs**:
  - "Q1. Which AI model(s) is/are capable of generating this explanation type (e.g. trace-based)?"
  - "Q4. Given the system has ranked specific recommendations by comparing different medications, what explanations can be provided for that recommendation?"
  - "Q7. What factors contribute most to a loan applicant's credit approval?"
- **Non-functional reqs**: Apache 2.0 licence; versioned (v2.0 evolution-based evaluation); open catalogue on GitHub Pages; solicits community CQ suggestions.

---

## A) Per-paper summary table

| Paper | # CQs | CQ format | Source | Location | Paired with SPARQL? |
|---|---|---|---|---|---|
| FATO | ~24 (examples in body, full list in appendix) | NL questions grouped by user group | 24 operational errors from literature + FPIF form | Body + Appendix | Yes, appendix |
| RePlanIT | 55 | Numbered 1–55, 6 lifecycle categories, mapped to classes/properties | 11 expert interviews + literature survey | Appendix Table 6 (multi-page) | Indirect (KG evaluation) |
| GloSIS | 0 | Narrative "shall" requirements (ORSD-like bullets) | Standards + stakeholder input | Section 3.2 | No |
| NutriLink | 5 | CQ1–CQ5, NL + motivation paragraph, each tied to a UI view | Motivating scenario (dietary system) | Section 3.1 | Yes (.rq files per CQ in repo) |
| ANNO | 12 | 3 use cases × (a)(b)(c)… sub-queries, mixed imperative/NL | Expert elicitation | Section 3.1 inline list | No (conceptual) |
| SAE | 0 | No CQs; narrative objectives | SAE-J3016 standard | Section 3 | No |
| MAINT | 4 | Q1–Q4, NL + "specifically" clarification | Industry MWO use case | Section 5.1 | Via SWRL rules, not SPARQL |
| EXPL | 13 | Q1–Qn × 2 tables, grouped by Setting / Use Case, with complexity metrics | Authors + expert panel + 5 use cases | Tables 9 & 10 in main text | Yes, fully |

---

## B) Cross-paper observations

- **Median CQ count**: With counts {0, 0, 4, 5, 12, 13, 24, 55}, the median is ~8–9 (between 5 and 12). Typical "explicit CQ" papers land in the 5–15 range; RePlanIT's 55 is an outlier driven by lifecycle-wide coverage.
- **Universality of "numbered + NL + SPARQL"**: Only partially universal. 6/8 papers use explicit numbering (CQ1.. / Q1.. / 1..55). Natural-language phrasing dominates in 5/8 (RePlanIT, NutriLink, EXPL, MAINT, FATO); ANNO mixes imperative queries; GloSIS and SAE omit CQs entirely. Explicit SPARQL pairing appears in only 3/8 (NutriLink, EXPL, FATO-appendix). MAINT substitutes SWRL. So the "triple-pattern" is common but not mandatory.
- **ORSD vs ad-hoc**: None uses a full NeOn-style ORSD template. GloSIS is closest (shall-requirements list). RePlanIT and EXPL use structured CQ tables with mapping columns, which play the ORSD role in practice. The rest are ad-hoc.
- **CQ grouping**: Three patterns observed.
  1. **By module/lifecycle stage** — RePlanIT (device/component/material/CE strategy/agent/indicators); ANNO (annotation/spatial/phenotyping); GloSIS (implicit).
  2. **By actor/user group** — FATO (auditor/operator/developer); EXPL partly (system designer vs interface designer).
  3. **By setting/task** — EXPL Tab. 9 (System Design vs System Analysis); EXPL Tab. 10 (per use case); MAINT (per activity word).
- **What makes a "good" CQ in these papers**: (i) tied to a concrete scenario or real data (NutriLink, MAINT, EXPL); (ii) elicited from multiple sources — experts + literature + standards (RePlanIT, FATO); (iii) mapped explicitly to ontology artefacts (classes/properties in RePlanIT; SPARQL+metrics in EXPL); (iv) non-trivial — EXPL annotates each CQ with whether inference/property restrictions/filters are needed, signalling that a CQ should exercise the ontology's reasoning, not just retrieval; (v) user-validated (EXPL ran CQs past a designer panel).

---

## C) Recommendation for DAIMO

Current state: 19 CQs shown only as codes (CQ-R1..CQ-V5), no NL text, running scenario with ModelProvider / ModelConsumer / PlatformOperator / Evaluator.

**Best pattern to adopt: a hybrid of EXPL (Table 9/10) and RePlanIT (Table 6).** Concretely:

1. **Promote CQ-R1..CQ-V5 to a main-text table**, not codes scattered through prose. Reviewers need to count and read them in one place.
2. **Two-level grouping that matches the running scenario**.
   - Primary grouping: by the requirement letter families already in use (R / V / …) — this preserves traceability to requirement classes (governance, verifiability, etc.). Keep these as "Category" column like RePlanIT's 6 categories.
   - Secondary grouping: tag each CQ with the **actor** asking it (ModelProvider / ModelConsumer / PlatformOperator / Evaluator), following FATO's actor grouping and EXPL's "Setting" column. Reviewers immediately see whose question each CQ serves.
3. **Add natural-language phrasing for every CQ** (non-negotiable — 6/8 papers do this, and reviewers cannot judge coverage from codes alone). Keep each CQ to one sentence, resist multi-part questions (MAINT's "specifically…" compound form reads awkwardly).
4. **Pair each CQ with SPARQL** like NutriLink (one `.rq` file per CQ in the repo) and EXPL (SPARQL on companion site). With 19 CQs this is tractable and directly addresses the "how is it validated?" reviewer concern.
5. **Borrow EXPL's metadata columns**: SPARQL query length, property restrictions accessed?, inference required?, filter statements. This demonstrates each CQ exercises the ontology non-trivially — crucial for a governance ontology whose value rests on reasoning (e.g. deriving ModelConsumer obligations from ModelProvider declarations).
6. **Document elicitation source** per CQ family, RePlanIT-style: which came from the AI Act / data-space standards (IDS, Gaia-X), which from expert interviews, which from the running scenario. Reviewers reward explicit provenance.
7. **Keep it in main text, not appendix** (EXPL, NutriLink, MAINT) — 19 is small enough. Appendices are for the 55-CQ RePlanIT scale.
8. **Declare non-functional requirements separately** (licence, OWL 2 profile, FAIRness, multilingual, reuse of PROV-O/DPV/DCAT) so CQs stay purely about domain coverage, following RePlanIT and EXPL's separation.

**One-sentence template to use per row:**
`[Code] | [Category] | [Actor] | [NL question] | [SPARQL query ref] | [Inference needed? Y/N] | [Source: standard / expert / scenario]`

This is the minimum structure that every strong paper in the set would recognise as adequate.
