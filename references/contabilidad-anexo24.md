# Contabilidad electrónica y Anexo 24 RMF

Base: [Anexo 24 RMF 2026](https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo_24_RMF2026-13012026.pdf), publicado 13-01-2026; CFF 28/30-A y RMF del periodo. No confundir con Anexo 24 RGCE.

## Obligación por componente

Separar llevar registros, formato electrónico, envío de catálogo/balanza y entrega de pólizas/auxiliares por requerimiento o supuesto específico. Resolver facilidades por régimen, ingresos, opción y periodo; no eximir a todas las PF, plataformas o RESICO por etiqueta.

Consultar RMF 2026 2.8.1.5 (contabilidad), 2.8.1.6 (envío), 2.8.1.8 (requerimiento) y facilidades, contrastando modificaciones. No enviar pólizas mensualmente por defecto ni eliminar su conservación.

## Catálogo propio

Guardar número, nombre, superior, nivel, naturaleza, vigencia y código agrupador separado. Mapear cuentas exportables al catálogo SAT vigente con revisión; compartir número no prueba correspondencia. Por ejemplo, el Anexo oficial denomina 104.01 «Otros instrumentos financieros», no clientes.

## Archivos y controles

| Componente | Preparación |
|---|---|
| Catálogo | Jerarquía, cuentas reportables y equivalencia vigente |
| Balanza | Saldos iniciales, cargos, abonos y finales; periodo y normal/complementaria |
| Pólizas | Eventos, cuentas, comprobantes, pagos y detalle requerido según supuesto |
| Auxiliar de folios | Relaciones entre pólizas y documentos cuando corresponda |
| Auxiliar de cuentas | Movimientos y saldos trazables al mayor |

Descargar documento técnico y XSD oficiales con dependencias. Versionar namespaces, catálogos, nomenclatura y ZIP; validar contra esa versión. Revisar opcionalidad/obligatoriedad de sello/certificado por esquema/canal; no confundir firma de acceso/envío con timbrado CFDI ni afirmar que todo XML requiere el mismo sello.

Conciliar con mayor y periodo aprobado. Validar RFC, cuentas, fechas, decimales, relaciones y balance. Resolver balanza de cierre, complementarias y cambios de catálogo por regla; no crear «periodo 13» como mes válido por costumbre del ERP.

## Entrega

Calcular vencimiento por sujeto, periodicidad y supuesto, incluyendo meses sin movimientos y facilidades. Conservar XML/ZIP exacto, hash, versión, fecha, folio, respuesta y acuse de aceptación/rechazo. Corregir sin borrar envíos anteriores. El validador local no acredita recepción SAT.

Para registro y cierre usar [contabilidad-cierre.md](contabilidad-cierre.md). Preparar archivos está dentro del alcance; no se incluye un exportador ejecutable Anexo 24.
