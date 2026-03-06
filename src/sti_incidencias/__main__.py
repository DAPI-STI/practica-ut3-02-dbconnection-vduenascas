"""
Punto de entrada principal para pruebas manuales.
"""
from .db import get_connection
from .tecnicos import listar_tecnicos
from .equipos import listar_equipos
from .incidencias import listar_incidencias_activas

def main():
    print("=== SISTEMA DE INCIDENCIAS ===\n")
    
    try:
        conn = get_connection()
        print("✅ Conectado a la base de datos\n")
        
        # Mostrar técnicos
        print("📋 TÉCNICOS:")
        tecnicos = listar_tecnicos(conn)
        if tecnicos:
            for t in tecnicos:
                print(f"  {t['id']}: {t['nombre']} - {t['email']}")
        else:
            print("  No hay técnicos registrados")
        
        # Mostrar equipos
        print("\n📋 EQUIPOS:")
        equipos = listar_equipos(conn)
        if equipos:
            for e in equipos:
                print(f"  {e['id']}: {e['nombre']} - {e.get('tipo', 'Sin tipo')}")
        else:
            print("  No hay equipos registrados")
        
        # Mostrar incidencias activas
        print("\n📋 INCIDENCIAS ACTIVAS:")
        incidencias = listar_incidencias_activas(conn)
        if incidencias:
            for i in incidencias:
                print(f"  {i['id']}: {i['descripcion'][:50]}... - {i['prioridad']} - {i['estado']}")
        else:
            print("  No hay incidencias activas")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()