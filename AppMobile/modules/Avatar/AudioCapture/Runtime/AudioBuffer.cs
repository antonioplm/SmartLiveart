public class AudioBuffer
{
    public float[] Data { get; private set; }

    public AudioBuffer(int size = 1024)
    {
        Data = new float[size];
    }

    public void Write(float[] input)
    {
        int len = System.Math.Min(input.Length, Data.Length);
        System.Array.Copy(input, Data, len);
    }
}
