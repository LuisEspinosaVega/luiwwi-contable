# Taxonomía del CFDI 4.0 — Reglas de Sintaxis (Anexo 20)

## 1. Campos nuevos obligatorios en CFDI 4.0 (vs. 3.3)

Vigencia exclusiva desde el 1 de abril de 2023 (la versión 3.3 ya no tiene validez fiscal).

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| `Nombre` del Receptor | Sí | Razón social exacta según Constancia de Situación Fiscal (CSF). El SAT valida contra padrón en tiempo real al timbrar. |
| `DomicilioFiscalReceptor` | Sí | Código postal de 5 dígitos del domicilio fiscal del receptor. Validado contra padrón SAT. |
| `RegimenFiscalReceptor` | Sí | Clave del régimen vigente del receptor. Incompatible entre régimen y `UsoCFDI` → rechazo del PAC. |
| `Exportacion` | Sí | Siempre presente: `01` No aplica, `02` Definitiva, `03` Temporal, `04` No objeto. |

> **Regla de oro:** los 4 datos del receptor (RFC, Nombre, Código Postal, Régimen Fiscal) se validan simultáneamente contra el padrón del SAT en el momento del timbrado. Un solo dato incorrecto provoca rechazo.

## 2. Tipos de comprobante

### `"I"` — Ingreso
Ventas, honorarios, arrendamientos, donativos. También el CFDI de anticipo (primer paso del flujo de anticipos, ver `complementos.md`).
- `MetodoPago = PUE` → flujo directo a Bancos (`102.01`).
- `MetodoPago = PPD` → provisión con cuentas puente de IVA (`209.01`/`119.01`).
- Compatible con Comercio Exterior 1.1, Carta Porte 3.1 (cuando el ingreso ampara flete), Nómina 1.2, Plataformas Tecnológicas.

### `"E"` — Egreso (Nota de Crédito / Débito / Anticipo)
Devoluciones, descuentos, bonificaciones o aplicación de anticipos.
- **Obligatorio:** nodo `<cfdi:CfdiRelacionados>` con el UUID del CFDI original y el `TipoRelacion` correspondiente.
- Contablemente disminuye base de ingresos o cuentas por cobrar.
- `SubTotal` puede ser menor al original (descuento parcial) o igual (devolución total).
- No puede llevar `FormaPago = 99` si es nota de crédito por anticipo; usar `FormaPago = 30` (Aplicación de anticipo).

### `"T"` — Traslado
Ampara transporte de mercancías.
- `SubTotal = 0` y `Total = 0`.
- No existen `FormaPago`, `MetodoPago`, ni `<cfdi:Impuestos>` a nivel raíz.
- Debe incluir Complemento Carta Porte 3.1 cuando el traslado involucre bienes en tránsito dentro del territorio nacional.
- **No genera póliza contable de resultados** — solo movimiento de inventario/almacén si aplica.

### `"P"` — Pago (CRP — Complemento para Recepción de Pagos 2.0 Rev. B)
Liquida facturas PPD. En el CFDI base:
- `SubTotal = 0`, `Total = 0`.
- No existe `MetodoPago` ni `FormaPago` en el nodo raíz.
- El detalle del complemento `<pago20:Pagos>` está en `complementos.md`.

### `"N"` — Nómina
Ver `nomina.md` para el detalle completo.
- `Moneda` obligatoriamente `MXN`.
- No existe `FormaPago`, `CondicionesDePago`, ni nodo global `<cfdi:Impuestos>`.
- `ObjetoImp = "01"` en todos los conceptos. `UsoCFDI = CN01`.

## 3. Atributos estructurales críticos

| Atributo | Regla | Excepción / Nota |
|----------|-------|------------------|
| `Version` | Siempre `"4.0"` | — |
| `Serie` | Alfanumérico, máx. 25 caracteres | Opcional |
| `Folio` | Alfanumérico, máx. 40 caracteres | Opcional |
| `Fecha` | Formato `AAAA-MM-DDTHH:MM:SS` hora local | Diferencia máx. 72 h con sello TFD |
| `FormaPago` | Clave `c_FormaPago`; `99` si PPD | No existe en CFDI tipo T, P, N |
| `SubTotal` | Suma de importes de conceptos antes de descuentos | Siempre positivo |
| `Descuento` | Solo si existe en algún concepto o a nivel global | Siempre positivo |
| `Moneda` | Clave `c_Moneda` | `MXN` en nómina; `XXX` en CFDI sin monto |
| `TipoCambio` | FIX Banxico del día hábil anterior | Solo si `Moneda ≠ MXN` y `≠ XXX` |
| `Total` | `SubTotal – Descuento + TrasladosTotales – RetencionesTotales` | Siempre positivo |
| `TipoDeComprobante` | I / E / T / P / N | — |
| `Exportacion` | `01`/`02`/`03`/`04` | Obligatorio en v4.0 |
| `MetodoPago` | `PUE` o `PPD` | No existe en tipo T, P, N |
| `LugarExpedicion` | CP de 5 dígitos del domicilio fiscal del emisor | Obligatorio siempre |
| `Confirmacion` | Clave otorgada por el PAC | Solo si monto excede límite parametrizado |
| `UsoCFDI` | Clave `c_UsoCFDI` compatible con `RegimenFiscalReceptor` | Validación en tiempo real |

## 4. Catálogo `c_UsoCFDI` — claves frecuentes

| Clave | Descripción | Regímenes compatibles |
|-------|-------------|------------------------|
| `G01` | Adquisición de mercancías | PM, PF actividad empresarial |
| `G02` | Devoluciones, descuentos o bonificaciones | PM, PF |
| `G03` | Gastos en general | Casi todos |
| `I01` | Construcciones | PM, PF |
| `I02` | Mobiliario y equipo de oficina | PM, PF |
| `I04` | Equipo de cómputo y accesorios | PM, PF |
| `I08` | Otra maquinaria y equipo | PM, PF |
| `CN01` | Nómina | Solo 605 (Sueldos y Salarios) |
| `CP01` | Pagos | Solo cuando el receptor no puede definir el uso |
| `D01` | Honorarios médicos, dentales y hospitalarios | PF con deducciones personales |
| `D10` | Pagos por servicios educativos (colegiaturas) | PF |
| `S01` | Sin efectos fiscales | Público en general (XAXX/XEXX) |
| `P01` | Por definir | Transitorio; el receptor debe actualizarlo |

## 5. Catálogo `c_RegimenFiscal` — claves principales

| Clave | Descripción |
|-------|-------------|
| `601` | General de Ley Personas Morales |
| `603` | Personas Morales con Fines no Lucrativos |
| `605` | Sueldos y Salarios e Ingresos Asimilados a Salarios |
| `606` | Arrendamiento |
| `608` | Demás ingresos (PF) |
| `610` | Residentes en el Extranjero sin EP en México |
| `611` | Ingresos por Dividendos (socios y accionistas) |
| `612` | Personas Físicas con Actividades Empresariales y Profesionales |
| `616` | Sin obligaciones fiscales |
| `620` | Sociedades Cooperativas de Producción |
| `621` | Incorporación Fiscal (vigente para contratos anteriores) |
| `622` | Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras |
| `625` | Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas |
| `626` | Régimen Simplificado de Confianza (RESICO) |

> El Anexo 20 vigente ha ido incorporando claves adicionales de régimen para el sector primario bajo RESICO. Si el usuario menciona un régimen que no aparece en esta tabla, verifica el catálogo `c_RegimenFiscal` publicado en el portal del SAT (ver `normativa-urls.md`) antes de asumir que no existe.

## 6. Relaciones entre comprobantes — `<cfdi:CfdiRelacionados>`

Desde CFDI 4.0 se pueden relacionar **múltiples UUID** en el mismo nodo, incluso con distintos `TipoRelacion` en nodos separados.

| Clave | Descripción | Cuándo usar |
|-------|-------------|-------------|
| `01` | Nota de crédito de los documentos relacionados | CFDI `E` que reduce base del CFDI `I` original |
| `02` | Nota de débito de los documentos relacionados | Cargo adicional sobre CFDI `I` anterior |
| `03` | Devolución de mercancía sobre facturas o traslados previos | Devolución física de bienes |
| `04` | Sustitución de los CFDI previos | CFDI corrector tras cancelación Motivo 01 |
| `05` | Traslados de mercancías facturados previamente | Factura previa + traslado posterior |
| `06` | Factura generada por los traslados previos | Traslado previo → ahora se factura |
| `07` | CFDI por aplicación de anticipo | Flujo de anticipos |
| `08` | Factura generada por pagos en parcialidades | Referencia de pago parcial documentado |
| `09` | Factura generada por pagos diferidos | — |
| `10` | Factura de retenciones relacionadas | Referencia a retención previa |

## 7. Catálogos técnicos adicionales del Anexo 20

| Catálogo | Descripción |
|----------|-------------|
| `c_TipoDeComprobante` | I, E, T, P, N |
| `c_Moneda` | MXN, USD, EUR, XXX y demás ISO 4217 |
| `c_FormaPago` | 01 Efectivo, 02 Cheque, 03 Transferencia, 04 Tarjeta de crédito, 05 Monedero electrónico, 06 Dinero electrónico, 08 Vales, 12 Dación en pago, 13 Pago por subrogación, 14 Pago por consignación, 15 Condonación, 17 Compensación, 23 Novación, 24 Confusión, 25 Remisión de deuda, 26 Prescripción, 27 A satisfacción del acreedor, 28 Tarjeta de débito, 29 Tarjeta de servicios, 30 Aplicación de anticipos, 31 Intermediario pagos, 99 Por definir |
| `c_MetodoPago` | PUE (Pago en una sola exhibición), PPD (Pago en parcialidades o diferido) |
| `c_ObjetoImp` | 01 No objeto, 02 Sí objeto (obliga desglose), 03 Sí objeto y no obligado al desglose, 04 No objeto y sí desglosa (facilidad), 05/06 zonas PODEBI/POINBI |
| `c_ClaveProdServ` | Catálogo de 8 dígitos, actualizado periódicamente por el SAT |
| `c_ClaveUnidad` | Unidades de medida (H87 pieza, KGM kg, MTR metro, LTR litro, etc.) |
| `c_Pais` | Catálogo ISO de países, con campo "Agrupación" para validar Unión Europea |
| `c_CodigoPostal` | Catálogo completo del INEGI — validado en tiempo real |

Si necesitas la clave exacta de un producto/servicio (`c_ClaveProdServ`) o unidad de medida que no reconoces, no la inventes: dile al usuario que la busque en el buscador de claves del SAT o realiza una búsqueda web del catálogo oficial (ver `normativa-urls.md`).