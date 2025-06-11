import { useState } from "react"
import { Lightbulb, LightbulbOff } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { invokeCommand } from "@/lib/api"

export function LightCard({
  name,
  state,
  refresh,
}: {
  name: string
  state: any
  refresh: () => void
}) {
  const [localStatus, setLocalStatus] = useState(state.status)
  const [localAuto, setLocalAuto] = useState(state.autolight_status)

  return (
    <Card className="aspect-square flex flex-col justify-between p-4">
      <CardContent className="flex flex-col h-full justify-between">
        <div className="flex flex-col items-center gap-2">
          {localStatus === "on" ? (
            <Lightbulb className="w-10 h-10 text-yellow-500" />
          ) : (
            <LightbulbOff className="w-10 h-10 text-muted-foreground" />
          )}
          <div className="text-center font-medium capitalize text-sm">
            {name.replaceAll("_", " ")}
          </div>
        </div>
        <div className="flex flex-col gap-2 mt-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Power</span>
            <Switch
              checked={localStatus === "on"}
              onCheckedChange={(checked) => {
                setLocalStatus(checked ? "on" : "off")
                invokeCommand("light", checked ? "on" : "off", [name]).finally(refresh)
              }}
            />
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Auto</span>
            <Switch
              checked={localAuto === "on"}
              onCheckedChange={(checked) => {
                setLocalAuto(checked ? "on" : "off")
                invokeCommand("light", checked ? "enable_autolights" : "disable_autolights", [name]).finally(refresh)
              }}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
