@echo off
echo ========================================
echo Switching from SWC to Babel
echo ========================================
echo.
echo This will disable SWC and use Babel instead.
echo Babel is slower but more compatible.
echo.
pause

cd /d "%~dp0"

echo.
echo Creating .babelrc file...
(
echo {
echo   "presets": ["next/babel"]
echo }
) > .babelrc
echo ✓ Created .babelrc

echo.
echo Updating next.config.js...
(
echo /** @type {import('next'^).NextConfig} */
echo const nextConfig = {
echo   reactStrictMode: true,
echo   swcMinify: false,  // Disable SWC minification
echo   compiler: {
echo     // Disable SWC compiler
echo     styledComponents: false,
echo   },
echo }
echo.
echo module.exports = nextConfig
) > next.config.js
echo ✓ Updated next.config.js

echo.
echo ========================================
echo Switch Complete!
echo ========================================
echo.
echo Now try running: npm run dev
echo.
echo Note: First build will be slower with Babel
echo.
pause
