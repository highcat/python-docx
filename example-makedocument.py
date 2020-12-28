#!/usr/bin/env python
'''
This file makes an docx (Office 2007) file from scratch, showing off most of python-docx's features.

If you need to make documents from scratch, use this file as a basis for your work.

Part of Python's docx module - http://github.com/mikemaccana/python-docx
See LICENSE for licensing information.
'''
import shutil
from copy import deepcopy
from tempfile import TemporaryFile, mkdtemp
import docx as dx

if __name__ == '__main__':
    temp_dir = mkdtemp()

    # Default set of relationshipships - these are the minimum components of a document
    relationships = dx.relationshiplist()

    # Make a new document tree - this is the main part of a Word document
    document = dx.newdocument()
    
    # This xpath location is where most interesting content lives 
    docbody = document.xpath('/w:document/w:body', namespaces=dx.nsprefixes)[0]

    # Append two headings and a paragraph
    docbody.append(dx.heading('''Welcome to Python's docx module''',1)  )   
    docbody.append(dx.heading('Make and edit docx in 200 lines of pure Python',2))
    docbody.append(dx.paragraph('The module was created when I was looking for a Python support for MS Word .doc files on PyPI and Stackoverflow. Unfortunately, the only solutions I could find used:'))

    # Add a numbered list
    for point in ['''COM automation''','''.net or Java''','''Automating OpenOffice or MS Office''']:
        docbody.append(dx.paragraph(point,style='ListNumber'))
    docbody.append(dx.paragraph('''For those of us who prefer something simpler, I made docx.''')) 
    
    docbody.append(dx.heading('Making documents',2))
    docbody.append(dx.paragraph('''The docx module has the following features:'''))

    # Add some bullets
    for point in ['Paragraphs','Bullets','Numbered lists','Multiple levels of headings','Tables','Document Properties']:
        docbody.append(dx.paragraph(point,style='ListBullet'))

    docbody.append(dx.paragraph('Tables are just lists of lists, like this:'))
    # Append a table
    docbody.append(dx.table([['A1','A2','A3'],['B1','B2','B3'],['C1','C2','C3']]))

    docbody.append(dx.heading('Editing documents',2))
    docbody.append(dx.paragraph('Thanks to the awesomeness of the lxml module, we can:'))
    for point in ['Search and replace',
                  'Extract plain text of document',
                  'Add and delete items anywhere within the document']:
        docbody.append(dx.paragraph(point, style='ListBullet'))

    # Add an image
    relationships, picpara = dx.picture(
        relationships,
        'image1.png',
        'This is a test description',
        temp_dir = temp_dir)
    docbody.append(picpara)

    docbody.append(dx.paragraph([
        ('hello', ''),
        ('2', [dx.makeelement('vertAlign', attributes={'val': 'superscript'})]),
        ]))

    # Append a table with special properties and cells
    spec_cell = dx.paragraph([
        ('2', [dx.makeelement('vertAlign', attributes={'val': 'superscript'})]),
        ])
    t_prop_margin = dx.makeelement('tblCellMar')
    for margin_type in ['top', 'left', 'right', 'bottom']:
        t_prop_margin.append(dx.makeelement(margin_type, attributes={'w': '0', 'type': 'dxa'}))
    CELL_SIZE = 12*30 # twenties of a point
    docbody.append(dx.table([['A1',
                              {'content': spec_cell, 'style': {'vAlign': {'val': 'top'},
                                                               'shd': {'fill': '777777'}}},
                              ('A3', 'ttt')],
                             ['B1','B2','B3'],
                             ['C1','C2','C3']],
        heading=False,
        colw=[CELL_SIZE]*3,
        cwunit='dxa', # twenties of a point
        borders={'all': {'color': 'AAAAAA'}},
        celstyle=[{'align': 'center', 'vAlign': {'val': 'center'}}]*3,
        rowstyle={'height': CELL_SIZE},
        table_props={'jc': {'val': 'center'},
                     '__margin__': t_prop_margin,
                     },
    ))
    
    # Search and replace
    print('Searching for something in a paragraph ...',)
    if dx.search(docbody, 'the awesomeness'):
         print('found it!')
    else:
         print('nope.')
         
    print('Searching for something in a heading ...',)
    if dx.search(docbody, '200 lines'):
         print('found it!')
    else:
         print('nope.')
    
    print('Replacing ...',)
    docbody = dx.replace(docbody,'the awesomeness','the goshdarned awesomeness') 
    print('done.')

    # Add a pagebreak
    docbody.append(dx.pagebreak(type='page', orient='portrait'))

    docbody.append(dx.heading('Ideas? Questions? Want to contribute?',2))
    docbody.append(dx.paragraph('''Email <python.docx@librelist.com>'''))

    # Create our properties, contenttypes, and other support files
    coreprops = dx.coreproperties(
        title='Python docx demo',
        subject='A practical example of making docx from Python',
        creator='Mike MacCana',
        keywords=['python','Office Open XML','Word'])
    appprops = dx.appproperties()
    my_contenttypes = dx.contenttypes()
    my_websettings = dx.websettings()
    my_wordrelationships = dx.wordrelationships(relationships)
    
    # Save our document
    temp_file = TemporaryFile()
    dx.savedocx(
        document,
        coreprops,
        appprops,
        my_contenttypes,
        my_websettings,
        my_wordrelationships,
        # can be either file-like object, or file name:
        output=temp_file,
        temp_dir=temp_dir,
        )
    temp_file.seek(0)
    print("temp dir is:", temp_dir)
    shutil.rmtree(temp_dir)
    print("temp dir deleted")

    f = open('example.docx', 'w+b')
    f.write(temp_file.read())
    f.close()
    
