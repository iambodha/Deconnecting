@echo off

:AddGitKeep
    for /d %%d in (*) do (
        if not exist "%%d\.gitkeep" echo.> "%%d\.gitkeep"
        pushd "%%d"
        call :AddGitKeep
        popd
    )
    exit /b

call :AddGitKeep

echo Done!
pause