# 8. Conclusión

Este artículo presentó **Blind Multi-Agent Synthesis (BMAS)**, una metodología para elicitar, comparar y sintetizar respuestas de múltiples modelos de lenguaje grande en estricto aislamiento, y presentó resultados empíricos de un experimento de 150 ejecuciones en cinco LLMs frontier y tres estratos de dominio.

## 8.1 Resumen de contribuciones

Demostramos que:

1. **La convergencia es dependiente del dominio y medible.** En 30 prompts, los dominios A y B (técnico y regulatorio) mostraron consistentemente mayor similitud semántica inter-modelos que el dominio C (prompts estratégicos y ambiguos). [Véase la sección 4 para valores exactos.]

2. **La divergencia señaliza error en los dominios factuales.** Los modelos identificados como valores atípicos semánticos mostraron menor precisión factual frente a las respuestas de referencia pre-registradas que los modelos no atípicos, apoyando la hipótesis H2.

3. **La calidad de la síntesis varía según la estrategia y el dominio.** La síntesis LLM-as-Judge (S3) produjo la mayor precisión factual en los dominios A y B, mientras que el voto mayoritario (S1) proporcionó la cobertura más exhaustiva. Ninguna estrategia única dominó en todos los tipos de prompts.

4. **La longitud del token no es un indicador de calidad.** Observamos una variación significativa en el recuento de tokens de respuesta entre modelos en prompts idénticos (hasta 6,5 veces en algunos prompts), sin correlación consistente con la precisión factual.

## 8.2 Conclusiones prácticas

Para los profesionales que despliegan LLMs en entornos regulados o de alto riesgo, BMAS sugiere una arquitectura práctica: ejecutar prompts en múltiples proveedores de modelos independientes, medir la convergencia semántica y enrutar las respuestas de baja confianza (alta divergencia) hacia revisión humana. El protocolo de pre-registro utilizado en este estudio es transferible a cualquier esfuerzo de evaluación multi-modelo y evita el sesgo de confirmación.

## 8.3 Relación con AEGIS, AAHP y failprompt

BMAS fue desarrollado en el contexto de AEGIS, un sistema de verificación de identidad gubernamental transfronterizo de la UE que abarca conectores para múltiples países europeos, AAHP (AI-to-AI Handoff Protocol), un framework estructurado de orquestación multi-agente para pipelines de IA en producción, y failprompt, una herramienta CLI para validar respuestas de IA en entornos CI/CD. Juntos, estos tres proyectos forman un kit de herramientas integrado para el despliegue responsable de IA multi-modelo: AAHP proporciona la capa de orquestación, failprompt el portal CI, y BMAS la base empírica para comprender cuándo y por qué el consenso multi-modelo es más fiable que la salida de un modelo único.

Todos los códigos, prompts, respuestas de referencia pre-registradas y resultados experimentales se publican como datasets abiertos que apoyan la replicación y extensión de este trabajo.

---

*El dataset BMAS, el runner, el pipeline de métricas y el código de síntesis están disponibles en: https://github.com/homeofe/BMAS*
