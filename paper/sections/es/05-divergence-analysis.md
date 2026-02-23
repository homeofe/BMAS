# 5. Análisis de divergencia

## 📊 5.1 Resultados de detección de valores atípicos

En los 45 prompts, 12 (44 %) produjeron al menos un modelo semánticamente atípico identificado por DBSCAN (eps=0,15, min_samples=2). La frecuencia de valores atípicos fue mayor en el dominio C (estratégico), coherente con la expectativa de que las preguntas ambiguas producen embeddings de respuesta más diversos.

**Tabla 3: Frecuencia de valores atípicos por dominio**

| Dominio | Prompts con atípicos | Total prompts | Tasa |
|---|---|---|---|
| Técnico (A) | 5 | 10 | 50 % |
| Regulatorio (B) | 4 | 10 | 40 % |
| Estratégico (C) | 3 | 7 | 43 % |

**Tabla 4: Tasa de valores atípicos por modelo (todos los prompts)**

| Modelo | Número de atípicos | Tasa de atípicos |
|---|---|---|
| M1 (Sonnet) | 4 | 0,15 (15 %) |
| M2 (Opus) | 4 | 0,15 (15 %) |
| M3 (GPT-5.3) | 3 | 0,11 (11 %) |
| M4 (Gemini-2.5) | 8 | 0,30 (30 %) |
| M5 (Sonar) | 2 | 0,07 (7 %) |

Gemini-2.5 (M4) tuvo la mayor tasa de valores atípicos con 0,30, mientras que Sonar (M5) tuvo la más baja con 0,07. Una alta tasa de atípicos para un modelo específico no indica necesariamente menor calidad - puede reflejar un estilo de respuesta más distintivo o una tendencia a una cobertura más completa que aleja su embedding del centroide.

## 5.2 Correlación divergencia-alucinación (Hipótesis H2)

Para probar H2, comparamos las puntuaciones de precisión factual entre respuestas de modelos atípicos y no atípicos para prompts de los dominios A y B. La precisión factual se evaluó puntuando cada respuesta contra la lista de verificación de verdad terrain pre-registrada para cada prompt.

> Nota: Los resultados detallados de H2 incluyendo puntuaciones de precisión factual requieren anotación manual de la verdad terrain, parcialmente completada antes de las ejecuciones de modelos (ver sección 3.3.3). Los resultados completos de anotación están disponibles en el dataset suplementario.

Un caso notable de los datos piloto (A01, puntuación CVSS): M1 puntuó 9,8 (matemáticamente correcto dado el vector), mientras que los modelos convergentes aceptaban el 9,6 declarado por el proveedor. La anomalía (M1) era factualment superior al consenso. Esto demuestra que H2 debe interpretarse con cautela: **el estado de atípico es una señal para revisión humana, no un veredicto de incorrección.**

## 5.3 Patrones de divergencia por dominio

El dominio estratégico (C) mostró la mayor divergencia no solo en puntuaciones de similitud semántica sino también en características estructurales. Las respuestas a prompts del dominio C variaban en recomendaciones fundamentales: diferentes modelos favorecían diferentes arquitecturas (microservicios vs. monolito), diferentes prioridades de migración (TLS-primero vs. firma de código-primero) y diferentes estrategias de inversión (certificación vs. controles técnicos).

Esta diversidad es legítima. A diferencia de los prompts factuales donde una respuesta es correcta, los prompts estratégicos no tienen una verdad terrain autoritativa. El marco BMAS trata esto como señal informativa: cuando los sistemas expertos no están de acuerdo, el desacuerdo mismo argumenta a favor de la deliberación humana en lugar de la toma de decisiones automática.
