Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SetOutputToWaveFile("c:\Users\hp\Desktop\China_project\test_speech.wav")
$synth.Speak("Testing text to speech for sand and dust storm forecasting video.")
$synth.Dispose()
Write-Host "Audio generated successfully"
