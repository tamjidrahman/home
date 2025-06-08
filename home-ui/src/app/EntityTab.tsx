
import { LightCard } from "./LightCard"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { invokeCommand } from "@/lib/api"

export function EntityTab({
  type,
  data,
  commands,
  refresh,
  showRaw,
}: {
  type: string
  data: Record<string, any>
  commands: string[]
  refresh: () => void
  showRaw: boolean
}) {
  if (type === "light") {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {Object.entries(data).map(([name, state]) => (
          <LightCard key={name} name={name} state={state} refresh={() => refresh()} />
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {Object.entries(data).map(([name, state]) => (
        <Card key={name}>
          <CardContent className="p-4 space-y-2">
            <div className="font-medium capitalize">{name.replaceAll("_", " ")}</div>
            {showRaw ? (
              <pre className="text-xs text-muted-foreground">{JSON.stringify(state, null, 2)}</pre>
            ) : (
              <div className="text-sm text-muted-foreground">
                {Object.entries(state).map(([k, v]) => `${k}: ${v ?? "–"}`).join(", ")}
              </div>
            )}
            <div className="flex flex-wrap gap-2">
              {commands.filter(c => c !== "status").map(cmd => (
                <Button
                  key={cmd}
                  variant="outline"
                  onClick={() => invokeCommand(type, cmd, [name]).then(refresh)}
                >
                  {cmd}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
