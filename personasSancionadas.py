import psycopg2
import psycopg2.extras
import updateControlLists
class personasSancionadas:

    def __init__(self):
        self.conexion =  psycopg2.connect(dbname="postgres", user="postgres", password="admin")
        self.cursor=self.conexion.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def abrir(self):
        conexion = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
        return conexion

    def updateControlLists(self):
        updateControlLists.executeScript()

    def identificacionesPersona(self,codigo):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select * from personas_sancionadas_identificaciones where id_person=%s"
        cursor.execute(sql, (codigo,))
        return cursor.fetchall()

    def personLikeIdentification(self,identification):
        identification=identification[0]
        cone=self.abrir()
        cursor=cone.cursor()
        sql = """
          SELECT personas_sancionadas.id,personas_sancionadas_identificaciones.numberidentification,personas_sancionadas.firstname, personas_sancionadas.lastname, personas_sancionadas.typecontrol
            FROM personas_sancionadas_identificaciones
            LEFT JOIN personas_sancionadas ON personas_sancionadas_identificaciones.id_person = personas_sancionadas.id
            WHERE personas_sancionadas_identificaciones.numberidentification ILIKE %s;

        """
        cursor.execute(sql, ('%' + identification + '%',))
        return cursor.fetchall()

    def personLikeName(self,Nombre):
        Nombre=Nombre[0]
        cone=self.abrir()
        cursor=cone.cursor()
        sql = """
          SELECT personas_sancionadas.id,personas_sancionadas_identificaciones.numberidentification,personas_sancionadas.firstname, personas_sancionadas.lastname, personas_sancionadas.typecontrol
            FROM personas_sancionadas_identificaciones
            LEFT JOIN personas_sancionadas ON personas_sancionadas_identificaciones.id_person = personas_sancionadas.id
            WHERE lastname ILIKE %s;

        """
        cursor.execute(sql, ('%' + Nombre + '%',))
        return cursor.fetchall()


    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select id, firstname, lastname, typecontrol from personas_sancionadas"
        cursor.execute(sql)
        return cursor.fetchall()

    def identificacionesPersona_json(self,codigo):
        sql="select * from personas_sancionadas_identificaciones where id_person=%s"
        self.cursor.execute(sql, (codigo,))
        return self.cursor.fetchall()

    def recuperar_todos_json(self):
        #cone=self.abrir()
        sql="select id, firstname, lastname, typecontrol from personas_sancionadas"
        self.cursor.execute(sql)
        persons=self.cursor.fetchall()
        for person in persons:
            print(person['id'])
            identifications=[]
            identifications.append(self.identificacionesPersona_json(person['id']))
            person["identifications"]=identifications
        return persons

    def recuperar_todos_jsonTest(self):
        sql = """
            SELECT p.id, p.firstname, p.lastname, p.typecontrol,
                pi.documentType, pi.numberIdentification, pi.country
            FROM personas_sancionadas_identificaciones pi
            RIGHT JOIN personas_sancionadas p ON p.id = pi.id_person
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        persons = {}
        for row in rows:
            id_person = row['id']
            if id_person not in persons:
                persons[id_person] = {
                    'id': id_person,
                    'firstname': row['firstname'],
                    'lastname': row['lastname'],
                    'typecontrol': row['typecontrol'],
                    'identifications': []
                }
            if row['documenttype'] is not None:
                persons[id_person]['identifications'].append({
                    'documentType': row['documenttype'],
                    'numberIdentification': row['numberidentification'],
                    'country': row['country']
                })
            else:
                persons[id_person]['identifications'].append(None)

        return list(persons.values())

