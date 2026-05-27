import streamlit as st
import httpx
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()

URL_API = os.getenv('URL_API')

async def cargar_libros():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{URL_API}/books")
            response.raise_for_status()
            st.success("Libros cargados")
            return response.json()

        except httpx.HTTPStatusError as ex:
            st.error(ex.response.text)
            return []

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")
            return []

async def eliminar_libro(libro_id: int):
    payload = {"book_id": libro_id}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{URL_API}/books", headers=st.session_state.get('headers_auth'), params=payload)
            response.raise_for_status()
            st.success(f"Libro {libro_id} eliminado exitosamente")

        except httpx.HTTPStatusError as ex:
            st.error(ex.response.text)

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")

async def crear_libro(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{URL_API}/books", headers=st.session_state.get('headers_auth'), json=payload)
            response.raise_for_status()
            st.success("Libro guardado correctamente")
            time.sleep(1)

        except httpx.HTTPStatusError as ex:
            st.error(ex.response.text)

        except httpx.RequestError:
            st.error("Error de conexión con el servidor")

st.title("Catálogo de Libros")

if st.session_state.token:
    rol = st.session_state.user_info.get("role")

    if rol == "ADMIN":
        with (st.expander("Registrar Nuevo Libro")):
            st.subheader("Datos del Libro")
            with st.form("form_libro", clear_on_submit=True):
                autor_libro = st.number_input("Autor")
                titulo_libro = st.text_input("Título")
                description_libro = st.text_input("Description")
                total_stock_libro = st.number_input("Total Stock")
                disponible_stock_libro = st.number_input("Stock disponible")

                if st.form_submit_button("Guardar libro"):
                    if not titulo_libro:
                        st.error("Falto agregar el 'Titulo' ")
                    elif not autor_libro:
                        st.error("Falto agregar el 'Autor' ")
                    elif not description_libro:
                        st.error("Falto agregar la 'Description' ")
                    elif not total_stock_libro:
                        st.error("Falto agregar el 'Total Stock' ")
                    elif not disponible_stock_libro:
                        st.error("Falto agregar el 'Stock disponible' ")
                    else:
                        payload = {
                            "author_id": autor_libro,
                            "title": titulo_libro,
                            "description": description_libro,
                            "total_stock": total_stock_libro,
                            "available_stock": disponible_stock_libro
                        }
                        asyncio.run(crear_libro(payload))

    st.header("Libros en existencia")
    libros = asyncio.run(cargar_libros())

    size = [2, 3, 3, 3, 2, 2] if rol == "ADMIN" else [2, 3, 3, 3, 2]

    filas_titulos = st.columns(size, vertical_alignment="center")
    filas_titulos[0].write("ID")
    filas_titulos[1].write("TITULO")
    filas_titulos[2].write("AUTOR")
    filas_titulos[3].write("DESCRIPCIÓN")
    filas_titulos[4].write("STOCK")
    if rol == "ADMIN":
        filas_titulos[5].write("ELIMINAR")

    for libro in libros:
        filas = st.columns(size, border=True)

        filas[0].write(libro.get("id"))
        filas[1].write(libro.get("title"))
        filas[2].write(libro.get("author").get("name"))
        filas[3].write(libro.get("description"))
        filas[4].write(libro.get("available_stock"))
        if rol == "ADMIN":
            filas[5].button("Eliminar", key= f"Eliminar_{libro.get('id')}", on_click=lambda id_libro=libro.get("id"): asyncio.run(eliminar_libro(id_libro)))