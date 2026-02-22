# 1. Introduccion

Los modelos de lenguaje grande han alcanzado un nivel de capacidad suficiente para ser desplegados en dominios donde la precision no es opcional: analisis juridico, diagnostico medico, cumplimiento regulatorio y sistemas de identidad gubernamentales. En estos dominios, una respuesta segura pero incorrecta de un modelo unico no es un inconveniente menor - es un fallo con consecuencias reales.

El enfoque dominante para mejorar la fiabilidad de los LLM es o bien un mejor entrenamiento (RLHF, Constitutional AI) o bien un mejor prompting (cadena de pensamiento, aumento por recuperacion). Ambos operan dentro de un paradigma de modelo unico: un modelo, una salida, una respuesta en la que confiar o no.

Este trabajo adopta un enfoque diferente. En lugar de preguntar "como hacemos un modelo mas fiable", preguntamos: **que podemos aprender del desacuerdo entre multiples modelos que no pueden influirse mutuamente?**

## 1.1 La intuicion central

Cuando cinco expertos independientes responden a la misma pregunta sin consultarse entre si, y cuatro de ellos dan la misma respuesta mientras uno da una diferente, no concluimos que los cuatro estan equivocados. Examinamos la respuesta disidente con mas cuidado, pero confiamos en el consenso como punto de partida.

Este es el metodo Delphi, aplicado desde 1963 a la prediccion experta. Su fortaleza es estructural: **el aislamiento previene el pensamiento grupal; el consenso emerge del razonamiento independiente, no de la presion social.**

BMAS aplica esta logica a los LLMs. Cada modelo es un experto con una distribucion de entrenamiento particular, un horizonte de conocimiento y un conjunto de sesgos. Cuando se les aisla entre si y se les hace la misma pregunta, su convergencia o divergencia es en si misma informativa.

## 1.2 Que hay de nuevo

Varios trabajos previos son relacionados pero distintos:

**Self-Consistency** (Wang et al., 2022) genera multiples cadenas de razonamiento a partir de un *unico* modelo y usa votacion mayoritaria. BMAS utiliza modelos *diferentes* - esto prueba a traves de distribuciones de entrenamiento, no solo varianza de decodificacion.

**Mixture of Agents** (Wang et al., 2024) permite a los modelos ver las salidas de los demas en rondas de agregacion. Esto produce refinamiento colaborativo, pero introduce el riesgo de propagacion de errores: si un modelo produce una alucinacion segura en la primera ronda, los modelos siguientes pueden anclarse a ella.

**LLM-as-Judge** (Zheng et al., 2023) usa un modelo para evaluar a otro. BMAS usa un modelo para *sintetizar* las salidas de varios otros - el papel de juez se limita a la fase final de sintesis.

BMAS es el primer framework que combina cuatro propiedades:
1. Aislamiento ciego estricto (sin contaminacion cruzada)
2. Diversidad de modelos (distintos proveedores, arquitecturas, distribuciones de entrenamiento)
3. Analisis estratificado por dominio (factual, regulatorio, estrategico)
4. Divergencia como senal (no como fallo)

## 1.3 Motivacion practica

Esta investigacion surgio de la experiencia operativa construyendo AEGIS, un sistema de verificacion de identidad gubernamental transfronterizo de la UE, y AAHP (AI-to-AI Handoff Protocol), un framework estructurado de orquestacion multi-agente. En ambos sistemas, los pipelines multi-agente se utilizan para decisiones de arquitectura, analisis de cumplimiento y revision de implementaciones.

Surgio una pregunta practica: cuando se utilizan multiples LLMs como revisores independientes en un pipeline, cuanto difieren realmente sus salidas? Y cuando difieren, quien tiene razon?

BMAS es la respuesta formal a esa pregunta.

## 1.4 Contribuciones

Este trabajo realiza las siguientes contribuciones:

1. **Metodologia BMAS:** Un protocolo formalizado de sintesis multi-agente ciega con restricciones de aislamiento, suite de metricas y estrategias de sintesis.
2. **Estudio empirico:** Resultados de 30 prompts sobre 5 LLMs en 3 estratos de dominio, con respuestas de referencia pre-registradas para los dominios A y B.
3. **Validacion de la hipotesis divergencia-como-senal:** Evidencia estadistica de que la divergencia inter-modelos predice la tasa de error factual.
4. **Comparacion de estrategias de sintesis:** Evaluacion empirica del voto mayoritario, el centroide semantico y la sintesis LLM-as-Judge frente a respuestas de referencia.
5. **Dataset abierto:** Todos los prompts, salidas brutas de los modelos y puntuaciones de metricas publicados como benchmark publico.

## 1.5 Estructura del articulo

La seccion 2 revisa los trabajos relacionados. La seccion 3 describe la metodologia BMAS y el diseno experimental. La seccion 4 presenta los resultados. La seccion 5 analiza la correlacion divergencia-alucinacion. La seccion 6 evalua las estrategias de sintesis. La seccion 7 discute implicaciones, limitaciones y trabajo futuro. La seccion 8 concluye.
