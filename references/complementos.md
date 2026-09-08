# Complementos y documentos especializados

## Versiones de referencia

| Documento o complemento | Versión técnica | Tratamiento |
|---|---:|---|
| Timbre Fiscal Digital | 1.1 | Identidad del timbrado; validar por su propio esquema/cadena |
| Recepción de Pagos | 2.0 | Pagos, parcialidades, saldos e impuestos |
| Nómina | 1.2 | Percepciones, deducciones y otros pagos |
| Carta Porte | 3.1 | Información de traslado/transporte cuando corresponde |
| Comercio Exterior | 2.0 | Operaciones de exportación aplicables |
| Retenciones e información de pagos | 2.0 | Documento independiente, no confundir con CFDI 4.0 tipo `P` |

La versión anterior de esta skill registraba verificación de estos XSD al 2026-08-19; no se revalidó todo el paquete técnico en la auditoría del 07-09-2026. Antes de validar o emitir seleccionar y recuperar el paquete oficial por fecha/vigencia. La revisión de catálogos puede cambiar sin alterar el número principal del complemento.

## Estrategia de parser

1. Identificar por URI de namespace, no por prefijo (`pago20`, `nomina12`, etc.).
2. Conservar el subárbol XML original aunque no exista parser especializado.
3. Registrar namespace, versión declarada, hash y resultado XSD.
4. Ejecutar un adaptador versionado por complemento.
5. Marcar `unsupported` o `partial`, nunca descartar silenciosamente.

## Nómina

No reutilizar el catálogo de CFDI de ingreso para percepciones/deducciones. Validar contra catálogos y matriz de Nómina vigentes al periodo. No copiar una lista fija de claves “2026” en la lógica: una revisión de catálogo puede añadir claves sin cambiar Nómina 1.2.

Separar importe gravado/exento declarado de un recálculo laboral/fiscal. El CFDI informa, pero no basta para concluir que cálculo de ISR, subsidio o seguridad social fue correcto.

## Carta Porte

No inferir su obligatoriedad sólo porque exista un CFDI de traslado o una clave de producto. Depende de quién transporta, medio, trayecto y reglas vigentes. Si se analiza, revisar ubicaciones, mercancías, figuras, transporte y consistencia con el CFDI base.

## Comercio Exterior

Usar 2.0 para documentos dentro de su vigencia; no proponer 1.1 como versión actual. Validar moneda, tipo de cambio, mercancías, destinatario y pedimento según esquema y reglas aplicables, sin convertir el complemento en dictamen aduanero.

## Extensibilidad

El sistema debe admitir complementos nuevos sin migrar toda la tabla de CFDI. Mantener una tabla/nodo de complementos y vistas especializadas. Los KPIs generales deben declarar si ignoran datos de un complemento no soportado.
