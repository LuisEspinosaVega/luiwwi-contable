# Nómina CFDI 1.2 — Complemento Revisión E

> El SAT publicó el 2 de diciembre de 2025 la actualización del Complemento de Nómina 1.2 conocida como **Revisión E**, vigente desde el 1 de enero de 2026. Es una actualización de catálogos, matriz de errores y validaciones — no cambia la estructura del XML del complemento. Si trabajas contra un sistema de timbrado desactualizado (que no soporte Revisión E), muchos CFDI que antes timbraban sin problema serán rechazados a partir de 2026; vale la pena preguntarle al usuario si su PAC/CONTPAQi ya está actualizado antes de diagnosticar un rechazo como error de negocio.

## Validaciones obligatorias del comprobante base

| Campo | Regla |
|-------|-------|
| `Moneda` | Siempre `MXN` |
| `UsoCFDI` | Siempre `CN01` |
| `TipoDeComprobante` | Siempre `N` |
| `ObjetoImp` | Siempre `01` (no objeto de impuesto) |
| `ClaveProdServ` | Siempre `84111505` |
| `Descripcion` | Siempre "Pago de nómina" (literal) |
| `RegimenFiscalReceptor` | `605` (sueldos), `606` (arrendadores que perciben asimilados), `608` (asimilados), `611` (dividendos) |
| No debe existir | `FormaPago`, `CondicionesDePago`, `<cfdi:Impuestos>` a nivel raíz |

## Tipos de nómina

- `TipoNomina = "O"` — Ordinaria: periodos regulares (semanal, catorcenal, quincenal, mensual).
- `TipoNomina = "E"` — Extraordinaria: aguinaldo, PTU, indemnizaciones, liquidaciones, prima vacacional especial, retroactivos.
- No mezclar percepciones ordinarias y extraordinarias en el mismo CFDI cuando esto rompa validaciones; usar 2 CFDI separados.

## Cuadratura obligatoria del complemento

```
TotalSueldos + TotalSeparacionIndemnizacion + TotalJubilacionPensionRetiro
    = TotalGravado + TotalExento          [en nodo Percepciones]

Total del Comprobante = TotalPercepciones + TotalOtrosPagos − TotalDeducciones
```

## Cambios clave de la Revisión E (vigente desde el 1 de enero de 2026)

1. **Ningún concepto de percepción puede reportar `ImporteGravado` e `ImporteExento` ambos en cero.** Al menos uno debe tener un valor real mayor a cero. Un concepto en ceros dobles ahora es rechazo directo del PAC (antes timbraba sin problema).
2. **La percepción `038 Otros ingresos por salario` debe reportarse en su totalidad como gravada.** Ya no se permite asignar valor a `ImporteExento` bajo esta clave; si el sistema del usuario la usaba como "comodín" para exentos no catalogados, hay que reclasificar esos conceptos a la clave correcta.
3. **El subsidio causado máximo pasa de $475.00 a $628.00 MXN mensual.** La validación del atributo `SubsidioCausado` ahora depende también de `NumDiasPagados`: para periodos de hasta 31 días, el tope es $628.00; para periodos mayores se aplica un factor proporcional (verifica el factor vigente contra la matriz de errores publicada por el SAT, ya que fuentes secundarias reportan valores ligeramente distintos para el multiplicador — no repitas una cifra exacta sin confirmarla).
4. **Nuevas claves de percepciones:** `054` Días de descanso laborados, `055` Días de descanso obligatorio laborados.
5. **Nuevas claves de deducciones:** `108` Ajuste a días de descanso laborados gravados, `109` Ajuste a días de descanso laborados exentos, `110` Ajuste a días de descanso obligatorios laborados gravados, `111` Ajuste a días de descanso obligatorios laborados exentos.
6. **Matriz de errores actualizada:** se modifican los criterios de los errores `NOM75`, `NOM101` y `NOM108`; se agregan los nuevos códigos `NOM109` y `NOM110` para las validaciones de importes en cero y de nuevas claves.

Si el usuario reporta un rechazo con alguno de estos códigos de error (`NOM75`, `NOM101`, `NOM108`, `NOM109`, `NOM110`), la causa casi siempre es una de las 3 reglas nuevas de arriba (ceros dobles, clave 038 mal usada, o tope de subsidio excedido) — revisa esas primero antes de sospechar de un problema de conectividad con el PAC.

## Catálogo de percepciones — claves frecuentes

| Clave | Descripción | Tipo |
|-------|-------------|------|
| `001` | Sueldos, salarios, rayas y jornales | Gravado y/o Exento |
| `002` | Gratificación anual (aguinaldo) | G/E — exento hasta el tope de SMG vigente |
| `003` | Participación de utilidades (PTU) | G/E — exento hasta el tope de SMG vigente |
| `004` | Reembolso de gastos médicos, dentales y hospitalarios | Exento si cumple requisitos |
| `005` | Fondo de ahorro | Exento si cumple los requisitos LISR |
| `006` | Caja de ahorro | Exento |
| `007` | Cuotas sindicales pagadas por el patrón | Exento |
| `008` | Ayuda para renta | Exento |
| `009` | Ayuda para artículos escolares y útiles | Exento |
| `010` | Ayuda para anteojos | Exento |
| `011` | Ayuda para transporte | Exento |
| `012` | Ayuda para gastos de funeral | Exento |
| `013` | Tiempo extra | Exento hasta el límite legal (Art. 93 fr. I LISR) |
| `014` | Subsidios por incapacidad | Exento — activa nodo `Incapacidades` |
| `019` | Horas extra | Según cálculo Art. 93 fr. I LISR |
| `022` | Prima dominical | G/E |
| `023` | Prima vacacional | G/E — exento hasta el tope de SMG vigente |
| `025` | Alimentación | G/E — exento hasta el porcentaje de SMG vigente si es en especie |
| `038` | Otros ingresos por salario | **100% gravado** (Revisión E) |
| `039` | Jubilaciones, pensiones o haberes de retiro | G/E (cálculo especial) |
| `044` | Indemnizaciones | G/E (cálculo especial de ISR anualizado) |
| `045` | Reconocimiento de años de servicio | G/E |
| `046` | Tiempo extraordinario | G/E |
| `047` | Viáticos (comprobados) | Exento si cumplen requisitos Art. 93 fr. XVII LISR |
| `050` | Premio por puntualidad | Gravado |
| `051` | Prima de seguro de vida | Exento (póliza colectiva) |
| `052` | Gastos funerarios | Exento |
| `053` | Cuotas IMSS de empleados pagadas por el patrón | Exento |
| `054` | Días de descanso laborados | G/E (nueva Revisión E) |
| `055` | Días de descanso obligatorio laborados | G/E (nueva Revisión E) |

## Catálogo de deducciones — claves frecuentes

| Clave | Descripción |
|-------|-------------|
| `001` | Seguridad social (cuota obrera IMSS) |
| `002` | ISR retenido |
| `003` | Aportaciones a retiro, cesantía y vejez (AFORE — cuota obrera) |
| `004` | Impuesto local sobre sueldos y salarios (ISN obrero, si aplica) |
| `005` | Aportación al INFONAVIT (cuota obrera) |
| `006` | Descuento por incapacidad — activa nodo `Incapacidades` |
| `007` | Pensión alimenticia |
| `008` | Renta (descuento por préstamo de casa habitación) |
| `009` | Préstamos provenientes del fondo de ahorro |
| `010` | Pago por crédito de vivienda INFONAVIT o FOVISSSTE |
| `011` | Pago de abonos FONACOT |
| `071` | Ajuste del subsidio para el empleo (reintegro al patrón) |
| `081` | Ajuste de viáticos comprobados |
| `102`–`106` | Ajustes por pagos de jubilación / pensiones en múltiples exhibiciones |
| `108`–`111` | Ajustes a días de descanso laborados / obligatorios, gravados y exentos (nuevas Revisión E) |

## Catálogo de otros pagos — claves frecuentes

| Clave | Descripción |
|-------|-------------|
| `001` | Reintegro de ISR retenido en exceso que no se enteró al SAT (uso reservado para este supuesto desde la Revisión E — ya no es genérico para subsidio) |
| `002` | Subsidio para el empleo efectivamente entregado |
| `003` | Viáticos (entregados; la distinción comprobados/no comprobados se resuelve en Percepciones) |
| `004` | Aplicación de saldo a favor por compensación anual ISR |
| `005` | Reintegro de ISR retenido en exceso de ejercicio anterior |
| `006` | Alimentos (en especie) |
| `007` | Ajuste al subsidio para el empleo: diferencia entre subsidio causado mayor que el entregado |
| `008` | Ajuste al subsidio para el empleo: diferencia entre subsidio causado menor que el entregado |
| `999` | Pagos distintos a los listados que no deben considerarse ingreso por sueldos (incluye préstamos a empleados) |

> **Regla de viáticos (OtroPago 003):** se reportan en `OtrosPagos` en el momento de la entrega. Cuando el empleado los comprueba, se registran como percepción exenta (`047`) y el importe se deduce en `Deducciones` (`081`). Los no comprobados son percepción gravada.
>
> **Préstamos a empleados:** se reportan en `OtrosPagos` con clave `999`; no son ingresos acumulables para el trabajador. El descuento del pago del préstamo va en `Deducciones` con la clave correspondiente.

## Reglas especiales — casos críticos

**Incapacidades:**
- Nodo `<nomina12:Incapacidades>` obligatorio cuando existe `Percepcion 014` (subsidio IMSS) o `Deduccion 006` (descuento por días no laborados).
- Atributos: `DiasIncapacidad`, `TipoIncapacidad` (`01` Riesgo de trabajo, `02` Enfermedad general, `03` Maternidad), `ImporteMonetario`.
- Si se necesita reportar tanto la deducción como la percepción por incapacidad, se pueden emitir 2 CFDI de nómina o 2 complementos en el mismo período.

**Extrabajadores / Liquidaciones:**
- Percepciones `044` (Indemnizaciones) y `045` (Reconocimiento por años de servicio) requieren cálculo especial de ISR anualizado (Art. 95 y 96 LISR).
- Para pagos diferidos de jubilación o pensión: percepciones `039`/`051`/`052`/`053`. Ajustes: deducciones `102`–`106`.

**Subsidio al empleo — procedimiento:**
1. Calcular el subsidio causado según las tablas LISR vigentes (tope 2026: $628.00 mensual, con factor proporcional para periodos distintos a 31 días — confirma el factor exacto contra la publicación oficial si el cálculo es para producción).
2. Comparar con el ISR retenido calculado.
3. Si subsidio causado > ISR retenido → el patrón entrega la diferencia (`OtroPago 002`).
4. Si ISR retenido > subsidio causado → el patrón retiene la diferencia.
5. El ajuste de fin de período se registra con `OtroPago 007` u `008` según el caso.
6. El subsidio efectivo nunca puede generar retención negativa; si resulta negativo, se deja en cero.

**Cancelación de CFDI de Nómina:**
- El patrón puede cancelar CFDI de nómina **sin requerir aceptación del trabajador**, sin importar el monto.
- Procedimiento: emitir nuevo CFDI con los datos correctos; el CFDI anterior se cancela con Motivo `01` (sustitución) referenciando el UUID del corrector con `TipoRelacion = "04"`.

## Contabilización de nómina

**Póliza de provisión (al cierre del período):**

| Cuenta | Cargo | Abono |
|--------|-------|-------|
| `601.01` Sueldos y salarios | Total Percepciones bruto | — |
| `601.26` Cuotas IMSS patronal | Cuota patronal IMSS | — |
| `601.27` Aportaciones INFONAVIT patronal | Aportación patronal INFONAVIT | — |
| `601.28` PTU | Provisión PTU (estimada) | — |
| `216.01` ISR retenido sueldos | — | ISR retenido a empleados |
| `211.01` IMSS por pagar | — | Cuota obrera + patronal IMSS |
| `211.02` INFONAVIT por pagar | — | Aportación INFONAVIT total |
| `210.01` Sueldos por pagar | — | Neto a pagar a empleados |

**Póliza de pago (al dispersar nómina):**

| Cuenta | Cargo | Abono |
|--------|-------|-------|
| `210.01` Sueldos por pagar | Neto dispersado | — |
| `102.01` Bancos | — | Neto dispersado |

**Póliza de pago de IMSS/INFONAVIT (bimestral/mensual según el caso):**

| Cuenta | Cargo | Abono |
|--------|-------|-------|
| `211.01` IMSS por pagar | Total IMSS (obrera + patronal) | — |
| `211.02` INFONAVIT por pagar | Aportación total | — |
| `102.01` Bancos | — | Total IMSS + INFONAVIT |