# 💡 7. Discusión

## 7.1 Interpretación de convergencia y divergencia

La afirmación central de BMAS es que la convergencia inter-modelos es informativa: no solo como propiedad estadística del experimento, sino como señal práctica para aplicaciones posteriores. Nuestros resultados [véase la sección 4] apoyan esta afirmación para los dominios factuales mientras revelan matices importantes.

La alta convergencia en los dominios A y B valida la intuición de que los modelos bien calibrados, entrenados con las mismas fuentes autorizadas, tienden hacia las mismas respuestas correctas cuando las preguntas son inequívocas. La baja convergencia en el dominio C refleja la genuina dificultad epistémica de las preguntas. Cuando doce sistemas expertos independientes no están de acuerdo sobre decisiones de arquitectura óptimas, el desacuerdo en sí mismo es significativo: señaliza que la pregunta no tiene una respuesta correcta dominante y merece deliberación humana. BMAS actúa así como un **oráculo de complejidad** además de una señal de calidad.

## 7.2 La conexión divergencia-alucinación

Nuestro análisis de valores atípicos proporciona evidencia preliminar de que los modelos identificados como atípicos en el espacio de embedding tienden a tener puntuaciones de precisión factual más bajas. Un sistema de producción que implemente monitoreo estilo BMAS podría marcar respuestas que se desvían significativamente del cluster de consenso para revisión humana.

Sin embargo, advertimos que la correlación no es causalidad. Una respuesta atípica puede ser correcta mientras el consenso está equivocado. La respuesta de M1 a A01 (puntuación CVSS de CVE-2024-21762) lo demostró: la puntuación atípica era matemáticamente correcta mientras los modelos de consenso aceptaban la puntuación declarada por el proveedor. Cualquier implementación de producción de filtrado basado en divergencia debe mantener la capacidad de anulación humana.

## 7.3 Comparación de estrategias de síntesis

S1 (voto mayoritario) produce una cobertura exhaustiva pero puede ser verboso e incluir ocasionalmente afirmaciones de minoría de baja confianza. Es más apropiado cuando la exhaustividad tiene prioridad sobre la concisión.

S2 (centroide semántico) produce de forma fiable la respuesta más "promedio". Funciona mejor cuando se necesita una respuesta representativa y la pregunta está bien acotada.

S3 (LLM-as-Judge) produce la mayor precisión factual en los dominios A y B pero introduce una nueva dependencia: los sesgos propios del modelo juez. El uso de un modelo reservado como juez mitiga este riesgo.

## ⚠️ 7.4 Limitaciones

**Tamaño de muestra.** Con 45 prompts en tres dominios, este estudio establece evidencia inicial pero no permite una generalización estadística amplia. Un estudio de seguimiento con 100+ prompts por dominio fortalecería sustancialmente las afirmaciones.

**Selección de modelos.** Los doce modelos representan una muestra de conveniencia. La composición de modelos afecta la distribución del consenso. Los trabajos futuros deberían variar sistemáticamente la composición de modelos.

**Calidad de las respuestas de referencia.** Tres elementos se marcaron como que requieren verificación manual (discrepancia CVSS de A01, fuente BSI de A10, referencia EDPB de B09).

**Validez temporal.** Las fechas de corte del conocimiento de los LLM y las versiones de los modelos cambian. Los estudios de replicación deben documentar la versión del modelo con precisión.

**Temperatura y muestreo.** No se controló la temperatura entre modelos. La replicación con temperatura controlada aislaría esta variable.

**La longitud del token no es densidad de información.** M4 (Gemini 2.5-pro) fue consistentemente el más verboso sin una mayor precisión factual.

## 7.5 Implicaciones para el despliegue de IA

1. **Consenso como portal de calidad.** En sistemas de IA de alto riesgo, una capa estilo BMAS puede ejecutar varios modelos en la misma consulta y retener la respuesta hasta que el consenso alcance un umbral definido. La discordancia activa revisión humana en lugar de acciones automáticas.
2. **Enrutamiento por dominio.** Para consultas factuales con fuentes autorizadas, un único modelo de alto rendimiento puede ser suficiente. El overhead multi-modelo se justifica más para consultas estratégicas.
3. **Requisitos de diversidad.** El rendimiento de BMAS depende de la diversidad de modelos. Dos modelos similares del mismo proveedor aportan menos información que dos de distintas familias arquitectónicas.

## 7.6 Trabajo futuro

- Estudio de deriva temporal: ejecutar los mismos prompts cada 6 meses
- Expansión de dominios: diagnóstico médico, análisis financiero, razonamiento jurídico
- Análisis de calibración: si la confianza del modelo correlaciona con el acuerdo de consenso
- Síntesis adaptativa: selección dinámica de S1, S2 o S3 según la convergencia medida
- Evaluación humana: comparar la calidad de la síntesis BMAS con respuestas de expertos humanos
