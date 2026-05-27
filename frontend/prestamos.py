import streamlit as st
import httpx
import datetime
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()

URL_API = os.getenv('URL_API')

async def cargar_prestamos():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{URL_API}/loans", headers=st.session_state.get('headers_auth'))
            response.raise_for_status()
            st.success("Prestamos cargados")
            return response.json()

        except httpx.HTTPStatusError as ex:
            st.error(ex.response.text)
            return []

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")
            return []

async def eliminar_prestamo(prestamo_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{URL_API}/loans/{prestamo_id}", headers=st.session_state.get('headers_auth'))
            response.raise_for_status()
            st.success(f"Préstamo {prestamo_id} eliminado exitosamente")

        except httpx.HTTPStatusError as ex:
            try:
                code = ex.response.status_code
                error_json = ex.response.json()
                if code == 404:
                    msg = error_json.get("detail")
                else:
                    detail = error_json.get("detail", [])
                    msg = detail[0].get("msg")
                st.error(msg)
            except ValueError:
                st.error("Error en el servidor")

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")

async def actualizar_prestamo(prestamo_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{URL_API}/loans/{prestamo_id}", headers=st.session_state.get('headers_auth'))
            response.raise_for_status()
            st.success(f"Préstamo {prestamo_id} actualizado exitosamente")

        except httpx.HTTPStatusError as ex:
            try:
                code = ex.response.status_code
                error_json = ex.response.json()

                if code == 404:
                    msg = error_json.get("detail")
                else:
                    detail = error_json.get("detail", [])
                    msg = detail[0].get("msg")
                st.error(msg)
            except ValueError:
                st.error("Error en el servidor")

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")

async def crear_préstamo(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{URL_API}/loans", headers=st.session_state.get('headers_auth'), json=payload)
            response.raise_for_status()
            st.success("Préstamo guardado correctamente")
            time.sleep(1)

        except httpx.HTTPStatusError as ex:
            try:
                code = ex.response.status_code
                error_json = ex.response.json()

                if code == 404:
                    msg = error_json.get("detail")
                else:
                    detail = error_json.get("detail", [])
                    msg = detail[0].get("msg")
                st.error(msg)
            except ValueError:
                st.error("Error en el servidor")

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")

st.title("📖 Catálogo de Préstamos")

if st.session_state.token:
    rol = st.session_state.user_info.get("role")

    if rol == "ADMIN":
        with (st.expander("Registrar Nuevo Préstamo")):
            st.subheader("Datos del Préstamo")
            with st.form("form_prestamo", clear_on_submit=True):
                id_libro = st.number_input("Id Libro")
                id_usuario = st.number_input("Id Usuario")
                fecha_prestamo = st.datetime_input(
                    "Fecha Préstamo",
                    datetime.datetime(2025, 11, 19, 16, 45, 16, 20)
                )
                fecha_retorno_prevista = st.datetime_input(
                    "Fecha Devolución",
                    datetime.datetime(2025, 11, 19, 16, 45, 16, 20)
                )

                if st.form_submit_button("Guardar Préstamo"):
                    if not id_libro:
                        st.error("Falto agregar el 'Id Préstamo' ")
                    elif not id_usuario:
                        st.error("Falto agregar el 'Id Usuario' ")
                    elif not fecha_prestamo:
                        st.error("Falto agregar la 'Fecha Préstamo' ")
                    elif not fecha_retorno_prevista:
                        st.error("Falto agregar la 'Fecha Devolución' ")
                    else:
                        payload = {
                            "book_id": id_libro,
                            "user_id": id_usuario,
                            "lend_date": fecha_prestamo.isoformat(),
                            "expected_return_date": fecha_retorno_prevista.isoformat(),
                        }
                        asyncio.run(crear_préstamo(payload))

    st.header("Prestamos Activos")
    prestamos = asyncio.run(cargar_prestamos())

    size = [1, 2, 2, 2, 1, 1, 1, 1] if rol == "ADMIN" else [1, 2, 2, 2, 1, 1, 1]

    filas_titulos = st.columns(size, vertical_alignment="center")
    filas_titulos[0].write("ID_PRÉSTAMO")
    filas_titulos[1].write("TITULO")
    filas_titulos[2].write("FECHA_PRÉSTAMO")
    filas_titulos[3].write("FECHA_RETORNO")
    filas_titulos[4].write("ACTIVO")
    filas_titulos[5].write("ID_USUARIO")
    filas_titulos[6].write("ACTUALIZAR")

    if rol == "ADMIN":
        filas_titulos[7].write("ELIMINAR")

    for prestamo in prestamos:
        filas = st.columns(size, border=True)

        filas[0].write(prestamo.get("id"))
        filas[1].write(prestamo.get("book").get("title"))
        filas[2].write(prestamo.get("lend_date"))
        filas[3].write(prestamo.get("expected_return_date"))
        filas[4].write(prestamo.get("is_active"))
        filas[5].write(prestamo.get("user").get("id"))
        filas[6].button("Actualizar", key=f"Actualizar_{prestamo.get('id')}",on_click=lambda id_prestamo=prestamo.get("id"): asyncio.run(actualizar_prestamo(id_prestamo)))

        if rol == "ADMIN":
            filas[7].button("Eliminar", key= f"Eliminar_{prestamo.get('id')}", on_click=lambda id_prestamo=prestamo.get("id"): asyncio.run(eliminar_prestamo(id_prestamo)))