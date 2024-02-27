import requests 
from lxml import etree
import psycopg2



def main():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
    cursor = conn.cursor()
    table_creation = '''
    CREATE TABLE IF NOT EXISTS personas_sancionadas (
        id SERIAL PRIMARY KEY,
        firstname TEXT NOT NULL,
        lastname TEXT
    );

    CREATE TABLE IF NOT EXISTS personas_sancionadas_identificaciones (
        id SERIAL PRIMARY KEY,
        documentType TEXT,
        numberIdentification TEXT,
        country TEXT,
        id_person INT,
        FOREIGN KEY (id_person) REFERENCES personas_sancionadas(id)
    );
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
            first_name = persona.find('FIRST_NAME').text if persona.find('FIRST_NAME') is not None else ""
            second_name = persona.find('SECOND_NAME').text if persona.find('SECOND_NAME') is not None else ""
            nationality = persona.find('NATIONALITY/VALUE').text if persona.find('NATIONALITY') is not None else "No Info"
            #print(nationality)
            lastDataUpdate=None
            for day_updates in persona.findall('.//LAST_DAY_UPDATED'):
                lastDataUpdate=day_updates.text
            

            #print("First Name:", first_name)
            #print("Second Name:", second_name)
            person['firstName']=first_name
            person['lastName']=second_name
            person['nationality']=nationality
            identifications=[]
            #print("---------------")
            #print(persona.findall('INDIVIDUAL_DOCUMENT'))
            for document in persona.findall('INDIVIDUAL_DOCUMENT'):
                #print(document)
                person_document={}
                tipo_documento = document.find("TYPE_OF_DOCUMENT")
                try:
                    person_document['typeDocument'] = tipo_documento.text 
                except:
                    continue

                tipo_documento = document.find("NUMBER")
                try:
                     person_document['numberDocument'] = tipo_documento.text 
                except:
                    person_document['numberDocument'] = "None :p"
                tipo_documento = document.find("ISSUING_COUNTRY")
                try:
                     person_document['countryDocument'] = tipo_documento.text 
                except:
                    person_document['countryDocument'] = "No Especified"
                
            
                identifications.append(person_document)
            person['identifications']=identifications
            data.append(person)  
        
        for datos in data:
            #print(datos)
            cursor.execute("INSERT INTO personas_sancionadas (firstname, lastname) VALUES (%s, %s) RETURNING id",(datos['firstName'], datos['lastName']))
            person_id = int(cursor.fetchone()[0])
            if datos['identifications']:
                for identificacion in datos['identifications']:
                     #print(identificacion)
                     cursor.execute("INSERT INTO personas_sancionadas_identificaciones (documentType, numberIdentification, country, id_person) VALUES (%s, %s, %s, %s)", (identificacion['typeDocument'], identificacion['numberDocument'], identificacion['countryDocument'], person_id))
        conn.commit()
        cursor.close()
        conn.close()
    else:
        print("Error al obtener el documento XML:", response.status_code)
    #print(data)


    #cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

if __name__== '__main__':
    main()