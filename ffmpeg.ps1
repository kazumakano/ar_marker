Param (
    [parameter(mandatory=$True)] $Src,
    [parameter(mandatory=$True)] $Tgt,
    [ValidateSet('h264_cuvid', 'hevc_cuvid', 'mjpeg_cuvid', 'mpeg1_cuvid', 'mpeg2_cuvid', 'mpeg4_cuvid', 'vc1_cuvid', 'vp8_cuvid', 'vp9_cuvid')] $Codec
)

if (!(Test-Path $Tgt)) {
    New-Item $Tgt
}

$Src = wsl wslpath "'$(Convert-Path $Src)'"
$Tgt = wsl wslpath "'$(Convert-Path $Tgt)'"

if ($Codec) {
    wsl ffmpeg -y -codec $Codec -i $Src $Tgt
} else {
    wsl ffmpeg -y -i $Src $Tgt
}
