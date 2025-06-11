export async function fetchDeviceStatus(type: string, names?: string[]) {
  const params = names?.length ? `?${type}=${names.join(",")}` : "";
  const res = await fetch(`https://api.basha.cloud/${type}/status${params}`);
  if (!res.ok) throw new Error(`Failed to fetch ${type} status`);
  return res.json();
}

export async function invokeCommand(
  type: string,
  command: string,
  names?: string[],
  params: Record<string, string | number | boolean> = {}
) {
  const query = new URLSearchParams();

  // Add the device names (e.g., light=living_room,office)
  if (names?.length) {
    query.set(type, names.join(","));
  }

  // Add additional arbitrary params
  for (const [key, value] of Object.entries(params)) {
    query.set(key, String(value));
  }

  const res = await fetch(`https://api.basha.cloud/${type}/${command}?${query.toString()}`, {
    method: "POST",
  });

  if (!res.ok) throw new Error(`Failed to invoke ${command}`);
  return res.json();
}
export async function fetchDeviceCommands(type: string): Promise<string[]> {
  const res = await fetch(`https://api.basha.cloud/${type}/commands`)
  if (!res.ok) return []
  return res.json()
}
