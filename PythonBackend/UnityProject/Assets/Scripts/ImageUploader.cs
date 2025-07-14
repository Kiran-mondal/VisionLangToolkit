using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class ImageUploader : MonoBehaviour
{
    public RawImage previewImage;
    public Texture2D defaultTexture;

    public void LoadImage()
    {
#if UNITY_EDITOR
        string path = UnityEditor.EditorUtility.OpenFilePanel("Select Image", "", "png,jpg,jpeg");
        if (!string.IsNullOrEmpty(path))
        {
            byte[] fileData = File.ReadAllBytes(path);
            Texture2D tex = new Texture2D(2, 2);
            tex.LoadImage(fileData);
            previewImage.texture = tex;

            PlayerPrefs.SetString("ImagePath", path);
        }
        else
        {
            previewImage.texture = defaultTexture;
        }
#else
        Debug.LogWarning("Image selection is only supported in the Unity Editor.");
#endif
    }
}
