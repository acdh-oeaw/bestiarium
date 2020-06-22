'''
Namespaces used in the TEI XMLs
'''

XML_NS = u'http://www.w3.org/XML/1998/namespace'
TEI_NS = 'http://www.tei-c.org/ns/1.0'

NS = {'xml': XML_NS, 'tei': TEI_NS}


def get_attribute(attrib_name, namespace):
    return '{' + namespace + '}' + attrib_name


XML_ID = get_attribute('id', XML_NS)
