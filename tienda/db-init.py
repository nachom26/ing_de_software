#SOLO EJECUTAR CUANDO SE INICIALICE UNA NUEVA BASE DE DATOS

import psycopg2
from psycopg2 import sql
import sys

# Define los datos de regiones y comunas
RegionesYcomunas = {
    "regiones": [
        {
            "NombreRegion": "Arica y Parinacota",
            "comunas": ["Arica", "Camarones", "Putre", "General Lagos"]
        },
        {
            "NombreRegion": "Tarapacá",
            "comunas": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"]
        },
        {
            "NombreRegion": "Antofagasta",
            "comunas": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"]
        },
        {
            "NombreRegion": "Atacama",
            "comunas": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"]
        },
        {
            "NombreRegion": "Coquimbo",
            "comunas": [
                "La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña",
                "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá",
                "Monte Patria", "Punitaqui", "Río Hurtado"
            ]
        },
        {
            "NombreRegion": "Valparaíso",
            "comunas": [
                "Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví",
                "Quintero", "Viña del Mar", "Isla de Pascua", "Los Andes", "Calle Larga",
                "Rinconada", "San Esteban", "La Ligua", "Cabildo", "Papudo", "Petorca",
                "Zapallar", "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales",
                "San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo",
                "Santo Domingo", "San Felipe", "Catemu", "Llaillay", "Panquehue",
                "Putaendo", "Santa María", "Quilpué", "Limache", "Olmué", "Villa Alemana"
            ]
        },
        {
            "NombreRegion": "Región del Libertador Gral. Bernardo O’Higgins",
            "comunas": [
                "Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros",
                "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo",
                "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente",
                "Pichilemu", "La Estrella", "Litueche", "Marchihue", "Navidad",
                "Paredones", "San Fernando", "Chépica", "Chimbarongo", "Lolol",
                "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"
            ]
        },
        {
            "NombreRegion": "Región del Maule",
            "comunas": [
                "Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco",
                "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes",
                "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina",
                "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén",
                "Linares", "Colbún", "Longaví", "Parral", "Reviro", "San Javier",
                "Villa Alegre", "Yerbas Buenas"
            ]
        },
        {
            "NombreRegion": "Región del Biobío",
            "comunas": [
                "Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui",
                "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano",
                "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo",
                "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco",
                "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco",
                "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel",
                "Alto Biobío", "Chillán", "Bulnes", "Cobquecura", "Coelemu",
                "Coihueco", "Chillán Viejo", "El Carmen", "Ninhue", "Ñiquén",
                "Pemuco", "Pinto", "Portezuelo", "Quillón", "Quirihue", "Ránquil",
                "San Carlos", "San Fabián", "San Ignacio", "San Nicolás", "Treguaco",
                "Yungay"
            ]
        },
        {
            "NombreRegion": "Región de la Araucanía",
            "comunas": [
                "Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino",
                "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial",
                "Padre las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra",
                "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol",
                "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay",
                "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"
            ]
        },
        {
            "NombreRegion": "Región de Los Ríos",
            "comunas": [
                "Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina",
                "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco",
                "Río Bueno"
            ]
        },
        {
            "NombreRegion": "Región de Los Lagos",
            "comunas": [
                "Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar",
                "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro",
                "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón",
                "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay",
                "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa",
                "San Pablo", "Chaitén", "Futaleufú", "Hualaihué", "Palena"
            ]
        },
        {
            "NombreRegion": "Región Aisén del Gral. Carlos Ibáñez del Campo",
            "comunas": [
                "Coihaique", "Lago Verde", "Aisén", "Cisnes", "Guaitecas",
                "Cochrane", "O’Higgins", "Tortel", "Chile Chico", "Río Ibáñez"
            ]
        },
        {
            "NombreRegion": "Región de Magallanes y de la Antártica Chilena",
            "comunas": [
                "Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio",
                "Cabo de Hornos (Ex Navarino)", "Antártica", "Porvenir",
                "Primavera", "Timaukel", "Natales", "Torres del Paine"
            ]
        },
        {
            "NombreRegion": "Región Metropolitana de Santiago",
            "comunas": [
                "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque",
                "Estación Central", "Huechuraba", "Independencia", "La Cisterna",
                "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes",
                "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú",
                "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia",
                "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca",
                "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto",
                "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil",
                "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla",
                "Alhué", "Curacaví", "María Pinto", "San Pedro", "Talagante",
                "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"
            ]
        }
    ]
}

# Configuración de la conexión a PostgreSQL
db_config = {
    'host': 'localhost',             # Cambia si es necesario
    'port': '5432',                  # Cambia si es necesario
    'dbname': 'tienda',    # Reemplaza con el nombre de tu base de datos
    'user': 'tienda',            # Reemplaza con tu usuario
    'password': '2643'      # Reemplaza con tu contraseña
}

def insertar_datos(regiones_y_comunas, config):
    try:
        # Establecer la conexión
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        conn.set_client_encoding('UTF8')

        # Iniciar una transacción
        conn.autocommit = False
        
        # Insertar regiones y almacenar sus IDs
        region_id_map = {}
        insert_region_query = sql.SQL("INSERT INTO regiones (nombre) VALUES (%s) RETURNING id;")
        
        print("Insertando regiones...")
        for region in regiones_y_comunas['regiones']:
            nombre_region = region['NombreRegion']
            cursor.execute(insert_region_query, (nombre_region,))
            region_id = cursor.fetchone()[0]
            region_id_map[nombre_region] = region_id
            print(f"  - Insertada región '{nombre_region}' con ID {region_id}")
        
        # Insertar comunas
        insert_comuna_query = sql.SQL("INSERT INTO comunas (nombre, id_region) VALUES (%s, %s);")
        
        print("Insertando comunas...")
        for region in regiones_y_comunas['regiones']:
            nombre_region = region['NombreRegion']
            id_region = region_id_map[nombre_region]
            comunas = region['comunas']
            for comuna in comunas:
                cursor.execute(insert_comuna_query, (comuna, id_region))
                print(f"    - Insertada comuna '{comuna}' en región ID {id_region}")
        
        # Confirmar la transacción
        conn.commit()
        print("Datos insertados exitosamente.")
    
    except Exception as e:
        # En caso de error, revertir la transacción
        if 'conn' in locals():
            conn.rollback()
        print("Ocurrió un error durante la inserción de datos:", e)
        sys.exit(1)
    
    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    insertar_datos(RegionesYcomunas, db_config)
