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
  const togglePower = () => {
    const newStatus = state.status === "on" ? "off" : "on"
    invokeCommand("light", newStatus, [name]).finally(refresh)
  }

  const toggleAuto = (checked: boolean) => {
    invokeCommand(
      "light",
      checked ? "enable_autolights" : "disable_autolights",
      [name]
    ).finally(refresh)
  }

  return (
    <Card className="aspect-square flex flex-col p-4">
      <CardContent className="flex flex-col items-center h-full gap-y-4 pt-4">
        <div className="flex flex-col items-center gap-2 cursor-pointer" onClick={togglePower}>
          {state.status === "on" ? (
            <Lightbulb className="w-10 h-10 text-yellow-500" />
          ) : (
            <LightbulbOff className="w-10 h-10 text-muted-foreground" />
          )}
          <div className="text-center font-medium capitalize text-sm">
            {name.replaceAll("_", " ")}
          </div>
        </div>

        <div className="flex items-center justify-between text-sm w-full px-1 mt-2">
          <span className="text-muted-foreground">Auto</span>
          <Switch
            checked={state.autolight_status === "on"}
            onCheckedChange={toggleAuto}
          />
        </div>
      </CardContent>
    </Card>
  )
}
