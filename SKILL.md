---
name: luiwwi-contable
description: Analiza, audita y diseña contabilidad mexicana y cumplimiento SAT para personas físicas y morales. Úsala con CFDI/XML, pólizas, cierres, ISR, IVA, IEPS, nómina, declaraciones, DIOT, contabilidad electrónica, conciliaciones y software contable mexicano. Resuelve régimen, periodo y fuentes oficiales antes de determinar obligaciones; identifica sectores especiales y separa evidencia documental, reconocimiento contable y efectos fiscales.
---

# Luiwwi Contable

## Objetivo

Producir contabilidad y papeles fiscales reproducibles con trazabilidad hasta la evidencia. Separar documentos, hechos económicos, reconocimiento contable, determinación fiscal y presentación ante la autoridad. El SAT no emite las NIF ni sustituye las obligaciones laborales, aduaneras o locales. Cubrir sólo los módulos aplicables al caso, sin convertir un análisis de XML en una implementación completa no solicitada.

## Principios obligatorios

1. Priorizar SAT, DOF y Cámara de Diputados. Para reglas, catálogos, límites o versiones que puedan cambiar, consultar la fuente oficial vigente al periodo; usar `references/fuentes-oficiales.md`.
2. Conservar el XML original y su hash antes de normalizar. Nunca reconstruir el original desde la base de datos.
3. Separar cinco capas: sintaxis/XML, XSD y catálogos, sello/timbrado, estado SAT y conciliación económica. Una capa aprobada no sustituye a las demás.
4. Usar decimales exactos y las reglas de redondeo del estándar; no usar `float` binario para importes.
5. No equiparar `PUE` con cobro bancario confirmado. Es una declaración documental y admite la opción de pago dentro del mismo mes prevista por la RMF.
6. No presentar IVA, ISR o saldo a cargo como definitivo si faltan régimen, periodo, pagos, deducciones, acreditamiento, retenciones o reglas aplicables.
7. Asignar a cada resultado uno de estos niveles:
   - **Confirmado:** existe evidencia independiente suficiente, por ejemplo XML vigente más movimiento bancario conciliado.
   - **Documental:** está declarado en CFDI/REP o en el estado SAT, pero no confirmado externamente.
   - **Estimado:** deriva de una regla o supuesto identificado.
   - **Incompleto:** faltan datos que pueden cambiar materialmente el resultado.
8. Explicar la fecha de corte. No mezclar fecha de emisión, fecha de pago, descarga y cancelación.
9. Para pólizas, usar doble partida, catálogo del contribuyente y periodo controlado; corregir registros contabilizados mediante reversión o ajuste trazable. Ésta es una política de integridad del sistema, no una afirmación de que toda entidad tiene idénticas obligaciones de envío.
10. Diferenciar obligación de llevar contabilidad, formato electrónico, envío periódico y entrega por requerimiento; una facilidad no elimina automáticamente las otras obligaciones.
11. No fijar tasas, cuotas, plazos, UMA, UMI, INPC, tipos de cambio ni layouts sin fuente y vigencia. Separar versiones anticipadas, publicación DOF, transitorios y compilaciones informativas.

## Flujo de trabajo

### 1. Delimitar

Identificar RFC, PF/PM, residencia fiscal, ejercicio, regímenes y cambios, actividades, obligaciones registradas, ubicación, monedas y finalidad. Detectar empleados, inventarios, importaciones, partes relacionadas y supuestos especiales con [la matriz de alcance](references/alcance-cobertura.md). La constancia fiscal es evidencia de registro, no prueba de que las obligaciones estén correctamente actualizadas. Preguntar sólo faltantes materiales y continuar con el trabajo independiente.

### 2. Adquirir y preservar

Descargar mediante el servicio oficial o importar XML/ZIP. Registrar procedencia, solicitud, paquete, instante, hash SHA-256 y errores. Aplicar `references/descarga-almacenamiento.md`.

### 3. Inspeccionar y validar

Para una inspección inicial local ejecutar:

```bash
python3 scripts/inspect_cfdi.py ruta/al/cfdi.xml --pretty
```

El script no sustituye validación XSD, sello, timbre ni consulta de estado. Completar las capas descritas en `references/validacion-matematica.md`.

### 4. Normalizar sin perder evidencia

Extraer comprobante, participantes, conceptos, impuestos, relaciones, timbre y complementos. Mantener valor lexical original junto al valor decimal/fecha normalizado. Consultar `references/taxonomia-cfdi.md` y, si corresponde, `references/complementos.md`.

### 5. Determinar estado económico

Procesar cancelaciones, notas de crédito y REP antes de calcular saldos. Separar pago declarado, pago conciliado y pago inferido. Consultar `references/pagos-cobranza.md` y `references/cancelaciones-relaciones.md`.

### 6. Calcular

Definir universo, filtros, moneda, conversión, fórmula y tolerancia. Para métricas documentales aplicar `references/analitica-financiera.md`. Para contabilidad reconstruir operaciones y saldos iniciales, proponer pólizas y conciliar auxiliares según [contabilidad y cierre](references/contabilidad-cierre.md). Para impuestos aplicar [regímenes](references/fiscal-regimenes.md) y [papeles fiscales](references/impuestos-determinacion.md); para cumplimiento usar [declaraciones](references/declaraciones-informativas.md). No forzar los cálculos fiscales a coincidir con el prellenado SAT: explicar las diferencias.

### 7. Comunicar

Entregar:

- resultado y unidad;
- periodo y fecha de corte;
- documentos incluidos/excluidos y por qué;
- fórmula y política de moneda/redondeo;
- nivel de certeza;
- faltantes y efecto posible;
- fuente oficial para toda conclusión normativa.

## Enrutamiento de referencias

| Necesidad | Leer |
|---|---|
| Servicio de descarga, estados, idempotencia y bóveda XML | `references/descarga-almacenamiento.md` |
| Tipos, fechas, PUE/PPD, relaciones y campos base | `references/taxonomia-cfdi.md` |
| Cuadratura, decimales y capas de validación | `references/validacion-matematica.md` |
| REP 2.0, parcialidades, monedas y saldos | `references/pagos-cobranza.md` |
| Cancelación, aceptación, motivos y sustitución | `references/cancelaciones-relaciones.md` |
| Versiones y tratamiento de complementos | `references/complementos.md` |
| KPIs útiles para freelancers y PyME | `references/analitica-financiera.md` |
| ISR/IVA por régimen y límites de una estimación | `references/fiscal-regimenes.md` |
| Pólizas, catálogo propio y código agrupador SAT | `references/contabilidad-anexo24.md` |
| Seguridad, privacidad, auditoría y riesgo | `references/cumplimiento-seguridad.md` |
| Arquitectura de un MVP Laravel modular | `references/arquitectura-mvp.md` |
| Fuentes oficiales y precedencia | `references/fuentes-oficiales.md` |
| Clasificación, matriz de obligaciones y sectores especiales | [alcance-cobertura.md](references/alcance-cobertura.md) |
| Mayor, bancos, inventarios, activos, NIF, estados financieros y cierre | [contabilidad-cierre.md](references/contabilidad-cierre.md) |
| ISR, IVA, IEPS y conciliación contable-fiscal | [impuestos-determinacion.md](references/impuestos-determinacion.md) |
| Declaraciones, DIOT, devoluciones e informativas | [declaraciones-informativas.md](references/declaraciones-informativas.md) |
| Nómina, subsidio, PTU e interfaces IMSS/INFONAVIT | [nomina.md](references/nomina.md) |
| RFC, Buzón, certificados, beneficiario controlador y facultades | [cumplimiento-sat.md](references/cumplimiento-sat.md) |
| Comercio exterior, grupos y obligaciones sectoriales | [sectores-especiales.md](references/sectores-especiales.md) |
| Auditoría de esta skill y escenarios de evaluación | [auditoria-skill.md](references/auditoria-skill.md) |

## Límites y prohibiciones

- No inventar una póliza universal a partir del tipo de CFDI. Requiere catálogo, configuración contable, contexto y evidencia de pago.
- No usar `FormaPago`, `MetodoPago` o el estado vigente como prueba bancaria.
- No convertir una nota de crédito en devolución de efectivo sin evidencia.
- No asumir que `LugarExpedicion` es siempre el domicilio fiscal.
- No reutilizar catálogos obsoletos como `P01` ni números de versión recordados; validar el catálogo vigente.
- No rechazar automáticamente a una contraparte por una alerta de riesgo. Informar la fuente, fecha y alcance para revisión humana.
- No registrar, imprimir ni incluir e.firma, contraseña o llave privada en prompts, logs o errores.
- No procesar DTD ni entidades externas. Limitar tamaño y profundidad antes de analizar XML no confiable.

## Implementación de producto

Usar `references/arquitectura-mvp.md` sólo si se solicita arquitectura o implementación. La skill permite preparar pólizas, cierres, DIOT y declaraciones dentro del alcance autorizado; no los posterga automáticamente por ser un MVP. Entregar borradores con faltantes cuando falte evidencia y bloquear únicamente la conclusión o salida oficial afectada. Preparar archivos no equivale a presentarlos: timbrar, cancelar, enviar, firmar o pagar requiere autorización que cubra esa operación y contribuyente; respetar la ya otorgada.

No afirmar «cumplimiento total» por una lista de funciones. Informar por obligación: aplicabilidad, fuente, evidencia, cálculo, validación técnica y acuse cuando corresponda. Un archivo válido no demuestra aceptación SAT y un acuse no demuestra corrección sustantiva.
