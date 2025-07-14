using UnityEngine;
using System.Diagnostics;
using System.IO;
using UnityEngine.UI;

public class PythonBridge : MonoBehaviour
{
    public Text outputText;
    public string pythonScript = "PythonBackend/extractor.py";

    public void RunExtraction()
    {
        string imagePath = PlayerPrefs.GetString("ImagePath");
        if (string.IsNullOrEmpty(imagePath))
        {
            outputText.text = "No image selected.";
            return;
        }

        ProcessStartInfo start = new ProcessStartInfo()
        {
            FileName = "python3", // or "python" on Windows
            Arguments = $"{pythonScript} \"{imagePath}\"",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        using (Process process = Process.Start(start))
        {
            StreamReader reader = process.StandardOutput;
            string result = reader.ReadToEnd();
            outputText.text = result;
        }
    }
}
