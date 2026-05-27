# 1. Entrar a la carpeta del backend
cd backend

# 2. Crear el entorno virtual específico para el servidor
python -m venv .venv

# 3. Activar el entorno virtual
.venv\\Scripts\\activate

# 4. Instalar todas las librerías necesarias 
pip install -r requirements.txt

# 5. Ejecutar el servidor backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


# 6. Entrar a la carpeta del frontend desde la raíz del proyecto
cd frontend

# 7. Crear el entorno virtual específico para la interfaz
python -m venv .venv

# 8. Activar el entorno virtual
.venv\\Scripts\\activate

# 9. Instalar las librerías necesarias 
pip install -r requirements.txt

# 10. Ejecutar el servidor frontend
streamlit run main.py

# 11. Finalizar ejecución

ctrl + c

# 12. Desactivar entorno virtual (backend - frontend)

deactivate