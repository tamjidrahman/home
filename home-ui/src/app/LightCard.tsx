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

  const togglePower = () => {
    const newStatus = localStatus === "on" ? "off" : "on"
    setLocalStatus(newStatus)
    invokeCommand("light", newStatus, [name]).finally(refresh)
  }

  return (
    <Card className="aspect-square flex flex-col">
      <CardContent className="flex flex-col items-center h-full pt-4">
        <div className="flex flex-col items-center gap-2 cursor-pointer" onClick={togglePower}>
          {localStatus === "on" ? (
            <Lightbulb className="w-10 h-10 text-yellow-500" />
          ) : (
            <LightbulbOff className="w-10 h-10 text-muted-foreground" />
          )}
          <div className="text-center font-medium capitalize text-sm">
            {name.replaceAll("_", " ")}
          </div>
        </div>

        <div className="flex items-center justify-between text-sm w-full px-1">
          <span className="text-muted-foreground">Auto</span>
          <Switch
            checked={localAuto === "on"}
            onCheckedChange={(checked) => {
              const newAuto = checked ? "on" : "off"
              setLocalAuto(newAuto)
              invokeCommand(
                "light",
                checked ? "enable_autolights" : "disable_autolights",
                [name]
              ).finally(refresh)
            }}
          />
        </div>
      </CardContent>
    </Card>
  )
}
