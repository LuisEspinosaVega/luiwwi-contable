# Arquitectura del MVP Laravel modular

Aplicar sólo al diseñar un producto y respetar la tecnología elegida. Estos módulos son una base, no una restricción de cobertura. Si el alcance incluye contabilidad, agregar catálogo/pólizas/mayor, auxiliares, periodos/cierre, reglas fiscales y declaraciones según [la matriz](alcance-cobertura.md). Separar generación, validación y presentación oficial. Mantener reglas y layouts versionados con vigencia y pruebas del caso.

## Módulos

| Módulo | Responsabilidad |
|---|---|
| Identity/Tenancy | usuarios, organizaciones, RFC, roles y permisos |
| Credentials | referencias cifradas a e.firma y operación de firma aislada |
| SAT Download | solicitudes, estados, paquetes, reintentos y cuotas |
| XML Vault | objeto original, hash, cuarentena y procedencia |
| CFDI | parser, modelo normalizado, validaciones y estado SAT |
| Reconciliation | REP, relaciones, cancelaciones y futuro banco |
| Analytics | proyecciones versionadas, KPIs y cobertura |
| Audit | eventos sensibles y versiones de reglas |

Mantener dependencias dirigidas: descarga entrega bytes a la bóveda; CFDI consume una referencia inmutable; analítica consume proyecciones, no XML en cada petición.

## Persistencia

MySQL es suficiente para metadatos y proyecciones si se usan:

- `DECIMAL`, nunca `FLOAT`, para importes;
- índices por tenant, UUID, RFC, fechas, tipo y estado;
- claves únicas idempotentes;
- JSON sólo para datos variables/diagnóstico, no para campos críticos de consulta;
- tablas separadas para conceptos, impuestos, relaciones, pagos y estados históricos.

Guardar XML/ZIP en almacenamiento de objetos cifrado, no como blobs principales de MySQL. Conservar hash, tamaño y referencia en la base.

## Ejecución

Laravel + React/Inertia funciona para el monolito modular. Ejecutar descarga, descompresión, parsing, XSD, consulta SAT y recálculo en colas. Dividir trabajos por solicitud, paquete y XML, con idempotencia, timeouts, backoff y cola de fallos.

No mantener una petición HTTP abierta esperando al SAT. El frontend consulta progreso agregado y errores accionables sin recibir secretos.

## Proyecciones y reglas

Guardar hechos inmutables y construir proyecciones recalculables. Versionar:

- parser/esquemas;
- catálogos y matrices;
- reglas fiscales;
- política de moneda/redondeo;
- definición de KPI.

Cuando cambie una regla, crear una nueva versión y recalcular de forma controlada. No reinterpretar silenciosamente reportes anteriores.

## Escalamiento

Empezar con un despliegue monolítico, workers separados y almacenamiento de objetos. Extraer servicios sólo cuando existan límites medidos —aislamiento criptográfico, volumen de parsing o equipos independientes—, manteniendo contratos de módulo desde el inicio.

## Pruebas esenciales

- fixtures anonimizados por tipo, moneda, complemento y estado;
- duplicados, ZIP bomb, XML enorme, namespace alternativo y XML malicioso;
- redondeos límite, parcialidades y multimoneda;
- cancelación/sustitución y relaciones faltantes;
- aislamiento entre tenants;
- reintentos sin duplicar paquetes, XML o métricas;
- pruebas de regresión por versión de XSD/catálogo/regla.
