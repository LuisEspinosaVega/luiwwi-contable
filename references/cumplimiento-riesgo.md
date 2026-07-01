# Auditoría, Riesgos y Validaciones Legales (Compliance CFF)

## 1. EFOS y EDOS — Art. 69-B CFF

**EFOS (Empresa que Factura Operaciones Simuladas):**
- Contribuyentes que emiten CFDI sin contar con activos, personal, infraestructura o capacidad material para realizar las operaciones que amparan.
- El SAT los publica en el DOF: primero como **presuntos** (con plazo de aclaración), luego como **definitivos** si no desvirtuaron la presunción.

**EDOS (Empresa que Deduce Operaciones Simuladas):**
- Empresa que da efecto fiscal (deducción o acreditamiento) a CFDI emitidos por un EFOS.
- Una vez publicado el listado definitivo, la EDOS tiene un plazo (históricamente 30 días) para acreditar ante el SAT la materialidad de las operaciones o corregir su situación fiscal.
- Si no lo hace, los comprobantes pierden sus efectos fiscales de pleno derecho.

**Consecuencias para la EDOS:**
- Gastos no deducibles → mayor ISR a pagar.
- IVA no acreditable → mayor IVA a pagar.
- Multas (Art. 75-79 CFF).
- Cancelación de sellos digitales (Art. 17-H Bis CFF).
- **Responsabilidad penal:** Art. 113-Bis CFF — prisión por uso o adquisición de CFDI que amparen operaciones inexistentes. Verifica el rango de años vigente al citarlo en un contexto formal, ya que las penas del CFF se han ajustado en reformas recientes.

**Lo que debes hacer al procesar un CFDI de gasto:**
1. Indicar al usuario que cruce el RFC del emisor contra las listas publicadas en el portal del SAT (ver `normativa-urls.md`); tú no tienes acceso directo a ese padrón salvo que uses búsqueda web para verificar un caso puntual.
2. Si el usuario confirma que el RFC aparece como EFOS **definitivo** → bloquear la póliza y explicar la consecuencia concreta (deducción nula, riesgo penal) en vez de solo citar el artículo.
3. Si aparece como EFOS **presunto** → alertar y continuar la póliza marcada como "en revisión", no bloquearla de forma definitiva todavía.
4. Recordar que existen otras listas del Art. 69 CFF (no localizados, incumplidos, etc.) relevantes para una debida diligencia completa, no solo la de EFOS.

## 2. Materialidad de las operaciones

El SAT no acepta el CFDI como única prueba de deducibilidad o acreditamiento. La **materialidad** exige demostrar que la operación económicamente ocurrió.

**Documentos que acreditan materialidad por tipo de operación:**

| Tipo de operación | Documentos de materialidad |
|--------------------|------------------------------|
| Servicios profesionales | Contrato, propuestas, entregables (reportes, código, diseños), correos, minutas, evidencia de pago bancarizado |
| Compra de bienes | Orden de compra, remisión/albarán, entrada de almacén, fotografías del bien recibido, carta porte |
| Arrendamiento | Contrato de arrendamiento, comprobante de pago, fotografías del inmueble usado |
| Fletes y transportes | Carta Porte, manifiesto de carga, bitácoras del operador, órdenes de servicio |
| Publicidad y marketing | Brief, artes, métricas de campaña, reportes de resultados |
| Servicios de TI/Software | Especificaciones técnicas, código fuente entregado, tickets de soporte, ambientes de prueba |

**Recomendación operativa:** por cada CFDI de gasto relevante (montos altos, proveedores nuevos, o servicios intangibles como consultoría/TI), sugiere generar un "expediente de materialidad" vinculado al UUID con la evidencia de la operación real. Esto es especialmente relevante para el tipo de deliverables de software/consultoría con los que suele trabajar el usuario, donde la evidencia de materialidad (specs, código entregado, tickets) es más fácil de perder que en compra de bienes físicos.

## 3. Sello digital de la contabilidad electrónica

Los archivos XML de contabilidad electrónica (catálogo, balanza, pólizas) deben llevar un **sello digital propio**, generado con la e.firma del contribuyente (no con el CSD de facturación). Este sello garantiza la integridad del archivo enviado al SAT.

**Proceso:**
1. Generar la cadena original del archivo XML conforme al XSLT del SAT.
2. Aplicar el algoritmo SHA-256 sobre la cadena original.
3. Cifrar con la llave privada de la e.firma (RSA).
4. El resultado en Base64 es el `Sello` del archivo.
5. Incluir el `NoCertificado` y el `Certificado` (contenido Base64 del archivo `.cer` de la e.firma).

## 4. CSD — Certificado de Sello Digital

- Compuesto por 2 archivos: `.cer` (llave pública) y `.key` (llave privada, protegida con contraseña).
- Vigencia de varios años desde la fecha de expedición (verifica el plazo exacto vigente si es relevante para el caso concreto). No se renueva automáticamente.
- Distinción clave: el CSD es para **facturación**; la e.firma (FIEL) es para **trámites ante el SAT**.
- Personas físicas pueden timbrar con e.firma directamente; personas morales requieren CSD.
- El PAC consulta la **Lista de Contribuyentes Obligados (LCO)** antes de cada timbrado:
  - Si el CSD es activo → acepta el timbrado.
  - Si el CSD está revocado o caducado:
    - Fecha de emisión del CFDI anterior a la fecha de caducidad del CSD → acepta.
    - Fecha de emisión posterior → rechaza.
- El SAT puede revocar el CSD (Art. 17-H Bis CFF) por incumplimiento fiscal grave.

## 5. Proceso de timbrado — flujo técnico

```
Contribuyente genera XML del CFDI
         ↓
Firma con su CSD (Sello Digital Emisor)
         ↓
Envía al PAC (Proveedor Autorizado de Certificación)
         ↓
PAC valida:
  ① Estructura XSD y reglas Anexo 20
  ② Vigencia y estatus del CSD del emisor (vía LCO)
  ③ Datos del receptor contra padrón SAT
  ④ Compatibilidad UsoCFDI ↔ RegimenFiscalReceptor
  ⑤ Cálculos matemáticos (límites inferior/superior)
  ⑥ Reglas específicas del tipo de comprobante
         ↓
PAC sella con su Certificado de Timbre (emitido por el SAT)
         ↓
PAC incorpora nodo <tfd:TimbreFiscalDigital> con:
  UUID, FechaTimbrado, RfcProvCertif, SelloCFD, SelloSAT, NoCertificadoSAT
         ↓
PAC retorna el CFDI timbrado al contribuyente
         ↓
PAC reporta al SAT
```

## 6. RESICO — Régimen Simplificado de Confianza

**Personas Físicas (Art. 113-E LISR):**
- Tope de ingresos anuales para permanecer en el régimen (verifica el monto exacto vigente, ya que se ha ajustado entre ejercicios).
- ISR calculado con tasas progresivas bajas sobre ingresos cobrados (pagos definitivos mensuales).
- No llevan contabilidad electrónica completa; pueden usar "Mis Cuentas".
- Sin DIOT mensual ni declaraciones informativas múltiples.
- Si los ingresos superan el tope, salen automáticamente al cierre del ejercicio.
- Si una PM les retiene ISR e IVA, estas retenciones son acreditables.

**Personas Morales (Art. 206 LISR):**
- Tope de ingresos anuales distinto al de personas físicas (verificar monto vigente).
- ISR con tasas bajas aplicadas directamente sobre ingresos cobrados.
- Sí llevan contabilidad electrónica completa.

**Obligaciones CFDI en RESICO:**
- Emitir CFDI 4.0 en todas las operaciones, igual que cualquier régimen.
- CFDI global con periodicidad restringida (mensual, no diaria ni semanal) para el público en general.
- Mantener buzón tributario y e.firma activos.

Los topes de ingresos de RESICO (tanto PF como PM) son de los datos que más frecuentemente se actualizan en reformas fiscales anuales — si el usuario va a tomar una decisión real basada en si está dentro o fuera del tope, verifica la cifra vigente con búsqueda web en vez de repetir un monto de memoria.