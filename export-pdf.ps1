param(
    [switch]$Compact = $false,
    [string]$Output = ""
)

if ($Compact) {
    if (-not $Output) { $Output = "Gonzalo_Bartual_CV_1Page.pdf" }
    python export_pdf.py --1page "$Output"
} else {
    if (-not $Output) { $Output = "Gonzalo_Bartual_CV.pdf" }
    python export_pdf.py "$Output"
}
