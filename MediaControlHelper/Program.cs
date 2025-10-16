// File: MediaControlHelper.cs
using System;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using Windows.Media.Control;
using Windows.Media.Playback;

namespace MediaControlHelper
{
    class Program
    {
        static async Task<int> Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Usage: MediaControlHelper.exe [playpause|next|prev|getvolume|setvolume <0-100>]");
                return 1;
            }

            string command = args[0].ToLower();

            switch (command)
            {
                case "playpause":
                case "next":
                case "prev":
                    await HandleMediaCommand(command);
                    break;

                case "getvolume":
                    float currentVolume = AudioManager.GetMasterVolume();
                    Console.WriteLine($"Current volume: {currentVolume * 100:F0}%");
                    break;

                case "setvolume":
                    if (args.Length < 2 || !float.TryParse(args[1], out float target))
                    {
                        Console.WriteLine("Usage: MediaControlHelper.exe setvolume <0-100>");
                        return 1;
                    }
                    target = Math.Clamp(target, 0, 100);
                    AudioManager.SetMasterVolume(target / 100f);
                    Console.WriteLine($"Volume set to {target:F0}%");
                    break;

                default:
                    Console.WriteLine("Unknown command.");
                    return 1;
            }

            return 0;
        }

        private static async Task HandleMediaCommand(string command)
        {
            var sessions = await GlobalSystemMediaTransportControlsSessionManager.RequestAsync();
            var current = sessions.GetCurrentSession();

            if (current == null)
            {
                Console.WriteLine("No active media session.");
                return;
            }

            switch (command)
            {
                case "playpause":
                    var status = current.GetPlaybackInfo().PlaybackStatus;
                    if (status == GlobalSystemMediaTransportControlsSessionPlaybackStatus.Playing)
                        await current.TryPauseAsync();
                    else
                        await current.TryPlayAsync();
                    break;

                case "next":
                    await current.TrySkipNextAsync();
                    break;

                case "prev":
                    await current.TrySkipPreviousAsync();
                    break;
            }
        }
    }

    // Volume control via Core Audio API (IAudioEndpointVolume)
    static class AudioManager
    {
        private const int DEVICE_STATE_ACTIVE = 0x00000001;
        private static readonly Guid IID_IAudioEndpointVolume = new Guid("5CDF2C82-841E-4546-9722-0CF74078229A");

        [ComImport]
        [Guid("A95664D2-9614-4F35-A746-DE8DB63617E6")]
        [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IMMDeviceEnumerator
        {
            int NotImpl1();

            [PreserveSig]
            int GetDefaultAudioEndpoint(EDataFlow dataFlow, ERole role, out IMMDevice ppDevice);
        }

        private enum EDataFlow { eRender, eCapture, eAll }
        private enum ERole { eConsole, eMultimedia, eCommunications }

        [ComImport]
        [Guid("D666063F-1587-4E43-81F1-B948E807363F")]
        [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IMMDevice
        {
            [PreserveSig]
            int Activate(ref Guid iid, int dwClsCtx, IntPtr pActivationParams, out IAudioEndpointVolume ppInterface);
        }

        [ComImport]
        [Guid("5CDF2C82-841E-4546-9722-0CF74078229A")]
        [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        private interface IAudioEndpointVolume
        {
            // Only using needed methods
            int RegisterControlChangeNotify(IntPtr pNotify);
            int UnregisterControlChangeNotify(IntPtr pNotify);
            int GetChannelCount(out int pnChannelCount);
            int SetMasterVolumeLevel(float fLevelDB, Guid pguidEventContext);
            int SetMasterVolumeLevelScalar(float fLevel, Guid pguidEventContext);
            int GetMasterVolumeLevel(out float pfLevelDB);
            int GetMasterVolumeLevelScalar(out float pfLevel);
            int SetMute(bool bMute, Guid pguidEventContext);
            int GetMute(out bool pbMute);
            int GetVolumeStepInfo(out uint pnStep, out uint pnStepCount);
            int VolumeStepUp(Guid pguidEventContext);
            int VolumeStepDown(Guid pguidEventContext);
            int QueryHardwareSupport(out uint pdwHardwareSupportMask);
            int GetVolumeRange(out float pflVolumeMindB, out float pflVolumeMaxdB, out float pflVolumeIncrementdB);
        }

        [ComImport]
        [Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
        private class MMDeviceEnumeratorComObject { }

        private static IAudioEndpointVolume GetVolumeObject()
        {
            var enumerator = (IMMDeviceEnumerator)new MMDeviceEnumeratorComObject();
            enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender, ERole.eMultimedia, out var device);

            Guid iid = IID_IAudioEndpointVolume; // ← local copy
            device.Activate(ref iid, 23 /*CLSCTX_ALL*/, IntPtr.Zero, out var volume);
            return volume;
        }


        public static void SetMasterVolume(float level)
        {
            var volume = GetVolumeObject();
            volume.SetMasterVolumeLevelScalar(level, Guid.Empty);
        }

        public static float GetMasterVolume()
        {
            var volume = GetVolumeObject();
            volume.GetMasterVolumeLevelScalar(out float level);
            return level;
        }
    }
}
