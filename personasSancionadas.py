import psycopg2
import updateControlLists
class personasSancionadas:

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