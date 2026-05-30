
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
  const [values, setValues] = useState<Record<string, string | string[]>>({})

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
    const params: Record<string, string | number | boolean | string[]> = {}
    for (const p of command.params) {
      const raw = values[p.name] ?? (p.default != null ? String(p.default) : "")
      if (p.choices && p.multi) {
        const selected = Array.isArray(raw) ? raw : []
        if (selected.length === 0) continue
        params[p.name] = selected
        continue
      }
      if (typeof raw !== "string" || raw === "") continue
      if (p.type === "number") params[p.name] = Number(raw)
      else if (p.type === "boolean") params[p.name] = raw === "true"
      else params[p.name] = raw
    }
    invokeCommand(type, command.name, [name], params).then(refresh)
  }

  const toggleChoice = (param: string, choice: string) => {
    setValues(prev => {
      const current = Array.isArray(prev[param]) ? (prev[param] as string[]) : []
      const next = current.includes(choice)
        ? current.filter(c => c !== choice)
        : [...current, choice]
      return { ...prev, [param]: next }
    })
  }

  const hasChoiceParam = command.params.some(p => p.choices && p.multi)

  // Choice params get their own row above the go button so the toggle
  // buttons don't visually mix with the action button.
  if (hasChoiceParam) {
    return (
      <div className="flex flex-col gap-2 rounded border border-border px-2 py-2">
        <span className="text-sm">{command.name}</span>
        {command.params.map(p => {
          if (p.choices && p.multi) {
            const selected = Array.isArray(values[p.name]) ? (values[p.name] as string[]) : []
            return (
              <div key={p.name} className="flex flex-wrap gap-1">
                {p.choices.map(choice => {
                  const isOn = selected.includes(choice)
                  return (
                    <Button
                      key={choice}
                      variant={isOn ? "default" : "outline"}
                      size="sm"
                      onClick={() => toggleChoice(p.name, choice)}
                    >
                      {choice}
                    </Button>
                  )
                })}
              </div>
            )
          }
          return (
            <input
              key={p.name}
              type={p.type === "number" ? "number" : "text"}
              placeholder={p.name + (p.default != null ? ` (${p.default})` : "")}
              value={typeof values[p.name] === "string" ? (values[p.name] as string) : ""}
              onChange={e => setValues(prev => ({ ...prev, [p.name]: e.target.value }))}
              onKeyDown={e => e.key === "Enter" && invoke()}
              className="w-24 rounded border border-input bg-background px-2 py-1 text-sm"
            />
          )
        })}
        <div className="flex justify-end">
          <Button variant="outline" size="sm" onClick={invoke}>go</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-wrap items-center gap-2 rounded border border-border px-2 py-1">
      <span className="text-sm">{command.name}</span>
      {command.params.map(p => (
        <input
          key={p.name}
          type={p.type === "number" ? "number" : "text"}
          placeholder={p.name + (p.default != null ? ` (${p.default})` : "")}
          value={typeof values[p.name] === "string" ? (values[p.name] as string) : ""}
          onChange={e => setValues(prev => ({ ...prev, [p.name]: e.target.value }))}
          onKeyDown={e => e.key === "Enter" && invoke()}
          className="w-24 rounded border border-input bg-background px-2 py-1 text-sm"
        />
      ))}
      <Button variant="outline" size="sm" onClick={invoke}>go</Button>
    </div>
  )
}
