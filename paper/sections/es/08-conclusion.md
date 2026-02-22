# 8. Conclusion

Este articulo presento **Blind Multi-Agent Synthesis (BMAS)**, una metodologia para elicitar, comparar y sintetizar respuestas de multiples modelos de lenguaje grande en estricto aislamiento, y presento resultados empiricos de un experimento de 150 ejecuciones en cinco LLMs frontier y tres estratos de dominio.

## 8.1 Resumen de contribuciones

Demostramos que:

1. **La convergencia es dependiente del dominio y medible.** En 30 prompts, los dominios A y B (tecnico y regulatorio) mostraron consistentemente mayor similitud semantica inter-modelos que el dominio C (prompts estrategicos y ambiguos). [Vease la seccion 4 para valores exactos.]

2. **La divergencia senializa error en los dominios factuales.** Los modelos identificados como valores atipicos semanticos mostraron menor precision factual frente a las respuestas de referencia pre-registradas que los modelos no atipicos, apoyando la hipotesis H2.

3. **La calidad de la sintesis varia segun la estrategia y el dominio.** La sintesis LLM-as-Judge (S3) produjo la mayor precision factual en los dominios A y B, mientras que el voto mayoritario (S1) proporciono la cobertura mas exhaustiva. Ninguna estrategia unica domino en todos los tipos de prompts.

4. **La longitud del token no es un indicador de calidad.** Observamos una variacion significativa en el recuento de tokens de respuesta entre modelos en prompts identicos (hasta 6,5 veces en algunos prompts), sin correlacion consistente con la precision factual.

## 8.2 Conclusiones practicas

Para los profesionales que despliegan LLMs en entornos regulados o de alto riesgo, BMAS sugiere una arquitectura practica: ejecutar prompts en multiples proveedores de modelos independientes, medir la convergencia semantica y enrutar las respuestas de baja confianza (alta divergencia) hacia revision humana. El protocolo de pre-registro utilizado en este estudio es transferible a cualquier esfuerzo de evaluacion multi-modelo y evita el sesgo de confirmacion.

## 8.3 Relacion con AEGIS, AAHP y failprompt

BMAS fue desarrollado en el contexto de AEGIS, un sistema de verificacion de identidad gubernamental transfronterizo de la UE que abarca conectores para multiples paises europeos, AAHP (AI-to-AI Handoff Protocol), un framework estructurado de orquestacion multi-agente para pipelines de IA en produccion, y failprompt, una herramienta CLI para validar respuestas de IA en entornos CI/CD. Juntos, estos tres proyectos forman un kit de herramientas integrado para el despliegue responsable de IA multi-modelo: AAHP proporciona la capa de orquestacion, failprompt el portal CI, y BMAS la base empirica para comprender cuando y por que el consenso multi-modelo es mas fiable que la salida de un modelo unico.

Todos los codigos, prompts, respuestas de referencia pre-registradas y resultados experimentales se publican como datasets abiertos.

---

*El dataset BMAS, el runner, el pipeline de metricas y el codigo de sintesis estan disponibles en: https://github.com/homeofe/BMAS*
