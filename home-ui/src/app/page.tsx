"use client"

import { useEffect, useState } from "react"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Switch } from "@/components/ui/switch"
import { EntityTab } from "./EntityTab"
import { fetchDeviceStatus, fetchDeviceCommands } from "@/lib/api"

const entityTypes = ["light", "speaker", "thermostat", "vacuum", "door"]

export default function HomePage() {
  const [data, setData] = useState<Record<string, Record<string, any>>>({})
  const [commands, setCommands] = useState<Record<string, string[]>>({})
  const [showRaw, setShowRaw] = useState(false)

  useEffect(() => {
    fetchAll()
  }, [])

  const fetchAll = async () => {
    const results = await Promise.allSettled(entityTypes.map(fetchDeviceStatus))
    const commandsResults = await Promise.allSettled(entityTypes.map(fetchDeviceCommands))

    const combined: Record<string, any> = {}
    results.forEach((res, i) => {
      if (res.status === "fulfilled") combined[entityTypes[i]] = res.value
    })
    setData(combined)

    const cmdMap: Record<string, string[]> = {}
    commandsResults.forEach((res, i) => {
      if (res.status === "fulfilled") cmdMap[entityTypes[i]] = res.value
    })
    setCommands(cmdMap)
  }

  const refreshEntity = async (type: string) => {
    try {
      const result = await fetchDeviceStatus(type)
      setData(prev => ({ ...prev, [type]: result }))
    } catch (_) { }
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold tracking-tight">Home Control</h1>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          Raw JSON
          <Switch checked={showRaw} onCheckedChange={setShowRaw} />
        </div>
      </div>

      <Tabs defaultValue="light" className="w-full">
        <TabsList className="flex w-full overflow-x-auto">
          {entityTypes.map(type => (
            <TabsTrigger key={type} value={type} className="capitalize">
              {type}
            </TabsTrigger>
          ))}
        </TabsList>

        {entityTypes.map(type => (
          <TabsContent key={type} value={type} className="mt-6">
            <EntityTab
              type={type}
              data={data[type] ?? {}}
              commands={commands[type] ?? []}
              refresh={() => refreshEntity(type)}
              showRaw={showRaw}
            />
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}
