#!/usr/bin/env python3
"""Inspección local y conservadora de un CFDI; no valida XSD, sello ni SAT."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.etree import ElementTree as ET

MAX_BYTES = 25 * 1024 * 1024
CFDI_NS = "http://www.sat.gob.mx/cfd/4"
TFD_NS = "http://www.sat.gob.mx/TimbreFiscalDigital"
FORBIDDEN = (b"<!DOCTYPE", b"<!ENTITY")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def namespace(tag: str) -> str | None:
    return tag[1:].split("}", 1)[0] if tag.startswith("{") else None


def decimal_or_none(value: str | None) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def as_text(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")


def child(parent: ET.Element, name: str) -> ET.Element | None:
    return parent.find(f"{{{CFDI_NS}}}{name}")


def inspect(path: Path) -> dict:
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(f"XML excede el límite de {MAX_BYTES} bytes")
    raw = path.read_bytes()
    upper = raw.upper()
    if any(token in upper for token in FORBIDDEN):
        raise ValueError("DTD o entidades no permitidas")

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError(f"XML no bien formado: {exc}") from exc

    if local_name(root.tag) != "Comprobante":
        raise ValueError("La raíz no es Comprobante")

    ns = namespace(root.tag)
    emisor = child(root, "Emisor")
    receptor = child(root, "Receptor")
    conceptos_parent = child(root, "Conceptos")
    conceptos = [] if conceptos_parent is None else list(conceptos_parent)
    relaciones = []
    for group in root.findall(f"{{{CFDI_NS}}}CfdiRelacionados"):
        uuids = [node.get("UUID") for node in list(group) if node.get("UUID")]
        relaciones.append({"tipo": group.get("TipoRelacion"), "uuids": uuids})

    timbre = root.find(f".//{{{TFD_NS}}}TimbreFiscalDigital")
    complementos = []
    complemento = child(root, "Complemento")
    if complemento is not None:
        for node in list(complemento):
            complementos.append(
                {
                    "elemento": local_name(node.tag),
                    "namespace": namespace(node.tag),
                    "version": node.get("Version") or node.get("version"),
                }
            )

    subtotal = decimal_or_none(root.get("SubTotal"))
    descuento = decimal_or_none(root.get("Descuento")) or Decimal("0")
    total = decimal_or_none(root.get("Total"))
    impuestos = child(root, "Impuestos")
    trasladados = decimal_or_none(None if impuestos is None else impuestos.get("TotalImpuestosTrasladados")) or Decimal("0")
    retenidos = decimal_or_none(None if impuestos is None else impuestos.get("TotalImpuestosRetenidos")) or Decimal("0")
    esperado = None if subtotal is None else subtotal - descuento + trasladados - retenidos
    diferencia = None if total is None or esperado is None else total - esperado

    return {
        "archivo": str(path),
        "bytes": size,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "documento": {
            "namespace": ns,
            "es_cfdi_4": ns == CFDI_NS and root.get("Version") == "4.0",
            "version": root.get("Version"),
            "tipo": root.get("TipoDeComprobante"),
            "fecha": root.get("Fecha"),
            "moneda": root.get("Moneda"),
            "metodo_pago": root.get("MetodoPago"),
            "forma_pago": root.get("FormaPago"),
            "lugar_expedicion": root.get("LugarExpedicion"),
        },
        "emisor": None if emisor is None else {"rfc": emisor.get("Rfc"), "nombre": emisor.get("Nombre"), "regimen": emisor.get("RegimenFiscal")},
        "receptor": None if receptor is None else {"rfc": receptor.get("Rfc"), "nombre": receptor.get("Nombre"), "uso": receptor.get("UsoCFDI"), "regimen": receptor.get("RegimenFiscalReceptor")},
        "timbre": None if timbre is None else {"uuid": timbre.get("UUID"), "fecha": timbre.get("FechaTimbrado"), "version": timbre.get("Version")},
        "conteos": {"conceptos": len(conceptos), "relaciones": sum(len(g["uuids"]) for g in relaciones), "complementos": len(complementos)},
        "relaciones": relaciones,
        "complementos": complementos,
        "cuadratura_inicial": {
            "subtotal": as_text(subtotal),
            "descuento": as_text(descuento),
            "trasladados": as_text(trasladados),
            "retenidos": as_text(retenidos),
            "total": as_text(total),
            "total_esperado": as_text(esperado),
            "diferencia": as_text(diferencia),
            "coincide_exactamente": None if diferencia is None else diferencia == 0,
            "alcance": "Control aritmético inicial; no valida límites, XSD, catálogos, sello, timbre ni estado SAT.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = inspect(args.xml)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
