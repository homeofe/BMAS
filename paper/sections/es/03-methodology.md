# 3. Metodología

## 3.1 Descripción general del protocolo BMAS

Blind Multi-Agent Synthesis (BMAS) es un protocolo de cuatro fases para elicitar, comparar y sintetizar respuestas de múltiples LLMs sobre prompts idénticos:

1. **Elicitación ciega** - Cada modelo recibe el mismo prompt sin conocimiento del estudio, otros modelos u otras respuestas.
2. **Cálculo de métricas** - Se calculan similitud semántica por pares, precisión factual y detección de valores atípicos para todas las respuestas.
3. **Síntesis** - Tres estrategias de síntesis agregan las respuestas individuales en una única salida.
4. **Evaluación** - Las salidas de síntesis se puntúan frente a respuestas de referencia pre-registradas (dominios A y B) o evaluación experta (dominio C).

El protocolo impone una estricta **regla de no contaminación**: ninguna respuesta de un modelo se pone a disposición de otro modelo en ninguna fase anterior a la síntesis.

## 3.2 Modelos

Evaluamos cinco LLMs de cinco proveedores distintos:

| ID | Modelo | Proveedor | Ventana de contexto |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI | 272k tokens |
| M4 | gemini-2.5-pro | Google | 1M tokens |
| M5 | sonar-pro | Perplexity | 127k tokens |

La diversidad multi-proveedor es deliberada. Los modelos del mismo proveedor comparten linaje arquitectónico y pipelines de datos de entrenamiento, lo que puede reducir la divergencia incluso en condiciones ciegas.

**Implementación de aislamiento:** Cada modelo corre en una sesión aislada separada sin contexto compartido. El system prompt es idéntico en todos los modelos:

> *"Eres un asistente experto con amplio conocimiento. Responde la siguiente pregunta con la mayor precisión y exhaustividad posible. Sé preciso, factual y estructurado. Si no estás seguro de algún detalle específico, indícalo explícitamente."*

La temperatura no se modifica. Preservamos deliberadamente el comportamiento de muestreo predeterminado de cada modelo para capturar la varianza natural de respuestas.

## 3.3 Diseño de prompts

### 3.3.1 Estructura de dominios

Construimos 30 prompts en tres estratos de dominio:

**Dominio A - Técnico de alta precisión (A01-A10):** Preguntas con respuestas objetivamente correctas verificables frente a fuentes primarias autorizadas (estándares NIST FIPS, NVD, RFCs IETF, especificaciones OpenID Foundation). Ejemplos: justificación de puntuación CVSS, tamaños de clave de algoritmos PQC, enumeración de cipher suites TLS 1.3.

**Dominio B - Regulatorio/Cumplimiento (B01-B10):** Preguntas basadas en texto legal y regulatorio con fuentes autorizadas (RGPD, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Las respuestas centrales están definidas en texto formal. Ejemplos: excepciones de borrado del Artículo 17(3) del RGPD, clasificaciones sectoriales de NIS2, diferencias de nivel de evaluación TISAX.

**Dominio C - Estratégico/Ambiguo (C01-C10):** Preguntas sin respuesta única correcta que requieren juicio experto y razonamiento arquitectónico. Existen múltiples posiciones defendibles. Ejemplos: decisiones de arquitectura zero-trust, priorización de migración PQC, compensaciones de inversión en cumplimiento.

### 3.3.2 Requisitos de los prompts

Todos los prompts satisfacen cuatro criterios:
1. **Autónomos** - respondibles sin contexto externo ni recuperación de documentos
2. **Respuesta estructurada** - cada prompt especifica el formato de salida requerido
3. **Longitud acotada** - respuesta esperada de 300-600 tokens para dominios A-B; 400-800 para dominio C
4. **Verificables** - para los dominios A y B existe una respuesta verificable

### 3.3.3 Pre-registro

Siguiendo las mejores prácticas de ciencia abierta, las respuestas de referencia para los dominios A y B fueron documentadas y bloqueadas antes de cualquier ejecución de modelos. Esto evita el sesgo de confirmación inconsciente en la puntuación.

## 3.4 Métricas

### 3.4.1 Similitud semántica (primaria)

Calculamos la similitud coseno por pares entre embeddings de respuestas usando el modelo sentence-transformer `all-mpnet-base-v2`. Para N modelos, esto produce una matriz de similitud N x N por prompt. Reportamos:
- **Similitud por pares media (MPS):** media de todos los N(N-1)/2 scores por pares
- **Similitud mínima por pares:** el par más divergente
- **Desviación estándar de similitud:** varianza dentro del cluster de respuestas del prompt

### 3.4.2 BERTScore

Calculamos BERTScore F1 por pares como medida secundaria de similitud semántica a nivel de token. BERTScore captura la proximidad léxica más allá de los embeddings a nivel de oración.

### 3.4.3 Jaccard sobre afirmaciones clave

Extraemos afirmaciones factuales discretas de cada respuesta mediante segmentación de oraciones y calculamos la similitud Jaccard por pares sobre conjuntos de afirmaciones normalizados. Esta métrica captura el acuerdo estructural.

### 3.4.4 Detección de valores atípicos

Aplicamos DBSCAN con eps=0.15 y min_samples=2. Los modelos cuyos embeddings caen fuera de todos los clusters de vecindario reciben una etiqueta de valor atípico (-1). Tratamos el estado de valor atípico como señal de alucinación potencial en los dominios A y B.

### 3.4.5 Precisión factual (solo dominios A y B)

Para cada respuesta de los dominios A y B, puntuamos la precisión factual frente a la lista de verificación de respuestas de referencia pre-registradas. La puntuación de precisión factual es la fracción de elementos satisfechos.

## 3.5 Estrategias de síntesis

**S1 - Voto mayoritario (nivel de afirmación):** Las afirmaciones factuales se aceptan si aparecen en respuestas de al menos el 60% de los modelos. Las afirmaciones minoritarias se añaden con un marcador [MINORITY].

**S2 - Centroide semántico:** La respuesta cuyo embedding es más cercano a la media de todos los embeddings se selecciona como base de síntesis. No se añade nuevo contenido.

**S3 - LLM-as-Judge:** Las cinco respuestas anonimizadas se presentan a una sexta instancia de modelo (M2, claude-opus-4-6) con instrucción de producir una síntesis autoritativa única, marcando afirmaciones minoritarias ([MINORITY]) y contradicciones ([DISPUTED]).

## 3.6 Hipótesis

**H1 (Convergencia en dominios factuales):** La similitud semántica por pares media para los prompts de los dominios A y B superará 0.75 (BERTScore F1).

**H2 (La divergencia señaliza error):** Entre las respuestas de los dominios A y B, los modelos atípicos (etiqueta DBSCAN -1) tendrán puntuaciones de precisión factual significativamente más bajas que los modelos no atípicos (t-test unilateral, alfa=0.05).

**H3 (Efecto del dominio sobre la convergencia):** La similitud por pares media para el dominio C será significativamente menor que para los dominios A y B (ANOVA unidireccional, Tukey HSD post-hoc, alfa=0.05).

## 3.7 Configuración experimental

Todas las ejecuciones de modelos se ejecutaron a través del gateway de OpenClaw, que enruta de forma independiente a la API de cada proveedor. El dataset completo de 150 ejecuciones (30 prompts x 5 modelos) se publica junto con este artículo.
