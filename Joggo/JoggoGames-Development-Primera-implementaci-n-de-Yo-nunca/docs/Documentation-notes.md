## Implementation Notes
Se han creado endopoints para crear usuarios, eliminar usuarios repetidos, para conseguir usuarios, 
para postear frases y obtenerlas.

```python
@router.post("/usuario/", response_model=Usuario_Pydantic)
async def create_usuario(usuario: UsuarioIn_Pydantic):
    # Verificar si el nombre ya existe
    existing_usuario = await Usuario.filter(nombre=usuario.nombre).first()
    
    if existing_usuario:
        raise HTTPException(status_code=400, detail="El nombre ya existe, introduce uno nuevo.")

    # Si no existe, crear el nuevo usuario
    usuario_obj = await Usuario.create(**usuario.dict())
    return await Usuario_Pydantic.from_tortoise_orm(usuario_obj)

@router.delete("/usuarios/duplicados")
async def delete_usuarios_duplicados():
    # Obtener una lista de los nombres repetidos
    usuarios_con_mismo_nombre = await Usuario.all().values('nombre')
    nombres_repetidos = set([usuario['nombre'] for usuario in usuarios_con_mismo_nombre if usuarios_con_mismo_nombre.count(usuario) > 1])

    if not nombres_repetidos:
        raise HTTPException(status_code=404, detail="No hay usuarios duplicados")

    usuarios_eliminados = 0

    # Eliminar los duplicados manteniendo solo uno
    for nombre in nombres_repetidos:
        usuarios_con_duplicados = await Usuario.filter(nombre=nombre).all()

        # Mantener solo el primero y eliminar el resto
        for usuario in usuarios_con_duplicados[1:]:
            await usuario.delete()
            usuarios_eliminados += 1

    return {"message": f"{usuarios_eliminados} usuarios duplicados eliminados."}

@router.get("/usuarios/", response_model=List[Usuario_Pydantic])
async def list_usuarios():
    return await Usuario_Pydantic.from_queryset(Usuario.all())

@router.get("/usuario/{usuario_nombre}", response_model=Usuario_Pydantic)
async def get_usuario(nombre: str):
    return await Usuario_Pydantic.from_queryset_single(Usuario.get(nombre=nombre))

# Endpoints para Frases
@router.post("/frase/", response_model=FraseRead)
async def create_frase(frase: FraseCreate, autor_nombre: str):
    autor = await Usuario.get(nombre=autor_id)
    frase_obj = await Frase.create(**frase.dict(), autor=autor)
    return await Frase.from_tortoise_orm(frase_obj)

@router.get("/frase/{usuario_nombre}", response_model=FraseRead)
async def get_frase():
    return await FraseRead.from_queryset(Frase.all())

# Endpoints para Respuestas
@router.post("/respuestas/", response_model=RespuestaRead)
async def create_respuesta(respuesta: RespuestaCreate, usuario_id: str):
    usuario = await Usuario.get(id=usuario_id)
    frase = await Frase.get(id=respuesta.frase_id)
    respuesta_obj = await Respuesta.create(
        usuario=usuario,
        frase=frase,
        hecho=respuesta.hecho,
        like=respuesta.like
    )
    return await RespuestaRead.from_tortoise_orm(respuesta_obj)
```