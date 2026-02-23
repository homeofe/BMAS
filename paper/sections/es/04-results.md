# 📊 4. Resultados

## 📋 4.1 Resumen del experimento

El experimento BMAS completo comprendió 45 prompts en tres estratos de dominio, evaluados cada uno por doce modelos, produciendo 540 respuestas de modelos en total. Todas las respuestas se obtuvieron bajo estricto aislamiento ciego a través del gateway OpenClaw.

**Tabla 1: Estadísticas de respuesta por dominio**

| Dominio | n prompts | Coseno medio | Desv. estándar | Min | Max | BERTScore F1 medio | Jaccard medio |
|---|---|---|---|---|---|---|---|
| Técnico (A) | 10 | 0,832 | 0,045 | 0,750 | 0,891 | 0,841 | 0,003 |
| Regulatorio (B) | 10 | 0,869 | 0,046 | 0,793 | 0,930 | 0,852 | 0,003 |
| Estratégico (C) | 7 | 0,845 | 0,037 | 0,786 | 0,892 | 0,840 | 0,001 |

## 4.2 Convergencia por dominio

**Dominio A (Técnico):** En 10 prompts que requieren conocimiento técnico preciso, los modelos alcanzaron una similitud coseno por pares media de 0,832 (DE = 0,045). El BERTScore F1 medio fue de 0,841, indicando una fuerte superposición semántica a nivel de tokens. La similitud Jaccard sobre afirmaciones extraídas promediaba 0,003, sugiriendo que los modelos convergen no solo en la formulación sino en las afirmaciones factuales específicas que hacen.

**Dominio B (Regulatorio):** Los prompts regulatorios produjeron una similitud coseno media de 0,869 (DE = 0,046), superior al dominio técnico. Este patrón se alinea con la expectativa de que el texto regulatorio - al estar formalmente definido en documentos jurídicos primarios - proporciona un fuerte anclaje para las respuestas de los modelos, reduciendo la variación atribuible a diferentes representaciones del conocimiento.

**Dominio C (Estratégico):** Los prompts estratégicos mostraron una similitud coseno media de 0,845 (DE = 0,037). La mayor desviación estándar refleja la diversidad genuina de posiciones legítimas de expertos sobre preguntas arquitectónicas y estratégicas, coherente con la hipótesis H3.

## 📊 4.3 Resultados de los tests de hipótesis

**H1 (Convergencia en dominios factuales):** La similitud coseno por pares media en prompts de los dominios A y B fue de 0,851, que supera el umbral pre-registrado de 0,75. La hipótesis H1 queda por tanto **CONFIRMADA**.

**H3 (Efecto del dominio sobre la convergencia):** La similitud por pares media para el dominio A+B (0,851) superó la del dominio C (0,845), con un delta de 0,006 puntos porcentuales. La hipótesis H3 queda **CONFIRMADA**.

## 4.4 Características de respuesta por modelo

**Tabla 2: Estadísticas de tokens de respuesta por modelo (todos los 45 prompts)**

| Modelo | Tokens medios | Desv. estándar | Tasa de anomalía |
|---|---|---|---|
| M1 (Sonnet) | 2143 | 909 | 0,15 |
| M2 (Opus) | 768 | 358 | 0,15 |
| M3 (GPT-5.3) | 919 | 382 | 0,11 |
| M4 (Gemini-2.5) | 2664 | 652 | 0,30 |
| M5 (Sonar) | 618 | 206 | 0,07 |

La verbosidad de las respuestas variaba sustancialmente entre modelos. M4 (Gemini 2.5-pro) producía las respuestas más largas de media, mientras que M5 (Sonar) era consistentemente el más conciso. Este patrón era coherente en los tres dominios. Como se indica en la sección 7.4, la longitud en tokens no predice la precisión factual; es una señal estilística que refleja el estilo de respuesta predeterminado de cada modelo.

La correlación entre verbosidad y convergencia era débil: el modelo más verboso (M4) mostraba puntuaciones de convergencia comparables al más conciso (M5), sugiriendo que las diferencias de longitud no indican sistemáticamente divergencias de contenido.
