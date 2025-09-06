// File: MediaControlHelper.cs
using System;
using Windows.Media.Control;
using Windows.Media.Playback;
using System.Threading.Tasks;

namespace MediaControlHelper
{
    class Program
    {
        static async Task<int> Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Usage: MediaControlHelper.exe [playpause|next|prev]");
                return 1;
            }

            string command = args[0].ToLower();

            var sessions = await GlobalSystemMediaTransportControlsSessionManager.RequestAsync();
            var current = sessions.GetCurrentSession();

            if (current == null)
            {
                Console.WriteLine("No active media session.");
                return 1;
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

                default:
                    Console.WriteLine("Unknown command.");
                    return 1;
            }

            return 0;
        }
    }
}

