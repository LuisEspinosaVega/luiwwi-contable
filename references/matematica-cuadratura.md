# Algoritmos Matemáticos de Cuadratura y Redondeo (Anexo 20)

No se permiten valores negativos en ningún atributo monetario del CFDI. Las operaciones se realizan con hasta **6 decimales**; los totales globales se redondean a los decimales soportados por la moneda (2 en MXN).

## 1. Límites del importe de un concepto

```
NumDecimalesCantidad      = decimales de Cantidad (máx. 6)
NumDecimalesValorUnitario = decimales de ValorUnitario (máx. 6)

Límite Inferior =
  TRUNCAR[(Cantidad - 10^(-NumDecimalesCantidad) / 2)
          × (ValorUnitario - 10^(-NumDecimalesValorUnitario) / 2),
          NumDecimalesMoneda]

Límite Superior =
  REDONDEAR_ARRIBA[(Cantidad + 10^(-NumDecimalesCantidad) / 2 - 10^(-12))
                   × (ValorUnitario + 10^(-NumDecimalesValorUnitario) / 2 - 10^(-12)),
                   NumDecimalesMoneda]
```

> **Ejemplo SAT:** Importe matemático `924.224956` MXN (2 decimales) → Inferior = `924.22`, Superior = `924.23`.

Usa estos límites para decidir si un `Importe` reportado en el XML es válido: si cae fuera del rango [Límite Inferior, Límite Superior], el comprobante tiene un error de cálculo que el PAC debería haber rechazado — repórtalo como anomalía en vez de "corregirlo" silenciosamente.

## 2. Límites del importe de impuestos por concepto

Para cada `<cfdi:Traslado>` o `<cfdi:Retencion>` dentro de un concepto con `ObjetoImp = "02"`:

```
NumDecimalesBase = decimales de la Base del impuesto

Límite Inferior =
  TRUNCAR[(Base - 10^(-NumDecimalesBase) / 2) × TasaOCuota, NumDecimalesMoneda]

Límite Superior =
  REDONDEAR_ARRIBA[(Base + 10^(-NumDecimalesBase) / 2 - 10^(-12)) × TasaOCuota,
                   NumDecimalesMoneda]
```

- Si `TipoFactor = "Exento"`: no deben existir los atributos `TasaOCuota` ni `Importe`. Solo se registra la `Base`. Un CFDI con `TipoFactor="Exento"` que además trae `TasaOCuota="0.000000"` no es lo mismo que uno con `TipoFactor="Tasa"` y `TasaOCuota="0.000000"` (tasa 0%) — son dos tratamientos fiscales distintos y deben ir a cuentas contables separadas (ver `polizas-anexo24.md`, grupo 401).
- La `TasaOCuota` del IVA tiene hasta **6 decimales** de precisión (ej. `0.160000`, `0.080000`, `0.000000`).

## 3. Cuadratura final del comprobante

```
Total = SubTotal − Descuento + TotalImpuestosTrasladados − TotalImpuestosRetenidos
```

- `TotalImpuestosTrasladados` = suma de todos los importes de traslados agrupados a nivel comprobante.
- `TotalImpuestosRetenidos` = suma de todos los importes de retenciones agrupados a nivel comprobante.
- Los traslados y retenciones globales se agrupan por `Impuesto` + `TipoFactor` + `TasaOCuota`; no se repiten.

## 4. Moneda extranjera — conversión a MXN para pólizas

```
ImporteMXN = ImporteMonedaExtranjera × TipoCambio (FIX Banxico día hábil anterior)
```

- El `TipoCambio` se expresa con máximo 6 decimales.
- La póliza Anexo 24 puede registrarse en moneda extranjera si la cuenta contable está parametrizada; el nodo `<PLZ:CompNal>` acepta el campo `Moneda`.
- Si la operación supera los límites máximos parametrizados por el PAC, se exige el atributo `Confirmacion` otorgado por el PAC antes del timbrado.
- Si el usuario no te da el tipo de cambio FIX del día correspondiente, no lo inventes: pídelo o indícale que lo consulte en Banxico (búsqueda web) para esa fecha específica.

## 5. Algoritmo CRP — cuadratura del Complemento de Pago (Rev. B)

**Caso 1: `MonedaDR = MonedaP`**

```
∑ ImpPagado[i] ≤ Monto        (sin márgenes de variación)
```

**Caso 2: `MonedaDR ≠ MonedaP`**

```
Para cada DoctoRelacionado[i]:
  LI[i] = Límite inferior de (ImpPagado[i] / EquivalenciaDR[i])
  LS[i] = Límite superior de (ImpPagado[i] / EquivalenciaDR[i])

Resultado = TRUNCAR[∑(ImpPagado[i] / EquivalenciaDR[i]), decimales MonedaP]
∑ LI[i] ≤ Monto  y  Resultado ≤ ∑ LS[i]
```

## Depurando descuadres reales (IVA exento vs. gravado)

Cuando el objetivo sea conciliar un reporte generado contra la cifra de un contador (caso frecuente: diferencias en "IVA exento"), sigue este orden de diagnóstico antes de tocar el código:

1. **Separa por `TipoFactor`, no solo por tasa.** Un concepto puede ser `Exento` (sin `TasaOCuota`) o `Tasa` con `TasaOCuota="0.000000"` (tasa 0%). Si el reporte suma ambos en el mismo bucket "exento", ahí está la primera fuente de diferencia.
2. **Verifica `ObjetoImp` por concepto.** Un concepto con `ObjetoImp="01"` (no objeto) no debería aparecer en ningún desglose de IVA, ni siquiera como exento — simplemente no genera impuesto.
3. **Revisa si el CFDI tiene impuestos a nivel concepto y a nivel comprobante simultáneamente** y que el reporte no esté sumando ambos niveles (doble conteo clásico).
4. **Confirma que las notas de crédito (`E`) relacionadas se están restando del acumulado**, y no solo las facturas de ingreso.
5. Solo después de descartar estos cuatro puntos, revisa redondeos con las fórmulas de arriba.