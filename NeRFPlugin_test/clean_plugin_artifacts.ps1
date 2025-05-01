# clean_plugin_artifacts.ps1
Write-Host "Cleaning NeRFPlugin build artifacts..."

# 1. Move native build folder out of Assets
$buildPath = "Assets/NeRFPlugin/instant-ngp/build"
$targetPath = "NeRFPlugin_external_build"

if (Test-Path $buildPath) {
    Move-Item $buildPath $targetPath -Force
    Write-Host "Moved native build folder to: $targetPath"
}

# 2. Delete one of the duplicate nvngx_dlss.dll files
$dup1 = "Assets/NeRFPlugin/instant-ngp/dependencies/dlss/lib/Windows_x86_64/dev/nvngx_dlss.dll"
$dup2 = "Assets/NeRFPlugin/instant-ngp/dependencies/dlss/lib/Windows_x86_64/rel/nvngx_dlss.dll"

if (Test-Path $dup1 -and Test-Path $dup2) {
    Remove-Item $dup2 -Force
    Write-Host "Removed duplicate plugin: $dup2"
}

# 3. Remove broken .meta files
$metaFiles = Get-ChildItem -Recurse -Filter *.meta
foreach ($meta in $metaFiles) {
    $assetPath = $meta.FullName -replace '\\.meta$', ''
    if (-not (Test-Path $assetPath)) {
        Remove-Item $meta.FullName -Force
        Write-Host "Removed orphaned meta: $($meta.FullName)"
    }
}

Write-Host "Cleanup complete!"
