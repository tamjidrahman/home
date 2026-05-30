import { authHeaders } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "https://api.basha.cloud";

export async function fetchDeviceStatus(type: string, names?: string[]) {
  const params = names?.length ? `?${type}=${names.join(",")}` : "";
  const res = await fetch(`${API_URL}/${type}/status${params}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`Failed to fetch ${type} status`);
  return res.json();
}

export async function invokeCommand(
  type: string,
  command: string,
  names?: string[],
  params: Record<string, string | number | boolean | string[]> = {}
) {
  const query = new URLSearchParams();

  // Add the device names (e.g., light=living_room,office)
  if (names?.length) {
    query.set(type, names.join(","));
  }

  // Array values become repeated query params (?rooms=A&rooms=B) for
  // FastAPI list[...] params; scalars stay as a single key=value.
  for (const [key, value] of Object.entries(params)) {
    if (Array.isArray(value)) {
      for (const v of value) query.append(key, String(v));
    } else {
      query.set(key, String(value));
    }
  }

  const res = await fetch(`${API_URL}/${type}/${command}?${query.toString()}`, {
    method: "POST",
    headers: authHeaders(),
  });

  if (!res.ok) throw new Error(`Failed to invoke ${command}`);
  return res.json();
}
export type CommandParam = {
  name: string
  type: "number" | "string" | "boolean"
  default: string | number | boolean | null
  choices?: string[]
  multi?: boolean
}

export type Command = {
  name: string
  params: CommandParam[]
}

export async function fetchDeviceCommands(type: string): Promise<Command[]> {
  const res = await fetch(`${API_URL}/${type}/commands`, {
    headers: authHeaders(),
  })
  if (!res.ok) return []
  return res.json()
}
