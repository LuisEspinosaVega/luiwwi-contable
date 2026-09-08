# Cumplimiento, seguridad y riesgo

## Datos sensibles

CFDI y e.firma contienen datos fiscales, personales y comerciales. Aplicar mínimo privilegio, segregación por tenant, cifrado en tránsito/reposo, auditoría de acceso, respaldo probado y borrado conforme a política autorizada.

La llave privada de e.firma no debe salir del componente de firma. No exponerla a personal de soporte, frontend, analítica, prompts, logs o volcados. Implementar expiración, rotación, revocación de acceso y respuesta a incidentes.

## Aislamiento multi-tenant

- Incluir `tenant_id` en todas las claves y consultas de dominio.
- Aplicar autorización en servicio y base de datos cuando sea posible.
- Usar rutas de objetos no predecibles y URLs firmadas breves.
- Probar fugas horizontales, exportaciones, trabajos en cola y cachés.
- No usar RFC como secreto ni como único control de acceso.

## Auditoría

Registrar quién, qué, cuándo y por qué para credenciales, solicitudes SAT, descargas, cambios de clasificación, conciliaciones, exportaciones y cancelaciones. El log debe ser inmutable o resistente a manipulación y omitir secretos.

Conservar la versión de parser, reglas, catálogos y fuentes que produjo cada resultado. Un recálculo no debe borrar el resultado histórico.

## Riesgo fiscal

Consultas como listas del artículo 69-B son señales con fecha y etapa procesal. Mostrar fuente, coincidencia exacta del RFC, fecha, categoría y última actualización. No bloquear pagos ni acusar a una contraparte automáticamente; escalar a revisión humana.

## Retención

No fijar un único plazo de conservación para todo. Parametrizar por tipo de expediente y revisar CFF, obligaciones mercantiles, laborales, privacidad y litigios aplicables. Una eliminación debe estar autorizada, auditada y considerar respaldos.

## Salidas y soporte

- Enmascarar RFC/UUID cuando no sean necesarios.
- Evitar exportaciones masivas por defecto.
- Usar datos sintéticos en desarrollo y soporte.
- No mandar XML reales a servicios de terceros sin base, contrato, información al usuario y controles adecuados.
- Mostrar que la aplicación organiza evidencia y estimaciones; no garantiza por sí sola cumplimiento fiscal.
