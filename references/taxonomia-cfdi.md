# Taxonomía CFDI 4.0

## Tipos de comprobante

| Clave | Tipo | Lectura económica inicial |
|---|---|---|
| `I` | Ingreso | Operación facturada; no demuestra cobro |
| `E` | Egreso | Ajuste, descuento o devolución; su efecto depende de la relación y contexto |
| `T` | Traslado | Movimiento de bienes; normalmente `Total=0` |
| `N` | Nómina | Pago laboral con complemento Nómina |
| `P` | Pago | REP; `Total=0` y sin `MetodoPago`/`FormaPago` en la raíz |

No imponer `Total > 0` a todos los tipos. Un comprobante de pagos o traslado puede tener total cero conforme a su estándar.

## Roles y fechas

- Derivar “emitido” o “recibido” comparando el RFC del tenant con Emisor y Receptor; no confiar sólo en la carpeta de origen.
- `Fecha` es la expedición declarada. La fecha de timbrado está en Timbre Fiscal Digital. Ninguna equivale necesariamente a pago o descarga.
- `LugarExpedicion` es el código postal del lugar de expedición conforme al estándar, no una prueba automática del domicilio fiscal.
- Conservar zona horaria asumida y texto original; el CFDI no incluye un offset explícito en esos atributos.

## PUE y PPD

- `PUE` significa pago en una sola exhibición. La RMF permite usarlo si se estima pago total a más tardar el último día del mismo mes y se cumplen las correcciones previstas si la estimación falla.
- `PPD` significa pago en parcialidades o diferido. Se emite el comprobante por el total y posteriormente un CFDI `P` por cada pago, con la opción de consolidación prevista por la RMF.
- Tratar ambos como datos documentales. Sólo una conciliación independiente eleva el cobro a “Confirmado”.

`FormaPago` en un CFDI de ingreso describe la forma declarada bajo las reglas aplicables; no es una referencia bancaria. En `PPD` suele emplearse la clave por definir en el comprobante relacionado, mientras la forma efectiva se declara en el REP. Validar siempre catálogo y matriz vigentes.

## Relaciones

Guardar grupo de relación, tipo y todos los UUID relacionados. No asumir que toda relación modifica saldo. Para notas de crédito, sustituciones, devoluciones o aplicaciones de anticipos se necesita la semántica del tipo vigente y el contexto.

Cuando exista sustitución, conservar ambos documentos y la transición SAT. El nuevo UUID no borra el anterior.

## Conceptos e impuestos

Extraer, al menos:

- clave de producto/servicio, identificación, cantidad, unidad, descripción;
- valor unitario, importe y descuento con texto y decimal;
- objeto de impuesto;
- traslados y retenciones por concepto: base, impuesto, tipo factor, tasa/cuota e importe cuando proceda;
- impuestos globales y totales.

No tratar `Exento`, tasa cero y no objeto como sinónimos. Los códigos de `ObjetoImp` y sus condiciones evolucionan; cargarlos desde el catálogo/matriz oficial vigente, no desde una lista recordada.

## Emisión y casos económicos

Para preparar timbrado, además de XSD/catálogos validar RFC/nombre/domicilio/régimen/uso, datos del emisor, CSD, serie/folio, moneda, exportación, impuestos y complementos condicionados. Separar borrador, solicitud, respuesta PAC, UUID y estado SAT. Ante timeout consultar resultado antes de reintentar para evitar doble timbrado. La autorización para analizar no autoriza emitir.

Resolver con guía oficial y RMF del periodo estos casos antes de elegir tipo/relación:

- Anticipo frente a pago parcial: determinar si bien/servicio y precio están definidos; documentar aplicación y evitar duplicar ingresos/IVA.
- Factura global: operaciones con público en general, periodicidad y campos de información global; conciliar tickets y facturas nominativas para no duplicar ventas.
- Egresos: descuentos, bonificaciones y devoluciones con soporte económico; distinguir ajuste de contraprestación, devolución de dinero y sustitución documental.
- Pagos por cuenta de terceros, gastos reembolsables, viáticos, factoraje y cesión: identificar titular de operación, deuda y flujo; no convertir el depósito neto en base fiscal automáticamente.
- Moneda extranjera, exportación y residentes extranjeros: resolver RFC genérico, identificación, domicilio y complementos por supuesto.
- CFDI de retenciones e información de pagos: documento independiente con sus complementos (dividendos, intereses, extranjero u otros aplicables); no sustituirlo con REP ni duplicar ingreso por reportarlo.

## Catálogos versionados

Guardar clave y etiqueta versionada, pero usar la clave como dato normativo. `P01` fue una clave de UsoCFDI anterior y no debe proponerse en CFDI 4.0. Evitar listas estáticas de regímenes, usos, formas o productos en lógica de negocio: registrar versión, vigencia y fuente del catálogo.
