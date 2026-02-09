@echo off
chcp 65001 >nul
echo.
echo ----------------------------------------------------------
echo            ЗАПУСК ТЕСТОВ В 1 ПОТОК (последовательно)
echo ----------------------------------------------------------
echo.

call .venv\Scripts\activate
rmdir /s /q allure-results
mkdir allure-results

echo.
echo.

pytest tests/ -v -n 1 --alluredir=allure-results

echo.
echo ----------------------------------------------------------
echo                     ВЫПОЛНЕНИЕ ЗАВЕРШЕНО
echo ----------------------------------------------------------
pause