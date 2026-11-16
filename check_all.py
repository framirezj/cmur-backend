from pydantic import ValidationError
from fastapi import HTTPException
from core.security import (
    hash_pin,
    verify_pin,
    create_access_token,
    decode_access_token,
    get_current_user_id,
    require_admin,
)
from features.usuarios.schemas import RegistroRequest, LoginRequest, normalizar_rut

def run_tests():
    print("1. Probando normalizar_rut...")
    assert normalizar_rut(" 12.345.678-k ") == "12345678-K"
    assert normalizar_rut("9.876.543-2") == "9876543-2"
    print("   -> OK")

    print("2. Probando hash_pin y verify_pin con bcrypt...")
    pin = "1234"
    h = hash_pin(pin)
    assert h != pin
    assert verify_pin("1234", h) is True
    assert verify_pin("0000", h) is False
    assert verify_pin("123", h) is False
    print("   -> OK")

    print("3. Probando validaciones de PIN en Pydantic...")
    reg = RegistroRequest(rut="12.345.678-9", nombre="Juan Perez", pin="1234")
    assert reg.rut == "12345678-9"
    assert reg.pin == "1234"

    try:
        RegistroRequest(rut="12345678-9", nombre="Juan", pin="123")
        assert False, "Debió fallar con 3 dígitos"
    except ValidationError:
        pass

    try:
        RegistroRequest(rut="12345678-9", nombre="Juan", pin="abcd")
        assert False, "Debió fallar con letras"
    except ValidationError:
        pass
    print("   -> OK")

    print("4. Probando JWT y RBAC (Control de acceso por roles)...")
    # Usuario normal
    u_tok = create_access_token({"sub": "42", "rol": "usuario"})
    p_u = decode_access_token(u_tok)
    assert get_current_user_id(p_u) == 42
    try:
        require_admin(p_u)
        assert False, "Debió bloquear al rol usuario"
    except HTTPException as e:
        assert e.status_code == 403
        print(f"   -> Rol 'usuario' bloqueado correctamente (403 Forbidden): {e.detail}")

    # Admin
    a_tok = create_access_token({"sub": "1", "rol": "admin"})
    p_a = decode_access_token(a_tok)
    admin_id = require_admin(p_a)
    assert admin_id == 1
    print(f"   -> Rol 'admin' autorizado correctamente: ID {admin_id}")

    print("5. Verificando rutas y endpoints registrados en OpenAPI...")
    import main
    paths = list(main.app.openapi()["paths"].keys())
    assert "/auth/register" in paths
    assert "/auth/login" in paths
    assert "/anexos/" in paths
    assert "/anexos/{anexo_id}" in paths
    assert "/usuarios/me" in paths
    assert "/usuarios/me/favoritos" in paths
    assert "/auth/google" not in paths
    print("   -> OK, Endpoints activos:")
    for path in sorted(paths):
        print(f"      • {path}")

    print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")

if __name__ == "__main__":
    run_tests()
