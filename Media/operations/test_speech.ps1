Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$outputPath = Join-Path $PSScriptRoot "test_speech.wav"
$synth.SetOutputToWaveFile($outputPath)
$synth.Speak("Testing text to speech for sand and dust storm forecasting video.")
$synth.Dispose()
Write-Host "Audio generated successfully"
