# FUMOFUMO_STORE ᗜˬᗜ
DA FUNNY FUMOFUMO STORE ᗜˬᗜ

Bitacoras de uso de IA

1. "Actúa como un arquitecto de software senior especializado en desarrollo web backend con Python y Django. Necesito diseñar la estructura de directorios y el flujo de vistas para una aplicación modular que gestione catálogos digitales y galerías interactivas. Propón una arquitectura limpia (Clean Architecture o patrón MTV adaptado) que separe la lógica de negocio, las vistas de enrutamiento y la persistencia de datos, priorizando la escalabilidad y minimizando acoplamientos innecesarios."

Razón: La respuesta del uso de este prompt de la separación de los microservicios excesivo para este proyecto, la cual se ajusto para que Django pueda garantizar un tiempo de desarrollo agradable sin sacrificar codigo

2. "Actúa como un especialista en bases de datos relacionales y optimización de ORM. Necesito definir los modelos de datos para una aplicación que maneje usuarios, colecciones de arte digital y metadatos asociados. Escribe las clases de modelos optimizadas utilizando el ORM de Django, asegurando el uso correcto de claves foráneas (ForeignKey, ManyToManyField), índices en campos de búsqueda frecuente, y la prevención del problema de consultas N+1 mediante el uso de select_related y prefetch_related."

Razón:  En primeras iteraciónes, la IA ocupada se ómitio la restriccion de de rendimiento al frente de consultas masivas. Fue necesario para la precarga se (select_related) para la pagina

3. "Actúa como un auditor de ciberseguridad y desarrollador backend consciente de OWASP. Revisa los mecanismos de autenticación y gestión de sesiones para nuestra aplicación web. Proporciona directrices y fragmentos de código para implementar hashing de contraseñas seguro, protección contra ataques CSRF, validación estricta de formularios y restricciones de acceso basadas en roles (RBAC) a nivel de vistas."

Razón: Las recomendación de uso de un experto de ciberseguridad fue para poder recomendar la seguridad de la pagina web y que garantice que la pagina sea segura sin que comprometa alguna vulnerabilidad cibernetica 