from json2xml import dicttoxml


class TestDict2xml:
    def test_dict2xml_with_namespaces(self):
        data = {'ns1:node1': 'data in namespace 1', 'ns2:node2': 'data in namespace 2'}
        namespaces = {'ns1': 'http://www.google.de/ns1', 'ns2': 'http://www.google.de/ns2'}
        result = dicttoxml.dicttoxml(data, attr_type=False, xml_namespaces=namespaces)
        assert b'<?xml version="1.0" encoding="UTF-8" ?>' \
               b'<root xmlns:ns1="http://www.google.de/ns1" xmlns:ns2="http://www.google.de/ns2">' \
               b'<ns1:node1>data in namespace 1</ns1:node1>' \
               b'<ns2:node2>data in namespace 2</ns2:node2>' \
               b'</root>' == result

    def test_dict2xml_with_xmlns_namespaces(self):
        data = {'ns1:node1': 'data in namespace 1', 'ns2:node2': 'data in namespace 2'}
        namespaces = {'xmlns': "http://www.w3.org/1999/XSL/Transform"}
        result = dicttoxml.dicttoxml(obj=data, attr_type=False, xml_namespaces=namespaces)
        assert b'<?xml version="1.0" encoding="UTF-8" ?>' \
               b'<root xmlns="http://www.w3.org/1999/XSL/Transform">' \
               b'<ns1:node1>data in namespace 1</ns1:node1>' \
               b'<ns2:node2>data in namespace 2</ns2:node2>' \
               b'</root>' == result

    def test_dict2xml_with_xsi_location(self):
        data = {'bike': 'blue'}
        wrapper = 'vehicle'
        namespaces = {
            'xsi': {
                'schemaInstance': "http://www.w3.org/2001/XMLSchema-instance",
                'schemaLocation': "https://www.w3schools.com/note.xsd"
            }
        }
        result = dicttoxml.dicttoxml(data, custom_root=wrapper, xml_namespaces=namespaces, attr_type=False)
        print(result)
        assert b'<?xml version="1.0" encoding="UTF-8" ?>' \
               b'<vehicle xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
               b'xsi:schemaLocation="https://www.w3schools.com/note.xsd">' \
               b'<bike>blue</bike>' \
               b'</vehicle>' == result

    def test_dict2xml_xsi_xmlns(self):
        data = {'bike': 'blue'}
        wrapper = 'vehicle'
        xml_namespace = {
            'xsd': "https://www.w3schools.com/note.xsd",
            'xmlns': "http://www.google.de/ns1",
            'xsi': {
                'schemaInstance': "http://www.w3.org/2001/XMLSchema-instance",
                'schemaLocation': "https://www.w3schools.com"
            },

        }
        result = dicttoxml.dicttoxml(data, custom_root=wrapper, xml_namespaces=xml_namespace,
                                     attr_type=False).decode()
        print(result)
        assert '<?xml version="1.0" encoding="UTF-8" ?>' \
            '<vehicle xmlns:xsd="https://www.w3schools.com/note.xsd" xmlns="http://www.google.de/ns1" ' \
               '' \
               '' \
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://www.w3schools.com">' \
            '<bike>blue</bike></vehicle>' == result

    def test_dict2xml_with_flat(self):
        data = {'flat_list@flat': [1, 2, 3], 'non_flat_list': [4, 5, 6]}
        result = dicttoxml.dicttoxml(data, attr_type=False)
        assert b'<?xml version="1.0" encoding="UTF-8" ?>' \
            b'<root><item>1</item><item>2</item><item>3</item>' \
            b'<non_flat_list><item>4</item><item>5</item><item>6</item></non_flat_list>' \
            b'</root>' == result

    def test_dict2xml_omit_list(self):
        obj = {'list': [
            {'bike': 'blue'},
            {'wheel': 'black'}
        ]
        }
        dicttoxml.dicttoxml(obj, root=False, attr_type=False, item_wrap=False)
        assert b'<list><bike>blue</bike><wheel>black</wheel></list>'

    def test_dict2xml_with_val_and_custom_attr(self):
        # in order to use @attr in non-dict objects, we need to lift into a dict and combine with @val as key
        data = {'list1': [1, 2, 3], 'list2': {'@attrs': {'myattr1': 'myval1', 'myattr2': 'myval2'}, '@val': [4, 5, 6]}}
        result = dicttoxml.dicttoxml(data, attr_type=False)
        assert b'<?xml version="1.0" encoding="UTF-8" ?>' \
               b'<root><list1><item>1</item><item>2</item><item>3</item></list1>' \
               b'<list2 myattr1="myval1" myattr2="myval2"><item>4</item><item>5</item><item>6</item></list2>' \
               b'</root>' == result

    def test_dict2xml_with_ampersand(self):
        dict_without_attrs = {'Bicycles': 'Wheels & Steers'}
        root = False
        attr_type = False
        result = dicttoxml.dicttoxml(
            dict_without_attrs, root=root, attr_type=attr_type).decode('UTF-8')
        assert '<Bicycles>Wheels &amp; Steers</Bicycles>' == result

    def test_dict2xml_with_ampsersand_and_attrs(self):
        dict_with_attrs = {'Bicycles': {'@attrs': {'xml:lang': 'nl'}, '@val': 'Wheels & Steers'}}
        root = False
        attr_type = False
        assert '<Bicycles xml:lang="nl">Wheels &amp; Steers</Bicycles>' == dicttoxml.dicttoxml(
            dict_with_attrs, root=root, attr_type=attr_type).decode('UTF-8')

    def test_make_id(self):
        make_id_elem = dicttoxml.make_id("li")
        assert 'li' in make_id_elem

    def test_get_unique_id(self):
        unique_id_elem_1 = dicttoxml.get_unique_id("li")
        unique_id_elem_2 = dicttoxml.get_unique_id("li")
        unique_id_elem_3 = dicttoxml.get_unique_id("li")
        unique_id_elem_4 = dicttoxml.get_unique_id("li")
        assert len(list(set({unique_id_elem_1, unique_id_elem_2, unique_id_elem_3, unique_id_elem_4}))) == 4

    def test_key_is_valid_xml(self):
        valid_key = "li"
        invalid_key = "/li"
        assert dicttoxml.key_is_valid_xml(valid_key) is True
        assert dicttoxml.key_is_valid_xml(invalid_key) is False

    def test_get_xml_type(self):
        assert dicttoxml.get_xml_type("abc") == "str"
        assert dicttoxml.get_xml_type(1) == "int"
        assert dicttoxml.get_xml_type(True) == "bool"
        assert dicttoxml.get_xml_type({}) == "dict"

    def test_is_primitive_type(self):
        assert dicttoxml.is_primitive_type(True) is True
        assert dicttoxml.is_primitive_type("abc") is True
        assert dicttoxml.is_primitive_type({}) is False

    def test_escape_xml(self):
        elem = "&"
        escaped_string = dicttoxml.escape_xml(elem)
        assert "&" != escaped_string
        assert "&amp;" == escaped_string

    def test_wrap_cdata(self):
        elem = "li"
        assert "CDATA" in dicttoxml.wrap_cdata(elem)

    def test_list_parent_elements(self):
        default_item_func = dicttoxml.default_item_func
        item = [{'frame_color': 'red'}, {'frame_color': 'green'}]
        conList = dicttoxml.convert_list(items=item, attr_type=False, cdata=False, ids=None,
                                         item_func=default_item_func, item_wrap=False, parent='Bike', list_headers=True)
        print(conList)
        assert '<Bike><frame_color>red</frame_color></Bike><Bike><frame_color>green</frame_color></Bike>' == conList

    def test_dict2xml_str_list_header(self):
        from json2xml.dicttoxml import dict2xml_str
        item_func = dicttoxml.default_item_func
        item = {'frame_color': 'red'}
        parent = 'Bike'
        xml_str = dict2xml_str(attr_type=False, attr={}, item=item, item_func=item_func,
                               cdata=False, item_name='item', item_wrap=False, parentIsList=True,
                               parent=parent, list_headers=True)

        assert '<Bike><frame_color>red</frame_color></Bike>' == xml_str

    def test_list_headers(self):
        dict = {"Bike": [
            {'frame_color': 'red'},
            {'frame_color': 'green'}
        ]}
        result = dicttoxml.dicttoxml(dict, root=False, item_wrap=False, attr_type=False, list_headers=True)
        print(result)
        assert b'<Bike><frame_color>red</frame_color></Bike><Bike><frame_color>green</frame_color></Bike>' == result

    def test_list_headers_nested(self):
        dict = {"transport": {
            "Bike": [
                {'frame_color': 'red'},
                {'frame_color': 'green'}
            ]}
        }
        result = dicttoxml.dicttoxml(dict, root=False, item_wrap=False, attr_type=False, list_headers=True)
        assert b'<transport><Bike><frame_color>red</frame_color></Bike>' \
            b'<Bike><frame_color>green</frame_color></Bike></transport>' == result

    def test_list_headers_root(self):
        dict = {"Bike": [
            {'frame_color': 'red'},
            {'frame_color': 'green'}
        ]}
        result = dicttoxml.dicttoxml(dict, root=True, item_wrap=False, attr_type=False, list_headers=True)
        assert b'<?xml version="1.0" encoding="UTF-8" ?><root>' \
            b'<Bike><frame_color>red</frame_color></Bike>' \
            b'<Bike><frame_color>green</frame_color></Bike></root>' == result

    def test_dict2xml_no_root(self):
        payload = {'mock': 'payload'}
        result = dicttoxml.dicttoxml(payload, attr_type=False, root=False)
        assert b'<mock>payload</mock>' == result

    def test_dict2xml_with_root(self):
        payload = {'mock': 'payload'}
        result = dicttoxml.dicttoxml(payload, attr_type=False)
        assert b'<?xml version="1.0" encoding="UTF-8" ?><root><mock>payload</mock></root>' == result

    def test_dict2xml_with_custom_root(self):
        payload = {'mock': 'payload'}
        result = dicttoxml.dicttoxml(payload, attr_type=False, custom_root="element")
        assert b'<?xml version="1.0" encoding="UTF-8" ?><element><mock>payload</mock></element>' == result

    def test_dict2xml_with_item_func(self):
        data = {'flat_list@flat': [1, 2, 3], 'non_flat_list': [4, 5, 6]}
        result = dicttoxml.dicttoxml(data, attr_type=False, item_func=lambda x: 'a')
        print(result)
        assert b'<?xml version="1.0" encoding="UTF-8" ?>' \
            b'<root><a>1</a><a>2</a><a>3</a><non_flat_list><a>4</a><a>5</a><a>6</a></non_flat_list>' \
            b'</root>' == result

    def test_dict2xml_with_item_func_issue_151(self):
        data = [{'x': [1]}]
        result = dicttoxml.dicttoxml(data, root=False, attr_type=False, item_func=lambda y: y+'item')
        print(result)
        assert b'<item><x><xitem>1</xitem></x></item>' == result

    def test_dict2xml_issue_151(self):
        data = [{'x': [1]}]
        result = dicttoxml.dicttoxml(data, root=False, attr_type=False)
        print(result)
        assert b'<item><x><item>1</item></x></item>' == result
