# Analítica financiera para freelancers y PyME

## Dimensiones mínimas

Todo indicador debe fijar:

- RFC/tenant y rol;
- periodo por emisión o por pago;
- estado SAT y fecha de corte;
- moneda y política de conversión;
- tratamiento de egresos, sustituciones y REP;
- nivel de certeza.

## Métricas de primera versión

| Métrica | Base sugerida | Advertencia |
|---|---|---|
| Ingresos facturados vigentes | CFDI `I` emitidos vigentes | No equivale a ingreso cobrado ni fiscal definitivo |
| Notas/ajustes emitidos | CFDI `E` emitidos y sus relaciones | Una nota no prueba devolución bancaria |
| Gastos facturados recibidos | CFDI `I` recibidos vigentes | No todo gasto es deducible/acreditable |
| Cobros documentados | REP vigentes aplicados; PUE en columna separada | REP/PUE no sustituyen conciliación bancaria |
| Cuentas por cobrar documentales | Factura ajustada menos REP/ajustes aplicables | PUE sin banco requiere estado “inferido” |
| IVA trasladado facturado | Impuestos trasladados en CFDI emitidos | No es automáticamente IVA causado del periodo |
| IVA acreditable potencial | IVA en CFDI recibidos elegibles preliminarmente | Requiere pago, requisitos y destino, entre otros |
| Retenciones documentadas | Retenciones en CFDI/REP | Contrastar con régimen, periodo y enteros |
| Concentración de clientes | Participación por receptor en ingreso facturado | Un RFC genérico limita el análisis |
| Antigüedad de saldo | Fecha pactada o política explícita | El vencimiento comercial puede no estar en el CFDI |

## Fórmulas transparentes

Mantener por separado:

- `facturacion_bruta`: suma de `Total` de ingresos vigentes seleccionados;
- `ajustes_documentales`: egresos vinculados y clasificados;
- `facturacion_neta_documental`: bruta menos ajustes aplicables;
- `cobrado_por_rep`: importes pagados documentados en REP vigentes;
- `cobrado_confirmado`: sólo movimientos bancarios conciliados;
- `saldo_calculado`: importe ajustado menos aplicaciones documentales válidas.

No restar todos los CFDI `E` indiscriminadamente. Presentar egresos sin relación o con relación ambigua en una categoría de revisión.

## PUE sin banco

Mostrar al menos tres columnas: `documentado_PUE`, `documentado_REP` y `confirmado_banco`. Si el usuario no conectó bancos, el flujo de efectivo es estimado/incompleto. Evitar gráficas que nombren “cobrado” a la suma PUE sin aclaración.

## IVA e ISR

Un tablero puede mostrar impuestos **identificados en CFDI** y una **estimación preliminar**. Para estimar obligación se requieren reglas de causación/acreditamiento, régimen, fecha efectiva de cobro/pago, actos gravados/exentos, retenciones, saldos y otros datos. Etiquetar el resultado y enlazar cada ajuste a evidencia.

## Moneda y comparación

Ofrecer vista por moneda original. Si se consolida:

- identificar fuente y fecha de tipo de cambio;
- almacenar valor original y convertido;
- no mezclar la conversión documental de un REP con una conversión gerencial sin etiquetarla;
- recalcular periodos históricos sólo si la política lo indica.

## Calidad

Publicar cobertura: porcentaje de XML parseado, estado SAT actualizado, CFDI con complementos no soportados, relaciones faltantes y saldo conciliado. Un KPI sin cobertura puede parecer preciso y ser materialmente falso.
