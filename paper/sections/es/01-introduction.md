# 📝 1. Introducción

Los modelos de lenguaje grande han alcanzado un nivel de capacidad suficiente para ser desplegados en dominios donde la precisión no es opcional: análisis jurídico, diagnóstico médico, cumplimiento regulatorio y sistemas de identidad gubernamentales. En estos dominios, una respuesta segura pero incorrecta de un modelo único no es un inconveniente menor - es un fallo con consecuencias reales.

El enfoque dominante para mejorar la fiabilidad de los LLM es o bien un mejor entrenamiento (RLHF, Constitutional AI) o bien un mejor prompting (cadena de pensamiento, aumento por recuperación). Ambos operan dentro de un paradigma de modelo único: un modelo, una salida, una respuesta en la que confiar o no.

Este trabajo adopta un enfoque diferente. En lugar de preguntar "cómo hacemos un modelo más fiable", preguntamos: **¿qué podemos aprender del desacuerdo entre múltiples modelos que no pueden influirse mutuamente?**

## 1.1 La intuición central

Cuando cinco expertos independientes responden a la misma pregunta sin consultarse entre sí, y cuatro de ellos dan la misma respuesta mientras uno da una diferente, no concluimos que los cuatro están equivocados. Examinamos la respuesta disidente con más cuidado, pero confiamos en el consenso como punto de partida.

Este es el método Delphi, aplicado desde 1963 a la predicción experta. Su fortaleza es estructural: **el aislamiento previene el pensamiento grupal; el consenso emerge del razonamiento independiente, no de la presión social.**

BMAS aplica esta lógica a los LLMs. Cada modelo es un experto con una distribución de entrenamiento particular, un horizonte de conocimiento y un conjunto de sesgos. Cuando se les aísla entre sí y se les hace la misma pregunta, su convergencia o divergencia es en sí misma informativa.

## 1.2 Qué hay de nuevo

Varios trabajos previos son relacionados pero distintos:

**Self-Consistency** (Wang et al., 2022) genera múltiples cadenas de razonamiento a partir de un *único* modelo y usa votación mayoritaria. BMAS utiliza modelos *diferentes* - esto prueba a través de distribuciones de entrenamiento, no solo varianza de decodificación.

**Mixture of Agents** (Wang et al., 2024) permite a los modelos ver las salidas de los demás en rondas de agregación. Esto produce refinamiento colaborativo, pero introduce el riesgo de propagación de errores: si un modelo produce una alucinación segura en la primera ronda, los modelos siguientes pueden anclarse a ella.

**LLM-as-Judge** (Zheng et al., 2023) usa un modelo para evaluar a otro. BMAS usa un modelo para *sintetizar* las salidas de varios otros - el papel de juez se limita a la fase final de síntesis.

BMAS es el primer framework que combina cuatro propiedades:
1. Aislamiento ciego estricto (sin contaminación cruzada)
2. Diversidad de modelos (distintos proveedores, arquitecturas, distribuciones de entrenamiento)
3. Análisis estratificado por dominio (factual, regulatorio, estratégico)
4. Divergencia como señal (no como fallo)

## 1.3 Motivación práctica

Esta investigación surgió de la experiencia operativa construyendo AEGIS, un sistema de verificación de identidad gubernamental transfronterizo de la UE, y AAHP (AI-to-AI Handoff Protocol), un framework estructurado de orquestación multi-agente. En ambos sistemas, los pipelines multi-agente se utilizan para decisiones de arquitectura, análisis de cumplimiento y revisión de implementaciones.

Surgió una pregunta práctica: cuando se utilizan múltiples LLMs como revisores independientes en un pipeline, ¿cuánto difieren realmente sus salidas? ¿Y cuando difieren, quién tiene razón?

BMAS es la respuesta formal a esa pregunta.

## 1.4 Contribuciones

Este trabajo aporta:

1. **Metodología BMAS:** Un protocolo formalizado de síntesis ciega multi-agente con restricciones de aislamiento, conjunto de métricas y estrategias de síntesis.
2. **Estudio empírico:** Resultados de 45 prompts para 12 LLMs en 3 estratos de dominio, con respuestas de referencia pre-registradas para los dominios A y B.
3. **Validación de la hipótesis divergencia-como-señal:** Evidencia estadística de que la divergencia entre modelos predice la tasa de errores factuales.
4. **Comparación de estrategias de síntesis:** Evaluación empírica del voto mayoritario, centroide semántico y síntesis LLM-as-Judge frente a respuestas de referencia.
5. **Dataset abierto:** Todos los prompts, respuestas crudas de los modelos e indicadores de métricas publicados como benchmark público.

## 1.5 Estructura del artículo

La sección 2 revisa trabajos relacionados. La sección 3 describe la metodología BMAS y el diseño experimental. La sección 4 presenta los resultados. La sección 5 analiza correlaciones divergencia-alucinación. La sección 6 evalúa las estrategias de síntesis. La sección 7 discute implicaciones, limitaciones y trabajos futuros. La sección 8 concluye.
