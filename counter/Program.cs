using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Encodings.Web;
using System.Text.Unicode;

if (args.Length < 1)
{
    Console.Error.WriteLine("You should provide a file path!");
    Environment.Exit(1);
}
var path = args.FirstOrDefault()!;

if (!Path.Exists(path))
{
    Console.Error.WriteLine("File not found!");
    Environment.Exit(1);
}

using var reader = new StreamReader(new FileStream(path, FileMode.OpenOrCreate), Encoding.UTF8);
var counter = new Dictionary<char, long>();

do
{
    foreach (var ch in reader.ReadLine() ?? "")
    {
        if (counter.TryGetValue(ch, out long value))
            counter[ch] = value + 1;
        else
            counter[ch] = 1;
    }
} while (!reader.EndOfStream);
var options = new JsonSerializerOptions
{
    Encoder = JavaScriptEncoder.Create(UnicodeRanges.All),
    WriteIndented = true,
};

var outputPath = Path.Combine(Path.GetDirectoryName(path)!, "count.txt");
using var writer = new StreamWriter(outputPath, false, Encoding.UTF8);
writer.Write(JsonSerializer.Serialize(counter, options));
