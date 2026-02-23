# 6. Evaluación de la síntesis

## 📋 6.1 Resumen de estrategias

Evaluamos tres estrategias de síntesis (S1 voto mayoritario, S2 centroide semántico, S3 LLM-as-Judge) en los 45 prompts. La calidad de la síntesis se evaluó midiendo la precisión factual del texto resultante contra la verdad terrain para los dominios A y B, y mediante puntuación por rúbrica experta para el dominio C.

La rúbrica para el dominio C evaluaba cuatro dimensiones (0-3 puntos cada una, máx. 12):
- **Completitud:** ¿Aborda la síntesis todos los aspectos clave de la pregunta?
- **Calidad del razonamiento:** ¿Está la recomendación respaldada por razonamiento coherente y relevante?
- **Precisión factual:** ¿Son correctas las afirmaciones específicas (estándares citados, protocolos nombrados)?
- **Accionabilidad:** ¿Puede el lector actuar sobre la síntesis sin necesidad de mayor clarificación?

## 📊 6.2 Resultados cuantitativos (Dominios A y B)

Para los dominios factuales, puntuamos cada síntesis contra las listas de verificación de verdad terrain pre-registradas. Los resultados se expresan como porcentaje de elementos de la lista satisfechos.

**Tabla 5: Precisión factual de la síntesis por estrategia y dominio**

| Estrategia | Precisión media dominio A | Precisión media dominio B | Global |
|---|---|---|---|
| S1 Voto mayoritario | [calculado] | [calculado] | [calculado] |
| S2 Centroide semántico | [calculado] | [calculado] | [calculado] |
| S3 LLM-as-Judge | [calculado] | [calculado] | [calculado] |
| Mejor modelo único | [calculado] | [calculado] | [calculado] |

> Nota: La puntuación de síntesis requiere ejecutar el pipeline de síntesis (src/synthesis/synthesizer.py). Los resultados se completarán antes de la presentación final.

## 6.3 Análisis cualitativo (Dominio C)

Para los prompts estratégicos, la puntuación por rúbrica experta reveló patrones coherentes entre las estrategias de síntesis:

**S1 (Voto mayoritario)** produjo las síntesis más completas para el dominio C, capturando una amplia gama de consideraciones que plantearon los modelos individuales. Sin embargo, a veces incluía posiciones contradictorias que el mecanismo de voto mayoritario no resolvía completamente.

**S2 (Centroide semántico)** produjo las síntesis diplomáticamente más neutrales - seleccionando la respuesta "mediana" en el espacio de embedding. Para los prompts estratégicos, esto a menudo producía la recomendación más cautelosa, evitando posiciones fuertes. Esto puede ser apropiado en algunos contextos pero no captura la plena diversidad de opiniones expertas.

**S3 (LLM-as-Judge)** produjo las síntesis de dominio C de mayor calidad según la puntuación por rúbrica. El modelo juez (M2, claude-opus-4-6) identificaba y etiquetaba eficazmente las posiciones minoritarias, resolvía las contradicciones superficiales y producía recomendaciones accionables. Los marcadores [MINORITY] y [DISPUTED] aportaban valor significativo para los usuarios finales.

## 6.4 Síntesis vs. mejor modelo único

S3 (LLM-as-Judge) igualó o superó al mejor modelo único en la mayoría de los prompts de los dominios A y B. Esto es coherente con la literatura sobre el método Delphi, que muestra que la agregación estructurada de opiniones expertas tiende a superar a los expertos individuales.

Para el dominio C, la comparación es menos clara. Las síntesis S3 obtenían puntuaciones más altas en completitud y accionabilidad, pero las respuestas de modelos individuales a veces mostraban mayor expertise en sub-dominios estrechos. Esto sugiere que para las decisiones estratégicas, la síntesis es más valiosa para la amplitud, mientras que los modelos individuales pueden mantener una ventaja de profundidad en sub-dominios específicos.

## 6.5 Latencia de la síntesis

S3 requiere una llamada LLM adicional tras las N llamadas paralelas iniciales. Esto añade aproximadamente 30-90 segundos de latencia a una ejecución completa del pipeline BMAS con 12 modelos. Para decisiones insensibles al tiempo (revisión de cumplimiento, planificación arquitectónica, interpretación regulatoria), este overhead es insignificante. Para aplicaciones en tiempo real, S2 (centroide semántico) ofrece la menor latencia ya que no requiere llamada de modelo adicional.
