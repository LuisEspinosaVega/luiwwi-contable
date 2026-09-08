# Cancelaciones y relaciones

## Estado y evidencia

Una cancelación es un cambio de estado, no un borrado. Conservar XML, estado anterior, solicitud, motivo, folio de sustitución si aplica, respuesta, instante y evidencia de aceptación/rechazo.

Estados internos recomendados: `desconocido`, `vigente`, `cancelable_sin_aceptacion`, `cancelable_con_aceptacion`, `solicitud_pendiente`, `cancelado`, `rechazado` y `no_cancelable`. Mapearlos desde respuestas reales; no deducirlos sólo del motivo.

## Aceptación del receptor

La regla 2.7.1.34 de la RMF 2026 da al receptor tres días siguientes a la recepción de la solicitud para aceptar o rechazar. En general, el silencio se considera aceptación; hay tratamientos expresos para ciertas operaciones de hidrocarburos/combustibles con Carta Porte. Verificar siempre la regla del ejercicio.

## Cancelación sin aceptación

La regla 2.7.1.35 contiene supuestos específicos. Entre los relevantes:

- comprobantes hasta $1,000, con excepciones; este supuesto no incluye CFDI de pagos y tiene restricciones para operaciones de hidrocarburos/combustibles;
- nómina, egreso, traslado y retenciones bajo sus condiciones;
- operaciones con público en general y ciertos residentes en el extranjero;
- cancelación dentro del día hábil siguiente a la expedición, también sujeta a la restricción final de la regla para determinadas operaciones de hidrocarburos/combustibles.

No convertir esta lista resumida en código sin leer la regla completa y sus excepciones. Es incorrecto afirmar que un REP sólo puede cancelarse sin aceptación el mismo día: el supuesto del día hábil siguiente debe evaluarse conforme a la regla aplicable.

## Motivos

Las claves usadas actualmente son:

| Clave | Sentido |
|---|---|
| `01` | Comprobante emitido con errores con relación |
| `02` | Comprobante emitido con errores sin relación |
| `03` | No se llevó a cabo la operación |
| `04` | Operación nominativa relacionada en una factura global |

Con `01`, registrar el UUID sustituto exigido por el flujo. El motivo no demuestra por sí mismo que el reemplazo sea materialmente correcto.

## Efecto analítico

- Excluir un CFDI sólo desde la perspectiva temporal que corresponda al reporte; para auditoría histórica mostrar su transición.
- Un CFDI cancelado no aporta facturación vigente, pero puede explicar una sustitución.
- Una solicitud pendiente no equivale a cancelación consumada.
- Recalcular REP, saldos, notas y métricas cuando cambie el estado.
- Mantener la fecha de última consulta y marcar como incompleto un reporte con estado envejecido.

## Relaciones

Guardar relaciones como aristas dirigidas con tipo y fecha de conocimiento. Detectar ciclos, múltiples sustitutos y referencias ausentes. No asumir que el XML relacionado está disponible: reportar huecos de descarga.
