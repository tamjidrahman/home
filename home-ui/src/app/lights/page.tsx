"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { fetchDeviceStatus, invokeCommand } from "@/lib/api"

export default function LightsPage() {
  const [status, setStatus] = useState<Record<string, any>>({})
  const [showRaw, setShowRaw] = useState(false)

  const refresh = () => {
    fetchDeviceStatus("light").then(setStatus).catch(console.error)
  }

  useEffect(() => {
    refresh()
  }, [])

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Lights</h1>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          Raw JSON
          <Switch checked={showRaw} onCheckedChange={setShowRaw} />
        </div>
      </div>

      {Object.entries(status).map(([name, state]) => (
        <Card key={name}>
          <CardContent className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 py-4">
            <div>
              <div className="font-semibold text-lg capitalize">{name.replaceAll("_", " ")}</div>
              {showRaw ? (
                <pre className="text-xs text-muted-foreground overflow-auto max-w-[90vw]">
                  {JSON.stringify(state, null, 2)}
                </pre>
              ) : (
                <div className="text-sm text-muted-foreground mt-1">
                  status: {state.status}, brightness: {state.brightness ?? "–"}, color temp: {state.color_temp ?? "–"}
                </div>
              )}
            </div>

            <div className="flex gap-2">
              <Button
                onClick={() => invokeCommand("light", "on", [name]).then(refresh)}
                className="w-16"
              >
                On
              </Button>
              <Button
                variant="outline"
                onClick={() => invokeCommand("light", "off", [name]).then(refresh)}
                className="w-16"
              >
                Off
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
