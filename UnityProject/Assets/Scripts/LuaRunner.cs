using UnityEngine;
using MoonSharp.Interpreter;

public class LuaRunner : MonoBehaviour
{
    public string RunLua(string jsonAttributes)
    {
        // Initialize Lua interpreter
        Script script = new Script();

        // Load Lua file from plugin folder
        script.DoFile("LanguageRuntime/plugins/custom_processing.lua");

        // Get Lua function called 'process'
        DynValue processFunc = script.Globals["process"];

        // Convert JSON string to Lua table
        DynValue attrTable = script.DoString($"return {jsonAttributes}");

        // Call the Lua function with the attribute table
        DynValue result = script.Call(processFunc, attrTable);

        return result.String;
    }
}
