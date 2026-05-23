@echo off
chcp 65001
title ControlS / s off 14:40 - 14:50, 23 05 2026
color 0B

:menu
cls
echo ==================
echo ВЫБЕРИТЕ ДЕЙСТВИЕ:
echo ==================
echo   1. Открыть Paint
    echo   2. Открыть Блокнот
	echo   3. Выход
    echo   4. Настройки Windows
	echo   5. Настройки дисплея
    echo   6. Отключить обои рабочего стола
	echo   7. Создать новую папку
    echo   8. Включить темную тему
	echo   9. Включить светлую тему
    echo   10. Информация о системе
	echo   11. Пинг
    echo   12. Панель управления
	echo   13. Параметры сетевых адаптеров
    echo   14. Управление аккаунтами
	echo   15. Открыть поиск
	echo   16. Симуляция матрицы
	echo   17. Стать мамкиным хацкером
echo ---------------
set /p choice="Ваш выбор (номер): "

if "%choice%"=="1" (
    start mspaint
    goto menu
)
if "%choice%"=="2" (
    start notepad
    goto menu
)
if "%choice%"=="3" (
    exit

)	
	if "%choice%"=="4" (
    start ms-settings:
	goto menu
)		
	if "%choice%"=="5" (
    start ms-settings:display
	goto menu
)
if "%choice%"=="6" (
    powershell -command "Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name WallPaper -Value ''; Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Wallpapers' -Name BackgroundType -Type DWORD -Value 1; Set-ItemProperty -Path 'HKCU:\Control Panel\Colors' -Name Background -Value '0 0 0'; Add-Type -MemberDefinition '[DllImport(\"user32.dll\")] public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);' -Name Win32Utils -Namespace Win32; [Win32.Win32Utils]::SystemParametersInfo(20, 0, '', 3)"
	goto menu
	
	)
if "%choice%"=="7" (
    mkdir "%userprofile%\Desktop\New_folder
	goto menu
)
if "%choice%"=="8" (
    powershell -command "Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'SystemUsesLightTheme' -Value 0; Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'AppsUseLightTheme' -Value 0"
	goto menu

)	
	if "%choice%"=="9" (
    powershell -command "Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'SystemUsesLightTheme' -Value 1; Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'AppsUseLightTheme' -Value 1"
	goto menu
)
if "%choice%"=="10" (
    systeminfo
	pause
	
)
if "%choice%"=="11" (
    ping google.com -n 4
	pause
	goto menu
)
if "%choice%"=="12" (
    start control
	goto menu
)
if "%choice%"=="13" (
    start ncpa.cpl
	goto menu
)
if "%choice%"=="14" (
    start netplwiz
	goto menu
)

    



if "%choice%"=="15" (
    explorer.exe shell:::{2559a1f8-21d7-11d4-bdaf-00c04f60b9f0}
	goto menu

)
if "%choice%"=="16" (
    cls
    color 0A
    echo Запуск симуляции Матрицы...
    echo Нажмите CTRL + C, чтобы остановить поток кода.
    timeout /t 2 > nul
    goto menu
	
	
    :matrix_loop
    echo %random% %random% %random% %random% %random% %random% %random% %random% %random% %random%
    goto matrix_loop
)
if "%choice%"=="17" (
    cls
    color 0C
    echo [СИСТЕМА]: Подключение к удаленному серверу...
    timeout /t 2 > nul
    echo [УСПЕШНО]: Обход брандмауэра пройден.
    timeout /t 1 > nul
    echo [СТАТУС]: Скачивание базы данных... 12%%
    timeout /t 1 > nul
    echo [СТАТУС]: Скачивание базы данных... 48%%
    timeout /t 1 > nul
    echo [СТАТУС]: Скачивание базы данных... 89%%
    timeout /t 2 > nul
    echo [ГОТОВО]: Все данные успешно скопированы на ваш ПК.
    echo.
    color 0A
    echo Шутка! Ваши файлы в безопасности. :)
    pause
    goto menu
)


)

goto menu
