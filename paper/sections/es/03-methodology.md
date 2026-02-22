# 3. Metodologia

## 3.1 Descripcion general del protocolo BMAS

Blind Multi-Agent Synthesis (BMAS) es un protocolo de cuatro fases para elicitar, comparar y sintetizar respuestas de multiples LLMs sobre prompts identicos:

1. **Elicitacion ciega** - Cada modelo recibe el mismo prompt sin conocimiento del estudio, otros modelos u otras respuestas.
2. **Calculo de metricas** - Se calculan similitud semantica por pares, precision factual y deteccion de valores atipicos para todas las respuestas.
3. **Sintesis** - Tres estrategias de sintesis agregan las respuestas individuales en una unica salida.
4. **Evaluacion** - Las salidas de sintesis se puntuan frente a respuestas de referencia pre-registradas (dominios A y B) o evaluacion experta (dominio C).

El protocolo impone una estricta **regla de no contaminacion**: ninguna respuesta de un modelo se pone a disposicion de otro modelo en ninguna fase anterior a la sintesis.

## 3.2 Modelos

Evaluamos cinco LLMs de cinco proveedores distintos:

| ID | Modelo | Proveedor | Ventana de contexto |
|---|---|---|---|
| M1 | claude-sonnet-4-6 | Anthropic | 1M tokens |
| M2 | claude-opus-4-6 | Anthropic | 1M tokens |
| M3 | gpt-5.3-codex | OpenAI | 272k tokens |
| M4 | gemini-2.5-pro | Google | 1M tokens |
| M5 | sonar-pro | Perplexity | 127k tokens |

La diversidad multi-proveedor es deliberada. Los modelos del mismo proveedor comparten linaje arquitectonico y pipelines de datos de entrenamiento, lo que puede reducir la divergencia incluso en condiciones ciegas.

**Implementacion de aislamiento:** Cada modelo corre en una sesion aislada separada sin contexto compartido. El system prompt es identico en todos los modelos:

> *"Eres un asistente experto con amplio conocimiento. Responde la siguiente pregunta con la mayor precision y exhaustividad posible. Se preciso, factual y estructurado. Si no estas seguro de algun detalle especifico, indicalo explicitamente."*

La temperatura no se modifica. Preservamos deliberadamente el comportamiento de muestreo predeterminado de cada modelo para capturar la varianza natural de respuestas.

## 3.3 Diseno de prompts

### 3.3.1 Estructura de dominios

Construimos 30 prompts en tres estratos de dominio:

**Dominio A - Tecnico de alta precision (A01-A10):** Preguntas con respuestas objetivamente correctas verificables frente a fuentes primarias autorizadas (estandares NIST FIPS, NVD, RFCs IETF, especificaciones OpenID Foundation). Ejemplos: justificacion de puntuacion CVSS, tamanios de clave de algoritmos PQC, enumeracion de cipher suites TLS 1.3.

**Dominio B - Regulatorio/Cumplimiento (B01-B10):** Preguntas basadas en texto legal y regulatorio con fuentes autorizadas (RGPD, eIDAS 2.0, NIS2, ISO 27001, BSI C5). Las respuestas centrales estan definidas en texto formal. Ejemplos: excepciones de borrado del Articulo 17(3) del RGPD, clasificaciones sectoriales de NIS2, diferencias de nivel de evaluacion TISAX.

**Dominio C - Estrategico/Ambiguo (C01-C10):** Preguntas sin respuesta unica correcta que requieren juicio experto y razonamiento arquitectonico. Existen multiples posiciones defendibles. Ejemplos: decisiones de arquitectura zero-trust, priorizacion de migracion PQC, compensaciones de inversion en cumplimiento.

### 3.3.2 Requisitos de los prompts

Todos los prompts satisfacen cuatro criterios:
1. **Autonomos** - respondibles sin contexto externo ni recuperacion de documentos
2. **Respuesta estructurada** - cada prompt especifica el formato de salida requerido
3. **Longitud acotada** - respuesta esperada de 300-600 tokens para dominios A-B; 400-800 para dominio C
4. **Verificables** - para los dominios A y B existe una respuesta verificable

### 3.3.3 Pre-registro

Siguiendo las mejores practicas de ciencia abierta, las respuestas de referencia para los dominios A y B fueron documentadas y bloqueadas antes de cualquier ejecucion de modelos. Esto evita el sesgo de confirmacion inconsciente en la puntuacion.

## 3.4 Metricas

### 3.4.1 Similitud semantica (primaria)

Calculamos la similitud coseno por pares entre embeddings de respuestas usando el modelo sentence-transformer `all-mpnet-base-v2`. Para N modelos, esto produce una matriz de similitud N x N por prompt. Reportamos:
- **Similitud por pares media (MPS):** media de todos los N(N-1)/2 scores por pares
- **Similitud minima por pares:** el par mas divergente
- **Desviacion estandar de similitud:** varianza dentro del cluster de respuestas del prompt

### 3.4.2 BERTScore

Calculamos BERTScore F1 por pares como medida secundaria de similitud semantica a nivel de token. BERTScore captura la proximidad lexica mas alla de los embeddings a nivel de oracion.

### 3.4.3 Jaccard sobre afirmaciones clave

Extraemos afirmaciones factuales discretas de cada respuesta mediante segmentacion de oraciones y calculamos la similitud Jaccard por pares sobre conjuntos de afirmaciones normalizados. Esta metrica captura el acuerdo estructural.

### 3.4.4 Deteccion de valores atipicos

Aplicamos DBSCAN con eps=0.15 y min_samples=2. Los modelos cuyos embeddings caen fuera de todos los clusters de vecindario reciben una etiqueta de valor atipico (-1). Tratamos el estado de valor atipico como senal de alucinacion potencial en los dominios A y B.

### 3.4.5 Precision factual (solo dominios A y B)

Para cada respuesta de los dominios A y B, puntuamos la precision factual frente a la lista de verificacion de respuestas de referencia pre-registradas. La puntuacion de precision factual es la fraccion de elementos satisfechos.

## 3.5 Estrategias de sintesis

**S1 - Voto mayoritario (nivel de afirmacion):** Las afirmaciones factuales se aceptan si aparecen en respuestas de al menos el 60% de los modelos. Las afirmaciones minoritarias se anaden con un marcador [MINORITY].

**S2 - Centroide semantico:** La respuesta cuyo embedding es mas cercano a la media de todos los embeddings se selecciona como base de sintesis. No se anade nuevo contenido.

**S3 - LLM-as-Judge:** Las cinco respuestas anonimizadas se presentan a una sexta instancia de modelo (M2, claude-opus-4-6) con instruccion de producir una sintesis autoritativa unica, marcando afirmaciones minoritarias ([MINORITY]) y contradicciones ([DISPUTED]).

## 3.6 Hipotesis

**H1 (Convergencia en dominios factuales):** La similitud semantica por pares media para los prompts de los dominios A y B superara 0.75 (BERTScore F1).

**H2 (La divergencia senializa error):** Entre las respuestas de los dominios A y B, los modelos atipicos (etiqueta DBSCAN -1) tendran puntuaciones de precision factual significativamente mas bajas que los modelos no atipicos (t-test unilateral, alfa=0.05).

**H3 (Efecto del dominio sobre la convergencia):** La similitud por pares media para el dominio C sera significativamente menor que para los dominios A y B (ANOVA unidireccional, Tukey HSD post-hoc, alfa=0.05).

## 3.7 Configuracion experimental

Todas las ejecuciones de modelos se ejecutaron a traves del gateway de OpenClaw, que enruta de forma independiente a la API de cada proveedor. El dataset completo de 150 ejecuciones (30 prompts x 5 modelos) se publica junto con este articulo.
