# Nómina, subsidio y seguridad social

## Flujo y evidencia

Separar relación laboral/asimilados, remuneración, ISR, timbrado, dispersión, contabilidad y enteros. Pedir periodo, días, incidencias, percepciones, deducciones, acumulados, otros patrones cuando afecten el cálculo, altas/bajas y datos fiscales. No inferir gravado/exento sólo por descripción o clave.

Consultar LISR 93–99, Reglamento, tarifas, decreto de subsidio y [documentación SAT](http://omawww.sat.gob.mx/tramitesyservicios/Paginas/complemento_nomina.htm). Descargar guía, XSD, catálogos y matriz vigentes; una revisión puede cambiar sin modificar la versión 1.2. No afirmar soporte de revisión sólo por namespace.

## Validaciones técnicas

Distinguir `RegimenFiscalReceptor` del CFDI de `TipoRegimen` del complemento. No aceptar 606, 608 o 611 como sustitutos genéricos del régimen de nómina. Resolver identidad, uso y claves contra la matriz oficial; no mantener catálogos manuales con etiquetas fiscales no sustentadas.

Conciliar percepciones gravadas/exentas, deducciones, otros pagos y total; revisar agrupaciones de sueldos, separación y jubilaciones. Validar nodos condicionales de horas extra, incapacidades, acciones, jubilación y separación y tipo ordinario/extraordinario. No forzar dos recibos ni duplicar complementos sin fundamento.

## Subsidio por vigencia

El [decreto DOF de 31-12-2025](https://sidof.segob.gob.mx/notas/docFuente/5777649), consultado el 07-09-2026, establece para 2026 límite mensual de base ISR de $11,492.66 y cálculo con UMA mensual por 15.02%; enero tiene transitorio de 15.59%. Para periodos menores al mes usa división entre 30.4, días del periodo y límite mensual; para pagos de dos o más meses hay regla específica. Son parámetros de ese decreto, sujetos a reformas posteriores.

No usar $628 como subsidio legal fijo ni confundir límite técnico de timbrado con derecho fiscal. Separar subsidio causado, aplicado y efectivamente entregado. Consultar también el decreto original de 01-05-2024 y modificaciones para los párrafos no reproducidos en 2025: no ordenar entrega de excedente sobre ISR basándose en el procedimiento histórico de tablas. Si falta texto consolidado, dejar pendiente ese efecto.

## Cálculos y conciliaciones

Preparar papel por trabajador/concepto con base, exención y unidad legal aplicable (UMA o salario mínimo según fundamento), tarifa, subsidio, ISR, ajuste mensual/anual y neto. Resolver viáticos, aguinaldo, vacaciones, prima, PTU, horas extra, indemnizaciones y jubilaciones por supuesto. No declarar exentas ayudas, fondos o previsión social sólo por su nombre.

Conciliar acumulados ↔ CFDI vigentes/sustituidos ↔ visor SAT ↔ dispersión ↔ ISR declarado/enterado ↔ mayor. Cancelar un documento no revierte automáticamente transferencia ni devengo.

En sustituciones distinguir relación del CFDI nuevo hacia el anterior y UUID sustituto reportado al cancelar el anterior; aplicar [cancelaciones](cancelaciones-relaciones.md).

## PTU, IMSS e INFONAVIT

Separar PTU determinada, provisión contable, reparto, límites laborales, exención y retención. Consultar [Manual laboral y fiscal PTU 2026 SAT](https://www.sat.gob.mx/minisitio/RepartodeUtilidades/documentos/manuallaboralfiscal2026.pdf) y leyes aplicables sin trasladar fechas a otro ejercicio.

Para seguridad social verificar LSS, Ley INFONAVIT y publicaciones IMSS/INFONAVIT: SBC fijo/variable/mixto, integración/exclusiones, topes, días, incidencias, riesgo, cuotas obreras/patronales, retiro/cesantía/vejez, vivienda y amortizaciones. Resolver UMA/UMI/salario mínimo y tabla de cuotas por fecha; no calcular todo con un porcentaje del bruto.

Conciliar movimientos afiliatorios, SUA/IDSE/SIPARE, emisiones y pagos con sus periodicidades. Para servicios especializados activar REPSE/ICSOE/SISUB y para construcción SIROC. Requieren documentación de su autoridad, no sólo SAT.

Contabilizar costo/gasto y pasivos al trabajador/autoridades con catálogo propio; al pagar extinguir el pasivo. No copiar códigos agrupadores como cuentas internas.
