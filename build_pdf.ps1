# =====================================================================
# Lagging Truth - series PDF build  (Research-to-Publication Standard)
# =====================================================================
# Reusable across every paper in the series. It:
#   1. writes the series header.tex + metadata.yaml to TEMP as UTF-8 *no-BOM*
#      (via [System.IO.File]::WriteAllText - avoids the PowerShell UTF-16/BOM
#       redirection trap that corrupts a redirected/Set-Content file),
#   2. (if the paper has an appendix) demotes every appendix heading one level
#      in a TEMP copy, so the -1 heading shift renders "Appendix A" as a
#      top-level \section instead of demoting its leading "# " to a paragraph,
#   3. renders manuscript_rendered.md [+ demoted appendix] with pandoc + xelatex.
#
# Only the committed slug-named PDF is kept (no committed PDF_Build/ folder) -
# this matches the current-Standard convention (Adaptation / MSC), recorded in
# the MSC ledger as D-026.
#
# PER PAPER, edit only the four variables in the SETTINGS block.
# Requires: pandoc + xelatex (MiKTeX/TeX Live) on PATH; Cambria + Cambria Math
# installed (Windows / Office fonts).
#
# How to run (from the repo root, with this script there):
#     .\build_pdf.ps1
#   or, if execution policy complains:
#     powershell -ExecutionPolicy Bypass -File .\build_pdf.ps1
# =====================================================================

$ErrorActionPreference = "Stop"

# --------------------------- SETTINGS -------------------------------
$PaperDir   = Join-Path $PSScriptRoot "paper"
$Slug       = "Cross-Domain-Validation"
$Manuscript = Join-Path $PaperDir "Cross-Domain-Validation.rendered.md"
$Appendix   = $null   # appendix is now inline in the manuscript (set a path here only for a separate appendix)
# --------------------------------------------------------------------

$Output = Join-Path $PaperDir "$Slug.pdf"

Write-Host ""
Write-Host "=== Lagging Truth PDF build: $Slug ===" -ForegroundColor Cyan

# --- pre-flight: tools on PATH ---
foreach ($t in @("pandoc","xelatex")) {
    if (-not (Get-Command $t -ErrorAction SilentlyContinue)) {
        Write-Host "ERROR: '$t' not found on PATH." -ForegroundColor Red
        Write-Host "       pandoc: https://pandoc.org/installing.html" -ForegroundColor Red
        Write-Host "       xelatex: install MiKTeX (https://miktex.org) or TeX Live" -ForegroundColor Red
        exit 1
    }
    Write-Host ("[ OK ] {0} -> {1}" -f $t, (Get-Command $t).Source)
}
if (-not (Test-Path $Manuscript)) { Write-Host "ERROR: manuscript not found: $Manuscript" -ForegroundColor Red; exit 1 }
Write-Host "[ OK ] manuscript: $Manuscript"

# --- stale-output guard: remember the pre-build stamp (series lesson: an
#     exists-only check reports SUCCESS on a permission-denied write) ---
$PreBuildStamp = $null
if (Test-Path $Output) {
    $PreBuildStamp = (Get-Item $Output).LastWriteTime
    Write-Host ("[ OK ] existing PDF stamp recorded: {0}" -f $PreBuildStamp)
} else {
    Write-Host "[ OK ] no existing PDF (first build)"
}

# --- series header.tex (Cambria + Cambria Math; matches Papers 1 and 2) ---
# Identical across the series; the only paper-specific content (title/author/date)
# lives in the manuscript_rendered.md YAML front matter, NOT here.
$Header = @'
% header.tex - Lagging Truth series preamble (Cambria + Cambria Math)
% --- fonts (Ligatures=NoCommon applies to all four faces) ---
\usepackage{unicode-math}
\setmainfont{Cambria}[Ligatures=NoCommon]
\setmathfont{Cambria Math}
% --- spacing / typography ---
\usepackage[margin=1.25in]{geometry}
\linespread{1.15}
\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}
% --- math ---
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{cases}
% --- checkmark glyph (\ding{51}) ---
\usepackage{pifont}
% --- section title formatting ---
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection}{1em}{}
% --- tables ---
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{longtable}
% --- code blocks: wrap long lines if any paper has code ---
\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\}}
\RecustomVerbatimEnvironment{verbatim}{Verbatim}{breaklines,breakanywhere}
% --- title rule under the title ---
\usepackage{titling}
\pretitle{\begin{center}\LARGE}
\posttitle{\par\end{center}\vspace{1em}\begin{center}\rule{0.35\textwidth}{0.5pt}\end{center}\vspace{0.5em}}
% --- hyperref last ---
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}
% --- equation numbering within section ---
\numberwithin{equation}{section}
% --- allow long URLs to break ---
\usepackage{xurl}
'@

# --- series metadata.yaml (settings only; geometry lives in header.tex to avoid an option clash) ---
# map the manuscript's raw Unicode check/cross marks to pifont glyphs at runtime;
# kept out of the here-string so build_pdf.ps1 stays pure ASCII (PS 5.1 reads a no-BOM script as ANSI).
# pifont is already loaded above; Cambria has no glyph for U+2713 / U+2717.
$Header = $Header + "`n% raw-Unicode mark mapping (added by build script)`n\usepackage{newunicodechar}`n\newunicodechar{$([char]0x2713)}{\ding{51}}`n\newunicodechar{$([char]0x2717)}{\ding{55}}`n"

$Metadata = @'
---
documentclass: article
fontsize: 11pt
papersize: letter
colorlinks: true
linkcolor: blue
urlcolor: blue
citecolor: blue
header-includes:
  - \usepackage{microtype}
...
'@

$utf8NoBom    = New-Object System.Text.UTF8Encoding($false)
$Tmp          = [System.IO.Path]::GetTempPath()
$HeaderPath   = Join-Path $Tmp "lt_header.tex"
$MetadataPath = Join-Path $Tmp "lt_metadata.yaml"
[System.IO.File]::WriteAllText($HeaderPath,   $Header,   $utf8NoBom)
[System.IO.File]::WriteAllText($MetadataPath, $Metadata, $utf8NoBom)
Write-Host "[ OK ] header.tex + metadata.yaml written to TEMP (UTF-8 no-BOM)"

# --- PDF-only series-conformance transforms (committed artifacts untouched) ---
$man = [System.IO.File]::ReadAllText($Manuscript, $utf8NoBom)
# 0) strip a leading GENERATED HTML comment if the renderer prepends one
#    (pandoc only parses front matter that starts the file)
$man = [regex]::Replace($man, '^\s*<!--.*?-->\s*', '', [System.Text.RegularExpressions.RegexOptions]::Singleline)
# 1) standalone approx-tilde (series lesson; harmless if absent)
$man = $man.Replace('$\sim$', '~')
# 2) Series heading style: '## 2. Related Literature' -> '## 2 Related Literature'
$man = [regex]::Replace($man, '(?m)^(#{1,4}) (\d+(?:\.\d+)*)\. ', '$1 $2 ')
$ManTmp = Join-Path $Tmp "lt_manuscript_pdf.md"
[System.IO.File]::WriteAllText($ManTmp, $man, $utf8NoBom)
Write-Host "[ OK ] PDF-only transforms applied -> $ManTmp"

# --- assemble inputs; demote appendix headings one level if present ---
$Inputs = @($ManTmp)
if ($Appendix -and (Test-Path $Appendix)) {
    $apx = [System.IO.File]::ReadAllText($Appendix, $utf8NoBom)   # UTF-8 read (Get-Content defaults to ANSI on PS 5.1 and mangles em/en-dashes)
    $apx = [regex]::Replace($apx, '(?m)^(#{1,6}) ', '#$1 ')   # +1 level to every ATX heading
    $apx = "\newpage`r`n`r`n" + $apx                          # page break before the appendix
    $ApxTmp = Join-Path $Tmp "lt_appendix_demoted.md"
    [System.IO.File]::WriteAllText($ApxTmp, $apx, $utf8NoBom)
    $Inputs += $ApxTmp
    Write-Host "[ OK ] appendix headings demoted -> $ApxTmp"
}

# --- render ---
Write-Host "Building PDF -> $Output" -ForegroundColor Cyan
& pandoc @Inputs `
    --pdf-engine=xelatex `
    --metadata-file="$MetadataPath" `
    --include-in-header="$HeaderPath" `
    --shift-heading-level-by=-1 `
    --resource-path="$PaperDir" `
    --output="$Output"

if (-not (Test-Path $Output)) {
    Write-Host "=== BUILD FAILED === (see xelatex errors above)" -ForegroundColor Red
    exit 1
}
$PostBuildStamp = (Get-Item $Output).LastWriteTime
if ($PreBuildStamp -and ($PostBuildStamp -le $PreBuildStamp)) {
    Write-Host "=== BUILD FAILED === STALE OUTPUT" -ForegroundColor Red
    Write-Host ("The PDF on disk was NOT rewritten by this run (stamp unchanged: {0})." -f $PostBuildStamp) -ForegroundColor Red
    Write-Host "The usual cause is that the PDF is open in a viewer, so the write was denied." -ForegroundColor Red
    Write-Host "Close the PDF and re-run. Do NOT ship this file - it is the previous build." -ForegroundColor Red
    exit 1
}
$kb = [math]::Round((Get-Item $Output).Length / 1KB, 1)
Write-Host "=== SUCCESS ===" -ForegroundColor Green
Write-Host ("PDF: {0}  ({1} KB, modified {2})" -f $Output, $kb, $PostBuildStamp)
Write-Host "Stale-output guard: PASSED (file rewritten by this run)."
