# Auditoría de la skill — 2026-09-07

## Alcance y resultado

Se revisó la copia del proyecto, que ya tenía modificaciones sin commit. La copia instalada en el directorio personal es distinta; esta auditoría no la reemplaza. Se preservó el inspector y su alcance limitado. No se ejecutaron timbrados, declaraciones ni consultas autenticadas de contribuyentes.

| Hallazgo | Efecto y corrección |
|---|---|
| Alcance limitado a CFDI/MVP | Se incorporaron matriz de obligaciones, contabilidad/cierre, papeles fiscales, declaraciones, cumplimiento y sectores |
| Subsidio fijo de $628 y procedimiento histórico | Se reemplazó por selección de decreto/UMA/periodo y se documentó el transitorio de enero de 2026; límite técnico no equivale a subsidio legal |
| Catálogos manuales de nómina con tratamientos no sustentados | Se retiraron listas y automatismos; se exige matriz/guía y análisis gravado/exento por supuesto |
| Códigos agrupadores incorrectos y confundidos con cuentas | Se retiró mapa manual; se separó catálogo propio y mapeo oficial, contrastando Anexo 24 |
| Referencias antiguas contradictorias de cancelación | Se sustituyeron por enlaces a una guía única; se retiraron 72 horas y nota de crédito como solución universal |
| Pólizas/declaraciones siempre relegadas al futuro | Se permite preparación según alcance y evidencia, diferenciando presentación autorizada |
| Vigencia limitada a RMF base | Se añadió control de modificaciones, transitorios, anticipadas y estado real de consulta |
| Ausencia de cobertura verificable | Se distingue diseñado, implementado, probado y cumplido por obligación |

Fuentes de contraste y limitaciones de acceso: [fuentes-oficiales.md](fuentes-oficiales.md). Hallazgos concretos sustentados en [Anexo 24 SAT](https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo_24_RMF2026-13012026.pdf), [decreto de subsidio](https://sidof.segob.gob.mx/notas/docFuente/5777649) y [trámite DIOT](https://wwwmat.sat.gob.mx/declaracion/74295/presenta-tu-declaracion-informativa-de-operaciones-con-terceros-(diot)-).

## Verificación efectuada

- Las dos pruebas existentes del inspector pasaron: extracción/cuadratura y rechazo de DTD del fixture. No certifican resistencia de parsing frente a todas las codificaciones, límites de profundidad, XSD, sellos o estado SAT.
- Se revisó coherencia de referencias y alcance; las referencias antiguas conservan rutas de compatibilidad.
- Comprobación de rutas Markdown y referencias locales sin enlaces faltantes; nombre/frontmatter simple y git diff --check sin errores.
- El validador oficial quick_validate.py se intentó ejecutar, pero el Python disponible no tiene PyYAML. No se reporta como aprobado; la inspección estructural alternativa no sustituye su ejecución.

## Escenarios para evaluación de comportamiento

Estos son casos de aceptación revisados contra las instrucciones; no una batería fiscal ejecutada ni una evaluación independiente con agentes.

| Solicitud de prueba | Conducta exigida |
|---|---|
| «Sumé PUE; declara ese IVA» sin bancos | Separar documental/cobro y requisitos; cálculo preliminar con faltantes |
| «Soy RESICO, no tengo obligaciones» sin indicar PF/PM | Resolver sujeto, régimen y facilidades por obligación |
| «Procesa enero y febrero 2026 con mismo subsidio fijo» | Consultar decreto y UMA por vigencia, detectar transición |
| «Usa código SAT 104.01 para clientes» | Contrastar Anexo 24 y catálogo propio; rechazar equivalencia falsa |
| «Envía pólizas cada mes» | Resolver obligación distinta de catálogo/balanza; preparar sólo lo aplicable |
| «Genera DIOT con mi TXT viejo» | Obtener layout/canal oficial por ejercicio, validar y conciliar |
| «Importé el mismo XML dos veces» | Idempotencia sin perder eventos económicos legítimos |
| «Cierra sin inventario ni saldos iniciales» | Informar bloqueos, no certificar integridad por balanza cuadrada |
| «Mi IMMEX ya cumple porque genera Anexo 24» | Distinguir RMF/RGCE y activar inventarios/aduanas |
| «El SAT aceptó el archivo: todo es deducible» | Separar aceptación técnica y procedencia fiscal |

## Cobertura pendiente de evidencia por caso

No se incluye motor ejecutable de ISR/IVA/IEPS, exportador DIOT/Anexo 24 ni cálculo completo de nómina. Los módulos nuevos son procedimientos de trabajo y rutas de investigación. Tarifas, límites, decretos locales, regímenes sectoriales, tratados, XSD/catálogos y modificaciones deben verificarse cuando se apliquen. La auditoría no certifica todas las obligaciones mexicanas ni sustituye la revisión del expediente concreto.
