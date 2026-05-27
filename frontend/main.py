import streamlit as st
import httpx
import time
import os
from dotenv import load_dotenv

load_dotenv()

URL_API = os.getenv('URL_API')


st.set_page_config(page_title="Sistema de Biblioteca", layout="wide")

if 'token' not in st.session_state:
    st.session_state.token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'headers_auth' not in st.session_state:
    st.session_state.headers_auth = None

if st.session_state.token is None:
    st.title("Sistema de Biblioteca")
    st.subheader('Autenticacion')

    tab_login, tab_signup = st.tabs(["Login", "Signup"])

    with tab_login:
        with st.form("Login"):
            st.header("Ingresa tus datos")
            email_login = st.text_input("Correo Electrónico ('ejemplo'@'provedor'.com)")
            password_login = st.text_input("Contraseña (6-24 caracteres)", type="password")
            submitted_login = st.form_submit_button("Iniciar Sesión")

        if submitted_login:
            if not email_login:
                st.error("Falta agregar el 'Email' ")
            elif not password_login:
                st.error("Falta agregar el 'Password' ")
            else:
                 payload = {
                    "username": email_login,
                    "password": password_login
                 }
                 with httpx.Client() as client:
                    try:
                        response = client.post(f"{URL_API}/auth/login", data = payload)
                        response.raise_for_status()
                        data = response.json()
                        token = data["access_token"]
                        token_type = data["token_type"]
                        user_info = data["user"]
                        st.session_state.token = token
                        st.session_state.user_info = user_info
                        st.session_state.headers_auth = {"Authorization": f"{token_type} {token}"}
                        st.success("Inicio de sesión exitoso")
                        time.sleep(1)
                        st.rerun()

                    except httpx.HTTPStatusError as ex:
                        try:
                            code = ex.response.status_code
                            error_json = ex.response.json()

                            if code == 400 or code == 401:
                                msg = error_json.get("detail")
                            else:
                                detail = error_json.get("detail", [])
                                msg = detail[0].get("msg")
                            st.error(msg)
                        except ValueError:
                            st.error("Error en el servidor")
                    except httpx.RequestError:
                        st.error("Error de conexión con el servidor")

    with tab_signup:
        with st.form("Signup",  False):
            st.header("Ingresa tus datos")

            username_signup = st.text_input("Ingresa tu username", key="username_input")
            email_signup = st.text_input("Ingresa tu email ('ejemplo'@'provedor'.com)", key="email_input")
            password_signup = st.text_input("Ingresa tu password (6-24 caracteres)", type="password", key="password_input")

            submitted_signup = st.form_submit_button("Registrar Cuenta")

        if submitted_signup:
            if not username_signup:
                st.error("Falta agregar el 'Username' ")
            elif not email_signup:
                st.error("Falta agregar el 'Email' ")
            elif not password_signup:
                st.error("Falta agregar el 'Password' ")
            else:
                payload = {
                    "username": username_signup,
                    "email": email_signup,
                    "password": password_signup,
                }
                with httpx.Client() as client:
                    try:
                        response = client.post(f"{URL_API}/auth/signup", json = payload)
                        response.raise_for_status()
                        st.success("Usuario registrado, ya puedes iniciar sesión")

                    except httpx.HTTPStatusError as ex:
                        try:
                            code = ex.response.status_code
                            error_json = ex.response.json()

                            if code == 409:
                                msg = error_json.get("detail")
                            else:
                                detail = error_json.get("detail", [])
                                msg = detail[0].get("msg")
                            st.error(msg)
                        except ValueError:
                            st.error("Error en el servidor")
                    except httpx.RequestError:
                        st.error("Error de conexión con el servidor")
else:
    if st.sidebar.button("Cerrar Sesión", type="primary", use_container_width=True):
        st.session_state.token = None
        st.session_state.user_info = None
        st.session_state.headers_auth = None
        st.logout()

    pages = {
        "Recursos": [
            st.Page("libros.py", title="Libros"),
            st.Page("prestamos.py", title="Prestamos"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()