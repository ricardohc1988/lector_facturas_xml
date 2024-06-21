import xml.etree.ElementTree as ET
import datetime
import re

class LeerFactura:
    """
    Clase para leer y procesar datos de una factura en formato XML.
    """
    def __init__(self, nombre_factura: str):
        """
        Inicializa la instancia de la clase LeerFactura.

        Args:
        - nombre_factura (str): Nombre del archivo de factura en formato XML.
                               Debe tener la extensión '.xml'.

        Raises:
        - ValueError: Si el archivo no tiene la extensión '.xml' o no es
                      un archivo de factura válido.
        """
        try:
            assert nombre_factura.endswith('.xml'), "El archivo no tiene la extensión '.xml'."
            self.root = ET.parse(nombre_factura).getroot()
            assert self.root.tag == '{http://www.sat.gob.mx/cfd/4}Comprobante', "El archivo no es un archivo de factura válido."
        except ET.ParseError as e:
            raise ValueError(f"Error al parsear el archivo XML: {e}")
        except AssertionError as e:
            raise ValueError(f"Error de validación: {e}")

    def obtener_datos_generales(self):
        """
        Obtiene los datos generales de la factura.

        Returns:
        - dict: Diccionario con los datos generales de la factura, incluyendo
                fecha y número de factura.
        """
        try:
            generales = {}
            fecha_str = self.root.attrib.get('Fecha', '')
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S')
            generales['fecha'] = fecha.strftime('%d/%m/%Y')
            generales['factura'] = self.root.attrib.get('Folio', '')
            return generales
        except Exception as e:
            print(f'Error: {e}')

    def obtener_datos_receptor(self):
        """
        Obtiene los datos del receptor de la factura.

        Returns:
        - dict: Diccionario con los datos del receptor, incluyendo nombre y RFC.
        """
        datos_receptor = self.root.find('{http://www.sat.gob.mx/cfd/4}Receptor')
        receptor = {}
        receptor['nombre'] = datos_receptor.get('Nombre', '')
        receptor['rfc'] = datos_receptor.get('Rfc', '')

        return receptor

    def obtener_datos_conceptos(self):
        """
        Obtiene los datos de los conceptos (productos) de la factura.

        Returns:
        - list: Lista de diccionarios, cada uno representando un concepto
                con sus detalles como código, descripción, cantidad, etc.
        """
        datos_conceptos = self.root.find('{http://www.sat.gob.mx/cfd/4}Conceptos')
        conceptos = []
        if datos_conceptos is not None:
            for elemento in datos_conceptos.iter('{http://www.sat.gob.mx/cfd/4}Concepto'):
                concepto = {
                    'codigo': elemento.get('NoIdentificacion', ''),
                    'descripcion': elemento.get('Descripcion', ''),
                    'cantidad': int(float(elemento.get('Cantidad', '0'))),
                    'valor_u': elemento.get('ValorUnitario', ''),
                    'subtotal': elemento.get('Importe', ''),
                    'iva': float(elemento.get('Importe', '0')) * 0.16,
                    'ret_isr': float(elemento.get('Importe', '0')) * 0.012500,
                }
                concepto['total'] = float(concepto['subtotal']) + concepto['iva'] - concepto['ret_isr']
                conceptos.append(concepto)
        return conceptos
    
    def obtener_datos_addenda(self):
        """
        Obtiene los datos adicionales (Addenda) de la factura, específicamente
        el número de pedido y número de remisión si están disponibles.

        Returns:
        - dict or None: Diccionario con los números de pedido y remisión, o None
                        si no se encontraron en la Addenda.
        """
        addenda = self.root.find('{http://www.sat.gob.mx/cfd/4}Addenda')
        addenda_info = {'numero_pedido': None, 'numero_remision': None}
        
        if addenda is not None:
            addenda_informativa = addenda.find('.//pac4gf:addendaInformativa', namespaces={'pac4gf': 'http://www.4gfactura.com/'})
            if addenda_informativa is not None:
                info_texto = addenda_informativa.find('./pac4gf:informativa', namespaces={'pac4gf': 'http://www.4gfactura.com/'}).attrib.get('text', '')
                info_elementos = info_texto.split('NO.')
                
                numero_pedido = next((re.findall(r'\b\d{10}\b', elemento) for elemento in info_elementos if 'PEDIDO:' in elemento), None)
                numero_remision = next((re.findall(r'\b\d{1,2}\b', elemento) for elemento in info_elementos if 'REMISIÓN:' in elemento), None)

                addenda_info = {'numero_pedido': numero_pedido, 'numero_remision': numero_remision}

        return addenda_info if addenda_info['numero_pedido'] or addenda_info['numero_remision'] else None

    def datos_completos(self):
        """
        Obtiene todos los datos disponibles de la factura.

        Returns:
        - dict: Diccionario con todos los datos obtenidos de la factura,
                incluyendo datos generales, receptor, conceptos y datos de la Addenda.
        """
        try:
            generales = self.obtener_datos_generales()
            receptor = self.obtener_datos_receptor()
            conceptos = self.obtener_datos_conceptos()
            addenda_info = self.obtener_datos_addenda()

            datos = {
                'fecha': generales['fecha'],
                'factura': generales['factura'],
                'nombre': receptor['nombre'],
                'rfc': receptor['rfc'],
                'productos': conceptos,
                'numero_pedido': addenda_info['numero_pedido'],
                'numero_remision': addenda_info['numero_remision']
            }

            return datos
        except Exception as e:
            raise ValueError(f"Error al obtener datos de factura: {e}")
    