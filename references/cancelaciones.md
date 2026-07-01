# Cancelación de CFDI — Reglas 2.7.1.34 y 2.7.1.35 (RMF 2026)

> La RMF 2026 (publicada en el DOF el 28 de diciembre de 2025, vigente desde el 1 de enero de 2026) endureció de forma significativa el proceso de cancelación, especialmente para CFDI con Complemento de Pago e hidrocarburos. Si el usuario pregunta por cancelación con base en reglas de años anteriores ("antes se podía cancelar directo hasta $1,000"), acláralo: ese supuesto ya no aplica igual para los CFDI con Complemento de Pago desde 2026.

## 1. Proceso general (regla 2.7.1.34)

1. El emisor solicita la cancelación a través del Portal del SAT o de su PAC.
2. El CFDI pasa a estatus **"En proceso de cancelación"**.
3. El SAT notifica al receptor por Buzón Tributario.
4. El receptor tiene **3 días hábiles** para aceptar o rechazar.
5. Si no responde: **silencio positivo** → estatus "Cancelado por plazo vencido".
6. Si acepta: "Cancelado".
7. Si rechaza: "Vigente" (se requiere acuerdo entre las partes, o corregir vía nota de crédito/complemento de ajuste).

## 2. Cancelación sin aceptación del receptor (regla 2.7.1.35)

Cancelaciones directas (sin intervención del receptor), entre otros supuestos:

| Supuesto | Condición 2026 |
|----------|-----------------|
| Monto total ≤ $1,000 MXN | **Excluye expresamente** a los CFDI con Complemento para Recepción de Pagos (REP), sin importar el monto |
| Cancelación dentro de 72 horas de la emisión | Aplica a CFDI de ingreso/egreso en general (verifica si el caso concreto tiene una excepción sectorial) |
| CFDI de nómina | Sin importar el monto — el patrón cancela directo, sin requerir aceptación del trabajador |
| CFDI emitidos a residentes en el extranjero o a público en general (XAXX/XEXX) | En los supuestos que fije la regla vigente |

> **Cambio central de la RMF 2026:** los CFDI con Complemento de Pago (REP) quedaron **excluidos** de la facilidad de cancelación sin aceptación del receptor, independientemente del monto. Antes, un REP de hasta $1,000 MXN sí se podía cancelar directo; desde el 1 de enero de 2026 ya no. Todo REP se cancela por la vía de "aceptación del receptor" (aunque sí opera el silencio positivo a los 3 días hábiles).
>
> **Ventana operativa de facto para el REP:** en la práctica, la única cancelación verdaderamente ágil de un CRP es **el mismo día de su emisión**. Fuera de esa ventana, conviene resolver el error con un complemento de ajuste o una nota de crédito en vez de intentar la cancelación.
>
> **Excepción hidrocarburos y petrolíferos:** los CFDI de ingreso y egreso con el "Complemento Concepto para la facturación de Hidrocarburos y Petrolíferos" (sujeto a que el SAT lo publique y transcurra el plazo de 30 días naturales para su uso obligatorio) requieren **aceptación expresa** del receptor, sin posibilidad de silencio positivo. Lo mismo aplica a los CFDI tipo `I` con Complemento Carta Porte cuando las mercancías transportadas correspondan a claves de gasolina o diésel.

## 3. Motivos de cancelación

| Motivo | Descripción | Requisito adicional |
|--------|-------------|----------------------|
| `01` | Comprobante emitido con errores con relación | Timbrar el CFDI corrector **antes** de cancelar. El nuevo CFDI debe incluir `CfdiRelacionados` con `TipoRelacion = "04"` referenciando el UUID del cancelado. La cancelación exige el `FolioSustitucion` (UUID del nuevo CFDI). |
| `02` | Comprobante emitido con errores sin relación | No se emite CFDI sustituto. Solo se cancela y se emite uno nuevo independiente. |
| `03` | No se llevó a cabo la operación | La operación comercial nunca se concretó. Usar este motivo cuando sí hubo operación puede detonar que el SAT exija el ISR/IVA del CFDI original más recargos y multas si se detecta en auditoría. |
| `04` | Operación nominativa relacionada en factura global | El cliente solicita su factura individual que ya estaba incluida en un CFDI global. |

## 4. Plazos máximos para cancelar

- **CFDI de ingreso:** a más tardar en el mes en que se presenta la declaración anual del ISR del ejercicio en que se emitió (Art. 29-A CFF).
  - Personas Morales: hasta el último día del mes de presentación de la declaración anual.
  - Personas Físicas: hasta el cierre de la declaración anual.
  - **Verifica siempre el mes exacto vigente para el ejercicio en cuestión** antes de dar una fecha límite concreta — es un dato que cambia de referencia cada año fiscal y donde una fecha vieja puede hacer que el usuario pierda la ventana real.
- **CFDI con Complemento de Pago:** ventana operativa reducida al mismo día de emisión para cancelación ágil (ver sección 2). Después, usar complemento de ajuste o nota de crédito.
- Cancelar fuera de plazo genera inconsistencias en declaraciones y puede derivar en requerimientos y multas — reportadas en distintas fuentes en un rango del **5% al 10% del monto del CFDI** conforme al Art. 81, fracción XLVI CFF, además de ajustes contables obligatorios. Confirma el porcentaje exacto vigente si el usuario necesita el dato para una decisión con consecuencias legales reales.

## 5. Cómo aplicar esto en la práctica al construir/depurar una póliza

- Si el CFDI que estás procesando está **"En proceso de cancelación"**, no lo contabilices como cancelado ni como vigente definitivo — repórtalo como "en revisión" y espera la resolución (aceptación, rechazo o silencio positivo).
- Si detectas que un CFDI fue cancelado con Motivo `01` pero no encuentras el UUID sustituto relacionado (`TipoRelacion = "04"`), márcalo como inconsistencia: la sustitución es obligatoria en ese motivo.
- Si el usuario pide "cancelar" un CRP fuera del mismo día de su emisión pensando que aplicará la vieja regla de silencio automático para montos bajos, corrígelo explícitamente: desde 2026 esa facilidad no cubre a los REP.