#!/usr/bin/env python3
"""Pruebas unitarias sin red para inspect_cfdi.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from inspect_cfdi import inspect


SAMPLE = b'''<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4"
 xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital"
 Version="4.0" Fecha="2026-08-19T10:00:00" TipoDeComprobante="I"
 Moneda="MXN" SubTotal="100.00" Total="116.00" LugarExpedicion="06000">
 <cfdi:Emisor Rfc="AAA010101AAA" Nombre="EMISOR" RegimenFiscal="601"/>
 <cfdi:Receptor Rfc="BBB010101BBB" Nombre="RECEPTOR" DomicilioFiscalReceptor="06000"
  RegimenFiscalReceptor="612" UsoCFDI="G03"/>
 <cfdi:Conceptos>
  <cfdi:Concepto ClaveProdServ="01010101" Cantidad="1" ClaveUnidad="ACT"
   Descripcion="PRUEBA" ValorUnitario="100.00" Importe="100.00" ObjetoImp="02"/>
 </cfdi:Conceptos>
 <cfdi:Impuestos TotalImpuestosTrasladados="16.00"/>
 <cfdi:Complemento>
  <tfd:TimbreFiscalDigital Version="1.1" UUID="00000000-0000-0000-0000-000000000000"
   FechaTimbrado="2026-08-19T10:00:01"/>
 </cfdi:Complemento>
</cfdi:Comprobante>'''


class InspectTest(unittest.TestCase):
    def write(self, data: bytes) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "sample.xml"
        path.write_bytes(data)
        return path

    def test_extracts_and_checks_total(self) -> None:
        result = inspect(self.write(SAMPLE))
        self.assertTrue(result["documento"]["es_cfdi_4"])
        self.assertEqual(result["conteos"]["conceptos"], 1)
        self.assertEqual(result["timbre"]["uuid"], "00000000-0000-0000-0000-000000000000")
        self.assertTrue(result["cuadratura_inicial"]["coincide_exactamente"])

    def test_rejects_doctype(self) -> None:
        with self.assertRaisesRegex(ValueError, "DTD"):
            inspect(self.write(b'<!DOCTYPE x><Comprobante/>'))


if __name__ == "__main__":
    unittest.main()
