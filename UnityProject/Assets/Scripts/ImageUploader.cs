using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class ImageUploader : MonoBehaviour
{
    public RawImage previewImage;

    void Start()
    {
        string path = Application.dataPath + "/../test_image.jpg";

        if (File.Exists(path))
        {
            byte[] fileData = File.ReadAllBytes(path);
            Texture2D tex = new Texture2D(2, 2);
            tex.LoadImage(fileData);
            previewImage.texture = tex;

            PlayerPrefs.SetString("ImagePath", path);
            Debug.Log("✅ Image loaded automatically: " + path);
        }
        else
        {
            Debug.LogWarning("❌ test_image.jpg not found.");
        }
    }
}