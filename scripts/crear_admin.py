"""
Script utilitario para crear o promover un usuario a rol 'admin' en el CESFAM.

Uso:
    python scripts/crear_admin.py --rut 11111111-1 --nombre "Administrador CESFAM" --pin 1234
    python scripts/crear_admin.py  (modo interactivo)
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path al ejecutar directamente: python scripts/crear_admin.py
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy import select
from core.database import AsyncSessionLocal
from core.security import hash_pin
from features.usuarios.models import Usuario
from features.usuarios.schemas import normalizar_rut


async def crear_o_promover_admin(rut_raw: str, nombre: str, pin: str, email: str | None = None):
    rut = normalizar_rut(rut_raw)
    if len(pin) != 4 or not pin.isdigit():
        print("❌ Error: El PIN debe contener exactamente 4 dígitos numéricos.")
        sys.exit(1)

    pin_hasheado = hash_pin(pin)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Usuario).where(Usuario.rut == rut))
        usuario = result.scalar_one_or_none()

        if usuario:
            usuario.rol = "admin"
            usuario.pin_hash = pin_hasheado
            if nombre:
                usuario.nombre = nombre
            if email:
                usuario.email = email
            await session.commit()
            print(f"✅ Usuario existente con RUT {rut} promovido exitosamente a rol 'admin'.")
        else:
            nuevo_admin = Usuario(
                rut=rut,
                nombre=nombre or "Administrador",
                pin_hash=pin_hasheado,
                rol="admin",
                email=email,
            )
            session.add(nuevo_admin)
            await session.commit()
            print(f"✅ Administrador creado exitosamente con RUT {rut} y rol 'admin'.")


def main():
    parser = argparse.ArgumentParser(description="Crear o promover administrador para el CESFAM")
    parser.add_argument("--rut", help="RUT del administrador (ej. 11111111-1)")
    parser.add_argument("--nombre", help="Nombre del administrador")
    parser.add_argument("--pin", help="PIN numérico de 4 dígitos")
    parser.add_argument("--email", help="Correo electrónico opcional", default=None)

    args = parser.parse_args()

    rut = args.rut or input("RUT del administrador: ").strip()
    nombre = args.nombre or input("Nombre completo: ").strip()
    pin = args.pin or input("PIN (4 dígitos): ").strip()

    asyncio.run(crear_o_promover_admin(rut, nombre, pin, args.email))


if __name__ == "__main__":
    main()
