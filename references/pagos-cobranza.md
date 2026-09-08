# Pagos, REP 2.0 y cobranza

## Regla documental

En PPD, primero existe el CFDI por el total y después un CFDI de tipo `P` por cada pago. La RMF permite un REP mensual por receptor para pagos del mismo mes y exige emitirlo a más tardar el quinto día natural del mes siguiente, bajo las condiciones de la regla vigente.

En el CFDI `P`:

- la raíz tiene `Total=0`;
- no lleva `MetodoPago` ni `FormaPago` en la raíz;
- el complemento Pagos 2.0 contiene uno o más `Pago`;
- cada pago puede relacionar uno o más `DoctoRelacionado`.

## Campos esenciales

Por pago: fecha, forma, moneda, tipo de cambio cuando proceda y monto. Por documento relacionado: UUID, moneda, equivalencia cuando proceda, número de parcialidad, saldo anterior, importe pagado, saldo insoluto y objeto de impuesto.

Los impuestos del documento relacionado usan nodos `ImpuestosDR`; los impuestos a nivel pago usan `ImpuestosP`, con atributos como `BaseP` en los traslados/retenciones que correspondan. No usar el nombre incorrecto `BasePo`.

En `Totales`, `MontoTotalPagos` es requerido. Los totales de impuestos son condicionales según la composición del complemento; no afirmar que todos son siempre obligatorios.

## Reconciliación

Construir tres estados separados:

1. `pago_declarado`: REP vigente aplicado al UUID.
2. `pago_bancario`: movimiento conciliado con evidencia y criterio.
3. `pago_inferido`: supuesto por PUE, marca manual u otro indicio.

No elevar el tercero a confirmado. Un REP es evidencia documental fuerte de la declaración, pero puede requerir estado SAT y banco para confirmación económica.

## Saldos

Ordenar parcialidades por fecha de pago, parcialidad y UUID del REP. Verificar:

- continuidad razonable de `NumParcialidad`;
- `ImpSaldoAnt - ImpPagado ≈ ImpSaldoInsoluto`;
- que no se aplique más de lo disponible sin explicación;
- moneda y equivalencia;
- estado vigente tanto del REP como del documento relacionado;
- efectos de notas de crédito y sustituciones.

No corregir saldos sobrescribiendo XML. Registrar discrepancia y construir un saldo calculado aparte del saldo declarado.

## Correcciones

No existe una receta universal de “cancelar y reemplazar el REP”. Determinar motivo, estado de aceptación, documento relacionado y regla vigente. Preservar el REP original, la solicitud de cancelación, el sustituto si existe y su relación.

## Cuentas por cobrar/pagar

Para PPD, el saldo documental puede basarse en REP vigentes. Para PUE sin banco, mostrar una categoría separada: “cobro declarado/inferido, no conciliado”. La antigüedad debe indicar si usa fecha de emisión, vencimiento capturado o fecha pactada; el CFDI no siempre contiene vencimiento comercial.
