import requests 
from lxml import etree
import psycopg2



def main():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    cursor = conn.cursor()
    table_creation = '''
    CREATE TABLE IF NOT EXISTS test (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        lastname TEXT NOT NULL
    )
    '''
    cursor.execute(table_creation)
    
    url = "https://scsanctions.un.org/resources/xml/sp/consolidated.xml"

    response = requests.get(url)

    data=[]

    if response.status_code == 200:
        xml_content = response.content
        root = etree.fromstring(xml_content)

        print("Nombre de la etiqueta raíz:", root)
        
        for persona in root.findall('.//INDIVIDUALS/'):
            person={}
            first_name = persona.find('FIRST_NAME').text if persona.find('FIRST_NAME') is not None else "NO TIENE PRIMER NOMBRE OMG"
            second_name = persona.find('SECOND_NAME').text if persona.find('SECOND_NAME') is not None else "NO TIENE SEGUNDO NOMBRE OMG"
            #print("First Name:", first_name)
            #print("Second Name:", second_name)
            person['firstName']=first_name
            person['lastName']=second_name
            #for document in persona.findall('.//INDIVIDUAL_DOCUMENT'):
                #for individualDocument in document.findall('.//NUMBER'):
                    #print("Document NUMBER:",individualDocument.text)
                    #person['ci']=individualDocument.text
            data.append(person)  
        for datos in data:
            cursor.execute("INSERT INTO test (name, lastname) VALUES (%s, %s)",(datos['firstName'], datos['lastName']))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        print("Error al obtener el documento XML:", response.status_code)
    print(data)


    #cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

if __name__== '__main__':
    main()