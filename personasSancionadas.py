import psycopg2

class personasSancionadas:

    def abrir(self):
        conexion = psycopg2.connect(dbname="postgres", user="postgres", password="admin")
        return conexion
    
    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select firstname, lastname from personas_sancionadas where firstname=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def identificacionesPersona(self,codigo):
        print("Codigo: ",codigo)
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select * from personas_sancionadas_identificaciones where id_person=%s"
        cursor.execute(sql, (codigo,))
        return cursor.fetchall()

    def personLikeIdentification(self,identification):
        print("Idenfificacion TEST=> ",identification[0])
        identification=identification[0]
        cone=self.abrir()
        cursor=cone.cursor()
        sql = """
          SELECT personas_sancionadas.id,personas_sancionadas_identificaciones.numberidentification,personas_sancionadas.firstname, personas_sancionadas.lastname, personas_sancionadas.typecontrol
            FROM personas_sancionadas_identificaciones
            LEFT JOIN personas_sancionadas ON personas_sancionadas_identificaciones.id_person = personas_sancionadas.id
            WHERE personas_sancionadas_identificaciones.numberidentification LIKE %s;

        """
        cursor.execute(sql, ('%' + identification + '%',))
        return cursor.fetchall()

    def personByIdentification(self,identification):
        print("Codigo: ",identification)
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select * from personas_sancionadas_identificaciones where numberidentification=%s"
        cursor.execute(sql, (identification,))
        identificationPerson=cursor.fetchone()
        if(identificationPerson):
            identificationPerson=identificationPerson[4]
            sql="select * from personas_sancionadas where id=%s"
            cursor.execute(sql, (identificationPerson,))
            return cursor.fetchone()
        else:
            return None
        

    def recuperar_todos(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select * from personas_sancionadas"
        cursor.execute(sql)
        return cursor.fetchall()