import pytest
import os
from datetime import datetime

# 1. Define the report folder path (Ruta de la carpeta de reportes)
# Usamos 'r' para que Windows no interprete mal las barras invertidas
reports_path = r"C:\Users\Señora Betsy\Documents\Practica Automation\Reports"

# 2. Create the folder if it doesn't exist (Crear la carpeta si no existe)
if not os.path.exists(reports_path):
    os.makedirs(reports_path)

# 3. Format the filename with the current date (Formatear el nombre con la fecha)
current_date = datetime.now().strftime("%d-%m-%Y")
report_name = f"Report_{current_date}.html"
final_path = os.path.join(reports_path, report_name)

# 4. Run pytest with the generated path (Ejecutar pytest con la ruta generada)
if __name__ == "__main__":
    # --html genera el reporte y --self-contained-html mete todo en un solo archivo
    pytest.main(
        [
            f"--html={final_path}",
            "--self-contained-html",
            "tests/test_shopping_cart.py",  # Apuntamos directamente a tu archivo de test
        ]
    )
