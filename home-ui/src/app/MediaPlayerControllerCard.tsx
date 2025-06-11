import { useState } from "react"
import {
  Volume2, VolumeX,
  Play, Pause, SkipForward, SkipBack, StopCircle
} from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Button } from "@/components/ui/button"
import { invokeCommand } from "@/lib/api"

type SpeakerState = {
  is_muted: boolean
  volume: number
  image_url?: string
  media_title?: string
  media_artist?: string
  media_album_name?: string
  media_playlist?: string
}

export function MediaPlayerControllerCard({
  state,
  refresh,
}: {
  state: Record<string, SpeakerState>
  refresh: () => void
}) {
  const [localState, setLocalState] = useState(state)

  const handleMuteToggle = (name: string, checked: boolean) => {
    setLocalState(prev => ({
      ...prev,
      [name]: { ...prev[name], is_muted: checked }
    }))
    invokeCommand("speaker", checked ? "volume_mute" : "volume_unmute", [name])
      .finally(refresh)
  }

  const handleVolumeChange = (name: string, value: number[]) => {
    const newVolume = value[0]
    setLocalState(prev => ({
      ...prev,
      [name]: { ...prev[name], volume: newVolume }
    }))
    invokeCommand("speaker", "volume_set", [name], { volume: newVolume })
      .finally(refresh)
  }

  const handleTransport = (command: string) => {
    invokeCommand("speaker", command).finally(refresh)
  }

  const representative = Object.values(state).find(s => s.image_url || s.media_title)
  const {
    image_url,
    media_title,
    media_artist,
    media_album_name,
    media_playlist
  } = representative || {}

  return (
    <Card className="flex flex-col justify-between p-4">
      <CardContent className="flex flex-col gap-6 items-center">
        {image_url && (
          <img
            src={image_url}
            alt="Now playing"
            className="w-32 h-32 rounded-full object-cover shadow-md"
          />
        )}

        {(media_title || media_artist) && (
          <div className="text-center text-sm space-y-0.5">
            <div className="font-medium text-foreground">{media_title}</div>
            {media_artist && <div className="text-muted-foreground">{media_artist}</div>}
            {(media_album_name || media_playlist) && (
              <div className="text-muted-foreground text-xs italic">
                {media_album_name ?? media_playlist}
              </div>
            )}
          </div>
        )}

        <div className="flex items-center justify-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => handleTransport("previous")}>
            <SkipBack className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => handleTransport("play")}>
            <Play className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => handleTransport("pause")}>
            <Pause className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => handleTransport("stop")}>
            <StopCircle className="w-5 h-5" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => handleTransport("next")}>
            <SkipForward className="w-5 h-5" />
          </Button>
        </div>

        <div className="w-full space-y-4">
          {Object.entries(localState).map(([room, data]) => (
            <div key={room} className="flex flex-col gap-2">
              <div className="flex items-center justify-between text-sm font-medium capitalize">
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleMuteToggle(room, !data.is_muted)}
                    className="h-6 w-6 p-0"
                  >
                    {data.is_muted ? (
                      <VolumeX className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <Volume2 className="h-4 w-4 text-green-500" />
                    )}
                  </Button>
                  <span>{room.replaceAll("_", " ")}</span>
                </div>
                <span className="w-10 text-right text-muted-foreground">{data.volume}%</span>
              </div>
              <Slider
                value={[data.volume]}
                min={0}
                max={100}
                step={1}
                onValueChange={value => handleVolumeChange(room, value)}
              />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
