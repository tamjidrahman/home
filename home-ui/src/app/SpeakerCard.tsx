import { Volume2, VolumeX } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
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
  console.log(name, state)
  return (
    <Card className="aspect-square flex flex-col justify-between p-4">
      <CardContent className="flex flex-col h-full justify-between">
        <div className="flex flex-col items-center gap-2">
          {state.status === "playing" ? (
            <Volume2 className="w-10 h-10 text-green-500" />
          ) : (
            <VolumeX className="w-10 h-10 text-muted-foreground" />
          )}
          <div className="text-center font-medium capitalize text-sm">
            {name.replaceAll("_", " ")}
            {state.status}
          </div>
        </div>
        <div className="flex flex-col gap-2 mt-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Power</span>
            <Switch
              checked={state.status === "on"}
              onCheckedChange={(checked) =>
                invokeCommand("speaker", checked ? "on" : "off", [name]).then(refresh)
              }
            />
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Mute</span>
            <Switch
              checked={state.muted === true}
              onCheckedChange={(checked) =>
                invokeCommand("speaker", checked ? "mute" : "unmute", [name]).then(refresh)
              }
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
