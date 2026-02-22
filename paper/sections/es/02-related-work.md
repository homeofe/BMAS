# 2. Trabajos relacionados

BMAS se basa en métodos de consenso experto estructurado, técnicas LLM multi-muestra y multi-modelo, métricas de evaluación automatizada y clustering basado en densidad. Esta sección revisa cada área y clarifica el posicionamiento de BMAS respecto a trabajos previos.

## 2.1 El método Delphi

Dalkey y Helmer (1963) introdujeron el método Delphi en la RAND Corporation como enfoque estructurado de predicción experta. En el protocolo original, un panel de expertos proporcionaba estimaciones independientes sin conocer las respuestas de los demás, y un facilitador agregaba los resultados en múltiples rondas iterativas. La fortaleza central del método era que el aislamiento prevenía el anclaje y el pensamiento grupal, permitiendo que el desacuerdo genuino emergiera antes de buscar el consenso. BMAS toma prestado este principio de aislamiento directamente: cada LLM responde a los prompts sin observar las salidas de ningún otro modelo, garantizando que la convergencia, cuando ocurre, refleja razonamiento independiente y no imitación.

## 2.2 Self-Consistency

Wang et al. (2022) propusieron la self-consistency como estrategia de decodificación que muestrea múltiples cadenas de razonamiento de un único modelo de lenguaje y selecciona la respuesta final por voto mayoritario. El método demostró mejoras significativas en benchmarks de razonamiento aritmético y de sentido común al explotar la intuición de que los caminos de razonamiento correctos tienen más probabilidad de converger en la misma respuesta que los incorrectos. Sin embargo, dado que todas las cadenas de razonamiento provienen del mismo modelo, la self-consistency captura solo la varianza de decodificación intra-modelo, no las diferencias más profundas en datos de entrenamiento, arquitectura y alineación que distinguen a diferentes proveedores. BMAS extiende la intuición de convergencia-como-señal-de-calidad al marco multi-proveedor, donde el acuerdo entre modelos entrenados independientemente constituye un prior más fuerte para la corrección.

## 2.3 Mixture of Agents

Wang et al. (2024) introdujeron el framework Mixture-of-Agents (MoA), en el que varios LLMs participan en rondas de agregación iterativas donde cada modelo puede observar y refinar los outputs de los demás. MoA demostró que el refinamiento colaborativo entre modelos mejoraba el rendimiento en benchmarks como AlpacaEval y MT-Bench. La diferencia crítica con BMAS es que MoA no es ciego: los modelos en rondas posteriores están expuestos a outputs previos, lo que introduce el riesgo de propagación de errores. BMAS evita deliberadamente esto imponiendo un aislamiento estricto durante la fase de respuesta y difiriendo cualquier interacción entre modelos a una fase de síntesis separada.

## 2.4 LLM-as-Judge

Zheng et al. (2023) investigaron el uso de grandes modelos de lenguaje como evaluadores de outputs de otros modelos, introduciendo los benchmarks MT-Bench y Chatbot Arena. Su trabajo mostró que los LLMs potentes podían servir como proxies escalables para la evaluación humana. En BMAS, el papel de juez se limita a una de las tres estrategias de síntesis (S3): un sexto modelo sintetiza las cinco respuestas ciegas en un único output, pero la corrección se mide en última instancia frente a respuestas de referencia pre-registradas, no frente a las preferencias del juez.

## 2.5 BERTScore

Zhang et al. (2020) propusieron BERTScore, una métrica de evaluación automática que calcula la similitud a nivel de tokens entre textos candidato y de referencia usando embeddings contextuales de modelos transformer pre-entrenados. A diferencia de las métricas de solapamiento de n-gramas como BLEU o ROUGE, BERTScore captura la equivalencia semántica a través de diferentes formas superficiales y es robusta a la paráfrasis. BMAS adopta BERTScore F1 como métrica principal de similitud por pares para medir la convergencia inter-modelos.

## 2.6 Constitutional AI

Bai et al. (2022) introdujeron Constitutional AI (CAI) en Anthropic, una metodología de entrenamiento en la que un modelo critica y revisa sus propios outputs según un conjunto de principios antes del aprendizaje por refuerzo con retroalimentación humana. BMAS puede verse como la extensión de la intuición de crítica-y-revisión de un bucle de modelo único a un marco multi-modelo y multi-proveedor: en lugar de un modelo que se juzga a sí mismo, varios modelos entrenados independientemente sirven como críticos implícitos entre sí a través de la señal de divergencia.

## 2.7 DBSCAN

Ester et al. (1996) propusieron DBSCAN (Density-Based Spatial Clustering of Applications with Noise), un algoritmo de clustering que agrupa puntos de datos basándose en la conectividad de densidad e identifica los puntos en regiones de baja densidad como ruido o valores atípicos. A diferencia de k-means, DBSCAN no requiere especificar el número de clusters a priori. BMAS emplea DBSCAN sobre el espacio de embeddings de las respuestas de los modelos para detectar outputs atípicos: en dominios factuales, una respuesta atípica se trata como una alucinación candidata.

## 2.8 Posicionamiento

BMAS es, según nuestro conocimiento, el primer framework que combina cuatro propiedades ausentes de cualquier enfoque previo individual. Primero, impone aislamiento ciego entre proveedores. Segundo, introduce análisis estratificado por dominio. Tercero, trata la divergencia como señal de anomalía en lugar de fallo de coordinación. Cuarto, proporciona una comparación controlada de estrategias de síntesis evaluadas frente a respuestas de referencia pre-registradas.
