# Propuesta de Proyecto: Sistema de Alerta Sísmicas

## Entendimiento de la situación actual

En esta sección, vamos a contextualizar la problemática de las alertas sísmicas y expresar posibles análisis y soluciones en torno a la misma.

En la actualidad, la detección temprana de sismos y la rápida notificación a la población son aspectos fundamentales para reducir los daños y las pérdidas humanas ocasionadas por los terremotos. Sin embargo, existen desafíos importantes que requieren atención:

- La falta de un sistema de alerta sísmica eficiente y confiable dificulta la capacidad de las autoridades y los ciudadanos para tomar medidas preventivas.
- La falta de una infraestructura adecuada para la detección y comunicación de sismos impide una respuesta rápida y coordinada ante eventos sísmicos.
- Las tecnologías existentes para la detección de sismos a menudo presentan falsas alarmas o no logran detectar sismos de menor magnitud que también pueden ser peligrosos.
- La falta de concientización y educación de la población sobre cómo actuar durante un sismo y cómo interpretar las alertas sísmicas contribuye a la vulnerabilidad de las comunidades.

Para abordar estos desafíos, es necesario desarrollar un sistema de alerta sísmica que combine tecnologías avanzadas de detección y comunicación, así como estrategias de difusión y educación de la población. El proyecto busca establecer un sistema confiable y robusto que permita una detección temprana de los sismos, una rápida notificación a la población afectada y una correcta interpretación de las alertas para tomar las medidas adecuadas de protección.

Además, es fundamental considerar aspectos como la escalabilidad del sistema, su integración con los dispositivos y plataformas existentes, y la posibilidad de colaborar con instituciones gubernamentales y expertos en sismología para obtener datos precisos y actualizados.

Al abordar estos desafíos y desarrollar un sistema de alerta sísmica efectivo, estaremos contribuyendo significativamente a la protección de la vida humana y la reducción de los impactos negativos causados por los sismos.

## Objetivos

Los objetivos del proyecto son acciones concretas que describen claramente lo que buscamos lograr:

- Desarrollar un sistema de alerta sísmicas eficiente y confiable.
- Crear una plataforma para la detección temprana de sismos y notificación a la población afectada.
- Implementar algoritmos de procesamiento de señales sísmicas para una detección precisa.
- Integrar el sistema con dispositivos móviles y otros medios de comunicación para una amplia difusión de las alertas.

## Alcance

Dado que las temáticas relacionadas con las alertas sísmicas son amplias, es importante delimitar el alcance del proyecto y definir las tareas y desarrollos principales. Sin embargo, es posible que existan aspectos más complejos o que requieran más tiempo y estén fuera del alcance actual del proyecto. Estas son algunas posibilidades de continuidad del proyecto:

- Desarrollo e implementación de un bot de notificación para enviar alertas sísmicas a la población afectada.
- Integración del bot con una fuente confiable de información sísmica para obtener datos actualizados en tiempo real.
- Configuración del bot para recibir y procesar información sobre los sismos detectados y enviar notificaciones de manera oportuna.
- Realización de pruebas exhaustivas del sistema de alerta para evaluar su funcionamiento y eficacia.
- Documentación detallada del proceso de desarrollo del bot y las pruebas realizadas.


## KPI Asociados
- Promedio de temblores por mes: Calcula el promedio de temblores registrados por mes en los datos históricos. Este KPI  dará una idea de los meses con mayor actividad sísmica.

- Máximo y mínimo de magnitud de temblores: Identifica el temblor de mayor magnitud y el de menor magnitud registrado en los datos históricos. Estos KPIs darán información sobre la variabilidad en la intensidad de los temblores.

- Porcentaje de temblores por nivel de intensidad: Clasifica los temblores en diferentes niveles de intensidad (por ejemplo, bajo, moderado, alto) y calcula el porcentaje de temblores en cada categoría. Este KPI  permitirá comprender la distribución de los temblores en función de su intensidad.

- Histograma de ocurrencias mensuales: Crea un histograma que muestre la distribución de temblores a lo largo del año, con barras que representen el número de temblores por mes. Este KPI visual ayudará a identificar los meses con mayor y menor ocurrencia de temblores.

- Tendencias temporales de la actividad sísmica: Utiliza análisis de series de tiempo para identificar tendencias en la actividad sísmica a lo largo de los años.


## Solución Propuesta
### Stack Tecnológico
- Lenguaje de programación: Python
- Base de datos: MongoDB
- Librerías de procesamiento de señales: NumPy, Pandas
- Librerías de machine learning: Scikit-learn
- Herramientas de visualización de datos: Matplotlib, Seaborn y Flourish
- Integración con dispositivos móviles: Telegram, WhatsApp (Opcional) 

### Metodología de Trabajo
Para el desarrollo del proyecto de Sistema de Alerta Sísmicas, se utilizará la metodología de trabajo ágil, específicamente Scrum. Esta metodología permitirá una gestión eficiente del proyecto, fomentando la colaboración, la adaptabilidad y la entrega continua de valor.

El equipo de desarrollo se organizará de la siguiente manera:

**Product Owner**: Será responsable de definir y priorizar los requisitos del proyecto, basándose en las necesidades de los usuarios y las metas del negocio. Además, será el enlace entre el equipo de desarrollo y los stakeholders, asegurando una comunicación fluida y una visión clara del producto.

**Scrum Master**: Actuará como facilitador del proceso Scrum, asegurando que se sigan las prácticas y los roles establecidos. El Scrum Master será responsable de remover los obstáculos que puedan surgir durante el desarrollo y garantizará un ambiente de trabajo colaborativo y productivo.

**Equipo de Desarrollo**: Estará compuesto por desarrolladores, diseñadores y especialistas en bases de datos. Serán responsables de implementar las funcionalidades del sistema, realizar las pruebas necesarias y entregar los entregables definidos en cada sprint.

### Diseño detallado - Entregables
### Equipo de trabajo - Roles y responsabilidades
Por favor revisar [contributing.md](https://github.com/Magic-Mario/sismos_clas_henry/blob/test/contributing.md)
### Cronograma General - Gantt
Direccionamiento a diagrama de Gantt [aqui](https://github.com/Magic-Mario/sismos_clas_henry/blob/test/diag_gantt/PF-Henry-diagrama_gantt.pdf)
### Análisis preliminar de calidad de datos
Link directo al notebook con el analisis exploratorio de datos [aqui](https://github.com/Magic-Mario/sismos_clas_henry/blob/test/src/notebooks/eda.ipynb)
