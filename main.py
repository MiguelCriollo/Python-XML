import requests 
from lxml import etree
import xml.etree.ElementTree as ET
from personasSancionadas import personasSancionadas
from mainMenu import mainMenu
conexion=personasSancionadas()
def databaseStart():
    conn = conexion.abrir()
    cursor = conn.cursor()
    table_creation = '''
    DROP TABLE IF EXISTS personas_sancionadas, personas_sancionadas_identificaciones CASCADE;

    CREATE TABLE IF NOT EXISTS personas_sancionadas (
        id SERIAL PRIMARY KEY,
        firstname TEXT NOT NULL,
        typeControl VARCHAR(10),
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
    return cursor,conn

def onuSanctionsDB(cursor):
    url = "https://scsanctions.un.org/resources/xml/sp/consolidated.xml"

    response = requests.get(url)

    data=[]

    if response.status_code == 200:
        xml_content = response.content
        root = etree.fromstring(xml_content)

        print("Nombre de la etiqueta raíz:", root)
        
        for persona in root.findall('.//INDIVIDUALS/'):
            person={}

            person['firstName']=persona.find('FIRST_NAME').text if persona.find('FIRST_NAME') is not None else ""
            person['lastName']=persona.find('SECOND_NAME').text if persona.find('SECOND_NAME') is not None else ""
            person['nationality']=persona.find('NATIONALITY/VALUE').text if persona.find('NATIONALITY') is not None else "No Info"
            identifications=[]

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
            cursor.execute("INSERT INTO personas_sancionadas (firstname, lastname, typeControl) VALUES (%s, %s, %s) RETURNING id",(datos['firstName'], datos['lastName'], "ONU"))
            person_id = int(cursor.fetchone()[0])
            if datos['identifications']:
                for identificacion in datos['identifications']:
                     #print(identificacion)
                     cursor.execute("INSERT INTO personas_sancionadas_identificaciones (documentType, numberIdentification, country, id_person) VALUES (%s, %s, %s, %s)", (identificacion['typeDocument'], identificacion['numberDocument'], identificacion['countryDocument'], person_id))
        print("Onu sanctions list successful")
    else:
        print("Error al obtener el documento XML:", response.status_code)

def ofacSanctions(cursor):
    url = "https://www.treasury.gov/ofac/downloads/sdn.xml"

    response = requests.get(url)

   

    if response.status_code == 200:
        data=[]
        print("Content Succesfuly Downloaded")
        xml_content = response.content
        root = ET.fromstring(xml_content)
        dn='.//{http://tempuri.org/sdnList.xsd}'
        sdn_entries = root.findall(dn+'sdnEntry')
        for sdn_entry in sdn_entries:
            person={}
            person['lastName']=sdn_entry.find(dn+'lastName').text
            person['firstName']= sdn_entry.find(dn+'firstName').text if sdn_entry.find(dn+'firstName') is not None else ""
            ids=sdn_entry.find(dn+'idList') if sdn_entry.find(dn+'idList') is not None else None
            identifications=[]
            if(ids):
                for id in ids:
                    identification={}
                    identification["typeDocument"]=id.find(dn+'idType').text if id.find(dn+'idType') is not None else "No specified"
                    identification["numberDocument"]=id.find(dn+'idNumber').text if id.find(dn+'idNumber') is not None else "No specified"
                    identification["countryDocument"]=id.find(dn+'idCountry').text if id.find(dn+'idCountry') is not None else "No specified"
                    identifications.append(identification)
            person['identifications']=identifications
            data.append(person)
        for datos in data:
            #print(datos)
            cursor.execute("INSERT INTO personas_sancionadas (firstname, lastname, typeControl) VALUES (%s, %s, %s) RETURNING id",(datos['firstName'], datos['lastName'], "OFAC"))
            person_id = int(cursor.fetchone()[0])
            if datos['identifications']:
                for identificacion in datos['identifications']:
                    #print(identificacion)
                    cursor.execute("INSERT INTO personas_sancionadas_identificaciones (documentType, numberIdentification, country, id_person) VALUES (%s, %s, %s, %s)", (identificacion['typeDocument'], identificacion['numberDocument'], identificacion['countryDocument'], person_id))
        print("OFAC sanctions list successful")
    else:
        print("There has been an error idk")
            

def main():
    #mainMenu()
    cursor,conn=databaseStart()
    onuSanctionsDB(cursor)
    ofacSanctions(cursor)
    conn.commit()
    cursor.close()
    conn.close()

if __name__== '__main__':
    main()