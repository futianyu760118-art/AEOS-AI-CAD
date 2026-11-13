# Run in PowerShell on a Windows workstation with internet access.
$ErrorActionPreference='Stop'
Set-Location (Join-Path $PSScriptRoot '..')
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
 Write-Host 'Please install uv from https://docs.astral.sh/uv/getting-started/installation/ and re-run.'
 exit 2
}
uv venv --python 3.13 .venv-img2cad
if ($LASTEXITCODE -ne 0) { throw 'Creating Python 3.13 environment failed' }
& .\.venv-img2cad\Scripts\python.exe -m pip --version 2>$null
if ($LASTEXITCODE -ne 0) { uv pip install --python .\.venv-img2cad\Scripts\python.exe pip }
uv pip install --python .\.venv-img2cad\Scripts\python.exe 'img2cad==0.15.0'
& .\.venv-img2cad\Scripts\img2cad.exe doctor
if ($LASTEXITCODE -ne 0) { throw 'img2cad doctor failed: do not continue' }
Write-Host 'Img2cad installed. Use img2cad_job/AGENT_INSTRUCTIONS.md to generate model.py.'
