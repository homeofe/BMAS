# 2. Trabajos relacionados

BMAS se basa en metodos de consenso experto estructurado, tecnicas LLM multi-muestra y multi-modelo, metricas de evaluacion automatizada y clustering basado en densidad. Esta seccion revisa cada area y clarifica el posicionamiento de BMAS respecto a trabajos previos.

## 2.1 El metodo Delphi

Dalkey y Helmer (1963) introdujeron el metodo Delphi en la RAND Corporation como enfoque estructurado de prediccion experta. En el protocolo original, un panel de expertos proporcionaba estimaciones independientes sin conocer las respuestas de los demas, y un facilitador agregaba los resultados en multiples rondas iterativas. La fortaleza central del metodo era que el aislamiento prevenia el anclaje y el pensamiento grupal, permitiendo que el desacuerdo genuino emergiera antes de buscar el consenso. BMAS toma prestado este principio de aislamiento directamente: cada LLM responde a los prompts sin observar las salidas de ningun otro modelo, garantizando que la convergencia, cuando ocurre, refleja razonamiento independiente y no imitacion.

## 2.2 Self-Consistency

Wang et al. (2022) propusieron la self-consistency como estrategia de decodificacion que muestrea multiples cadenas de razonamiento de un unico modelo de lenguaje y selecciona la respuesta final por voto mayoritario. El metodo demostro mejoras significativas en benchmarks de razonamiento aritmetico y de sentido comun al explotar la intuicion de que los caminos de razonamiento correctos tienen mas probabilidad de converger en la misma respuesta que los incorrectos. Sin embargo, dado que todas las cadenas de razonamiento provienen del mismo modelo, la self-consistency captura solo la varianza de decodificacion intra-modelo, no las diferencias mas profundas en datos de entrenamiento, arquitectura y alineacion que distinguen a diferentes proveedores. BMAS extiende la intuicion de convergencia-como-senal-de-calidad al marco multi-proveedor, donde el acuerdo entre modelos entrenados independientemente constituye un prior mas fuerte para la correccion.

## 2.3 Mixture of Agents

Wang et al. (2024) introdujeron el framework Mixture-of-Agents (MoA), en el que varios LLMs participan en rondas de agregacion iterativas donde cada modelo puede observar y refinar los outputs de los demas. MoA demostro que el refinamiento colaborativo entre modelos mejoraba el rendimiento en benchmarks como AlpacaEval y MT-Bench. La diferencia critica con BMAS es que MoA no es ciego: los modelos en rondas posteriores estan expuestos a outputs previos, lo que introduce el riesgo de propagacion de errores. BMAS evita deliberadamente esto imponiendo un aislamiento estricto durante la fase de respuesta y difiriendo cualquier interaccion entre modelos a una fase de sintesis separada.

## 2.4 LLM-as-Judge

Zheng et al. (2023) investigaron el uso de grandes modelos de lenguaje como evaluadores de outputs de otros modelos, introduciendo los benchmarks MT-Bench y Chatbot Arena. Su trabajo mostro que los LLMs potentes podian servir como proxies escalables para la evaluacion humana. En BMAS, el papel de juez se limita a una de las tres estrategias de sintesis (S3): un sexto modelo sintetiza las cinco respuestas ciegas en un unico output, pero la correccion se mide en ultima instancia frente a respuestas de referencia pre-registradas, no frente a las preferencias del juez.

## 2.5 BERTScore

Zhang et al. (2020) propusieron BERTScore, una metrica de evaluacion automatica que calcula la similitud a nivel de tokens entre textos candidato y de referencia usando embeddings contextuales de modelos transformer pre-entrenados. A diferencia de las metricas de solapamiento de n-gramas como BLEU o ROUGE, BERTScore captura la equivalencia semantica a traves de diferentes formas superficiales y es robusta a la parafrasis. BMAS adopta BERTScore F1 como metrica principal de similitud por pares para medir la convergencia inter-modelos.

## 2.6 Constitutional AI

Bai et al. (2022) introdujeron Constitutional AI (CAI) en Anthropic, una metodologia de entrenamiento en la que un modelo critica y revisa sus propios outputs segun un conjunto de principios antes del aprendizaje por refuerzo con retroalimentacion humana. BMAS puede verse como la extension de la intuicion de critica-y-revision de un bucle de modelo unico a un marco multi-modelo y multi-proveedor: en lugar de un modelo que se juzga a si mismo, varios modelos entrenados independientemente sirven como criticos implicitos entre si a traves de la senal de divergencia.

## 2.7 DBSCAN

Ester et al. (1996) propusieron DBSCAN (Density-Based Spatial Clustering of Applications with Noise), un algoritmo de clustering que agrupa puntos de datos basandose en la conectividad de densidad e identifica los puntos en regiones de baja densidad como ruido o valores atipicos. A diferencia de k-means, DBSCAN no requiere especificar el numero de clusters a priori. BMAS emplea DBSCAN sobre el espacio de embeddings de las respuestas de los modelos para detectar outputs atipicos: en dominios factuales, una respuesta atipica se trata como una alucinacion candidata.

## 2.8 Posicionamiento

BMAS es, segun nuestro conocimiento, el primer framework que combina cuatro propiedades ausentes de cualquier enfoque previo individual. Primero, impone aislamiento ciego entre proveedores. Segundo, introduce analisis estratificado por dominio. Tercero, trata la divergencia como senal de anomalia en lugar de fallo de coordinacion. Cuarto, proporciona una comparacion controlada de estrategias de sintesis evaluadas frente a respuestas de referencia pre-registradas.
