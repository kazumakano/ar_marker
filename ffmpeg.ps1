Param (
    [parameter(mandatory=$True)] $Src,
    [parameter(mandatory=$True)] $Tgt,
    $Start,
    $Stop
)

if (!(Test-Path $Tgt)) {
    New-Item $Tgt
}

$Src = wsl wslpath "'$(Convert-Path $Src)'"
$Tgt = wsl wslpath "'$(Convert-Path $Tgt)'"

if ($Start -and $Stop) {
    wsl ffmpeg -y -i $Src -codec copy -to $Stop -ss $Start $Tgt
} elseif ($Start) {
    wsl ffmpeg -y -i $Src -codec copy -ss $Start $Tgt
} elseif ($Stop) {
    wsl ffmpeg -y -i $Src -codec copy -to $Stop $Tgt
} else {
    wsl ffmpeg -y -i $Src -codec copy $Tgt
}
