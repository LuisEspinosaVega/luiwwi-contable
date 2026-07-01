# Automatización de Pólizas Contables — Estándar Anexo 24

## 1. Arquitectura del archivo XML de pólizas

**Namespace:** `http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo`

El archivo se llama `{RFC}_{AAAAMM}PL.xml` y se envía comprimido en `.zip`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PLZ:Polizas
  xmlns:PLZ="http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo"
  Version="1.3"
  RFC="EMP010101XY6"
  Mes="05"
  Anio="2026"
  TipoSolicitud="AF"
  NumOrden="ABC123456/2026"
  Sello="..."
  noCertificado="..."
  Certificado="...">

  <PLZ:Poliza
    NumUnIdenPol="D-0001"
    Fecha="2026-05-25"
    Concepto="Provisión de Factura de Compra">

    <PLZ:Transaccion
      NumCta="201.01"
      DesCta="Proveedores nacionales"
      Concepto="Pasivo por factura de proveedor"
      Debe="0.00"
      Haber="11600.00">
      <PLZ:CompNal
        UUID_CFDI="5FB2822E-396D-4725-8521-CDC4BDD20CCF"
        RFC="PROV990101XYZ"
        MontoTotal="11600.00"
        Moneda="MXN"/>
    </PLZ:Transaccion>

    <PLZ:Transaccion
      NumCta="501.01"
      DesCta="Costo de Venta"
      Concepto="Mercancía adquirida"
      Debe="10000.00"
      Haber="0.00"/>

    <PLZ:Transaccion
      NumCta="119.01"
      DesCta="IVA pendiente de pago"
      Concepto="IVA Trasladado 16% PPD"
      Debe="1600.00"
      Haber="0.00"/>

  </PLZ:Poliza>
</PLZ:Polizas>
```

**Para pólizas de flujo de efectivo**, reemplaza `<PLZ:CompNal>` por:
```xml
<PLZ:Transferencia
  CtaOri="012180015548785456"
  BancoOriNal="012"
  CtaDest="072840011199991234"
  BancoDestNal="072"
  Fecha="2026-05-25"
  Monto="11600.00"/>
```
O bien:
```xml
<PLZ:Cheque
  Num="001234"
  BanEmisNal="014"
  CtaOri="014180015548785456"
  Fecha="2026-05-25"
  Benef="Proveedor Nacional S.A. de C.V."
  RFC="PROV990101XYZ"
  Monto="11600.00"
  Moneda="MXN"/>
```

**Atributos del archivo `<PLZ:Polizas>`:**
- `TipoSolicitud`: `AF` = Acto de Fiscalización, `FC` = Fiscalización Compulsa, `DE` = Devolución, `CO` = Compensación.
- `NumOrden`: número de orden del acto de fiscalización emitido por el SAT (requerido solo si el SAT lo solicita).
- El archivo lleva **sello digital** de la contabilidad electrónica, generado con la e.firma (ver `cumplimiento-riesgo.md`, sección de sello digital de la contabilidad electrónica).

## 2. Cuándo se envían las pólizas — no confundir con el envío mensual

Las pólizas **no se envían mensualmente de forma proactiva**; solo cuando el SAT las requiere explícitamente mediante:
- Revisión electrónica (Art. 53-B CFF)
- Visita domiciliaria (Art. 42, fracción III CFF)
- Revisión de gabinete (Art. 42, fracción II CFF)

Lo que **sí se envía mensualmente** vía Buzón Tributario:

| Archivo | Quién | Plazo |
|---------|-------|-------|
| Catálogo de cuentas (primera vez o cuando se modifica) | PM y PF obligadas | Con la primera balanza o al mes de la modificación |
| Balanza de comprobación mensual | Personas Morales | Primeros días hábiles del 2º mes posterior (verifica el número exacto de días vigente, ya que la RMF lo ajusta ocasionalmente) |
| Balanza de comprobación mensual | Personas Físicas | Primeros días hábiles del 2º mes posterior (ídem, verificar plazo exacto vigente) |
| Balanza de cierre del ejercicio ("Balanza 13") | Personas Morales | Fecha límite en abril del año siguiente (confirmar día exacto vigente) |
| Balanza de cierre del ejercicio ("Balanza 13") | Personas Físicas | Fecha límite en mayo del año siguiente (confirmar día exacto vigente) |
| Empresas que cotizan en bolsa | PM | Primeros días hábiles del 2º mes posterior al trimestre |
| Sector primario (semestral) | PM y PF | Primeros días hábiles del 2º mes posterior al semestre |

> Los plazos exactos en días hábiles y las fechas límite de abril/mayo se fijan en la regla 2.8.1.6 de la RMF y pueden variar ligeramente entre resoluciones anuales. Si el usuario necesita el plazo exacto para cumplir una obligación real (no solo entender el concepto), verifícalo con búsqueda web contra la RMF del ejercicio en curso antes de darlo como definitivo.

**Nomenclatura de archivos XML:**
- Catálogo: `{RFC}_{AAAAMM}CT.xml`
- Balanza normal: `{RFC}_{AAAAMM}BN.xml`
- Balanza complementaria: `{RFC}_{AAAAMM}BC.xml`
- Pólizas: `{RFC}_{AAAAMM}PL.xml`
- Auxiliares de folios fiscales: `{RFC}_{AAAAMM}XF.xml`
- Auxiliares de cuentas: `{RFC}_{AAAAMM}XC.xml`

**Exenciones de contabilidad electrónica completa:**
- PF con ingresos del año anterior por debajo del tope vigente para "Mis Cuentas" (verificar el monto exacto vigente antes de aplicarlo, ya que el tope se ha movido entre ejercicios).
- Contribuyentes RESICO PF (obligaciones simplificadas, sin DIOT mensual ni contabilidad electrónica completa).
- PF asalariadas y quienes solo generan ingresos por plataformas digitales.

## 3. Catálogo de cuentas agrupador SAT — mapa de referencia

El catálogo de cuentas del contribuyente se mapea a los Códigos Agrupadores del SAT. El código agrupador se asocia a nivel de **subcuenta de primer nivel** (nivel 2). Trata los códigos de abajo como un punto de partida razonable — el catálogo real de cada contribuyente puede tener variantes; no fuerces una cuenta que no exista en el catálogo real que te compartan.

### Activo

| Código | Descripción |
|--------|-------------|
| `101.01` | Caja (efectivo en moneda nacional) |
| `101.02` | Caja (moneda extranjera) |
| `102.01` | Bancos nacionales |
| `102.02` | Bancos extranjeros |
| `103.01` | Inversiones temporales (hasta 3 meses) |
| `104.01` | Documentos y cuentas por cobrar a clientes nacionales |
| `104.02` | Documentos y cuentas por cobrar a clientes extranjeros |
| `105.01` | Clientes nacionales |
| `105.02` | Clientes extranjeros |
| `106.01` | Cuentas por cobrar a corto plazo (no clientes) |
| `107.01` | Deudores diversos nacionales |
| `108.01` | Deudores diversos extranjeros |
| `109.01` | Documentos por cobrar a corto plazo |
| `110.01` | Intereses por cobrar a corto plazo |
| `115.01` | Inventario de materias primas |
| `115.02` | Inventario de productos en proceso |
| `115.03` | Inventario de productos terminados |
| `115.04` | Mercancías en tránsito |
| `118.01` | IVA acreditable pagado (compras PUE o tras pago CRP) |
| `118.02` | IVA acreditable pendiente de acreditación (transitoria) |
| `119.01` | IVA pendiente de pago / acreditar (compras PPD — cuenta puente) |
| `120.01` | Anticipo a proveedores nacional |
| `120.02` | Anticipo a proveedores extranjero |
| `121.01` | Pagos anticipados |
| `123.01` | Estimaciones y provisiones deudoras (corto plazo) |
| `150.01` | Terrenos |
| `151.01` | Edificios y construcciones |
| `152.01` | Maquinaria y equipo |
| `153.01` | Equipo de transporte |
| `154.01` | Equipo de cómputo |
| `155.01` | Mobiliario y equipo de oficina |
| `160.01` | Activos intangibles |
| `161.01` | Depreciaciones acumuladas (activo fijo) |
| `162.01` | Amortizaciones acumuladas (intangibles) |

### Pasivo

| Código | Descripción |
|--------|-------------|
| `201.01` | Proveedores nacionales |
| `201.02` | Proveedores extranjeros |
| `202.01` | Documentos por pagar a corto plazo |
| `203.01` | Acreedores diversos nacionales |
| `205.01` | Préstamos bancarios a corto plazo (nacionales) |
| `206.01` | Anticipo de clientes nacional |
| `206.02` | Anticipo de clientes extranjero |
| `207.01` | Ingresos cobrados por anticipado |
| `208.01` | IVA trasladado cobrado (ventas PUE o tras cobro CRP) |
| `209.01` | IVA trasladado no cobrado (ventas PPD — cuenta puente) |
| `210.01` | Sueldos y salarios por pagar |
| `211.01` | IMSS por pagar (cuotas patronales y obreras) |
| `211.02` | INFONAVIT por pagar |
| `212.01` | Participación de utilidades por pagar (PTU) |
| `213.01` | Dividendos por pagar |
| `214.01` | Impuestos por pagar (ISR, IVA) |
| `215.01` | Impuestos y derechos por pagar (otros) |
| `216.01` | ISR retenido por sueldos y salarios |
| `216.02` | ISR retenido por asimilados a salarios |
| `216.03` | ISR retenido por arrendamiento |
| `216.04` | ISR retenido por servicios profesionales (honorarios) |
| `216.05` | ISR retenido por dividendos |
| `216.06` | ISR retenido por intereses |
| `216.07` | ISR retenido por actividades empresariales |
| `216.10` | IVA retenido (2/3 del IVA en servicios de personas físicas) |
| `217.01` | Contribuciones de mejoras por pagar |
| `218.01` | Derechos por pagar |
| `219.01` | Multas, recargos y actualizaciones (correcciones fiscales) |

### Resultados — Ingresos

| Código | Descripción |
|--------|-------------|
| `401.01` | Ventas y/o servicios gravados a tasa general (16%) |
| `401.02` | Ventas y/o servicios gravados a tasa 0% |
| `401.03` | Ventas y/o servicios exentos de IVA |
| `401.04` | Ventas de contado gravadas a tasa general |
| `401.05` | Ventas a crédito gravadas a tasa general |
| `402.01` | Devoluciones, descuentos y bonificaciones sobre ventas |
| `403.01` | Ingresos por arrendamiento |
| `404.01` | Ingresos por intereses |
| `405.01` | Ingresos por dividendos |
| `406.01` | Ingresos financieros (diferencial cambiario favorable) |

> **Separación obligatoria del grupo 401:** el Anexo 24 exige separar los ingresos entre tasa general, tasa 0%, exentos, contado y crédito. Esta es la causa más común de descuadres al conciliar contra un reporte de contador — si el catálogo del usuario solo tiene una cuenta "Ventas", sugiere desagregarla en estas subcuentas antes de intentar cuadrar cifras de IVA (ver también `matematica-cuadratura.md`, sección de diagnóstico IVA exento vs. gravado).

### Resultados — Costos y Gastos

| Código | Descripción |
|--------|-------------|
| `501.01` | Costo de ventas |
| `502.01` | Costo de producción |
| `601.01` | Gastos de operación — Sueldos y salarios |
| `601.26` | Gastos de operación — Cuotas IMSS patronal |
| `601.27` | Gastos de operación — Aportaciones INFONAVIT |
| `601.28` | Gastos de operación — PTU |
| `601.29` | Gastos de operación — Honorarios personas físicas |
| `601.30` | Gastos de operación — Arrendamiento personas físicas |
| `601.34` | Gastos de operación — Honorarios personas morales |
| `601.43` | Gastos de operación — Servicios de comunicaciones |
| `601.44` | Gastos de operación — Publicidad y propaganda |
| `601.45` | Gastos de operación — Consumos de energía |
| `601.50` | Gastos de operación — Teléfono / Internet |
| `601.84` | Gastos de operación — Seguros y fianzas |
| `602.01` | Gastos de venta — Sueldos y salarios |
| `603.XX` | Gastos de administración (misma estructura que 601) |
| `604.01` | Intereses y gastos financieros |
| `605.01` | Diferencias cambiarias desfavorables |
| `606.01` | Depreciación del ejercicio |
| `607.01` | Amortización del ejercicio |

## 4. Determinación del asiento por tipo de comprobante — vista extendida

```
I (Ingreso) ──→  ¿Emisor o Receptor?
  Como emisor   → Ingreso en 401.XX + Cliente/Banco
  Como receptor → Gasto/Costo + Proveedor/Banco + IVA

E (Egreso)  ──→  Reversa del asiento de la factura relacionada
                 Leer CfdiRelacionados obligatoriamente

T (Traslado) ─→  IGNORAR para pólizas de resultados
                 Solo registrar movimiento de inventario si aplica

P (Pago CRP) ─→  Cancelar saldo 105.01/201.01
                 Reclasificar IVA: 119.01→118.01 / 209.01→208.01
                 Afectar 102.01 Bancos por el monto cobrado/pagado

N (Nómina)  ──→  Provisión: 601.XX + 211.XX + 216.01 + 210.01
                 Pago: 210.01 → 102.01
```

Antes de generar el XML final, valida siempre `∑Debe = ∑Haber` por póliza. Si no cuadra, reporta el diferencial exacto y la transacción donde ocurre — no redondees para forzar el cuadre.