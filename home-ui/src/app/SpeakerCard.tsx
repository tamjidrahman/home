import { useState } from "react"
import { Volume2, VolumeX } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { invokeCommand } from "@/lib/api"

export function SpeakerCard({
  name,
  state,
  refresh,
}: {
  name: string
  state: any
  refresh: () => void
}) {
  const [isMuted, setIsMuted] = useState(state.is_muted)
  const [volume, setVolume] = useState(Math.round((state.volume ?? 0)))

  const handleVolumeChange = (value: number[]) => {
    const newVolume = value[0]
    setVolume(newVolume)
    invokeCommand("speaker", "volume_set", [name,], { "volume": newVolume }).finally(refresh)
  }

  return (
    <Card className="aspect-square flex flex-col justify-between p-4">
      <CardContent className="flex flex-col h-full justify-between">
        <div className="flex flex-col items-center gap-2">
          {!isMuted ? (
            <Volume2 className="w-10 h-10 text-green-500" />
          ) : (
            <VolumeX className="w-10 h-10 text-muted-foreground" />
          )}
          <div className="text-center font-medium capitalize text-sm">
            {name.replaceAll("_", " ")}
          </div>
        </div>
        <div className="flex flex-col gap-3 mt-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Mute</span>
            <Switch
              checked={isMuted}
              onCheckedChange={(checked) => {
                setIsMuted(checked)
                invokeCommand("speaker", checked ? "volume_mute" : "volume_unmute", [name]).finally(refresh)
              }}
            />
          </div>
          <div className="flex flex-col gap-1 text-sm">
            <span className="text-muted-foreground flex justify-between">
              <span>Volume</span>
              <span>{volume}%</span>
            </span>
            <Slider
              value={[volume]}
              min={0}
              max={100}
              step={1}
              onValueChange={handleVolumeChange}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
