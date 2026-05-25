
import { useState } from "react"
import { LightCard } from "./LightCard"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { invokeCommand, type Command } from "@/lib/api"
import { MediaPlayerControllerCard } from "./MediaPlayerControllerCard"

export function EntityTab({
  type,
  data,
  commands,
  refresh,
  showRaw,
}: {
  type: string
  data: Record<string, any>
  commands: Command[]
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
  if (type === "speaker") {
    return (
      <div className="max-w-xl mx-auto">
        <MediaPlayerControllerCard state={data} refresh={refresh} />
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
              {commands.filter(c => c.name !== "status").map(cmd => (
                <CommandControl
                  key={cmd.name}
                  type={type}
                  name={name}
                  command={cmd}
                  refresh={refresh}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

function CommandControl({
  type,
  name,
  command,
  refresh,
}: {
  type: string
  name: string
  command: Command
  refresh: () => void
}) {
  const [values, setValues] = useState<Record<string, string>>({})

  if (command.params.length === 0) {
    return (
      <Button
        variant="outline"
        onClick={() => invokeCommand(type, command.name, [name]).then(refresh)}
      >
        {command.name}
      </Button>
    )
  }

  const invoke = () => {
    const params: Record<string, string | number | boolean> = {}
    for (const p of command.params) {
      const raw = values[p.name] ?? (p.default != null ? String(p.default) : "")
      if (raw === "") continue
      if (p.type === "number") params[p.name] = Number(raw)
      else if (p.type === "boolean") params[p.name] = raw === "true"
      else params[p.name] = raw
    }
    invokeCommand(type, command.name, [name], params).then(refresh)
  }

  return (
    <div className="flex items-center gap-2 rounded border border-border px-2 py-1">
      <span className="text-sm">{command.name}</span>
      {command.params.map(p => (
        <input
          key={p.name}
          type={p.type === "number" ? "number" : "text"}
          placeholder={p.name + (p.default != null ? ` (${p.default})` : "")}
          value={values[p.name] ?? ""}
          onChange={e => setValues(prev => ({ ...prev, [p.name]: e.target.value }))}
          onKeyDown={e => e.key === "Enter" && invoke()}
          className="w-24 rounded border border-input bg-background px-2 py-1 text-sm"
        />
      ))}
      <Button variant="outline" size="sm" onClick={invoke}>go</Button>
    </div>
  )
}
