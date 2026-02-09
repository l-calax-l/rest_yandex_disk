@echo off
chcp 65001 >nul
echo.
echo ----------------------------------------------------------
echo            ЗАПУСК ТЕСТОВ В 3 ПОТОКА (параллельно)
echo ----------------------------------------------------------
echo.

call .venv\Scripts\activate
rmdir /s /q allure-results
mkdir allure-results

echo.
echo.

pytest tests/ -v -n 3 --alluredir=allure-results

echo ----------------------------------------------------------
echo                     ВЫПОЛНЕНИЕ ЗАВЕРШЕНО
echo ----------------------------------------------------------
pause