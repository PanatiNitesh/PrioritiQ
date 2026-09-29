@echo off
echo ========================================================
echo   PrioritiQ Automated Verification & Benchmark Suite
echo ========================================================
echo.

pytest tests -v --tb=short
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   [SUCCESS] All PrioritiQ test suites passed! (100%%)
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [FAILURE] Test suite encountered errors.
    echo ========================================================
)
