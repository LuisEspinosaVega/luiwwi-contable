# Complementos del CFDI 4.0 y Retenciones 2.0

## 1. Complemento para Recepción de Pagos (CRP / REP) 2.0 Rev. B

Namespace: `http://www.sat.gob.mx/Pagos20`

**Estructura del nodo `<pago20:Pago>`:**

```xml
<pago20:Pago
  FechaPago="2026-05-25T10:00:00"
  FormaDePagoP="03"
  MonedaP="MXN"
  TipoCambioP="1"
  Monto="11600.00"
  NumOperacion="SPEI-20260525-001"
  RfcEmisorCtaOrd="BCON771013XY6"
  NomBancoOrdExt="BBVA BANCOMER"
  CtaOrdenante="012180015548785456"
  RfcEmisorCtaBen="PROV990101XYZ"
  CtaBeneficiario="072840011199991234">

  <pago20:DoctoRelacionado
    IdDocumento="5FB2822E-396D-4725-8521-CDC4BDD20CCF"
    Serie="A"
    Folio="123"
    MonedaDR="MXN"
    EquivalenciaDR="1"
    NumParcialidad="1"
    ImpSaldoAnt="11600.00"
    ImpPagado="11600.00"
    ImpSaldoInsoluto="0.00"
    ObjetoImpDR="02">
    <!-- Si ObjetoImpDR = 02, incluir ImpuestosDR -->
  </pago20:DoctoRelacionado>

  <pago20:ImpuestosP>
    <pago20:TrasladosP>
      <pago20:TrasladoP
        BasePo="10000.00"
        ImpuestoP="002"
        TipoFactorP="Tasa"
        TasaOCuotaP="0.160000"
        ImporteP="1600.00"/>
    </pago20:TrasladosP>
  </pago20:ImpuestosP>
</pago20:Pago>
```

**Totales del complemento (obligatorios):**
```xml
<pago20:Totales
  TotalRetencionesIVA="0.00"
  TotalRetencionesISR="0.00"
  TotalRetencionesIEPS="0.00"
  TotalTrasladosBaseIVA16="10000.00"
  TotalTrasladosImpuestoIVA16="1600.00"
  TotalTrasladosBaseIVA8="0.00"
  TotalTrasladosImpuestoIVA8="0.00"
  TotalTrasladosBaseIVA0="0.00"
  TotalTrasladosImpuestoIVA0="0.00"
  MontoTotalPagos="11600.00"/>
```

**Validación IVA en CRP (Rev. B):** cuando `ImpuestoP = 002 (IVA)`, debe existir al menos uno de: `TotalTrasladadosBaseIVA16`, `TotalTrasladadosBaseIVA8`, `TotalTrasladadosBaseIVA0`, `TotalTrasladosBaseIVAExento`.

**Contablemente:** cancela saldo de `105.01 Clientes` o `201.01 Proveedores` y reclasifica IVA de cuenta puente a cuenta de flujo (`119.01→118.01` / `209.01→208.01`).

### Reglas críticas de cancelación del CRP (RMF 2026)

Desde el 1 de enero de 2026 (regla 2.7.1.35 modificada por la RMF 2026, publicada en el DOF el 28 de diciembre de 2025):

- Los CFDI con Complemento de Pago **quedaron excluidos de la cancelación directa/sin aceptación del receptor**, sin importar el monto (antes, los REP de hasta $1,000 MXN sí podían cancelarse directo; esa excepción ya no aplica).
- El emisor solicita la cancelación, el CFDI pasa a estatus **"En proceso de cancelación"**, el SAT notifica al receptor por Buzón Tributario y este tiene 3 días hábiles para aceptar o rechazar. Si no responde, opera silencio positivo y el CFDI queda "Cancelado por plazo vencido".
- En la práctica, la ventana operativa para cancelar un CRP sin fricción es **el mismo día de su emisión**; después de eso conviene usar un complemento de ajuste o una nota de crédito en vez de intentar cancelar.
- Los CFDI de hidrocarburos y petrolíferos (y Carta Porte con claves de combustible) requieren **aceptación expresa** del receptor — no aplica silencio positivo en ningún caso.

Ver `cancelaciones.md` para el proceso general y los 4 motivos de cancelación.

## 2. Complemento Carta Porte 3.1

Obligatorio en todo CFDI que ampare traslado de bienes dentro del territorio nacional (autotransporte federal, ferroviario, aéreo, marítimo). Vigente desde el 17 de julio de 2024; catálogos con actualizaciones periódicas.

**Campos obligatorios clave:**

| Nodo / Campo | Descripción |
|--------------|-------------|
| `TranspInternac` | `Sí` si cruza frontera, `No` si es nacional |
| `TotalDistRec` | Distancia en kilómetros del recorrido |
| `IdCCP` | Folio único del complemento (36 caracteres, patrón RFC 4122, inicia con "C") |
| `<Ubicaciones>` | Nodos `Origen` y `Destino` con código postal, municipio, estado y fecha/hora |
| `<Mercancias>` | Descripción, clave SAT, peso bruto, unidad de medida de aduana |
| `<Autotransporte>` | Permiso SCT, placa, configuración vehicular, seguros |
| `<FiguraTransporte>` | Operador (RFC/CURP), arrendador, propietario según aplique |

**Facilidad de traslado local:** una regla de facilidad permite acreditar el transporte local (sin transitar tramos federales) con el CFDI de ingreso o traslado, sin necesidad de incluir el complemento Carta Porte — confirma con el usuario si el traslado es puramente local antes de exigirle Carta Porte.

**Sanciones por incumplimiento:** multas por documento conforme al Art. 84 y 84-A CFF, retención de mercancías en carretera por SAT/Guardia Nacional, y rechazo de la deducibilidad del gasto de flete.

**Tipos de CFDI con Carta Porte:**
- **Transportista:** CFDI tipo `I` (cobra el servicio) + Carta Porte.
- **Propietario de los bienes:** CFDI tipo `T` (ampara el traslado propio) + Carta Porte.
- Si hay cambio de unidad, ruta o mercancía durante el traslado → cancelar el CFDI original y emitir uno nuevo.
- Los CFDI de tipo `I` con Carta Porte cuyas mercancías correspondan a claves de hidrocarburos/combustibles requieren aceptación expresa del receptor para cancelarse (igual que el complemento de hidrocarburos).

## 3. Complemento de Comercio Exterior 1.1

Obligatorio para exportaciones definitivas con clave de pedimento `A1` (enajenación de bienes). Namespace: `http://www.sat.gob.mx/ComercioExterior11`

| Campo | Descripción |
|-------|-------------|
| `TipoOperacion` | `2` para exportación, `1` para importación |
| `ClaveDePedimento` | Clave de pedimento aduanal (ej. `A1`) |
| `CertificadoOrigen` | `1` si hay certificado, `0` si no aplica |
| `NumCertificadoOrigen` | Folio del certificado (6-40 caracteres alfanuméricos) si `CertificadoOrigen = 1` |
| `IncoTerm` | Término de comercio internacional (FOB, CIF, DDP, etc.) |
| `TotalUSD` | Valor total de la operación en dólares USD |
| `TipoCambioUSD` | Tipo de cambio peso/dólar para los cálculos del complemento |
| `<Emisor><Domicilio>` | Dirección completa del emisor |
| `<Receptor><Domicilio>` | Dirección completa del receptor/destinatario (obligatoria) |
| `<Mercancias>` | Por concepto: `FraccionArancelaria`, `CantidadAduana`, `UnidadAduana`, `ValorUnitarioAduana`, `ValorDolares` |

- Si `UnidadAduana ≠ "99"` (servicios), el `ValorUnitarioAduana` debe ser mayor a cero.
- Si `UnidadAduana = "9"`, el campo `FraccionArancelaria` no debe existir.
- La `FraccionArancelaria` puede corresponder a múltiples fracciones por producto (v1.1).

## 4. Complemento Servicios Plataformas Tecnológicas

Obligatorio para los CFDI de retenciones que emiten plataformas como Uber, DiDi, Rappi, Airbnb, Mercado Libre, Amazon, etc. Se emite a más tardar el **día 5 del mes siguiente** al del servicio (plazo de la regla que fija la emisión del complemento de pagos para operaciones que no se pagan en una sola exhibición).

**Tasas de retención de referencia (verifica siempre la LIF vigente del ejercicio, ya que se actualizan anualmente):**

| Tipo de actividad | Retención ISR |
|-------------------|----------------|
| Transporte terrestre de pasajeros y entrega de bienes | Tramos progresivos según ingreso mensual |
| Hospedaje (Airbnb, Booking, Vrbo) | Tramos progresivos según ingreso mensual |
| Enajenación de bienes y demás servicios | Tasa fija sobre el monto (verificar LIF del ejercicio) |
| IVA (todas las actividades) | 8% del IVA trasladado |

> Los contribuyentes pueden optar por que las retenciones sean **pago definitivo** de ISR si cumplen los requisitos del Art. 113-B LISR; de lo contrario son pagos provisionales acreditables en la declaración anual. **No repitas de memoria una tasa exacta de retención sin verificarla** — la Ley de Ingresos de la Federación ajusta estos porcentajes cada año y usar una cifra vieja puede llevar a una retención mal calculada.

**Contabilización en el prestador de servicios:**
```
Cargo  102.01  Bancos (neto recibido)
Cargo  216.07  ISR retenido por actividades empresariales
Cargo  216.10  IVA retenido (si aplica)
       Abono  401.01  Ingresos gravados
       Abono  208.01  IVA trasladado cobrado
```

## 5. Retenciones e Información de Pagos 2.0

Documento independiente al CFDI estándar. Namespace: `http://www.sat.gob.mx/esquemas/retencionpago/2`

**Nodo raíz:**
```xml
<retenciones:Retenciones
  xmlns:retenciones="http://www.sat.gob.mx/esquemas/retencionpago/2"
  Version="2.0"
  FolioInt="RET-001"
  Sello="..."
  NoCertificado="..."
  Certificado="..."
  FechaExp="2026-05-25T10:00:00"
  CveRetenc="14"
  DescRetenc="Dividendos o utilidades distribuidos"
  Periodo="...">
```

**`CveRetenc` — principales claves:**

| Clave | Descripción |
|-------|-------------|
| `01` | Arrendamiento |
| `02` | Honorarios (servicios profesionales) |
| `03` | Enajenación de bienes |
| `04` | Fideicomisos no empresariales |
| `05` | Intereses |
| `06` | Premios por juegos o sorteos |
| `09` | Otros ingresos de fuente de riqueza nacional a extranjeros |
| `14` | Dividendos o utilidades distribuidos |
| `17` | Enajenación de acciones |
| `18` | Operaciones con instrumentos derivados |
| `19` | Pagos a residentes en el extranjero |
| `20` | Servicios de intermediación tecnológica (plataformas) |
| `25` | Otros (requiere `DescRetenc` obligatorio) |
| `28` | Utilidades distribuidas fictas (requiere `UtilidadBimestral > 0` e `ISRCorrespondiente > 0`; `MontoTotGrav = 0` y `MontoTotExent = 0`) |

**Nodo `<retenciones:Totales>` (cuadratura obligatoria):**
```
MontoTotOperacion = MontoTotGrav + MontoTotExent
MontoTotRet = Suma de todos los importes de retención
```

**Receptor nacional vs. extranjero:**
- `<retenciones:Nacional>`: validar `RfcR` contra padrón SAT.
- `<retenciones:Extranjero>`: incluir opcionalmente `NumRegIdTribR` (Tax ID en su país) y obligatoriamente `NomDenRazSocR` y `PaisResidencia`.

**Contabilización de retenciones:**
- ISR retenido → `216.0X` según tipo.
- IVA retenido → `216.10`.
- El monto bruto de la operación → cuenta de gasto correspondiente.
- El neto a pagar → `102.01 Bancos` o `201.01/203.01 Proveedores`.

En caso de error en un CFDI de Retenciones, se debe cancelar y reexpedir con los datos correctos (no existe CFDI de "egreso" análogo para retenciones).

## 6. Flujo completo de anticipos

Si el bien o precio **no están definidos al momento de recibir el pago**, es un anticipo. Existen dos flujos:

### Flujo A — Con CFDI de Egreso (más común)

**Paso 1 — Recepción del anticipo:**
- CFDI tipo `I`, `ClaveProdServ = 84111506`, `ClaveUnidad = ACT`, Descripción = "Anticipo del bien o servicio", `MetodoPago = PUE`, `FormaPago` = clave real.
- Póliza: Cargo `102.01 Bancos` → Abono `206.01 Anticipo de Clientes` + Abono `208.01 IVA Trasladado Cobrado`.

**Paso 2 — CFDI de operación total:**
- CFDI tipo `I` por el valor global. `CfdiRelacionados` con el UUID del Paso 1, `TipoRelacion = "07"`. `MetodoPago = PUE` o `PPD` según acuerdo.
- Póliza: Cargo `105.01 Clientes` (o `102.01` si PUE) → Abono `401.01 Ventas` + Abono `208.01`/`209.01` IVA según `MetodoPago`.

**Paso 3 — CFDI de Egreso por aplicación del anticipo:**
- CFDI tipo `E`, `ClaveProdServ = 84111506`, `FormaPago = "30"` (Aplicación de anticipo). `CfdiRelacionados` con el UUID del Paso 2, `TipoRelacion = "07"`.
- Póliza: Cargo `206.01 Anticipos de Clientes` → Abono `105.01 Clientes`.

### Flujo B — Sin CFDI de Egreso (descuento en factura final)

**Paso 1 — Recepción del anticipo:** igual que el Paso 1 del Flujo A.

**Paso 2 — CFDI de operación por el remanente:**
- CFDI tipo `I` con el valor total del bien, menos el anticipo registrado como `Descuento`. `CfdiRelacionados` con el UUID del Paso 1, `TipoRelacion = "07"`.
- El receptor paga solo el remanente (`Total - Anticipo ya pagado`).
- Póliza: Cargo `102.01 Bancos` (por el remanente) + Cargo `206.01 Anticipos` → Abono `401.01 Ventas` + Abono `208.01 IVA`.

## 7. Facturación al público en general (CFDI Global)

- **RFC del receptor:** `XAXX010101000` (nacional) o `XEXX010101000` (extranjero).
- **Nodo obligatorio:** `<cfdi:InformacionGlobal Periodicidad="01" Meses="05" Año="2026"/>`.
- **Claves de Periodicidad:** `01` Diario, `02` Semanal, `03` Quincenal, `04` Mensual, `05` Bimestral.
- El IVA y el IEPS deben desglosarse por separado en la factura global.
- Los contribuyentes de RESICO PF suelen tener restringida la periodicidad de esta factura global a mensual — confirma la regla vigente antes de asumirlo como definitivo si depende del ejercicio fiscal.
- **Motivo de cancelación 04:** si el cliente solicita factura nominativa después de emitida la global, se cancela el CFDI global con Motivo `04` y se emite el CFDI individual con los datos del cliente.
- **UsoCFDI:** `S01` (Sin efectos fiscales) para el público en general.

## 8. Operaciones en zonas PODEBI / POINBI

Para contribuyentes con actividades en los Polos de Desarrollo para el Bienestar del Istmo de Tehuantepec (PODEBI) o en Polos de Bienestar (POINBI):

- Se deben emitir **dos CFDI separados**: uno exclusivamente para ingresos de las actividades dentro del polo (con tasa preferencial de IVA si aplica), y otro para actividades fuera.
- `ObjetoImp = "05"` para operaciones dentro del polo con tasa reducida.
- `ObjetoImp = "06"` para operaciones dentro del polo exentas.

## 9. Addenda

Nodo de libre formato `<cfdi:Addenda>` al final del CFDI, después de todos los complementos. No forma parte de la cadena original para efectos fiscales, pero el PAC la incluye en el XML timbrado. Se usa para información adicional del receptor (orden de compra, código de proveedor, penalizaciones contractuales, datos logísticos). Ignora su contenido para efectos de la póliza contable, a menos que el usuario pida explícitamente mapear algún campo de la addenda.

## 10. Factura con IEPS

Cuando la actividad involucra bebidas alcohólicas, tabaco, combustibles, refrescos, alimentos con alto contenido calórico u otros bienes sujetos al IEPS:

- `Impuesto = "003"` (IEPS), `TipoFactor = "Tasa"` o `"Cuota"`.
- Las tasas de IEPS pueden tener hasta 6 decimales de precisión.
- El IEPS forma parte de la base del IVA: `Base IVA = SubTotal + IEPS`.
- En el catálogo de cuentas se registra una cuenta específica para IEPS trasladado/acreditable, separada del IVA.