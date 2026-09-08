# Validación y matemática

## Capas independientes

1. **Transporte:** bytes íntegros, hash, tamaño y procedencia.
2. **XML:** bien formado, codificación aceptable, sin DTD/entidades externas.
3. **Esquema:** XSD, catálogos y matrices correspondientes a fecha y versión.
4. **Criptografía:** certificado, sello, cadena original y Timbre Fiscal Digital.
5. **Estado:** consulta SAT con fecha de corte.
6. **Economía:** relaciones, REP, notas, cancelaciones y banco.

Reportar cada resultado por separado. “XML válido” no significa “vigente”, y “vigente” no significa “pagado”.

## Representación numérica

- Parsear importes con decimal exacto desde el texto.
- Conservar texto original, escala y moneda.
- Redondear sólo donde lo ordene el estándar o al presentar; no redondear en cada suma intermedia por comodidad.
- Aplicar la cantidad de decimales permitida por moneda y atributo según catálogos/matriz vigentes.
- Documentar tolerancia; no usar una tolerancia universal para todo atributo.

## Cuadratura raíz

Como control aritmético inicial:

`Total ≈ SubTotal - Descuento + TotalImpuestosTrasladados - TotalImpuestosRetenidos`

La presencia y escala de cada término dependen del tipo y del esquema. Verificar además reglas de límites inferior/superior del Anexo 20; una igualdad a centavos no sustituye esas reglas.

## Cuadratura de conceptos

- Contrastar `Importe` contra `Cantidad × ValorUnitario` con los límites permitidos.
- Contrastar descuento de concepto y descuento global.
- Sumar bases e impuestos por combinación normativa, no sólo por tasa visible.
- Verificar que los impuestos de conceptos sustenten los totales globales cuando deban existir.
- Distinguir traslado, retención, exento y tasa cero.

## Moneda

No convertir automáticamente con FIX del día anterior. El significado, obligatoriedad y fuente del tipo de cambio dependen del atributo, documento y regla. En REP usar `MonedaP`, `TipoCambioP`, `MonedaDR` y `EquivalenciaDR` conforme a Pagos 2.0. Guardar importe original y resultado convertido, con fórmula explícita.

## Firma y timbre

La validación completa requiere reproducir la cadena original con el XSLT oficial aplicable, validar el sello con el certificado, revisar vigencia/identidad del certificado y validar el timbre. No implementar una “validación” comparando cadenas o regex.

## Resultado estructurado

Para cada control devolver:

- identificador y capa;
- `pass`, `fail`, `warning` o `not_run`;
- evidencia observada;
- regla/fuente y versión;
- severidad y efecto;
- acción recomendada.

No sumar advertencias heterogéneas en una calificación opaca. Los bloqueos deben ser configurables y auditables.
