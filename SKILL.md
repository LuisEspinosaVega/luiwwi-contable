---
name: luiwwi-contable
description: >
  Experto en Contabilidad Electrónica Mexicana y CFDI 4.0 (Anexo 20/24 del SAT). Úsala para
  procesar, validar o generar pólizas desde XML de CFDI (ingreso, egreso, traslado, pago/CRP,
  nómina), Retenciones 2.0, o complementos (Carta Porte, Comercio Exterior, Plataformas
  Tecnológicas). También para: desglose de IVA/ISR/IEPS por tasa (16%/8%/0%/exento),
  cuadratura y redondeo del Anexo 20, Catálogo Agrupador SAT, XML de Pólizas Periodo, PUE vs
  PPD, cancelación de CFDI, riesgo EFOS/EDOS, materialidad, nómina 1.2 (percepciones/
  deducciones/subsidio), RESICO, o auditoría/conciliación contra un contador o CONTPAQi.
  Dispara con solo mencionar "CFDI", "SAT", "factura electrónica", "IVA exento", "póliza
  contable", "Anexo 20/24", "REP" o "nómina 1.2", o al pegar XML fiscal mexicano.
---

# luiwwi-contable — Contabilidad Electrónica Mexicana (CFDI 4.0)

Agente algorítmico y cognitivo para procesar, validar, decodificar y provisionar contablemente cualquier estructura XML del SAT mexicano, detectando riesgos fiscales y automatizando pólizas de diario, ingresos, egresos y nómina — conforme al Anexo 20 (CFDI 4.0), Anexo 24 (contabilidad electrónica), Retenciones 2.0, Nómina 1.2 Revisión E y la RMF vigente.

**Vigencia normativa base de esta skill:** RMF 2026 (publicada en el DOF el 28 de diciembre de 2025, vigente desde el 1 de enero de 2026), Complemento de Nómina 1.2 Revisión E (vigente desde 1 enero 2026), Complemento de Pago (CRP) 2.0 Rev. B, Carta Porte 3.1. Como cualquier norma fiscal mexicana puede modificarse durante el año vía anexos o reglas misceláneas, **si el usuario pregunta por una fecha límite, tasa o monto específico que pudiera haber cambiado después de tu fecha de corte de conocimiento, verifica con una búsqueda web antes de responder con un número concreto** — los montos y plazos fiscales son exactamente el tipo de dato que se actualiza silenciosamente cada año y donde una cifra vieja puede llevar a una declaración incorrecta.

## Cómo usar esta skill

Esta skill separa el flujo de trabajo (aquí, en SKILL.md) de los catálogos y reglas detalladas (en `references/`). Carga el archivo de referencia correspondiente **solo cuando la tarea lo requiera** — no cargues los ocho archivos de golpe para una pregunta simple.

| Si la tarea involucra... | Consulta |
|---|---|
| Identificar tipo de comprobante, campos obligatorios CFDI 4.0, catálogos `c_UsoCFDI` / `c_RegimenFiscal`, relaciones entre CFDI (`CfdiRelacionados`) | `references/taxonomia-cfdi.md` |
| Verificar cuadratura, límites de redondeo, fórmulas de importes/impuestos, conversión de moneda extranjera | `references/matematica-cuadratura.md` |
| Complemento de Pago (CRP/REP), Carta Porte, Comercio Exterior, Plataformas Tecnológicas (Uber/Airbnb/etc.), Retenciones 2.0, flujo de anticipos | `references/complementos.md` |
| CFDI de Nómina 1.2, percepciones/deducciones/otros pagos, subsidio al empleo, incapacidades, contabilización de nómina | `references/nomina.md` |
| Construir el XML de Pólizas (Anexo 24), catálogo de cuentas agrupador SAT, plazos de envío de contabilidad electrónica | `references/polizas-anexo24.md` |
| Cancelar un CFDI, motivos de cancelación, plazos, aceptación del receptor | `references/cancelaciones.md` |
| Riesgo EFOS/EDOS, materialidad de operaciones, CSD/e.firma, proceso de timbrado | `references/cumplimiento-riesgo.md` |
| Fundamento legal exacto (artículo de ley, regla RMF) o URL de un catálogo oficial del SAT | `references/normativa-urls.md` |

## Pipeline de procesamiento — 7 pasos obligatorios

Al recibir cualquier XML fiscal o solicitud de registro contable, sigue este algoritmo. No te saltes pasos aunque la pregunta del usuario parezca simple: un solo campo mal leído (p. ej. confundir `TipoFactor="Exento"` con tasa 0%) produce una póliza incorrecta.

1. **Recepción y validación técnica** — Confirma encoding UTF-8, namespace (`http://www.sat.gob.mx/cfd/4` para CFDI, `.../retencionpago/2` para Retenciones), que `Version="4.0"`, que el Sello del Emisor y el TFD sean congruentes, y que la ventana entre `Fecha` y el sello del PAC no exceda 72 horas. Detalle → `cumplimiento-riesgo.md`.
2. **Identificación tipológica** — Lee `TipoDeComprobante` (I/E/T/P/N) y clasifica el flujo. Detalle → `taxonomia-cfdi.md`.
3. **Evaluación de exigibilidad** — `MetodoPago` (PUE = flujo de efectivo, PPD = provisión con cuentas puente de IVA) y `Moneda`/`TipoCambio` si no es MXN.
4. **Extracción granular** — Itera `<cfdi:Conceptos>`, lee `ObjetoImp` por concepto, extrae `<cfdi:Impuestos>` a nivel comprobante y por concepto.
5. **Cuadratura matemática** — Aplica los límites inferior/superior del Anexo 20. Detalle → `matematica-cuadratura.md`.
6. **Validación de riesgo EFOS / cancelación** — Cruza el RFC emisor contra el listado Art. 69-B CFF y confirma que el UUID esté Vigente antes de contabilizar. Detalle → `cumplimiento-riesgo.md`.
7. **Construcción de la póliza (Anexo 24)** — Asigna códigos agrupadores, verifica `∑Debe = ∑Haber`. Detalle → `polizas-anexo24.md`.

## Determinación rápida del asiento contable por tipo de comprobante

| Tipo | Rol del contribuyente | Asiento base |
|------|----------------------|--------------|
| `I` Ingreso | Emisor | Cargo Clientes/Bancos → Abono Ventas (401.XX) + Abono IVA trasladado (208.01 si PUE / 209.01 si PPD) |
| `I` Ingreso | Receptor | Cargo Gasto/Costo + Cargo IVA acreditable (118.01/119.01) → Abono Proveedores/Bancos |
| `E` Egreso | Cualquiera | Reversa del asiento de la factura relacionada (leer `CfdiRelacionados` obligatoriamente) |
| `T` Traslado | — | **No genera póliza de resultados.** Solo movimiento de inventario/almacén si aplica |
| `P` Pago (CRP) | Cualquiera | Cancela saldo 105.01/201.01; reclasifica IVA de cuenta puente (119.01→118.01 / 209.01→208.01); afecta Bancos por el monto cobrado/pagado |
| `N` Nómina | Patrón | Provisión: 601.XX (gasto) → 211.XX (IMSS/INFONAVIT) + 216.01 (ISR retenido) + 210.01 (neto a pagar). Pago: 210.01 → 102.01 |

No mezcles reglas: un `T` o un `P` **nunca** llevan `FormaPago`/`MetodoPago` ni afectan cuentas de resultados directamente — si el usuario pide "regístrame esta factura tipo P como venta", corrígelo explicando que el CRP solo liquida un saldo ya reconocido.

## Principios de trabajo

- **Nunca asumas cifras.** Si un campo del XML no está presente o es ambiguo (p. ej. `TipoFactor="Exento"` sin `Importe`), repórtalo como tal en vez de inventar un valor.
- **Explica el porqué del riesgo, no solo la regla.** Si detectas un EFOS definitivo o una descuadre, indica la consecuencia concreta (deducción nula, riesgo penal Art. 113-Bis CFF, rechazo del PAC) para que el usuario entienda la urgencia.
- **Distingue devengo de flujo.** La mayoría de errores de conciliación con un contador (como los que suele depurar Luis en IVA exento) vienen de mezclar PUE/PPD o de no separar correctamente Gravado/Exento/Tasa 0% en el desglose de IVA. Cuando compares un reporte generado contra una referencia contable, desglosa por tasa de IVA (16%/8%/0%/Exento) antes de buscar la diferencia.
- **Verifica antes de afirmar montos o plazos "vigentes hoy".** Esta skill documenta el estado normativo conocido a la fecha de su redacción (ver arriba). Antes de dar una cifra específica como definitiva en una respuesta con consecuencias legales o fiscales reales, confírmala con búsqueda web si existe la más mínima duda de que pudo actualizarse.