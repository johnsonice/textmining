import logging
import time
import re
import xml.etree.cElementTree as ET
import lxml.etree
from xml_server_connect import Connect_SQL_Server

logger = logging.getLogger("connect")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

SKIP_LIST = set(['fig', 'table-wrap', 'boxlabel', 'attrib', 'sup', 'graphic'])

def extract_text_from_report(xmlstring):
    root = lxml.etree.fromstring(xmlstring.encode('utf8'))
    nodes = root.findall('./body')
    textList = []
    for node in nodes:
        process_node(node, textList=textList, content=[])
        
    return textList

#BFS to parse the xml tress
def process_node(node, textList, content):
    if node.tag in SKIP_LIST:
        return
    #import pdb;pdb.set_trace()
    if node.tag == 'title':
        content.append('<Title> ')

    if node.text is not None and len(node.text) != 0:
        content.append(node.text)
    
    children = node.getchildren()
    for child in children:
        process_node(child, textList, content)
    
    if node.tail is not None and len(node.tail) != 0:
        content.append(node.tail + ' ')
    
    if node.tag == 'p':
        textList.append("".join(content))
        content[:] = []

    if node.tag == 'title':
        content.append('.')
        textList.append("".join(content))
        content[:] = []
    return

if __name__ == '__main__':
    query = '''select d.*, p.Country, p.Title
                from [IMF_EPUBS].[dbo].[DOCUMENT] as d left join 
                  [IMF_EPUBS].[dbo].[PUBLICATION] as p 
                  on d.SeriesNumber=p.SeriesNumber
                where p.Title like '%[Aa][Rr][Tt][Ii][Cc][Ll][Ee]_IV%' 
                      and d.PublisherId like '%A001%' 
                order by SeriesNumber'''
    imfReportServer = Connect_SQL_Server()
    imfReportServer.Execute_Query(query, name='Article IV')
    rows = imfReportServer.cursor.fetchall()
    with open('article_IV_corpus.txt', 'w', encoding='utf8') as f:
        for row in rows:
            try:
                contents = extract_text_from_report(row.Content)
                f.writelines('\n'.join(contents))
                f.writeline('\n')
            except:
                logger.warning('%s cannot be parsed by xml'%(row.Title))
                continue
            
    
