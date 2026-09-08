# Contabilidad, operación y cierre

Estas son políticas de trabajo y controles de diseño. Para obligaciones fiscales consultar CFF 28 y 30, su Reglamento y RMF; para reconocimiento y presentación identificar el marco NIF, NIIF o regulatorio aplicable. No atribuir al SAT normas de información financiera ni reproducir textos NIF sin autorización.

## Registro y mayor

Una póliza incluye entidad, fecha económica/contable, periodo, concepto, cuentas vigentes, cargos/abonos, moneda funcional y original, tipo de cambio con fuente, contraparte, dimensiones pertinentes, evidencia y autor/aprobación. Balancear en moneda funcional; conservar auxiliares por moneda sin exigir artificialmente equilibrio de cada moneda original en una operación cambiaria.

Separar borrador, validada, contabilizada y revertida. Contabilizar de forma atómica e idempotente: reimportar una factura no duplica la póliza; una misma factura puede soportar varios eventos legítimos. Conciliar saldos iniciales con el cierre anterior. Corregir pólizas contabilizadas mediante ajustes enlazados y controlar reaperturas; no cambiar el histórico al actualizar una plantilla.

## Reconstrucción de operaciones

| Ciclo | Controles y decisiones |
|---|---|
| Ventas y CxC | Entrega/prestación, reconocimiento, anticipos, descuentos, devoluciones, intereses, incobrables y vencimientos; cobro separado del ingreso |
| Compras y CxP | Recepción, factura, gastos devengados sin factura, anticipos, financiamiento y devoluciones; pago separado de deducción |
| Tesorería | Saldos inicial/final, cargos, abonos, transferencias propias, comisiones, contracargos, pagos agrupados y depósitos netos de plataformas |
| Inventario y producción | Propiedad, almacén, unidad, cantidades, costos directos/indirectos, mermas, obsolescencia, tránsito, consignación y conteo físico; negativos requieren investigación |
| Activos | Monto original, costos capitalizables, puesta en uso, vida útil, valor residual, deterioro, arrendamientos, bajas y venta; libros fiscal y contable separados |
| Financiamiento y capital | Principal, intereses, comisiones, aportaciones, reembolsos, dividendos y actas; un depósito no es automáticamente ingreso |
| Nómina | Devengo, pasivos al trabajador/autoridades, pago y enteros; evitar contabilizar de nuevo el gasto al dispersar |

Aplicar coincidencias bancarias por importe, fecha, referencia, contraparte y moneda, con evidencia y tolerancia explícitas. Soportar muchos-a-muchos, efectivo y extinciones distintas del pago; no inventar un banco para cuadrar. Una diferencia no justifica una cuenta puente permanente sin seguimiento.

## Cierre y estados

1. Congelar el universo y corte; listar documentos faltantes y eventos posteriores relevantes.
2. Conciliar bancos y submayores con mayor: clientes, proveedores, inventarios, activos, nómina e impuestos.
3. Registrar devengamientos, provisiones sustentadas, depreciación, deterioro, diferencias cambiarias y reclasificaciones. Una provisión contable no acredita deducción fiscal.
4. Preparar conciliación contable-fiscal y revisar movimientos de patrimonio.
5. Validar saldos de apertura + movimientos = cierre, doble partida y consistencia entre estados. Preparar situación financiera, resultado integral, cambios en capital y flujos conforme al marco; enlazar notas, comparativos y políticas.
6. Identificar salvedades materiales y aprobar/cerrar según responsabilidades. Un balance cuadrado no demuestra integridad del universo.

En flujos de efectivo excluir operaciones no monetarias y evitar contar traspasos propios como entradas/salidas operativas. Separar rentabilidad, facturación y caja.

## Multimoneda y grupos

Separar moneda de transacción, funcional, presentación y conversión fiscal. Documentar tasas de reconocimiento, liquidación y cierre; no reutilizar `TipoCambioP` como tasa universal. Conciliar intercompañías bilateralmente, identificar diferencias y eliminar saldos/operaciones intragrupo para consolidación cuando aplique. La consolidación financiera no permite compensar impuestos entre RFC ni implica régimen de integración fiscal.
