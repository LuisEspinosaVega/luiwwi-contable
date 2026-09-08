# Descarga y almacenamiento

## Servicio oficial

El servicio de descarga permite recuperar CFDI emitidos o recibidos como XML o metadatos. La autenticación usa e.firma vigente y WS-Security; no debe confundirse con una descarga automatizada del portal por navegador.

Flujo lógico:

1. firmar y enviar solicitud con contribuyente, rol, periodo y filtros admitidos;
2. guardar el identificador de solicitud y la huella de sus parámetros;
3. consultar su estado con espera incremental y límite de reintentos;
4. al terminar, guardar todos los identificadores de paquete;
5. descargar cada paquete, verificar integridad y registrar resultado;
6. descomprimir en entorno limitado e ingerir cada XML de forma idempotente.

Estados documentados por el SAT para la verificación: `1 Aceptada`, `2 En proceso`, `3 Terminada`, `4 Error`, `5 Rechazada`, `6 Vencida`. Los paquetes expiran 72 horas después de su generación según la especificación consultada. No inventar un estado adicional: modelar fallas locales por separado.

## Idempotencia y reintentos

- La clave de una solicitud local debe incluir tenant, RFC, rol, intervalo, filtros y versión del conector.
- Un mismo XML puede aparecer en distintos paquetes. Deduplicar por hash y UUID, sin perder la relación con cada paquete.
- Reintentar sólo fallas transitorias. Errores de autenticación, parámetros o límites requieren acción específica.
- Registrar código SAT y mensaje sin incluir llave, contraseña, XML completo ni datos innecesarios.
- No fijar en código endpoints o cuotas obtenidos de una guía antigua; obtenerlos de configuración versionada y documentación vigente.

## Bóveda original

Guardar el XML exactamente como fue recibido, cifrado y sin mutación. Metadatos mínimos:

- tenant y RFC propietario;
- UUID si se pudo extraer;
- rol emitido/recibido;
- hash SHA-256, tamaño y tipo MIME comprobado;
- solicitud y paquete de procedencia;
- instante de descarga/importación;
- ruta o identificador del objeto;
- versión del parser y resultado de cada capa de validación.

El hash identifica bytes, no validez fiscal. La unicidad primaria puede basarse en `tenant + UUID`, pero debe permitir cuarentena de colisiones, XML sin timbre y distintas copias binarias para investigación.

## Ingesta segura

- Limitar tamaño total, cantidad de entradas, tamaño expandido y relación de compresión del ZIP.
- Rechazar rutas absolutas o con `..`; no extraer directamente a una ruta pública.
- Desactivar DTD y entidades externas; controlar profundidad y cantidad de nodos.
- Detectar cifrado, corrupción y archivos no XML.
- Procesar por streaming o en trabajos pequeños; evitar cargar paquetes completos en memoria.
- Enviar a cuarentena lo ilegible sin perder evidencia.

## Estado SAT

La presencia en una descarga no prueba que el CFDI siga vigente. Consultar estado por un proceso separado, guardar fecha, parámetros, respuesta y transición. Conservar estados históricos; nunca sobrescribir la única evidencia anterior.

## Credenciales

La e.firma contiene una llave privada de alto impacto. Preferir firma en un componente aislado, cifrado con KMS/HSM, permisos mínimos, rotación y auditoría. Nunca guardarla en la base de datos general, repositorio, log, respaldo sin cifrar o telemetría.
