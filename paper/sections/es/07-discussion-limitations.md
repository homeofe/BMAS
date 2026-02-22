# 7. Discusion

## 7.1 Interpretacion de convergencia y divergencia

La afirmacion central de BMAS es que la convergencia inter-modelos es informativa: no solo como propiedad estadistica del experimento, sino como senal practica para aplicaciones posteriores. Nuestros resultados [vease la seccion 4] apoyan esta afirmacion para los dominios factuales mientras revelan matices importantes.

La alta convergencia en los dominios A y B valida la intuicion de que los modelos bien calibrados, entrenados con las mismas fuentes autorizadas, tienden hacia las mismas respuestas correctas cuando las preguntas son inequivocas. La baja convergencia en el dominio C refleja la genuina dificultad epistemica de las preguntas. Cuando cinco sistemas expertos independientes no estan de acuerdo sobre decisiones de arquitectura optimas, el desacuerdo en si mismo es significativo: senializa que la pregunta no tiene una respuesta correcta dominante y merece deliberacion humana. BMAS actua asi como un **oraculo de complejidad** ademas de una senal de calidad.

## 7.2 La conexion divergencia-alucinacion

Nuestro analisis de valores atipicos proporciona evidencia preliminar de que los modelos identificados como atipicos en el espacio de embedding tienden a tener puntuaciones de precision factual mas bajas. Un sistema de produccion que implemente monitoreo estilo BMAS podria marcar respuestas que se desvian significativamente del cluster de consenso para revision humana.

Sin embargo, advertimos que la correlacion no es causalidad. Una respuesta atipica puede ser correcta mientras el consenso esta equivocado. La respuesta de M1 a A01 (puntuacion CVSS de CVE-2024-21762) lo demostro: la puntuacion atipica era matematicamente correcta mientras los modelos de consenso aceptaban la puntuacion declarada por el proveedor. Cualquier implementacion de produccion de filtrado basado en divergencia debe mantener la capacidad de anulacion humana.

## 7.3 Comparacion de estrategias de sintesis

S1 (voto mayoritario) produce una cobertura exhaustiva pero puede ser verboso e incluir ocasionalmente afirmaciones de minoria de baja confianza. Es mas apropiado cuando la exhaustividad tiene prioridad sobre la concision.

S2 (centroide semantico) produce de forma fiable la respuesta mas "promedio". Funciona mejor cuando se necesita una respuesta representativa y la pregunta esta bien acotada.

S3 (LLM-as-Judge) produce la mayor precision factual en los dominios A y B pero introduce una nueva dependencia: los sesgos propios del modelo juez. El uso de un modelo reservado como juez mitiga este riesgo.

## 7.4 Limitaciones

**Tamano de muestra.** Con 30 prompts en tres dominios, este estudio establece evidencia inicial pero no permite una generalizacion estadistica amplia. Un estudio de seguimiento con 100+ prompts por dominio fortaleceria sustancialmente las afirmaciones.

**Seleccion de modelos.** Los cinco modelos representan una muestra de conveniencia. La composicion de modelos afecta la distribucion del consenso. Los trabajos futuros deberian variar sistematicamente la composicion de modelos.

**Calidad de las respuestas de referencia.** Tres elementos se marcaron como que requieren verificacion manual (discrepancia CVSS de A01, fuente BSI de A10, referencia EDPB de B09).

**Validez temporal.** Las fechas de corte del conocimiento de los LLM y las versiones de los modelos cambian. Los estudios de replicacion deben documentar la version del modelo con precision.

**Temperatura y muestreo.** No se controlo la temperatura entre modelos. La replicacion con temperatura controlada aislarla esta variable.

**La longitud del token no es densidad de informacion.** M4 (Gemini 2.5-pro) fue consistentemente el mas verboso sin una mayor precision factual.

## 7.5 Implicaciones para el despliegue de IA

1. **Consenso como portal de calidad.** En sistemas de IA de alto riesgo, una capa estilo BMAS puede ejecutar varios modelos en la misma consulta y retener la respuesta hasta que el consenso alcance un umbral definido.
2. **Enrutamiento por dominio.** Para consultas factuales con fuentes autorizadas, un unico modelo de alto rendimiento puede ser suficiente. El overhead multi-modelo se justifica mas para consultas estrategicas.
3. **Requisitos de diversidad.** El rendimiento de BMAS depende de la diversidad de modelos. Dos modelos similares del mismo proveedor aportan menos informacion que dos de distintas familias arquitectonicas.

## 7.6 Trabajo futuro

- Estudio de deriva temporal: ejecutar los mismos prompts cada 6 meses
- Expansion de dominios: diagnostico medico, analisis financiero, razonamiento juridico
- Analisis de calibracion: si la confianza del modelo correlaciona con el acuerdo de consenso
- Sintesis adaptativa: seleccion dinamica de S1, S2 o S3 segun la convergencia medida
- Evaluacion humana: comparar la calidad de la sintesis BMAS con respuestas de expertos humanos
