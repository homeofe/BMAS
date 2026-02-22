#!/usr/bin/env python3
"""
Fix all paper section files to reflect the real experiment:
- 5 models → 12 models (M1-M12)
- 30 prompts → 45 prompts (15 per domain)
- 150 runs → 540 runs
- 27 prompts (pilot) → 45 prompts
- 135 responses → 540 responses
- Majority vote threshold: three of five → seven of twelve
- LLM-as-Judge: sixth model → thirteenth model
- Update real outlier and domain stats
"""

import os
import re

SECTIONS_DIR = "/home/chef-linux/.openclaw/workspace/BMAS/paper/sections"

# --------------------------------------------------------------------------
# Language-specific substitution tables
# Each entry: (pattern, replacement) — applied via re.sub
# --------------------------------------------------------------------------

SUBSTITUTIONS = {
    # ---- English (root sections/*.md) ----
    "en": [
        # Model counts
        (r"five frontier LLMs", "twelve frontier LLMs"),
        (r"five frontier LLM", "twelve frontier LLMs"),
        (r"five state-of-the-art LLMs", "twelve state-of-the-art LLMs"),
        (r"five state-of-the-art LLM", "twelve state-of-the-art LLMs"),
        (r"\bfive LLMs\b", "twelve LLMs"),
        (r"\b5 LLMs\b", "12 LLMs"),
        (r"We evaluate five", "We evaluate twelve"),
        (r"five models used represent", "twelve models used represent"),
        (r"The five models", "The twelve models"),
        (r"five independent expert systems", "twelve independent expert systems"),
        (r"using five Anthropic models", "using twelve Anthropic models"),
        (r"\bfive models\b", "twelve models"),
        (r"\bfive model\b", "twelve models"),
        # Prompt counts
        (r"30 prompts across three domain strata", "45 prompts across three domain strata"),
        (r"30 prompts across three domains", "45 prompts across three domains"),
        (r"\b30 prompts\b", "45 prompts"),
        (r"\b30 Prompts\b", "45 Prompts"),
        (r"10 per domain", "15 per domain"),
        (r"10-per-domain", "15-per-domain"),
        # Run counts
        (r"150-run experiment", "540-run experiment"),
        (r"150 runs", "540 runs"),
        (r"150 run", "540 runs"),
        (r"\(30 prompts x 5 models\)", "(45 prompts x 12 models)"),
        (r"30 prompts x 5 models", "45 prompts x 12 models"),
        # Pilot-era 27-prompt references → 45
        (r"Across all 27 prompts", "Across all 45 prompts"),
        (r"all 27 prompts", "all 45 prompts"),
        (r"\b27 prompts\b", "45 prompts"),
        (r"\b27 Prompts\b", "45 Prompts"),
        # Response counts
        (r"135 total model responses", "540 total model responses"),
        (r"yielding 135 total model responses", "yielding 540 total model responses"),
        (r"135 model responses", "540 model responses"),
        # Majority vote
        (r"at least 60% of models \(three of five\)", "at least 58% of models (seven of twelve)"),
        (r"three of five", "seven of twelve"),
        # LLM-as-Judge
        (r"All five anonymized responses", "All twelve anonymized responses"),
        (r"five anonymized responses", "twelve anonymized responses"),
        (r"five blind responses", "twelve blind responses"),
        (r"a sixth model instance", "a thirteenth model instance"),
        (r"a sixth model", "a thirteenth model"),
        (r"synthesizes the five blind", "synthesizes the twelve blind"),
        (r"pipeline BMAS with 5 models", "pipeline BMAS with 12 models"),
        (r"N parallel calls", "12 parallel calls"),
        # Sample size
        (r"With 30 prompts across three domains", "With 45 prompts across three domains"),
        # Domain A size reference
        (r"10 prompts requiring", "15 prompts requiring"),
        # Model table — description of providers
        (r"from four distinct providers:", "from four distinct providers (Anthropic, OpenAI, Google, Perplexity):"),
        # Results section: old pilot cosine/bertscore numbers
        (r"mean cosine similarity of 0\.832 \(SD = 0\.045\)", "mean cosine similarity of 0.479 (SD = 0.038)"),
        (r"BERTScore F1 mean was 0\.841", "BERTScore F1 mean was 0.811"),
        (r"mean cosine similarity of 0\.851", "mean cosine similarity of 0.508"),
        (r"cosine similarity drops to 0\.845", "cosine similarity drops to 0.485"),
        # Outlier model references (pilot data)
        (r"Gemini-2\.5 \(M4\) had the highest outlier rate at 0\.30", "Sonar Deep Research (M6) had the highest outlier rate at 0.11"),
        (r"while Sonar \(M5\) had the lowest at 0\.07", "while Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10), and Claude Sonnet 4.5 (M12) had zero outlier runs"),
        # full experiment line in 04-results
        (r"The full BMAS experiment comprised 27 prompts across three domain strata, each evaluated by five models, yielding 135 total model responses\.",
         "The full BMAS experiment comprised 45 prompts across three domain strata, each evaluated by twelve models, yielding 540 total model responses."),
        # Table headers
        (r"all 30 prompts\)", "all 45 prompts)"),
        # Conclusion specific line
        (r"Across 30 prompts, Models A and B", "Across 45 prompts, Domains A and B"),
        # synthesis: N calls
        (r"after the N initial parallel calls\.", "after the 12 initial parallel calls."),
        (r"with 5 models\.", "with 12 models."),
        # README in sections
        (r"27 prompts, 135 model responses", "45 prompts, 540 model responses"),
    ],

    # ---- German (de/) ----
    "de": [
        (r"fünf frontier LLMs", "zwölf frontier LLMs"),
        (r"fünf LLMs", "zwölf LLMs"),
        (r"5 LLMs", "12 LLMs"),
        (r"fünf LLM", "zwölf LLM"),
        (r"5 LLM", "12 LLM"),
        (r"Wir evaluieren fünf", "Wir evaluieren zwölf"),
        (r"fünf modernste", "zwölf modernste"),
        (r"Die fünf Modelle", "Die zwölf Modelle"),
        (r"fünf unabhängige Expertensysteme", "zwölf unabhängige Expertensysteme"),
        (r"fünf Anthropic.Modelle", "zwölf Anthropic-Modelle"),
        (r"\bfünf Modelle\b", "zwölf Modelle"),
        (r"\bfünf Modell\b", "zwölf Modelle"),
        (r"\b30 Prompts\b", "45 Prompts"),
        (r"\b30 prompts\b", "45 Prompts"),
        (r"10 pro Domäne", "15 pro Domäne"),
        (r"10 Prompts pro Domäne", "15 Prompts pro Domäne"),
        (r"150-Läufe-Experiment", "540-Läufe-Experiment"),
        (r"150 Läufen", "540 Läufen"),
        (r"150 Läufe", "540 Läufe"),
        (r"\(30 Prompts x 5 Modelle\)", "(45 Prompts x 12 Modelle)"),
        (r"30 Prompts x 5 Modelle", "45 Prompts x 12 Modelle"),
        (r"Über alle 27 Prompts", "Über alle 45 Prompts"),
        (r"alle 27 Prompts", "alle 45 Prompts"),
        (r"\b27 Prompts\b", "45 Prompts"),
        (r"\b27 prompts\b", "45 Prompts"),
        (r"135 Modellantworten", "540 Modellantworten"),
        (r"mindestens 60% der Modelle \(drei von fünf\)", "mindestens 58% der Modelle (sieben von zwölf)"),
        (r"drei von fünf", "sieben von zwölf"),
        (r"Alle fünf anonymisierten Antworten", "Alle zwölf anonymisierten Antworten"),
        (r"fünf anonymisierten Antworten", "zwölf anonymisierten Antworten"),
        (r"fünf anonymisierten", "zwölf anonymisierten"),
        (r"fünf blinden Antworten", "zwölf blinden Antworten"),
        (r"ein sechstes Modell", "ein dreizehntes Modell"),
        (r"einem sechsten Modell", "einem dreizehnten Modell"),
        (r"Mit 30 Prompts über drei Domänen", "Mit 45 Prompts über drei Domänen"),
        (r"Über 30 Prompts", "Über 45 Prompts"),
        (r"Das vollständige BMAS-Experiment umfasste 27 Prompts über drei Domänenschichten, die jeweils von fünf Modellen bewertet wurden, was insgesamt 135 Modellantworten ergibt\.",
         "Das vollständige BMAS-Experiment umfasste 45 Prompts über drei Domänenschichten, die jeweils von zwölf Modellen bewertet wurden, was insgesamt 540 Modellantworten ergibt."),
        (r"alle 27 Prompts\)", "alle 45 Prompts)"),
        (r"27 Prompts, 135 Modellantworten", "45 Prompts, 540 Modellantworten"),
        (r"Gemini-2\.5 \(M4\) hatte die höchste Ausreißerrate von 0,30", "Sonar Deep Research (M6) hatte die höchste Ausreißerrate von 0,11"),
        (r"während Sonar \(M5\) die niedrigste von 0,07 hatte", "während Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10) und Claude Sonnet 4.5 (M12) keine Ausreißer hatten"),
    ],

    # ---- French (fr/) ----
    "fr": [
        (r"cinq LLMs frontier", "douze LLMs frontier"),
        (r"cinq LLMs de pointe", "douze LLMs de pointe"),
        (r"cinq LLMs", "douze LLMs"),
        (r"cinq LLM", "douze LLM"),
        (r"5 LLMs", "12 LLMs"),
        (r"Nous évaluons cinq", "Nous évaluons douze"),
        (r"Les cinq modèles", "Les douze modèles"),
        (r"cinq systèmes experts indépendants", "douze systèmes experts indépendants"),
        (r"cinq modèles Anthropic", "douze modèles Anthropic"),
        (r"\bcinq modèles\b", "douze modèles"),
        (r"\bcinq modèle\b", "douze modèles"),
        (r"\b30 prompts\b", "45 prompts"),
        (r"10 par domaine", "15 par domaine"),
        (r"10 prompts par domaine", "15 prompts par domaine"),
        (r"expérience de 150 lancements", "expérience de 540 lancements"),
        (r"150 lancements", "540 lancements"),
        (r"\(30 prompts x 5 modèles\)", "(45 prompts x 12 modèles)"),
        (r"30 prompts x 5 modèles", "45 prompts x 12 modèles"),
        (r"Sur les 27 prompts", "Sur les 45 prompts"),
        (r"tous les 27 prompts", "tous les 45 prompts"),
        (r"\b27 prompts\b", "45 prompts"),
        (r"135 réponses de modèles au total", "540 réponses de modèles au total"),
        (r"produisant 135 réponses", "produisant 540 réponses"),
        (r"au moins 60 % des modèles \(trois sur cinq\)", "au moins 58 % des modèles (sept sur douze)"),
        (r"trois sur cinq", "sept sur douze"),
        (r"Toutes les cinq réponses anonymisées", "Toutes les douze réponses anonymisées"),
        (r"cinq réponses anonymisées", "douze réponses anonymisées"),
        (r"cinq réponses aveugles", "douze réponses aveugles"),
        (r"un sixième modèle", "un treizième modèle"),
        (r"une sixième instance", "une treizième instance"),
        (r"Avec 30 prompts sur trois domaines", "Avec 45 prompts sur trois domaines"),
        (r"Sur 30 prompts", "Sur 45 prompts"),
        (r"L'expérience BMAS complète comprenait 27 prompts sur trois strates de domaine, évalués chacun par cinq modèles, produisant 135 réponses de modèles au total\.",
         "L'expérience BMAS complète comprenait 45 prompts sur trois strates de domaine, évalués chacun par douze modèles, produisant 540 réponses de modèles au total."),
        (r"tous les 27 prompts\)", "tous les 45 prompts)"),
        (r"Gemini-2\.5 \(M4\) avait le taux d'anomalie le plus élevé à 0,30", "Sonar Deep Research (M6) avait le taux d'anomalie le plus élevé à 0,11"),
        (r"tandis que Sonar \(M5\) avait le plus bas à 0,07", "tandis que Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10) et Claude Sonnet 4.5 (M12) n'avaient aucune anomalie"),
        (r"avec 5 modèles\.", "avec 12 modèles."),
        (r"après les N appels parallèles initiaux\.", "après les 12 appels parallèles initiaux."),
    ],

    # ---- Spanish (es/) ----
    "es": [
        (r"cinco LLMs frontier", "doce LLMs frontier"),
        (r"cinco LLMs de última generación", "doce LLMs de última generación"),
        (r"cinco LLMs", "doce LLMs"),
        (r"cinco LLM", "doce LLM"),
        (r"5 LLMs", "12 LLMs"),
        (r"Evaluamos cinco", "Evaluamos doce"),
        (r"Los cinco modelos", "Los doce modelos"),
        (r"cinco sistemas expertos independientes", "doce sistemas expertos independientes"),
        (r"cinco modelos Anthropic", "doce modelos Anthropic"),
        (r"\bcinco modelos\b", "doce modelos"),
        (r"\bcinco modelo\b", "doce modelos"),
        (r"\b30 prompts\b", "45 prompts"),
        (r"10 por dominio", "15 por dominio"),
        (r"experimento de 150 ejecuciones", "experimento de 540 ejecuciones"),
        (r"150 ejecuciones", "540 ejecuciones"),
        (r"\(30 prompts x 5 modelos\)", "(45 prompts x 12 modelos)"),
        (r"30 prompts x 5 modelos", "45 prompts x 12 modelos"),
        (r"En los 27 prompts", "En los 45 prompts"),
        (r"los 27 prompts", "los 45 prompts"),
        (r"\b27 prompts\b", "45 prompts"),
        (r"135 respuestas de modelos en total", "540 respuestas de modelos en total"),
        (r"produciendo 135 respuestas", "produciendo 540 respuestas"),
        (r"al menos el 60% de los modelos \(tres de cinco\)", "al menos el 58% de los modelos (siete de doce)"),
        (r"tres de cinco", "siete de doce"),
        (r"Todas las cinco respuestas anonimizadas", "Todas las doce respuestas anonimizadas"),
        (r"cinco respuestas anonimizadas", "doce respuestas anonimizadas"),
        (r"cinco respuestas ciegas", "doce respuestas ciegas"),
        (r"un sexto modelo", "un decimotercer modelo"),
        (r"Con 30 prompts en tres dominios", "Con 45 prompts en tres dominios"),
        (r"En 30 prompts", "En 45 prompts"),
        (r"El experimento BMAS completo comprendió 27 prompts en tres estratos de dominio, evaluados cada uno por cinco modelos, produciendo 135 respuestas de modelos en total\.",
         "El experimento BMAS completo comprendió 45 prompts en tres estratos de dominio, evaluados cada uno por doce modelos, produciendo 540 respuestas de modelos en total."),
        (r"todos los 27 prompts\)", "todos los 45 prompts)"),
        (r"Gemini-2\.5 \(M4\) tuvo la tasa de valores atípicos más alta en 0,30", "Sonar Deep Research (M6) tuvo la tasa de valores atípicos más alta en 0,11"),
        (r"mientras que Sonar \(M5\) tuvo la más baja en 0,07", "mientras que Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10) y Claude Sonnet 4.5 (M12) no tuvieron ningún valor atípico"),
        (r"con 5 modelos\.", "con 12 modelos."),
    ],

    # ---- Italian (it/) ----
    "it": [
        (r"cinque LLM frontier", "dodici LLM frontier"),
        (r"cinque LLM all'avanguardia", "dodici LLM all'avanguardia"),
        (r"cinque LLM", "dodici LLM"),
        (r"5 LLM", "12 LLM"),
        (r"Valutiamo cinque", "Valutiamo dodici"),
        (r"I cinque modelli", "I dodici modelli"),
        (r"cinque sistemi esperti indipendenti", "dodici sistemi esperti indipendenti"),
        (r"cinque modelli Anthropic", "dodici modelli Anthropic"),
        (r"\bcinque modelli\b", "dodici modelli"),
        (r"\bcinque modello\b", "dodici modelli"),
        (r"\b30 prompt\b", "45 prompt"),
        (r"10 per dominio", "15 per dominio"),
        (r"esperimento con 150 esecuzioni", "esperimento con 540 esecuzioni"),
        (r"150 esecuzioni", "540 esecuzioni"),
        (r"\(30 prompt x 5 modelli\)", "(45 prompt x 12 modelli)"),
        (r"30 prompt x 5 modelli", "45 prompt x 12 modelli"),
        (r"Su tutti i 27 prompt", "Su tutti i 45 prompt"),
        (r"tutti i 27 prompt", "tutti i 45 prompt"),
        (r"\b27 prompt\b", "45 prompt"),
        (r"135 risposte di modelli", "540 risposte di modelli"),
        (r"producendo in totale 135", "producendo in totale 540"),
        (r"almeno il 60% dei modelli \(tre su cinque\)", "almeno il 58% dei modelli (sette su dodici)"),
        (r"tre su cinque", "sette su dodici"),
        (r"Tutte le cinque risposte anonimizzate", "Tutte le dodici risposte anonimizzate"),
        (r"cinque risposte anonimizzate", "dodici risposte anonimizzate"),
        (r"cinque risposte cieche", "dodici risposte cieche"),
        (r"un sesto modello", "un tredicesimo modello"),
        (r"Con 30 prompt su tre domini", "Con 45 prompt su tre domini"),
        (r"Su 30 prompt", "Su 45 prompt"),
        (r"L'esperimento BMAS completo comprendeva 27 prompt su tre strati di dominio, ognuno valutato da cinque modelli, producendo in totale 135 risposte di modelli\.",
         "L'esperimento BMAS completo comprendeva 45 prompt su tre strati di dominio, ognuno valutato da dodici modelli, producendo in totale 540 risposte di modelli."),
        (r"tutti i 27 prompt\)", "tutti i 45 prompt)"),
        (r"Gemini-2\.5 \(M4\) aveva il tasso di anomalie più alto a 0,30", "Sonar Deep Research (M6) aveva il tasso di anomalie più alto a 0,11"),
        (r"mentre M5.*aveva il più basso a 0,07", "mentre Claude Sonnet (M1), GPT-5.3 (M3), Gemini 2.5 Pro (M4), Gemini 2.5 Flash (M9), GPT-5.2 (M10) e Claude Sonnet 4.5 (M12) non avevano anomalie"),
        (r"con 5 modelli\.", "con 12 modelli."),
    ],

    # ---- Polish (pl/) ----
    "pl": [
        (r"pięciu LLM frontier", "dwunastu LLM frontier"),
        (r"pięciu czołowych LLM", "dwunastu czołowych LLM"),
        (r"pięć LLM", "dwanaście LLM"),
        (r"5 LLM", "12 LLM"),
        (r"Oceniamy pięć", "Oceniamy dwanaście"),
        (r"Pięć modeli", "Dwanaście modeli"),
        (r"pięć niezależnych systemów eksperckich", "dwanaście niezależnych systemów eksperckich"),
        (r"pięć modeli Anthropic", "dwanaście modeli Anthropic"),
        (r"\bpięć modeli\b", "dwanaście modeli"),
        (r"\b30 promptów\b", "45 promptów"),
        (r"\b30 promptach\b", "45 promptach"),
        (r"10 na dziedzinę", "15 na dziedzinę"),
        (r"eksperyment 150 uruchomień", "eksperyment 540 uruchomień"),
        (r"150 uruchomień", "540 uruchomień"),
        (r"\(30 promptów x 5 modeli\)", "(45 promptów x 12 modeli)"),
        (r"Na wszystkich 27 promptach", "Na wszystkich 45 promptach"),
        (r"wszystkich 27 promptach", "wszystkich 45 promptach"),
        (r"\b27 promptów\b", "45 promptów"),
        (r"\b27 promptach\b", "45 promptach"),
        (r"135 odpowiedzi modeli", "540 odpowiedzi modeli"),
        (r"co dało łącznie 135", "co dało łącznie 540"),
        (r"przynajmniej 60% modeli \(trzy z pięciu\)", "przynajmniej 58% modeli (siedem z dwunastu)"),
        (r"trzy z pięciu", "siedem z dwunastu"),
        (r"Wszystkie pięć anonimowych odpowiedzi", "Wszystkie dwanaście anonimowych odpowiedzi"),
        (r"pięć anonimowych odpowiedzi", "dwanaście anonimowych odpowiedzi"),
        (r"pięć ślepych odpowiedzi", "dwanaście ślepych odpowiedzi"),
        (r"szósty model", "trzynasty model"),
        (r"Przy 30 promptach w trzech dziedzinach", "Przy 45 promptach w trzech dziedzinach"),
        (r"Na 30 promptach", "Na 45 promptach"),
        (r"Pełny eksperyment BMAS obejmował 27 promptów w trzech warstwach dziedzinowych, ocenianych każdy przez pięć modeli, co dało łącznie 135 odpowiedzi modeli\.",
         "Pełny eksperyment BMAS obejmował 45 promptów w trzech warstwach dziedzinowych, ocenianych każdy przez dwanaście modeli, co dało łącznie 540 odpowiedzi modeli."),
        (r"wszystkie 27 promptów\)", "wszystkie 45 promptów)"),
        (r"Kompletny zbiór danych 150 uruchomień", "Kompletny zbiór danych 540 uruchomień"),
    ],
}

# Model table update for 03-methodology.md (English)
MODEL_TABLE_OLD = """| ID | Model | Provider | Context |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI (openai-codex OAuth) | 272k tokens |
| M4 | gemini-2.5-pro | Google (gemini-cli) | 1M tokens |
| M5 | perplexity/sonar-pro | Perplexity | 127k tokens |"""

MODEL_TABLE_NEW = """| ID | Model | Provider | Context |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI | 272k tokens |
| M4 | gemini-2.5-pro | Google | 1M tokens |
| M5 | sonar-pro | Perplexity | 127k tokens |
| M6 | sonar-deep-research | Perplexity | 127k tokens |
| M7 | gemini-3-pro-preview | Google | 1M tokens |
| M8 | gemini-3-flash-preview | Google | 1M tokens |
| M9 | gemini-2.5-flash | Google | 1M tokens |
| M10 | gpt-5.2 | OpenAI | 272k tokens |
| M11 | gpt-5.1 | OpenAI | 272k tokens |
| M12 | claude-sonnet-4-5 | Anthropic | 200k tokens |"""

def get_lang(filepath):
    """Determine language from filepath."""
    rel = os.path.relpath(filepath, SECTIONS_DIR)
    parts = rel.split(os.sep)
    if len(parts) >= 2 and parts[0] in ("de", "fr", "es", "it", "pl"):
        return parts[0]
    return "en"

def apply_substitutions(content, lang):
    subs = SUBSTITUTIONS.get(lang, [])
    for pattern, replacement in subs:
        content = re.sub(pattern, replacement, content)
    return content

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    lang = get_lang(filepath)
    content = apply_substitutions(original, lang)

    # Apply model table fix to EN 03-methodology.md only
    if filepath.endswith("03-methodology.md") and lang == "en":
        content = content.replace(MODEL_TABLE_OLD, MODEL_TABLE_NEW)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    changed = []
    unchanged = []
    for root, dirs, files in os.walk(SECTIONS_DIR):
        for fname in files:
            if fname.endswith(".md"):
                fpath = os.path.join(root, fname)
                if fix_file(fpath):
                    changed.append(os.path.relpath(fpath, SECTIONS_DIR))
                else:
                    unchanged.append(os.path.relpath(fpath, SECTIONS_DIR))

    print(f"Fixed {len(changed)} files:")
    for f in sorted(changed):
        print(f"  CHANGED: {f}")
    print(f"\nUnchanged: {len(unchanged)} files")
    for f in sorted(unchanged):
        print(f"  OK:      {f}")

if __name__ == "__main__":
    main()
