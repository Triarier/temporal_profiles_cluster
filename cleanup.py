import lxml.etree as ET
import lxml

with open('data1.xes') as f:
    xml = f.read()

tree = ET.XML(xml.encode('ascii'))

print(tree.tag)


pr = None
pn = None
pd = None
ns = {"xes": "http://www.xes-standard.org/"}
for target in tree.xpath("//xes:event", namespaces=ns):
    da = False
    for x in target:
        if x.get("key")== "concept:name":
            da =True
    if not da:
        target.getparent().remove(target)
        continue

    n = target.xpath("xes:string[@key='concept:name']/@value", namespaces=ns)
    d = target.xpath("xes:date[@key='time:timestamp']/@value", namespaces=ns)
    if pr is not None:
        if n==pn and d==pd:
            target.getparent().remove(target)
        else:
            pr = target
            pn = n
            pd = d
    else:
        pr = target
        pn = n
        pd = d


#print(lxml.etree.tostring(tree,  xml_declaration=True))
with open("cleaned_long.xes", "w") as text_file:
    text_file.write(lxml.etree.tostring(tree,  xml_declaration=True).decode("utf-8"))

